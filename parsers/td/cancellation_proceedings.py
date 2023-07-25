
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

    parts_tag = './/tmk:TrademarkBag/tmk:Trademark/tmk:LegalProceedingsBag/tmk:LegalProceedings/tmk:CancellationProceedings[@xsi:type="catmk:CancellationProceedingsType"]'

    sub_tags = ['.//tmk:LegalProceedingIdentifier',
                './/tmk:LegalProceedingFilingDate',
                './/catmk:NationalOppositionCaseType/catmk:OppositionCaseTypeDescriptionBag/catmk:OppositionCaseTypeDescription[@com:languageCode="en"]',
                './/catmk:NationalOppositionCaseType/catmk:OppositionCaseTypeDescriptionBag/catmk:OppositionCaseTypeDescription[@com:languageCode="fr"]',
                './/tmk:ProceedingStatus/tmk:NationalStatusCategory',
                './/tmk:ProceedingStatus/tmk:NationalStatusCode',
                './/tmk:ProceedingStatus/tmk:NationalStatusDate',
                './/tmk:ProceedingStatus/tmk:NationalStatusInternalDescriptionText',
                './/tmk:PlaintiffBag/tmk:Plaintiff/com:LegalEntityName',
                './/tmk:PlaintiffBag/tmk:Plaintiff/com:Contact/com:Name/com:EntityName',
                './/tmk:PlaintiffBag/tmk:Plaintiff/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="1"]',
                './/tmk:PlaintiffBag/tmk:Plaintiff/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="2"]',
                './/tmk:PlaintiffBag/tmk:Plaintiff/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="3"]',
                './/tmk:PlaintiffBag/tmk:Plaintiff/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:GeographicRegionName[@com:geographicRegionCategory="Province"]',
                './/tmk:PlaintiffBag/tmk:Plaintiff/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:CountryCode',
                './/tmk:PlaintiffBag/tmk:Plaintiff/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:PostalCode',
                './/tmk:PlaintiffBag/tmk:Plaintiff/tmk:Correspondent/com:Contact/com:Name/com:EntityName',
                './/tmk:PlaintiffBag/tmk:Plaintiff/tmk:Correspondent/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="1"]',
                './/tmk:PlaintiffBag/tmk:Plaintiff/tmk:Correspondent/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="2"]',
                './/tmk:PlaintiffBag/tmk:Plaintiff/tmk:Correspondent/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="3"]',
                './/tmk:PlaintiffBag/tmk:Plaintiff/tmk:Correspondent/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:GeographicRegionName[@com:geographicRegionCategory="Province"]',
                './/tmk:PlaintiffBag/tmk:Plaintiff/tmk:Correspondent/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:CountryCode',
                './/tmk:PlaintiffBag/tmk:Plaintiff/tmk:Correspondent/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:PostalCode',
                './/tmk:PlaintiffBag/tmk:Plaintiff/com:RepresentativeBag/com:Representative/com:CommentText',
                './/tmk:PlaintiffBag/tmk:Plaintiff/com:RepresentativeBag/com:Representative/com:Contact/com:Name/com:EntityName',
                './/tmk:PlaintiffBag/tmk:Plaintiff/com:RepresentativeBag/com:Representative/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="1"]',
                './/tmk:PlaintiffBag/tmk:Plaintiff/com:RepresentativeBag/com:Representative/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="2"]',
                './/tmk:PlaintiffBag/tmk:Plaintiff/com:RepresentativeBag/com:Representative/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="3"]',
                './/tmk:PlaintiffBag/tmk:Plaintiff/com:RepresentativeBag/com:Representative/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:GeographicRegionName[@com:geographicRegionCategory="Province"]',
                './/tmk:PlaintiffBag/tmk:Plaintiff/com:RepresentativeBag/com:Representative/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:CountryCode',
                './/tmk:PlaintiffBag/tmk:Plaintiff/com:RepresentativeBag/com:Representative/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:PostalCode',
                './/tmk:DefendantBag/tmk:Defendant/com:Contact/com:Name/com:EntityName',
                './/tmk:DefendantBag/tmk:Defendant/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="1"]',
                './/tmk:DefendantBag/tmk:Defendant/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="2"]',
                './/tmk:DefendantBag/tmk:Defendant/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="3"]',
                './/tmk:DefendantBag/tmk:Defendant/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:GeographicRegionName[@com:geographicRegionCategory="Province"]',
                './/tmk:DefendantBag/tmk:Defendant/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:CountryCode',
                './/tmk:DefendantBag/tmk:Defendant/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:PostalCode',
                './/tmk:DefendantBag/tmk:Defendant/tmk:Correspondent/com:CommentText',
                './/tmk:DefendantBag/tmk:Defendant/tmk:Correspondent/com:Contact/com:Name/com:EntityName',
                './/tmk:DefendantBag/tmk:Defendant/tmk:Correspondent/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="1"]',
                './/tmk:DefendantBag/tmk:Defendant/tmk:Correspondent/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="2"]',
                './/tmk:DefendantBag/tmk:Defendant/tmk:Correspondent/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="3"]',
                './/tmk:DefendantBag/tmk:Defendant/tmk:Correspondent/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:GeographicRegionName[@com:geographicRegionCategory="Province"]',
                './/tmk:DefendantBag/tmk:Defendant/tmk:Correspondent/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:CountryCode',
                './/tmk:DefendantBag/tmk:Defendant/tmk:Correspondent/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:PostalCode',
                './/tmk:DefendantBag/tmk:Defendant/com:RepresentativeBag/com:Representative/com:CommentText',
                './/tmk:DefendantBag/tmk:Defendant/com:RepresentativeBag/com:Representative/com:Contact/com:Name/com:EntityName',
                './/tmk:DefendantBag/tmk:Defendant/com:RepresentativeBag/com:Representative/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="1"]',
                './/tmk:DefendantBag/tmk:Defendant/com:RepresentativeBag/com:Representative/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="2"]',
                './/tmk:DefendantBag/tmk:Defendant/com:RepresentativeBag/com:Representative/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:AddressLineText[@com:sequenceNumber="3"]',
                './/tmk:DefendantBag/tmk:Defendant/com:RepresentativeBag/com:Representative/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:GeographicRegionName[@com:geographicRegionCategory="Province"]',
                './/tmk:DefendantBag/tmk:Defendant/com:RepresentativeBag/com:Representative/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:CountryCode',
                './/tmk:DefendantBag/tmk:Defendant/com:RepresentativeBag/com:Representative/com:Contact/com:PostalAddressBag/com:PostalAddress/com:PostalStructuredAddress/com:PostalCode' 
		]

    parts_tag2 = './/catmk:ProceedingStageBag/catmk:ProceedingStage'
    sub_tags2 =['.//catmk:ProceedingStageCode',
                './/catmk:ProceedingStageDescriptionTextBag/catmk:ProceedingStageDescriptionText[@com:languageCode="en"]',
                './/catmk:ProceedingStageDescriptionTextBag/catmk:ProceedingStageDescriptionText[@com:languageCode="fr"]' 
                ]
    return helpers.td_extract(xml_part, to_extract, ns, parts_tag, sub_tags, parts_tag2, sub_tags2,bool_proceeding=True)


