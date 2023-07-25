import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_claim'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'ClaimCategoryType STRING,'
            'ClaimNumber STRING,'
            'ClaimTypeDescription_en STRING,'
            'ClaimCode BIGINT,'
            'StructuredClaimDate STRING,'
            'ClaimYear STRING,'
            'ClaimMonth STRING,'
            'ClaimDay STRING,'
            'ClaimCountryCode BIGINT,'
            'ClaimForeignRegistrationNbr STRING,'
            'ClaimAdditionalInfo STRING,'
            'ClaimText STRING,'
            'GoodsServicesReferenceIdentifier STRING,'
            'PRIMARY KEY(ST13ApplicationNumber,proc_date,ClaimCategoryType,ClaimNumber)) STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'ClaimCategoryType STRING,'
            'ClaimNumber STRING,'
            'ClaimTypeDescription_en STRING,'
            'ClaimCode BIGINT,'
            'StructuredClaimDate STRING,'
            'ClaimYear STRING,'
            'ClaimMonth STRING,'
            'ClaimDay STRING,'
            'ClaimCountryCode BIGINT,'
            'ClaimForeignRegistrationNbr STRING,'
            'ClaimAdditionalInfo STRING,'
            'ClaimText STRING,'
            'GoodsServicesReferenceIdentifier STRING)    ') 

model = helpers.tbl_model(table, [body, body_ext])
