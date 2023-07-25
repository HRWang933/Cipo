import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'app_info'
body   =   ('(app_id BIGINT,'
            'app_type STRING,'
            'app_status STRING,'
            'app_status_date STRING,'
            'app_attr_doc_number STRING,'
            'app_cust_number STRING,'
            'proc_date STRING,'
            'PRIMARY KEY(app_id)) PARTITION BY HASH(app_id) PARTITIONS 8 STORED AS KUDU ')

body_ext =   ('(app_id BIGINT,'
            'app_type STRING,'
            'app_status STRING,'
            'app_status_date STRING,'
            'app_attr_doc_number STRING,'
            'app_cust_number STRING,'
            'proc_date STRING) ')

model = helpers.tbl_model(table, [body, body_ext])
