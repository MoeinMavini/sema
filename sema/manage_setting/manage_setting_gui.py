import re
import sys
from sema.common import check, get, set
from sema.manage_setting import common
import tkinter as tk
import tkinter.filedialog
from tkinter import messagebox
import tkinter.ttk as ttk
import os

class ManageSettingMainApp:

    current_path = '' # Path of .setting file we are working on
    current_option_name = '' # Sets to the option name when frame is first seen
    is_value_new = True # Frame for edit value and new value are the same this flag distinguishes them

    def __init__(self, master=None):

        # build ui
        self.toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)

        # main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame_label = ttk.Label(self.main_frame)
        self.main_frame_label.configure(text='''Welcome to sema setting maker,
This is the developer tool to make settings and edit created settings.\n
Use buttons below to create or open a setting maker setting.''')
        self.main_frame_label.pack(padx='10', pady='10', side='top')
        self.new_file_button = ttk.Button(self.main_frame)
        self.new_file_button.configure(text='New')
        self.new_file_button.pack(padx='10', pady='5', side='left')
        self.new_file_button.bind('<Button-1>', lambda event: ManageSettingMainApp.new_file_event(self))
        self.open_file_button = ttk.Button(self.main_frame)
        self.open_file_button.configure(text='Open')
        self.open_file_button.pack(pady='5', side='left')
        self.open_file_button.bind('<Button-1>', lambda event: ManageSettingMainApp.open_file_event(self))
        self.main_frame.configure(height='200', width='200')
        self.main_frame.pack(side='top')
        self.toplevel1.title('sema setting maker - manage setting')

        # create file
        self.new_file_frame = ttk.Frame()
        self.new_file_back = ttk.Button(self.new_file_frame)
        self.new_file_back.configure(text='Back')
        self.new_file_back.bind('<Button-1>', lambda event: ManageSettingMainApp.switch_to_main(self))
        self.new_file_back.pack(anchor='w', side='top')
        self.new_file_frame_label = ttk.Label(self.new_file_frame)
        self.new_file_frame_label.configure(text='Enter any description you may have for this file:')
        self.new_file_frame_label.pack(anchor='w', padx='10', pady='10', side='top')
        self.new_file_text = tk.Text(self.new_file_frame)
        self.new_file_text.configure(height='10', width='50')
        self.new_file_text.pack(padx='10', pady='5', side='top')
        self.new_file_create_button = ttk.Button(self.new_file_frame)
        self.new_file_create_button.configure(text='Next')
        self.new_file_create_button.pack(side='bottom')
        self.new_file_create_button.bind('<Button-1>', lambda event: ManageSettingMainApp.create_new_file(self))
        self.new_file_frame.configure(height='200', width='200')
        self.new_file_frame.pack_forget()

        # edit file
        self.edit_file_frame = ttk.Frame()
        self.edit_file_back = ttk.Button(self.edit_file_frame)
        self.edit_file_back.configure(text='Back')
        self.edit_file_back.pack(anchor='w', side='top')
        self.edit_file_back.bind('<Button-1>', lambda event: ManageSettingMainApp.switch_to_main(self))
        self.edit_file_sub_frame = ttk.Frame(self.edit_file_frame)
        self.edit_file_label = ttk.Label(self.edit_file_sub_frame)
        self.edit_file_label.configure(text='Options: ')
        self.edit_file_label.pack(anchor='w', side='left')
        self.edit_file_list_combobox = ttk.Combobox(self.edit_file_sub_frame)
        self.edit_file_list_combobox.configure(state='readonly')
        self.edit_file_list_combobox.pack(side='left')
        self.edit_file_edit_button = ttk.Button(self.edit_file_sub_frame)
        self.edit_file_edit_button.configure(text='Edit')
        self.edit_file_edit_button.pack(padx='10', side='left')
        self.edit_file_edit_button.bind('<Button-1>', lambda event: ManageSettingMainApp.switch_to_edit_option(self))
        self.edit_file_remove_button = ttk.Button(self.edit_file_sub_frame)
        self.edit_file_remove_button.configure(text='Remove')
        self.edit_file_remove_button.pack(side='left')
        self.edit_file_remove_button.bind('<Button-1>', lambda event: ManageSettingMainApp.on_option_remove_event(self))
        self.edit_file_sub_frame.configure(height='200', width='200')
        self.edit_file_sub_frame.pack(padx='10', pady='10', side='top')
        self.edit_file_separator = ttk.Separator(self.edit_file_frame)
        self.edit_file_separator.configure(orient='horizontal')
        self.edit_file_separator.pack(expand='true', fill='x', padx='3', side='top')
        self.edit_file_new_button = ttk.Button(self.edit_file_frame)
        self.edit_file_new_button.configure(text='Add Option')
        self.edit_file_new_button.pack(padx='10', pady='5', side='left')
        self.edit_file_new_button.bind('<Button-1>', lambda event: ManageSettingMainApp.switch_to_new_option(self))
        self.edit_file_description_button = ttk.Button(self.edit_file_frame)
        self.edit_file_description_button.configure(text='Edit File Description')
        self.edit_file_description_button.pack(side='left')
        self.edit_file_description_button.bind('<Button-1>', lambda event: ManageSettingMainApp.switch_to_file_description(self))
        self.edit_file_frame.configure(height='200', width='200')
        self.edit_file_frame.pack_forget()

        # edit option
        self.edit_option_frame = ttk.Frame()
        self.edit_option_back = ttk.Button(self.edit_option_frame)
        self.edit_option_back.configure(text='Back')
        self.edit_option_back.pack(anchor='w', side='top')
        self.edit_option_back.bind('<Button-1>', lambda event: ManageSettingMainApp.switch_to_edit_file(self))
        self.edit_option_sparator_1 = ttk.Separator(self.edit_option_frame)
        self.edit_option_sparator_1.configure(orient='horizontal')
        self.edit_option_sparator_1.pack(fill='x', pady='10 0', side='top')
        self.edit_option_name_frame = ttk.Frame(self.edit_option_frame)
        self.edit_option_name_label = ttk.Label(self.edit_option_name_frame)
        self.edit_option_name_label.configure(text='Name: ')
        self.edit_option_name_label.pack(side='left')
        self.edit_option_name_entry = ttk.Entry(self.edit_option_name_frame)
        self.edit_option_name_entry.pack(expand='true', fill='x', side='left')
        self.edit_option_name_frame.configure(height='200', width='200')
        self.edit_option_name_frame.pack(anchor='w', padx='10', pady='10 0', side='top')
        self.edit_option_default_value_frame = ttk.Frame(self.edit_option_frame)
        self.edit_option_default_value_label = ttk.Label(self.edit_option_default_value_frame)
        self.edit_option_default_value_label.configure(text='Default Value: ')
        self.edit_option_default_value_label.pack(anchor='w', side='left')
        self.edit_option_default_value_entry = ttk.Entry(self.edit_option_default_value_frame)
        self.edit_option_default_value_entry.pack(expand='true', fill='x', side='left')
        self.edit_option_default_value_frame.configure(height='200', width='200')
        self.edit_option_default_value_frame.pack(anchor='w', padx='10', pady='10 0', side='top')
        self.edit_option_comment_frame = ttk.Frame(self.edit_option_frame)
        self.edit_option_comment_label = ttk.Label(self.edit_option_comment_frame)
        self.edit_option_comment_label.configure(text='Comment: ')
        self.edit_option_comment_label.pack(anchor='w', side='left')
        self.edit_option_comment_entry = ttk.Entry(self.edit_option_comment_frame)
        self.edit_option_comment_entry.configure(width='50')
        self.edit_option_comment_entry.pack(expand='true', fill='x', side='left')
        self.edit_option_comment_frame.configure(height='200', width='200')
        self.edit_option_comment_frame.pack(anchor='w', padx='10', pady='10 0', side='top')
        self.edit_option_save_button = ttk.Button(self.edit_option_frame)
        self.edit_option_save_button.configure(text='Save')
        self.edit_option_save_button.pack(pady='10 0', side='top')
        self.edit_option_save_button.bind('<Button-1>', lambda event: ManageSettingMainApp.edit_option_save_event(self))
        self.edit_option_sparator_2 = ttk.Separator(self.edit_option_frame)
        self.edit_option_sparator_2.configure(orient='horizontal')
        self.edit_option_sparator_2.pack(fill='x', pady='10 0', side='top')
        self.edit_option_possible_values_button = ttk.Button(self.edit_option_frame)
        self.edit_option_possible_values_button.configure(text='Manage Possible Values')
        self.edit_option_possible_values_button.pack(pady='10', side='top')
        self.edit_option_possible_values_button.bind('<Button-1>', lambda event: ManageSettingMainApp.switch_to_option_values(self))
        self.edit_option_frame.configure(height='200', width='200')
        self.edit_option_frame.pack_forget()

        # new option
        self.new_option_frame = ttk.Frame()
        self.new_option_back = ttk.Button(self.new_option_frame)
        self.new_option_back.configure(text='Back')
        self.new_option_back.pack(anchor='w', side='top')
        self.new_option_back.bind('<Button-1>', lambda event: ManageSettingMainApp.switch_to_edit_file(self))
        self.new_option_sparator_1 = ttk.Separator(self.new_option_frame)
        self.new_option_sparator_1.configure(orient='horizontal')
        self.new_option_sparator_1.pack(fill='x', pady='10 0', side='top')
        self.new_option_name_frame = ttk.Frame(self.new_option_frame)
        self.new_option_name_label = ttk.Label(self.new_option_name_frame)
        self.new_option_name_label.configure(text='Name:(*) ')
        self.new_option_name_label.pack(side='left')
        self.new_option_name_entry = ttk.Entry(self.new_option_name_frame)
        self.new_option_name_entry.pack(expand='true', fill='x', side='left')
        self.new_option_name_frame.configure(height='200', width='200')
        self.new_option_name_frame.pack(anchor='w', padx='10', pady='10 0', side='top')
        self.new_option_default_value_frame = ttk.Frame(self.new_option_frame)
        self.new_option_default_value_label = ttk.Label(self.new_option_default_value_frame)
        self.new_option_default_value_label.configure(text='Default Value: ')
        self.new_option_default_value_label.pack(anchor='w', side='left')
        self.new_option_default_value_entry = ttk.Entry(self.new_option_default_value_frame)
        self.new_option_default_value_entry.pack(expand='true', fill='x', side='left')
        self.new_option_default_value_frame.configure(height='200', width='200')
        self.new_option_default_value_frame.pack(anchor='w', padx='10', pady='10 0', side='top')
        self.new_option_comment_frame = ttk.Frame(self.new_option_frame)
        self.new_option_comment_label = ttk.Label(self.new_option_comment_frame)
        self.new_option_comment_label.configure(text='Comment: ')
        self.new_option_comment_label.pack(anchor='w', side='left')
        self.new_option_comment_entry = ttk.Entry(self.new_option_comment_frame)
        self.new_option_comment_entry.configure(width='50')
        self.new_option_comment_entry.pack(expand='true', fill='x', side='left')
        self.new_option_comment_frame.configure(height='200', width='200')
        self.new_option_comment_frame.pack(anchor='w', padx='10', pady='10 0', side='top')
        self.new_option_save_button = ttk.Button(self.new_option_frame)
        self.new_option_save_button.configure(text='Create')
        self.new_option_save_button.pack(pady='10 5', side='top')
        self.new_option_save_button.bind('<Button-1>', lambda event: ManageSettingMainApp.new_option_save_event(self))
        self.new_option_frame.configure(height='200', width='200')
        self.new_option_frame.pack_forget()

        # option value
        self.option_values_frame = ttk.Frame()
        self.option_values_back = ttk.Button(self.option_values_frame)
        self.option_values_back.configure(text='Back')
        self.option_values_back.pack(anchor='w', side='top')
        self.option_values_back.bind('<Button-1>', lambda event: ManageSettingMainApp.switch_to_edit_option(self))
        self.option_values_sub_frame = ttk.Frame(self.option_values_frame)
        self.option_values_label = ttk.Label(self.option_values_sub_frame)
        self.option_values_label.configure(text='Values: ')
        self.option_values_label.pack(anchor='w', side='left')
        self.option_values_list_combobox = ttk.Combobox(self.option_values_sub_frame)
        self.option_values_list_combobox.configure(state='readonly')
        self.option_values_list_combobox.pack(side='left')
        self.option_values_edit_button = ttk.Button(self.option_values_sub_frame)
        self.option_values_edit_button.configure(text='Edit')
        self.option_values_edit_button.pack(padx='10', side='left')
        self.option_values_edit_button.bind('<Button-1>', lambda event: ManageSettingMainApp.on_value_edit_event(self))
        self.option_values_remove_button = ttk.Button(self.option_values_sub_frame)
        self.option_values_remove_button.configure(text='Remove')
        self.option_values_remove_button.pack(side='left')
        self.option_values_remove_button.bind('<Button-1>', lambda event: ManageSettingMainApp.on_value_remove_event(self))
        self.option_values_sub_frame.configure(height='200', width='200')
        self.option_values_sub_frame.pack(padx='10', pady='10', side='top')
        self.option_values_separator = ttk.Separator(self.option_values_frame)
        self.option_values_separator.configure(orient='horizontal')
        self.option_values_separator.pack(expand='true', fill='x', padx='3', side='top')
        self.option_values_add_simple_button = ttk.Button(self.option_values_frame)
        self.option_values_add_simple_button.configure(text='Add Simple Value')
        self.option_values_add_simple_button.pack(anchor='w', padx='10', pady='5', side='left')
        self.option_values_add_simple_button.bind('<Button-1>', lambda event: ManageSettingMainApp.switch_to_simple_values(self))
        self.option_values_add_ranged_button = ttk.Button(self.option_values_frame)
        self.option_values_add_ranged_button.configure(text='Add Ranged Value')
        self.option_values_add_ranged_button.pack(anchor='w', side='left')
        self.option_values_add_ranged_button.bind('<Button-1>', lambda event: ManageSettingMainApp.switch_to_ranged_values(self))
        self.option_values_frame.configure(height='200', width='200')
        self.option_values_frame.pack_forget()

        # simple value
        self.simple_value_frame = ttk.Frame()
        self.simple_value_back = ttk.Button(self.simple_value_frame)
        self.simple_value_back.configure(text='Back')
        self.simple_value_back.pack(anchor='w', side='top')
        self.simple_value_back.bind('<Button-1>', lambda event: ManageSettingMainApp.switch_to_option_values(self))
        self.simple_value_sparator = ttk.Separator(self.simple_value_frame)
        self.simple_value_sparator.configure(orient='horizontal')
        self.simple_value_sparator.pack(expand='true', fill='x', pady='5 0', side='top')
        self.simple_value_value_frame = ttk.Frame(self.simple_value_frame)
        self.simple_value_value_label = ttk.Label(self.simple_value_value_frame)
        self.simple_value_value_label.configure(text='Value: ')
        self.simple_value_value_label.pack(side='left')
        self.simple_value_value_entry = ttk.Entry(self.simple_value_value_frame)
        self.simple_value_value_entry.pack(expand='true', fill='x', side='left')
        self.simple_value_value_frame.configure(height='200', width='200')
        self.simple_value_value_frame.pack(anchor='w', padx='10', pady='10', side='top')
        self.simple_value_comment_frame = ttk.Frame(self.simple_value_frame)
        self.simple_value_comment_label = ttk.Label(self.simple_value_comment_frame)
        self.simple_value_comment_label.configure(text='Comment: ')
        self.simple_value_comment_label.pack(side='left')
        self.simple_value_comment_entry = ttk.Entry(self.simple_value_comment_frame)
        self.simple_value_comment_entry.configure(width='50')
        self.simple_value_comment_entry.pack(expand='true', fill='x', side='left')
        self.simple_value_comment_frame.configure(height='200', width='200')
        self.simple_value_comment_frame.pack(anchor='w', padx='10', pady='0 10', side='top')
        self.simple_value_save_button = ttk.Button(self.simple_value_frame)
        self.simple_value_save_button.configure(text='Save')
        self.simple_value_save_button.pack(pady='0 5', side='bottom')
        self.simple_value_save_button.bind('<Button-1>', lambda event: ManageSettingMainApp.on_simple_save_event(self))
        self.simple_value_frame.configure(height='200', width='200')
        self.simple_value_frame.pack_forget()

        # ranged value
        self.ranged_value_frame = ttk.Frame()
        self.ranged_value_back = ttk.Button(self.ranged_value_frame)
        self.ranged_value_back.configure(text='Back')
        self.ranged_value_back.pack(anchor='w', side='top')
        self.ranged_value_back.bind('<Button-1>', lambda event: ManageSettingMainApp.switch_to_option_values(self))
        self.ranged_value_sparator = ttk.Separator(self.ranged_value_frame)
        self.ranged_value_sparator.configure(orient='horizontal')
        self.ranged_value_sparator.pack(expand='true', fill='x', pady='5 0', side='top')
        self.ranged_value_value_frame = ttk.Frame(self.ranged_value_frame)
        self.registred_number_validation = self.ranged_value_value_frame.register(self.validate_number)
        self.ranged_value_min_label = ttk.Label(self.ranged_value_value_frame)
        self.ranged_value_min_label.configure(text='Min: ')
        self.ranged_value_min_label.pack(side='left')
        self.ranged_value_min_entry = ttk.Entry(self.ranged_value_value_frame)
        self.ranged_value_min_entry.configure(width='7', validate="key", validatecommand=(self.registred_number_validation, '%P'))
        self.ranged_value_min_entry.pack(expand='true', fill='x', padx='0 10', side='left')
        self.ranged_value_max_label = ttk.Label(self.ranged_value_value_frame)
        self.ranged_value_max_label.configure(text='Max: ')
        self.ranged_value_max_label.pack(side='left')
        self.ranged_value_max_entry = ttk.Entry(self.ranged_value_value_frame)
        self.ranged_value_max_entry.configure(width='7', validate="key", validatecommand=(self.registred_number_validation, '%P'))
        self.ranged_value_max_entry.pack(padx='0 10', side='left')
        self.ranged_value_step_label = ttk.Label(self.ranged_value_value_frame)
        self.ranged_value_step_label.configure(text='Step: ')
        self.ranged_value_step_label.pack(side='left')
        self.ranged_value_step_entry = ttk.Entry(self.ranged_value_value_frame)
        self.ranged_value_step_entry.configure(width='7', validate="key", validatecommand=(self.registred_number_validation, '%P'))
        self.ranged_value_step_entry.pack(side='left')
        self.ranged_value_value_frame.configure(height='200', width='200')
        self.ranged_value_value_frame.pack(anchor='w', padx='10', pady='10', side='top')
        self.ranged_value_comment_frame = ttk.Frame(self.ranged_value_frame)
        self.ranged_value_comment_label = ttk.Label(self.ranged_value_comment_frame)
        self.ranged_value_comment_label.configure(text='Comment: ')
        self.ranged_value_comment_label.pack(side='left')
        self.ranged_value_comment_entry = ttk.Entry(self.ranged_value_comment_frame)
        self.ranged_value_comment_entry.configure(width='50')
        self.ranged_value_comment_entry.pack(expand='true', fill='x', side='left')
        self.ranged_value_comment_frame.configure(height='200', width='200')
        self.ranged_value_comment_frame.pack(anchor='w', padx='10', pady='0 10', side='top')
        self.ranged_value_save_button = ttk.Button(self.ranged_value_frame)
        self.ranged_value_save_button.configure(text='Save')
        self.ranged_value_save_button.pack(pady='0 5', side='bottom')
        self.ranged_value_save_button.bind('<Button-1>', lambda event: ManageSettingMainApp.on_ranged_save_event(self))
        self.ranged_value_frame.configure(height='200', width='200')
        self.ranged_value_frame.pack_forget()

        # file description
        self.file_description_frame = ttk.Frame()
        self.file_description_back = ttk.Button(self.file_description_frame)
        self.file_description_back.configure(text='Back')
        self.file_description_back.pack(anchor='w', side='top')
        self.file_description_back.bind('<Button-1>', lambda event: ManageSettingMainApp.switch_to_edit_file(self))
        self.file_description_frame_label = ttk.Label(self.file_description_frame)
        self.file_description_frame_label.configure(text='Enter any description you may have for this file:')
        self.file_description_frame_label.pack(anchor='w', padx='10', pady='10', side='top')
        self.file_description_text = tk.Text(self.file_description_frame)
        self.file_description_text.configure(height='10', width='50')
        self.file_description_text.pack(padx='10', pady='5', side='top')
        self.file_description_edit_button = ttk.Button(self.file_description_frame)
        self.file_description_edit_button.configure(text='Edit')
        self.file_description_edit_button.pack(side='bottom')
        self.file_description_edit_button.bind('<Button-1>', lambda event: ManageSettingMainApp.on_file_description_button_event(self))
        self.file_description_frame.configure(height='200', width='200')
        self.file_description_frame.pack_forget()

        # Main widget
        self.mainwindow = self.toplevel1


    def run_main(self):
        self.mainwindow.mainloop()

    def new_file_event(self):
        filename =  tk.filedialog.asksaveasfilename(initialdir = "/", defaultextension='.setting', title = "Save File", filetypes=[("setting", '*.setting')])
        
        if filename != '':
            response = common.create_setting_file(filename[:-8]) #To ommit the .setting for the specific module
        
            if response == 200:

                self.current_path = filename
                self.main_frame.pack_forget()
                self.new_file_frame.pack(side='top')

            elif response == 701:
                tk.messagebox.showwarning(title='Already exists', message='.setting file already exists')
            elif response == 702:
                tk.messagebox.showwarning(title='Already exists', message='.setting.xml file already exists')
            else:
                tk.messagebox.showwarning(title='Error', message=response)


    def open_file_event(self):
        filename = tk.filedialog.askopenfilename(initialdir = "/", title='Select a .setting file', filetypes=[("setting", '*.setting')])
        
        if filename != '':
            result = check.file_exists(filename)

            if result == 702:
                tk.messagebox.showwarning(title='.setting.xml missing', message='.setting.xml file missing! Both .setting and .setting.xml are required')
            elif result == 700:
                tk.messagebox.showwarning(title='Unusual error', message='700') #Unusual because it is a cli error
            elif result == 701:
                tk.messagebox.showwarning(title='Unusual error', message='701')
            else:
                self.current_path = result
                self.switch_to_edit_file()

    
    def switch_to_main(self):

        self.current_path == ''
        self.new_file_frame.pack_forget()
        self.edit_file_frame.pack_forget()
        self.main_frame.pack(side='top')


    def create_new_file(self):

        description = self.new_file_text.get("1.0", "end-1c")
        
        if description != '':
                set.file_description(self.current_path, description)

        self.switch_to_edit_file()

    
    def switch_to_edit_file(self):
        self.edit_option_frame.pack_forget()
        self.new_option_frame.pack_forget()
        self.new_file_frame.pack_forget()
        self.main_frame.pack_forget()
        self.file_description_frame.pack_forget()
        
        options_list = get.option_names_in_file(self.current_path)

        if options_list == []:
            self.edit_file_list_combobox.config(state="disabled")
            self.edit_file_edit_button.config(state="disabled")
            self.edit_file_remove_button.config(state="disabled")
        else:
            self.edit_file_list_combobox.config(state="normal")
            self.edit_file_edit_button.config(state="normal")
            self.edit_file_remove_button.config(state="normal")
            self.edit_file_list_combobox.configure(values=options_list)
            self.edit_file_list_combobox.current(0)

        self.edit_file_frame.pack(side='top')

    
    def switch_to_edit_option(self):
        self.option_values_frame.pack_forget()
        self.edit_file_frame.pack_forget()
        self.new_option_frame.pack_forget()

        self.edit_option_name_entry.delete(0, tk.END)
        self.edit_option_name_entry.insert(0,self.edit_file_list_combobox.get())
        self.current_option_name = self.edit_file_list_combobox.get()
        self.edit_option_default_value_entry.delete(0, tk.END)
        self.edit_option_default_value_entry.insert(0,get.default_value(self.current_path, self.edit_file_list_combobox.get()))
        self.edit_option_comment_entry.delete(0, tk.END)

        comment = get.option_comment(self.current_path, self.edit_file_list_combobox.get())
        if comment == None:
            comment = ''

        self.edit_option_comment_entry.insert(0,comment)

        self.edit_option_frame.pack(side='top')


    def edit_option_save_event(self):

        error_list = ''
        success_list = ''

        new_name = self.edit_option_name_entry.get()

        if new_name != self.current_option_name:
            name_check = check.option_name(new_name)

            if name_check == 701:
                error_list += "Option name must not contain ':'\n"
            elif name_check == 702:
                error_list += "Option name must not contain ','\n"
            elif name_check == 703:
                error_list += "Option name cannot start with '#'\n"
            elif name_check == 704:
                error_list += "Error: Option name includes new line\n"
            elif name_check == 700:
                error_list += 'Option name cannot be empty!\n'
            elif name_check != 200:
                error_list += 'Unspecified Option Name Error\n'
            elif check.option_exists_in_file(self.current_path, new_name):
                error_list += 'This option name already exists!\n'
            else:
                response = common.change_option_name(self.current_path, self.current_option_name, new_name)

                if response == 200:
                    self.current_option_name = self.edit_option_name_entry.get()
                    success_list += 'Name changed successfully\n'

                else:
                    error_list += 'Name changed successfully.\nCaution: Option name was not found in .setting.xml file, file could be corrupted\n'
            
        new_default = self.edit_option_default_value_entry.get()

        if get.default_value(self.current_path, self.current_option_name) != new_default:
            check_value = check.general_value(new_default)

            if check_value == 700:
                error_list += "Default must not contain ','\n"
            elif check_value == 701:
                error_list += "Error: Default includes new line\n"
            elif check_value != 200:
                error_list += 'Unspecified Default Error\n'
            else:
                response = set.default(self.current_path, self.current_option_name, new_default)

                if response == 200:
                    success_list += 'Default changed successfully\n'
                elif response == 201:
                    error_list += 'Default changed successfully.\nCaution: Option name was not found in .setting.xml file, file could be corrupted\n'
                    
        comment = self.edit_option_comment_entry.get()
        
        if comment != get.option_comment(self.current_path, self.current_option_name):
            if '\n' in comment:
                error_list += 'Error: Comment includes new line\n'
            else:
                response = set.option_comment(self.current_path, self.current_option_name, comment)

                if response == 200:
                    success_list += 'Comment changed successfully\n'
                elif response == 201:
                    error_list += 'Comment changed successfully.\nCaution: Option name was not found in .setting.xml file, file could be corrupted\n'

        if success_list != '':
            tk.messagebox.showinfo(title='Saved Successfully', message=success_list)
        if error_list != '':
            tk.messagebox.showerror(title='Error', message=error_list)

    def switch_to_option_values(self):
        self.edit_option_frame.pack_forget()
        self.simple_value_frame.pack_forget()
        self.ranged_value_frame.pack_forget()

        self.is_value_new = True

        values_list = get.option_values(self.current_path, self.current_option_name)

        if values_list == []:
            self.option_values_list_combobox.config(state="disabled")
            self.option_values_edit_button.config(state="disabled")
            self.option_values_remove_button.config(state="disabled")
        else:
            self.option_values_list_combobox.config(state="normal")
            self.option_values_edit_button.config(state="normal")
            self.option_values_remove_button.config(state="normal")
            self.option_values_list_combobox.configure(values=values_list)
            self.option_values_list_combobox.current(0)

        self.option_values_frame.pack(side='top')


    def switch_to_simple_values(self, value = '', comment = ''):
        
        self.option_values_frame.pack_forget()

        self.simple_value_value_entry.delete(0, tk.END)
        self.simple_value_value_entry.insert(0, value)
        self.simple_value_comment_entry.delete(0, tk.END)
        self.simple_value_comment_entry.insert(0, comment)

        self.simple_value_frame.pack(side='top')


    def switch_to_ranged_values(self, min = '', max = '', step = '', comment = ''):
        
        self.option_values_frame.pack_forget()

        self.ranged_value_min_entry.delete(0, tk.END)
        self.ranged_value_min_entry.insert(0, min)
        self.ranged_value_max_entry.delete(0, tk.END)
        self.ranged_value_max_entry.insert(0, max)
        self.ranged_value_step_entry.delete(0, tk.END)
        self.ranged_value_step_entry.insert(0, step)
        self.ranged_value_comment_entry.delete(0, tk.END)
        self.ranged_value_comment_entry.insert(0, comment)

        self.ranged_value_frame.pack(side='top')


    def validate_number(self, p):
        '''For tkinter validation'''

        num_regex = re.compile(r'^[+-]?[0-9]*[.]?[0-9]*$')

        if num_regex.match(p):
            return True
                        
        elif p is "":
            return True

        else:
            return False


    def on_simple_save_event(self):
        """On simple value add or edit 'Save' button is pressed"""
        
        value = self.simple_value_value_entry.get()

        if value == '':
            tk.messagebox.showerror(title='Error', message="Value cannot be empty")
        else:
            check_value = check.general_value(value)
        
            if check_value == 700:
                tk.messagebox.showerror(title='Error', message="Value must not contain ','")
            elif check_value == 701:
                tk.messagebox.showerror(title='Error', message="Error: Value includes new line")
            elif check_value != 200:
                tk.messagebox.showerror(title='Error', message="Unspecified Value Error")
            elif ( ((self.is_value_new) or (get.possible_value_by_number(self.current_path, self.current_option_name, self.option_values_list_combobox.current())['name'] != value)) and
                (check.option_simple_value_exists(self.current_path, self.current_option_name, value)) ):
                tk.messagebox.showerror(title='Error', message="This value already exists")
            else:
                comment = self.simple_value_comment_entry.get()

                if self.is_value_new:
                    response = common.add_simple_value(self.current_path, self.current_option_name, value, comment)

                    if response == 200:
                        self.simple_value_value_entry.delete(0, tk.END)
                        self.simple_value_comment_entry.delete(0, tk.END)
                        tk.messagebox.showinfo(title='Success', message="Value saved successfully")
                    else:
                        tk.messagebox.showerror(title='Faild', message="Value failed to save unexpectedly")

                else:
                    response_1 = common.set_value_comment_by_number(self.current_path, self.current_option_name, self.option_values_list_combobox.current(), comment)
                    response_2 = common.set_simple_possible_value_by_number(self.current_path, self.current_option_name, self.option_values_list_combobox.current(), value)

                    if response_1 == 200 and response_2 == 200:
                        tk.messagebox.showinfo(title='Success', message="Value saved successfully")
                    else:
                        tk.messagebox.showerror(title='Faild', message="Failed to save unexpectedly")


    def on_ranged_save_event(self):
        """On ranged value add or edit 'Save' button is pressed"""
        
        min = self.ranged_value_min_entry.get()
        max = self.ranged_value_max_entry.get()
        step = self.ranged_value_step_entry.get()
        comment = self.ranged_value_comment_entry.get()

        file_value = get.possible_value_by_number(self.current_path, self.current_option_name, self.option_values_list_combobox.current()) # Value which is currently saved

        if min == max == step == '':
            tk.messagebox.showerror(title='Error', message="All fields cannot be empty")
        elif ( ((self.is_value_new) or (file_value['min'] != min or file_value['max'] != max or file_value['step'] != step)) and
                (check.option_renage_value_exists(self.current_path, self.current_option_name, min, max, step)) ):
            tk.messagebox.showerror(title='Error', message="This range already exists")
        else:

            if self.is_value_new:
                response = common.add_range_value(self.current_path, self.current_option_name, min, max, step, comment)

                if response == 200:
                    self.ranged_value_min_entry.delete(0, tk.END)
                    self.ranged_value_max_entry.delete(0, tk.END)
                    self.ranged_value_step_entry.delete(0, tk.END)
                    self.ranged_value_comment_entry.delete(0, tk.END)
                    tk.messagebox.showinfo(title='Success', message="Range saved successfully")
                else:
                    tk.messagebox.showerror(title='Faild', message="Range failed to save unexpectedly")

            else:
                response_1 = common.set_value_comment_by_number(self.current_path, self.current_option_name, self.option_values_list_combobox.current(), comment)
                response_2 = response = common.set_ranged_possible_value_by_number(self.current_path, self.current_option_name, self.option_values_list_combobox.current(), min, max, step)

                if response_1 == 200 and response_2 == 200:
                    tk.messagebox.showinfo(title='Success', message="Range saved successfully")
                else:
                    tk.messagebox.showerror(title='Faild', message="Failed to save unexpectedly")


    def on_value_edit_event(self):

        self.is_value_new = False

        value = get.possible_value_by_number(self.current_path, self.current_option_name, self.option_values_list_combobox.current())

        if value['comment'] == None:
            value['comment'] = ''

        if 'min' in value:#Check if value is ranged
            self.switch_to_ranged_values(min = value['min'], max = value['max'], step = value['step'], comment = value['comment'])
        elif 'name' in value:
            self.switch_to_simple_values(value = value['name'], comment = value['comment'])


    def on_value_remove_event(self):

        response = tk.messagebox.askquestion('Confirmation', 'Are you sure you want delete this value?')
        
        if response == 'yes':
            common.remove_possible_value_by_number(self.current_path, self.current_option_name, self.option_values_list_combobox.current())

            values_list = get.option_values(self.current_path, self.current_option_name)

            if values_list == []:
                self.option_values_list_combobox.config(state="disabled")
                self.option_values_edit_button.config(state="disabled")
                self.option_values_remove_button.config(state="disabled")
            else:
                self.option_values_list_combobox.config(state="normal")
                self.option_values_edit_button.config(state="normal")
                self.option_values_remove_button.config(state="normal")
                self.option_values_list_combobox.configure(values=values_list)
                self.option_values_list_combobox.current(0)
        
    
    def switch_to_new_option(self):
        self.edit_file_frame.pack_forget()

        self.new_option_name_entry.delete(0, tk.END)
        self.new_option_default_value_entry.delete(0, tk.END)
        self.new_option_comment_entry.delete(0, tk.END)

        self.new_option_frame.pack(side='top')


    def new_option_save_event(self):
        error_list = ''
        success_list = ''

        new_name = self.new_option_name_entry.get()

        name_check = check.option_name(new_name)

        if name_check == 701:
            error_list += "Option name must not contain ':'\n"
        elif name_check == 702:
            error_list += "Option name must not contain ','\n"
        elif name_check == 703:
            error_list += "Option name cannot start with '#'\n"
        elif name_check == 704:
            error_list += "Error: Option name includes new line\n"
        elif name_check == 700:
            error_list += 'Option name cannot be empty!\n'
        elif name_check != 200:
            error_list += 'Unspecified Option Name Error\n'
        elif check.option_exists_in_file(self.current_path, new_name):
            error_list += 'This option name already exists!\n'
        else:
            comment = self.new_option_comment_entry.get()
       
            if '\n' in comment:
                error_list += 'Error: Comment includes new line\n'
                comment = ''

            response = common.add_option_to_file(self.current_path, new_name, comment)

            if response == 200:
                success_list += 'Option created successfully\n'
            elif response == 201:
                error_list += 'Caution: Option created successfully! Definition for option ' + new_name + ' already exists in setting.xml file\n'
            
            options_list = get.option_names_in_file(self.current_path)

            self.edit_file_list_combobox.config(state="normal")
            self.edit_file_edit_button.config(state="normal")
            self.edit_file_remove_button.config(state="normal")
            self.edit_file_list_combobox.configure(values=options_list)
            self.edit_file_list_combobox.current(len(options_list) -1)

            new_default = self.new_option_default_value_entry.get()

            check_value = check.general_value(new_default)

            if check_value == 700:
                error_list += "Default must not contain ','\n"
            elif check_value == 701:
                error_list += "Error: Default includes new line\n"
            elif check_value != 200:
                error_list += 'Unspecified Default Error\n'
            else:
                response = set.default(self.current_path, new_name, new_default)
                    
        if success_list != '':
            tk.messagebox.showinfo(title='Created Successfully', message=success_list)
        if error_list != '':
            tk.messagebox.showerror(title='Error', message=error_list)
        if success_list != '':
            self.switch_to_edit_option()

    
    def on_option_remove_event(self):
        response = tk.messagebox.askquestion('Confirmation', 'Are you sure you want delete this option?')
        
        if response == 'yes':
            response = common.remove_option_from_file(self.current_path, self.edit_file_list_combobox.get())

            option_list = get.option_names_in_file(self.current_path)

            if option_list == []:
                self.edit_file_list_combobox.config(state="disabled")
                self.edit_file_edit_button.config(state="disabled")
                self.edit_file_remove_button.config(state="disabled")
            else:
                self.edit_file_list_combobox.config(state="normal")
                self.edit_file_edit_button.config(state="normal")
                self.edit_file_remove_button.config(state="normal")
                self.edit_file_list_combobox.configure(values=option_list)
                self.edit_file_list_combobox.current(0)


    def switch_to_file_description(self):
        self.edit_file_frame.pack_forget()

        self.file_description_text.delete('1.0', tk.END)
        self.file_description_text.insert('1.0', get.file_description(self.current_path))

        self.file_description_frame.pack(side='top')


    def on_file_description_button_event(self):
        set.file_description(self.current_path, self.file_description_text.get('1.0', tk.END))

        self.switch_to_edit_file()


if __name__ == '__main__':
    app = ManageSettingMainApp()
    app.run_main()

