#############################################################################
# Extract claims data from OLD Application XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):
    to_extract = ["country-code", 
                  "priority-application-number/doc-number", 
                  "filing-date"
                 ]

    app_num_tag = ".//domestic-filing-data/application-number/doc-number"

    parts_tag = ".//foreign-priority-data"

    return helpers.extract(xml_part, to_extract, parts_tag, app_num_tag)

