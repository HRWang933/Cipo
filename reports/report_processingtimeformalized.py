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
    if reportType == 'new':
        today_date = pd.to_datetime('now').strftime('%Y-%m-%d')
        queryPre = "select * from ipv_db.ca_tm_trademark where proc_date = 'W{}'".format(today_date)
        print(queryPre)
        impala_cur.execute(queryPre)
        data = impala_cur.fetchall()
        if len(data)==0:
            print('no data uploaded today,skip')
            return

    impala_cur.execute('DROP TABLE IF EXISTS ipv_db.tmp1;')
    impala_cur.execute('DROP TABLE IF EXISTS ipv_db.tmp2;')
    impala_cur.execute('CREATE TABLE IF NOT EXISTS ipv_db.tmp1 (st13applicationnumber bigint,proc_date string);')
    impala_cur.execute('CREATE TABLE IF NOT EXISTS ipv_db.tmp2 (st13applicationnumber bigint,markeventdate string);')
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
              where app.nationallegalentitycode='CA'
              and nti.markcurrentstatusinternaldescriptiontext= 'Searched'
              and app.st13applicationnumber not in (select r.st13applicationnumber from ipv_db.ca_tm_national_representative r)
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
             where markeventcode in (20,22,15,12,18,23)
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
    select distinct 'SEARCHED' as MailerType,a.st13applicationnumber,substr(cast(a.st13applicationnumber as string),7,7) as Fileid
    ,substr(cast(a.st13applicationnumber as string),14,2) as ExtensionCounter
    ,CASE
    
    WHEN c.applicationlanguagecode = 'en' AND (int_months_between(b.markeventresponsedate,NOW()) BETWEEN 0 AND 2) THEN 'US3_E_1'
    WHEN c.applicationlanguagecode = 'fr' AND (int_months_between(b.markeventresponsedate,NOW()) BETWEEN 0 AND 2) THEN 'US3_F_1'
    WHEN c.applicationlanguagecode = 'en' AND (int_months_between(b.markeventresponsedate,NOW()) BETWEEN 3 AND 4) THEN 'US2_E_1'
    WHEN c.applicationlanguagecode = 'fr' AND (int_months_between(b.markeventresponsedate,NOW()) BETWEEN 3 AND 4) THEN 'US2_F_1'
    WHEN c.applicationlanguagecode = 'en' AND (int_months_between(b.markeventresponsedate,NOW()) >= 5) THEN 'US1_E_1'
    WHEN c.applicationlanguagecode = 'fr' AND (int_months_between(b.markeventresponsedate,NOW()) >- 5) THEN 'US1_F_1'
    ELSE ''
    END as CardType
    ,d.legalentityname,d.addresslinetext1,d.addresslinetext2,d.geographicregionname,d.countrycode,d.postalcode
    ,CASE
    when e.marksignificantverbalelementtext='-' then concat('TM: ' , substr(cast(a.st13applicationnumber as string),7,7) , ' - ' , ISNULL(f.indexheadingtext1,''))
    else concat('TM: ' , substr(cast(a.st13applicationnumber as string),7,7) , ' - ' , ISNULL(e.marksignificantverbalelementtext,''))
    END as Text1_TMNumber
    ,CASE
    WHEN c.applicationlanguagecode = 'en' THEN 'STATUS: SEARCHED'
    WHEN c.applicationlanguagecode = 'fr' THEN 'STATUS: A FAIT L’OBJET D’UNE RECHERCHE'
    END as Text2_Status
    ,CASE
    WHEN c.applicationlanguagecode = 'en' THEN concat("CIPO RESPONSE DEADLINE: ",from_unixtime(unix_timestamp(b.markeventresponsedate),'MMM'),' ',from_unixtime(unix_timestamp(b.markeventresponsedate),'dd'),' ',from_unixtime(unix_timestamp(b.markeventresponsedate),'yyyy'))
    
    WHEN c.applicationlanguagecode = 'fr' THEN concat("DATE LIMITE DE RÉPONSE DE L'OPIC: ",from_unixtime(unix_timestamp(b.markeventresponsedate),'MMM'),' ',from_unixtime(unix_timestamp(b.markeventresponsedate),'dd'),' ',from_unixtime(unix_timestamp(b.markeventresponsedate),'yyyy'))
    END as Text3
    ,c.proc_date
    
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
    
    where markeventcode in (20,22,15,12,18,23) and markeventresponsedate<>'-' and markeventresponsedate<>' '
    and c.proc_date=(select max(cc.proc_date) from ipv_db.ca_tm_trademark cc where cc.st13applicationnumber=c.st13applicationnumber)
    and d.proc_date=(select max(dd.proc_date) from ipv_db.ca_tm_applicant dd where dd.st13applicationnumber=d.st13applicationnumber)
    and e.proc_date=(select max(ee.proc_date) from ipv_db.ca_tm_markrepresentation ee where ee.st13applicationnumber=e.st13applicationnumber)
    and f.proc_date=(select max(ff.proc_date) from ipv_db.ca_tm_index_heading ff where ff.st13applicationnumber=f.st13applicationnumber)
    and b.markeventresponsedate>NOW()
    and a.st13applicationnumber not in (select distinct st13applicationnumber from ipv_db.mailer_blacklist where st13applicationnumber is not NULL) 
    order by a.st13applicationnumber
             """
    impala_cur.execute(query2)
    data = impala_cur.fetchall()
    df_data = pd.DataFrame(data)
    #print(len(df_data))
    df_data.columns = ['mailertype','st13applicationnumber','fileid','extensioncounter','cardtype','legalentityname','addresslinetext1','addresslinetext2','geographicregionname','countrycode','postalcode','text1_tmnumber','text2_status','text3','proc_date']
    df_data['entityname_lower'] = df_data['legalentityname'].str.lower()
    df_final = df_data
    df_final['drop'] = 0
    for x,row in df_final.iterrows():
        for b in df_blacklistName['entityname_bl'].unique():
            if row['entityname_lower'] in b: 
                #print(x,row['entityname_lower'],b)
                df_final.loc[x,'drop'] =1
                break
            elif b in row['entityname_lower']:
                if len(b.split()) == 1:
                    if b+' ' in row['entityname_lower']:
                        pass
                    elif ' '+b in row['entityname_lower']:
                        pass
                    else:
                        continue
    
                #print(x,row['entityname_lower'],b)
                df_final.loc[x,'drop'] =1
                break
    df_final = df_final[df_final['drop']==0]
    df_final = df_final.drop('drop',axis=1)
    df_final = df_final.drop('entityname_lower',axis=1)
    # get city
    postcode_list = ''
    for p_no,p in enumerate(df_final['postalcode'].values):
        if p_no == len(df_final)-1:
            postcode_list += '"' + p + '"'
        else:
            postcode_list += '"' + p + '",'
    query4 = """
             select * from ipv_db.city_postcode where postcode in ({});
             """.format(postcode_list)
    impala_cur.execute(query4)
    data1= impala_cur.fetchall()
    df_city = pd.DataFrame(data1)
    df_city.columns = ['county','postcode','city','state']
    df_final = df_final.merge(df_city[['postcode','city']], how = 'left',left_on = 'postalcode', right_on = 'postcode')
    df_final = df_final.drop('postcode',axis=1)
    #print(df_final.shape)
    df_final = df_final.loc[:,['mailertype','st13applicationnumber','fileid','extensioncounter','cardtype','legalentityname','addresslinetext1','addresslinetext2','city','geographicregionname','countrycode','postalcode','text1_tmnumber','text2_status','text3','proc_date']]
    for i,row in df_final.iterrows():
        if row['city'] =='' or pd.isnull(row['city']): continue
        tmp_str = re.sub('Montr\\xc3\\xa9al','Montreal',row['addresslinetext2'])
        tmp_str = re.sub('Qu\\xc3\\xa9bec', 'Quebec',tmp_str)
        if re.search(row['city'],tmp_str , re.IGNORECASE):
            #print(i, row['addresslinetext2'], row['city'])
            extra_string = re.sub(row['city'].lower()+'[\,]?','',tmp_str.lower()).strip()
            if extra_string =='':
                df_final.loc[i,'addresslinetext2'] = row['city']
                #print('1:',i, row['addresslinetext2'], row['city'])
            else:
                extra_string = re.sub(row['city']+'[\,]?','',tmp_str).strip()
                df_final.loc[i,'addresslinetext1'] += ', '+extra_string
                df_final.loc[i,'addresslinetext2'] = row['city']
                #print('2:',i, row['addresslinetext2'], row['city'])
            pass
        else:
            #print(i, row['addresslinetext2'], row['city'])
            df_final.loc[i,'addresslinetext1'] += ', '+df_final.loc[i,'addresslinetext2'] 
            df_final.loc[i,'addresslinetext2'] = row['city']

    df_final = df_final.drop('city',axis=1)
    df_final.to_excel('formalized_ptime.xlsx',index=None, engine='openpyxl')
    print(df_final.shape)
    #############################################################################
    # Get credential for EMail notification
    #############################################################################
    #CIPO Unrepresented - Searched Report: October 2020
    td = pd.to_datetime('today')
    def get_mail_params(rfile):
        mail_params =  cfg.mail_params
    
        var_params  = {
            'text'     : '',
            'subject'  : 'CIPO Unrepresented Formalized – Processing time: {} {}'.format(td.strftime("%B"), td.strftime("%Y")),
            'attach_file': rfile,
            }
    
        mail_params.update(var_params)
    
        return mail_params
    send_mail(get_mail_params('formalized_ptime.xlsx'))
    print('email sent')
if __name__ == "__main__":
    try:
	print('='*30)
	print('Getting CIPO Unrepresented Formalized – Processing time')
	print('='*30)
        try:
            send_search(sys.argv[1])
        except:
            send_search()

    except Exception as err:
        print('fail')
        print(err)
