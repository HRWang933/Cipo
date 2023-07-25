# -*- coding: utf-8 -*-
import sys

sys.path.append('../')

import pandas as pd
from impala.dbapi import connect
import importlib
import re
from routines.send_mail import send_mail

cfg = importlib.import_module('.cfg', 'config')


def send_historyAC(reportType=None):
    impala_con = connect(host=cfg.impala_host)
    impala_cur = impala_con.cursor()
    proc_date = ''
    if reportType == 'new':
        query = 'select max(proc_date) from ipv_db.ca_tm_trademark'
        impala_cur.execute(query)
        data = impala_cur.fetchall()
        proc_date = data[0][0]

        query = "select status from etl_db.reports_status where proc_date='{}' and report_name='report_historyAC'".format(
            proc_date)

        impala_cur.execute(query)
        data = impala_cur.fetchall()
        status = data[0][0]

        if status == 1:
            print('no new data uploaded, skip')
            return

    writer = pd.ExcelWriter('report_history_action_code.xlsx', engine='xlsxwriter')
    table_List = ['ca_tm_mark_event', 'ca_tm_cancellationproceeding_events', 'ca_tm_oppositionproceeding_events']
    sheetname_List = ['MarkEvent', 'CancellationProceedings', 'OppositionProceedings']
    for t_no, tb in enumerate(table_List):
        # if t_no != 0 : continue
        impala_con = connect(host=cfg.impala_host)
        impala_cur = impala_con.cursor()
        impala_cur.execute('DROP TABLE IF EXISTS ipv_db.history_action_code;')
        impala_cur.execute(
            'CREATE TABLE IF NOT EXISTS ipv_db.history_action_code (proc_date string, action_code string);')
        queryd = """
                  select distinct proc_date from ipv_db.ca_tm_trademark order by proc_date 
                """
        impala_cur.execute(queryd)
        data = impala_cur.fetchall()
        df_proc_date = pd.DataFrame(data)
        for dt in df_proc_date[0].tolist():
            # print(dt)

            query0 = """
                      select * from ipv_db.history_action_code where proc_date = '{}'
                    """.format(dt)
            impala_cur.execute(query0)
            data = impala_cur.fetchall()
            # print(len(data))
            if len(data) != 0:
                continue

            query1 = """
                      insert into ipv_db.history_action_code
                      select distinct proc_date,markeventdescriptiontext from ipv_db.{} where proc_date = '{}'
                    """.format(tb, dt)
            impala_cur.execute(query1)
            # data = impala_cur.fetchall()
            # df_actioncode = pd.DataFrame(data)
            # print(df_actioncode)

            # print(df_actioncode[0].str.cat(sep=','))
            #
            # query2 = """
            #    insert into ipv_db.history_action_code
            #    select "{}" as proc_date,{} as count, "{}" as action_code
            #         """.format(dt,len(df_actioncode[0]),df_actioncode[0].str.cat(sep=','))
            # impala_cur.execute(query2)

        query3 = """
                  select * from ipv_db.history_action_code order by proc_date
                """
        impala_cur.execute(query3)
        data = impala_cur.fetchall()
        df_report = pd.DataFrame(data)
        df_report.columns = ['proc_date', 'action_code']
        # print(df_report)
        clms = ['source', 'action_code', 'new', 'remove']
        for i, proc_date in enumerate(df_report['proc_date'].unique()):
            clms.append(proc_date)
        df_summary = pd.DataFrame(columns=clms)
        for i, actioncode in enumerate(df_report['action_code'].unique()):
            # print(i,actioncode)
            df_summary.loc[i, 'source'] = sheetname_List[t_no]
            df_summary.loc[i, 'action_code'] = actioncode
            tmp_1code = df_report[df_report['action_code'] == actioncode]
            # print(len(tmp_1code))
            bool_first = False
            bool_inuselastmonth = False
            for j, proc_date in enumerate(df_report['proc_date'].unique()):
                if len(tmp_1code[tmp_1code['proc_date'] == proc_date]) != 0:
                    df_summary.loc[i, proc_date] = 1
                    df_summary.loc[i, 'remove'] = ''
                    bool_inuselastmonth = True
                    if bool_first == False:
                        df_summary.loc[i, 'new'] = proc_date
                        bool_first = True
                else:
                    df_summary.loc[i, proc_date] = 0
                    if bool_inuselastmonth:
                        bool_inuselastmonth = False
                        df_summary.loc[i, 'remove'] = proc_date

                        #    print(row['proc_date'])
        #    if i ==0:
        #        prevList = row['action_code']
        #    else:
        #        newList = []
        #        removeList = []
        #        #print(prevList)
        #        #print(row['action_code'])
        #        for n in row['action_code'].split(','):
        #            if n not in prevList:
        #                #print('new:',n)
        #                newList.append(n)
        #        for p in prevList.split(','):
        #            if p not in row['action_code'].split(','):
        #                #print('old:',p)
        #                removeList.append(p)
        #        print('New:',newList)
        #        print('Remove:',removeList)
        #        prevList = row['action_code']
        #        df_report.loc[i,'new'] = ','.join(newList)
        #        df_report.loc[i,'removed'] = ','.join(removeList)
        df_summary = df_summary.loc[:, ['source', 'action_code', 'new']]
        df_summary.to_excel(writer, sheet_name=sheetname_List[t_no], index=None)
        print(df_summary.shape)
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
            'subject': 'CIPO History Action Code Report: {} {}'.format(td.strftime("%B"), td.strftime("%Y")),
            'attach_file': rfile,
        }

        mail_params.update(var_params)

        return mail_params

    send_mail(get_mail_params('report_history_action_code.xlsx'))
    print('email sent!')

    query = "update etl_db.reports_status set status=1 where proc_date='{}' and report_name='report_historyAC'".format(
        proc_date)
    impala_cur.execute(query)


if __name__ == "__main__":
    try:
        print('=' * 30)
        print('CIPO History Action Code Report')
        print('=' * 30)
        try:
            send_historyAC(sys.argv[1])
        except:
            send_historyAC()

    except Exception as err:
        print('fail')
        print(err)
