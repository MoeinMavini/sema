import os
import lxml.etree as ET

def file_exists(path, complete=True):
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


def diff_to_step(min, max, step, value):
    """Returns '0' if value is in step or how much value should change to reach step"""

    round_by = len(str(value).split('.')[1])#round the value to avoid many decimal ponit 1 stuff in result

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


def setting_name(name):
    """Checks if setting name is valid 
    
        Returns:
            200 if ok,
            700 if name == '',
            701 if ':' in name,
            702 if ',' in name,
            703 if name[0] == '#',
            704 if '\n' in name"""

    if name == '':
        return 700
    elif ':' in name:
        return 701
    elif ',' in name:
        return 702
    elif name[0] == '#':
        return 703
    elif '\n' in name:
        return 704
    else:
        return 200


def general_value(value):
    """Checks if value is generally valid 
    
        Returns:
            200 if ok,
            700 if ',' in value,
            701 if '\n' in value"""

    if ',' in value:
        return 700
    elif '\n' in value:
        return 701
    else:
        return 200