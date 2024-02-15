# Import files
from simopt.directory import model_directory, model_unabbreviated_directory
from simopt.data_farming_base import DataFarmingExperiment
# Import tkinter library
import tkinter as tk
from tkinter import ttk, filedialog
# Import other libraries
import csv
import ast
import time
import os
import pandas as pd

class Data_Farming():
    def __init__(self, master, main_widow, forced_creation = False):
        if not forced_creation:
            self.master = master
            self.main_window = main_widow
            self.master.grid_rowconfigure(0, weight=0)
            self.master.grid_rowconfigure(1, weight=0)
            self.master.grid_rowconfigure(2, weight=0)
            self.master.grid_rowconfigure(3, weight=0)
            self.master.grid_rowconfigure(4, weight=0)
            self.master.grid_rowconfigure(5, weight=0)
            self.master.grid_rowconfigure(6, weight=0)
            self.master.grid_rowconfigure(7, weight=0)
            self.master.grid_columnconfigure(0, weight=1)
            self.master.grid_columnconfigure(1, weight=1)
            self.master.grid_columnconfigure(2, weight=1)
            self.master.grid_columnconfigure(3, weight=1)
            self.master.grid_columnconfigure(4, weight=1)
            
            # Intitialize frames so prevous entries can be deleted
            self.design_frame = tk.Frame(master = self.master)
            self.design_frame.grid(row = 5, column = 0)
            
            self.create_design_frame = tk.Frame(master = self.master)
            self.run_frame = tk.Frame(master = self.master)
            self.factor_canvas = tk.Canvas (master = self.master)
            self.factors_frame = tk.Frame( master = self.factor_canvas)
            
            
            # Initial variable values
            self.factor_que_length = 1
            self.default_values_list = []
            self.checkstate_list=[]
            self.min_list = []
            self.max_list = []
            self.dec_list = []
            
            
            
            # Create main window title
            self.title_frame = tk.Frame(master=self.master)
            self.title_frame.grid_rowconfigure(0, weight=1)
            self.title_frame.grid_columnconfigure(0, weight=1)
            self.title_frame.grid( row=0, column = 0, sticky = tk.N)
            self.datafarming_title_label = tk.Label(master=self.title_frame,
                                                    text = "Model Data Farming",
                                                    font = "Calibri 15 bold")
            self.datafarming_title_label.grid( row = 0, column = 0) 
            
            # Create model selection drop down menu
            self.model_list = model_unabbreviated_directory
            self.modelselect_frame = tk.Frame(master=self.master)
            self.modelselect_frame.grid_rowconfigure(0, weight=1)
            self.modelselect_frame.grid_rowconfigure(1, weight=1)
            self.modelselect_frame.grid_columnconfigure(0, weight=1)
            self.modelselect_frame.grid_columnconfigure(1, weight=1)
            self.modelselect_frame.grid_columnconfigure(2, weight=1)
            self.modelselect_frame.grid_columnconfigure(3, weight=1)
            self.modelselect_frame.grid_columnconfigure(4, weight=1)
            
            self.modelselect_frame.grid( row =2, column = 0, sticky = tk.W )
            self.model_label = tk.Label(master=self.modelselect_frame, # window label is used in
                            text = "Select Model:",
                            font = "Calibri 13",
                            width = 20)
            self.model_label.grid( row = 0, column = 0, sticky = tk.W)       
            self.model_var = tk.StringVar()
            self.model_menu = ttk.OptionMenu(self.modelselect_frame, self.model_var, "Model", 
                                             *self.model_list, command= self.show_model_factors)
            self.model_menu.grid( row = 0, column = 1, sticky = tk.W)
            
            # Create load design button
            
            self.or_label = tk.Label(master = self.modelselect_frame,
                                     text = "OR",
                                     font = "Calibri 13",
                                     width = 20)
            self.or_label.grid( row = 0, column = 2, sticky = tk.W)
            
            self.load_design_button = tk.Button( master = self.modelselect_frame, text = 'Load Design CSV',
                                                width = 20, command = self.load_design)
            self.load_design_button.grid( row = 0, column = 3, sticky = tk.W)
            
            
    
            
            
    def load_design(self):
        
    
        #Clear previous selections
        for widget in self.factors_frame.winfo_children():
            widget.destroy()
            
        # Delete previous design tree
        for widget in self.create_design_frame.winfo_children():
            widget.destroy()
        
        for widget in self.run_frame.winfo_children():
            widget.destroy()
            
        for widget in self.design_frame.winfo_children():
            widget.destroy()
            
        
        # Initialize frame canvas
        self.factor_canvas = tk.Canvas (master = self.master)
        self.factor_canvas.grid_rowconfigure(0, weight = 1)
        self.factor_canvas.grid_columnconfigure(0, weight = 1)
        self.factor_canvas.grid( row = 4, column = 0, sticky = 'nsew')
        
        self.factors_title_frame = tk.Frame(master = self.master)
        self.factors_title_frame.grid( row = 3, column = 0, sticky = tk.N + tk.W)
        self.factors_title_frame.grid_rowconfigure(0, weight = 0)
        self.factors_title_frame.grid_columnconfigure(0, weight =1)
        self.factors_title_frame.grid_columnconfigure(1, weight =1)
        self.factors_title_frame.grid_columnconfigure(2, weight =1)
        
        self.factors_frame = tk.Frame( master = self.factor_canvas)
        self.factors_frame.grid( row = 0, column = 0, sticky = tk.W + tk.N)
        self.factors_frame.grid_rowconfigure(0, weight =1)
        self.factors_frame.grid_columnconfigure(0, weight =1)
        self.factors_frame.grid_columnconfigure(1, weight =1)
        self.factors_frame.grid_columnconfigure(2, weight =1)
        self.factors_frame.grid_columnconfigure(3, weight =1)
        
        
        # Create column for model factor names
        self.headername_label = tk.Label(master = self.factors_frame, text = 'Default Factors', font = "Calibri 13 bold", width = 20, anchor = 'w')
        self.headername_label.grid(row = 0, column = 0, sticky = tk.N + tk.W, padx = 10)
        
        # Create column for factor type
        self.headertype_label = tk.Label(master = self.factors_frame, text = 'Factor Type', font = "Calibri 13 bold", width = 20, anchor = 'w' )
        self.headertype_label.grid(row = 0, column = 1, sticky = tk.N + tk.W)
        
        #Values to help with formatting
        entry_width = 20
        
        # List to hold default values
        self.default_values_list = []
        self.fixed_str = {}
        
        # Create column for factor default values
        self.headerdefault_label = tk.Label(master = self.factors_frame, text = 'Default Value', font = "Calibri 13 bold", width = 20 )
        self.headerdefault_label.grid(row = 0, column = 2, sticky = tk.N + tk.W)
            
        # Name of design csv file
        self.design_csv_name = filedialog.askopenfilename()
        
        #Specify what model is being used
        split_name = self.design_csv_name.split("experiments/")
        split_name = split_name[1].split('_')
        self.selected_model = split_name[0]
     
       
        self.model_object = model_unabbreviated_directory[self.selected_model]() #Eventually allow selection here
        
        
        
        
        self.model_var.set(self.selected_model)
        
        
        #Determine factors not included in design
 
        with open( self.design_csv_name, 'r') as design_file:
            reader = csv.reader(design_file)
            self.all_factor_headers = next(reader)[1:]
         
        self.default_factor_list = [] 
        for model_factor in self.model_object.specifications:
            if model_factor not in self.all_factor_headers:
                self.default_factor_list.append(model_factor)
       
        # Number of all factors in model
        num_all_factors = len(self.all_factor_headers)
        # Number of vaired factors in experiment        
        num_factors = num_all_factors - len(self.default_factor_list)
        # Factor headers dictionary to be used in run function
        self.factor_headers = self.all_factor_headers[: num_factors]
        print('factor headers', self.factor_headers)
        #print( 'num factors', num_factors)
        
        # Determine values of default factors
        default_list = []
        with open( self.design_csv_name, 'r') as design_file:
            reader = csv.reader(design_file)
            # skip header row
            next(reader)
            # Read only default factor values
            default_list = next(reader)[num_factors + 1:]
            #print('default_list', default_list)
        

        # Allow user to change default values
        factor_idx = 0
        for  factor in self.default_factor_list:
            
            self.factor_datatype = self.model_object.specifications[factor].get("datatype")
            self.factor_description = self.model_object.specifications[factor].get("description")
            self.factor_default = default_list[factor_idx]
            
            
            self.factors_frame.grid_rowconfigure(self.factor_que_length, weight =1)
            
            if self.factor_datatype == int:
                self.str_type = 'int'
            elif self.factor_datatype == float:
                self.str_type = 'float'
            elif self.factor_datatype == list:
                self.str_type = 'list'
            elif self.factor_datatype == tuple:
                self.str_type = 'tuple'
          
           
            # Add label for factor names
            self.factorname_label = tk.Label (master = self.factors_frame, text = f"{factor} - {self.factor_description}", font = "Calibri 13", width = 40, anchor = 'w')
            self.factorname_label.grid( row = self.factor_que_length, column = 0, sticky = tk.N + tk.W, padx = 10)
            
            # Add label for factor type
            self.factortype_label = tk.Label (master = self.factors_frame, text = self.str_type, font = "Calibri 13", width = 20, anchor = 'w')
            self.factortype_label.grid( row = self.factor_que_length, column = 1, sticky = tk.N + tk.W)
            
            #Add entry box for default value
            default_len = len(str(self.factor_default))
            if default_len > entry_width:
                entry_width = default_len
                if default_len > 150:
                    entry_width = 150
            self.default_value= tk.StringVar()
            self.default_entry = tk.Entry( master = self.factors_frame, width = entry_width, textvariable = self.default_value, justify = 'right')
            self.default_entry.grid( row =self.factor_que_length, column =2, sticky = tk.N + tk.W, columnspan = 5)
            #Display original default value
            self.default_entry.insert(0, str(self.factor_default))
            self.default_values_list.append(self.default_value)
            
            
            self.factor_que_length += 1
            factor_idx += 1
            
        #Create change defaults button
        self.change_def_frame = tk.Frame( master = self.master)
        self.change_def_frame.grid(row = 5, column = 0)
        self.change_def_button = tk.Button(master = self.change_def_frame, text = 'Change Experiment Defaults', font = "Calibri 13",
                                                width = 30, command = self.update_defaults_button)
        self.change_def_button.grid( row = 0, column = 0)
            
           
        
        # Run to store default values
        self.update_defaults()
        
     
        
        # Create design text file to be used in experiment "model_factors_design"
        with open( "./data_farming_experiments/model_factors_design.txt", 'w', encoding="utf-8") as design_file:
            design_file.write("")
        with open(self.design_csv_name, 'r') as design_csv:
            reader = csv.reader(design_csv)
            next(reader)
            for row in design_csv:
                data_insert = ""
                # values for all factors
                factor_list = row.split(',')
                # values only for vaired factors in experiment
                design_list = factor_list[1: num_factors + 1]
                
                
                for factor in design_list:
                    data_insert += str(factor) + "\t"
                                       
                data_insert = data_insert[:-1]
                with open( "./data_farming_experiments/model_factors_design.txt", 'a', encoding="utf-8" ) as design_file:
                    design_file.write(data_insert + "\n")
                    
                    
                
            
            
                  
    def update_defaults(self):
        
        
        
        # Get default user values
        self.fixed_factors = {}
        default_csv_insert = []
        
        # List of values entered by user
        self.default_values = [self.default_value.get() for self.default_value in self.default_values_list]
        factor_index = 0
        for factor in self.default_factor_list:
            self.factor_datatype = self.model_object.specifications[factor].get("datatype")
            current_def_val = self.default_values[factor_index]
            if self.factor_datatype == float:
                self.fixed_factors[factor] = float(current_def_val)
            
            elif self.factor_datatype == int:
                self.fixed_factors[factor] = int(current_def_val)
            
            if self.factor_datatype == list:
                self.fixed_factors[factor] = ast.literal_eval(current_def_val)
        
            elif self.factor_datatype == tuple:
           
                tuple_str = tuple(current_def_val[1:-1].split(","))
                self.fixed_factors[factor] = tuple(float(s) for s in tuple_str)
            
            default_csv_insert.append(self.fixed_factors[factor])    
            factor_index += 1
    
        
        self.display_design_tree()
        

    # Display Model Factors
    def show_model_factors(self,*args ):
        
        
    
        self.factor_canvas.destroy()
        
        # Initialize frame canvas
        self.factor_canvas = tk.Canvas (master = self.master)
        self.factor_canvas.grid_rowconfigure(0, weight = 1)
        self.factor_canvas.grid_columnconfigure(0, weight = 1)
        self.factor_canvas.grid( row = 4, column = 0, sticky = 'nsew')
        self.factors_frame = tk.Frame( master = self.factor_canvas)
        self.factor_canvas.create_window((0, 0), window=self.factors_frame, anchor="nw")
        
        self.factors_frame.grid_rowconfigure(self.factor_que_length + 1, weight =1)
        

        
        self.factors_title_frame = tk.Frame(master = self.master)
        self.factors_title_frame.grid( row = 3, column = 0, sticky = 'nsew')
        self.factors_title_frame.grid_rowconfigure(0, weight = 0)
        self.factors_title_frame.grid_columnconfigure(0, weight =0)
        self.factors_title_frame.grid_columnconfigure(1, weight =0)
        self.factors_title_frame.grid_columnconfigure(2, weight =0)
        self.factors_title_frame.grid_columnconfigure(3, weight =0)
        self.factors_title_frame.grid_columnconfigure(4, weight =0)
        self.factors_title_frame.grid_columnconfigure(5, weight =0)
        self.factors_title_frame.grid_columnconfigure(6, weight =0)
        self.factors_title_frame.grid_columnconfigure(7, weight =0)
        
        #self.factors_frame = tk.Frame( master = self.factor_canvas)
        self.factors_frame.grid( row = 0, column = 0, sticky = 'nsew')
        self.factors_frame.grid_rowconfigure(0, weight =0)
        self.factors_frame.grid_columnconfigure(0, weight =0)
        self.factors_frame.grid_columnconfigure(1, weight =0)
        self.factors_frame.grid_columnconfigure(2, weight =0)
        self.factors_frame.grid_columnconfigure(3, weight =0)
        self.factors_frame.grid_columnconfigure(4, weight =0)
        self.factors_frame.grid_columnconfigure(5, weight =0)
        self.factors_frame.grid_columnconfigure(6, weight =0)
        self.factors_frame.grid_columnconfigure(7, weight =0)
        
      
  
        #Clear previous selections
        for widget in self.factors_frame.winfo_children():
            widget.destroy()
            
            
        # Delete previous design tree
        for widget in self.create_design_frame.winfo_children():
            widget.destroy()
        
        for widget in self.run_frame.winfo_children():
            widget.destroy()
            
        for widget in self.design_frame.winfo_children():
            widget.destroy()
        
        # Widget lists
        self.default_widgets = {}
        self.check_widgets = {}
        self.min_widgets = {}
        self.max_widgets = {}
        self.dec_widgets = {}
        self.cat_widgets = {}
        
               
        # Initial variable values
        self.factor_que_length = 1
        self.default_values_list = []
        self.checkstate_list=[]
        self.min_list = []
        self.max_list = []
        self.dec_list = []
        self.cat_checklist = []
        
        #Values to help with formatting
        entry_width = 20
        
        # Create column for model factor names
        self.headername_label = tk.Label(master = self.factors_frame, text = 'Model Factors', font = "Calibri 13 bold", width = 10, anchor = 'w')
        self.headername_label.grid(row = 0, column = 0, sticky = tk.N + tk.W, padx = 10)
        
        # Create column for factor type
        self.headertype_label = tk.Label(master = self.factors_frame, text = 'Factor Type', font = "Calibri 13 bold", width = 10, anchor = 'w' )
        self.headertype_label.grid(row = 0, column = 1, sticky = tk.N + tk.W)
        
        
        # Create column for factor default values
        self.headerdefault_label = tk.Label(master = self.factors_frame, text = 'Default Value', font = "Calibri 13 bold", width = 15 )
        self.headerdefault_label.grid(row = 0, column = 2, sticky = tk.N + tk.W)
        
        # Create column for factor check box
        self.headercheck_label = tk.Label(master = self.factors_frame, text = 'Include in Experiment', font = "Calibri 13 bold", width = 20 )
        self.headercheck_label.grid(row = 0, column = 3, sticky = tk.N + tk.W)
        
        # Create header for experiment options
        self.headercheck_label = tk.Label(master = self.factors_frame, text = 'Experiment Options', font = "Calibri 13 bold", width = 60 )
        self.headercheck_label.grid(row = 0, column = 4, columnspan = 3)
        
    
        
       
        
        
        # Get model selected from drop down
        self.selected_model = self.model_var.get()
        

        
    
                
        
        # Get model infor from dictionary
        self.model_object = self.model_list[self.selected_model]()
        
        for  factor in self.model_object.specifications:
            
            self.factor_datatype = self.model_object.specifications[factor].get("datatype")
            self.factor_description = self.model_object.specifications[factor].get("description")
            self.factor_default = self.model_object.specifications[factor].get("default")
            
            
            #Values to help with formatting
            entry_width = 10
            
            self.factors_frame.grid_rowconfigure(self.factor_que_length, weight =1)
            
            # Add label for factor names
            self.factorname_label = tk.Label (master = self.factors_frame, text = f"{factor} - {self.factor_description}", font = "Calibri 13", width = 40, anchor = 'w')
            self.factorname_label.grid( row = self.factor_que_length, column = 0, sticky = tk.N + tk.W, padx = 10)
        
            
            
            if self.factor_datatype == float:
            
                self.factors_frame.grid_rowconfigure(self.factor_que_length, weight =1)
                
                self.str_type = 'float'
             
                
                # Add label for factor type
                self.factortype_label = tk.Label (master = self.factors_frame, text = self.str_type, font = "Calibri 13", width = 10, anchor = 'w')
                self.factortype_label.grid( row = self.factor_que_length, column = 1, sticky = tk.N + tk.W)
                
                # Add entry box for default value
                self.default_value= tk.StringVar()
                self.default_entry = tk.Entry( master = self.factors_frame, width = entry_width, textvariable = self.default_value, justify = 'right')
                self.default_entry.grid( row =self.factor_que_length, column =2, sticky = tk.N + tk.W)
                #Display original default value
                self.default_entry.insert(0, self.factor_default)
                self.default_values_list.append(self.default_value)
                
                self.default_widgets[factor] = self.default_entry
                
                
                # Add check box
                self.checkstate = tk.BooleanVar()
                self.checkbox = tk.Checkbutton( master = self.factors_frame, variable = self.checkstate,
                                               command = self.include_factor, width = 5)
                self.checkbox.grid( row = self.factor_que_length, column = 3, sticky = 'nsew')
                self.checkstate_list.append(self.checkstate)
                
                self.check_widgets[factor] = self.checkbox
                
                # Add entry box for min val
                self.min_frame = tk.Frame (master = self.factors_frame)
                self.min_frame.grid( row = self.factor_que_length, column = 4, sticky = tk.N + tk.W )
                
                self.min_label = tk.Label(master = self.min_frame, text = 'Min Value', font = "Calibri 13", width = 10 )
                self.min_label.grid( row = 0, column = 0)
                self.min_val = tk.StringVar()
                self.min_entry = tk.Entry( master = self.min_frame, width = 10, textvariable = self.min_val, justify = 'right')
                self.min_entry.grid( row = 0, column = 1, sticky = tk.N + tk.W)
                
                self.min_list.append(self.min_val)    
                
                self.min_widgets[factor] = self.min_entry
                
                self.min_entry.configure(state = 'disabled')
                
                # Add entry box for max val
                self.max_frame = tk.Frame (master = self.factors_frame)
                self.max_frame.grid( row = self.factor_que_length, column = 5, sticky = tk.N + tk.W )
                
                self.max_label = tk.Label(master = self.max_frame, text = 'Max Value', font = "Calibri 13", width = 10 )
                self.max_label.grid( row = 0, column = 0) 
                
                self.max_val = tk.StringVar()
                self.max_entry = tk.Entry( master = self.max_frame, width = 10, textvariable = self.max_val, justify = 'right')
                self.max_entry.grid( row = 0, column = 1, sticky = tk.N + tk.W)
               
                self.max_list.append(self.max_val)    
                
                self.max_widgets[factor] = self.max_entry
                
                self.max_entry.configure(state = 'disabled')
                
                # Add entry box for editable decimals
                self.dec_frame = tk.Frame (master = self.factors_frame)
                self.dec_frame.grid( row = self.factor_que_length, column = 6, sticky = tk.N + tk.W )
                
                self.dec_label = tk.Label(master = self.dec_frame, text = '# Decimals', font = "Calibri 13", width = 10 )
                self.dec_label.grid( row = 0, column = 0) 
                
                self.dec_val = tk.StringVar()
                self.dec_entry = tk.Entry( master = self.dec_frame, width = 10, textvariable = self.dec_val, justify = 'right')
                self.dec_entry.grid( row = 0, column = 1, sticky = tk.N + tk.W)
                
                self.dec_list.append(self.dec_val)  
                
                self.dec_widgets[factor] = self.dec_entry
                
                self.dec_entry.configure(state = 'disabled')
                
                self.factor_que_length += 1
            
            elif self.factor_datatype == int:
            
                self.factors_frame.grid_rowconfigure(self.factor_que_length, weight =1)
                
                self.str_type = 'int'
    
                
                # Add label for factor type
                self.factortype_label = tk.Label (master = self.factors_frame, text = self.str_type, font = "Calibri 13", width = 10, anchor = 'w')
                self.factortype_label.grid( row = self.factor_que_length, column = 1, sticky = tk.N + tk.W)
                
                # Add entry box for default value
                self.default_value= tk.StringVar()
                self.default_entry = tk.Entry( master = self.factors_frame, width = entry_width, textvariable = self.default_value, justify = 'right')
                self.default_entry.grid( row =self.factor_que_length, column =2, sticky = tk.N + tk.W)
                #Display original default value
                self.default_entry.insert(0, self.factor_default)
                self.default_values_list.append(self.default_value)
                
                self.default_widgets[factor] = self.default_entry
                
                self.checkstate = tk.BooleanVar()
                self.checkbox = tk.Checkbutton( master = self.factors_frame, variable = self.checkstate,
                                               command = self.include_factor)
                self.checkbox.grid( row = self.factor_que_length, column = 3, sticky = 'nsew')
                self.checkstate_list.append(self.checkstate)
                
                self.check_widgets[factor] = self.checkbox
                
                # Add entry box for min val
                self.min_frame = tk.Frame (master = self.factors_frame)
                self.min_frame.grid( row = self.factor_que_length, column = 4, sticky = tk.N + tk.W )
                
                self.min_label = tk.Label(master = self.min_frame, text = 'Min Value', font = "Calibri 13", width = 10 )
                self.min_label.grid( row = 0, column = 0)
                self.min_val = tk.StringVar()
                self.min_entry = tk.Entry( master = self.min_frame, width = 10, textvariable = self.min_val, justify = 'right')
                self.min_entry.grid( row = 0, column = 1, sticky = tk.N + tk.W)
                
                self.min_list.append(self.min_val)    
                
                self.min_widgets[factor] = self.min_entry
                
                self.min_entry.configure(state = 'disabled')
                
                # Add entry box for max val
                self.max_frame = tk.Frame (master = self.factors_frame)
                self.max_frame.grid( row = self.factor_que_length, column = 5, sticky = tk.N + tk.W )
                
                self.max_label = tk.Label(master = self.max_frame, text = 'Max Value', font = "Calibri 13", width = 10 )
                self.max_label.grid( row = 0, column = 0) 
                
                self.max_val = tk.StringVar()
                self.max_entry = tk.Entry( master = self.max_frame, width = 10, textvariable = self.max_val, justify = 'right')
                self.max_entry.grid( row = 0, column = 1, sticky = tk.N + tk.W)
               
                self.max_list.append(self.max_val)    
                
                self.max_widgets[factor] = self.max_entry
                
                self.max_entry.configure(state = 'disabled')
                
                self.factor_que_length += 1
            
            elif self.factor_datatype == list:
                
                self.factors_frame.grid_rowconfigure(self.factor_que_length, weight =1)
                
                self.str_type = 'list'
               
                # Add label for factor names
                # self.factorname_label = tk.Label (master = self.factors_frame, text = factor, font = "Calibri 13", width = 30, anchor = 'w')
                # self.factorname_label.grid( row = self.factor_que_length, column = 0, sticky = tk.N + tk.W)
                
                # Add label for factor type
                self.factortype_label = tk.Label (master = self.factors_frame, text = self.str_type, font = "Calibri 13", width = 10, anchor = 'w')
                self.factortype_label.grid( row = self.factor_que_length, column = 1, sticky = tk.N + tk.W)
                
                #Add entry box for default value
                default_len = len(str(self.factor_default))
                if default_len > entry_width:
                    entry_width = default_len
                    if default_len > 25:
                        entry_width = 25
                self.default_value= tk.StringVar()
                self.default_entry = tk.Entry( master = self.factors_frame, width = entry_width, textvariable = self.default_value, justify = 'right')
                self.default_entry.grid( row =self.factor_que_length, column =2, sticky = tk.N + tk.W, columnspan = 5)
                #Display original default value
                self.default_entry.insert(0, str(self.factor_default))
                self.default_values_list.append(self.default_value)
                
                
                
      
                
                # Add checkbox (currently not visible)
                self.checkstate = tk.BooleanVar()
                self.checkbox = tk.Checkbutton( master = self.factors_frame, variable = self.checkstate,
                                               command = self.include_factor)
                #self.checkbox.grid( row = self.factor_que_length, column = 3, sticky = 'nsew')
                self.checkstate_list.append(self.checkstate)
                
                self.check_widgets[factor] = self.checkbox
            
                self.factor_que_length += 1
                
            elif self.factor_datatype == tuple:
                
                self.factors_frame.grid_rowconfigure(self.factor_que_length, weight =1)
                
                self.str_type = 'tuple'
               
                
                # Add label for factor type
                self.factortype_label = tk.Label (master = self.factors_frame, text = self.str_type, font = "Calibri 13", width = 10, anchor = 'w')
                self.factortype_label.grid( row = self.factor_que_length, column = 1, sticky = tk.N + tk.W)
                
                # Add entry box for default value
                default_len = len(str(self.factor_default))
                if default_len > entry_width:
                    entry_width = default_len
                    if default_len > 25:
                        entry_width = 25
                self.default_value= tk.StringVar()
                self.default_entry = tk.Entry( master = self.factors_frame, width = entry_width, textvariable = self.default_value, justify = 'right')
                self.default_entry.grid( row =self.factor_que_length, column =2, sticky = tk.N + tk.W, columnspan = 5)
                #Display original default value
                self.default_entry.insert(0, str(self.factor_default))
                self.default_values_list.append(self.default_value)
                
             
                
                # Add checkbox (currently not visible)
                self.checkstate = tk.BooleanVar()
                self.checkbox = tk.Checkbutton( master = self.factors_frame, variable = self.checkstate,
                                               command = self.include_factor)
                #self.checkbox.grid( row = self.factor_que_length, column = 3, sticky = 'nsew')
                self.checkstate_list.append(self.checkstate)
                
                self.check_widgets[factor] = self.checkbox
               
                self.factor_que_length += 1

        

        
        # Design type selection menu
        self.design_frame = tk.Frame(master = self.master)
        self.design_frame.grid(row = 5, column = 0)
        self.design_type_label = tk.Label (master = self.design_frame, text = 'Select Design Type', font = "Calibri 13", width = 20)
        self.design_type_label.grid( row = 0, column = 0)
        
        self.design_types_list = ['NOLH']
        self.design_var = tk.StringVar()
        self.design_type_menu = ttk.OptionMenu(self.design_frame, self.design_var, 'Design Type', *self.design_types_list, command = self.enable_stacks)
        self.design_type_menu.grid(row = 0, column = 1, padx = 30)
        
        #Stack selection menu
        self.stack_label = tk.Label (master = self.design_frame, text = "Select Number of Stacks", font = "Calibri 13", width = 20)
        self.stack_label.grid( row =1, column = 0)
        self.stack_list = ['1', '2', '3']
        self.stack_var = tk.StringVar()
        self.stack_menu = ttk.OptionMenu(self.design_frame, self.stack_var, 'Stacks', *self.stack_list, command = self.get_design_pts)
        self.stack_menu.grid( row = 1, column = 1)
        self.stack_menu.configure(state = 'disabled')
        
        # # Design pts label
        # self.design_pts_title = tk.Label (master = self.design_frame, text = 'Design Points', font = "Calibri 13", width = 50)
        # self.design_pts_title.grid( row = 0, column = 2)
        
        # Create design button
        self.create_design_button = tk.Button(master = self.design_frame, text = 'Create Design', font = "Calibri 13", command = self.create_design , width = 20)
        self.create_design_button.grid( row = 0, column = 3)
        self.create_design_button.configure(state = 'disabled')
        
 
    def onFrameConfigure_factor(self, *args):
        self.factor_canvas.configure(scrollregion=self.factor_canvas.bbox('all'))
        
 
    # Used to display the design tree for both created and loaded designs
    def display_design_tree(self):
        
        

        # Get list of factor names from csv file
        with open( self.design_csv_name, 'r') as design_file:
            reader = csv.reader(design_file)
            self.all_factor_headers = next(reader)[1:]
       
        #Get list of default factor names 
        default_factor_names = [] 
        for factor in self.all_factor_headers:
            if factor not in self.model_object.specifications:
                default_factor_names.append(factor)
        # number of variable factors in experiment
        self.num_factors = len(self.all_factor_headers) - len(default_factor_names)
       
        
        #Initialize design tree
        self.create_design_frame = tk.Frame(master = self.master)
        self.create_design_frame.grid( row = 6, column = 0)
        self.create_design_frame.grid_rowconfigure( 0, weight = 0)
        self.create_design_frame.grid_rowconfigure( 1, weight = 1)
        self.create_design_frame.grid_columnconfigure( 0, weight = 1)
        self.create_design_frame.grid_columnconfigure( 1, weight = 1)
        
        self.create_design_label = tk.Label( master = self.create_design_frame, text = 'Generated Designs', font = "Calibri 13 bold", width = 50)
        self.create_design_label.grid(row = 0, column = 0, sticky = tk.W)
   
        self.design_tree = ttk.Treeview( master = self.create_design_frame)
        self.design_tree.grid(row = 1, column = 0, sticky = 'nsew', padx = 10)
        
        # Create headers for each factor 
        self.design_tree['columns'] = self.all_factor_headers
        self.design_tree.column("#0", width=80, anchor = 'e' )
        for factor in self.all_factor_headers:
            self.design_tree.column(factor, width=250, anchor = 'e') 
            self.design_tree.heading( factor, text = factor)
       
        
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=('Calibri', 13, 'bold'))
        self.style.configure("Treeview", foreground="black", font = ('Calibri', 13))
        self.design_tree.heading( '#0', text = 'Design #' )
        
        # Read design file and output row plus default values to design tree
        with open( self.design_csv_name, 'r') as design_file:
            reader = csv.reader(design_file)
            #skip header row
            next(reader)
            # used to number design rows
            row_index = 0
            for row in reader:
                current_design_row = row[1:]
                data_insert = current_design_row 
                self.design_tree.insert("", 'end', text = row_index, values = data_insert, tag = 'style')
                row_index += 1
                
            # Create a horizontal scrollbar
        xscrollbar = ttk.Scrollbar(master = self.create_design_frame, orient="horizontal", command= self.design_tree.xview)
        xscrollbar.grid(row = 2, column = 0, sticky = 'nsew')
        yscrollbar = ttk.Scrollbar(master = self.create_design_frame, orient="vertical", command= self.design_tree.yview)
        yscrollbar.grid(row = 1, column = 1, sticky = 'nsew')
        
        # Configure the Treeview to use the horizontal scrollbar
        self.design_tree.configure(xscrollcommand=xscrollbar.set)
        self.design_tree.configure(yscrollcommand=yscrollbar.set)
        
        # Create buttons to run experiment
        self.run_frame = tk.Frame(master = self.master)
        self.run_frame.grid(row = 7, column = 0)
        self.run_frame.grid_columnconfigure(0, weight = 1)
        self.run_frame.grid_columnconfigure(1, weight = 1)
        self.run_frame.grid_columnconfigure(2, weight = 1)
        self.run_frame.grid_rowconfigure(0, weight = 0)
        self.run_frame.grid_rowconfigure(1, weight = 0)
  
        
        self.rep_label = tk.Label(master = self.run_frame, text = 'Replications', font = 'Calibri 13', width = 20)
        self.rep_label.grid( row = 0, column = 0, sticky = tk.W)
        self.rep_var = tk.StringVar()
        self.rep_entry = tk.Entry( master = self.run_frame, textvariable = self.rep_var, width = 10)
        self.rep_entry.grid( row = 0, column = 1, sticky = tk.W)
        
        self.crn_label = tk.Label(master = self.run_frame, text = 'CRN', font = 'Calibri 13', width = 20)
        self.crn_label.grid( row = 1, column = 0, sticky = tk.W)
        self.crn_var = tk.StringVar()
        self.crn_option = ttk.OptionMenu( self.run_frame, self.crn_var,'Yes', 'Yes', 'No')
        self.crn_option.grid(row = 1, column =1, sticky = tk.W)
        
      
        
        self.run_button = tk.Button(master = self.run_frame, text = 'Run All', font = 'Calibri 13', width = 20, command = self.run_experiment)
        self.run_button.grid( row = 0, column = 2, sticky = tk.E, padx = 30)
        
  
        
        
    def enable_stacks(self, *args):
        self.stack_menu.configure(state = 'normal')
    
    def get_design_pts(self, *args):
        self.design_pts = self.stack_var.get() + " test "
        
        #self.design_pts_label = tk.Label( master = self.design_frame, text = self.design_pts, font = "Calibri 13", width = 50)
        #self.design_pts_label.grid( row = 1, column =2)
        
        self.create_design_button.configure(state = 'normal')
        
        
        
    def create_design(self, *args):
       
        self.create_design_frame = tk.Frame(master = self.master)
        self.create_design_frame.grid( row = 6, column = 0)
        self.create_design_frame.grid_rowconfigure( 0, weight = 0)
        self.create_design_frame.grid_rowconfigure( 1, weight = 1)
        self.create_design_frame.grid_columnconfigure( 0, weight = 1)
    
        
        #Export design factors
        
        self.default_values = [self.default_value.get() for self.default_value in self.default_values_list]
        self.check_values = [self.checkstate.get() for self.checkstate in self.checkstate_list]
        self.min_values = [self.min_val.get() for self.min_val in self.min_list]
        self.max_values = [self.max_val.get() for self.max_val in self.max_list]
        self.dec_values = [self.dec_val.get() for self.dec_val in self.dec_list]
        self.fixed_factors = {}
        self.factor_index = 0
        self.maxmin_index = 0
        self.dec_index = 0
        # List used for parsing design file
        self.factor_headers = [] 
        
        #Dictionary used for tree view display of fixed factors
        self.fixed_str = {}
        
       
      
        # Write model factors file
        
        with open("./data_farming_experiments/model_factors.txt", "w") as self.model_design_factors:
            self.model_design_factors.write("")
         
        # List to hold names of all factors part of model to be displayed in csv
        self.factor_names = []
        self.def_factor_names = []
        # Get experiment information    
        for  factor in self.model_object.specifications:
            
            self.factor_datatype = self.model_object.specifications[factor].get("datatype")
            self.factor_description = self.model_object.specifications[factor].get("description")
           
            
            
            
            self.factor_default = self.default_values[self.factor_index]
            self.factor_include = self.check_values[self.factor_index]
            
            
            
            if self.factor_include == True:
                
                # Add factor to list of design factors in order that will be varied
                self.factor_headers.append(factor)
                # Factor names in csv are unedited
                self.factor_names.append(factor)
            
                if self.factor_datatype == float or self.factor_datatype == int:
                    self.factor_min = str(self.min_values[self.maxmin_index])
                    self.factor_max = str(self.max_values[self.maxmin_index])
                    self.maxmin_index += 1
                    
                    if self.factor_datatype == float:
                        self.factor_dec = str(self.dec_values[self.dec_index])
                        self.dec_index += 1
                        
                    elif self.factor_datatype == int:
                        self.factor_dec = '0'
                        
                    self.data_insert = self.factor_min + ' ' + self.factor_max + ' ' + self.factor_dec
                    with open("./data_farming_experiments/model_factors.txt", "a") as self.model_design_factors:
                        self.model_design_factors.write(self.data_insert + '\n') 
                        
                
                          
                   
            
            # Include fixed default values in design
            if self.factor_include == False:
                
                # Factor names in csv have "(default)" appended to end
                self.def_factor_names.append(factor + ' (default)')
                
                # Values to be placed in tree view of design
                self.fixed_str[factor] = self.factor_default
               
                if self.factor_datatype == float or self.factor_datatype == int:
                    # self.factor_default = str(self.default_values[self.factor_index])
                    # self.data_insert = self.factor_default + ' ' + self.factor_default + ' 0'
                    self.maxmin_index += 1
               
                # Add default values to exeriment and set to correct datatype
                if self.factor_datatype == float:
                    self.fixed_factors[factor] = float(self.factor_default)
                    self.dec_index += 1
                    
                elif self.factor_datatype == int:
                    self.fixed_factors[factor] = int(self.factor_default)
                    
            if self.factor_datatype == list:
                self.fixed_factors[factor] = ast.literal_eval(self.factor_default)
                
            elif self.factor_datatype == tuple:
                   
                tuple_str = tuple(self.factor_default[1:-1].split(","))
                self.fixed_factors[factor] = tuple(float(s) for s in tuple_str)
   
            self.factor_index += 1
            
        
        #Create design file
        model_name = self.model_object.name
        model_fixed_factors = self.fixed_factors
        
        self.model = model_directory[model_name](fixed_factors=model_fixed_factors)
        
        factor_settings_filename = 'model_factors'
       
        
        # for  factor in self.model_object.specifications:
            
        # # Specify the names of the model factors (in order) that will be varied.
        
        #     # factor_headers.append(factor)
            
        
        # Number of stacks specified by user
        num_stack = self.stack_var.get()
        # Create model factor design from .txt file of factor settings.
        # Hard-coded for a single-stack NOLHS.
        #command = "stack_nolhs.rb -s 1 model_factor_settings.txt > outputs.txt"
        #command = f"stack_nolhs.rb -s 2 ./data_farming_experiments/{factor_settings_filename}.txt > ./data_farming_experiments/{factor_settings_filename}_design.txt"
        command = "stack_nolhs.rb -s " + num_stack + f" ./data_farming_experiments/{factor_settings_filename}.txt > ./data_farming_experiments/{factor_settings_filename}_design.txt"
       
        os.system(command) 
        # Append design to base filename.
        design_filename = f"{factor_settings_filename}_design"
        # Read in design matrix from .txt file. Result is a pandas DataFrame.
        design_table = pd.read_csv(f"./data_farming_experiments/{design_filename}.txt", header=None, delimiter="\t", encoding="utf-8")
        # Count number of design_points.
        self.n_design_pts = len(design_table)
        # Create all design points.
        self.design = []
     
        
        #Time stamp for file name
        timestamp = time.strftime("%Y%m%d%H%M%S")
        
        # Create design csv file with headers
        self.design_csv_name= "./data_farming_experiments/" + self.selected_model + "_design_" + timestamp + ".csv"
      
        with open(self.design_csv_name, "w", newline='') as self.model_design_csv:
            writer = csv.writer(self.model_design_csv)
            writer.writerow(['Design #'] + self.factor_names + self.def_factor_names)
        


        # Get default values for factors not included in experiment
        default_list = []
        for factor in self.fixed_str:
            default_list.append(self.fixed_str[factor])
            
        for dp_index in range(self.n_design_pts):
            current_factor_designs = []
            for factor_idx in range(len(self.factor_headers)):
                current_factor_designs.append(design_table[factor_idx][dp_index])
            data_insert = current_factor_designs + default_list   
                
             
            
            
            # Write design points to csv file
            with open(self.design_csv_name, "a", newline='') as self.model_design_csv:
                writer = csv.writer(self.model_design_csv)
                writer.writerow([dp_index] + data_insert)
                
        # Pop up message that csv design file has been created
        tk.messagebox.showinfo("Information", "Design file " + self.design_csv_name + " has been created.")    
    
    
        # Display Design Values
        self.display_design_tree() 
        
        
        
            
    def update_defaults_button(self):
        
        # Get default user values
        self.fixed_factors = {}
        default_csv_insert = []
        
        # List of values entered by user
        self.default_values = [self.default_value.get() for self.default_value in self.default_values_list]
        factor_index = 0
        for factor in self.default_factor_list:
            self.factor_datatype = self.model_object.specifications[factor].get("datatype")
            current_def_val = self.default_values[factor_index]
            if self.factor_datatype == float:
                self.fixed_factors[factor] = float(current_def_val)
            
            elif self.factor_datatype == int:
                self.fixed_factors[factor] = int(current_def_val)
            
            if self.factor_datatype == list:
                self.fixed_factors[factor] = ast.literal_eval(current_def_val)
        
            elif self.factor_datatype == tuple:
           
                tuple_str = tuple(current_def_val[1:-1].split(","))
                self.fixed_factors[factor] = tuple(float(s) for s in tuple_str)
            
            default_csv_insert.append(self.fixed_factors[factor])    
            factor_index += 1
    
        
        self.display_design_tree()
        
        tk.messagebox.showinfo("Defaults Updated", "Defaults have been successfully updated.")   
        
    def run_experiment(self, *args):
        
        #Name of model used for default save file
        model_save_name = self.selected_model
        
        #Time stamp for file name
        timestamp = time.strftime("%Y%m%d%H%M%S")
        
        # Ask user for file save location
        save_path = filedialog.asksaveasfilename(initialfile = self.selected_model + "_datafarming_experiment_" + timestamp)
        
        
               
        # Specify the name of the model as it appears in directory.py
        model_name = self.model_object.name
        
        
       
        # factor_headers = [] 
        
        # for  factor in self.model_object.specifications:
        # # Specify the names of the model factors (in order) that will be varied.
        
        #     factor_headers.append(factor)

        # If creating the design, provide the name of a .txt file containing
        # the following:
        #    - one row corresponding to each model factor being varied
        #    - three columns:
        #         - first column: lower bound for factor value
        #         - second column: upper bound for factor value
        #         - third column: (integer) number of digits for discretizing values
        #                         (e.g., 0 corresponds to integral values for the factor)
        #factor_settings_filename = "model_factors"
        factor_settings_filename = None

        # OR, if the design has been created, provide the name of a .text file
        # containing the following:
        #    - one row corresponding to each design point
        #    - the number of columns equal to the number of factors being varied
        #    - each value in the table gives the value of the factor (col index)
        #      for the design point (row index)
        # E.g., design_filename = "model_factor_settings_design"
        #design_filename = None
        design_filename = "model_factors_design"

        # Specify a common number of replications to run of the model at each
        # design point.
        n_reps = int(self.rep_var.get())

        # Specify whether to use common random numbers across different versions
        # of the model.
        if self.crn_var.get() == 'Yes':
            crn_across_design_pts = True
        else:
            crn_across_design_pts = False

        # Specify filename for outputs.
        #output_filename = "test_experiment"
        output_filename = save_path

        # No code beyond this point needs to be edited.

        # Create DataFarmingExperiment object.
        myexperiment = DataFarmingExperiment(model_name=model_name,
                                             factor_settings_filename=factor_settings_filename,
                                             factor_headers=self.factor_headers,
                                             design_filename=design_filename,
                                             model_fixed_factors = self.fixed_factors
                                             )

        
        
        # Run replications and print results to file.
        myexperiment.run(n_reps=n_reps, crn_across_design_pts=crn_across_design_pts)
        myexperiment.print_to_csv(csv_filename=output_filename)
        
        # run confirmation message
        tk.messagebox.showinfo("Run Completed", f"Experiment Completed. Output file can be found at {output_filename}")  

            
   
    def include_factor(self, *args):

        self.check_values = [self.checkstate.get() for self.checkstate in self.checkstate_list]
        self.check_index = 0
        self.cat_index = 0
    
        # If checkbox to include in experiment checked, enable experiment option buttons
        for factor in self.model_object.specifications:
                  
            # Get current checksate values from include experiment column
            self.current_checkstate = self.check_values[self.check_index]
            # Cross check factor type
            self.factor_datatype = self.model_object.specifications[factor].get("datatype")
            self.factor_description = self.model_object.specifications[factor].get("description")
            self.factor_default = self.model_object.specifications[factor].get("default")
            
            # Disable / enable experiment option widgets depending on factor type
            if self.factor_datatype == float or self.factor_datatype == int:
                self.current_min_entry = self.min_widgets[factor]
                self.current_max_entry = self.max_widgets[factor]               
                
                             
                if self.current_checkstate == True:
                    self.current_min_entry.configure(state = 'normal')
                    self.current_max_entry.configure(state = 'normal')
                    
                elif self.current_checkstate == False:
                    #Empty current entries
                    self.current_min_entry.delete(0, tk.END)
                    self.current_max_entry.delete(0, tk.END)
                   
                    
                    self.current_min_entry.configure(state = 'disabled')
                    self.current_max_entry.configure(state = 'disabled')
                                      
            if self.factor_datatype == float:              
                self.current_dec_entry = self.dec_widgets[factor]
                
                if self.current_checkstate == True:
                    self.current_dec_entry.configure(state = 'normal')
                    
                elif self.current_checkstate == False:
                    self.current_dec_entry.delete(0, tk.END)
                    self.current_dec_entry.configure(state = 'disabled')
                    
            self.check_index += 1     
