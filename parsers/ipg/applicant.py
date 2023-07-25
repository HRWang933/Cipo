#############################################################################
# Extract applicant data from Grant XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):
    to_extract = [
                  ".//first-name",
                  ".//last-name",
                  ".//orgname",
                  ".//address/street",
                  ".//address/city",
                  ".//address/country",
                  ".//address/state",
                  ".//address/postcode",
                  ".//residence/country", 
                  ".//nationality/country"
                 ]

    app_num_tag = ".//application-reference/document-id/doc-number"

    parts_tag = ".//us-applicants/us-applicant"

    return helpers.extract(xml_part, to_extract, parts_tag, app_num_tag)
