#############################################################################
# Extract agent data from Applicaton XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):
    to_extract = [
                  "addressbook/first-name",
                  "addressbook/last-name",
                  "addressbook/orgname",
                  "addressbook/address/country"
                 ]

    app_num_tag = ".//application-reference/document-id/doc-number"

    parts_tag = ".//agents/agent"

    return helpers.w_extract(xml_part, to_extract, parts_tag, app_num_tag, 'rep-type')
