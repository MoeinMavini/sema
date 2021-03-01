def start():
    print('st')


##import os
##from tkinter import Tk
##from tkinter.filedialog import askopenfilename
##import lxml.etree as ET
##
##if not os.path.isfile('Setting_Maker.setting.xml'):
##    root = ET.Element("root")
##
##    element = ET.Element('tk')
##    element.text = '1'
##
##    root.insert(1, element)
##
##    tree = ET.ElementTree(root)
##    tree.write('Setting_Maker.setting.xml', xml_declaration=True, pretty_print=True)
##
##print('Warning: Manage_Setting.py is for developers only, don\'t distribute this to users.\n')
##
##while True:
##    choice = input("Enter '1' to edit a setting file\nEnter '2' to create a new setting file\n"
##                   "Enter '3' to add an existing setting.xml file\nEnter '4' for removing a setting file\n" + 
##                   "Enter '5' for Preferences\nEnter 0 to exit\n\n->")
##
##    if choice == '0' or choice == '':
##        break;
##
##    elif choice == '1':
##        print('Edit')
##
##    elif choice == '2':
##        print('Create')
##
##    elif choice == '3':
##
##        tree = ET.parse('Setting_Maker.setting.xml')
##        root = tree.getroot()
##
##        if root.find('tk').text == '1':
##
##            Tk().withdraw()
##            filename = askopenfilename(initialdir='.')
##            print(filename)
##
##        else:
##            print('No tk option')
##
##    elif choice == '4':
##        print('Remove')
##
##    elif choice == '5':
##        
##        while True:
##
##            tree = ET.parse('Setting_Maker.setting.xml')
##            root = tree.getroot()
##
##            tk_option = 'enabled'
##
##            if root.find('tk').text == '0':
##                tk_option = 'disabled'
##            
##            print('\nTkinter usage is ' + tk_option)
##
##            choice = input("\nEnter '1' to disable\\enable tkinter usage\nEnter 0 to get back to main menu\n\n->")
##
##            
##            if choice == '0' or choice == '':
##                break;
##
##            elif choice == '1':
##
##                tree = ET.parse('Setting_Maker.setting.xml')
##                root = tree.getroot()
##
##                if root.find('tk').text == '0':
##                    root.find('tk').text = '1'
##                else:
##                    root.find('tk').text = '0'
##
##                tree.write('Setting_Maker.setting.xml', xml_declaration=True, pretty_print=True)
##
##            else:
##                print('Command not found!')
##
##    else:
##        print('Command not found!')

