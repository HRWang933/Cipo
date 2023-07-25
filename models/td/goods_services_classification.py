import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_goods_services_classification'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'ClassificationKindCode STRING,'
            'CommentText STRING,'
            'ClassNumber BIGINT,'
            'ClassTitleText STRING,'
            'PRIMARY KEY(ST13ApplicationNumber,proc_date,ClassificationKindCode,CommentText,ClassNumber,ClassTitleText)) PARTITION BY HASH(ST13ApplicationNumber) PARTITIONS 12 STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'ClassificationKindCode STRING,'
            'CommentText STRING,'
            'ClassNumber BIGINT,'
            'ClassTitleText STRING) ')

model = helpers.tbl_model(table, [body, body_ext])
