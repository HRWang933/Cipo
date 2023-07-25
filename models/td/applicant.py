import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_applicant'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'LegalEntityName STRING,'
            'EntityName STRING,'
            'AddressLineText1 STRING,'
            'AddressLineText2 STRING,'
            'GeographicRegionName STRING,'
            'CountryCode STRING,'
            'PostalCode STRING,'
            'NationalLegalEntityCode STRING,'
            'PRIMARY KEY(ST13ApplicationNumber,proc_date)) PARTITION BY HASH(ST13ApplicationNumber) PARTITIONS 12 STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'LegalEntityName STRING,'
            'EntityName STRING,'
            'AddressLineText1 STRING,'
            'AddressLineText2 STRING,'
            'GeographicRegionName STRING,'
            'CountryCode STRING,'
            'PostalCode STRING,'
            'NationalLegalEntityCode STRING)  ')

model = helpers.tbl_model(table, [body, body_ext])
