#############################################################################
# Extract classification data from OLD Application XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):
    to_extract = ["country",
                  ".//classification-us-primary/uspc/class",
                  ".//classification-us-primary/uspc/subclass",
                  ".//classification-us-secondary/uspc/class",
                  ".//classification-us-secondary/uspc/subclass"
                 ]


    app_num_tag = ".//domestic-filing-data/application-number/doc-number"

    parts_tag = ".//technical-information"

    return helpers.extract(xml_part, to_extract, parts_tag, app_num_tag)

