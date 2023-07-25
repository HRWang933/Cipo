import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_categorized_text'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'CategorizedText1 STRING,'
            'C_CategoryCode BIGINT,'
            'CategoryDescription_en STRING,'
            'ChangedDate STRING,'
            'TextLine_en STRING,' 
            'PRIMARY KEY(ST13ApplicationNumber,proc_date)) STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'CategorizedText1 STRING,'
            'C_CategoryCode BIGINT,'
            'CategoryDescription_en STRING,'
            'ChangedDate STRING,'
            'TextLine_en STRING)    ') 

model = helpers.tbl_model(table, [body, body_ext])
