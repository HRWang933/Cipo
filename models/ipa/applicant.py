import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'application_applicant'

body   =   ('(app_id BIGINT,'
            'first_name STRING,'
            'last_name STRING,'
            'orgname STRING,'
            'addr_street STRING,'
            'addr_city STRING,'
            'addr_country STRING,'
            'addr_state STRING,'
            'addr_postcode STRING,'
            'residence STRING,'
            'nationality STRING) ')

model = helpers.tbl_model(table, [body, None])

