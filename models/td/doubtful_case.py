import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_doubtful_case'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'App_ST13ApplicationNumber STRING,'
            'RegistrationNumber STRING,'
            'IPOfficeCode BIGINT,'
            'PRIMARY KEY(ST13ApplicationNumber,proc_date,App_ST13ApplicationNumber,RegistrationNumber)) STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'App_ST13ApplicationNumber STRING,'
            'RegistrationNumber STRING,'
            'IPOfficeCode BIGINT)   ')

model = helpers.tbl_model(table, [body, body_ext])
