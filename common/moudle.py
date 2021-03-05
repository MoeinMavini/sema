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


def edit(path):

    verfy_result = verfy_file(path)

    if verfy_result == 700:
        print('\nChosen file is not a setting maker file\nFile must have .setting extension with a .setting.xml file in the same directory\n')
    elif verfy_result == 701:
        print('\n.setting file missing! Both .setting and .setting.xml are required\n')
    elif verfy_result == 702:
        print('\n.setting.xml file missing! Both .setting and .setting.xml are required\n')
    else:
        path = verfy_result

        print('\nThis file contains this settings: ' + str(get_setting_names_in_file(path)))

        while True:
            choice = input("\nEnter '1' to edit a setting\nEnter '2' to add a new setting\n"
                           "Enter '3' to remove a setting\nEnter '4' to see the list of settings in current file\n"
                           "Enter 0 to get back\n\n->").strip()

            if choice == '0' or choice == '':
                break;

            elif choice == '1':
                pass

            elif choice == '2':
                while True:
                    name = input('Enter the setting name: ').strip()

                    if ':' in name:
                        print("\nName must not contain ':'\n")
                    elif '\n' in name:
                        print("\nError: Name includes new line\n")
                    elif name == '':
                        break
                    elif setting_exists_in_file(path, name):
                        print('\nThis setting name already exists!\n')
                    else:
                        while True:
                            comment = input('Enter the single line comment for setting: ')

                            if '\n' in comment:
                                print("\nError: Comment includes new line\n")
                            else:
                                file = open(path, 'a')

                                file.write('#' + comment + '\n' + name + ':\n')

                                file.close()

                                tree = ET.parse(path + '.xml')

                                root = tree.getroot()
                            
                                if root.find(name) == None:
                                    ET.SubElement(root, name)

                                    tree.write(path + '.xml', xml_declaration=True, pretty_print=True)

                                    print('\nSetting created successfully\n')
                                else:
                                    print('\nCaution: Definition for setting ' + name + ' already exists in setting.xml file\n')
                            
                                break
                    break

            elif choice == '3':
                pass

            elif choice == '4':
                print('\nThis file contains this settings: ' + str(get_setting_names_in_file(path)))

            else:
                print('\nCommand not found!\n')


def verfy_file(path):
    """Verfies that path has .setting and .setting.xml file for the given file name.
    
    ** returns name.setting path if file is verfied.
       700: Chosen file is not a setting maker file,
       701: .setting file missing,
       702: .setting.xml file missing"""

    if path[-12:] == '.setting.xml':
        if os.path.isfile(path[:-4]):
            return path[:-4]
        else:
           return 701

    elif path[-8:] == '.setting':
        if os.path.isfile(path + '.xml'):
            return path
        else:
           return 702
    else:
        if not os.path.isfile(path + '.setting') and not os.path.isfile(path + '.setting.xml'):
            return 700
        elif not os.path.isfile(path + '.setting'):
            return 701
        elif not os.path.isfile(path + '.setting.xml'):
            return 702
        else:
            return path + '.setting'


def setting_exists_in_file(path_of_dot_setting, name):
    file = open(path_of_dot_setting, 'r')

    for line in file.readlines():
        if line[0] == '#' or line[0] == ' ' or line[0] == '\n':
            pass
        elif name.upper() + ':' in line.upper():
            return True

    return False

    file.close()

def get_setting_names_in_file(path_of_dot_setting):
    
    name_list = []

    if os.path.isfile(path_of_dot_setting):
        file = open(path_of_dot_setting, 'r')

        for line in file.readlines():
            if line[0] != '#' and line[0] != ' ' and line[0] != '\n':
                name_list.append(line.split(':')[0])

        file.close()

    return name_list

