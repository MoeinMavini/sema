from common import module
import os

#If sema_files file is available in this directory, files written in there will be used.
#Otherwise line below will be used
dot_setting_list = []#List of .setting files associated to this program

if os.path.isfile('sema_files'):
    files = open('sema_files', 'r')

    dot_setting_list = []

    for line in files.readlines():
        if line.strip() != '\n' and line.strip() != '':
            dot_setting_list.append(line.strip())

    files.close()


print('Welcome to setting maker.')

approved_dot_setting_list = []

for item in dot_setting_list:
    if os.path.isfile(item):
        approved_dot_setting_list.append(item)
    else:
        print('\nCaution: ' + item + ' not found!')

if len(approved_dot_setting_list) == 0:
    print('\n\nNo valid file definition found. Cannot proceed!\n')
    input()
else:
    while True:
        print('\n')
        for i in range(len(approved_dot_setting_list)):
            print(str(i+1) + '. ' + approved_dot_setting_list[i])

        choice = input('\nEnter the number of file you want to edit (1 to ' + str(len(approved_dot_setting_list)) + ", 0 to exit): ").strip()

        if choice == '0' or choice == '':
            break

        elif choice.isdecimal():
            choice = int(choice)

            if choice < 1 or choice > len(approved_dot_setting_list):
                print('\nNumber is not in range!\n')
            else:
                path = approved_dot_setting_list[choice-1]

                setting_list = module.get_setting_names_in_file(path)

                if len(setting_list) == 0:
                    print('\nThis file has no setting\n')
                    continue

                has_dot_xml = True
                
                if not os.path.isfile(path + '.xml'):
                    has_dot_xml = False
                    print('\nCaution: .setting.xml file missing, no additional data is provided for this setting')

                description = module.get_file_description(path)

                if description != None:
                    print('\nSetting file description: ' +  description + '\n')

                for i in range(len(setting_list)):
                    comment = module.get_setting_comment(path, setting_list[i])

                    if comment != None:
                        comment = ': ' + comment
                    else:
                        comment = ': '

                    print(str(i+1) + '. ' + setting_list[i] + comment)

                while True:
                    choice = input("\nEnter the number of setting to change it's value (1 to " + str(len(setting_list)) + ", 0 to get back): ").strip()

                    if choice == '0' or choice == '':
                        break

                    elif choice.isdecimal():
                        choice = int(choice)

                        if choice < 1 or choice > len(setting_list):
                            print('\nNumber is not in range!\n')
                        else:
                            setting_name = setting_list[choice-1]

                            if has_dot_xml:
                                pass
                            else:
                                while True:
                                    value = input('Enter the new value: ').strip()

                                    if ':' in value:
                                        print("\nValue must not contain ':'\n")
                                    elif '\n' in value:
                                        print("\nError: Value includes new line\n")
                                    elif value == '':
                                        break
                                    else:
                                        response = module.set_setting_value(path, setting_name, value)

                                        if response == 200:
                                            print('\nValue set successfully.\n')
                                        elif response == 701:
                                            print('\n701 Error\n')
                                        break
                    else:
                        print('\nInput must be a number!\n')
        else:
            print('\nInput must be a number!\n')

