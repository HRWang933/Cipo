######################################################################
# Working DataBases initialization
######################################################################
from impala.dbapi import connect 
import logging
import importlib

cfg = importlib.import_module('.cfg', 'config')
def init_dbs():
    create_command = 'CREATE DATABASE IF NOT EXISTS '
    dbs = ['ipv_db', 'ipv_ext']

    try:
        impala_con = connect(host=cfg.impala_host)
        #impala_con = connect(host='localhost')
        impala_cur = impala_con.cursor()
        for db in dbs: impala_cur.execute(create_command + db)
        impala_cur.close()
        impala_con.close() 
        logging.info("DB successfully initialized!")
        return True
    except Exception as err:
        print(err)
        logging.error("DB Init failed!")
        logging.error("DB Init failed!")
        return False
