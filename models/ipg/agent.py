import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'grant_agent'

body   =   ('(`app_id` BIGINT,'
             '`agent_type` STRING,'
             '`first_name` STRING,'
             '`last_name` STRING,'
             '`org_name` STRING,'
             '`country` STRING ) ')

model = helpers.tbl_model(table, [body,None])

