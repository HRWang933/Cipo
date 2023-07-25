import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_oppositionproceeding_events'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'OppositionIdentifier STRING,'
            'ProceedingStageCode STRING,'
            'MarkEventCategory STRING,'
            'MarkEventResponseDate STRING,'
            'MarkEventCode STRING,'
            'MarkEventDescriptionText STRING,'
            'MarkEventDescriptionText_fr STRING,'
            'MarkEventAdditionalText STRING,'
            'MarkEventDate STRING,'
            'PRIMARY KEY(ST13ApplicationNumber,proc_date,OppositionIdentifier,ProceedingStageCode,MarkEventCategory,MarkEventResponseDate,MarkEventCode,MarkEventDescriptionText,MarkEventDescriptionText_fr,MarkEventAdditionalText,MarkEventDate)) PARTITION BY HASH(ST13ApplicationNumber) PARTITIONS 12 STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'OppositionIdentifier STRING,'
            'ProceedingStageCode STRING,'
            'MarkEventCategory STRING,'
            'MarkEventResponseDate STRING,'
            'MarkEventCode STRING,'
            'MarkEventDescriptionText STRING,'
            'MarkEventDescriptionText_fr STRING,'
            'MarkEventAdditionalText STRING,'
            'MarkEventDate STRING) ')

model = helpers.tbl_model(table, [body, body_ext])
