#############################################################################
# Extract provisional data from Grant XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):
    to_extract = [
                  ".//document-id/country",
                  ".//document-id/doc-number",
                  ".//document-id/kind",
                  ".//document-id/date"
                 ]

    app_num_tag = ".//application-reference/document-id/doc-number"

    parts_tag = ".//us-provisional-application"

    return helpers.extract(xml_part, to_extract, parts_tag, app_num_tag)

