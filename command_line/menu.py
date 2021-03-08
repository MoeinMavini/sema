from common import moudle

def start():

    print('\nWelcome to sema setting maker\n')

    while True:
        choice = input("Enter '1' to edit a setting file\nEnter '2' to create a new setting file\n"
                       "Enter 0 to exit\n\n->").strip()

        if choice == '0' or choice == '':
            break;

        elif choice == '1':
            path = input('Enter the name of setting file you want to edit (can include path): ').strip()

            if path != '':
                verfy_result = moudle.verfy_file(path)

                if verfy_result == 700:
                    print('\nChosen file is not a setting maker file\nFile must have .setting extension with a .setting.xml file in the same directory\n')
                elif verfy_result == 701:
                    print('\n.setting file missing! Both .setting and .setting.xml are required\n')
                elif verfy_result == 702:
                    print('\n.setting.xml file missing! Both .setting and .setting.xml are required\n')
                else:
                    edit(verfy_result)

        elif choice == '2':
            path = input('Enter the file name (can include path): ').strip()

            if path != '':
                response = moudle.create_setting_file(path)

                if response == 200:

                    description = get_multiline_input('\nEnter any description you may have for this file')

                    if description != '':
                        moudle.set_file_description(path + '.setting', description)

                    print('\nSetting file created successfully')

                    edit(path + '.setting')

                elif response == 701:
                    print('\nFile already exists\n')
                elif response == 702:
                    print('\nsetting.xml file already exists\n')
                else:
                    print(response)

        else:
            print('\nCommand not found!\n')


def edit(path_to_dot_setting):
    path = path_to_dot_setting

    print('\nThis file contains these settings: ' + str(moudle.get_setting_names_in_file(path)))

    while True:
        choice = input("\nEnter '1' to edit a setting\nEnter '2' to add a new setting\n"
                        "Enter '3' to remove a setting\nEnter '4' to see the list of settings in current file\n"
                        "Enter '5' to set description for this file\nEnter 0 to get back\n\n->").strip()

        if choice == '0' or choice == '':
            break;

        elif choice == '1':
            while True:
                name = input('Enter the setting name: ').strip()

                if ':' in name:
                    print("\nName must not contain ':'\n")
                elif '\n' in name:
                    print("\nError: Name includes new line\n")
                elif name == '':
                    break
                elif not moudle.setting_exists_in_file(path, name):
                    print('\nSetting not found!\n')
                else:
                    while True:
                        choice = input("\nEnter '1' to change setting name\nEnter '2' to change default value\n"
                        "Enter '3' to change comment\nEnter '4' to manage possible values for this setting\n"
                        "Enter 0 to get back\n\n->").strip()

                        if choice == '0' or choice == '':
                            break;

                        elif choice == '1':
                            while True:
                                new_name = input('Enter new setting name: ').strip()

                                if ':' in new_name:
                                    print("\nName must not contain ':'\n")
                                elif '\n' in new_name:
                                    print("\nError: Name includes new line\n")
                                elif new_name == '':
                                    break
                                elif moudle.setting_exists_in_file(path, new_name):
                                    print('\nThis setting name already exists!\n')
                                else:
                                    response = moudle.change_setting_name(path, name, new_name)

                                    if response == 200:
                                        print('\nName changed successfully.\n')
                                    elif response == 201:
                                        print('\nName changed successfully.\nCaution: Setting name was not found in .setting.xml file, file could be corrupted\n')
                                    break

                        elif choice == '2':
                            while True:
                                value = input('Enter default value: ').strip()

                                if ':' in value:
                                    print("\nValue must not contain ':'\n")
                                elif '\n' in value:
                                    print("\nError: Value includes new line\n")
                                elif value == '':
                                    break
                                else:
                                    response = moudle.set_default(path, name, value)

                                    if response == 200:
                                        print('\nDefault value set successfully.\n')
                                    elif response == 201:
                                        print('\nDefault value set successfully.\nCaution: Setting name was not found in .setting.xml file, file could be corrupted\n')
                                    break

                        elif choice == '3':
                            while True:
                                comment = input('Enter the comment: ').strip()

                                if '\n' in comment:
                                    print("\nError: Comment includes new line\n")
                                elif comment == '':
                                    break
                                else:
                                    response = moudle.set_setting_comment(path, name, comment)

                                    if response == 200:
                                        print('\nComment set successfully.\n')
                                    elif response == 201:
                                        print('\nComment set successfully.\nCaution: Setting name was not found in .setting.xml file, file could be corrupted\n')

                                    break

                        elif choice == '4':
                            pass

                        else:
                                print('\nCommand not found!\n')
                                    
                    break


        elif choice == '2':
            while True:
                name = input('Enter the setting name: ').strip()

                if ':' in name:
                    print("\nName must not contain ':'\n")
                elif '\n' in name:
                    print("\nError: Name includes new line\n")
                elif name == '':
                    break
                elif moudle.setting_exists_in_file(path, name):
                    print('\nThis setting name already exists!\n')
                else:
                    while True:
                        comment = input('Enter the single line comment for setting: ').strip()

                        if '\n' in comment:
                            print("\nError: Comment includes new line\n")
                        else:
                            response = moudle.add_setting_to_file(path, name, comment)

                            if response == '200':
                                print('\nSetting created successfully\n')
                            elif response == 201:
                                print('\nCaution: Definition for setting ' + name + ' already exists in setting.xml file\n')
                            break
                break

        elif choice == '3':
            while True:
                name = input('Enter the setting name: ').strip()

                if ':' in name:
                    print("\nName must not contain ':'\n")
                elif '\n' in name:
                    print("\nError: Name includes new line\n")
                elif name == '':
                    break
                elif not moudle.setting_exists_in_file(path, name):
                    print('\nSetting with this name does not exist!\n')
                else:
                    response = moudle.remove_setting_from_file(path, name)

                    if respose == 200:
                        print('\nSetting removed successfully\n')
                    elif response == 201:
                        print("\nCaution: Setting removed successfully but Setting '" + name + "' didn't exist in setting.xml file.\n"
                            "It causes no problem in removing but means that your .setting.xml was corrupted.\n")
                    break

        elif choice == '4':
            print('\nThis file contains these settings: ' + str(moudle.get_setting_names_in_file(path)))

        elif choice == '5':
            description = get_multiline_input('\nEnter any description you may have for this file')

            if description != '':
                        moudle.set_file_description(path, description)
            
            print('\nDescription changed successfully\n')

        else:
            print('\nCommand not found!\n')


def get_multiline_input(prompt):
    
    print(prompt + '\n***To end input, write nothing just press Enter (New line)***\n')

    content = ''

    while True:
        temp = input(':')

        if temp == '':
            break
        else:
            content += temp + '\n'
    
    return content[:-1]

