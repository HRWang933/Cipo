import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_mark_event'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'MarkEventCategory STRING,'
            'MarkEventDate STRING,'
            'MarkEventCode BIGINT,'
            'MarkEventResponseDate STRING,'
            'MarkEventDescriptionText STRING,'
            'MarkEventDescriptionText_fr STRING,'
            'MarkEventAdditionalText STRING,'
            'PRIMARY KEY(ST13ApplicationNumber,proc_date,MarkEventCategory,MarkEventDate,MarkEventCode,MarkEventResponseDate)) PARTITION BY HASH(ST13ApplicationNumber) PARTITIONS 12 STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'MarkEventCategory STRING,'
            'MarkEventDate STRING,'
            'MarkEventCode BIGINT,'
            'MarkEventResponseDate STRING,'
            'MarkEventDescriptionText STRING,'
            'MarkEventDescriptionText_fr STRING,'
            'MarkEventAdditionalText STRING) ')

model = helpers.tbl_model(table, [body, body_ext])
