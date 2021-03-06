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
                moudle.edit(path)

        elif choice == '2':
            path = input('Enter the file name (can include path): ').strip()

            if path != '':
                response = moudle.create_setting_file(path)

                if response == 200:
                    print('\nSetting file created successfully')
                    moudle.edit(path)

                elif response == 701:
                    print('\nFile already exists\n')
                elif response == 702:
                    print('\nsetting.xml file already exists\n')
                else:
                    print(response)

        else:
            print('\nCommand not found!\n')

