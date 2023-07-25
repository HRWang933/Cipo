import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_authorization'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'AuthorizationDate STRING,'
            'AuthorizationCategory STRING,'
            'CommentText STRING,'  
            'PRIMARY KEY(ST13ApplicationNumber,proc_date)) STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'AuthorizationDate STRING,'
            'AuthorizationCategory STRING,'
            'CommentText STRING)    ')

model = helpers.tbl_model(table, [body, body_ext])
