import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_legislation'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'LegislationCode BIGINT,'
            'LegislationDescription_en STRING,'
            'LegislationDescription_fr STRING,'
            'PRIMARY KEY(ST13ApplicationNumber,proc_date)) STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'LegislationCode BIGINT,'
            'LegislationDescription_en STRING,'
            'LegislationDescription_fr STRING)    ') 

model = helpers.tbl_model(table, [body, body_ext])
