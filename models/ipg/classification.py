import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'grant_classification'

body   =   ('(app_id BIGINT,'
            'country STRING,'
            'main_class STRING,'
            'main_subclass STRING,'
            'further_class STRING,'
            'further_subclass STRING) ')

model = helpers.tbl_model(table, [body, None])
