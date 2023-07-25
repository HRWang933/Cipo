import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'grant_d_inventor'

body   =   ('(app_id BIGINT,'
            'first_name STRING,'
            'last_name STRING,'
            'addr_city STRING,'
            'addr_country STRING) ')

model = helpers.tbl_model(table, [body, None])
