######################################################################
# Tables initialization handlers
######################################################################
from impala.dbapi import connect
import importlib
import logging
import os

models = importlib.import_module('.cfg', 'config').active_models
cfg = importlib.import_module('.cfg', 'config')


######################################################################
# Get list of active (allowed) table models
######################################################################
def init_models(mtype):
    tlist = []
    modules = {}
    tlist = models[mtype]
    if len(tlist) > 0:
        for mod in tlist:
            modules[mod] = importlib.import_module('.' + mod, 'models.' + mtype)
        return modules
    else:
        raise Exception('Tables type is incorrect!')


######################################################################
# Init tables
######################################################################
def init_tables(ttype):
    try:
        impala_con = connect(host=cfg.impala_host)
        impala_cur = impala_con.cursor()
        modules = init_models(ttype)
        for mod in modules:
            impala_cur.execute(modules[mod].model.get_int_schema(ttype))
            impala_cur.execute(modules[mod].model.get_ext_schema(ttype))
            logging.info(('Table %s has been successfully initialized!') % (mod))
        impala_cur.close()
        impala_con.close()
        return True
    except Exception as err:
        logging.error('Tables initialization failed!')
        logging.error(err)
        return False


######################################################################
# Show allowed models list
######################################################################
def show_tables(ttype):
    modules = init_models(ttype)
    for mod in modules:
        print
        modules[mod].model.get_int_schema(ttype)
        print
        '###################################################################################'
        print
        modules[mod].model.get_ext_schema(ttype)
        print
        '###################################################################################'


######################################################################
# Two step table loading process
# 1st step: HDFS -> External table
# 2nd step: External table -> Internal table
######################################################################
def load_tables(properties, t_init=True):
    if (not properties) or properties['f_type'] not in list(models.keys()):
        logging.error('Incorrect argument for tables loader!')
        return False

    modules = init_models(properties['f_type'])

    try:
        if t_init:
            if not init_tables(properties['f_type']): raise Exception('Failed in load_tables')
        impala_con = connect(host=cfg.impala_host)
        impala_cur = impala_con.cursor()
        for mod in models[properties['f_type']]:
            # if mod !='goods_services':
            #    continue
            # print mod
            table_name = modules[mod].model.get_table_name()
            # target_path = ('hdfs://nameservice1/ipv/results/%s/%s/data%s.tsv') % (properties['f_type'], mod, properties['proc_date'])
            # target_path = ('hdfs://master:8020/ipv/results/%s/%s/data%s.tsv') % (properties['f_type'], mod, properties['proc_date'])
            target_path = ('hdfs://192.168.250.30:8020/ipv/results/%s/%s/data%s.tsv') % (
                properties['f_type'], mod, properties['proc_date'])
            # print(target_path)
            #            target_path = ('/ipv/results/%s/%s/data%s.tsv') % (properties['f_type'], mod, properties['proc_date'])
            #            print target_path
            if properties['f_type'] in ['att', 'ad', 'ainf', 'phi']:
                insert_sql = ('UPSERT INTO TABLE `%s`.`%s` '
                              'SELECT * FROM `%s`.`%s`') % ('ipv_db', table_name, 'ipv_ext', table_name)
            elif properties['f_type'] == 'thist':
                insert_sql = ('UPSERT INTO TABLE `%s`.`%s` '
                              'SELECT app_id, record_date, code, description,'
                              'count(*) AS events_count, proc_date  FROM `%s`.`%s` '
                              'GROUP BY app_id, record_date, code, '
                              'description, proc_date') % ('ipv_db', table_name, 'ipv_ext', table_name)

            elif properties['f_type'] in ['ipa', 'ipg', 'pa', 'pg']:
                insert_sql = ('INSERT OVERWRITE TABLE `%s`.`%s` PARTITION (proc_date=\'%s\') '
                              'SELECT * FROM `%s`.`%s`') % ('ipv_db', table_name, properties['proc_date'],
                                                            'ipv_ext', table_name)
            elif properties['f_type'] in ['td']:
                # insert_sql = ('INSERT INTO TABLE `%s`.`%s` PARTITION (proc_date=\'%s\') '
                #              'SELECT * FROM `%s`.`%s`') % ('ipv_db', table_name, properties['proc_date'],
                #                                            'ipv_ext',table_name)
                insert_sql = ('INSERT INTO TABLE `%s`.`%s` '
                              'SELECT * FROM `%s`.`%s`') % ('ipv_db', table_name,
                                                            'ipv_ext', table_name)
            elif properties['f_type'] in ['fee_m']:
                insert_sql = ('INSERT OVERWRITE TABLE `%s`.`%s` PARTITION (year) '
                              'SELECT *, \'%s\', SUBSTR(app_filing_date,1,4)  FROM `%s`.`%s`') % ('ipv_db',
                                                                                                  table_name,
                                                                                                  properties[
                                                                                                      'proc_date'],
                                                                                                  'ipv_ext',
                                                                                                  table_name)
            elif properties['f_type'] in ['fee_d']:
                insert_sql = ('INSERT OVERWRITE TABLE `%s`.`%s` '
                              'SELECT * FROM `%s`.`%s`') % ('ipv_db', table_name, 'ipv_ext', table_name)

            load_sql = ('LOAD DATA INPATH \'%s\' OVERWRITE INTO TABLE `%s`.`%s`') % (target_path, 'ipv_ext', table_name)

            #            refresh = ('INVALIDATE METADATA `%s`.`%s`') % ('ipv_ext', table_name)
            #            impala_cur.execute(refresh)
            #            print load_sql
            #            print insert_sql
            # try:
            # 	impala_cur.execute(load_sql)
            # 	logging.info(('Data has been successfully loaded into temporary table: %s!') % (table_name))
            # except:
            #		continue
            impala_cur.execute(load_sql)
            logging.debug(('Data has been successfully loaded into temporary table: %s!') % (table_name))
            impala_cur.execute(insert_sql)
            logging.debug(('Data has been successfully loaded into HDFS table: %s!') % (table_name))
        impala_cur.close()
        impala_con.close()
        return True
    except Exception as err:
        logging.error('Tables loading failed!')
        logging.error(err)
        return False


def insert_new_proc_date_reports_status():
    report_names = cfg.report_names
    query = 'select max(proc_date) from ipv_db.ca_tm_trademark'
    impala_con = connect(host=cfg.impala_host)
    impala_cur = impala_con.cursor()

    impala_cur.execute(query)

    data = impala_cur.fetchall()
    if len(data) == 0:
        return
    proc_date = data[0][0]

    query = 'select distinct proc_date from etl_db.reports_status'
    impala_cur.execute(query)

    data = impala_cur.fetchall()
    proc_dates = [x[0] for x in data]

    if proc_date in proc_dates:
        logging.info('No new insertion. proc_date {} already exist'.format(proc_date))
        return

    logging.info('Making insertion for proc_date: {}'.format(proc_date))
    insert_query = "insert into etl_db.reports_status values "
    for i, report_name in enumerate(report_names):
        if i == (len(report_names) - 1):
            insert_query += "('{}', '{}', {});".format(proc_date, report_name, 0)
        else:
            insert_query += "('{}', '{}', {}),".format(proc_date, report_name, 0)
    # print(insert_query)
    impala_cur.execute(insert_query)
    logging.info('Successfully insertion for proc_date {}'.format(proc_date))

    impala_cur.close()
    impala_con.close()


def get_max_proc_date():
    query = 'select max(proc_date) from ipv_db.ca_tm_trademark'
    impala_con = connect(host=cfg.impala_host)
    impala_cur = impala_con.cursor()

    impala_cur.execute(query)
    data = impala_cur.fetchall()
    if len(data) == 0:
        return ''
    proc_date = data[0][0]

    return proc_date
