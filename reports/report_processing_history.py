# -*- coding: utf-8 -*-
import sys

sys.path.insert(0, '/home/tarek/ipv_siewling/ipv/')
import os

working_dir = os.getcwd()
print(os.getcwd())

import pandas as pd
from impala.dbapi import connect
import importlib
import re
from routines.send_mail import send_mail
import datetime as dt

cfg = importlib.import_module('.cfg', 'config')


def send_processing(reportType=None):
    impala_con = connect(host=cfg.impala_host)
    impala_cur = impala_con.cursor()
    proc_date = ''
    if reportType == 'new':
        query = 'select max(proc_date) from ipv_db.ca_tm_trademark'
        impala_cur.execute(query)
        data = impala_cur.fetchall()
        proc_date = data[0][0]

        query = "select status from etl_db.reports_status where proc_date='{}' and report_name='report_processing_history'".format(
            proc_date)

        impala_cur.execute(query)
        data = impala_cur.fetchall()
        status = data[0][0]

        if status == 1:
            print('no new data uploaded, skip')
            return

    # impala_cur.execute('DROP TABLE ipv_db.tmp1;')
    # impala_cur.execute('DROP TABLE ipv_db.tmp2;')
    # impala_cur.execute('CREATE TABLE IF NOT EXISTS ipv_db.tmp1 (st13applicationnumber bigint,proc_date string);')
    # impala_cur.execute('CREATE TABLE IF NOT EXISTS ipv_db.tmp2 (st13applicationnumber bigint,markeventdate string);')
    query0 = """
              select substr(cast(mf.st13applicationnumber as string),7,7) as FileID,mf.proc_date,CASE
              when mf.MarkFeatureDescription = '-' then f.indexheadingtext1 else mf.MarkFeatureDescription END as Trade_Mark,'Action History',
              me.MarkEventDate,me.MarkEventCode,me.MarkEventDescriptionText,tm.ApplicationDate
              from ipv_db.ca_tm_feature mf
              left join ipv_db.ca_tm_national_representative nr 
              on mf.st13applicationnumber=nr.st13applicationnumber and mf.proc_date=nr.proc_date
              inner join ipv_db.ca_tm_mark_event me
              on mf.st13applicationnumber=me.st13applicationnumber and mf.proc_date=me.proc_date
              left outer join ipv_db.ca_tm_markrepresentation mp
              on mf.st13applicationnumber=mp.st13applicationnumber and mf.proc_date=mp.proc_date
              left outer join ipv_db.ca_tm_index_heading f
              on  mf.st13applicationnumber=f.st13applicationnumber and mf.proc_date=f.proc_date
              left outer join ipv_db.ca_tm_trademark tm
              on  mf.st13applicationnumber=tm.st13applicationnumber and mf.proc_date=tm.proc_date
              left outer join ipv_db.ca_tm_national_trademark_information nti
              on mf.st13applicationnumber=nti.st13applicationnumber and mf.proc_date=nti.proc_date
              right join (
                         select st13applicationnumber,max(proc_date) proc_date
                         from ipv_db.ca_tm_trademark 
                         group by st13applicationnumber
                         order by st13applicationnumber
                        ) AS newrecord on (mf.st13applicationnumber = newrecord.st13applicationnumber and mf.proc_date = newrecord.proc_date) 
              where nr.entityname in ('BAYO ODUTOLA','KAREN HANSEN','OLLIP P.C.')
              and nti.markcurrentstatusinternaldescriptiontext = 'Formalized'
              order by FileID,me.MarkEventDate
              
              """
    # and me.MarkEventDate > date_sub(now(), interval 2 weeks)
    # and me.MarkEventDate < date_add(now(), interval 3 months)
    impala_cur.execute(query0)
    data = impala_cur.fetchall()
    df_data = pd.DataFrame(data)
    df_data = df_data.drop_duplicates()
    print(df_data)
    print(len(df_data))
    df_data.columns = ['File ID', 'Proc Date', 'Trade Mark', 'Change Type', 'Last Action Date', 'Action Code',
                       'Action History', 'Filing Date']
    df_data['process date'] = pd.to_datetime(df_data['Proc Date'].str.replace('W', '').str.replace('G', ''),
                                             format='%Y-%m-%d')
    df_data['Filing Date'] = pd.to_datetime(df_data['Filing Date'], format='%Y-%m-%d')
    df_data['Days'] = (pd.to_datetime('now') - df_data['Filing Date']).dt.days
    df_data['Months from Filing to date of report'] = df_data['Days'] / 30

    print(df_data['Action History'].value_counts())
    exclude_list = df_data.loc[df_data['Action History'].isin(
        ["Search Recorded", "Examiner's First Report", "Total Provisional Refusal", "Withdrawn by Owner", "Advertised",
         "Registered"]), 'File ID'].tolist()
    df_data = df_data[~df_data['File ID'].isin(exclude_list)]
    df_data.sort_values(by=['File ID', 'Filing Date'], inplace=True, ascending=False)
    df_data = df_data.drop_duplicates(subset=['File ID'], keep='last')
    df_data.drop(columns=['Action Code', 'Action History', 'process date', 'Days'], axis=1, inplace=True)

    df_data.to_excel(working_dir + 'report_processing_history.xlsx', index=None, engine='openpyxl')

    def make_table(df):
        table_html = """
    <tr>"""
        for c in df.columns:
            table_html += """
     <th>{}</th>""".format(c)
        table_html += """
    </tr>"""
        for i, row in df.iterrows():
            table_html += """
        <tr>"""
            for c in df.columns:
                if c == 'File ID':
                    href = 'http://www.ic.gc.ca/app/opic-cipo/trdmrks/srch/viewTrademark.html?id={0}-0&lang=eng&fileNumber={0}&extension=0&startingDocumentIndexOnPage=1'.format(
                        row[c])
                    table_html += """
             <td>
                 <a href="{}">{}</a>
             </td>""".format(href, row[c])
                else:
                    table_html += """
             <td>{}</td>""".format(row[c])

            table_html += """
        </tr>"""

        BODY_HTML = """<html>
<head></head>
<body>
  <h1>Pending Marks</h1>
  <table style="width:100%">
  {}
  </table>
                </body>
                </html>
                            """.format(table_html)
        # print(BODY_HTML)
        return BODY_HTML

    table_html = make_table(df_data)
    file = open(working_dir + "report_cipo_processing.html", "w")
    file.write(table_html)
    file.close()
    #############################################################################
    # Get credential for EMail notification
    #############################################################################
    # td = pd.to_datetime('today')
    td = dt.datetime.today() - dt.timedelta(days=1)

    def get_mail_params(table_html):
        mail_params = cfg.mail_params

        var_params = {
            'text': table_html,
            'subject': 'CIPO Processing History Report: {} {}, {}'.format(td.strftime("%B"), td.strftime("%d"),
                                                                          td.strftime("%Y")),
            'attach_file': '',
            'as_table': False,
            'table_html': '',
            'text_type': 'html',
            'send_to': ['tmgroup@ollip.com', 'owaiskarni81@hotmail.com']
        }
        del mail_params['send_to']
        mail_params.update(var_params)

        return mail_params

    send_mail(get_mail_params(table_html))
    print('email sent')

    query = "update etl_db.reports_status set status=1 where proc_date='{}' and report_name='report_processing_history'".format(
        proc_date)
    impala_cur.execute(query)


if __name__ == "__main__":
    try:
        print('=' * 30)
        print('Getting CIPO Processing History Report')
        print('=' * 30)
        try:
            send_processing(sys.argv[1])
        except:
            send_processing()

    except Exception as err:
        print('fail')
        print(err)
