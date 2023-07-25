
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

    repeat_tag_keylist = ['.//tmk:TrademarkBag/tmk:Trademark/tmk:LegalProceedingsBag/tmk:LegalProceedings/tmk:CancellationProceedings[@xsi:type="catmk:CancellationProceedingsType"]',
                          './/catmk:ProceedingStageBag/catmk:ProceedingStage',
                          './/tmk:ProceedingEventBag/tmk:ProceedingEvent'
                         ]
    repeat_tag = {'.//tmk:TrademarkBag/tmk:Trademark/tmk:LegalProceedingsBag/tmk:LegalProceedings/tmk:CancellationProceedings[@xsi:type="catmk:CancellationProceedingsType"]':['.//tmk:LegalProceedingIdentifier'],
                  './/catmk:ProceedingStageBag/catmk:ProceedingStage':['.//catmk:ProceedingStageCode'],
                  './/tmk:ProceedingEventBag/tmk:ProceedingEvent':['.//tmk:MarkEventCategory','.//tmk:MarkEventResponseDate','.//tmk:NationalMarkEvent/tmk:MarkEventCode','.//tmk:NationalMarkEvent/tmk:MarkEventDescriptionText','.//tmk:NationalMarkEvent/catmk:MarkEventOtherLanguageDescriptionTextBag/catmk:MarkEventDescriptionText[@com:languageCode="fr"]','.//tmk:MarkEventAdditionalText','.//tmk:MarkEventDate']
                 }

    return helpers.td_extractProceeding(xml_part, to_extract, ns, repeat_tag_keylist,repeat_tag)

