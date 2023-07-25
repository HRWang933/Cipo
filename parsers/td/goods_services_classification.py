#############################################################################
# Extract assignee data from Assignment XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):
    
    ns = {'tmk':'http://www.wipo.int/standards/XMLSchema/ST96/Trademark',
          'com':'http://www.wipo.int/standards/XMLSchema/ST96/Common',
          'catmk':'http://www.cipo.ic.gc.ca/standards/XMLSchema/ST96/Trademark',
          'cacom':'http://www.cipo.ic.gc.ca/standards/XMLSchema/ST96/Common'

         }
    to_extract = [".//tmk:TrademarkBag/tmk:Trademark/com:ApplicationNumber/com:ST13ApplicationNumber"]

    parts_tag = './/tmk:TrademarkBag/tmk:Trademark/tmk:GoodsServicesBag/tmk:GoodsServices/tmk:GoodsServicesClassificationBag/tmk:GoodsServicesClassification'

    sub_tags = ['.//tmk:ClassificationKindCode',
                './/com:CommentText',
                './/tmk:ClassNumber',
                './/tmk:ClassTitleText' 
               ]

    to_extract2= []
    parts_tag2 = ''
    sub_tags2 = []

    return helpers.td_extract(xml_part, to_extract, ns, parts_tag, sub_tags,parts_tag2, sub_tags2, to_extract2)

