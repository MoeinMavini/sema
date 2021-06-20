from sema.common import check, get, cli, set
from sema.manage_setting import common

def start():

    print('\nWelcome to sema setting maker. This is the developer tool to make settings and edit created settings.\n')

    while True:
        choice = input("Enter '1' to edit a setting file\nEnter '2' to create a new setting file\n"
                       "Enter 0 to exit\n\n->").strip()

        if choice == '0' or choice == '':
            break;

        elif choice == '1':
            path = input('Enter the name of setting file you want to edit (can include path): ').strip()

            if path != '':
                result = check.file_exists(path)

                if result == 700:
                    print('\nChosen file is not a setting maker file\nFile must have .setting extension with a .setting.xml file in the same directory\n')
                elif result == 701:
                    print('\n.setting file missing! Both .setting and .setting.xml are required\n')
                elif result == 702:
                    print('\n.setting.xml file missing! Both .setting and .setting.xml are required\n')
                else:
                    edit(result)

        elif choice == '2':
            path = input('Enter the file name (can include path): ').strip()

            if path != '':
                response = common.create_setting_file(path)

                if response == 200:

                    description = cli.get_multiline_input('\nEnter any description you may have for this file')

                    if description != '':
                        set.file_description(path + '.setting', description)

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

    print('\nThis file contains these options: ' + str(get.option_names_in_file(path)))

    while True:
        choice = input("\nEnter '1' to edit a option\nEnter '2' to add a new option\n"
                        "Enter '3' to remove a option\nEnter '4' to see the list of options in current file\n"
                        "Enter '5' to set description for this file\nEnter 0 to get back\n\n->").strip()

        if choice == '0' or choice == '':
            break;

        elif choice == '1':
            while True:
                name = input('Enter the option name: ').strip()

                name_check = check.option_name(name)

                if name_check == 701:
                    print("\nName must not contain ':'\n")
                elif name_check == 702:
                    print("\nName must not contain ','\n")
                elif name_check == 700:
                    break
                elif name_check == 703:
                    print("\nName cannot start with '#'\n")
                elif name_check == 704:
                    print("\nError: Name includes new line\n")
                elif name_check != 200:
                    print("\nUnspecified Error\n")
                elif not check.option_exists_in_file(path, name):
                    print('\nOption not found!\n')
                else:
                    while True:
                        choice = input("\nEnter '1' to change option name\nEnter '2' to change default value\n"
                        "Enter '3' to change comment\nEnter '4' to manage possible values for this option\n"
                        "Enter 0 to get back\n\n->").strip()

                        if choice == '0' or choice == '':
                            break;

                        elif choice == '1':
                            while True:
                                new_name = input('Enter new option name: ').strip()

                                name_check = check.option_name(new_name)

                                if name_check == 701:
                                    print("\nName must not contain ':'\n")
                                elif name_check == 702:
                                    print("\nName must not contain ','\n")
                                elif name_check == 703:
                                    print("\nName cannot start with '#'\n")
                                elif name_check == 704:
                                    print("\nError: Name includes new line\n")
                                elif name_check == 700:
                                    break
                                elif name_check != 200:
                                    print("\nUnspecified Error\n")
                                elif check.option_exists_in_file(path, new_name):
                                    print('\nThis option name already exists!\n')
                                else:
                                    response = common.change_option_name(path, name, new_name)

                                    if response == 200:
                                        print('\nName changed successfully.\n')
                                    elif response == 201:
                                        print('\nName changed successfully.\nCaution: Option name was not found in .setting.xml file, file could be corrupted\n')
                                    break

                        elif choice == '2':
                            while True:
                                value = input('Enter default value: ').strip()

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
                                    response = set.default(path, name, value)

                                    if response == 200:
                                        print('\nDefault value set successfully.\n')
                                    elif response == 201:
                                        print('\nDefault value set successfully.\nCaution: Option name was not found in .setting.xml file, file could be corrupted\n')
                                    break

                        elif choice == '3':
                            while True:
                                comment = input('Enter the comment: ').strip()

                                if '\n' in comment:
                                    print("\nError: Comment includes new line\n")
                                elif comment == '':
                                    break
                                else:
                                    response = set.option_comment(path, name, comment)

                                    if response == 200:
                                        print('\nComment set successfully.\n')
                                    elif response == 201:
                                        print('\nComment set successfully.\nCaution: Option name was not found in .setting.xml file, file could be corrupted\n')

                                    break

                        elif choice == '4':
                            show_option_values(path, name)

                            while True:
                                choice = input("\nEnter '1' to add a value\nEnter '2' to edit a value\n"
                                "Enter '3' to remove a value\nEnter '4' to see a list of current values\n"
                                "Enter 0 to get back\n\n->").strip()

                                if choice == '0' or choice == '':
                                    break;

                                elif choice == '1':
                                    while True:
                                        choice = input("\nEnter '1' for simple value\nEnter '2' for number range value\n"
                                        "Enter 0 to get back\n\n->")

                                        if choice == '0' or choice == '':
                                            break;

                                        elif choice == '1':
                                            while True:
                                                value = input('Enter the value: ').strip()

                                                check_value = check.general_value(value)

                                                if check_value == 700:
                                                    print("\nValue must not contain ','\n")
                                                elif check_value == 701:
                                                    print("\nError: Value includes new line\n")
                                                elif check_value != 200:
                                                    print("\nUnspecified Error\n")
                                                elif value == '':
                                                    break
                                                elif check.option_simple_value_exists(path, name, value):
                                                    print('\nThis value already exists!\n')
                                                else:
                                                    while True:
                                                        comment = input('Enter the single line comment for option: ').strip()

                                                        if '\n' in comment:
                                                            print("\nError: Comment includes new line\n")
                                                        else:
                                                            response = common.add_simple_value(path, name, value, comment)

                                                            if response == 200:
                                                                print('\nValue added successfully\n')
                                                            else:
                                                                print('\nSome error occured\n')
                                                            break
                                                    break

                                        elif choice == '2':
                                            while True:
                                                min = input('Enter the minimum (Enter nothing to skip): ').strip()

                                                if min == '':
                                                    break

                                                try:
                                                    float(min)
                                                    break
                                                except:
                                                    print('\n' + min + ' is not a number!\n')
                                                
                                            while True:
                                                max = input('Enter the maximum (Enter nothing to skip): ').strip()

                                                if max == '':
                                                    break

                                                try:
                                                    float(max)
                                                    break
                                                except:
                                                    print('\n' + max + ' is not a number!\n')
                                                
                                            while True:
                                                step = input('Enter the step (Enter nothing to skip): ').strip()

                                                if step == '':
                                                    break

                                                try:
                                                    float(step)
                                                    break
                                                except:
                                                    print('\n' + step + ' is not a number!\n')

                                            if min == max == step == '':
                                                continue

                                            elif check.option_renage_value_exists(path, name, min, max, step):
                                                    print('\nThis range is already added!\n')
                                            else:
                                                while True:
                                                    comment = input('Enter the single line comment for option: ').strip()

                                                    if '\n' in comment:
                                                        print("\nError: Comment includes new line\n")
                                                    else:
                                                        response = common.add_range_value(path, name, min, max, step, comment)

                                                        if response == 200:
                                                            print('\nRange added successfully\n')
                                                        else:
                                                            print('\nSome error occured\n')
                                                        break

                                        else:
                                            print('\nCommand not found!\n')

                                elif choice == '2':
                                    number_of_values = len(get.option_values(path, name))

                                    if number_of_values == 0:
                                        print('\nOption has no values\n')
                                    else:
                                        choice = input('\nEnter the number of value you want to edit (1 to ' + str(number_of_values) + '): ').strip()

                                        if choice.isdecimal():
                                            choice = int(choice)

                                            if choice < 1 or choice > number_of_values:
                                                print('\nNumber is not in range\n')
                                            else:
                                                while True:
                                                    action = input("\nEnter '1' set comment\nEnter '2' edit value\n"
                                                    "Enter 0 to get back\n\n->")

                                                    if action == '0' or action == '':
                                                        break;

                                                    elif action == '1':
                                                        while True:
                                                            comment = input('Enter the single line comment for option: ').strip()

                                                            if '\n' in comment:
                                                                print("\nError: Comment includes new line\n")
                                                            else:
                                                                response = common.set_value_comment_by_number(path, name, choice-1, comment)

                                                                if response == 200:
                                                                    print('\nCommented is set\n')
                                                                else:
                                                                    print('\nSome error occured\n')
                                                                break

                                                    elif action == '2':
                                                        value = get.possible_value_by_number(path, name, choice-1)
                                                        
                                                        if 'min' in value:#Check if value is ranged
                                                            while True:
                                                                action = input("\nEnter '1' to set min\nEnter '2' to set max\nEnter '3' to set step\n"
                                                                "Enter 0 to get back\n\n->").strip()

                                                                if action == '0' or action == '':
                                                                    break;

                                                                elif action == '1':
                                                                    while True:
                                                                        min = input('Enter the min (Enter nothing for empty): ').strip()

                                                                        if min != '':
                                                                            try:
                                                                                float(min)
                                                                            except:
                                                                                print('\n' + min + ' is not a number!\n')
                                                                                continue

                                                                        if min == value['max'] == value['step'] == '':
                                                                            print('\nCannot have min, max and step empty\n')

                                                                        elif check.option_renage_value_exists(path, name, min, value['max'], value['step']):
                                                                                print('\nThis range is already added!\n')
                                                                        else:
                                                                            response = common.set_ranged_possible_value_by_number(path, name, choice-1, min, value['max'], value['step'])

                                                                            if response == 200:
                                                                                print('\nValue is set\n')
                                                                            else:
                                                                                print('\nSome error occured\n')
                                                                            break
                                                                    break
                                                                elif action == '2':
                                                                    while True:
                                                                        max = input('Enter the max (Enter nothing for empty): ').strip()

                                                                        if max != '':
                                                                            try:
                                                                                float(max)
                                                                            except:
                                                                                print('\n' + max + ' is not a number!\n')
                                                                                continue

                                                                        if value['min'] == max == value['step'] == '':
                                                                            print('\nCannot have min, max and step empty\n')

                                                                        elif check.option_renage_value_exists(path, name, value['min'], max, value['step']):
                                                                                print('\nThis range is already added!\n')
                                                                        else:
                                                                            response = common.set_ranged_possible_value_by_number(path, name, choice-1, value['min'], max, value['step'])

                                                                            if response == 200:
                                                                                print('\nValue is set\n')
                                                                            else:
                                                                                print('\nSome error occured\n')
                                                                            break
                                                                    break
                                                                elif action == '3':
                                                                    while True:
                                                                        step = input('Enter the step (Enter nothing for empty): ').strip()

                                                                        if step != '':
                                                                            try:
                                                                                float(step)
                                                                            except:
                                                                                print('\n' + step + ' is not a number!\n')
                                                                                continue

                                                                        if value['min'] == value['max'] == step == '':
                                                                            print('\nCannot have min, max and step empty\n')

                                                                        elif check.option_renage_value_exists(path, name, value['min'], value['max'], step):
                                                                                print('\nThis range is already added!\n')
                                                                        else:
                                                                            response = common.set_ranged_possible_value_by_number(path, name, choice-1, value['min'], value['max'], step)

                                                                            if response == 200:
                                                                                print('\nValue is set\n')
                                                                            else:
                                                                                print('\nSome error occured\n')
                                                                            break
                                                                    break
                                                                else:
                                                                    print('\nCommand not found!\n')

                                                        elif 'name' in value:
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
                                                                elif check.option_simple_value_exists(path, name, value):
                                                                    print('\nThis value already exists!\n')
                                                                else:
                                                                    response = common.set_simple_possible_value_by_number(path, name, choice-1, value)

                                                                    if response == 200:
                                                                        print('\nName has changed\n')
                                                                    else:
                                                                        print('\nSome error occured\n')
                                                                    break
                                                            break
                                                    else:
                                                        print('\nCommand not found!\n')

                                        else:
                                            print('\nInput must be a number\n')

                                elif choice == '3':

                                    number_of_values = len(get.option_values(path, name))

                                    if number_of_values == 0:
                                        print('\nOption has no values\n')
                                    else:
                                        choice = input('\nEnter the number of value you want to be removed (1 to ' + str(number_of_values) + '): ').strip()

                                        if choice.isdecimal():
                                            choice = int(choice)

                                            if choice < 1 or choice > number_of_values:
                                                print('\nNumber is not in range\n')
                                            else:
                                                common.remove_possible_value_by_number(path, name, choice-1)
                                                print('\nValue removed successfully\n')

                                        else:
                                            print('\nInput must be a number\n')

                                elif choice == '4':
                                    show_option_values(path, name)

                                else:
                                    print('\nCommand not found!\n')
                        else:
                                print('\nCommand not found!\n')

                    break


        elif choice == '2':
            while True:
                name = input('Enter the option name: ').strip()

                name_check = check.option_name(name)

                if name_check == 701:
                    print("\nName must not contain ':'\n")
                elif name_check == 702:
                    print("\nName must not contain ','\n")
                elif name_check == 700:
                    break
                elif name_check == 703:
                    print("\nName cannot start with '#'\n")
                elif name_check == 704:
                    print("\nError: Name includes new line\n")
                elif name_check != 200:
                    print("\nUnspecified Error\n")
                elif check.option_exists_in_file(path, name):
                    print('\nThis option name already exists!\n')
                else:
                    while True:
                        comment = input('Enter the single line comment for option: ').strip()

                        if '\n' in comment:
                            print("\nError: Comment includes new line\n")
                        else:
                            response = common.add_option_to_file(path, name, comment)

                            if response == 200:
                                print('\nOption created successfully\n')
                            elif response == 201:
                                print('\nCaution: Option created successfully! Definition for option ' + name + ' already exists in setting.xml file\n')
                            break
                break

        elif choice == '3':
            while True:
                name = input('Enter the option name: ').strip()

                name_check = check.option_name(name)

                if name_check == 701:
                    print("\nName must not contain ':'\n")
                elif name_check == 702:
                    print("\nName must not contain ','\n")
                elif name_check == 700:
                    break
                elif name_check == 703:
                    print("\nName cannot start with '#'\n")
                elif name_check == 704:
                    print("\nError: Name includes new line\n")
                elif name_check != 200:
                    print("\nUnspecified Error\n")
                elif not check.option_exists_in_file(path, name):
                    print('\nOption with this name does not exist!\n')
                else:
                    response = common.remove_option_from_file(path, name)

                    if response == 200:
                        print('\nOption removed successfully\n')
                    elif response == 201:
                        print("\nCaution: Option removed successfully but Option '" + name + "' didn't exist in setting.xml file.\n"
                            "It causes no problem in removing but means that your .setting.xml was corrupted.\n")
                    break

        elif choice == '4':
            print('\nThis file contains these options: ' + str(get.option_names_in_file(path)))

        elif choice == '5':
            description = cli.get_multiline_input('\nEnter any description you may have for this file')

            if description != '':
                set.file_description(path, description)
            
            print('\nDescription changed successfully\n')

        else:
            print('\nCommand not found!\n')


def show_option_values(path_to_dot_setting, option_name):
    print('\nCurrent values are: ', end ="" )
    i = 1
    for value in get.option_values(path_to_dot_setting, option_name):
        print(str(i) + '.' + value, end =", " )
        i += 1

    print('\n')


if __name__ == "__main__":
    start()

