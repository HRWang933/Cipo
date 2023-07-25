#############################################################################
# Get links handlers
#############################################################################
import user_agents as ua
import logging
import requests
import urllib
from lxml import html
from impala.dbapi import connect
from datetime import datetime,timedelta
import importlib
cfg = importlib.import_module('.cfg', 'config')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep, time
import re
import pysftp
import os
import shutil
import zipfile

#############################################################################
# check through web scraped links, remove it from the list if it has been 
# processed and uploaded to impala table
#############################################################################
def clean_list(links):
    links2 = []
    dates = []     
    impala_con = connect(host=cfg.impala_host)
    impala_cur = impala_con.cursor()
    query = ('SELECT DISTINCT proc_date FROM `ipv_db`.`ca_tm_trademark` ')
    impala_cur.execute(query)
    dates = [elm[0] for elm in impala_cur.fetchall()]
    logging.debug('proc_date from implala')
    logging.debug(dates)
    impala_cur.close()
    impala_con.close()
    for link in links:
        short_name = os.path.basename(link)
        if re.search('WEEKLY',short_name):
            proc_date = 'W'+re.search('WEEKLY_(\d\d\d\d-\d\d-\d\d)',short_name).group(1)
            if proc_date in dates:
                print(link)
            else:
                links2.append(link)
        elif re.search('CA-TMK-GLOBAL',short_name):
            proc_date = 'G'+re.search('CA-TMK-GLOBAL_(\d\d\d\d-\d\d-\d\d)',short_name).group(1)
            if proc_date in dates:
                print(link)
            else:
                links2.append(link)

    return links2
#############################################################################
# Scrape for link name from sftp
#############################################################################
def get_linkssftp(year, ftype, all_files, tor,target_dir,links=[]):
    #links = ['https://opic-cipo.ca/cipo/client_downloads/Trademarks_Weekly/WEEKLY_2020-11-17_00-07-58.zip','https://opic-cipo.ca/cipo/client_downloads/Trademarks_Weekly/WEEKLY_2020-09-27_00-05-48.zip']
    link_dates = []
    if len(links)!=0:
        for l in links:
            print(l.split('/')[-1])
            print(re.search('WEEKLY_(\d{4}\-\d{2}\-\d{2})',l.split('/')[-1]).group(1))
            link_dates.append('W'+re.search('WEEKLY_(\d{4}\-\d{2}\-\d{2})',l.split('/')[-1]).group(1)) 
    print(link_dates)
    dates = []     
    impala_con = connect(host=cfg.impala_host)
    impala_cur = impala_con.cursor()
    query = ('SELECT DISTINCT proc_date FROM `ipv_db`.`ca_tm_trademark` order by proc_date')
    impala_cur.execute(query)
    dates = [elm[0] for elm in impala_cur.fetchall()]
    logging.debug('proc_date from implala')
    logging.debug(dates)
    impala_cur.close()
    impala_con.close()
    if not os.path.exists(target_dir):
        logging.info(('target_dir %s not found') % (str(target_dir)))
        os.makedirs(target_dir)
        logging.info('taget_dir created')
    #host = '38.117.69.16'
    host = 'iphorizonspi.opic-cipo.ca'
    username = 'cipo.customer74'
    password = 'rai7No5theu%ng'
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    historyfileListD = []
    weeklyfileListD = []
    hist_folderList = []
    with pysftp.Connection(host, username=username, password=password, cnopts=cnopts) as sftp:
        allFiles= sftp.listdir_attr()
        for f in allFiles:
            if re.search('Trademarks_Historical',f.filename):
	        hist_folderList.append(f.filename)
        for hist_folder in hist_folderList: 
            logging.info(('Checking in %s') %(str(hist_folder)))
            # no permission on some future folder
            try:
                with sftp.cd('/dev/cipo-d1/www/clients/client1/web3/web/cipo/client_downloads/'+hist_folder):           # temporarily chdir to allcode
                    #historyfileList = sftp.listdir()
                    historyfileList = sftp.listdir_attr()
                    historyfileList = [ele for ele in historyfileList if re.search('.*_(\d+)\.zip',ele.filename) ]
                    for i,h in enumerate(historyfileList):
                        t = datetime.fromtimestamp(h.st_mtime).strftime('%Y-%m-%d')
                        #print(i,h.filename,t)
                        logging.debug(h.filename)
                        #if re.search('WEEKLY',elm):
                        #    file_date = 'W'+re.search('WEEKLY_(\d\d\d\d-\d\d-\d\d)',elm).group(1)
                        #    #logging.info(elm)
                        #    #logging.info(file_date) 
                        file_date = 'G'+re.search('CA-TMK-GLOBAL_(\d\d\d\d-\d\d-\d\d)',h.filename).group(1)
                        if file_date not in dates and h.filename not in links:
                            sftp.get(h.filename,localpath=target_dir+os.path.basename(h.filename))
                            historyfileListD.append(h.filename)
                            logging.info(('Downloaing %s') % (str(os.path.basename(h.filename))))
            except Exception as histErr:
                logging.error(histErr)
        #logging.info('Checking in Trademarts_Weekly')
        #with sftp.cd('/dev/cipo-d1/www/clients/client1/web3/web/cipo/client_downloads/Trademarks_Weekly'):           # temporarily chdir to allcode
        #    #weeklyfilelist = sftp.listdir()
        #    weeklyfilelist = sftp.listdir_attr()
        #    weeklyfilelist = [ele for ele in weeklyfilelist if re.search('.*-(\d+)\.zip',ele.filename) ]
        #    for i,h in enumerate(weeklyfilelist):
        #        t = datetime.fromtimestamp(h.st_mtime).strftime('%y-%m-%d')
        #        logging.debug(h.filename)
        #        #print(i,h.filename,t)
        #        #WEEKLY_2019-06-18_09-58-15.zip
        #        file_date = 'W'+re.search('WEEKLY_(\d\d\d\d-\d\d-\d\d)',h.filename).group(1)
        #        if file_date not in dates and h.filename not in links:
        #            sftp.get(h.filename,localpath=target_dir+os.path.basename(h.filename))
        #            weeklyfileListD.append(h.filename)
        #            logging.info(('downloaing %s') % (str(os.path.basename(h.filename))))
        #        #if h.filename =='weekly_2020-08-04_00-04-37.zip':
        #        #    weeklyfileListD.append(h.filename)
        #        #    #sftp.get(h.filename,localpath=target_dir+os.path.basename(h.filename))
        logging.info('Checking in Trademarts_Weekly_Uncompressed')
        with sftp.cd('/dev/cipo-d1/www/clients/client1/web3/web/cipo/client_downloads/Trademarks_Weekly_Uncompressed'):           # temporarily chdir to allcode
            #weeklyfilelist = sftp.listdir()
            weeklyfilelist = sftp.listdir_attr()
            weeklyfilelist = [ele for ele in weeklyfilelist if re.search('.*_(\d+)\.zip',ele.filename) ]
            for i,h in enumerate(weeklyfilelist):
                t = datetime.fromtimestamp(h.st_mtime).strftime('%y-%m-%d')
                logging.debug(h.filename)
                logging.debug(t)
                try:
                    file_date = re.search('_\d\d\d\d-\d\d-\d\d-(\d\d\d\d-\d\d-\d\d)',h.filename).group(1)
                except:
                    logging.debug('no idea how to proceed')
                    continue
                file_date = datetime.strptime(file_date,'%Y-%m-%d')
                logging.debug(file_date)
                file_date = 'W'+(file_date + timedelta(days=1)).strftime("%Y-%m-%d")
                logging.debug(file_date)
                #if file_date == 'W2021-03-02' or (file_date not in dates and file_date not in link_dates):
                if file_date not in dates and file_date not in link_dates:
                    dir_name = 'WEEKLY_'+file_date.replace('W','')+'_00-00-00'
                    if dir_name in os.listdir(target_dir):
                        pass
                    else:
                        os.mkdir(os.path.join(target_dir,dir_name))
                    sftp.get(h.filename,localpath=os.path.join(target_dir,dir_name,os.path.basename(h.filename)))
                    if dir_name not in weeklyfileListD:
                        weeklyfileListD.append(dir_name)
                    logging.info(('downloaing %s') % (str(os.path.basename(h.filename))))
    for w_no,w in enumerate(weeklyfileListD):
        shutil.make_archive(os.path.join(target_dir,w), 'zip', os.path.join(target_dir,w))
        myZipFile = zipfile.ZipFile(os.path.join(target_dir,w)+'.zip', "w" )
        for filename in os.listdir(os.path.join(target_dir,w)):
            myZipFile.write(os.path.join(target_dir,w,filename), os.path.join(w,filename), zipfile.ZIP_DEFLATED )
        myZipFile.close()
        shutil.rmtree(os.path.join(target_dir,w))
        weeklyfileListD[w_no] = w+'.zip'

    return historyfileListD, weeklyfileListD
#############################################################################
# Scrape for link name from web
#############################################################################
def scrape_td(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
#    chrome_options.add_argument('start-maximized')
#    chrome_options.add_argument('disable-infobars')
#    chrome_options.add_argument("--disable-extensions")
#    chrome_options.add_argument("--enable-javascript")
#    chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
    chrome_options.add_argument(('user-agent=%s') % (ua.get_user_agent()))
    driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options,
                                  service_args=['--verbose', '--log-path=./log/chromedriver.log'])
    driver.set_window_size(1280, 1024)
    driver.implicitly_wait(10)

    try:
        driver.get(url)
        link_list = []
        tmp_list = []
        for section in ["historical-lnk","weekly-lnk"]:   
            # click on correct section
            #print(section)
            sectionTab = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//a[@id="{}"]'.format(section))))
            sectionTab.click()
            sleep(5)
            try:
               if section == "historical-lnk":
                   getname = driver.find_elements_by_xpath('.//div[@class="dataTables_length"]')[1].get_attribute('id')
               else:
                   getname = driver.find_elements_by_xpath('.//div[@class="dataTables_length"]')[0].get_attribute('id')
               #print(getname)
    	       logging.info('Click on {} tab'.format(section))
               btn100 = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//select[@name="{}"]/option[text()="100"]'.format(getname))))
               btn100.click()
               sleep(5)
            except Exception as xx:
    		logging.error('Fail to click on tab')
	        logging.error(xx)

    	    logging.info('Collecting zip file links')
            nextID = getname.replace('length','next')
            #print(nextID)
            for page in range(0,5):
                logging.debug('page: {}'.format(page))
                if page == 0:
                    pass
                else:
                    # click on next button
                    try:
                        #print(driver.find_element_by_xpath(".//a[@id='{}']".format(nextID)).text)
                        if section == "historical-lnk":
                            if driver.find_element_by_xpath(".//a[@id='{}']".format(nextID)).text == 'Next':
                                #print('Found next btn')
                                driver.find_element_by_xpath(".//a[@id='{}']".format(nextID)).click()
                                #driver.send_keys(Keys.END)
                                sleep(5)
                            else:
                                #print(link_list)
                                #driver.quit()
                                # todo, sending just 1 link
                                #return [link_list[0]]
                                #return link_list
    		                logging.info('Gathered all historical link')
                                break
                        elif section == "weekly-lnk":
                            if driver.find_element_by_xpath(".//a[@id='{}']".format(nextID)).text == 'Next':
                                #print('Found next btn')
                                driver.find_element_by_xpath(".//a[@id='{}']".format(nextID)).click()
                                #driver.send_keys(Keys.END)
                                sleep(5)
                            else:
                                #print(link_list)
                                driver.quit()
                                # todo, sending just 1 link
                                #return [link_list[0]]
		                link_list.reverse()
		                tmp_list.reverse()
                                link_list.extend(tmp_list)
    		                logging.info('Gathered all weekly link')
                                return link_list
                    except Exception as errxx:
    		       logging.error('Fail to load all files from tab')
                       logging.error(errxx)
                            
                           
                for i,tb in enumerate(driver.find_elements_by_xpath(".//div[@class='dataTables_wrapper no-footer']")):
                    #print(tb.find_element_by_xpath(".//div[@class='dataTables_paginate paging_simple_numbers']").text)
                    if section == 'weekly-lnk':
                        if i !=0:
                            continue
                    elif section == 'historical-lnk':
                        if i !=1:
                            continue
                    for e,each in enumerate(tb.find_elements_by_xpath(".//tbody/tr")):
                        #print(e,each.get_attribute('href'))#try:
                        filename = each.find_elements_by_tag_name('td')[0].text.strip()
                        fileLink = each.find_element_by_xpath('.//td/a').get_attribute('href').strip()
                        logging.debug(fileLink)
                        fileLink = re.sub('\.zip.*','.zip',str(fileLink))
                        if fileLink.split('/')[-1] == filename:
                            #print(fileLink)
                    	    if section != 'weekly-lnk':
                                link_list.append(fileLink)
                            else:
				tmp_list.append(fileLink)
                        else:
                            logging.warning('file link is not matching file name')
                            logging.warning(('File Name: %s') %(str(filename)))
                            logging.warning(('File Link: %s') %(str(fileLink)))
                        
                        #if re.search('[_-]\d+\.zip',each.get_attribute('href')):
                        #    #print(e,each.get_attribute('href'))#try:
                    	#    if section != 'weekly-lnk':
                        #        link_list.append(re.sub('\.zip.*','.zip',str(each.get_attribute('href'))))
                        #    else:
			#	tmp_list.append(re.sub('\.zip.*','.zip',str(each.get_attribute('href'))))
    except:
        driver.quit()


#############################################################################
# Get list of allowed file types
#############################################################################
def get_possible_ftypes():
   return [t if not t.startswith('fee') else 'fee' for t in cfg.active_parsers.keys()]

#############################################################################
# Get full links list from paricular web page (depending of file type)
#############################################################################
def get_links_list(year, ftype):
    logging.info('Creating links list')
    if ftype not in get_possible_ftypes(): raise Exception('Incorrect file type!')
    res = []
    if ftype == 'ad': 
        url = cfg.dwl_links[ftype]
        durl_prefix = url
    elif ftype in ['fee','att']:
        return [cfg.dwl_links[ftype]]
    elif ftype == 'td':
        url = cfg.dwl_links[ftype]
        res = scrape_td(url)
        return res if len(res) > 0 else False
    else:
        url =('%s%s/') % (cfg.dwl_links[ftype], year)
        durl_prefix = ('%s20') % (cfg.dwl_links[ftype])

    HEADERS = {'User-Agent': ua.get_user_agent()}

    page = requests.get(url, headers=HEADERS)

    content = html.fromstring(page.content)

    file_list =  content.xpath('.//tr/td/a/text()')

    for fl in file_list:
        if fl.endswith('.zip') and (fl.split('/')[-1].find('-') < 0):
            if ftype == 'ad':
                res.append(durl_prefix + fl)
            elif ftype in ['pg','pa']: res.append(durl_prefix + fl[2:4] + '/' + fl)
            else:res.append(durl_prefix + fl[3:5] + '/' + fl)

    return res if len(res) > 0 else False

#############################################################################
# Get full links list from paricular web page (depending of file type) TOR
#############################################################################
def get_links_list_(year, ftype):
    #print('in get_links_list_')
    logging.debug('Creating links list')
    if ftype not in get_possible_ftypes(): raise Exception('Incorrect file type!')
    res = []
    if ftype == 'ad': 
        url = cfg.dwl_links[ftype]
        durl_prefix = url
    elif ftype == 'td':
        url = cfg.dwl_links[ftype]
        # not adding proxies, just 2 page scraping
        res = scrape_td(url)
        return res if len(res) > 0 else False
    elif ftype in ['fee','att']:
        return [cfg.dwl_links[ftype]]
    else:
        url =('%s%s/') % (cfg.dwl_links[ftype], year)
        durl_prefix = ('%s20') % (cfg.dwl_links[ftype])

    HEADERS = {'User-Agent': ua.get_user_agent()}
    session = requests.session()
    session.proxies = {}
    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'

    page = session.get(url, headers=HEADERS)

    content = html.fromstring(page.content)

    file_list =  content.xpath('.//tr/td/a/text()')

    for fl in file_list:
        if fl.endswith('.zip') and (fl.split('/')[-1].find('-') < 0):
            if ftype == 'ad':
                res.append(durl_prefix + fl)
            elif ftype in ['pg','pa']: res.append(durl_prefix + fl[2:4] + '/' + fl)
            else:res.append(durl_prefix + fl[3:5] + '/' + fl)

    return res if len(res) > 0 else False

#############################################################################
# Get allowed to download links list (depending of file type)
#############################################################################
def get_links(year, ftype, full_list=None, tor=None):

    if ftype not in get_possible_ftypes(): raise Exception('Incorrect file type!')
    if tor: links = get_links_list_(year, ftype)
    else:
        links = get_links_list(year, ftype)
    if not links: raise Exception('No links were extracted for this year')
    res = []
    if not full_list:
        tbl_preffix = {'ipg' :'grant',
                       'ipa' :'application',
                        'ad' :'assignment',
                        'td' :'ca_tm_trademark',
                        'att':'attorney',
                        'fee':'fee'}[ftype]

        impala_con = connect(host=cfg.impala_host)
        impala_cur = impala_con.cursor()
        if ftype in ['ipg', 'ipa', 'pg', 'pa', 'fee']:
            query = ('SELECT DISTINCT proc_date FROM `ipv_db`.`%s_main` '
                     'WHERE SUBSTR(proc_date,1,4) = \'%s\' ORDER by proc_date DESC') % (tbl_preffix, year)
        elif ftype in ['att']:
            query = ('SELECT updated FROM `ipv_db`.`%s` LIMIT 1') % (tbl_preffix)
        elif ftype in ['td']:
#            last_file = 0
#            for i,l in enumerate(links):
#		if re.search('Trademarks_Weekly',l):
#                    last_file = i 
#                    break
            query = ('SELECT DISTINCT proc_date FROM `ipv_db`.`%s`') % (tbl_preffix)
        else:
            query = ('SELECT DISTINCT last_update FROM `ipv_db`.`%s_main` '
                     'WHERE SUBSTR(last_update,1,4) = \'%s\' ORDER BY last_update DESC') % (tbl_preffix, year)

        dates = []
        # todo
        impala_cur.execute(query)
        if ftype in ['td']:
            dates = [elm[0] for elm in impala_cur.fetchall()]
        else:
            dates = [elm[0][2:] for elm in impala_cur.fetchall()]

        logging.debug('Current proc_date in impala')
        logging.debug(dates)
        impala_cur.close()
        impala_con.close()

        if ftype in ['fee','att']:
            meta = urllib.urlopen(links[0]).info()
            file_date = datetime.strptime(meta.getheaders('Last-Modified')[0],'%a, %d %b %Y %H:%M:%S %Z')
            base_date = datetime.strptime('20' + dates[0], '%Y%m%d')
            if (file_date-base_date).days > 2: res = links[:]
        elif ftype in ['td']:
	    today =datetime.now()
            for elm in links:
                if (elm[-4:].lower() != '.zip'): continue
                #meta = urllib.urlopen(elm).info()
            	#file_date = datetime.strptime(meta.getheaders('Last-Modified')[0],'%a, %d %b %Y %H:%M:%S %Z')
		#if (today-file_date).days  <= 7:
                #    res.append(elm)
                # todo if file name contains date that exisited in the dates, continue 
                if re.search('WEEKLY',elm):
                    file_date = 'W'+re.search('WEEKLY_(\d\d\d\d-\d\d-\d\d)',elm).group(1)
                    #logging.info(elm)
                    #logging.info(file_date) 
                elif re.search('CA-TMK-GLOBAL',elm):
                    file_date = 'G'+re.search('CA-TMK-GLOBAL_(\d\d\d\d-\d\d-\d\d)',elm).group(1)
                if file_date not in dates:
                    res.append(elm)
        else:
            for elm in links:
                if (elm[-4:].lower() != '.zip') or (elm[-10:-4] in dates): continue
                res.append(elm)
    else:
        for elm in links:
            if (elm[-4:].lower() != '.zip'): continue
            res.append(elm)

    if ftype != 'td':
        if len(res) == 0: raise Exception('No new files to download were found')

    return res

