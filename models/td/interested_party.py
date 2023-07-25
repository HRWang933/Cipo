import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_interested_party'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'InterestedPartyCategory STRING,'
            'EntityName STRING,'
            'AddressLineText1 STRING,'
            'AddressLineText2 STRING,'
            'GeographicRegionName STRING,'
            'CountryCode STRING,'
            'PostalCode STRING,'
            'PRIMARY KEY(ST13ApplicationNumber,proc_date,InterestedPartyCategory)) PARTITION BY HASH(ST13ApplicationNumber) PARTITIONS 12 STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'InterestedPartyCategory STRING,'
            'EntityName STRING,'
            'AddressLineText1 STRING,'
            'AddressLineText2 STRING,'
            'GeographicRegionName STRING,'
            'CountryCode STRING,'
            'PostalCode STRING)    ') 

model = helpers.tbl_model(table, [body, body_ext])
