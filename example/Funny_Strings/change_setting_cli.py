from sema.common import check, get, set
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

                option_list = get.option_names_in_file(path)

                if len(option_list) == 0:
                    print('\nThis file has no options\n')
                    continue

                has_dot_xml = True
                
                if not os.path.isfile(path + '.xml'):
                    has_dot_xml = False
                    print('\nCaution: .setting.xml file missing, no additional data is provided for this setting')

                description = get.file_description(path)

                if description != None:
                    print('\nSetting file description: ' +  description + '\n')

                for i in range(len(option_list)):
                    comment = get.option_comment(path, option_list[i])

                    if comment != None:
                        comment = ': ' + comment
                    else:
                        comment = ': '

                    print(str(i+1) + '. ' + option_list[i] + comment)

                while True:
                    choice = input("\nEnter the number of option to change it's value (1 to " + str(len(option_list)) + ", 0 to get back): ").strip()

                    if choice == '0' or choice == '':
                        break

                    elif choice.isdecimal():
                        choice = int(choice)

                        if choice < 1 or choice > len(option_list):
                            print('\nNumber is not in range!\n')
                        else:
                            option_name = option_list[choice-1]

                            if has_dot_xml:

                                print('\nPossible values are: ', end ="" )
                                i = 1
                                for value in get.option_values(path, option_name):
                                    comment = get.possible_value_by_number(path, option_name, i-1)['comment']
                                    if comment == None:
                                        comment = ''
                                    else:
                                        comment = ': ' + comment

                                    print(str(i) + '. ' + value + comment, end =", " )
                                    i += 1

                                print(str(i) + '.Manual value')

                                number_of_values = len(get.option_values(path, option_name))

                                while True:
                                    choice = input('\nEnter the number of value you want to set (1 to ' + str( number_of_values + 1) + ', 0 to get back): ').strip()

                                    if choice == '0' or choice == '':
                                        break
                                    elif not choice.isdecimal():
                                        print('\nInput must be a number\n')
                                    elif int(choice) < 1 or int(choice) > number_of_values + 1:
                                        print('\nNumber is not in range\n')
                                    else:
                                        choice = int(choice)

                                        if choice == number_of_values + 1: # Manual Value Chosen
                                            while True:
                                                value = input('Enter the new value: ').strip()

                                                check_value = check.general_value(value)

                                                if check_value == 700:
                                                    print("\nValue must not contain ','\n")
                                                elif check_value == 701:
                                                    print("\nError: Value includes new line\n")
                                                elif check_value != 200:
                                                    print("\nUnspecified Error\n")
                                                elif value == '':
                                                    break
                                                else:
                                                    response = set.option_value(path, option_name, value)

                                                    if response == 200:
                                                        print('\nValue set successfully.\n')
                                                    elif response == 701:
                                                        print('\n701 Error\n')
                                                    break
                                        else:
                                            value = get.possible_value_by_number(path, option_name, choice-1)
                                                        
                                            if 'min' in value:#Check if value is ranged
                                                while True:
                                                    number = input('Enter the number: ').strip()

                                                    if number == '':
                                                        break

                                                    try:
                                                        number = float(number)
                                                    except:
                                                        print('\n' + number + ' is not a number!\n')
                                                        continue

                                                    diff_from_step = check.diff_to_step(value['min'], value['max'], value['step'], number)

                                                    if value['max'] != None and value['max'] != '':
                                                        if number > float(value['max']):
                                                            print('\nNumber is bigger than max\n')
                                                            continue
                                                    if value['min'] != None and value['min'] != '':
                                                        if number < float(value['min']):
                                                            print('\nNumber is less than min\n')
                                                            continue
                                                    if value['step'] != None and value['step'] != '':
                                                        if diff_from_step != 0:
                                                            print('\nNumber fails the step constraint by ' + str(diff_from_step) + '\n')
                                                            continue
                                                    
                                                    response = set.option_value(path, option_name, number)

                                                    if response == 200:
                                                        print('\nNumber set successfully.\n')
                                                    elif response == 701:
                                                        print('\n701 Error\n')
                                                    break
                                                              
                                            elif 'name' in value:
                                                response = set.option_value(path, option_name, value['name'])

                                                if response == 200:
                                                    print('\nValue set successfully.\n')
                                                elif response == 701:
                                                    print('\n701 Error\n')
                                                break

                            else:
                                while True:
                                    value = input('Enter the new value: ').strip()

                                    check_value = check.general_value(value)

                                    if check_value == 700:
                                        print("\nValue must not contain ','\n")
                                    elif check_value == 701:
                                        print("\nError: Value includes new line\n")
                                    elif check_value != 200:
                                        print("\nUnspecified Error\n")
                                    elif value == '':
                                        break
                                    else:
                                        response = set.option_value(path, option_name, value)

                                        if response == 200:
                                            print('\nValue set successfully.\n')
                                        elif response == 701:
                                            print('\n701 Error\n')
                                        break
                    else:
                        print('\nInput must be a number!\n')
        else:
            print('\nInput must be a number!\n')

