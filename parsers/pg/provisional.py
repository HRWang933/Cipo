#############################################################################
# Extract provisional data from OLD Grant XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):
    to_extract = [
                  ".//document-id/country",
                  ".//B680US/DOC/DNUM/PDAT",
                  ".//B680US/DOC/KIND/PDAT",
                  ".//B680US/DOC/DATE/PDAT"
                 ]

    app_num_tag = ".//SDOBI/B200/B210/DNUM/PDAT"

    parts_tag = ".//B600"

    return helpers.extract(xml_part, to_extract, parts_tag, app_num_tag)

