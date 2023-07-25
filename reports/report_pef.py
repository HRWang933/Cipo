# -*- coding: utf-8 -*-
from __future__ import division
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
import datetime

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

        query = "select status from etl_db.reports_status where proc_date='{}' and report_name='report_pef'".format(
            proc_date)

        impala_cur.execute(query)
        data = impala_cur.fetchall()
        status = data[0][0]

        if status == 1:
            print('no new data uploaded, skip')
            return

    impala_cur.execute('DROP TABLE IF EXISTS ipv_db.tmp1;')
    impala_cur.execute('DROP TABLE IF EXISTS ipv_db.tmp2;')
    impala_cur.execute('CREATE TABLE IF NOT EXISTS ipv_db.tmp1 (st13applicationnumber bigint,proc_date string);')
    impala_cur.execute('CREATE TABLE IF NOT EXISTS ipv_db.tmp2 (st13applicationnumber bigint,markeventdate string);')
    impala_cur.execute('CREATE TABLE IF NOT EXISTS ipv_db.pef (st13applicationnumber bigint,cardtype string);')
    query0 = """
              insert into ipv_db.tmp1
              select distinct tm.st13applicationnumber,tm.proc_date
              from ipv_db.ca_tm_trademark tm left outer join ipv_db.ca_tm_applicant app
              on
              tm.st13applicationnumber=app.st13applicationnumber and tm.proc_date=app.proc_date
              left outer join ipv_db.ca_tm_national_trademark_information nti
              on
              tm.st13applicationnumber=nti.st13applicationnumber and tm.proc_date=nti.proc_date
              right join (
                         select st13applicationnumber,max(proc_date) proc_date
                         from ipv_db.ca_tm_trademark 
                         group by st13applicationnumber
                         order by st13applicationnumber
                        ) AS newrecord on (tm.st13applicationnumber = newrecord.st13applicationnumber and tm.proc_date = newrecord.proc_date) 
              where  nti.markcurrentstatusinternaldescriptiontext in ("Formalized","Default Formalized")
              and app.st13applicationnumber not in (select r.st13applicationnumber from ipv_db.ca_tm_national_representative r)
              and tm.InternationalMarkIdentifier = '-'
              and tm.st13applicationnumber not in (select distinct(me.st13applicationnumber) from ipv_db.ca_tm_mark_event me where me.markeventcode in(27,26));
              
            """
    impala_cur.execute(query0)

    query1 = """
             insert into ipv_db.tmp2
             select a.st13applicationnumber,max(b.markeventdate)
             from ipv_db.tmp1 a 
             inner join ipv_db.ca_tm_mark_event b
             on a.st13applicationnumber=b.st13applicationnumber and a.proc_date=b.proc_date
             right join (
                        select st13applicationnumber,max(proc_date) proc_date
                        from ipv_db.ca_tm_trademark 
                        group by st13applicationnumber
                       ) AS newrecord on (a.st13applicationnumber = newrecord.st13applicationnumber and a.proc_date = newrecord.proc_date) 
             where markeventcode not in (10,5,180,20,22)
             group by a.st13applicationnumber
             """
    impala_cur.execute(query1)

    query3 = """
             select lower(entityname) from ipv_db.mailer_blacklist where entityname is not NULL;
             """
    impala_cur.execute(query3)
    data = impala_cur.fetchall()
    df_blacklistName = pd.DataFrame(data)
    df_blacklistName.columns = ['entityname_bl']

    query2 = """
    select distinct UPPER(g.markcurrentstatusinternaldescriptiontext) as MailerType,a.st13applicationnumber,substr(cast(a.st13applicationnumber as string),7,7) as Fileid
    ,substr(cast(a.st13applicationnumber as string),14,2) as ExtensionCounter
    ,CASE
    WHEN c.applicationlanguagecode = 'en' THEN 'UEXP_1_E'
    WHEN c.applicationlanguagecode = 'fr' THEN 'UEXP_1_F'
    ELSE ''
    END as CardType
    ,d.legalentityname,d.addresslinetext1,d.addresslinetext2,d.geographicregionname,d.countrycode,d.postalcode
    ,CASE
    when e.marksignificantverbalelementtext='-' then concat('TM: ' , substr(cast(a.st13applicationnumber as string),7,7) , ' - ' , ISNULL(f.indexheadingtext1,''))
    else concat('TM: ' , substr(cast(a.st13applicationnumber as string),7,7) , ' - ' , ISNULL(e.marksignificantverbalelementtext,''))
    END as Text1_TMNumber
    ,CASE
    WHEN c.applicationlanguagecode = 'en' THEN 'STATUS: FORMALIZED'
    WHEN c.applicationlanguagecode = 'fr' THEN 'STATUS: FORMALISÉE'
    END as Text2_Status
    , c.ApplicationDate as Text3
    ,c.proc_date,b.markeventcode,h.addresslinetext1,h.addresslinetext2,h.addresslinetext3,h.geographicregionname,h.countrycode,h.postalcode
    
    --,markeventdescriptiontext,a.markeventdate,b.markeventresponsedate
    from ipv_db.tmp2 a inner join ipv_db.ca_tm_mark_event b
    on
    a.st13applicationnumber=b.st13applicationnumber and a.markeventdate=b.markeventdate
    left outer join ipv_db.ca_tm_trademark c
    on
    a.st13applicationnumber=c.st13applicationnumber
    left outer join ipv_db.ca_tm_applicant d
    on
    a.st13applicationnumber=d.st13applicationnumber
    left outer join ipv_db.ca_tm_markrepresentation e
    on
    a.st13applicationnumber=e.st13applicationnumber
    left outer join ipv_db.ca_tm_index_heading f
    on
    a.st13applicationnumber=f.st13applicationnumber
    left outer join ipv_db.ca_tm_national_trademark_information g
    on
    a.st13applicationnumber=g.st13applicationnumber
    left outer join ipv_db.ca_tm_national_correspondent h
    on
    a.st13applicationnumber=h.st13applicationnumber
    
    where c.proc_date=(select max(cc.proc_date) from ipv_db.ca_tm_trademark cc where cc.st13applicationnumber=c.st13applicationnumber)
    and d.proc_date=(select max(dd.proc_date) from ipv_db.ca_tm_applicant dd where dd.st13applicationnumber=d.st13applicationnumber)
    and e.proc_date=(select max(ee.proc_date) from ipv_db.ca_tm_markrepresentation ee where ee.st13applicationnumber=e.st13applicationnumber)
    and f.proc_date=(select max(ff.proc_date) from ipv_db.ca_tm_index_heading ff where ff.st13applicationnumber=f.st13applicationnumber)
    and a.st13applicationnumber not in (select distinct st13applicationnumber from ipv_db.mailer_blacklist where st13applicationnumber is not NULL) 
    and c.InternationalMarkIdentifier = '-'
    and c.MarkCategory in ('Certification mark','Trademark')
    order by a.st13applicationnumber
             """
    # markeventcode not in (20,22,15,12,18,23) and
    #    and b.markeventresponsedate>NOW()
    impala_cur.execute(query2)
    data = impala_cur.fetchall()
    df_data = pd.DataFrame(data)
    df_data.columns = ['mailertype', 'st13applicationnumber', 'fileid', 'extensioncounter', 'cardtype',
                       'legalentityname', 'addresslinetext1', 'addresslinetext2', 'geographicregionname', 'countrycode',
                       'postalcode', 'text1_tmnumber', 'text2_status', 'text3', 'proc_date', 'markeventcode',
                       'nc_addresslinetext', 'nc_addresslinetext2', 'nc_addresslinetext3', 'nc_geographicregionname',
                       'nc_countrycode', 'nc_postalcode']
    exclude_list = df_data.loc[df_data['markeventcode'].isin([20, 22, 5, 10, 180]), 'st13applicationnumber'].tolist()
    df_data = df_data[~df_data['st13applicationnumber'].isin(exclude_list)]
    # Please make sure that you exclude all applications with an address for service in CA address except where the address for service postal code matches the applicant's postal code. I can still see for instance, application # 1917419, 1947024, 1979810, 1995224
    df_data = df_data[~((df_data['nc_countrycode'] == 'CA') & (df_data['nc_postalcode'] != df_data['postalcode']))]
    # Also please make sure that if "-" shows up for address for service to exclude it as well.
    df_data = df_data[df_data['nc_addresslinetext'] != '-']

    df_data['entityname_lower'] = df_data['legalentityname'].str.lower()
    df_final = df_data
    df_final['drop'] = 0
    # print('black listed')
    for x, row in df_final.iterrows():
        for b in df_blacklistName['entityname_bl'].unique():
            if row['entityname_lower'] in b:
                # print(x,row['entityname_lower'],b)
                df_final.loc[x, 'drop'] = 1
                break
            elif b in row['entityname_lower']:
                if len(b.split()) == 1:
                    if b + ' ' in row['entityname_lower']:
                        pass
                    elif ' ' + b in row['entityname_lower']:
                        pass
                    else:
                        continue

                # print(x,row['entityname_lower'],b)
                df_final.loc[x, 'drop'] = 1
                break
    df_final = df_final[df_final['drop'] == 0]
    df_final = df_final.drop('drop', axis=1)
    df_final = df_final.drop('entityname_lower', axis=1)
    # get city
    query4 = """
             select * from ipv_db.city_postcode;
             """
    impala_cur.execute(query4)
    data1 = impala_cur.fetchall()
    df_city = pd.DataFrame(data1)
    df_city.columns = ['county', 'postcode', 'city', 'state']
    # problem: postalcode is small letter
    df_final['tmp_upper'] = df_final['postalcode'].str.upper()
    df_final = df_final.merge(df_city[['postcode', 'city']], how='left', left_on='tmp_upper', right_on='postcode')
    df_final = df_final.drop('postcode', axis=1)
    #    #print(df_final.shape)
    df_final = df_final.loc[:,
               ['mailertype', 'st13applicationnumber', 'fileid', 'extensioncounter', 'cardtype', 'legalentityname',
                'addresslinetext1', 'addresslinetext2', 'city', 'geographicregionname', 'countrycode', 'postalcode',
                'text1_tmnumber', 'text2_status', 'text3', 'proc_date', 'markeventcode', 'nc_addresslinetext',
                'nc_addresslinetext2', 'nc_addresslinetext3', 'nc_geographicregionname', 'nc_countrycode',
                'nc_postalcode']]
    df_final['text4'] = ((pd.to_datetime('now') - pd.to_datetime(df_final['text3'])).dt.days / 30).astype('int')
    # Text 3: Please convert the dates from: 2019-06-17 to display as June 17, 2019 instead  
    df_final['text3'] = pd.to_datetime(df_final['text3'])
    df_final = df_final[df_final['text4'] > 12]
    datetime_lapse = pd.to_datetime('now') - datetime.datetime(2021, 6, 06, 00, 00, 00)
    cardtype_nu = 1
    if datetime_lapse.days < 60:
        pass
    elif datetime_lapse.days < 120:
        cardtype_nu = 2
    elif datetime_lapse.days < 180:
        cardtype_nu = 3

    df_final = df_final.drop_duplicates(subset=['st13applicationnumber'], keep='last')
    # cardtype
    query = """
            select st13applicationnumber from ipv_db.pef 
            """
    impala_cur.execute(query)
    data = impala_cur.fetchall()
    df_pef = pd.DataFrame(data)
    existing_list = df_pef[0].to_list()
    for i, row in df_final.iterrows():
        # if row['st13applicationnumber'] !=300000200001700: continue
        # print(row['st13applicationnumber'],row['city'],row['addresslinetext1'],row['addresslinetext2'],row['postalcode'])
        if pd.isnull(row['city']): continue
        tmp_str = re.sub('Montr\\xc3\\xa9al', 'Montreal', row['addresslinetext2'])
        tmp_str = re.sub('Qu\\xc3\\xa9bec', 'Quebec', tmp_str)
        if re.search(row['city'], tmp_str, re.IGNORECASE):
            # print(i, row['addresslinetext2'], row['city'])
            extra_string = re.sub(row['city'].lower() + '[\,]?', '', tmp_str.lower()).strip()
            if extra_string == '':
                df_final.loc[i, 'addresslinetext2'] = row['city']
                # print('1:',i, row['addresslinetext2'], row['city'])
            else:
                extra_string = re.sub(row['city'] + '[\,]?', '', tmp_str).strip()
                df_final.loc[i, 'addresslinetext1'] += ', ' + extra_string
                df_final.loc[i, 'addresslinetext2'] = row['city']
                # print('2:',i, row['addresslinetext2'], row['city'])
        elif tmp_str.replace(' ', '').lower() == row['postalcode'] or re.search('^\d+$', tmp_str):
            df_final.loc[i, 'addresslinetext2'] = row['city']
        else:
            # print(i, row['addresslinetext2'], row['city'])
            df_final.loc[i, 'addresslinetext1'] += ', ' + df_final.loc[i, 'addresslinetext2']
            df_final.loc[i, 'addresslinetext2'] = row['city']
        if row['st13applicationnumber'] in existing_list:
            if row['cardtype'] == 'UEXP_1_E':
                df_final.loc[i, 'cardtype'] = 'UEXP_{}_E'.format(cardtype_nu)
            elif row['cardtype'] == 'UEXP_1_F':
                df_final.loc[i, 'cardtype'] = 'UEXP_{}_F'.format(cardtype_nu)

    df_final = df_final.drop(columns=['city', 'markeventcode', 'proc_date'], axis=1)
    # print(df_final['st13applicationnumber'].nunique())

    # text5
    query0 = """
              select distinct tm.st13applicationnumber,tm.proc_date,tm.ApplicationDate,sr.MarkEventDescriptionText,sr.MarkEventDate,ta.RequestSearchCategory
              from ipv_db.ca_tm_trademark tm left outer join ipv_db.ca_tm_applicant app
              on
              tm.st13applicationnumber=app.st13applicationnumber and tm.proc_date=app.proc_date
              left outer join ipv_db.ca_tm_national_trademark_information nti
              on
              tm.st13applicationnumber=nti.st13applicationnumber and tm.proc_date=nti.proc_date
              left outer join ipv_db.ca_tm_trademark_application ta
              on
              tm.st13applicationnumber=ta.st13applicationnumber and tm.proc_date=ta.proc_date
              left outer join (
                              select st13applicationnumber,proc_date,MarkEventDescriptionText,max(MarkEventDate) as MarkEventDate
                              from ipv_db.ca_tm_mark_event me
                              where MarkEventDescriptionText = 'Search Recorded'     
                              group by st13applicationnumber,proc_date,MarkEventDescriptionText
                              ) as sr on (tm.st13applicationnumber = sr.st13applicationnumber and tm.proc_date = sr.proc_date) 
              right join (
                         select st13applicationnumber,max(proc_date) proc_date
                         from ipv_db.ca_tm_trademark 
                         group by st13applicationnumber
                         order by st13applicationnumber
                        ) AS newrecord on (tm.st13applicationnumber = newrecord.st13applicationnumber and tm.proc_date = newrecord.proc_date) 
              where tm.MarkCategory in ('Certification mark','Trademark')
              
            """
    impala_cur.execute(query0)
    data = impala_cur.fetchall()
    df_data = pd.DataFrame(data)
    df_data = df_data[df_data[2] != '-']
    df_data['month'] = (pd.to_datetime('now') - pd.to_datetime(df_data[2])).dt.days / 30
    df_data[2] = pd.to_datetime(df_data[2])
    df_data.sort_values(by=['month'], inplace=True, ascending=False)
    # print(df_data)
    # print('RequestSearchCategory')
    # print(df_data[5].value_counts())
    # text5
    df_final['text5'] = ''
    for i, row in df_final.iterrows():
        # print(row['st13applicationnumber'],row['text3'])
        tmp_total = len(df_data)
        # print('total application:', tmp_total)
        tmp_sr = len(df_data[(df_data[3] == 'Search Recorded') & (df_data[2] >= row['text3'])])
        # print('total search recorded:', tmp_sr)
        ## Text 5: please ensure that the numbers have a "," So for example right now file ID: 0279889 says 1232657 for Text 5. It should read 1,232,657.
        df_final.loc[i, 'text5'] = "{:,}".format(tmp_sr)
    df_final['text3'] = pd.to_datetime(df_final['text3']).dt.strftime('%b %d, %Y')

    # text6
    query0 = """
              select distinct tm.st13applicationnumber,tm.proc_date,tm.ApplicationDate,sr.MarkEventDescriptionText,sr.MarkEventDate,tm.MarkCategory
              from ipv_db.ca_tm_trademark tm left outer join ipv_db.ca_tm_applicant app
              on
              tm.st13applicationnumber=app.st13applicationnumber and tm.proc_date=app.proc_date
              left outer join ipv_db.ca_tm_national_trademark_information nti
              on
              tm.st13applicationnumber=nti.st13applicationnumber and tm.proc_date=nti.proc_date
              left join (
                              select st13applicationnumber,proc_date,MarkEventDescriptionText,max(MarkEventDate) as MarkEventDate
                              from ipv_db.ca_tm_mark_event me
                              where MarkEventDescriptionText = 'Search Recorded'     
                              group by st13applicationnumber,proc_date,MarkEventDescriptionText
                              ) as sr on (tm.st13applicationnumber = sr.st13applicationnumber and tm.proc_date = sr.proc_date) 
              right join (
                         select st13applicationnumber,max(proc_date) proc_date
                         from ipv_db.ca_tm_trademark 
                         group by st13applicationnumber
                         order by st13applicationnumber
                        ) AS newrecord on (tm.st13applicationnumber = newrecord.st13applicationnumber and tm.proc_date = newrecord.proc_date) 
              where sr.MarkEventDescriptionText is NULL
              and nti.markcurrentstatusinternaldescriptiontext in ("Formalized","Default Formalized")
              and tm.MarkCategory in ('Certification mark','Trademark')
              
            """
    impala_cur.execute(query0)
    data = impala_cur.fetchall()
    df_data = pd.DataFrame(data)
    df_data = df_data[df_data[2] != '-']
    df_data['month'] = (pd.to_datetime('now') - pd.to_datetime(df_data[2])).dt.days / 30
    df_data = df_data.sort_values(by=['month'], ascending=False).reset_index(drop=True)
    # print(df_data)
    # print(len(df_data))
    # print(df_data[0].nunique())
    # print(df_data[df_data[2] ==df_data[2].min()])
    # print(df_data.head())
    # print(df_data.loc[0:2,'month'].mean())
    if df_data.loc[0:2, 'month'].mean() >= 36:
        df_final['text6'] = '3 years'
    elif df_data.loc[0:2, 'month'].mean() >= 30:
        df_final['text6'] = '2.5 years'
    elif df_data.loc[0:2, 'month'].mean() >= 24:
        df_final['text6'] = '2 years'
    df_final['text7'] = df_data.loc[0:2, 'month'].mean()
    df_final.to_excel('pef_processingtime.xlsx', index=None, engine='openpyxl')

    # saving list into pef table
    df_list = df_final.loc[:, ['st13applicationnumber', 'cardtype']]
    df_list = df_list[~df_list['st13applicationnumber'].isin(existing_list)].reset_index(drop=1)
    # print(len(df_list))
    str_list = ''
    count = 0
    for i, row in df_list.iterrows():
        # print(i)
        str_tmp = '('
        for j, col in enumerate(row):
            if j == 0:
                str_tmp += str(col) + ","
            else:
                str_tmp += "'" + str(col) + "',"
        str_tmp = re.sub(',$', ')', str_tmp)
        # print(str_tmp)
        if str_list == '':
            str_list += str_tmp
        else:
            str_list += ',' + str_tmp
        count += 1
        if count == 100 or i == (len(df_list) - 1):
            # print(str_list)
            query = """
                    insert into ipv_db.pef (st13applicationnumber, cardtype)
                    VALUES {};
                    """.format(str_list)
            impala_cur.execute(query)
            str_list = ''
            count = 0

    # writer = pd.ExcelWriter('pef_processingtime.xlsx', engine='xlsxwriter')
    # for c in df_final['countrycode'].unique():
    #    tmp = df_final[df_final['countrycode']==c]
    #    try:
    #        tmp.to_excel(writer, sheet_name=c ,index=None)
    #    except Exception as err:
    #        print(err)
    # writer.save()
    print(df_final.shape)
    #############################################################################
    # Get credential for EMail notification
    #############################################################################
    # CIPO Unrepresented - Searched Report: October 2020
    td = pd.to_datetime('today')

    def get_mail_params(rfile):
        mail_params = cfg.mail_params

        var_params = {
            'text': '',
            'subject': 'CIPO Unrepresented Potential Expedited Formalized – Processing time: {} {}'.format(
                td.strftime("%B"), td.strftime("%Y")),
            'attach_file': rfile,
        }

        mail_params.update(var_params)

        return mail_params

    send_mail(get_mail_params('pef_processingtime.xlsx'))
    print('email sent')

    query = "update etl_db.reports_status set status=1 where proc_date='{}' and report_name='report_pef'".format(
        proc_date)
    impala_cur.execute(query)


if __name__ == "__main__":
    try:
        print('=' * 30)
        print('Getting CIPO Unrepresented Potential Expedited Formalized – Processing time')
        print('=' * 30)
        try:
            send_search(sys.argv[1])
        except:
            send_search()

    except Exception as err:
        print('fail')
        print(err)
