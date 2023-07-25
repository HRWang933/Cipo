import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_national_trademark_information'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'MarkFeatureCategory STRING,'
            'RegisterCategory STRING,'
            'ApplicationAbandonedDate STRING,'
            'MarkCurrentStatusInternalDescriptionText STRING,'
            'AllowedDate STRING,'
            'RenewalDate STRING,'
            'PRIMARY KEY(ST13ApplicationNumber,proc_date)) STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'MarkFeatureCategory STRING,'
            'RegisterCategory STRING,'
            'ApplicationAbandonedDate STRING,'
            'MarkCurrentStatusInternalDescriptionText STRING,'
            'AllowedDate STRING,'
            'RenewalDate STRING)    ') 

model = helpers.tbl_model(table, [body, body_ext])
