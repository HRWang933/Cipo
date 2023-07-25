import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_goods_services'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'ClassDescriptionBagNumber BIGINT,'
            'ClassificationVersion STRING,'
            'DescriptionClassNumber BIGINT,'
            'GoodsServicesDescriptionText STRING,'
            'ClassificationTermOfficeCode STRING,'
            'ClassificationTermSourceCategory STRING,'
            'ClassificationTermText STRING,'
            'GoodsServicesDescriptionText2 STRING,'
            'NationalClassTotalQuantity STRING,'
            'NoBasisIndicator STRING,'
            'BasisForeignApplicationIndicator STRING,'
            'BasisForeignRegistrationIndicator STRING,'
            'BasisUseIndicator STRING,'
            'BasisIntentToUseIndicator STRING,'
            'PRIMARY KEY(ST13ApplicationNumber,proc_date,ClassDescriptionBagNumber,ClassificationVersion,DescriptionClassNumber)) PARTITION BY HASH(ST13ApplicationNumber) PARTITIONS 12 STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'ClassDescriptionBagNumber BIGINT,'
            'ClassificationVersion STRING,'
            'DescriptionClassNumber BIGINT,'
            'GoodsServicesDescriptionText STRING,'
            'ClassificationTermOfficeCode STRING,'
            'ClassificationTermSourceCategory STRING,'
            'ClassificationTermText STRING,'
            'GoodsServicesDescriptionText2 STRING,'
            'NationalClassTotalQuantity STRING,'
            'NoBasisIndicator STRING,'
            'BasisForeignApplicationIndicator STRING,'
            'BasisForeignRegistrationIndicator STRING,'
            'BasisUseIndicator STRING,'
            'BasisIntentToUseIndicator STRING) ')

model = helpers.tbl_model(table, [body, body_ext])
