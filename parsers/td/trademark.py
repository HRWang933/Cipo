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

    to_extract = ['.//tmk:TrademarkBag/tmk:Trademark/com:ApplicationNumber/com:ST13ApplicationNumber',
                  './/tmk:TrademarkBag/tmk:Trademark/com:RegistrationOfficeCode',
                  './/tmk:TrademarkBag/tmk:Trademark/com:ReceivingOfficeCode',
                  './/tmk:TrademarkBag/tmk:Trademark/com:ReceivingOfficeDate',
                  './/tmk:TrademarkBag/tmk:Trademark/com:ApplicationNumber/com:IPOfficeCode',
                  './/tmk:TrademarkBag/tmk:Trademark/com:RegistrationNumber',   
                  './/tmk:TrademarkBag/tmk:Trademark/com:ApplicationDate',                     
                  './/tmk:TrademarkBag/tmk:Trademark/com:RegistrationDate',                     
                  './/tmk:TrademarkBag/tmk:Trademark/com:FilingPlace',                     
                  './/tmk:TrademarkBag/tmk:Trademark/com:ApplicantFileReference',
                  './/tmk:TrademarkBag/tmk:Trademark/com:ApplicationLanguageCode',
                  './/tmk:TrademarkBag/tmk:Trademark/com:ExpiryDate',                     
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:TerminationDate',               
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkCurrentStatusCode',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:AssociatedMarkBag/tmk:AssociatedMark/tmk:AssociationCategory',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:AssociatedMarkBag/tmk:AssociatedMark/tmk:AssociatedApplicationNumber/com:IPOfficeCode',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:AssociatedMarkBag/tmk:AssociatedMark/tmk:AssociatedApplicationNumber/com:ST13ApplicationNumber',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:DivisionalApplicationBag/tmk:InitialApplicationNumber/com:IPOfficeCode',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:DivisionalApplicationBag/tmk:InitialApplicationNumber/com:ST13ApplicationNumber',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:DivisionalApplicationBag/tmk:InitialApplicationDate',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:InternationalMarkIdentifierBag/tmk:InternationalMarkIdentifier',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkCurrentStatusDate',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkCategory',            
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkDisclaimerBag/tmk:MarkDisclaimerText[@com:languageCode="en"]',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkDisclaimerBag/tmk:MarkDisclaimerText[@com:languageCode="fr"]',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:NonUseCancelledIndicator',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:TradeDistinctivenessIndicator',            
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:TradeDistinctivenessText',            
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:UseLimitationText',
                  './/tmk:TrademarkBag/tmk:Trademark/com:CommentText',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:OppositionPeriodStartDate',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:OppositionPeriodEndDate',
               ]


    return helpers.td_extract(xml_part, to_extract, ns,bool_main= True)

