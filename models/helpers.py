######################################################################
# Wrapper class for creating full CREATE TABLE expression
# for each particular model
######################################################################
class tbl_model():

    def __init__(self, table, body):
        self.ext_db = 'ipv_ext'
        self.int_db = 'ipv_db'
        self.table  = table
        self.header = 'CREATE TABLE IF NOT EXISTS'
        self.body_int = body[0]
        self.body_ext = body[1]
        self.row_tab = 'ROW FORMAT DELIMITED FIELDS TERMINATED BY \'\\t\''
        self.row_space = 'ROW FORMAT DELIMITED FIELDS TERMINATED BY \' \''
        self.part_proc = 'PARTITIONED BY (proc_date STRING) STORED AS PARQUET '
        self.part_year = 'PARTITIONED BY (year STRING) STORED AS PARQUET '
        self.etpl = (self.header, self.ext_db, self.table)
        self.itpl = (self.header, self.int_db, self.table, self.body_int)
        self.ext_constructor = {
                                'ipg'  : ('%s `%s`.`%s` %s %s') % (self.etpl + (self.body_int, self.row_tab)),
                                'ipa'  : ('%s `%s`.`%s` %s %s') % (self.etpl + (self.body_int, self.row_tab)),
                                'pa'   : ('%s `%s`.`%s` %s %s') % (self.etpl + (self.body_int, self.row_tab)),
                                'pg'   : ('%s `%s`.`%s` %s %s') % (self.etpl + (self.body_int, self.row_tab)),
                                'ad'   : ('%s `%s`.`%s` %s %s') % (self.etpl + (self.body_ext, self.row_tab)),
                                'att'  : ('%s `%s`.`%s` %s %s') % (self.etpl + (self.body_ext, self.row_tab)),
                                'thist': ('%s `%s`.`%s` %s %s') % (self.etpl + (self.body_ext, self.row_tab)),
                                'phi'  : ('%s `%s`.`%s` %s %s') % (self.etpl + (self.body_ext, self.row_tab)),
                                'ainf' : ('%s `%s`.`%s` %s %s') % (self.etpl + (self.body_ext, self.row_tab)),
                                'fee_m': ('%s `%s`.`%s` %s %s') % (self.etpl + (self.body_ext, self.row_space)),
                                'fee_d': ('%s `%s`.`%s` %s %s') % (self.etpl + (self.body_ext, self.row_tab)),
                                'td'   : ('%s `%s`.`%s` %s %s') % (self.etpl + (self.body_ext, self.row_tab))
                                }

        self.int_constructor = {
                                'ipg'  : ('%s `%s`.`%s` %s %s') % (self.itpl + (self.part_proc,)),
                                'ipa'  : ('%s `%s`.`%s` %s %s') % (self.itpl + (self.part_proc,)),
                                'pa'   : ('%s `%s`.`%s` %s %s') % (self.itpl + (self.part_proc,)),
                                'pg'   : ('%s `%s`.`%s` %s %s') % (self.itpl + (self.part_proc,)),
                                'ad'   : ('%s `%s`.`%s` %s ') % self.itpl,
                                'thist': ('%s `%s`.`%s` %s ') % self.itpl,
                                'phi'  : ('%s `%s`.`%s` %s ') % self.itpl,
                                'ainf' : ('%s `%s`.`%s` %s ') % self.itpl,
                                'att'  : ('%s `%s`.`%s` %s ') % self.itpl,
                                'fee_m': ('%s `%s`.`%s` %s %s') % (self.itpl + (self.part_year,)),
                                'fee_d': ('%s `%s`.`%s` %s %s') % (self.itpl + ('STORED AS PARQUET',)),
                                'td'   : ('%s `%s`.`%s` %s ') % self.itpl
                                }

    def get_int_schema(self,ftype='ipg'):
        return self.int_constructor[ftype]

    def get_ext_schema(self,ftype='ipg'):
        return self.ext_constructor[ftype]

    def get_table_name(self):
        return self.table



