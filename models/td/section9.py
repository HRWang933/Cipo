import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_section9'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'Section9Code BIGINT,'
            'Section9Description_en STRING,'
            'Section9Description_fr STRING,'
            'Section9GCNumber STRING,'
            'PRIMARY KEY(ST13ApplicationNumber,proc_date)) STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'Section9Code BIGINT,'
            'Section9Description_en STRING,'
            'Section9Description_fr STRING,'
            'Section9GCNumber STRING)    ') 

model = helpers.tbl_model(table, [body, body_ext])
