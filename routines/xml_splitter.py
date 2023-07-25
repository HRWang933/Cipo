#############################################################################
# XML splitter handlers
#############################################################################
import os
import logging
import re
from xml_header import marker
from xml.sax.saxutils import unescape
import re

def repl_unknown(xml_part):
    unp = unescape(xml_part)
    matches = re.findall(r'&([a-zA-Z\d\s]*?);',unp)
    for elm in matches:
        xml_part = xml_part.replace('&'+elm+';','('+elm+')')
    return re.sub(r'[^\x00-\x7f]',r' ', xml_part)

#############################################################################
# Split Patent Grant XML file to list of XML
#############################################################################
def extract_xml_parts(xml_file):
    if not xml_file:
        logging.error('Incorrect argument for XML splitter')
        return False

    name = os.path.basename(xml_file)
    dig = re.search('\d', name)
    f_type = name[:dig.start()] if dig else False

    borders = {
               'ipg':{'open_tag':'<us-patent-grant', 'close_tag':'</us-patent-grant>'},
               'ipa':{'open_tag':'<us-patent-application', 'close_tag':'</us-patent-application>'},
               'ad' :{'open_tag':'<patent-assignment>', 'close_tag':'</patent-assignment>'},
               'pg' :{'open_tag':'<PATDOC', 'close_tag':'</PATDOC>'},
               'pa' :{'open_tag':'<patent-application-publication>', 'close_tag':'</patent-application-publication>'}
              }

    open_tag  = borders.get(f_type).get('open_tag')
    close_tag = borders.get(f_type).get('close_tag')

    if not open_tag or not close_tag:
        raise Exception(('Can\'t split file <%s>') % (name))

    in_file = open(xml_file, "r")
    res = []
    xmls = []
    i = 0
    for line in in_file:
        if line.lstrip().startswith(open_tag):
            if len(res) == 0:
                res.append(line.lstrip())
                continue
        if line.lstrip().startswith(close_tag):
            res.append(line.lstrip())
            res.insert(0, marker)
#            elm = ("".join(res)).replace('&',' ')
            elm = ("".join(res))
            xmls.append(elm)
            i+=1
            res = []
            continue
        if len(res) != 0: res.append(repl_unknown(line))


    return xmls


