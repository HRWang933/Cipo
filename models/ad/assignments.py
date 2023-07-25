import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'assignment_main'
body   =   ('(app_id BIGINT,'
            'reel_no BIGINT,'
            'frame_no BIGINT,'
            'last_update STRING,'
            'purge_ind STRING,'
            'recorded STRING,'
            'corr_name STRING,'
            'corr_addr1 STRING,'
            'corr_addr2 STRING,'
            'corr_addr3 STRING,'
            'corr_addr4 STRING,'
            'conv_text STRING, '
            'PRIMARY KEY(app_id, reel_no, frame_no, last_update)) PARTITION BY HASH(app_id) PARTITIONS 32 STORED AS KUDU ')

body_ext =   ('(app_id BIGINT,'
            'reel_no BIGINT,'
            'frame_no BIGINT,'
            'last_update STRING,'
            'purge_ind STRING,'
            'recorded STRING,'
            'corr_name STRING,'
            'corr_addr1 STRING,'
            'corr_addr2 STRING,'
            'corr_addr3 STRING,'
            'corr_addr4 STRING,'
            'conv_text STRING) ')

model = helpers.tbl_model(table, [body, body_ext])
