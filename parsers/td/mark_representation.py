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

    parts_tag = './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkRepresentation/tmk:MarkReproduction/tmk:MarkImageBag/tmk:MarkImage/tmk:MarkImageClassification/com:FigurativeElementClassificationBag/com:ViennaClassificationBag/com:ViennaClassification'


    sub_tags = ['.//com:ViennaCategory',
                './/com:ViennaDivision',
                './/com:ViennaSection',
                './/cacom:ViennaDescriptionBag/cacom:ViennaDescription[@com:languageCode="en"]',
                './/cacom:ViennaDescriptionBag/cacom:ViennaDescription[@com:languageCode="fr"]' 
               ]

    to_extract2=[ './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkRepresentation/tmk:MarkFeatureCategory',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkRepresentation/tmk:MarkReproduction/tmk:WordMarkSpecification/tmk:MarkSignificantVerbalElementText',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkRepresentation/tmk:MarkReproduction/tmk:WordMarkSpecification/tmk:MarkTranslationText',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkRepresentation/tmk:MarkReproduction/tmk:WordMarkSpecification/tmk:MarkTransliteration',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkRepresentation/tmk:MarkReproduction/tmk:WordMarkSpecification/tmk:MarkStandardCharacterIndicator',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkRepresentation/tmk:MarkReproduction/tmk:MarkImageBag/tmk:MarkImage/com:FileName',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkRepresentation/tmk:MarkReproduction/tmk:MarkImageBag/tmk:MarkImage/com:ImageFormatCategory',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkRepresentation/tmk:MarkReproduction/tmk:MarkImageBag/tmk:MarkImage/tmk:MarkImageColourClaimedText',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkRepresentation/tmk:MarkReproduction/tmk:MarkSoundBag/tmk:MarkSound/com:FileName',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkRepresentation/tmk:MarkReproduction/tmk:MarkSoundBag/tmk:MarkSound/tmk:SoundFileFormatCategory',
               #  './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkRepresentation/tmk:MarkReproduction/com:ViennaClassificationBag/',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkRepresentation/tmk:MarkReproduction/tmk:MarkMultimediaBag/tmk:MarkMultimedia/com:FileName',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkRepresentation/tmk:MarkReproduction/tmk:MarkMultimediaBag/tmk:MarkMultimedia/tmk:MarkMultimediaFileFormatCategory',
                  './/tmk:TrademarkBag/tmk:Trademark/tmk:MarkRepresentation/tmk:MarkDescriptionBag/tmk:MarkDescriptionText'
                  ]

    parts_tag2 = ''
    sub_tags2 = []

    return helpers.td_extract(xml_part, to_extract, ns, parts_tag, sub_tags,parts_tag2, sub_tags2, to_extract2)

