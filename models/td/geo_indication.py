import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_geo_indication'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'GeoInd_CategoryCode BIGINT,'
            'GeoInd_CategoryDescription_en STRING,'
            'GeoInd_CategoryDescription_fr STRING,'
            'GeographicalIndicationTranslationText STRING,'
            'FileName STRING,'
            'ImageFormatCategory STRING,'
            'NPC_CategoryCode BIGINT,'
            'NPC_CategoryDescription_en STRING,'
            'NPC_CategoryDescription_fr STRING,'
            'PRIMARY KEY(ST13ApplicationNumber,proc_date)) STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'GeoInd_CategoryCode BIGINT,'
            'GeoInd_CategoryDescription_en STRING,'
            'GeoInd_CategoryDescription_fr STRING,'
            'GeographicalIndicationTranslationText STRING,'
            'FileName STRING,'
            'ImageFormatCategory STRING,'
            'NPC_CategoryCode BIGINT,'
            'NPC_CategoryDescription_en STRING,'
            'NPC_CategoryDescription_fr STRING)    ') 

model = helpers.tbl_model(table, [body, body_ext])
