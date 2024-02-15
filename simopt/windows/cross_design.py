# Import other windows
import simopt.windows.experiment as window_experiment
# Import files
from simopt.directory import problem_directory, problem_unabbreviated_directory, solver_directory, solver_unabbreviated_directory
from simopt.experiment_base import ProblemsSolvers
# Import tkinter library
import tkinter as tk
from tkinter import ttk

class Cross_Design():
    def __init__(self, master, main_widow, forced_creation = False):
        if not forced_creation:
            self.master = master
            self.main_window = main_widow

            self.crossdesign_title_label = tk.Label(master=self.master,
                                                    text = "Create Cross-Design Problem-Solver Group",
                                                    font = "Calibri 13 bold")
            self.crossdesign_title_label.place(x=10, y=25)

            self.crossdesign_problem_label = tk.Label(master=self.master,
                                                        text = "Select Problems:",
                                                        font = "Calibri 13")
            self.crossdesign_problem_label.place(x=190, y=55)

            self.crossdesign_solver_label = tk.Label(master=self.master,
                                                        text = "Select Solvers:",
                                                        font = "Calibri 13")
            self.crossdesign_solver_label.place(x=10, y=55)

            self.crossdesign_checkbox_problem_list = []
            self.crossdesign_checkbox_problem_names = []
            self.crossdesign_checkbox_solver_list = []
            self.crossdesign_checkbox_solver_names = []

            solver_cnt = 0
            
            for solver in solver_unabbreviated_directory:
                self.crossdesign_solver_checkbox_var = tk.BooleanVar(self.master, value=False)
                self.crossdesign_solver_checkbox = tk.Checkbutton(master=self.master,
                                                                text = solver,
                                                                variable = self.crossdesign_solver_checkbox_var)
                self.crossdesign_solver_checkbox.place(x=10, y=85+(25*solver_cnt))

                self.crossdesign_checkbox_solver_list.append(self.crossdesign_solver_checkbox_var)
                self.crossdesign_checkbox_solver_names.append(solver)

                solver_cnt += 1

            problem_cnt = 0
            for problem in problem_unabbreviated_directory:
                self.crossdesign_problem_checkbox_var = tk.BooleanVar(self.master, value=False)
                self.crossdesign_problem_checkbox = tk.Checkbutton(master=self.master,
                                                    text = problem,
                                                    variable = self.crossdesign_problem_checkbox_var)
                self.crossdesign_problem_checkbox.place(x=190, y=85+(25*problem_cnt))

                self.crossdesign_checkbox_problem_list.append(self.crossdesign_problem_checkbox_var)
                self.crossdesign_checkbox_problem_names.append(problem)

                problem_cnt += 1

            

            if problem_cnt < solver_cnt:
                solver_cnt += 1
                self.crossdesign_macro_label = tk.Label(master=self.master,
                                                        text = "Number of Macroreplications:",
                                                        font = "Calibri 13")
                self.crossdesign_macro_label.place(x=15, y=80+(25*problem_cnt))

                self.crossdesign_macro_var = tk.StringVar(self.master)
                self.crossdesign_macro_entry = ttk.Entry(master=self.master, textvariable = self.crossdesign_macro_var, justify = tk.LEFT, width=15)
                self.crossdesign_macro_entry.insert(index=tk.END, string="10")
                self.crossdesign_macro_entry.place(x=15, y=105+(25*solver_cnt))

                self.crossdesign_button = ttk.Button(master=self.master,
                                                text = "Add Cross-Design Problem-Solver Group",
                                                width = 65,
                                                command = self.confirm_cross_design_function)
                self.crossdesign_button.place(x=15, y=135+(25*solver_cnt))

            if problem_cnt > solver_cnt:
                problem_cnt += 1

                self.crossdesign_macro_label = tk.Label(master=self.master,
                                                        text = "Number of Macroreplications:",
                                                        font = "Calibri 13")
                self.crossdesign_macro_label.place(x=15, y=80+(25*problem_cnt))

                self.crossdesign_macro_var = tk.StringVar(self.master)
                self.crossdesign_macro_entry = ttk.Entry(master=self.master, textvariable = self.crossdesign_macro_var, justify = tk.LEFT, width=15)
                self.crossdesign_macro_entry.insert(index=tk.END, string="10")

                self.crossdesign_macro_entry.place(x=15, y=105+(25*problem_cnt))

                self.crossdesign_button = ttk.Button(master=self.master,
                                                text = "Add Cross-Design Problem-Solver Group",
                                                width = 45,
                                                command = self.confirm_cross_design_function)
                self.crossdesign_button.place(x=15, y=135+(25*problem_cnt))

            if problem_cnt == solver_cnt:
                problem_cnt += 1

                self.crossdesign_macro_label = tk.Label(master=self.master,
                                                        text = "Number of Macroreplications:",
                                                        font = "Calibri 13")
                self.crossdesign_macro_label.place(x=15, y=80+(25*problem_cnt))

                self.crossdesign_macro_var = tk.StringVar(self.master)
                self.crossdesign_macro_entry = ttk.Entry(master=self.master, textvariable = self.crossdesign_macro_var, justify = tk.LEFT, width=15)
                self.crossdesign_macro_entry.insert(index=tk.END, string="10")
                self.crossdesign_macro_entry.place(x=15, y=105+(25*problem_cnt))

                self.crossdesign_button = ttk.Button(master=self.master,
                                                text = "Add Cross-Design Problem-Solver Group",
                                                width = 30,
                                                command = self.confirm_cross_design_function)
                self.crossdesign_button.place(x=15, y=135+(25*problem_cnt))
            else:
                # print("forced creation of cross design window class")
                pass

    def confirm_cross_design_function(self):
        solver_names_list = list(solver_directory.keys())
        problem_names_list = list(problem_directory.keys())
        problem_list = []
        solver_list = []

        for checkbox in self.crossdesign_checkbox_solver_list:
            if checkbox.get() == True:
                #(self.crossdesign_checkbox_solver_names[self.crossdesign_checkbox_solver_list.index(checkbox)] + " was selected (solver)")
                #solver_list.append(solver_directory[self.crossdesign_checkbox_solver_names[self.crossdesign_checkbox_solver_list.index(checkbox)]])
                solver_list.append(solver_names_list[self.crossdesign_checkbox_solver_list.index(checkbox)])
                
        for checkbox in self.crossdesign_checkbox_problem_list:
            if checkbox.get() == True:
                #(self.crossdesign_checkbox_problem_names[self.crossdesign_checkbox_problem_list.index(checkbox)] + " was selected (problem)")
                #problem_list.append(problem_directory[self.crossdesign_checkbox_problem_names[self.crossdesign_checkbox_problem_list.index(checkbox)]])
                problem_list.append(problem_names_list[self.crossdesign_checkbox_problem_list.index(checkbox)])

        

        # Solver can handle upto deterministic constraints, but problem has stochastic constraints.
        stochastic = ["FACSIZE-1","FACSIZE-2","RMITD-1"]
        if len(solver_list) == 0 or len(problem_list) == 0:
            self.crossdesign_warning = tk.Label(master=self.master,
                                                text = "Select at least one solver and one problem",
                                                font = "Calibri 13 bold",
                                                wraplength=300)
            self.crossdesign_warning.place(x=10, y=345)
            return

        if "ASTRODF" in solver_list and any(item in stochastic for item in problem_list) :
            self.crossdesign_warning = tk.Label(master=self.master,
                                                text = "ASTRODF can handle upto deterministic constraints, but problem has stochastic constraints",
                                                font = "Calibri 13 bold",
                                                wraplength=300)
            self.crossdesign_warning.place(x=10, y=345)
            return
        # macro_reps = self.crossdesign_macro_var.get()
        #(solver_list, problem_list)
        # self.crossdesign_ProblemsSolvers = ProblemsSolvers(solver_names=solver_list, problem_names=problem_list, fixed_factors_filename="all_factors")
        self.crossdesign_MetaExperiment = ProblemsSolvers(solver_names=solver_list, problem_names=problem_list)

        # if self.count_meta_experiment_queue == 0:
        #     self.create_meta_exp_frame()
        self.master.destroy()
        window_experiment.Experiment.add_meta_exp_to_frame(self.main_window, self.crossdesign_macro_var)

        return self.crossdesign_MetaExperiment

        #(self.crossdesign_MetaExperiment)

    def test_function(self, *args):
        # print("test function connected")
        pass

    def get_crossdesign_MetaExperiment(self):
        return self.crossdesign_MetaExperiment
