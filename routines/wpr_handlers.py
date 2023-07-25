#############################################################################
# Misc. parser handlers
#############################################################################
from multiprocessing import Pool,cpu_count
import xml_splitter as splitter
import importlib
import logging
import os
import re
import time
import pyarrow as pa
import subprocess
from subprocess import PIPE
import hashlib
from datetime import datetime

cfg = importlib.import_module('.cfg', 'config')

#############################################################################
# Get list of allowed parser models
#############################################################################
def init_parsers(f_type):
    modules = {}

    parsers = cfg.active_parsers

    for mod in parsers[f_type]: modules[mod] = importlib.import_module('.' + mod, 'parsers.'+f_type)
    return modules

#############################################################################
# Set JAVE env variables
#############################################################################
def set_env():
    # libhdfs.so path
    cmd = ["locate", "-l", "1", "libhdfs.so"]
    libhdfsso_path = subprocess.check_output(cmd).strip()
    os.environ["ARROW_LIBHDFS_DIR"] = os.path.dirname(libhdfsso_path)

    # JAVA_HOME path
    os.environ["JAVA_HOME"] = '/usr/lib/jvm/java-8-oracle-cloudera'

    # classpath
    cmd = ["/usr/bin/hadoop", "classpath", "--glob"]
    hadoop_cp = subprocess.check_output(cmd).strip()

    if "CLASSPATH" in os.environ:
        os.environ["CLASSPATH"] = os.environ["CLASSPATH"] + ":" + hadoop_cp
    else:
        os.environ["CLASSPATH"] = hadoop_cp

#############################################################################
# Set required permission to HDFS path
# It should be done for using HDFS file as Impala table source
#############################################################################
def set_impala_permissions(base_dir):
    try:
        logging.debug('Changing HDFS files permissions')
        cmd = ["sudo", "-u", "hdfs", "hdfs", "dfs", "-chown", "-R", "impala:supergroup", base_dir]
        subprocess.Popen(cmd, stdout=PIPE)
        cmd = ["sudo", "-u", "hdfs", "hdfs", "dfs", "-chmod", "-R", "777", base_dir]
        subprocess.Popen(cmd, stdout=PIPE)
    except Exception as err:
        logging.error('Can\'t change HDFS files permissions!')
        logging.error(err)

#############################################################################
# Get required information from file name
#############################################################################
def parse_file_name(file_name):
    name_templates = {'att'  : {'template':'WebRoster.txt', 'prefix': '' , 'reg': None},
                      'fee_m': {'template':'MaintFeeEvents_','prefix': '', 'reg': '([0-9]{8})'},
                      'fee_d': {'template':'MaintFeeEventsDesc_','prefix': '', 'reg': '([0-9]{8})'},
                      'ad'   : {'template':'ad', 'prefix': '', 'reg': '([0-9]{8})'},
                      'ipa'  : {'template':'ipa','prefix': '20', 'reg': '([0-9]{6})'},
                      'ipg'  : {'template':'ipg','prefix': '20', 'reg': '([0-9]{6})'},
                      'pg'   : {'template':'pg','prefix': '20', 'reg': '([0-9]{6})'},
                      'pa'   : {'template':'pa','prefix': '20', 'reg': '([0-9]{6})'},
                     }
    result = {}

    result['f_type'] = False
    for ftype in name_templates:
        if file_name.startswith(name_templates[ftype]['template']):
            result['f_type'] = ftype
            break

    if result['f_type'] not in list(cfg.active_parsers.keys()):
        raise Exception(('Incorrect file type for File parser <%s>') % (file_name))

    if name_templates[result['f_type']]['reg']:
        result['proc_date'] = name_templates[result['f_type']]['prefix'] + \
                              re.search(name_templates[result['f_type']]['reg'], file_name).group(0)
    else: result['proc_date'] = str(datetime.now())[:10].replace('-','')


    if len(result['proc_date']) != 8:
        raise Exception(('Incorrect date extracted from <%s>') % (file_name))

    return result

#############################################################################
# Get HDFS connector
#############################################################################
def hdfs_connect():
    #return pa.hdfs.connect("192.168.250.15", 8020, user='hdfs', driver='libhdfs')
    #return pa.hdfs.connect("161.35.109.221", 8020, user='root', driver='libhdfs')
    #return pa.hdfs.connect("10.116.0.5", 8020, user='hdfs', driver='libhdfs')
    return pa.hdfs.connect("192.168.250.30", 8020, user='hdfs', driver='libhdfs')

#############################################################################
# Parsing XML files for td type
#############################################################################
def parse_xml2(*args):
    file_name = args[0]
    f_prop = args[1]
    modules = args[2]
    short_name = os.path.basename(file_name[0])
    start = time.time()
    fstart = start
    hdfs = hdfs_connect()
    #if f_prop['f_type']!='td':
    #	xml = splitter.extract_xml_parts(file_name)
    #else:
    #    xml = []
    #    res = []
    #    f = open(file_name, "r")
    #    for line in f:
    #        res.append(line)
    #    xml.append("".join(res))

    #logging.info(('XML file %s has been splitted in %s sec. and contains %s DTDs') % (short_name,
    #                                                                                  str(round(time.time()-start, 2)),
    #                                                                                  len(xml)))
    #file_name_l = [file_name]
    for mod in modules:
        #if mod !='goods_services':
        #    continue
        #print mod
        start = time.time()
        results = []

#        for part in xml:
#            print "##############################################################"
#            part = part.replace('&',' ')
#            try:
#            results.append(modules[mod].create_line(part))
#            except Exception as err:
#                print part
#                print err

        pool = Pool(processes = 5, maxtasksperchild=1000)
        results = pool.map(modules[mod].create_line, file_name)

        pool.close()
        pool.join()

        results = [res for res in results if res]
	#print(results)
        logging.debug(('Parser <%s> has been done in %s sec.') % (mod, str(round(time.time()-start, 2))))
        logging.debug(('Output file contains %s elements') % (len(results)))

        proc_date =  f_prop['proc_date']
	#if len(results) != 0:
       	write_hdfs(hdfs, proc_date, f_prop['f_type'], mod, results)
    hdfs.close()
    set_impala_permissions(cfg.hdfs_base_dir)
    logging.debug(('XML file %s has been fully processed in %s sec.') % (short_name, str(round(time.time()-fstart, 2))))

#############################################################################
# Parsing XML files
#############################################################################
def parse_xml(*args):
    file_name = args[0]
    f_prop = args[1]
    modules = args[2]
    short_name = os.path.basename(file_name)
    start = time.time()
    fstart = start
    hdfs = hdfs_connect()
    xml = splitter.extract_xml_parts(file_name)

    logging.info(('XML file %s has been splitted in %s sec. and contains %s DTDs') % (short_name,
                                                                                      str(round(time.time()-start, 2)),
                                                                                      len(xml)))
    for mod in modules:
        start = time.time()
        results = []

#        for part in xml:
#            print "##############################################################"
#            part = part.replace('&',' ')
#            try:
#            results.append(modules[mod].create_line(part))
#            except Exception as err:
#                print part
#                print err

        pool = Pool(processes = 5, maxtasksperchild=1000)
        results = pool.map(modules[mod].create_line, xml)

        pool.close()
        pool.join()

        results = [res for res in results if res]
        logging.info(('Parser <%s> has been done in %s sec.') % (mod, str(round(time.time()-start, 2))))
        logging.info(('Output file contains %s elements') % (len(results)))

        proc_date =  f_prop['proc_date']
       	write_hdfs(hdfs, proc_date, f_prop['f_type'], mod, results)
    hdfs.close()
    set_impala_permissions(cfg.hdfs_base_dir)
    logging.info(('XML file %s has been fully processed in %s sec.') % (short_name, str(round(time.time()-fstart, 2))))

#############################################################################
# 
#############################################################################
def parse_txt(*args):
    hdfs_path = ('%s/results/%s/%s/data%s.tsv') % (cfg.hdfs_base_dir, args[1]['f_type'],'fee_main', args[1]['proc_date'])
    local_to_hdfs(args[0], hdfs_path)

#############################################################################
# Parser wrapper for Canada Trademark Data
#############################################################################
def parse2(file_name):
    if not file_name:
        logging.error(('Incorrect argument for File parser') % (file_name))
        return False

    try:
    #    short_name = os.path.basename(file_name)
    #   
    #    if file_name.rsplit('/',2)[-2] !='td':
    #        f_prop = parse_file_name(short_name)
    #    else:
    #        f_prop = {'f_type':'td','proc_date':short_name.split('.')[0]}
        short_name = os.path.basename(file_name[0])
        proc_date = short_name.split('_')[0]
        f_prop = {'f_type':'td','proc_date':proc_date}
            

        modules = init_parsers(f_prop['f_type'])
        #logging.info(('Start processing %s file') % (short_name))
        #logging.info(('proc_date is %s') % (proc_date))

        workers = {'att'  : [parse_att, (file_name, f_prop)],
                   'fee_m': [parse_txt, (file_name, f_prop)],
                   'fee_d': [parse_fee_d, (file_name, f_prop)],
                   'ad'   : [parse_xml, (file_name, f_prop, modules)],
                   'ipa'  : [parse_xml, (file_name, f_prop, modules)],
                   'ipg'  : [parse_xml, (file_name, f_prop, modules)],
                   'pg'   : [parse_xml, (file_name, f_prop, modules)],
                   'pa'   : [parse_xml, (file_name, f_prop, modules)],
                   'td'   : [parse_xml2, (file_name, f_prop, modules)]
                  }

        workers[f_prop['f_type']][0](*workers[f_prop['f_type']][1])

        return f_prop
    except Exception as err:
        logging.error(('XML files %s processing failed!') % (file_name))
        logging.error(err)
        return False

#############################################################################
# Parser wrapper
#############################################################################
def parse(file_name):
    if not file_name:
        logging.error(('Incorrect argument for File parser') % (file_name))
        return False

    try:
        short_name = os.path.basename(file_name)
        f_prop = parse_file_name(short_name)

        modules = init_parsers(f_prop['f_type'])
        logging.info(('Start processing %s file') % (short_name))

        workers = {'att'  : [parse_att, (file_name, f_prop)],
                   'fee_m': [parse_txt, (file_name, f_prop)],
                   'fee_d': [parse_fee_d, (file_name, f_prop)],
                   'ad'   : [parse_xml, (file_name, f_prop, modules)],
                   'ipa'  : [parse_xml, (file_name, f_prop, modules)],
                   'ipg'  : [parse_xml, (file_name, f_prop, modules)],
                   'pg'   : [parse_xml, (file_name, f_prop, modules)],
                   'pa'   : [parse_xml, (file_name, f_prop, modules)]
                  }

        workers[f_prop['f_type']][0](*workers[f_prop['f_type']][1])

        return f_prop
    except Exception as err:
        logging.error(('XML file %s processing failed!') % (short_name))
        logging.error(err)
        return False

#############################################################################
# Parse Attorney text file
#############################################################################
def parse_att(*args):
    file_name = args[0]
    f_prop = args[1]
    if not file_name:
        logging.error(('Incorrect file name') % (file_name))
        return False
    short_name = os.path.basename(file_name)
    updated = str(datetime.now())[:10].replace('-','')
    try:
        start = time.time()
        fstart = start
        with open(file_name, 'rb') as in_file:
            lines = in_file.readlines()
        content = []

        for line in lines:
            elm_list = line.strip().split('","')
            if len(elm_list) > 0:
                elm_list[0] = elm_list[0][1:]
                elm_list[-1] = elm_list[-1][:-1]+'\n'
                pk = hashlib.md5(''.join(elm_list[0:4])).hexdigest()
                elm_list.insert(0,updated)
                elm_list.insert(0,pk)
                content.append('\t'.join(elm_list))

        hdfs = hdfs_connect()

        hdfs_name = ('%s/results/att/attorney/data%s.tsv') % (cfg.hdfs_base_dir, f_prop['proc_date'])

        of = hdfs.open(hdfs_name, "wb")
        of.write("".join(content))
        of.close()

        logging.info(('File <%s> has been successfully copied to HDFS') % (short_name))

        hdfs.close()
        set_impala_permissions(cfg.hdfs_base_dir)
        return hdfs_name
    except Exception as err:
        logging.error(('Failed to copy <%s> to HDFS!') % (short_name))
        logging.error(err)
        return False

#############################################################################
# Parsing transaction fee description file
#############################################################################
def parse_fee_d(*args):
    file_name = args[0]
    f_prop = args[1]
    if not file_name:
        logging.error(('Incorrect file name') % (file_name))
        return False
    short_name = os.path.basename(file_name)
    updated = f_prop['proc_date']
    try:
        start = time.time()
        fstart = start
        with open(file_name, 'rb') as in_file:
            lines = in_file.readlines()
        content = []

        for line in lines:
            elm = line.strip()
            if len(elm) > 0:
                content.append(elm[:5].strip()+'\t'+elm[6:].strip()+'\n')

        content.append('FDFDF\t'+updated+'\n')
        hdfs = hdfs_connect()

        hdfs_name = ('%s/results/fee_d/fee_descr/data%s.tsv') % (cfg.hdfs_base_dir, f_prop['proc_date'])

        of = hdfs.open(hdfs_name, "wb")
        of.write("".join(content))
        of.close()

        logging.info(('File <%s> has been successfully copied to HDFS') % (short_name))

        hdfs.close()
        set_impala_permissions(cfg.hdfs_base_dir)
        return hdfs_name
    except Exception as err:
        logging.error(('Failed to copy <%s> to HDFS!') % (short_name))
        logging.error(err)
        return False

#############################################################################
# Copy file from local to HDFS
#############################################################################
def local_to_hdfs(local_file, hdfs_path):
    hdfs_dir = '/'.join(hdfs_path.split('/')[:-1])
    cmds = [["hdfs", "dfs", "-mkdir", "-p", hdfs_dir],
            ["hdfs", "dfs", "-copyFromLocal", "-f", local_file, hdfs_path]]

    for cmd in cmds:
        result = subprocess.check_output(cmd).strip()
        if len(result) > 0: raise Exception(result)

    set_impala_permissions(cfg.hdfs_base_dir)
    return True

#############################################################################
# Write content to the local file
#############################################################################
def write_result(proc_date, modul, results):
    try:
        file_name = os.getcwd() + '/results/' + modul + '/data' + proc_date +'.tsv'
        with open(file_name, "w") as of:
            of.write("".join(results))

        logging.debug(('Data for <%s> parser has been successfully written') % (modul))
    except Exception as err:
        logging.error(('Failed when writing results for <%s> parser') % (modul))
        logging.error(err)

#############################################################################
# Write content to the HDFS file
#############################################################################
def write_hdfs(hdfs, proc_date, ftype, modul, results):
    try:
        file_name = ('%s/results/%s/%s/data%s.tsv') % (cfg.hdfs_base_dir, ftype, modul, proc_date)
        of = hdfs.open(file_name, "wb")
        of.write("".join(results))
        of.close()
        logging.debug(('Data for <%s> parser has been successfully written') % (modul))
        return file_name
    except Exception as err:
        logging.error(('Failed when writing results for <%s> parser') % (modul))
        logging.error(err)
        return False

