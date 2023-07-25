#!/usr/bin/env python
#############################################################################
# IPV Patent information files Downloader&Parser
# Author: Alex Kovalsky
#############################################################################
import sys
import os
from os import walk
import time
import logging
import zipfile
import routines.dbs_handlers as dbs
import routines.ldr_handlers as loader
import routines.tbl_handlers as tbl
import routines.wpr_handlers as parser
import routines.lnk_handlers as lnk
from routines.send_mail import send_mail
from config import cfg
from datetime import datetime, date, timedelta
import argparse
import re


#############################################################################
# --type CLI parameter validation
#############################################################################
def check_type(value):
    value = value.strip().replace('\r', '').replace('\n', '')
    if value not in ['ipg', 'ipa', 'ad', 'fee', 'att', 'pg', 'pa', 'td']:
        # raise argparse.ArgumentTypeError("%s is an incorrect file type" % value)
        raise argparse.ArgumentTypeError("{} is an incorrect file type".format(value))
    return value


#############################################################################
# --mode CLI parameter validation
#############################################################################
def check_mode(value):
    value = value.strip().replace('\r', '').replace('\n', '')
    if value not in ['load', 'parse']:
        # raise argparse.ArgumentTypeError("%s is an incorrect procesing mode" % value)
        raise argparse.ArgumentTypeError("{} is an incorrect procesing mode".format(value))
    return value


#############################################################################
# --year CLI parameter validation
#############################################################################
def check_year(value):
    if int(value) < 2001 and int(value) > 2050:
        raise argparse.ArgumentTypeError("%s is an incorrect procesing year" % value)
    return value


#############################################################################
# Start loading process
#############################################################################
def load_proc(year, ftype, all_files=None, tor=None):
    logging.info('start loading')
    target_dir = ('./source/%s/') % (ftype)
    if ftype != 'td':
        links = lnk.get_links(year, ftype, all_files, tor)
        logging.info(('Found %s files to download') % (str(len(links))))
        for link in links:
            stime = time.time()
            logging.info(('Downloading: %s') % (link))
            if tor:
                zpf = loader.f_get_(link, target_dir)
            else:
                zpf = loader.f_get(link, target_dir)
            loader.f_unzip(zpf, target_dir)
            logging.info(('File %s has been downloaded and unzipped in %s sec.') % (link.split('/')[-1],
                                                                                    str(time.time() - stime).split('.')[
                                                                                        0]))
    else:
        # web scraping method
        logging.info('Scraping from webpage')
        links = []
        links = lnk.get_links(year, ftype, all_files, tor)
        logging.info(('Found %s files to download') % (str(len(links))))
        scraped_fn = []

        ## remove links that have been uploaded
        # links = lnk.clean_list(links)
        # print(links)
        for link in links:
            stime = time.time()
            if link.endswith('Schemas'): continue
            logging.info(('Downloading: %s') % (link))
            scraped_fn.append(os.path.basename(link))

            # if os.path.basename(link)!= 'WEEKLY_2020-08-04_00-04-37.zip': continue
            if tor:
                zpf = loader.f_get_(link, target_dir)
            else:
                zpf = loader.f_get(link, target_dir)

            loader.f_unzip2(zpf, target_dir)
            logging.info(('File %s has been downloaded and unzipped in %s sec.') % (link.split('/')[-1],
                                                                                    str(time.time() - stime).split('.')[
                                                                                        0]))
        # sftp method
        # connect to sftp and download into source/td/
        logging.info('Checking sftp for additional data to download')
        hlinks, wlinks = lnk.get_linkssftp(year, ftype, all_files, tor, target_dir, scraped_fn)
        # hlinks,wlinks = lnk.get_linkssftp(year, ftype, all_files, tor,target_dir)
        # sorting
        hlinks = sorted(hlinks, key=lambda x: re.search('.*_(\d+)\.zip', x).group(1))
        wlinks = sorted(wlinks)
        zpf = hlinks + wlinks
        if len(zpf) == 0 and len(scraped_fn) == 0:
            return False
        logging.info(('Found %s files to download') % (str(len(zpf))))
        for l, link in enumerate(hlinks + wlinks):
            print(l, link)
            if True:
                stime = time.time()
                loader.f_unzip2(target_dir + link, target_dir)
                logging.info(('File %s has been unzipped in %s sec.') % (target_dir + link.split('/')[-1],
                                                                         str(time.time() - stime).split('.')[0]))
    return True


#############################################################################
# Start parsing process
#############################################################################
def parse_proc(year, ftype, all_files=None, tor=None):
    logging.info('start parsing')
    stime = time.time()
    source_dir = ('./source/%s/') % (ftype)
    # print('source_dir', source_dir)
    processed_dir = ('./source/processed/%s/') % (ftype)
    # print('processed_dir', processed_dir)

    parser.set_env()
    flist = []
    for (dirpath, dirnames, filenames) in walk(source_dir):
        # print('dirpath:{}'.format(dirpath))
        # print('length', len(dirnames), len(filenames))
        if ftype == 'td':
            folderList = []
            folderList.extend([x for x in dirnames])
            if len(folderList) == 0:
                logging.info('Nothing to parse')
                return False
            # flist.extend([ x for x in filenames if x[-3:]=='xml'])
            logging.info(('Found %s folders to process') % (len(folderList)))
        else:
            flist.extend(filenames)
            logging.info(('Found %s files to process') % (len(flist)))
        break
    logging.info('parsing ftype: {}'.format(ftype))
    if ftype == 'td':
        hlinks = [link for link in folderList if link.startswith('CA-TMK')]
        hlinks = sorted(hlinks, key=lambda x: x.rsplit('_')[-1])
        wlinks = sorted([link for link in folderList if link.startswith('WEEKLY')])
        stime0 = time.time()
        for f_no, filename in enumerate(hlinks + wlinks):
            # print('f_no:{}, filename:{}'.format(f_no, filename))
            # if f_no !=0: continue
            stime1 = time.time()
            # print(f_no,filename)
            logging.info('Parsing {} '.format(filename))
            # todo
            # if filename == 'WEEKLY_2020-01-28_00-07-56':
            if True:
                flist = os.listdir(source_dir + filename)
                logging.info('Found {} xml files'.format(len(flist)))
                # print(flist)
                # print(len(flist))
                count = 0
                file_list = []
                filename_list = []
                # flist = flist[0:3000 ]
                for f_no, fl in enumerate(flist):
                    # print('f_no: {}, fl: {}'.format(f_no, fl))
                    stime = time.time()
                    if count == 3000 or f_no == len(flist) - 1:
                        # print(f_no-count,f_no, len(flist))
                        logging.info('parsing chunk of {} xml files'.format(count))
                        file_list.append(source_dir + filename + '/' + fl)
                        filename_list.append(fl)
                        # print(file_list)
                        count = 0
                        fls = ', '.join(filename_list)
                        # parser.parse2(file_list )
                        # print(tbl.load_tables(parser.parse2(file_list )))
                        # break
                        ##if tbl.load_tables(parser.parse(source_dir + fl), False):
                        if tbl.load_tables(parser.parse2(file_list), False):
                            if not os.path.exists(processed_dir + filename):
                                os.makedirs(processed_dir + filename)
                            for x in filename_list:
                                pass
                                # print(source_dir +filename+'/'+ x, processed_dir +filename+'/'+ x)
                                os.rename(source_dir + filename + '/' + x, processed_dir + filename + '/' + x)
                            # need to addin all file names
                            logging.debug(
                                ('File %s successfully parsed and loaded into Impala table in %s sec.') % (fls,
                                                                                                           str(round(
                                                                                                               time.time() - stime,
                                                                                                               2))))
                        else:
                            print(filename_list)
                            raise Exception(('Failed to process %s') % (fls))

                        file_list = []
                        filename_list = []
                        if len(os.listdir(source_dir + filename)) == 0:
                            os.rmdir(source_dir + filename)
                    elif count < 3000:
                        file_list.append(source_dir + filename + '/' + fl)
                        filename_list.append(fl)
                        count += 1
            logging.info(('Processing time for %s: %s') % (filename, str(round(time.time() - stime1, 2))))

        logging.info(('Total processing time: %s') % (str(round(time.time() - stime0, 2))))
        tbl.insert_new_proc_date_reports_status()

    else:
        for fl in flist:
            stime = time.time()
            if tbl.load_tables(parser.parse(source_dir + fl), False):
                if not os.path.exists(processed_dir):
                    os.makedirs(processed_dir)
                os.rename(source_dir + fl, processed_dir + fl)
                logging.info(('File %s successfully parsed and loaded into Impala table in %s sec.') % (fl,
                                                                                                        str(round(
                                                                                                            time.time() - stime,
                                                                                                            2))))
            else:
                raise Exception(('Failed to process %s') % (fl))
        logging.info(('Total processing time: %s') % (str(round(time.time() - stime, 2))))
    td = datetime.now()
    #    if int(td.strftime("%d"))<=7:
    #        logging.info('Generating Search Report')
    #        send_search()

    return True


#############################################################################
# Get credential for EMail notification
#############################################################################
def get_mail_params(ftype, mode, rfile):
    with open(rfile, 'r') as fl:
        text = fl.readlines()
        text = ''.join(text)
    mode_map = {
        'load': 'loading',
        'parse': 'parsing'
    }

    type_map = {
        'ipg': 'Grant XML',
        'ipa': 'Application XML',
        'ad': 'Assignments XML',
        'fee': 'Transactions fee TXT',
        'att': 'Attorney TXT',
        'pg': '(Old) grant XML',
        'pa': '(Old) application XML',
        'td': 'Canada Trademarks data'
    }

    mail_params = cfg.mail_params

    var_params = {
        'text': text,
        'subject': ('%s file %s report') % (type_map[ftype], mode_map[mode]),
    }

    mail_params.update(var_params)

    return mail_params


#############################################################################
if __name__ == "__main__":

    try:
        status = False
        max_proc_date = tbl.get_max_proc_date()
        print('max_proc_date', max_proc_date)
        if max_proc_date != '':
            max_proc_date = max_proc_date[1:]
        print('max_proc_date', max_proc_date)
        next_proc_date = datetime.strptime(max_proc_date, '%Y-%m-%d').date() + timedelta(days=7)
        print('next_proc_date', next_proc_date)
        today = date.today()
        diff = next_proc_date - today
        if diff.days > 0:
            sys.exit(1)

        descr = ('IPV Patent information files Downloader&Parser v0.1\n'
                 'Author: Alex Kovalsky')
        arg_parser = argparse.ArgumentParser(description=descr)
        arg_parser.add_argument("--type", type=check_type,
                                default='',
                                help="Type of processed file (ipa, ipg, ad etc.)")
        arg_parser.add_argument("--mode", type=check_mode,
                                default='',
                                help="Processing mode: load or parse")
        arg_parser.add_argument("--year", type=check_year,
                                default=datetime.now().year,
                                help="Year for source file downloads")
        arg_parser.add_argument("--full", action='store_true',
                                help="Loading mode: full load , instead of only new files")
        arg_parser.add_argument("--tor", action='store_true',
                                help="Using TOR (anonymous network)")
        arg_parser.add_argument("--init_tables", action='store_true',
                                help="Force tables initialization before processing")
        arg_parser.add_argument("--init_databases", action='store_true',
                                help="Force databases initialization before processing")

        if len(sys.argv) == 1:
            arg_parser.print_help()
            sys.exit(1)

        args = arg_parser.parse_args()

        log_file_name = ('./log/%s_%s_%s.log') % (args.type,
                                                  args.mode,
                                                  str(datetime.now())[2:19].replace(' ', '_'))
        log_file_name2 = ('./log/%s_%s_%s_email.log') % (args.type,
                                                         args.mode,
                                                         str(datetime.now())[2:19].replace(' ', '_'))

        logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s',
                            level=logging.DEBUG)
        #        logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s',
        #                            level=logging.INFO)

        logFormatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
        rootLogger = logging.getLogger()

        fileHandler = logging.FileHandler(log_file_name)
        fileHandler.setFormatter(logFormatter)

        emailHandler = logging.FileHandler(log_file_name2)
        emailHandler.setFormatter(logFormatter)
        emailHandler.setLevel(logging.INFO)
        rootLogger.addHandler(fileHandler)
        rootLogger.addHandler(emailHandler)

        arg = (args.year, args.type, args.full, args.tor)

        proc = {'load': load_proc,
                'parse': parse_proc}
        if args.init_databases: dbs.init_dbs()
        if args.init_tables: tbl.init_tables(args.type)

        status = proc[args.mode](*arg)
        print('status', status)

    except Exception as error:
        status = True
        logging.error('Failed to process!')
        logging.error(error)

    finally:
        # if status == False:
        #     logging.debug('Skip sending email. No new data downloaded/uploaded')
        # else:
        #     if len(sys.argv) != 1:
        if status:
            print('Log File Name: ', log_file_name)
            print('Sending email...')
            send_mail(get_mail_params(args.type, args.mode, log_file_name2))
        else:
            print('Skip sending email. No new data downloaded/uploaded')
            logging.info('Skip sending email. No new data downloaded/uploaded')

        # if status == False:
        #     logging.debug('Skip sending email. No new data downloaded/uploaded')
        # else:
        #     if len(sys.argv) != 1:
        #         send_mail(get_mail_params(args.type, args.mode, log_file_name2))
