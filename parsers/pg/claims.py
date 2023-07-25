#############################################################################
# Extract claims data from OLD Grant XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):
    to_extract = [".//B330/CTRY/PDAT",
                  ".//B310/DNUM/PDAT",
                  ".//B320/DATE/PDAT"
                 ]

    app_num_tag = ".//SDOBI/B200/B210/DNUM/PDAT"

    parts_tag = ".//B300"

    return helpers.extract(xml_part, to_extract, parts_tag, app_num_tag)

