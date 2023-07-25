#############################################################################
# Extract agent data from OLD Application XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):
    to_extract = [
                  "./name-1",
                  "./name-2",
                  "./addressbook/orgname",    #
                  "./address/country/country-code"
                 ]

    app_num_tag = ".//domestic-filing-data/application-number/doc-number"

    parts_tag = ".//correspondence-address"

    return helpers.w_old_extract(xml_part, to_extract, parts_tag, app_num_tag)
