#############################################################################
# Extract provisional data from OLD Application XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):
    to_extract = [
                  ".//document-id/country-code",
                  ".//document-id/doc-number",
                  ".//document-id/kind",                      #
                  ".//document-id/document-date"
                 ]

    app_num_tag = ".//domestic-filing-data/application-number/doc-number"

    parts_tag = ".//non-provisional-of-provisional"

    return helpers.extract(xml_part, to_extract, parts_tag, app_num_tag)

