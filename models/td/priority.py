import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_priority'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
	    'ApplicationNumberText STRING,'
	    'PriorityCountryCode STRING,'
	    'PriorityApplicationFilingDate STRING,'
	    'CommentText STRING,'
	    'ClassificationVersion BIGINT,'
	    'ClassNumber BIGINT,'
	    'GoodsServicesDescriptionText STRING,'
	    'GoodsServicesDescriptionText2 STRING,'
            'PRIMARY KEY(ST13ApplicationNumber,proc_date,ApplicationNumberText)) STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
	    'ApplicationNumberText STRING,'
	    'PriorityCountryCode STRING,'
	    'PriorityApplicationFilingDate STRING,'
	    'CommentText STRING,'
	    'ClassificationVersion BIGINT,'
	    'ClassNumber BIGINT,'
	    'GoodsServicesDescriptionText STRING,'
	    'GoodsServicesDescriptionText2 STRING) ')

model = helpers.tbl_model(table, [body, body_ext])
