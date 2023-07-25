#############################################################################
# Extract main data from OLD Grant XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):

    to_extract = [".//SDOBI/B200/B210/DNUM/PDAT",
                  ".//SDOBI/B100/B190/PDAT",
                  ".//SDOBI/B100/B110/DNUM/PDAT",
                  ".//SDOBI/B100/B130/PDAT",
                  ".//SDOBI/B100/B140/DATE/PDAT",
                  ".//application-reference/document-id/country",          #
                  ".//SDOBI/B200/B220/DATE/PDAT",
                  ".//SDOBI/B200/B211US/PDAT",
                  ".//us-issued-on-continued-prosecution-application",     #
                  ".//B221US",
                  ".//B474US/PDAT",
                  ".//B474/PDAT",                                          #
                  ".//B540/STEXT/PDAT",
                  ".//B577/PDAT",
                  ".//B578US/PDAT",
                  ".//NO_PARTUCULAR_TAG",                                  #
                  ".//examiners/primary-examiner/department",
                  ".//B746/PARTY-US/NAM/FNM/PDAT",
                  ".//B746/PARTY-US/NAM/SNM/STEXT/PDAT",
                  ".//B860/B861/DOC/DATE/PDATE",
                  ".//B860/B861/DOC/CTRY/PDAT",
                  ".//B860/B864US/DATE/PDAT",
                  ".//B870/B871/DOC/DATE/PDAT",
                  ".//B870/B871/DOC/CTRY/PDAT"
                 ]

    xml = ET.fromstring(xml_part)

    res_list = []

    for tag in to_extract:
        ct = xml.find(tag)
        if tag == ".//B221US":
            if ct is not None:
                res_list.append('True')
            else: res_list.append('False')
        else:
            res_list.append(helpers.get_value(ct))

#        res_list.append(helpers.get_value(ct))

    result = u"\t".join(res_list).encode('utf-8').strip()+"\n"
    return result
