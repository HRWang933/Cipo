# -*- coding: utf-8 -*-
import sys

sys.path.append('../')

import pandas as pd
from impala.dbapi import connect
import importlib
import re
from routines.send_mail import send_mail

cfg = importlib.import_module('.cfg', 'config')


def send_search(reportType=None):
    impala_con = connect(host=cfg.impala_host)
    impala_cur = impala_con.cursor()
    proc_date = ''
    if reportType == 'new':
        query = 'select max(proc_date) from ipv_db.ca_tm_trademark'
        impala_cur.execute(query)
        data = impala_cur.fetchall()
        proc_date = data[0][0]

        query = "select status from etl_db.reports_status where proc_date='{}' and report_name='report_processingtime'".format(
            proc_date)

        impala_cur.execute(query)
        data = impala_cur.fetchall()
        status = data[0][0]

        if status == 1:
            print('no new data uploaded, skip')
            return

    df_summary = pd.DataFrame()
    writer = pd.ExcelWriter('processingtime_report.xlsx', engine='xlsxwriter')
    for m, month in enumerate([30, 24, 18, 12, 6]):
        query0 = """
                  select tm.ST13Applicationnumber,tm.ApplicationDate,tm.InternationalMarkIdentifier,nti.markcurrentstatusinternaldescriptiontext,tm.proc_date,app.countrycode,me.MarkEventDescriptionText,me.MarkEventDate
                  from 
                  ipv_db.ca_tm_trademark tm 
                  left outer join ipv_db.ca_tm_applicant app
                  on
                  tm.st13applicationnumber=app.st13applicationnumber and tm.proc_date=app.proc_date
                  left outer join ipv_db.ca_tm_national_trademark_information nti
                  on
                  tm.st13applicationnumber=nti.st13applicationnumber and tm.proc_date=nti.proc_date
                  left join ipv_db.ca_tm_mark_event me 
                  on tm.st13applicationnumber=me.st13applicationnumber and tm.proc_date=me.proc_date 
                  right join (
                             select st13applicationnumber,max(proc_date) proc_date
                             from ipv_db.ca_tm_trademark 
                             group by st13applicationnumber
                            ) AS newrecord on (tm.st13applicationnumber = newrecord.st13applicationnumber and tm.proc_date = newrecord.proc_date) 
                  where tm.ApplicationDate > months_sub(now(), {})
                  and tm.InternationalMarkIdentifier <>'-';
                """.format(str(month))
        impala_cur.execute(query0)
        data = impala_cur.fetchall()
        df = pd.DataFrame(data)
        total = df[0].nunique()
        s = df[df[6] == 'Search Recorded'][0].nunique()
        et = df[(df[6] == "Examiner's First Report") | (df[6] == "Total Provisional Refusal")][0].nunique()
        # print('Total application',total)
        # print('Searched application',s)
        # print('exam.. total..',et)
        df_summary.loc[m, 'Type'] = 'International'
        df_summary.loc[m, 'Month'] = month
        df_summary.loc[m, 'Total Application'] = total
        df_summary.loc[m, 'Searched'] = s
        df_summary.loc[m, "Examiner's First Report or Total Provisional Refusal"] = et

        for t in ["Search Recorded", "Examiner's First Report", "Total Provisional Refusal"]:
            print(t)
            df_international = df[(df[6] == t)]
            # print(t, len(df_international))
            df_international['days'] = (
                    pd.to_datetime(df_international[7]) - pd.to_datetime(df_international[1])).dt.days
            df_international.columns = ['ST13Applicationnumber', 'ApplicationDate', 'InternationalMarkIdentifier',
                                        'markcurrentstatusinternaldescriptiontext', 'proc_date', 'countrycode',
                                        'MarkEventDescriptionText', 'MarkEventDate', 'days from filing to searched']
            print('before:', len(df_international))
            df_international = df_international.drop_duplicates(subset=['ST13Applicationnumber'], keep='last')
            print('after:', len(df_international))
            if t == "Examiner's First Report":
                df_international.to_excel(writer, sheet_name='Int_EFR_{}months'.format(str(month)), index=None)
            elif t == "Total Provisional Refusal":
                df_international.to_excel(writer, sheet_name='Int_TPR_{}months'.format(str(month)), index=None)
            elif t == "Search Recorded":
                df_international.to_excel(writer, sheet_name='Int_SR_{}months'.format(str(month)), index=None)
            if t == 'Search Recorded':
                average_days = df_international['days from filing to searched'].mean()
                median_days = df_international['days from filing to searched'].median()
                df_summary.loc[m, 'Average days'] = average_days
                df_summary.loc[m, 'Median days'] = median_days
                df_summary.loc[m, 'Average months'] = average_days / 30
                df_summary.loc[m, 'Median months'] = median_days / 30

    for m, month in enumerate([30, 24, 18, 12, 6]):
        query0 = """
                  select tm.ST13Applicationnumber,tm.ApplicationDate,tm.InternationalMarkIdentifier,nti.markcurrentstatusinternaldescriptiontext,tm.proc_date,app.countrycode,me.MarkEventDescriptionText,me.MarkEventDate
                  from 
                  ipv_db.ca_tm_trademark tm 
                  left outer join ipv_db.ca_tm_applicant app
                  on
                  tm.st13applicationnumber=app.st13applicationnumber and tm.proc_date=app.proc_date
                  left outer join ipv_db.ca_tm_national_trademark_information nti
                  on
                  tm.st13applicationnumber=nti.st13applicationnumber and tm.proc_date=nti.proc_date
                  left join ipv_db.ca_tm_mark_event me 
                  on tm.st13applicationnumber=me.st13applicationnumber and tm.proc_date=me.proc_date 
                  right join (
                             select st13applicationnumber,max(proc_date) proc_date
                             from ipv_db.ca_tm_trademark 
                             group by st13applicationnumber
                            ) AS newrecord on (tm.st13applicationnumber = newrecord.st13applicationnumber and tm.proc_date = newrecord.proc_date) 
                  where tm.ApplicationDate > months_sub(now(), {})
                  and tm.InternationalMarkIdentifier ='-'
                """.format(str(month))
        # where nti.markcurrentstatusinternaldescriptiontext= 'Searched'
        impala_cur.execute(query0)
        data = impala_cur.fetchall()
        df = pd.DataFrame(data)
        total = df[0].nunique()
        s = df[df[6] == 'Search Recorded'][0].nunique()
        et = df[(df[6] == "Examiner's First Report") | (df[6] == "Total Provisional Refusal")][0].nunique()
        # print('Total application',total)
        # print('Searched application',s)
        # print('exam.. total..',et)
        df_summary.loc[m + 5, 'Type'] = 'CA'
        df_summary.loc[m + 5, 'Month'] = month
        df_summary.loc[m + 5, 'Total Application'] = total
        df_summary.loc[m + 5, 'Searched'] = s
        df_summary.loc[m + 5, "Examiner's First Report or Total Provisional Refusal"] = et

        for t in ["Search Recorded", "Examiner's First Report", "Total Provisional Refusal"]:
            print(t)
            df_ca = df[(df[6] == t)]
            df_ca['days'] = (pd.to_datetime(df_ca[7]) - pd.to_datetime(df_ca[1])).dt.days
            df_ca.columns = ['ST13Applicationnumber', 'ApplicationDate', 'InternationalMarkIdentifier',
                             'markcurrentstatusinternaldescriptiontext', 'proc_date', 'countrycode',
                             'MarkEventDescriptionText', 'MarkEventDate', 'days from filing to searched']
            print('before:', len(df_ca))
            df_ca = df_ca.drop_duplicates(subset=['ST13Applicationnumber'], keep='last')
            print('after:', len(df_ca))
            if t == "Examiner's First Report":
                df_ca.to_excel(writer, sheet_name='CA_EFR_{}months'.format(str(month)), index=None)
            elif t == "Total Provisional Refusal":
                df_ca.to_excel(writer, sheet_name='CA_TPR_{}months'.format(str(month)), index=None)
            elif t == "Search Recorded":
                df_ca.to_excel(writer, sheet_name='CA_SR_{}months'.format(str(month)), index=None)
            if t == 'Search Recorded':
                average_days = df_ca['days from filing to searched'].mean()
                median_days = df_ca['days from filing to searched'].median()
                df_summary.loc[m + 5, 'Average days'] = average_days
                df_summary.loc[m + 5, 'Median days'] = median_days
                df_summary.loc[m + 5, 'Average months'] = average_days / 30
                df_summary.loc[m + 5, 'Median months'] = median_days / 30
    df_summary.to_excel(writer, sheet_name='Summary', index=None)
    writer.save()
    #############################################################################
    # Get credential for EMail notification
    #############################################################################
    # CIPO Unrepresented - Searched Report: October 2020
    td = pd.to_datetime('today')

    def get_mail_params(rfile):
        mail_params = cfg.mail_params

        var_params = {
            'text': '',
            'subject': 'CIPO Processing Time Report: {} {}'.format(td.strftime("%B"), td.strftime("%Y")),
            'attach_file': rfile,
        }

        mail_params.update(var_params)

        return mail_params

    send_mail(get_mail_params('processingtime_report.xlsx'))
    print('email sent')

    query = "update etl_db.reports_status set status=1 where proc_date='{}' and report_name='report_processingtime'".format(
        proc_date)
    impala_cur.execute(query)


if __name__ == "__main__":
    try:
        print('=' * 30)
        print('Getting Processing Time Report')
        print('=' * 30)
        try:
            send_search(sys.argv[1])
        except:
            send_search()

    except Exception as err:
        print('fail')
        print(err)
