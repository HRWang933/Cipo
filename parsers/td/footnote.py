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

    parts_tag = './/tmk:TrademarkBag/tmk:Trademark/tmk:NationalTrademarkInformation/catmk:FootnoteBag/catmk:Footnote'

    sub_tags = ['.//catmk:FootnoteStructured/cacom:CategoryCode',
                './/catmk:FootnoteStructured/cacom:CategoryDescription',
                './/catmk:FootnoteStructured/cacom:RegisteredDate',
                './/catmk:FootnoteStructured/cacom:ChangedDate',
                './/catmk:FootnoteStructured/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="1"]',
                './/catmk:FootnoteStructured/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="2"]',
                './/catmk:FootnoteStructured/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="3"]',
                './/catmk:FootnoteStructured/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="4"]',
                './/catmk:FootnoteStructured/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="5"]',
                './/catmk:FootnoteStructured/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="6"]',
                './/catmk:FootnoteStructured/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="7"]',
                './/catmk:FootnoteStructured/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="8"]',
                './/catmk:FootnoteStructured/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="9"]',
                './/catmk:FootnoteStructured/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="10"]',
                './/catmk:FootnoteFormattedText/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="1"]',
                './/catmk:FootnoteFormattedText/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="2"]',
                './/catmk:FootnoteFormattedText/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="3"]',
                './/catmk:FootnoteFormattedText/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="4"]',
                './/catmk:FootnoteFormattedText/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="5"]',
                './/catmk:FootnoteFormattedText/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="6"]',
                './/catmk:FootnoteFormattedText/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="7"]',
                './/catmk:FootnoteFormattedText/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="8"]',
                './/catmk:FootnoteFormattedText/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="9"]',
                './/catmk:FootnoteFormattedText/cacom:TextLineBag/cacom:TextLine[@com:sequenceNumber="10"]' 
               ]


    return helpers.td_extract(xml_part, to_extract, ns, parts_tag, sub_tags)

