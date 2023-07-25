#############################################################################
# Extract assignee data from OLD Application XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################


def create_line(xml_part):
    to_extract = [
                  ".//name/given-name",
                  ".//name/family-name",
                  ".//organization-name",
                  ".//address/city",
                  ".//address/country/country-code",
                  ".//assignee-type"
                 ]

    app_num_tag = ".//domestic-filing-data/application-number/doc-number"

    parts_tag = ".//assignee"

    return helpers.extract(xml_part, to_extract, parts_tag, app_num_tag)
