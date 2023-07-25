import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'assignment_assignee'
body   =   ('(app_id BIGINT,'
            'reel_no BIGINT,'
            'frame_no BIGINT,'
            'last_update STRING,'
            'name STRING,'
            'city STRING,'
            'state STRING,'
            'country STRING,'
            'postcode STRING,'
            'address1 STRING,'
            'address2 STRING,'
            'PRIMARY KEY(app_id, reel_no, frame_no, last_update, name)) PARTITION BY HASH(app_id) PARTITIONS 32 STORED AS KUDU ')

body_ext =   ('(app_id BIGINT,'
            'reel_no BIGINT,'
            'frame_no BIGINT,'
            'last_update STRING,'
            'name STRING,'
            'city STRING,'
            'state STRING,'
            'country STRING,'
            'postcode STRING,'
            'address1 STRING,'
            'address2 STRING) ')

model = helpers.tbl_model(table, [body, body_ext])
