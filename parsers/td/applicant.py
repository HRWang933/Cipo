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

    parts_tag = './/tmk:TrademarkBag/tmk:Trademark/tmk:ApplicantBag/tmk:Applicant'

    sub_tags = ['.//com:LegalEntityName',
                './/com:Contact/com:Name/com:EntityName',
                './/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="1"]',
                './/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="2"]',
                './/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:GeographicRegionName[@com:geographicRegionCategory="Province"]',
                './/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:CountryCode',
                './/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:PostalCode',
                './/com:NationalLegalEntityCode'
               ]


    return helpers.td_extract(xml_part, to_extract, ns, parts_tag, sub_tags)

