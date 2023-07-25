#############################################################################
# Extract assignee data from OLD Grant XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################


def create_line(xml_part):
    to_extract = [
                  ".//B731/PARTY-US/NAM/FNM/PDAT",
                  ".//B731/PARTY-US/NAM/SNM/STEXT/PDAT",
                  ".//B731/PARTY-US/NAM/ONM/STEXT/PDAT",
                  ".//B731/PARTY-US/ADR/CITY/PDAT",
                  ".//B731/PARTY-US/ADR/CTRY/PDAT",
                  ".//B732US/PDAT"
                 ]

    app_num_tag = ".//SDOBI/B200/B210/DNUM/PDAT"

    parts_tag = ".//B730"

    return helpers.extract(xml_part, to_extract, parts_tag, app_num_tag)
