#############################################################################
# Extract inventor data from OLD Application XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):
    to_extract = [
                  [".//name/given-name",],
                  [".//name/family-name",],
                  [".//residence/residence-non-us/city", ".//residence/residence-us/city"],
                  [".//residence/residence-non-us/country-code", ".//residence/residence-us/country-code"]
                 ]

    app_num_tag = ".//domestic-filing-data/application-number/doc-number"

    parts_tag = [".//inventors/first-named-inventor", ".//inventors/inventor",]

    return helpers.multi_extract(xml_part, to_extract, parts_tag, app_num_tag)

