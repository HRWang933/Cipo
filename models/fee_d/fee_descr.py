import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'fee_descr'
body   =   ('(code STRING,'
            'description STRING) ')

model = helpers.tbl_model(table, [body, body])
