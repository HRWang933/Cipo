# IPV project

The Goal:

Load and parse files:
    - Patent Application Full Text Data XML
    - Patent Grant Full Text Data XML
    - Patent Assignment XML
    - Maintenance Fee CSV
    - Attorney info TXT
    - Trademarks application data

Request from API:
    - Transaction history information

Scrape from WEB pages:
    - Patent holder information

SCRIPTS:
    - chromedriver 
      Binary, used by Selenium webdriver to communicate with Chromium headless browser

    - download_chrome_driver.sh
      BASH, downloading chrome driver

    - kill_proc.sh
      BASH, kill orphan processes

    - phi_start.py
      PYTHON, Start scrapping Patent Holder Information

    - etl_start.py
      PYTHON, Start both Loading and Parsing processes (depend on command line keys)

    - load_all.sh
      BASH, Start loading for all file types (used by CRON)

    - parse_all.sh 
      BASH, Start parsing for all file types (used by CRON)

    - tor_install.sh
      BASH, Install TOR service and depenancies

    - dependencies.sh
      BASH, Install all IPV project dependancies

    - install_headless_chrome.sh
      BASH, Install Headless Chrome browser

    - trh_start.py
      PYTHON, Start collecting information about Transaction history

    - crontab.lst
      TXT, Copy of current CRON task scheduler

USAGE:

    etl_start.py Command Line Parameters

    --mode=<mode> - Processing mode
       <mode>:
              load  - Loading files from bulkdata.uspto.gov,canada trademaeks to the Local FS
              parse - Parsing files from Local FS and bulk load parsed data into Impala or Kudu tables

    --type=<type> - Processing files type
       <type>:
              ipa - Application (starting from 2005)
              pa  - Application (2001 - 2004)
              ipg - Grants (starting from 2005)
              pg  - Grants (2001 - 2004)
              fee - Transactions history
              ad  - Assignments
              att - Attorney info
              td  - Canada Trademarks data

    --init_databases - Create databases structure before start processing (Could by used only once, after first project install)

    --init_tables - Create tables structure before start processing (Could by used only once, after first project install)

    --full - Load all files for particular year (not new files only) if not --year key used, load files for current year

    --year=<year> - Set particular year (used only with --full key)

    --tor - Force using TOR proxy for files downloading

    EXAMPLE: etl_start.py --mode=load --type=ipa --full --year=2017 --tor
             Application XML files for full year 2017 will be downloaded through the TOR proxy



