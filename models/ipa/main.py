import importlib
helpers = importlib.import_module('.helpers', 'models')

######################################################################
#
######################################################################
table  = 'application_main'
body   =   ('(app_id BIGINT,'
            'earliest_pub_country STRING,'
            'earliest_pub_number STRING,'
            'earliest_pub_kind STRING,'
            'earliest_pub_date STRING,'
            'app_ref_country STRING,'
            'app_ref_date STRING,'
            'us_app_ser_code STRING,'
            'us_iss_on_cnt_prc_app STRING,'
            'rule_47 STRING,'
            'us_term_ext STRING,'
            'len_of_grant STRING,'
            'inv_title STRING,'
            'nbr_of_claims BIGINT,'
            'us_exempl_claim STRING,'
            'us_botan_var STRING,'
            'exam_dept STRING,'
            'exam_first_name STRING,'
            'exam_last_name STRING,'
            'prfd_date STRING,'
            'prfd_country STRING,'
            'prfd_371c124 STRING,'
            'prpd_date STRING,'
            'rrpd_country STRING) ')

model = helpers.tbl_model(table, [body, None])
