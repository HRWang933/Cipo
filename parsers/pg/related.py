#############################################################################
# Extract related publication data from OLD Grant XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):
    to_extract = [
                  ".//document-id/country",
                  ".//PCIT/DOC/DNUM/PDAT",
                  ".//PCIT/DOC/KIND/PDAT",
                  ".//PCIT/DOC/DATE/PDAT"
                 ]

    app_num_tag = ".//SDOBI/B200/B210/DNUM/PDAT"

    parts_tag = ".//B560/B561"

    return helpers.extract(xml_part, to_extract, parts_tag, app_num_tag)

