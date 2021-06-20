import os
import lxml.etree as ET

def option_names_in_file(path_of_dot_setting):
    """Return a list of options in the specified file"""
    name_list = []

    if os.path.isfile(path_of_dot_setting):
        file = open(path_of_dot_setting, 'r')

        for line in file.readlines():
            if line[0] != '#' and line[0] != ' ' and line[0] != '\n':
                name_list.append(line.split(':', 1)[0])

        file.close()

    return name_list


def option_comment(path_to_dot_setting, option_name):

    if os.path.isfile(path_to_dot_setting + '.xml'):

        parser = ET.XMLParser(remove_blank_text=True)

        tree = ET.parse(path_to_dot_setting + '.xml', parser)

        root = tree.getroot()
    
        element = root.find("option[@name='" + option_name.lower().strip() + "']")

        if element == None:
            return None
        else:
            return element.text

    else:
        return None


def file_description(path_to_dot_setting):

    if os.path.isfile(path_to_dot_setting + '.xml'):
        parser = ET.XMLParser(remove_blank_text=True)

        tree = ET.parse(path_to_dot_setting + '.xml', parser)

        root = tree.getroot()

        element = root.find("Description")

        if element == None:
            return None
    
        else:
            return element.text
    else:
        return None


def file_description_lines_num(path_to_dot_setting):
    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()

    element = root.find("Description")

    if element == None:
        return 0
    
    else:
        return len(element.text.split('\n'))


def option_values(path_to_dot_setting, option_name):
    """Returns a list of all values including ranged values"""
    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()

    element = root.find("option[@name='" + option_name.lower().strip() + "']")
    
    value_list = []

    if element == None:
        return []

    for e in element.iter():
        if e.tag == 'value':
            value_list.append(e.attrib['name'])
        elif e.tag == 'range':
            min = 'Unlimited'

            if e.attrib['min'] != '':
                min = e.attrib['min']

            max = 'Unlimited'

            if e.attrib['max'] != '':
                max = e.attrib['max']
               
            step = ''
            if e.attrib['step'] != '':
                step = ' - Step ' + e.attrib['step']

            value_list.append(min + ' To ' + max + step)

    return value_list


def possible_value_by_number(path_to_dot_setting, option_name, number_from_zero):
    """Returns a value from option by it's position in .xml file
       If value is simple returns {'name':value, 'comment':comment}
       If value is range returns {'min':value, 'max':value, 'step':value,'comment':comment}
       700 on option not found
       701 number don't exist"""

    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()

    element = root.find("option[@name='" + option_name.lower().strip() + "']")

    if element == None:
        return 700

    if number_from_zero < 0:
        return 701

    if len(element.getchildren()) >= number_from_zero+1:
        
        value_element = element.getchildren()[number_from_zero]

        if value_element.tag == 'value':
            return {'name':value_element.attrib['name'], 'comment':value_element.text}
        elif value_element.tag == 'range':
            return {'min':value_element.attrib['min'], 'max':value_element.attrib['max'], 'step':value_element.attrib['step'],'comment':value_element.text}
    else:
        return 701


def default_value(path_to_dot_setting, option_name):
    """Returns the default value of an option
       700 on option not found"""

    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()

    element = root.find("option[@name='" + option_name.lower().strip() + "']")

    if element == None:
        return 700

    if 'default' in element.attrib:
        return element.attrib['default']
    else:
        return ''

