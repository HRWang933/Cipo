import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ca_tm_publication'
body   =   ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
	    'PublicationIdentifier STRING,'
	    'PublicationStatusCategory STRING,'
	    'PublicationActionDate STRING,'
            'PRIMARY KEY(ST13ApplicationNumber,proc_date)) STORED AS KUDU ')

body_ext = ('(ST13ApplicationNumber BIGINT,'
            'proc_date STRING,'
	    'PublicationIdentifier STRING,'
	    'PublicationStatusCategory STRING,'
	    'PublicationActionDate STRING) ') 

model = helpers.tbl_model(table, [body, body_ext])
