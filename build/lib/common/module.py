from . import const
import os
import lxml.etree as ET

def create_setting_file(path):
    if os.path.isfile(path + '.setting'):
        return 701

    if os.path.isfile(path + '.setting.xml'):
        return 702

    try:
        root = ET.Element("root")
        
        tree = ET.ElementTree(root)
        tree.write(path + '.setting.xml', xml_declaration=True, pretty_print=True)

        file = open(path + '.setting', 'w')

        file.write('#This is a setting maker file\n#This file is autogenerated!\n#Please use provided tools for editing and be cautious when editing it manually!\n')

        file.close()

        return 200

    except Exception as e:

        try:
            os.remove(path + '.setting.xml')
        except OSError:
            pass

        try:
            os.remove(path + '.setting')
        except OSError:
            pass

        return e


def verfy_file(path, complete=True):
    """Verfies that path has .setting and .setting.xml file for the given file name.
    If complete is False only checks for .setting file and .setting.xml is not needed

    ** returns name.setting path if file is verfied.
       700: Neither .setting nor .setting.xml file found,
       701: .setting file missing,
       702: .setting.xml file missing"""

    if path[-12:] == '.setting.xml':
        if os.path.isfile(path[:-4]):
            return path[:-4]
        else:
           return 701

    elif path[-8:] == '.setting':
        if complete:
            if os.path.isfile(path + '.xml'):
                return path
            else:
               return 702
        else:
            return path

    else:
        if complete:
            if not os.path.isfile(path + '.setting') and not os.path.isfile(path + '.setting.xml'):
                return 700
            elif not os.path.isfile(path + '.setting'):
                return 701
            elif not os.path.isfile(path + '.setting.xml'):
                return 702
            else:
                return path + '.setting'
        else:
            if not os.path.isfile(path + '.setting'):
                return 701
            else:
                return path + '.setting'


def setting_exists_in_file(path_of_dot_setting, name):
    file = open(path_of_dot_setting, 'r')

    for line in file.readlines():
        if line[0] == '#' or line[0] == ' ' or line[0] == '\n':
            pass
        elif name.upper().strip() == line[:line.find(':')].upper().strip():
            file.close()
            return True

    file.close()
    return False

def get_setting_names_in_file(path_of_dot_setting):
    """Return a list of settings in the specified file"""
    name_list = []

    if os.path.isfile(path_of_dot_setting):
        file = open(path_of_dot_setting, 'r')

        for line in file.readlines():
            if line[0] != '#' and line[0] != ' ' and line[0] != '\n':
                name_list.append(line.split(':', 1)[0])

        file.close()

    return name_list


def add_setting_to_file(path_to_dot_setting, name, comment):
    """Returns 200: Successful,
       201: Definition for setting already exists in setting.xml file"""

    file = open(path_to_dot_setting, 'a')

    file.write('#' + comment + '\n' + name + ':\n')

    file.close()

    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()
                      
    if root.find("setting[@name='" + name.lower() + "']") == None:
        element = ET.Element("setting", name=name.lower())
        element.text = comment
        root.append(element)
        
        tree.write(path_to_dot_setting + '.xml', xml_declaration=True, pretty_print=True)

        return 200
    else:
        return 201
        

def remove_setting_from_file(path_to_dot_setting, name):
    """Returns 200: Successful,
       201: Setting removed successfully but Setting didn't exist in setting.xml file
            It causes no problem in removing but means that .setting.xml was corrupted."""
    file_r = open(path_to_dot_setting, 'r')
    file_temp = open(path_to_dot_setting + '.temp', 'w')

    file_r_contents = file_r.readlines()

    skip = False

    for i in range(len(file_r_contents)):
        if skip == True:
            skip = False
            continue
        elif file_r_contents[i][0] == ' ' or file_r_contents[i][0] == '\n':
            pass
        elif file_r_contents[i][0] == '#' and file_r_contents[i+1][0] != '#':
            if name.upper().strip() == file_r_contents[i+1][:file_r_contents[i+1].find(':')].upper().strip():
                skip = True
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
    
    element = root.find("setting[@name='" + name.lower().strip() + "']")

    if element != None:
        root.remove(element)

        tree.write(path_to_dot_setting + '.xml', xml_declaration=True, pretty_print=True)

        return 200
        
    else:
        return 201


def change_setting_name(path_to_dot_setting, current_name, new_name):
    """Returns 200: Successful,
       201: Setting name was not found in .setting.xml file, file could be corrupted"""
    file_r = open(path_to_dot_setting, 'r')
    file_temp = open(path_to_dot_setting + '.temp', 'w')

    for line in file_r.readlines():
        if line[0] == ' ' or line[0] == '\n':
            pass
        elif current_name.upper().strip() == line[:line.find(':')].upper().strip() and line[0] != '#':
            file_temp.write(new_name.strip() + line[line.find(':'):])
        else:
            file_temp.write(line)

    file_r.close()
    file_temp.close()

    os.remove(path_to_dot_setting)
    os.rename(path_to_dot_setting + '.temp', path_to_dot_setting)

    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()
    
    element = root.find("setting[@name='" + new_name.lower().strip() + "']")

    if element != None:
        root.remove(element)

    element = root.find("setting[@name='" + current_name.lower().strip() + "']")

    if element == None:#This can only happen if .xml file is altered manually

        file_r = open(path_to_dot_setting, 'r')

        file_r_contents = file_r.readlines()
        
        comment = ''

        for i in range(len(file_r_contents)):
            if file_r_contents[i][0] == '#' and file_r_contents[i+1][0] != '#':
                if new_name.upper().strip() == file_r_contents[i+1][:file_r_contents[i+1].find(':')].upper().strip():
                    comment = file_r_contents[i][1:].replace('\n', '')
                    break

        file_r.close()

        element = ET.Element("setting", name=new_name.lower().strip())
        element.text = comment
        root.append(element)

        tree.write(path_to_dot_setting + '.xml', xml_declaration=True, pretty_print=True)

        return 201
    
    else:

        element.attrib['name'] = new_name.lower()

        tree.write(path_to_dot_setting + '.xml', xml_declaration=True, pretty_print=True)

        return 200


def set_default(path_to_dot_setting, setting_name, default_value):
    """Returns 200: Successful,
       201: Setting name was not found in .setting.xml file, file could be corrupted"""
    file_r = open(path_to_dot_setting, 'r')
    file_temp = open(path_to_dot_setting + '.temp', 'w')

    for line in file_r.readlines():
        if line[0] == ' ' or line[0] == '\n':
            pass
        elif setting_name.upper().strip() == line[:line.find(':')].upper().strip() and line[0] != '#':
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
    
    element = root.find("setting[@name='" + setting_name.lower().strip() + "']")

    if element == None:#This can only happen if .xml file is altered manually

        file_r = open(path_to_dot_setting, 'r')

        file_r_contents = file_r.readlines()
        
        comment = ''

        for i in range(len(file_r_contents)):
            if file_r_contents[i][0] == '#' and file_r_contents[i+1][0] != '#':
                if setting_name.upper().strip() == file_r_contents[i+1][:file_r_contents[i+1].find(':')].upper().strip():
                    comment = file_r_contents[i][1:].replace('\n', '')
                    break

        file_r.close()

        element = ET.Element("setting", name=setting_name.lower().strip())
        element.attrib['default']=default_value
        element.text = comment
        root.append(element)

        tree.write(path_to_dot_setting + '.xml', xml_declaration=True, pretty_print=True)

        return 201
    
    else:

        element.attrib['default'] = default_value

        tree.write(path_to_dot_setting + '.xml', xml_declaration=True, pretty_print=True)

        return 200


def set_setting_value(path_to_dot_setting, setting_name, value):
    """Returns 200: Successful,
       701: Setting name was not found in .setting"""

    value = str(value).strip() #Input could be str or int so let's cover both

    file_r = open(path_to_dot_setting, 'r')
    file_temp = open(path_to_dot_setting + '.temp', 'w')

    success = False

    for line in file_r.readlines():
        if line[0] == ' ' or line[0] == '\n':
            pass
        elif setting_name.upper().strip() == line[:line.find(':')].upper().strip() and line[0] != '#':
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


def set_setting_comment(path_to_dot_setting, setting_name, comment):
    """Returns 200: Successful,
       201: Setting name was not found in .setting.xml file, file could be corrupted"""
    file_r = open(path_to_dot_setting, 'r')
    file_temp = open(path_to_dot_setting + '.temp', 'w')

    file_r_contents = file_r.readlines()

    for i in range(len(file_r_contents)):
        if file_r_contents[i][0] == '#' and file_r_contents[i+1][0] != '#':
            if setting_name.upper().strip() == file_r_contents[i+1][:file_r_contents[i+1].find(':')].upper().strip():
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
    
    element = root.find("setting[@name='" + setting_name.lower().strip() + "']")

    if element == None:#This can only happen if .xml file is altered manually

        element = ET.Element("setting", name=setting_name.lower().strip())
        element.text = comment
        root.append(element)

        tree.write(path_to_dot_setting + '.xml', xml_declaration=True, pretty_print=True)

        return 201
    
    else:

        element.text = comment

        tree.write(path_to_dot_setting + '.xml', xml_declaration=True, pretty_print=True)

        return 200


def get_setting_comment(path_to_dot_setting, setting_name):

    if os.path.isfile(path_to_dot_setting + '.xml'):

        parser = ET.XMLParser(remove_blank_text=True)

        tree = ET.parse(path_to_dot_setting + '.xml', parser)

        root = tree.getroot()
    
        element = root.find("setting[@name='" + setting_name.lower().strip() + "']")

        if element == None:
            return None
        else:
            return element.text

    else:
        return None


def set_file_description(path_to_dot_setting, description):

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

    for i in range(get_file_description_lines_num(path_to_dot_setting) + const.RESERVE_LINES , len(file_r_contents)):
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


def get_file_description(path_to_dot_setting):

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


def get_file_description_lines_num(path_to_dot_setting):
    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()

    element = root.find("Description")

    if element == None:
        return 0
    
    else:
        return len(element.text.split('\n'))


def add_simple_value(path_to_dot_setting, setting_name, value, comment):
    """Returns 200: Successful,
       700: Setting not found in .xml file"""
    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()

    element = root.find("setting[@name='" + setting_name.lower().strip() + "']")

    if element == None:
        return 700
    
    else:

        sub_element = ET.Element("value", name=value.lower().strip())
        sub_element.text = comment

        element.append(sub_element)

        tree.write(path_to_dot_setting + '.xml', xml_declaration=True, pretty_print=True)

        return 200


def add_range_value(path_to_dot_setting, setting_name, min, max, step, comment):
    """Returns 200: Successful,
       700: Setting not found in .xml file
       701: Min is not a number
       702: Max is not a number
       703: step is not a number
       704: all are empty"""

    if min == max == step == '':
        return 704

    if min != '':
        try:
            float(min)
        except:
            return 701
    
    if max != '':
        try:
            float(max)
        except:
            return 702

    if step != '':
        try:
            float(step)
        except:
            return 703

    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()

    element = root.find("setting[@name='" + setting_name.lower().strip() + "']")

    if element == None:
        return 700
    
    else:

        sub_element = ET.Element("range")
        sub_element.attrib['min'] = min
        sub_element.attrib['max'] = max
        sub_element.attrib['step'] = step
        sub_element.text = comment

        element.append(sub_element)

        tree.write(path_to_dot_setting + '.xml', xml_declaration=True, pretty_print=True)

        return 200


def setting_simple_value_exists(path_to_dot_setting, setting_name, value):
    
    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()

    element = root.find("setting[@name='" + setting_name.lower().strip() + "']")

    if element == None:
        return False
    
    else:

        sub_element = element.find("value[@name='" + value.lower().strip() + "']")

        if sub_element == None:
            return False
        else:
            return True


def setting_renage_value_exists(path_to_dot_setting, setting_name, min, max, step):
    
    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()

    element = root.find("setting[@name='" + setting_name.lower().strip() + "']")

    if element == None:
        return False
    
    else:

        sub_element = element.find("range[@min='" + min.lower().strip() + "'][@max='" + max.lower().strip() + "'][@step='" + step.lower().strip() + "']")

        if sub_element == None:
            return False
        else:
            return True


def get_setting_values(path_to_dot_setting, setting_name):
    """Returns a list of all values including ranged values"""
    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()

    element = root.find("setting[@name='" + setting_name.lower().strip() + "']")
    
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
                step = ' Step: ' + e.attrib['step']

            value_list.append(min + ' To ' + max + step)

    return value_list


def remove_possible_value_by_number(path_to_dot_setting, setting_name, number_from_zero):
    """Removes a value from a setting by it's position in .xml file
       Return: 200 on success
               700 on setting not found
               701 number don't exist"""

    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()

    element = root.find("setting[@name='" + setting_name.lower().strip() + "']")

    if element == None:
        return 700

    if number_from_zero < 0:
        return 701

    if len(element.getchildren()) >= number_from_zero+1:
       
        element.remove(element.getchildren()[number_from_zero])

        tree.write(path_to_dot_setting + '.xml', xml_declaration=True, pretty_print=True)
        
        return 200

    else:
        return 701


def get_possible_value_by_number(path_to_dot_setting, setting_name, number_from_zero):
    """Returns a value from setting by it's position in .xml file
       If value is simple returns {'name':value, 'comment':comment}
       If value is range returns {'min':value, 'max':value, 'step':value,'comment':comment}
       700 on setting not found
       701 number don't exist"""

    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()

    element = root.find("setting[@name='" + setting_name.lower().strip() + "']")

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


def set_value_comment_by_number(path_to_dot_setting, setting_name, number_from_zero, comment):
    """Sets a comment for a value in setting by it's position in .xml file
       Return: 200 on success
               700 on setting not found
               701 number don't exist"""

    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()

    element = root.find("setting[@name='" + setting_name.lower().strip() + "']")

    if element == None:
        return 700

    if number_from_zero < 0:
        return 701

    if len(element.getchildren()) >= number_from_zero+1:
        
        element.getchildren()[number_from_zero].text = comment

        tree.write(path_to_dot_setting + '.xml', xml_declaration=True, pretty_print=True)

        return 200
        
    else:
        return 701


def set_simple_possible_value_by_number(path_to_dot_setting, setting_name, number_from_zero, new_name):
    """Sets name for a simple value in setting by it's position in .xml file
       Return: 200 on success
               700 on setting not found
               701 number don't exist"""

    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()

    element = root.find("setting[@name='" + setting_name.lower().strip() + "']")

    if element == None:
        return 700

    if number_from_zero < 0:
        return 701

    if len(element.getchildren()) >= number_from_zero+1:
        
        element.getchildren()[number_from_zero].attrib['name'] = new_name

        tree.write(path_to_dot_setting + '.xml', xml_declaration=True, pretty_print=True)

        return 200
        
    else:
        return 701


def set_ranged_possible_value_by_number(path_to_dot_setting, setting_name, number_from_zero, min, max, step):
    """Sets values for a ranged value in setting by it's position in .xml file
       Return: 200 on success
               700 on setting not found
               701 number don't exist
               703 Can't have 3 empty values"""


    if min == max == step == '':
        return 703

    parser = ET.XMLParser(remove_blank_text=True)

    tree = ET.parse(path_to_dot_setting + '.xml', parser)

    root = tree.getroot()

    element = root.find("setting[@name='" + setting_name.lower().strip() + "']")

    if element == None:
        return 700

    if number_from_zero < 0:
        return 701

    if len(element.getchildren()) >= number_from_zero + 1:
        
        range_element = element.getchildren()[number_from_zero]
       
        range_element.attrib['min'] = min
        range_element.attrib['max'] = max
        range_element.attrib['step'] = step

        tree.write(path_to_dot_setting + '.xml', xml_declaration=True, pretty_print=True)

        return 200
        
    else:
        return 701


def diff_to_step(min, max, step, value):
    """Returns '0' if value is in step or how much value should change to reach step"""

    round_by = len(str(step).split('.')[1])#round the value to avoid many decimal ponit 1 stuff in result

    if ( min == max and (min != None or min == '') ) or step == None or step == '' or min == value:
        return 0

    if min == None or min == '':
        min = 0
    
    try:
        min = float(min)
        step = float(step)
        value = float(value)
    except:
        pass

    if min < value:
        while min < value:
            value = round(value - step, round_by)

            if min == value:
                return 0
                break

        return round((value + step) - min, round_by)
        

    elif min > value:
        while value < min:
            value = round(value + step, round_by)

            if min == value:
                return 0
                break

        return round(min - (value - step), round_by)

