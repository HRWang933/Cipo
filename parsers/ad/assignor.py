#############################################################################
# Extract assignor data from Assignment XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):

    to_extract = [".//patent-properties/patent-property",
                  ".//assignment-record/reel-no",
                  ".//assignment-record/frame-no",
                  ".//assignment-record/last-update-date/date"
                 ]

    parts_tag = './/patent-assignor'

    sub_tags = ['.//name',
                './/execution-date/date',
                './/address-1',
                './/address-2'
               ]

    return helpers.as_extract(xml_part, to_extract, parts_tag, sub_tags)

