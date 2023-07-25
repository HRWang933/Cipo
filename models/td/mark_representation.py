import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_markrepresentation'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'ViennaCategory BIGINT,'
            'ViennaDivision BIGINT,'
            'ViennaSection BIGINT,'
            'ViennaDescription_en STRING,'
            'ViennaDescription_fr STRING,'
            'MarkFeatureCategory STRING,'
            'MarkSignificantVerbalElementText STRING,'
            'MarkTranslationText STRING,'
            'MarkTransliteration STRING,'
            'MarkStandardCharacterIndicator STRING,'
            'ImageFileName STRING,'
            'ImageFormatCategory STRING,'
            'MarkImageColourClaimedText STRING,'
            'SoundFileName STRING,'
            'SoundFileFormatCategory STRING,'
            'MultimediaFileName STRING,'
            'MarkMultimediaFileFormatCategory STRING,'
            'MarkDescriptionText STRING,'
            'PRIMARY KEY(ST13ApplicationNumber,proc_date,ViennaCategory,ViennaDivision,ViennaSection)) PARTITION BY HASH(ST13ApplicationNumber) PARTITIONS 12 STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
            'ViennaCategory BIGINT,'
            'ViennaDivision BIGINT,'
            'ViennaSection BIGINT,'
            'ViennaDescription_en STRING,'
            'ViennaDescription_fr STRING,'
            'MarkFeatureCategory STRING,'
            'MarkSignificantVerbalElementText STRING,'
            'MarkTranslationText STRING,'
            'MarkTransliteration STRING,'
            'MarkStandardCharacterIndicator STRING,'
            'ImageFileName STRING,'
            'ImageFormatCategory STRING,'
            'MarkImageColourClaimedText STRING,'
            'SoundFileName STRING,'
            'SoundFileFormatCategory STRING,'
            'MultimediaFileName STRING,'
            'MarkMultimediaFileFormatCategory STRING,'
            'MarkDescriptionText STRING)  ')

model = helpers.tbl_model(table, [body, body_ext])
