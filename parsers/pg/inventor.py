#############################################################################
# Extract inventor data from OLD Grant XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):
    to_extract = [
                  ".//PARTY-US/NAM/FNM/PDAT",
                  ".//PARTY-US/NAM/SNM/STEXT/PDAT",
                  ".//PARTY-US/ADR/CITY/PDAT",
                  ".//PARTY-US/ADR/CTRY/PDAT"
                 ]

    app_num_tag = ".//SDOBI/B200/B210/DNUM/PDAT"

    parts_tag = ".//B720/B721"

    return helpers.extract(xml_part, to_extract, parts_tag, app_num_tag)

