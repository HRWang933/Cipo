#############################################################################
# Loading and Unziping file from given URL
#############################################################################
import sys
import time
import logging
import requests
import ssl
from lxml import html
import zipfile
import subprocess
from subprocess import PIPE
import urllib
import os
import wget
from bs4 import BeautifulSoup
import socket
import shutil
import re

#############################################################################
# WGET - get file from URL and store it to the local filesystem
# If the size of file less than 1000 bytes it marks as EMPTY
# This process automaticaly overwrite existing files
#############################################################################
def f_get(url, target):
    name = url.split('/')[-1]
    logging.info(('Start downloading <%s>') % (name))
    stime = time.time()
    try:
        if not os.path.exists(target):
            os.makedirs(target)
        meta = urllib.urlopen(url).info()
        size = int(meta.getheaders("Content-Length")[0])

        if size < 1000:
            raise Exception(('Seems like file <%s> is empty') % (name))

        dfile = wget.download(url, target+name, bar=False)
        with open(dfile, 'rb') as fl:
            part = fl.read(500)

        res = BeautifulSoup(part, "html.parser").find('title')
        ind = bool(res)

        if ind:
            os.remove(dfile)
            raise Exception(res.text)

        if os.path.exists(target + name) and (target+name) != dfile:
            os.remove(target + name)
            os.rename(dfile, target + name)

        logging.info(('File <%s> has been downloaded in %s sec.') % (name, str(round(time.time()-stime,2))))
        return target + name
    except Exception as err:
        logging.error('Failed to download file')
        logging.error(err)
        return False

#############################################################################
#
#############################################################################
def f_get_(url, target):
    name = url.split('/')[-1]
    logging.info(('Start downloading <%s>') % (name))
    stime = time.time()
    try:
        if not os.path.exists(target):
            os.makedirs(target)

        session = requests.session()
        session.proxies = {}
        session.proxies['http'] = 'socks5h://localhost:9050'
        session.proxies['https'] = 'socks5h://localhost:9050'
        meta = session.head(url)
        size = int(meta.headers["Content-Length"])

        if size < 1000:
            raise Exception(('Seems like file <%s> is empty') % (name))

        r = session.get(url, stream=True)
        with open(target + name, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        with open(target + name, 'rb') as fl:
            part = fl.read(500)

        res = BeautifulSoup(part, "html.parser").find('title')
        ind = bool(res)

        if ind:
            os.remove(target + name)
            raise Exception(res.text)

#        if os.path.exists(target + name) dfile:
#            os.remove(target + name)
#            os.rename(dfile, target + name)

        logging.info(('File <%s> has been downloaded in %s sec.') % (name, str(round(time.time()-stime,2))))
        return target + name
    except Exception as err:
        logging.error('Failed to download file')
        logging.error(err)
        return False

#############################################################################
# Unzip the particular .zip file and delete source
#############################################################################
def f_unzip(zfile, target):
    if not zfile: return False
    stime = time.time()
    logging.info(('Start unzipping <%s>') % (zfile))
    try:
        zip_ref = zipfile.ZipFile(zfile, 'r')
        for f in zip_ref.namelist():
            if f.endswith('.zip'):
		zip_ref.extract(f,target)
                zip_ref2 = zipfile.ZipFile(zfile.rsplit('/',1)[0]+'/'+f, 'r')
                for f2 in zip_ref2.namelist():
                    if f2.endswith('.xml'):
                        logging.info(('Extracted <%s> from %s ') % (f2,zfile))
                        zip_ref2.extract(f2,target)
                zip_ref2.close()
            elif f.endswith('.xml'):
		zip_ref.extract(f,target)
                logging.info(('Extracted <%s> from %s') % (f,zfile))
        #zip_ref.extractall(target)
        zip_ref.close()
        os.remove(zfile)
        logging.info(('File <%s> has been unzipped in %s sec.') % (zfile, str(round(time.time()-stime,2))))
    except Exception as err:
        logging.error('Failed to unzip file')
        logging.error(err)
        return False
#############################################################################
# Unzip the particular .zip file and delete source
#############################################################################
def f_unzip2(zfile, target):
    if not zfile: return False
    stime = time.time()
    logging.info(('Start unzipping <%s>') % (zfile))
    try:
        zip_ref = zipfile.ZipFile(zfile, 'r')
        extract_dir =zfile.replace('.zip','') 
        if re.search('WEEKLY',zfile):
            proc_date = 'W'+re.search('WEEKLY_(\d\d\d\d-\d\d-\d\d)',zfile).group(1)
        elif re.search('CA-TMK-GLOBAL',zfile):
            proc_date = 'G'+re.search('CA-TMK-GLOBAL_(\d\d\d\d-\d\d-\d\d)',zfile).group(1)
        logging.debug('Folder:')
        logging.debug(extract_dir)
        logging.debug('proc_date:')
        logging.debug(proc_date)
        if not os.path.exists(extract_dir):
            os.makedirs(extract_dir)
        if  True:
            for f in zip_ref.namelist():
                if f.endswith('.zip'):
                    logging.debug(f)
	            zip_ref.extract(f,target)
		    logging.debug(zfile.rsplit('/',1)[0]+'/'+f)
                    zip_ref2 = zipfile.ZipFile(zfile.rsplit('/',1)[0]+'/'+f, 'r')
                    for f2 in zip_ref2.namelist():
                        if f2.endswith('.xml'):
                            logging.debug(('Extracted <%s> from %s ') % (f2,zfile))
                            zip_ref2.extract(f2,extract_dir)
                            os.rename(extract_dir+'/'+f2, extract_dir+'/'+proc_date+'_'+f2)
                    zip_ref2.close()
                    logging.debug('removing zip file')
                    logging.debug(zfile.rsplit('/',1)[0]+'/'+f)
                    os.remove(zfile.rsplit('/',1)[0]+'/'+f)
                elif f.endswith('.xml'):
	            zip_ref.extract(f,extract_dir)
                    os.rename(extract_dir+'/'+f, extract_dir+'/'+proc_date+'_'+f)
                    logging.debug(('Extracted <%s> from %s') % (f,zfile))
            zip_ref.close()
            os.remove(zfile)
            logging.info(('File <%s> has been unzipped in %s sec.') % (zfile, str(round(time.time()-stime,2))))
    except Exception as err:
        logging.error('Failed to unzip file')
        logging.error(err)
        return False
