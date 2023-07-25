#############################################################################
# Extract agent data from OLD Grant XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):
    to_extract = [
                  "PARTY-US/NAM/FNM/PDAT",
                  "PARTY-US/NAM/SNM/STEXT/PDAT",
                  "PARTY-US/NAM/ONM/STEXT/PDAT",
                  "addressbook/address/country"
                 ]

    app_num_tag = ".//SDOBI/B200/B210/DNUM/PDAT"

    parts_tag = ".//B740/B741"

    return helpers.w_extract(xml_part, to_extract, parts_tag, app_num_tag)
