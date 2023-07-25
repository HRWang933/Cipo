import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'fee_main'
body   =   ('(patent_no STRING,'
            'app_id BIGINT,'
            's_entity STRING,'
            'app_filing_date STRING,'
            'grant_issue_date STRING,'
            'mfe_entry_date STRING,'
            'code STRING,'
            'proc_date STRING) ')

body_ext = ('(patent_no STRING,'
            'app_id BIGINT,'
            's_entity STRING,'
            'app_filing_date STRING,'
            'grant_issue_date STRING,'
            'mfe_entry_date STRING,'
            'code STRING) ')

model = helpers.tbl_model(table, [body, body_ext])
