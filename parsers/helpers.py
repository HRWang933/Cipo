#############################################################################
# Helper functions for different parsers
#############################################################################
import xml.etree.ElementTree as ET
import logging
import time
import sys
import os
import collections

#############################################################################
# Extract value from given tag content, return "-" when no content found
#############################################################################
def get_value(arg):
    if arg is not None and len(arg) > 0:
        res = []
        for elm in arg:
            head = elm.text if (elm is not None and elm.text is not None) else "-"
            tail = elm.tail if (elm is not None and elm.tail is not None) else "-"
            res.extend([head,tail])
        return ' '.join(res)
    else: return arg.text.replace('\n',' ').strip() if (arg is not None and arg.text is not None) else "-"

#############################################################################
# Get list of tags content from particular tag
#############################################################################
def get_parts(xml_part, parts_tag, app_num_tag):

    xml = ET.fromstring(xml_part)

    app_num = xml.find(app_num_tag).text

    parts = xml.findall(parts_tag)

    return [parts, app_num]

#############################################################################
# Get nested lists of tags content from particular tag
#############################################################################
def get_multi_parts(xml_part, parts_tag, app_num_tag):

    xml = ET.fromstring(xml_part)

    app_num = xml.find(app_num_tag).text

    parts = []
    for part in parts_tag: parts.extend(xml.findall(part))

    return [parts, app_num]


#############################################################################
# Common extract routine used for extract plain list of results
#############################################################################
def extract(xml_part, to_extract, parts_tag, app_num_tag):
    try:
        args = get_parts(xml_part, parts_tag, app_num_tag)
        parts = args[0]
        app_num = args[1]
        if len(parts) != 0:
            result = ''
            for elm in parts:
                res_list = [app_num]
                for tag in to_extract:
                    ct = elm.find(tag)
                    res_list.append(get_value(ct))
                result += u"\t".join(res_list).encode('utf-8').strip()+"\n"
            return result

        else: return False
    except Exception as err:
        logging.error('General parser error!')
        logging.error(err)
        return False

#############################################################################
# Common extract routine used for extract nested lists of results
#############################################################################
def multi_extract(xml_part, to_extract, parts_tag, app_num_tag):
    try:
        args = get_multi_parts(xml_part, parts_tag, app_num_tag)
        parts = args[0]
        app_num = args[1]
        if len(parts) != 0:
            result = ''
            for elm in parts:
                res_list = [app_num]
                for e_part in to_extract:
                    for tag in e_part:
                        ct = elm.find(tag)
                        res = get_value(ct)
                        if res != '-': break

                    res_list.append(res)

                result += u"\t".join(res_list).encode('utf-8').strip()+"\n"
            return result

        else: return False
    except Exception as err:
        logging.error('General parser error!')
        logging.error(err)
        return False

#############################################################################
# Special extractor used by agent parser
#############################################################################
def w_extract(xml_part, to_extract, parts_tag, app_num_tag, add_tag=None):
    try:
        args = get_parts(xml_part, parts_tag, app_num_tag)
        parts = args[0]
        app_num = args[1]

        if len(parts) != 0:
            result = ''
            for elm in parts:
                if add_tag:
                    res_list = [app_num, elm.get(add_tag)]
                else:
                    res_list = [app_num, '-']
                for tag in to_extract:
                    ct = elm.find(tag)
                    res_list.append(get_value(ct))
                result += u"\t".join(res_list).encode('utf-8').strip() +"\n"
            return result

        else: return False
    except Exception as err:
        logging.error('W-parser error!')
        logging.error(err)
        return False

#############################################################################
# Special extractor used by agent parser (old XML version)
#############################################################################
def w_old_extract(xml_part, to_extract, parts_tag, app_num_tag, add_tag=None):
    try:
        args = get_parts(xml_part, parts_tag, app_num_tag)
        parts = args[0]
        app_num = args[1]

        if len(parts) != 0:
            result = ''
            for elm in parts:
                res_list = [app_num, '-']
                for tag in to_extract:
                    ct = elm.find(tag)
                    res_list.append(get_value(ct))
                result += u"\t".join(res_list).encode('utf-8').strip() +"\n"
            return result

        else: return False
    except Exception as err:
        logging.error('W-parser error!')
        logging.error(err)
        return False

#############################################################################
# Get and format classification string for classification parser
#############################################################################
def get_class(arg):

    tmp = arg.replace(' ','0')

    sbc = tmp[3:] if len(tmp[3:]) <= 3 else tmp[3:6] + '.' + tmp[6:] + '0'*(3-len(tmp[6:]))

    fpt = tmp[:3]
    return [fpt if fpt[0] != '0' else fpt[1:], sbc]

#############################################################################
# Special extractor used by classification parser
#############################################################################
def cl_extract(xml_part, to_extract, parts_tag, app_num_tag):
    try:
        args = get_parts(xml_part, parts_tag, app_num_tag)
        parts = args[0]
        app_num = args[1]
        if len(parts) != 0:
            result = ''
            for elm in parts:
                res_list = [app_num]
                for tag in to_extract:
                    ct = elm.find(tag)
                    if tag == "country":
                        res_list.append(get_value(ct))
                    elif tag == "main-classification":
                        value = get_value(ct)
                        if value != '-':
                            res_list.extend(get_class(value))
                        else: res_list.extend(['-', '-'])
                    elif tag == "further-classification":
                        temp_list = res_list[:]
                        ct = elm.findall(tag)
                        if len(ct) != 0:
                            for c in ct:
                                value = get_value(c)
                                if value != '-':
				    
                                    res_list.extend(get_class(value))
                                else: res_list.extend(['-', '-'])
                                result += u"\t".join(res_list).encode('utf-8').strip()+"\n"
                                res_list = temp_list[:]

                        else:
                             res_list.extend(['-', '-'])
                             result += u"\t".join(res_list).encode('utf-8').strip()+"\n"
            return result

        else: return False
    except Exception as err:
        logging.error('CL-parser error!')
        logging.error(err)
        return False

#############################################################################
# Special extractor used by classification parser (old XML version)
#############################################################################
def cl_old_extract(xml_part, to_extract, parts_tag, app_num_tag):
    try:
        args = get_parts(xml_part, parts_tag, app_num_tag)
        parts = args[0]
        app_num = args[1]
        if len(parts) != 0:
            result = ''
            for elm in parts:
                res_list = [app_num]
                for tag in to_extract:
                    ct = elm.find(tag)
                    if tag == "country":
                        res_list.append(get_value(ct))
                    elif tag == "B521/PDAT":
                        value = get_value(ct)
                        if value != '-':
                            res_list.extend(get_class(value))
                        else: res_list.extend(['-', '-'])
                    elif tag == "B522/PDAT":
                        temp_list = res_list[:]
                        ct = elm.findall(tag)
                        if len(ct) != 0:
                            for c in ct:
                                value = get_value(c)
                                if value != '-':
                                    res_list.extend(get_class(value))
                                else: res_list.extend(['-', '-'])
                                result += u"\t".join(res_list).encode('utf-8').strip()+"\n"
                                res_list = temp_list[:]

                        else:
                             res_list.extend(['-', '-'])
                             result += u"\t".join(res_list).encode('utf-8').strip()+"\n"
            return result

        else: return False
    except Exception as err:
        logging.error('CL_OLD-parser error!')
        logging.error(err)
        return False

#############################################################################
# Special extractor used by assignment XML parser
#############################################################################
def as_extract(xml_part, to_extract, parts_tag=None, sub_tags=None):
    try:
        t = time.time()
        tlist = to_extract[:]
        xml = ET.fromstring(xml_part)
        props = xml.findall(tlist.pop(0))

        app_id_list = []

        for elm in props:
            if get_value(elm.find('document-id/kind')) == 'X0':
                app_id_list.append(get_value(elm.find('document-id/doc-number')))

        if len(app_id_list) == 0: 
            return False

        result = ''
        main_part = []

        for tag in tlist:
            ct = xml.find(tag)
            main_part.append(get_value(ct))

        if parts_tag and sub_tags:
            parts_list = []
            parts = xml.findall(parts_tag)
            if len(parts) != 0:
                for elm in parts:
                    ins_list = []
                    for tag in sub_tags:
                        ct = elm.find(tag)
                        ins_list.append(get_value(ct))
                    parts_list.append(ins_list)
            else: return False

        for app_id in app_id_list:
            res_list = [app_id]
            res_list.extend(main_part)

            if parts_tag and sub_tags:
                for part in parts_list:
                    temp_list = res_list[:]
                    temp_list.extend(part)
                    result += u"\t".join(temp_list).encode('utf-8').strip()+"\n"
            else:
                result += u"\t".join(res_list).encode('utf-8').strip()+"\n"

        return result

    except Exception as err:
        logging.error('AS-parser error!')
        logging.error(err)
        return False
#############################################################################
# Special extractor used by td XML parser
#############################################################################
def td_extract(xml_file, to_extract, ns, parts_tag=None, sub_tags=None, parts_tag2=None, sub_tags2=None,to_extract2=None, bool_main=False,bool_checklongstr=False,bool_proceeding = False):
    try:
        t = time.time()
        tlist = to_extract[:]

        #xml = ET.fromstring(xml_part)
	proc_date = os.path.basename(xml_file).split('_')[0]
        tree = ET.parse(xml_file)
        xml = tree.getroot()
        props = xml.findall(tlist.pop(0),ns)

        app_id_list = []
  
        for elm in props:
            app_id_list.append(elm.text)
            #if get_value(elm.find('document-id/kind')) == 'X0':
            #    app_id_list.append(get_value(elm.find('document-id/doc-number')))

        if len(app_id_list) == 0: 
            return False

        result = ''
        main_part = []
        if bool_main:
            opC =  xml.find('.//tmk:TrademarkBag/tmk:Trademark',ns).attrib.values()[0]
            if opC:
                main_part.append(opC)
            else:
                main_part.append("-")

        # from to_extract[1:]
        for tag in tlist:
            ct = xml.find(tag,ns)
            main_part.append(get_value(ct))
	#print('main_part:',main_part)

        if parts_tag and sub_tags:
            parts_list = []
            parts = xml.findall(parts_tag,ns)
	    #print('parts:',parts)
            if len(parts) != 0:
                # for each parts_tag found (multiple tag)
                for part_no,elm in enumerate(parts):
                    parts_list2 = []
                    if bool_proceeding:
                        events = xml.findall(parts_tag2,ns)
                        if len(events) != 0:
                            for event in events:
                                ins_list2 = []
                                for tag2 in sub_tags2:
                                    tmp_st2 = get_value(event.find(tag2,ns))
                                    ins_list2.append(tmp_st2)
                                #print('ins_list2:',ins_list2)
                                parts_list2.append(ins_list2)
		            #print(parts_list2)


                    if bool_checklongstr:
                        ins_list = [str(part_no)]
                    else:
                        ins_list = []
                    # for each sub_tags
                    for tag in sub_tags:
                        tmp_st = '-'
                        #logging.info(tag)
                        #logging.info(len(elm.findall(tag,ns)))
                        for seq in range(0,len(elm.findall(tag,ns))):
                            ct = elm.findall(tag,ns)[seq]
                            tmp_st = get_value(ct)
                            #logging.info(tmp_st)
                        if bool_checklongstr:
                            str_keep2 = '-'
                    	    #if len(tmp_st) > 65536:
                            if sys.getsizeof(tmp_st) > 65536:
                    	        str_keep2 = tmp_st[len(tmp_st)/2:]
                    	        tmp_st = tmp_st[0:len(tmp_st)/2]+ '[cont]'
                                if sys.getsizeof(str_keep2) > 65536:
                    	            str_keep2 = tmp_st[len(tmp_st)/3:2*len(tmp_st)/3]
                    	            tmp_st = tmp_st[0:len(tmp_st)/3]+ '[cont]'

                    	ins_list.append(tmp_st)
                    if bool_checklongstr:
                        ins_list.append(str_keep2)
                    #print('ins_list:',len(ins_list), ins_list)
                    if bool_proceeding:
                        if len(parts_list2) !=0:
                            for part2 in parts_list2:
                                part2.insert(0,ins_list[0])
                                part2.extend(ins_list[1:])
                                parts_list.append(part2)
                                #print('part2:',len(part2),part2)
                        else:
                            parts_list.append(ins_list)
                    else:
                        #print('ins_list:',ins_list)
                        parts_list.append(ins_list)
		#print(parts_list)
            else: 
                parts_list = []
                ins_list = []
                # for each sub_tags
                for tag in sub_tags:
		    ins_list.append('-')
                #print('ins_list:',ins_list)
                parts_list.append(ins_list)
		#print(parts_list)
                if to_extract2:
		    pass
                else:
                    return False
        #for part in parts_list:
        #    print(len(part))
        if to_extract2:
            main_part2 = []
            for tag in to_extract2:
                #print(tag)
                ct = xml.find(tag,ns)
                tmp_2 = get_value(ct)
		#print(tmp_2)
                if bool_checklongstr:
                    str_keep = '-'
		    #print(tag,':\n',sys.getsizeof(tmp_2))
		    #print(tag,':\n',len(tmp_2))
                    if len(tmp_2) > 65536:
			#print('get solution')
                    #if sys.getsizeof(tmp_2) > 65536*2:
                        if len(tmp_2) <131072:
                            str_keep = tmp_2[len(tmp_2)/2:]
                            tmp_2 = tmp_2[0:len(tmp_2)/2]+ '[cont]'
                        else:
                            str_keep = tmp_2[65500:131000]
                            tmp_2 = tmp_2[0:65500]+ '[cont]'

	                #print len(tmp_2),tmp_2
	                #print len(str_keep),str_keep
                
                main_part2.append(tmp_2)
            #print('to_extract2:',main_part2)
               
	# appending data together
        for app_id in app_id_list:
            # always add proc_date after app_id ST13ApplicationNumber
            res_list = [app_id,proc_date]
            # from to_extract
            res_list.extend(main_part)

            if parts_tag and sub_tags:
		# from each parts_tag
                for part in parts_list:
                    temp_list = res_list[:]
                    #print('part:',part)
                    temp_list.extend(part)
		    #print(temp_list)
                    if to_extract2:
                        # from to_extract2
		        temp_list.extend(main_part2)
                        if bool_checklongstr:
                            temp_list.append(str_keep)
                            temp_list.append('-')
		    #print(temp_list)
                    result += u"\t".join(temp_list).encode('utf-8').strip()+"\n"
            elif to_extract2:
                temp_list = res_list[:]
                temp_list.extend(parts_list)
		temp_list.extend(main_part2)
                if bool_checklongstr:
                    temp_list.append(str_keep)
                    temp_list.append('-')
		#print(temp_list)
                result += u"\t".join(temp_list).encode('utf-8').strip()+"\n"
            else:
		#print(res_list)
                result += u"\t".join(res_list).encode('utf-8').strip()+"\n"

        return result

    except Exception as err:
        logging.error('TD-parser error!')
        logging.error(err)
        logging.error(xml_file)
        return False
#############################################################################
# Special extractor used by td XML parser
#############################################################################
def td_extractProceeding(xml_file, to_extract, ns, repeat_tag_keylist=None,repeat_tag=None, parts_tag2=None, sub_tags2=None,to_extract2=None, bool_main=False,bool_checklongstr=False,bool_proceeding = False):
    try:
        t = time.time()
        tlist = to_extract[:]

        #xml = ET.fromstring(xml_part)
	proc_date = os.path.basename(xml_file).split('_')[0]
        tree = ET.parse(xml_file)
        xml = tree.getroot()
        props = xml.findall(tlist.pop(0),ns)

        app_id_list = []
  
        for elm in props:
            app_id_list.append(elm.text)
            #if get_value(elm.find('document-id/kind')) == 'X0':
            #    app_id_list.append(get_value(elm.find('document-id/doc-number')))

        if len(app_id_list) == 0: 
            return False
        #print('app_id_list:',app_id_list)

        result = ''
        main_part = []
        if bool_main:
            opC =  xml.find('.//tmk:TrademarkBag/tmk:Trademark',ns).attrib.values()[0]
            if opC:
                main_part.append(opC)
            else:
                main_part.append("-")

        # from to_extract[1:]
        for tag in tlist:
            ct = xml.find(tag,ns)
            main_part.append(get_value(ct))
	#print('main_part:',main_part)

        parts_list = []
        if repeat_tag: 
            #print('repeat tag:',repeat_tag_keylist[0])
            layer1_elm = xml.findall(repeat_tag_keylist[0],ns)
            if len(layer1_elm) != 0:
                for p in xml.findall(repeat_tag_keylist[0],ns):
                    ind_list =[]
                    #print(p)
                    for q in repeat_tag[repeat_tag_keylist[0]]:
                        layer1 = []
                        tmp_st = '-'
                        tmp_st = get_value(p.find(q,ns))
                        #print(tmp_st)
                        layer1.append(tmp_st)
                    #print('repeat tag:',repeat_tag_keylist[1])
                    layer2_elm = p.findall(repeat_tag_keylist[1],ns)
                    if len(layer2_elm) != 0:
                        for p2 in p.findall(repeat_tag_keylist[1],ns):
                            layer2 =[]
                            #print(p2)
                            for q2 in repeat_tag[repeat_tag_keylist[1]]:
                                tmp_st2 = '-'
                                tmp_st2 = get_value(p2.find(q2,ns))
                                #print('=',tmp_st2)
                                layer2.append(tmp_st2)
                                #print('repeat tag:',repeat_tag_keylist[2])
                            layer3_elm = p2.findall(repeat_tag_keylist[2],ns)
                            if len(layer3_elm) != 0:
                                for p3 in p2.findall(repeat_tag_keylist[2],ns):
                                    layer3 =[]
                                    #print(p3)
                                    for q3 in repeat_tag[repeat_tag_keylist[2]]:
                                        tmp_st3 = '-'
                                        tmp_st3 = get_value(p3.find(q3,ns))
                                        #print('==',tmp_st3)
                                        layer3.append(tmp_st3)
                                    ind_list = []
                                    ind_list.extend(layer1)
                                    ind_list.extend(layer2)
                                    ind_list.extend(layer3)
                                    #print(layer1,layer2,layer3)
                                    #print(ind_list)
                                    parts_list.append(ind_list)
                            else:
                            # layer3 elm is none
                                layer3 =[]
                                for q3 in repeat_tag[repeat_tag_keylist[2]]:
                                    tmp_st3 = '-'
                                    #print('==',tmp_st3)
                                    layer3.append(tmp_st3)
                                ind_list = []
                                ind_list.extend(layer1)
                                ind_list.extend(layer2)
                                ind_list.extend(layer3)
                                #print(layer1,layer2,layer3)
                                #print(ind_list)
                                parts_list.append(ind_list)
                    else:
                    # layer2 elm is none 
                       layer2 =[]
                       layer3 =[]
                       for q2 in repeat_tag[repeat_tag_keylist[1]]:
                           tmp_st2 = '-'
                           #print('=',tmp_st2)
                           layer2.append(tmp_st2)
                           #print('repeat tag:',repeat_tag_keylist[2])
                       for q3 in repeat_tag[repeat_tag_keylist[2]]:
                           tmp_st3 = '-'
                           #print('==',tmp_st3)
                           layer3.append(tmp_st3)
                       ind_list = []
                       ind_list.extend(layer1)
                       ind_list.extend(layer2)
                       ind_list.extend(layer3)
                       #print(layer1,layer2,layer3)
                       #print(ind_list)
                       parts_list.append(ind_list)
            else:
                return False
        #for part in parts_list:
        #    print(len(part))
        #    print(part)

	# appending data together
        for app_id in app_id_list:
            # always add proc_date after app_id ST13ApplicationNumber
            res_list = [app_id,proc_date]
            # from to_extract
            res_list.extend(main_part)

            if repeat_tag:
                # from each parts_list
                for part in parts_list:
                    temp_list = res_list[:]
                    #print('part:',part)
                    temp_list.extend(part)
		    #print(temp_list)
                    result += u"\t".join(temp_list).encode('utf-8').strip()+"\n"
            

        return result

    except Exception as err:
        logging.error('TD-parser proceeding error!')
        logging.error(err)
        logging.error(xml_file)
        return False
