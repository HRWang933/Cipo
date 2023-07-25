import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_national_correspondent'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'CommentText STRING,'
            'EntityName_en STRING,'
            'EntityName_fr STRING,'
            'AddressLineText1 STRING,'
            'AddressLineText2 STRING,'
            'AddressLineText3 STRING,'
            'GeographicRegionName STRING,'
            'CountryCode STRING,'
            'PostalCode STRING,'
            'PRIMARY KEY(ST13ApplicationNumber,proc_date)) STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'CommentText STRING,'
            'EntityName_en STRING,'
            'EntityName_fr STRING,'
            'AddressLineText1 STRING,'
            'AddressLineText2 STRING,'
            'AddressLineText3 STRING,'
            'GeographicRegionName STRING,'
            'CountryCode STRING,'
            'PostalCode STRING)    ')

model = helpers.tbl_model(table, [body, body_ext])
