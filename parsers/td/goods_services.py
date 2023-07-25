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

    parts_tag = './/tmk:TrademarkBag/tmk:Trademark/tmk:GoodsServicesBag/tmk:GoodsServices/tmk:ClassDescriptionBag/tmk:ClassDescription'

    sub_tags = ['.//com:ClassificationVersion', 
                './/tmk:ClassNumber',
                './/tmk:GoodsServicesDescriptionText',
                './/tmk:ClassificationTermBag/tmk:ClassificationTerm/tmk:ClassificationTermOfficeCode',
                './/tmk:ClassificationTermBag/tmk:ClassificationTerm/tmk:ClassificationTermSourceCategory',
                './/tmk:ClassificationTermBag/tmk:ClassificationTerm/tmk:ClassificationTermText' 
               ]

    to_extract2= ['.//tmk:TrademarkBag/tmk:Trademark/tmk:GoodsServicesBag/tmk:GoodsServices/tmk:NationalGoodsServices/tmk:NationalClassTotalQuantity',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:GoodsServicesBag/tmk:GoodsServices/tmk:NationalFilingBasis/tmk:CurrentBasis/tmk:NoBasisIndicator',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:GoodsServicesBag/tmk:GoodsServices/tmk:NationalFilingBasis/tmk:CurrentBasis/tmk:BasisForeignApplicationIndicator',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:GoodsServicesBag/tmk:GoodsServices/tmk:NationalFilingBasis/tmk:CurrentBasis/tmk:BasisForeignRegistrationIndicator',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:GoodsServicesBag/tmk:GoodsServices/tmk:NationalFilingBasis/tmk:CurrentBasis/tmk:BasisUseIndicator',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:GoodsServicesBag/tmk:GoodsServices/tmk:NationalFilingBasis/tmk:CurrentBasis/tmk:BasisIntentToUseIndicator' 
                  ]
    parts_tag2 = ''
    sub_tags2 = []

    return helpers.td_extract(xml_part, to_extract, ns, parts_tag, sub_tags,parts_tag2, sub_tags2, to_extract2,bool_checklongstr = True)

