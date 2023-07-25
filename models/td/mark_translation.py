import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_mark_translation'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'MarkTranslationOrTransliteration_en STRING,'
            'PRIMARY KEY(ST13ApplicationNumber,proc_date)) PARTITION BY HASH(ST13ApplicationNumber) PARTITIONS 12 STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'MarkTranslationOrTransliteration_en STRING)    ') 

model = helpers.tbl_model(table, [body, body_ext])
