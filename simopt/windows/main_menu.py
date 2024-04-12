# Import other windows
import simopt.windows.experiment as window_experiment
import simopt.windows.data_farming as window_data_farming
import simopt.windows.solver_datafarming as window_solver_datafarming
import simopt.windows.win_functions as win_functions
# Import tkinter library
import tkinter as tk

class Main_Menu(tk.Toplevel):
    def __init__(self, master):
        self.master = master
        
        # Set size of window
        self.master.geometry("800x600")
        # Set min size of window
        self.master.minsize(800, 600)

        # Set title of window
        self.master.title("SimOpt Library Graphical User Interface - Main Menu")
        # Set window icon
        self.master.iconbitmap('logo/simopt.ico')

        # Get a frame (named self.frame) with scrollbars
        win_functions.get_frame(self)

        # Display the header text at the top of the window
        self.title_label = tk.Label(self.frame, text = "SimOpt Library Graphical User Interface", font = "Calibri 20 bold")
        self.title_label.grid(row = 0, column = 0, padx = 10, pady = 30)

        # Button to open original main window to run experiments across solvers & problems
        self.experiment_button = tk.Button(self.frame, text = 'Problem-Solver Experiment', font = "Calibri 13", width = 50, command = self.open_experiment_window)
        self.experiment_button.grid(row = 1, column = 0, padx = 10, pady = 10)
        
        # Button to open model data farming window
        self.datafarm_model_button = tk.Button(self.frame, text = 'Model Data Farming (beta)', font = "Calibri 13", width = 50, command = self.open_model_datafarming)
        self.datafarm_model_button.grid(row = 2, column = 0, padx = 10, pady = 10)
    
    def open_experiment_window(self):
        # Launch the experiment window
        self.experiment_window = tk.Toplevel(self.master)
        self.experiment_app = window_experiment.Experiment(self.experiment_window)
        # Hide the main menu
        self.master.withdraw()
        # Wait for the experiment window to close
        self.master.wait_window(self.experiment_window)
        # Unhide the main menu
        self.master.deiconify()
    
    def open_model_datafarming(self):
        # Launch the data farming window
        self.datafarming_window = tk.Toplevel(self.master)
        self.datafarming_app = window_data_farming.Data_Farming(self.datafarming_window, self)
        # Hide the main menu
        self.master.withdraw()
        # Wait for the data farming window to close
        self.master.wait_window(self.datafarming_window)
        # Unhide the main menu
        self.master.deiconify()

    def open_prob_sol_datafarming(self):
        # Launch the solver data farming window
        self.solver_datafarming_window = tk.Toplevel(self.master)
        self.solver_datafarm_app = window_solver_datafarming.Solver_Datafarming(self.solver_datafarming_window)
        # Hide the main menu
        self.master.withdraw()
        # Wait for the solver data farming window to close
        self.master.wait_window(self.solver_datafarming_window)
        # Unhide the main menu
        self.master.deiconify()
