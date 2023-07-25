import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_trademark_class'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'TrademarkClassCode BIGINT,'
            'TrademarkClassDescriptionBag_en STRING,'
            'TrademarkClassDescriptionBag_fr STRING,'
            'PRIMARY KEY(ST13ApplicationNumber,proc_date)) PARTITION BY HASH(ST13ApplicationNumber) PARTITIONS 12 STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'TrademarkClassCode BIGINT,'
            'TrademarkClassDescriptionBag_en STRING,'
            'TrademarkClassDescriptionBag_fr STRING)    ') 

model = helpers.tbl_model(table, [body, body_ext])
