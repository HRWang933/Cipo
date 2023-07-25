######################################################################
# Active models describe the model files used by processing routines
# to create particular Impala table structures
######################################################################
active_models = {
    'ipg': [
        'main',
        'assignee',
        'inventor',
        'd_inventor',
        'applicant',
        'claims',
        'classification',
        'agent',
        'provisional',
        'related',
    ],
    'ad': [
        'assignments',
        'assignee',
        'assignor'
    ],
    'pa': [
        'main',
        'assignee',
        'inventor',
        #             'd_inventor',
        #             'applicant',
        'claims',
        'classification',
        'agent',
        'provisional',
        'related',
    ],
    'pg': [
        'main',
        'assignee',
        'inventor',
        #             'd_inventor',
        #             'applicant',
        'claims',
        'classification',
        'agent',
        'provisional',
        'related',
    ],
    'ipa': [
        'main',
        'assignee',
        'inventor',
        'd_inventor',
        'applicant',
        'claims',
        'classification',
        'agent',
        'provisional',
        'related',
    ],
    'thist': ['transactions'],
    'ainf': ['add_info'],
    'att': ['attorney'],
    'fee_m': ['fee_main'],
    'fee_d': ['fee_descr'],
    'phi': ['ph_info'],
    'td': [
        'trademark_application',
        'trademark',
        'mark_representation',
        'goods_services',
        'goods_services_classification',
        'priority',
        'publication',
        'applicant',
        'national_representative',
        'national_correspondent',
        'authorization',
        'mark_event',
        'mark_feature',
        'cancellation_proceedings',
        'cancellationproceeding_events',
        'opposition_proceedings',
        'oppositionproceeding_events',
        'national_trademark_information',
        'section9',
        'trademark_class',
        'trademark_use_right',
        'legislation',
        'geo_indication',
        'footnote',
        'categorized_text',
        'doubtful_case',
        'claim',
        'index_heading',
        'mark_translation',
        'interested_party',
        'correspondence_address'
    ]
}

######################################################################
# Active parsers describe the parsers files used by processing routines
# to parse particular parts of XML or TXT source files
######################################################################
active_parsers = {
    'ipg': [
        'main',
        'assignee',
        'inventor',
        'd_inventor',
        'applicant',
        'claims',
        'classification',
        'agent',
        'provisional',
        'related',
    ],
    'pg': [
        'main',
        'assignee',
        'inventor',
        #             'd_inventor',
        #             'applicant',
        'claims',
        'classification',
        'agent',
        'provisional',
        'related',
    ],
    'pa': [
        'main',
        'assignee',
        'inventor',
        #             'd_inventor',
        #             'applicant',
        'claims',
        'classification',
        'agent',
        'provisional',
        'related',
    ],
    'ipa': [
        'main',
        'assignee',
        'inventor',
        'd_inventor',
        'applicant',
        'claims',
        'classification',
        'agent',
        'provisional',
        'related',
    ],
    'ad': [
        'assignments',
        'assignee',
        'assignor'
    ],
    'att': ['attorney'],
    'fee_m': ['fee_main'],
    'fee_d': ['fee_descr'],
    'td': [
        'trademark_application',
        'trademark',
        'mark_representation',
        'goods_services',
        'goods_services_classification',
        'priority',
        'publication',
        'applicant',
        'national_representative',
        'national_correspondent',
        'authorization',
        'mark_event',
        'mark_feature',
        'cancellation_proceedings',
        'cancellationproceeding_events',
        'opposition_proceedings',
        'oppositionproceeding_events',
        'national_trademark_information',
        'section9',
        'trademark_class',
        'trademark_use_right',
        'legislation',
        'geo_indication',
        'footnote',
        'categorized_text',
        'doubtful_case',
        'claim',
        'index_heading',
        'mark_translation',
        'interested_party',
        'correspondence_address'
    ]
}

######################################################################
# Base HDFS directory
######################################################################
hdfs_base_dir = '/ipv'

######################################################################
# Base links for downloading source files
######################################################################
dwl_links = {
    'ipg': 'https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/',
    'pg': 'https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/',
    'pa': 'https://bulkdata.uspto.gov/data/patent/application/redbook/fulltext/',
    'ipa': 'https://bulkdata.uspto.gov/data/patent/application/redbook/fulltext/',
    'ad': 'https://bulkdata.uspto.gov/data/patent/assignment/',
    'td': 'https://www.ic.gc.ca/eic/site/cipointernet-internetopic.nsf/eng/h_wr04302.html',
    'fee': 'https://bulkdata.uspto.gov/data/patent/maintenancefee/MaintFeeEvents.zip',
    'att': 'http://www.uspto.gov/attorney-roster/attorney.zip'
}

######################################################################
# Existing Reports Name
######################################################################

report_names = ['report_search', 'report_defaultsearch', 'report_opposition', 'report_cancellation',
                 'report_historyAC', 'report_cipo_prosecution', 'report_cipo_cancellation', 'report_cipo_opposition',
                 'report_wiposearch', 'report_section44p1notice', 'report_nicecorrespondencesent',
                 'report_processingtime', 'report_processing_history', 'report_pef']

######################################################################
# Impala entry point host
######################################################################
impala_host = '192.168.250.31'

######################################################################
# Mail credentials and parameters used by processing routines
# for sending notifications
######################################################################
mail_params = {
    #    'server': '192.168.0.220',
    #    'server': '127.0.0.1',
    #    'username': 'administrator@ollip.com',
    #    'password': 'Iwl2bavp',
    #    'send_from': 'administrator@ollip.com',
    #    'send_to': ['info@ipvisibility.com', 'laraebmussawir@gmail.com'],
    #    'attach_file': ''
    # }
    'server': '127.0.0.1',
    'username': 'notify@ipvisibility.com',
    'password': 'Linuxnotifications4m!',
    'send_from': 'notify@ipvisibility.com',
    #	'send_to': ['info@ipvisibility.com', 'hamza.khan.niazi04@gmail.com', 'owaiskarni81@hotmail.com'],
    'send_to': ['info@ipvisibility.com', 'owaiskarni81@hotmail.com'],
    #'send_to': ['owaiskarni81@hotmail.com'],
    'attach_file': ''
    #        'text'     : text,
    #        'subject'  : ('%s file %s report') % (type_map[ftype], mode_map[mode]),
    #        'files'    : [out_file_xlsx]
}
# mail_params =   {
#    'server'   : 'smtp.gmail.com',
#    'username' : 'bayo.laurance@gmail.com',
#    'password' : 'lego123lego',
#    'send_from': 'bayo.laurance@gmail.com',
#    'send_to'  : ['info@ipvisibility.com','limsiewling0803@gmail.com'],
#    'send_to'  : ['limsiewling0803@gmail.com'],
