import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_trademark_use_right'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'UseRightText STRING,'            
            'UseRightIndicator STRING,'            
            'PRIMARY KEY(ST13ApplicationNumber,proc_date,UseRightText)) STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'UseRightText STRING,'            
            'UseRightIndicator STRING)  ')            

model = helpers.tbl_model(table, [body, body_ext])
