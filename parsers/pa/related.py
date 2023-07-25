#############################################################################
# Extract related publication data from OLD Application XML file
#############################################################################
import xml.etree.ElementTree as ET
import importlib
import re
import sys
from datetime import datetime
helpers = importlib.import_module('.helpers', 'parsers')

#############################################################################
def create_line(xml_part):
    to_extract = [
                  ".//domestic-filing-data/application-number/doc-number",
                  ".//cross-reference-to-related-applications/paragraph",
                 ]

    xml = ET.fromstring(xml_part)

    res_list = []
    result = ''

    for tag in to_extract:
        if tag.endswith('paragraph'):
            parts = xml.findall(tag)
            for part in parts:
                unp = helpers.get_value(part)
                match_docs = re.findall(r' ((\d{1,}|\w{3})(/|,)+\w{2}?\d{1,},? ?/?\d{1,})',unp)
                match_dates = re.findall(r'([[a-zA-Z]{3}\.* \d{1,2}, ?\d{4}]*?)',unp)
                docs = []
                for elm in match_docs:
                    if elm[0] and elm[0] not in docs and len(elm[0]) >= 8: docs.append(elm[0])
                dates = []
                for elm in match_dates:
                    if elm:
                        dstr = elm.replace('.','')
                        dstr = dstr.replace(', ',',')
                        try:
                            date = datetime.strftime(datetime.strptime(dstr,'%b %d,%Y'), '%Y%m%d')
                        except Exception:
                            date = '-'
                        dates.append(date)
                corr = map(None, docs, dates)
                corr = [elm for elm in corr if elm[0]]
                for elm in corr:
                    buf_list = res_list[:]
                    buf_list.extend([elm[0]] + ['-'] + [elm[1] if elm[1] else '-'] )
                    result += u"\t".join(buf_list).encode('utf-8').strip()+"\n"
#                    sys.stdout.write(u"\t".join(buf_list).encode('utf-8').strip()+"\n")
        else:
            ct = xml.find(tag)
            res_list.extend([helpers.get_value(ct)] + ['-'])

    return result

