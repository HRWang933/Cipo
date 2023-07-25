#!/usr/bin/env python
#############################################################################
#
#############################################################################
import time
import logging
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.chrome.options import Options
import routines.tbl_handlers as tbl
import routines.wpr_handlers as parser
import routines.user_agents as ua
from multiprocessing import Manager, Process
from retrying import retry
from datetime import datetime
from datetime import timedelta
from impala.dbapi import connect
import importlib
from multiprocessing import Value, Array
from config import cfg
from routines.send_mail import send_mail
import re
import socket
import traceback

#############################################################################
#
#############################################################################
def write_local(arr,name):
    res = ''
    for elm in arr:
        res += u"\t".join(elm).encode('utf-8').strip()+"\n"
    with open(name, 'w') as fl:
       fl.write(res)


#############################################################################
#
#############################################################################
def run_query(query):
    impala_con = connect(host='localhost')
    impala_cur = impala_con.cursor()
    impala_cur.execute(query)
    result = impala_cur.fetchall()
    impala_cur.close()
    impala_con.close()
    return result

#############################################################################
#
#############################################################################
def get_partitions(years):
#    years = ','.join(map(lambda arg: '\''+arg+'\'', years))

    start_date = str(datetime.now() - timedelta(days=35))[:10].replace('-','')

    sql = ('SELECT t0.proc_date, count(*) AS nmb FROM `ipv_db`.grant_main t0 '
           'LEFT OUTER JOIN `ipv_db`.ph_info t1 '
           'ON t0.app_id = t1.app_id and t0.pub_ref_doc_number = t1.patent_no '
           'WHERE t1.app_id IS NULL and t1.patent_no IS NULL AND t0.proc_date >= \'%s\' '
           'GROUP BY t0.proc_date HAVING nmb >= 1 ORDER BY t0.proc_date DESC ') % (start_date)

#    sql = ('SELECT t0.proc_date, count(*) AS nmb FROM `ipv_db`.grant_main t0 '
#           'LEFT OUTER JOIN `ipv_db`.ph_info t1 '
#           'ON t0.app_id = t1.app_id and t0.pub_ref_doc_number = t1.patent_no '
#           'WHERE t1.app_id IS NULL and t1.patent_no IS NULL AND SUBSTR(t0.proc_date,1,4) IN (%s) '
#           'GROUP BY t0.proc_date HAVING nmb >= 1 ORDER BY t0.proc_date DESC ') % (years)
#           'ORDER BY t0.proc_date DESC LIMIT 1') % (years)

    return [ids[0] for ids in run_query(sql)]

#############################################################################
#
#############################################################################
def get_ids(partition):

    sql = ('SELECT DISTINCT t0.app_id, t0.pub_ref_doc_number FROM `ipv_db`.grant_main t0 '
           'LEFT OUTER JOIN `ipv_db`.ph_info t1 '
           'ON t0.app_id = t1.app_id and t0.pub_ref_doc_number = t1.patent_no '
           'WHERE t1.app_id IS NULL and t1.patent_no '
           'IS NULL AND t0.proc_date = \'%s\'') % (partition)
#           'IS NULL AND t0.proc_date = \'%s\' LIMIT 5') % (partition)

    return [list(ids) for ids in run_query(sql)]

#############################################################################
#
#############################################################################
def split_result(result, partition):
    phi_res = ''
    for elm in result: 
        if elm and len(elm) == 6:
            phi_res += u"\t".join(elm).encode('utf-8').strip()+"\n"
        else:
            st_data.inconsist = int(elm[0] if elm else 0)
    return {
        'phi': phi_res,
        'phi_len': len(result)
        }

#############################################################################
#
#############################################################################
def get_tasks():
    tasks = {'192.168.250.11' :['2001', '2002'],
             '192.168.250.12' :['2016', '2015'],
             '192.168.250.13' :['2010', '2011'],
             '192.168.250.15' :['2012', '2013'],
             '192.168.250.16' :['2014', '2015'],
             '192.168.250.17' :['2016',],
             '192.168.250.19' :['2006',],
             '192.168.250.20' :['2006','2007'],
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
        'subject'  : 'Patent holder crawler report'
        }

    mail_params.update(var_params)

    return mail_params

#############################################################################
#
#############################################################################
class Stat:
    def __init__(self, size):
        self.__dict__['stat'] = {
            'failed_ids': { 'lst': Array('i', size), 'idx': Value('i',0)},
            'inconsist' : { 'lst': Array('i', size), 'idx': Value('i',0)},
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
#
#############################################################################
class wait_for_non_empty_text(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            element_text = EC._find_element(driver, self.locator).text.strip()
            return element_text != ''
        except Exception:
            return False

#############################################################################
#
#############################################################################
class Browser:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
#        chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
        chrome_options.add_argument(('user-agent=%s') % (ua.get_user_agent()))
        self.driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options,
                                  service_args=['--verbose', '--log-path=./log/chromedriver.log'])
        self.driver.set_window_size(1024, 1024)

    @retry(wait_exponential_multiplier=10, wait_exponential_max=5000, stop_max_delay=10000)
    def get_data(self, arg):
        try:
            app_id = str(arg[0])
            if len(app_id) > 8: return False
            else:
                app_id = '0' * (8-len(app_id)) + app_id

            patent_no = arg[1]
            st_check = re.match(r'^[A-Z]{1,}', arg[1])

            if st_check:
                st_check = st_check.group(0)
                patent_no = st_check + patent_no[len(st_check) + 1:]
            elif patent_no.startswith('0'):
                 patent_no = patent_no[1:]

            target_link = ('https://fees.uspto.gov/MaintenanceFees/fees/details?'
                           'applicationNumber=%s&patentNumber=%s') % (app_id, patent_no)

#            logging.info(('Request started for APP_ID: %s PATENT_NO: %s') % (arg[0], arg[1]))

            self.driver.get(target_link)
            wait = WebDriverWait(self.driver, 5)
            wait.until(wait_for_non_empty_text((By.XPATH, '//span[@data-dojo-attach-point="address"]')))

            res = [str(arg[0]), arg[1]]
            res.append(self.driver.find_element_by_xpath('//span[@data-dojo-attach-point="customerNumber"]').text)
            res.append(self.driver.find_element_by_xpath('//span[@data-dojo-attach-point="entityStatus"]').text)
            res.append(self.driver.find_element_by_xpath('//span[@data-dojo-attach-point="phone"]').text)
            address = self.driver.find_element_by_xpath('//span[@data-dojo-attach-point="address"]').text
            address = address.replace('\n', ' ')
            res.append(address)
            return res

        except Exception as err:
            st_data.retries.value += 1
            raise Exception(('Request failed for APP_ID: %s PATENT_NO: %s') % (arg[0], arg[1]))

    def get_data_wrapper(self, arg):
        try:
            return self.get_data(arg)
        except Exception as err:
            logging.error(err)
            st_data.failed_ids = int(arg[0] if arg[0] else 0)
            return []

    def shutdown(self):
        self.driver.quit()

#############################################################################
#
#############################################################################
class Worker(Process):
    def __init__(self, worker_num, task_q, result_q):
        super(Worker, self).__init__()
        self.worker_num = worker_num
        self.task_q = task_q
        self.result_q = result_q
        self.scraper = Browser() 

    def handle_work(self, work):
        result = self.scraper.get_data_wrapper(work)
        self.result_q.put(result)

    def run(self):
        try:
            while True:
                work = self.task_q.get()
                if work == 'KILL':
                    self.scraper.shutdown()
                    break
                self.handle_work(work)
        except Exception:
            logging.error(traceback.format_exc())
            raise

#############################################################################
#
#############################################################################
def start_queue(ids):
    start = time.time()
    logging.info(('Numbers of records in partition: %s') % (str(len(ids))))

    num_workers = 10

    manager = Manager()
    task_q = manager.Queue()
    result_q = manager.Queue()

    workers = []
    for worker_num in range(num_workers):
        worker = Worker(worker_num, task_q, result_q)
        worker.start()
        workers.append(worker)

    for task in ids:
        task_q.put(task)

    results = []
    while len(results) < len(ids):
        results.append(result_q.get())

    for worker in workers: task_q.put("KILL")

    for worker in workers: worker.join()

    logging.info(('Ids processing completed %s sec') % (str(round(time.time()-start, 2))))
    return [res for res in results if res]

#############################################################################
if __name__ == "__main__":
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

    properties = {'proc_date': str(datetime.now())[:10].replace('-','')}

    cfg = importlib.import_module('.cfg', 'config')

    models = cfg.active_models

    models = {key: models[key] for key in ['phi']}

#    for model in models:
#        tbl.init_tables(model)

    for partition in get_partitions(get_tasks()):

        start = time.time()
        logging.info(('Start processing partition: %s') % (partition))

        ids = get_ids(partition)

        st_data = Stat(len(ids))

        final = split_result(start_queue(ids), partition)
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
        logging.info(('STAT: Partition                  =  %s') % (partition))
        logging.info(('STAT: Total records in partition =  %s') % (str(len(ids))))
        logging.info(('STAT: Total records extracted    =  %s') % (str(final['phi_len'])))
        logging.info(('STAT: Numbers of retries         =  %s') % (str(st_data.retries.value)))
        logging.info(('STAT: Failed records numbers     =  %s') % (str(len(st_data.failed_ids))))
        logging.info(('STAT: Inconsistent records       =  %s') % (str(len(st_data.inconsist))))
        logging.info(('STAT: Average req/sec. rate      =  %s') % (str(round(len(ids)/(time.time()-start), 2))))

        res_path = './log/phi/'
        marker = str(int(time.time()))
        logarr = {
            'failed_ids': st_data.failed_ids,
            'inconsist': st_data.inconsist,
            }
        for elm in logarr:
            name = ('%s%s_%s.log') % (res_path, elm, partition)
            write_local(logarr[elm], name)


        logging.info(('Partition processing completed in %s sec') % (str(round(time.time()-start, 2))))
    logging.info(('Overall processing time: %s sec') % (str(round(time.time()-t, 2))))

    send_mail(get_mail_params(log_file_name))

