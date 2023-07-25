import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'application_assignee'

body   =   ('(app_id BIGINT,'
            'first_name STRING,'
            'last_name STRING,'
            'orgname STRING,'
            'addr_city STRING,'
            'addr_country STRING,'
            '`role` STRING ) ')

model = helpers.tbl_model(table, [body, None])
