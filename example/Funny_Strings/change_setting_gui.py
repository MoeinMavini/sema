from enum import Enum
from sema.common import check, get, set
import sys
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import os

#If sema_files file is available in this directory, files written in there will be used.
#Otherwise line below will be used
dot_setting_list = []#List of .setting files associated to this program

class value_frame_scources(Enum): # Frames that value frame was initiated from
        POSSIBLE_VALUES = 0
        INSIDE_FILE = 1

class ChangeSettingMainApp:

    file_description_part_1 = 'Setting file description: '
    dot_setting_list = dot_setting_list
    approved_dot_setting_list = []
    has_dot_xml = False # If selected .setting has .setting.xml file with it
    value_frame_scource = value_frame_scources.POSSIBLE_VALUES # Frame that value frame was initiated from
    possible_values = []


    def __init__(self, master=None):

        # build ui
        self.toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)

        # main frame
        self.frame1 = ttk.Frame(self.toplevel1)
        self.file_label = ttk.Label(self.frame1)
        self.file_label.configure(text='Select the setting file')
        self.file_label.pack(padx='80', side='top')
        self.file_combobox = ttk.Combobox(self.frame1)
        self.file_combobox.configure(justify='left', state='readonly')
        self.file_combobox.pack(expand='true', fill='x', side='top')
        self.file_button = ttk.Button(self.frame1)
        self.file_button.configure(text='Accept')
        self.file_button.pack(side='top')
        self.file_button.bind('<Button-1>', lambda event: ChangeSettingMainApp.switch_to_inside_file(self))
        self.frame1.configure(height='200', width='200')
        self.frame1.pack(fill='both', side='top')
        self.toplevel1.configure(height='0', width='0')
        self.toplevel1.title('sema setting maker - change setting')
        
        # inside_file_frame
        self.inside_file_frame = ttk.Frame()
        self.back_to_main_button = ttk.Button(self.inside_file_frame)
        self.back_to_main_button.configure(text='Back')
        self.back_to_main_button.pack(anchor='w', side='top')
        self.back_to_main_button.bind('<Button-1>', lambda event: ChangeSettingMainApp.switch_to_main(self))
        self.select_setting_labelframe = ttk.Labelframe(self.inside_file_frame)
        self.select_setting_combobox = ttk.Combobox(self.select_setting_labelframe)
        self.select_setting_combobox.configure(state='readonly')
        self.select_setting_combobox.pack(fill='x', side='top')
        self.select_setting_button = ttk.Button(self.select_setting_labelframe)
        self.select_setting_button.configure(text='Accept')
        self.select_setting_button.pack(side='bottom')
        self.select_setting_button.bind('<Button-1>', lambda event: ChangeSettingMainApp.switch_to_possible_values(self))
        self.select_setting_labelframe.configure(height='200', text="Select the option you want to change it's value", width='200')
        self.select_setting_labelframe.pack(side='bottom')
        self.file_description_label = ttk.Label(self.inside_file_frame)
        self.file_description_label.configure(text=self.file_description_part_1)
        self.file_description_label.pack(padx='7', pady='12', side='left')
        self.inside_file_frame.configure(height='500', width='500')
        self.inside_file_frame.pack(side='top')
        self.inside_file_frame.pack_forget()

        # possible_values
        self.possible_values_frame = ttk.Frame()
        self.back_to_inside_file_button = ttk.Button(self.possible_values_frame)
        self.back_to_inside_file_button.configure(text='Back')
        self.back_to_inside_file_button.pack(anchor='w', side='top')
        self.back_to_inside_file_button.bind('<Button-1>', lambda event: ChangeSettingMainApp.switch_to_inside_file(self))
        self.select_value_labelframe = ttk.Labelframe(self.possible_values_frame)
        self.select_value_combobox = ttk.Combobox(self.select_value_labelframe)
        self.select_value_combobox.configure(state='readonly')
        self.select_value_combobox.pack(fill='x', side='top')
        self.select_value_button = ttk.Button(self.select_value_labelframe)
        self.select_value_button.configure(text='Accept')
        self.select_value_button.bind('<Button-1>', lambda event: ChangeSettingMainApp.select_possible_value_event(self))
        self.select_value_button.pack(side='bottom')
        self.select_value_labelframe.configure(height='200', text='Choose the new value', width='200')
        self.select_value_labelframe.pack(padx='7', pady='15', side='bottom')
        self.possible_values_frame.configure(height='500', width='500')
        self.possible_values_frame.pack(side='top')
        self.possible_values_frame.pack_forget()

        # generic_value
        self.generic_value_frame = ttk.Frame()
        self.back_from_generic_value_button = ttk.Button(self.generic_value_frame)
        self.back_from_generic_value_button.configure(text='Back')
        self.back_from_generic_value_button.pack(anchor='w', side='top')
        self.back_from_generic_value_button.bind('<Button-1>', lambda event: ChangeSettingMainApp.switch_to_before_set_value(self))
        self.separator1 = ttk.Separator(self.generic_value_frame)
        self.separator1.configure(orient='horizontal')
        self.separator1.pack(fill='x', side='top')
        self.generic_value_label = ttk.Label(self.generic_value_frame)
        self.generic_value_label.configure(text='Enter the new value:')
        self.generic_value_label.pack(padx='15', pady='8', side='top')
        self.generic_value_entery = ttk.Entry(self.generic_value_frame)
        self.generic_value_entery.pack(side='top')
        self.generic_value_submit_button = ttk.Button(self.generic_value_frame)
        self.generic_value_submit_button.configure(text='Submit')
        self.generic_value_submit_button.pack(pady='7', side='top')
        self.generic_value_submit_button.bind('<Button-1>', lambda event: ChangeSettingMainApp.submit_generic_value(self))
        self.generic_value_frame.configure(height='500', width='500')
        self.generic_value_frame.pack(side='top')
        self.generic_value_frame.pack_forget()

        # numeric_value
        self.numeric_value_frame = ttk.Frame()
        self.back_from_numeric_value_button = ttk.Button(self.numeric_value_frame)
        self.back_from_numeric_value_button.configure(text='Back')
        self.back_from_numeric_value_button.pack(anchor='w', side='top')
        self.back_from_numeric_value_button.bind('<Button-1>', lambda event: ChangeSettingMainApp.switch_to_before_set_value(self))
        self.separator2 = ttk.Separator(self.numeric_value_frame)
        self.separator2.configure(orient='horizontal')
        self.separator2.pack(fill='x', side='top')
        self.numeric_value_spinbox = ttk.Spinbox(self.numeric_value_frame)
        _text_ = '''Choose the new number'''
        self.numeric_value_spinbox.delete('0', 'end')
        self.numeric_value_spinbox.insert('0', _text_)
        self.numeric_value_spinbox.pack(padx='15', pady='8', side='top')
        self.numeric_value_submit_button = ttk.Button(self.numeric_value_frame)
        self.numeric_value_submit_button.configure(text='Submit')
        self.numeric_value_submit_button.pack(side='top')
        self.numeric_value_submit_button.bind('<Button-1>', lambda event: ChangeSettingMainApp.submit_numeric_value(self))
        self.numeric_value_frame.configure(height='500', width='500')
        self.numeric_value_frame.pack(side='top')
        self.numeric_value_frame.pack_forget()

        # Main widget
        self.mainwindow = self.toplevel1


    def run_main(self, show_error = True):
        if os.path.isfile('sema_files'):
            files = open('sema_files', 'r')

            self.dot_setting_list = []

            for line in files.readlines():
                if line.strip() != '\n' and line.strip() != '':
                    self.dot_setting_list.append(line.strip())

            files.close()

        error_list = ''

        for item in self.dot_setting_list:
            if os.path.isfile(item):
                self.approved_dot_setting_list.append(item)
            elif show_error:
                error_list += 'Caution: ' + item + ' not found!\n'

        if len(error_list) != 0 and show_error:
            tk.messagebox.showwarning(title='File not found', message=error_list)

        if len(self.approved_dot_setting_list) == 0:
            if show_error:
                tk.messagebox.showwarning(title='No Setting File Found', message='No Setting File Found!')
        else:
            self.file_combobox.configure(values=self.approved_dot_setting_list)
            self.file_combobox.current(0)
            self.mainwindow.mainloop()

    
    def switch_to_main(self):
        self.inside_file_frame.pack_forget()
        self.frame1.pack(side='top')


    def switch_to_inside_file(self):
        self.possible_values_frame.pack_forget()

        path = self.file_combobox.get()
        option_list = get.option_names_in_file(path)

        if len(option_list) == 0:
            tk.messagebox.showwarning(title='No options', message='This file has no options!')
        else:
            if os.path.isfile(path + '.xml'):
                self.has_dot_xml = True

                file_desciption  = get.file_description(path)
            
                if file_desciption != None:
                    file_desciption = self.file_description_part_1 + file_desciption
                else:
                    file_desciption = ''

                self.file_description_label.configure(text=file_desciption)

            else:
                self.file_description_label.configure(text='Caution: .setting.xml file missing, no additional data is provided for this setting!')

            self.frame1.pack_forget()
            
            for i in range(len(option_list)):
                comment = get.option_comment(path, option_list[i])

                if comment != None:
                    option_list[i] = option_list[i] + ': ' + comment

            file_desciption  = get.file_description(path)
            
            if file_desciption != None:
                file_desciption = self.file_description_part_1 + file_desciption
            else:
                file_desciption = ''

            self.select_setting_combobox.configure(values=setting_list)
            self.select_setting_combobox.current(0)
            self.inside_file_frame.pack(side='top')
    
    def switch_to_possible_values(self):
        path = self.file_combobox.get()
        option = get.option_names_in_file(path)[self.select_setting_combobox.current()]
        self.possible_values = []

        self.inside_file_frame.pack_forget()

        if self.has_dot_xml:
            i = 1
            for value in get.option_values(path, option):
                comment = get.possible_value_by_number(path, option, i-1)['comment']
                if comment == None:
                    comment = ''
                else:
                    comment = ': ' + comment

                self.possible_values.append(value + comment)
                i += 1

            self.possible_values.append('Manual Value')

            self.select_value_combobox.configure(values=self.possible_values)
            self.select_value_combobox.current(0)
            self.possible_values_frame.pack(side='top')

        else:
            self.generic_value_entery.delete(0, 'end')
            self.value_frame_scource = value_frame_scources.INSIDE_FILE
            self.generic_value_frame.pack(side='top')


    def switch_to_before_set_value(self):
        if self.value_frame_scource == value_frame_scources.INSIDE_FILE:
            self.generic_value_frame.pack_forget()
            self.switch_to_inside_file()
        else:
            self.numeric_value_frame.pack_forget()
            self.generic_value_frame.pack_forget()
            self.switch_to_possible_values()

    def submit_generic_value(self):
        value = self.generic_value_entery.get()

        check_value = check.general_value(value)

        if check_value == 700:
            tk.messagebox.showwarning(title='Bad Input', message="Value must not contain ','")
        elif check_value == 701:
            tk.messagebox.showwarning(title='Bad Input', message="Error: Value includes new line")
        elif check_value != 200:
            tk.messagebox.showwarning(title="Unspecified Error", message="Unspecified Error")
        else:
            path = self.file_combobox.get()
            option = get.option_names_in_file(path)[self.select_setting_combobox.current()]

            response = set.option_value(path, option, value)
        
            if response == 200:
                self.switch_to_before_set_value()
            elif response == 701:
                tk.messagebox.showwarning(title="Error", message="701 Error")


    def select_possible_value_event(self):
        self.possible_values_frame.pack_forget()
        
        if self.select_value_combobox.current() == len(self.possible_values) - 1:
            self.generic_value_entery.delete(0, 'end')
            self.value_frame_scource = value_frame_scources.POSSIBLE_VALUES
            self.generic_value_frame.pack(side='top')
        else:

            path = self.file_combobox.get()
            option = get.option_names_in_file(path)[self.select_setting_combobox.current()]

            value = get.possible_value_by_number(path, option, self.select_value_combobox.current())
                                                        
            if 'min' in value:# Check if value is ranged
                self.numeric_value_spinbox.delete(0, 'end')
                self.value_frame_scource = value_frame_scources.POSSIBLE_VALUES

                min = max = step = initial = 0
                style = ''

                if value['min'] == None or value['min'] == '':
                    min = -sys.maxsize
                else:
                    initial = min = float(value['min'])
                
                if value['max'] == None or value['max'] == '':
                    max = sys.maxsize
                else:
                    max = float(value['max'])

                if value['step'] == None or value['step'] == '':
                    step = 1
                else:
                    step = float(value['step'])

                style = '% ' + str(len(str(step).split('.')[1])) + 'f'

                self.numeric_value_spinbox.configure(from_=min, to=max, format=style, increment=step)
                self.numeric_value_spinbox.set(initial)
                self.numeric_value_frame.pack(side='top')

            elif 'name' in value: # Value is a single choice
                response = set.option_value(path, option, value['name'])

                if response == 200:
                    self.switch_to_before_set_value()
                elif response == 701:
                    tk.messagebox.showwarning(title="Error", message="701 Error")


    def submit_numeric_value(self):

        number = float(self.numeric_value_spinbox.get())

        path = self.file_combobox.get()
        option = get.option_names_in_file(path)[self.select_setting_combobox.current()]

        value = get.possible_value_by_number(path, option, self.select_value_combobox.current())

        diff_from_step = check.diff_to_step(value['min'], value['max'], value['step'], number)

        if value['max'] != None and value['max'] != '' and number > float(value['max']):
            tk.messagebox.showwarning(title='Out of range', message="Number is bigger than max")
        elif value['min'] != None and value['min'] != '' and number < float(value['min']):
            tk.messagebox.showwarning(title='Out of range', message="Number is less than min")
        elif value['step'] != None and value['step'] != '' and diff_from_step != 0:
            tk.messagebox.showwarning(title='Out of range', message='Number fails the step constraint by ' + str(diff_from_step))
        else:                                           
            response = set.option_value(path, option, number)

            if response == 200:
                self.switch_to_before_set_value()
            elif response == 701:
                tk.messagebox.showwarning(title="Error", message="701 Error")


if __name__ == '__main__':
    app = ChangeSettingMainApp()
    app.run_main(True)

