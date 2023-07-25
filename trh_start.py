#!/usr/bin/env python
#############################################################################
# IPV Transaction history API requester
# Author: Alex Kovalsky
#############################################################################
import sys
import time
import logging
import os
import pprint
import requests
import random
import json
from os import walk
import routines.dbs_handlers as dbs
import routines.tbl_handlers as tbl
import routines.wpr_handlers as parser
import routines.user_agents as ua
from multiprocessing.dummy import Pool
#from multiprocessing import Pool
from retrying import retry
from lxml import etree
from datetime import datetime
from datetime import timedelta
from impala.dbapi import connect
import importlib
from multiprocessing import Value, Array
from config import cfg
from routines.send_mail import send_mail

#############################################################################
# Write array of results to the local file
#############################################################################
def write_local(arr,name):
    res = ''
    for elm in arr:
        res += u"\t".join(elm).encode('utf-8').strip()+"\n"
    with open(name, 'w') as fl:
       fl.write(res)

#############################################################################
# Request TH API with retrying up to 60 sec.
#############################################################################
@retry(wait_exponential_multiplier=10, wait_exponential_max=5000, stop_max_delay=60000)
def get_data(app_id):
    try:
        headers = {'User-Agent': ua.custom_user_agent[random.randint(0,len(ua.custom_user_agent)-1)],
                   'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        #api_call = ('{\"searchText\":\"%s\",\"qf\":\"applId\"}') % (app_id) 
        api_call = ('{\"searchText\":\"applId:(%s)\",\"fl\":\"*\",\"qf\":\"applId\",\"facet\":\"false\"}') % (app_id)
        url = 'https://ped.uspto.gov/api/queries'
        response = requests.post(url, data=api_call, headers=headers, timeout = 15).text
        try:
            api_content = json.loads(response)
        except Exception:
            tree = etree.HTML(response)
            error = ('appID: %s, Error: %s') % (app_id, tree.xpath('.//body/h1')[0].text)
            raise Exception(error)

        stat = api_content['queryResults']['searchResponse']['response']['docs']
        res = []
        if stat:
            keys = ['appType', 'appStatus', 'appStatusDate', 'appAttrDockNumber', 'appCustNumber']
            res = [app_id]
            for k in keys: res.append(stat[0].get(k, '-'))

            thist = stat[0].get('transactions', [])
            pool = []
            if thist:
                keys = ['recordDate', 'code', 'description']
                for he in thist:
                    buf = []
                    for k in keys: buf.append(he.get(k, '-'))
                    pool.append(buf)
            else:
                st_data.no_thist = int(app_id)
            res.append(pool)
        else:
            st_data.no_info = int(app_id)

        return res
    except Exception as err:
        st_data.retries.value += 1
        raise Exception('Request failed'+str(err))

#############################################################################
# Wrap API reques process for using in multiprocessing pool
#############################################################################
def get_data_wrapper(app_id):
    try:
        return get_data(str(app_id))
    except Exception as err:
        st_data.failed_ids = int(app_id if app_id else 0)
        return []

#############################################################################
# Execute Impala query
#############################################################################
def run_query(query):
    #impala_con = connect(host='localhost')
    impala_con = connect(host=cfg.impala_host)
    impala_cur = impala_con.cursor()
    impala_cur.execute(query)
    result = impala_cur.fetchall()
    impala_cur.close()
    impala_con.close()
    return result

#############################################################################
# Get list of partitions starting from 35 days ago
#############################################################################
def get_partitions():
    start_date = str(datetime.now() - timedelta(days=35))[:10].replace('-','')

    sql = ('SELECT proc_date FROM '
           '(SELECT DISTINCT proc_date FROM `ipv_db`.grant_main '
           'WHERE proc_date >= \'%s\' '
           'UNION '
           'SELECT DISTINCT proc_date FROM `ipv_db`.application_main '
           'WHERE proc_date >= \'%s\') as t0 ORDER BY proc_date DESC') % (start_date, start_date)
    run_query(sql)
    return [ids[0] for ids in run_query(sql)]

#############################################################################
# Get application ids list from particular partition
#############################################################################
def get_ids(partition):

    sql = ('SELECT app_id FROM '
           '(SELECT DISTINCT app_id FROM `ipv_db`.grant_main '
           'WHERE proc_date = \'%s\' '
           'UNION '
           'SELECT DISTINCT app_id FROM `ipv_db`.application_main '
           'WHERE proc_date = \'%s\') as t0') % (partition, partition)

    return [ids[0] for ids in run_query(sql)]

#############################################################################
# Start multiprocessing pool
#############################################################################
def start_pool(ids):
    start = time.time()
    logging.info(('Numbers of appIds in partition: %s') % (str(len(ids))))
    pool = Pool(processes=10)
    results = pool.map(get_data_wrapper, ids)
    pool.close()
    pool.join()
    logging.info(('Ids processing completed %s sec') % (str(round(time.time()-start, 2))))
    return [res for res in results if res]

#############################################################################
# Split response to two separate data sets: common info and transactions
#############################################################################
def split_result(result, partition):
    info_pool = []
    trh_pool = []
    for elm in result:
        info_pool.extend([elm[:6] + [partition]])
        for tr in elm[-1]:
            trh_pool.extend([[elm[0]] + tr + [partition]])
    info_res = ''
    trh_res = ''

    for elm in info_pool: info_res += u"\t".join(elm).encode('utf-8').strip()+"\n"
    for elm in trh_pool: trh_res += u"\t".join(elm).encode('utf-8').strip()+"\n"

    return {
        'ainf': info_res,
        'thist': trh_res,
        'ainf_len': len(info_pool),
        'thist_len': len(trh_pool)
        }

#############################################################################
# Get year to process depend on host IP address
#############################################################################
def get_tasks():
    tasks = {'192.168.250.11' :['2006','2007'],
             '192.168.250.12' :['2008','2009'],
             '192.168.250.13' :['2010','2011'],
             '192.168.250.15' :['2012','2013'],
             '192.168.250.16' :['2014','2015'],
             '192.168.250.17' :['2016',],
             '192.168.250.19' :['2017',],
             '192.168.250.20' :['2018',],
            }
    return tasks.get(socket.gethostbyname(socket.gethostname()))

#############################################################################
# Get credential for EMail notification
#############################################################################
def get_mail_params(rfile):
    with open(rfile, 'r') as fl:
        text = fl.readlines()
        text = ''.join(text)

    mail_params =  cfg.mail_params

    var_params  = {
        'text'     : text,
        'subject'  : 'Transaction history downloader report'
        }

    mail_params.update(var_params)

    return mail_params

#############################################################################
# Thread safe data struct for store statistic info from different processes
#############################################################################
class Stat:
    def __init__(self):
        self.__dict__['stat'] = {
            'failed_ids': { 'lst': Array('i',20000), 'idx': Value('i',0)},
            'no_info'   : { 'lst': Array('i',20000), 'idx': Value('i',0)},
            'no_thist'  : { 'lst': Array('i',20000), 'idx': Value('i',0)}
            }
        self.__dict__['retries'] = Value('i',0)

    def __setattr__(self, name, value):
        if name != 'retries':
           self.__dict__['stat'][name]['lst'][self.__dict__['stat'][name]['idx'].value] = value
           self.__dict__['stat'][name]['idx'].value += 1

    def __getattr__(self, name):
        if name != 'retries':
            return [[str(elm)] for elm in self.__dict__['stat'][name]['lst'] if elm > 0]



#############################################################################
if __name__ == "__main__":

    #tbl.init_tables(args.type)
    t = time.time()

    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)


    log_file_name = ('./log/tr_history_%s.log') % (str(datetime.now())[2:19].replace(' ','_'))

    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s',
                        level=logging.INFO)

    logFormatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler(log_file_name)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    parser.set_env()
    i = 0
    properties = {'proc_date': str(datetime.now())[:10].replace('-','')}

    cfg = importlib.import_module('.cfg', 'config')
    models = cfg.active_models

    models = {key: models[key] for key in ['thist','ainf']}

    for partition in get_partitions():
        st_data = Stat()
        start = time.time()
        logging.info(('Start processing partition: %s') % (partition))

        ids = get_ids(partition)
        final = split_result(start_pool(ids), partition)
        
        

        hdfs_conn = parser.hdfs_connect()
        for model in models:
            for table in models[model]:
                parser.write_hdfs(hdfs_conn,
                                  properties['proc_date'],
                                  model, table, final[model])

            properties['f_type'] = model
            parser.set_impala_permissions(cfg.hdfs_base_dir)
            tbl.load_tables(properties)
        hdfs_conn.close()
        logging.info(('STAT: Partition                =  %s') % (partition))
        logging.info(('STAT: Total Ids in partition   =  %s') % (str(len(ids))))
        logging.info(('STAT: Total Ids extracted      =  %s') % (str(final['ainf_len'])))
        logging.info(('STAT: Total tr.history records =  %s') % (str(final['thist_len'])))
        logging.info(('STAT: Numbers of retries       =  %s') % (str(st_data.retries.value)))
        logging.info(('STAT: Failed Ids numbers       =  %s') % (str(len(st_data.failed_ids))))
        logging.info(('STAT: Ids with no app.info     =  %s') % (str(len(st_data.no_info))))
        logging.info(('STAT: Ids with no tr.history   =  %s') % (str(len(st_data.no_thist))))
        logging.info(('STAT: Average req/sec. rate    =  %s') % (str(round(len(ids)/(time.time()-start), 2))))

        res_path = './log/thist/'
        marker = str(int(time.time()))
        logarr = {
            'failed_ids': st_data.failed_ids,
            'no_info': st_data.no_info,
            'no_thist': st_data.no_thist
            }
        for elm in logarr:
            name = ('%s%s_%s.txt1') % (res_path, elm, partition)
            write_local(logarr[elm], name)


        logging.info(('Partition processing completed in %s sec') % (str(round(time.time()-start, 2))))
    logging.info(('Overall processing time: %s sec') % (str(round(time.time()-t, 2))))

    ##send_mail(get_mail_params(log_file_name))

