#############################################################################
# Extract assignments data from Assignment XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')


#############################################################################
def create_line(xml_part):

    to_extract = [".//patent-properties/patent-property",
                  ".//assignment-record/reel-no",
                  ".//assignment-record/frame-no",
                  ".//assignment-record/last-update-date/date",
                  ".//assignment-record/purge-indicator",
                  ".//assignment-record/recorded-date/date",
                  ".//assignment-record/correspondent/name",
                  ".//assignment-record/correspondent/address-1",
                  ".//assignment-record/correspondent/address-2",
                  ".//assignment-record/correspondent/address-3",
                  ".//assignment-record/correspondent/address-4",
                  ".//assignment-record/conveyance-text"
                 ]
#    to_extract = [".//patent-properties/patent-property",
#                  "assignment-record/reel-no",
#                  "assignment-record/frame-no",
#                  "assignment-record/last-update-date/date",
#                  "assignment-record/purge-indicator",
#                  "assignment-record/recorded-date/date",
#                  "assignment-record/correspondent/name",
#                  "assignment-record/correspondent/address-1",
#                  "assignment-record/correspondent/address-2",
#                  "assignment-record/correspondent/address-3",
#                  "assignment-record/correspondent/address-4",
#                  "assignment-record/conveyance-text"
#                 ]

    return helpers.as_extract(xml_part, to_extract)
