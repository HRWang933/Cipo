#############################################################################
# Extract classiication data from Grant XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):
    to_extract = ["country", 
                  "main-classification",
                  "further-classification"
                 ]


    app_num_tag = ".//application-reference/document-id/doc-number"

    parts_tag = ".//us-bibliographic-data-grant/classification-national"

    return helpers.cl_extract(xml_part, to_extract, parts_tag, app_num_tag)

