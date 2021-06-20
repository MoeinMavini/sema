from sema.common import const, get
import os
import lxml.etree as ET

def option_value(path_to_dot_setting, option_name, value):
    """Returns 200: Successful,
       701: Option name was not found in .setting"""

    value = str(value).strip() #Input could be str or int so let's cover both

    file_r = open(path_to_dot_setting, 'r')
    file_temp = open(path_to_dot_setting + '.temp', 'w')

    success = False

    for line in file_r.readlines():
        if line[0] == ' ' or line[0] == '\n':
            pass
        elif option_name.upper().strip() == line[:line.find(':')].upper().strip() and line[0] != '#':
            success = True
            file_temp.write(line[:line.find(':')] + ':' + value.strip() + '\n')
        else:
            file_temp.write(line)

    file_r.close()
    file_temp.close()

    os.remove(path_to_dot_setting)
    os.rename(path_to_dot_setting + '.temp', path_to_dot_setting)

    if success:
        return 200
    else:
        return 701


def file_description(path_to_dot_setting, description):

    description_list = description.split('\n')

    file_r = open(path_to_dot_setting, 'r')
    file_temp = open(path_to_dot_setting + '.temp', 'w')

    file_r_contents = file_r.readlines()

    for i in range(const.RESERVE_LINES):
            file_temp.write(file_r_contents[i])

    for i in range(len(description_list)):
            if description_list[i] == '\n':
                continue
            file_temp.write('#' + description_list[i] + '\n')

    for i in range(get.file_description_lines_num(path_to_dot_setting) + const.RESERVE_LINES , len(file_r_contents)):
        file_temp.write(file_r_contents[i])
            
    file_r.close()
    file_temp.close()

    os.remove(path_to_dot_setting)
    os.rename(path_to_dot_setting + '.temp', path_to_dot_setting)

    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()

    element = root.find("Description")

    if element == None:
        element = ET.Element("Description")
        element.text = description
        root.append(element)
    
    else:
        element.text = description

    tree.write(path_to_dot_setting + '.xml', xml_declaration=True, pretty_print=True)

    return 200


def default(path_to_dot_setting, option_name, default_value):
    """Returns 200: Successful,
       201: Option name was not found in .setting.xml file, file could be corrupted"""
    file_r = open(path_to_dot_setting, 'r')
    file_temp = open(path_to_dot_setting + '.temp', 'w')

    for line in file_r.readlines():
        if line[0] == ' ' or line[0] == '\n':
            pass
        elif option_name.upper().strip() == line[:line.find(':')].upper().strip() and line[0] != '#':
            if line.split(':', 1)[1].strip() == '':
                file_temp.write(line[:line.find(':')] + ':' + default_value + '\n')
            else:
                file_temp.write(line)
        else:
            file_temp.write(line)

    file_r.close()
    file_temp.close()

    os.remove(path_to_dot_setting)
    os.rename(path_to_dot_setting + '.temp', path_to_dot_setting)

    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()
    
    element = root.find("option[@name='" + option_name.lower().strip() + "']")

    if element == None:#This can only happen if .xml file is altered manually

        file_r = open(path_to_dot_setting, 'r')

        file_r_contents = file_r.readlines()
        
        comment = ''

        for i in range(len(file_r_contents)):
            if file_r_contents[i][0] == '#' and file_r_contents[i+1][0] != '#':
                if option_name.upper().strip() == file_r_contents[i+1][:file_r_contents[i+1].find(':')].upper().strip():
                    comment = file_r_contents[i][1:].replace('\n', '')
                    break

        file_r.close()

        element = ET.Element("option", name=option_name.lower().strip())
        element.attrib['default']=default_value
        element.text = comment
        root.append(element)

        tree.write(path_to_dot_setting + '.xml', xml_declaration=True, pretty_print=True)

        return 201
    
    else:

        element.attrib['default'] = default_value

        tree.write(path_to_dot_setting + '.xml', xml_declaration=True, pretty_print=True)

        return 200


def option_comment(path_to_dot_setting, option_name, comment):
    """Returns 200: Successful,
       201: Option name was not found in .setting.xml file, file could be corrupted"""
    file_r = open(path_to_dot_setting, 'r')
    file_temp = open(path_to_dot_setting + '.temp', 'w')

    file_r_contents = file_r.readlines()

    for i in range(len(file_r_contents)):
        if file_r_contents[i][0] == '#' and file_r_contents[i+1][0] != '#':
            if option_name.upper().strip() == file_r_contents[i+1][:file_r_contents[i+1].find(':')].upper().strip():
                file_temp.write('#' + comment + '\n')

            else:
                file_temp.write(file_r_contents[i])
        
        else:
            file_temp.write(file_r_contents[i])


    file_r.close()
    file_temp.close()

    os.remove(path_to_dot_setting)
    os.rename(path_to_dot_setting + '.temp', path_to_dot_setting)

    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()
    
    element = root.find("option[@name='" + option_name.lower().strip() + "']")

    if element == None:#This can only happen if .xml file is altered manually

        element = ET.Element("option", name=option_name.lower().strip())
        element.text = comment
        root.append(element)

        tree.write(path_to_dot_setting + '.xml', xml_declaration=True, pretty_print=True)

        return 201
    
    else:

        element.text = comment

        tree.write(path_to_dot_setting + '.xml', xml_declaration=True, pretty_print=True)

        return 200

