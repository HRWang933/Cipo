import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'ph_info'
body   =   ('(app_id BIGINT,'
            'patent_no STRING,'
            'customer_id STRING,'
            'entity_status STRING,'
            'phone_num STRING,'
            'address STRING,'
            'proc_date STRING,'
            'PRIMARY KEY(app_id, patent_no)) PARTITION BY HASH(app_id, patent_no) PARTITIONS 64 STORED AS KUDU ')

body_ext = ('(app_id BIGINT,'
            'patent_no STRING,'
            'customer_id STRING,'
            'entity_status STRING,'
            'phone_num STRING,'
            'address STRING,'
            'proc_date STRING) ')

model = helpers.tbl_model(table, [body, body_ext])
