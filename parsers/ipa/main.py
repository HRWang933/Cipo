#############################################################################
# Extract main data from Applicaton XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):

    to_extract = [".//application-reference/document-id/doc-number",
                  ".//publication-reference/document-id/country",
                  ".//publication-reference/document-id/doc-number",
                  ".//publication-reference/document-id/kind",
                  ".//publication-reference/document-id/date",
                  ".//application-reference/document-id/country",
                  ".//application-reference/document-id/date",
                  ".//us-application-series-code",
                  ".//us-issued-on-continued-prosecution-application",
                  ".//rule-47-flag",
                  ".//us-term-extension",
                  ".//length-of-grant",
                  ".//invention-title",
                  ".//number-of-claims",
                  ".//us-exemplary-claim",
                  ".//us-botanic/variety",
                  ".//examiners/primary-examiner/department",
                  ".//examiners/primary-examiner/first-name",
                  ".//examiners/primary-examiner/last-name",
                  ".//pct-or-regional-filing-data/document-id/date",
                  ".//pct-or-regional-filing-data/document-id/country",
                  ".//pct-or-regional-filing-data/us-371c124-date/date",
                  ".//pct-or-regional-publishing-data/document-id/date",
                  ".//pct-or-regional-publishing-data/document-id/country"
                 ]

    xml = ET.fromstring(xml_part)

    res_list = []

    for tag in to_extract:
        ct = xml.find(tag)
        if tag == ".//rule-47-flag":
            if ct is not None:
                res_list.append('True')
            else: res_list.append('False')
        else:
            res_list.append(helpers.get_value(ct))


    result = u"\t".join(res_list).encode('utf-8').strip()+"\n"
    return result
