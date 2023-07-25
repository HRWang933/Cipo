#############################################################################
# Extract claims data from Applicaton XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):
    to_extract = ["country", 
                  "doc-number", 
                  "date"
                 ]

    app_num_tag = ".//application-reference/document-id/doc-number"

    parts_tag = ".//priority-claims/priority-claim"

    return helpers.extract(xml_part, to_extract, parts_tag, app_num_tag)

