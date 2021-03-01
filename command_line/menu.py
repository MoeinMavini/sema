from common import moudle

def start():

    print('Welcome to sema setting maker\n')

    while True:
        choice = input("Enter '1' to edit a setting file\nEnter '2' for creating a new setting file\n"
                       "Enter 0 to exit\n\n->")

        if choice == '0' or choice == '':
            break;

        elif choice == '1':
            moudle.edit('')

        elif choice == '2':
            path = input('Enter the file name ex. commands.cfg (can include path): ')

            response = moudle.create_setting_file(path)

            if response == 200:
                print('Setting file created successfully')
                moudle.edit(path)

            elif response == 701:
                print('File already exists')
            elif response == 702:
                print('setting.xml file already exists')
            else:
                print(response)

        else:
            print('Command not found!')




