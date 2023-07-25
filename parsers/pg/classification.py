#############################################################################
# Extract classification data from OLD Grant XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):
    to_extract = ["country", 
                  "B521/PDAT",
                  "B522/PDAT"
                 ]


    app_num_tag = ".//SDOBI/B200/B210/DNUM/PDAT"

    parts_tag = ".//SDOBI/B500/B520"

    return helpers.cl_old_extract(xml_part, to_extract, parts_tag, app_num_tag)

