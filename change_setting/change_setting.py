import os

#If sema_files.setting file is available in this directory, files written in there will be used.
#Otherwise line below will be used
dot_setting_list = []#List of .setting file associated to this program

if os.path.isfile('sema_files.setting'):
    files = open('sema_files.setting', 'r')

    dot_setting_list = []

    for line in files.readlines():
        if line.strip() != '\n' and line.strip() == '':
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
    print('\n\nNo valid file definition found. Cannot proceed\n')
else:
    while True:
        choice = input('\nEnter the number of file you want to edit (1 to ' + str(len(approved_dot_setting_list)) + '): ').strip()

        if choice.isdecimal():
            choice = int(choice)

            if choice < 1 or choice > len(approved_dot_setting_list):
                print('\nNumber is not in range\n')
            else:
                pass
        else:
            print('\nInput must be a number\n')

