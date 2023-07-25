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
          'cacom':'http://www.cipo.ic.gc.ca/standards/XMLSchema/ST96/Common',
          'xsi':"http://www.w3.org/2001/XMLSchema-instance"

         }
    to_extract = [".//tmk:TrademarkBag/tmk:Trademark/com:ApplicationNumber/com:ST13ApplicationNumber"]

    parts_tag = './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkEventBag/tmk:MarkEvent'

    # need to check for duplicated data
    sub_tags = ['.//tmk:MarkEventCategory',
                './/tmk:MarkEventDate',
                './/tmk:NationalMarkEvent[@xsi:type="catmk:NationalMarkEventType"]/tmk:MarkEventCode',
                './/tmk:MarkEventResponseDate',
                './/tmk:NationalMarkEvent[@xsi:type="catmk:NationalMarkEventType"]/tmk:MarkEventDescriptionText',
                './/tmk:NationalMarkEvent[@xsi:type="catmk:NationalMarkEventType"]/catmk:MarkEventOtherLanguageDescriptionTextBag/catmk:MarkEventDescriptionText[@com:languageCode="fr"]',
                './/tmk:NationalMarkEvent[@xsi:type="catmk:NationalMarkEventType"]/tmk:MarkEventAdditionalText' 
               ]


    return helpers.td_extract(xml_part, to_extract, ns, parts_tag, sub_tags)

