# Import other windows
import simopt.windows.plot as Plot
# Import files
from simopt.experiment_base import post_normalize
# Import tkinter library
import tkinter as tk
from tkinter import ttk
# Import other libraries
import ast

class Post_Normal():
    """
    Post-Normalization Page of the GUI

    Arguments
    ----------
    master : tk.Tk
        Tkinter window created from Experiment_Window.run_single_function
    myexperiment : object(Experiment)
        Experiment object created in Experiment_Window.run_single_function
    experiment_list : list
        List of experiment object arguments
    """
    def __init__(self, master, experiment_list, main_window, meta = False):
        self.post_norm_exp_list = experiment_list
        self.meta = meta
        self.main_window = main_window
        self.master = master
        self.optimal_var = tk.StringVar(master=self.master)
        self.initial_var = tk.StringVar(master=self.master)
        self.check_var = tk.IntVar(master=self.master)
        self.init_var = tk.StringVar(self.master)
        self.proxy_var = tk.StringVar(self.master)
        self.proxy_sol = tk.StringVar(self.master)

        self.all_solvers = []
        for solvers in self.post_norm_exp_list:
            if solvers.solver.name not in self.all_solvers:
                self.all_solvers.append(solvers.solver.name)

        #("my exp post pro ", experiment_list)
        self.selected = experiment_list

        self.frame = tk.Frame(self.master)
        top_lab = "Welcome to the Post-Normalization Page for " + self.post_norm_exp_list[0].problem.name + " \n with Solvers:"
        if self.post_norm_exp_list[0].problem.minmax[0] == 1:
            minmax = "max"
        else:
            minmax = "min"

        opt = "unknown"
        if self.post_norm_exp_list[0].problem.optimal_solution != None:
            if len(self.post_norm_exp_list[0].problem.optimal_solution) == 1:
                opt = str(self.post_norm_exp_list[0].problem.optimal_solution[0])
            else:
                opt = str(self.post_norm_exp_list[0].problem.optimal_solution)


        for solv in self.all_solvers:
            top_lab = top_lab + " " + solv

        self.title = tk.Label(master = self.master,
                                text = top_lab,
                                font = "Calibri 15 bold",
                                justify="center")
        initsol = self.post_norm_exp_list[0].problem.factors['initial_solution']
        if len(initsol) == 1:
            initsol = str(initsol[0])
        else:
            initsol = str(initsol)

        self.n_init_label = tk.Label(master = self.master,
                                text = "The Initial Solution, x\u2080, is " + initsol +".",
                                font = "Calibri 13",
                                wraplength = "400")

        self.n_opt_label = tk.Label(master = self.master,
                                text = "The Optimal Solution, x\u002A, is " + opt +  " for this " + minmax + "imization Problem. \nIf the Proxy Optimal Value or the Proxy Optimal Solution is unspecified, SimOpt uses the best Solution found in the selected Problem-Solver Pair experiments as the Proxy Optimal Solution.",
                                font = "Calibri 13",
                                wraplength = "600",
                                justify="left")

        self.n_optimal_label = tk.Label(master = self.master,
                                text = "Optimal Solution (optional):",
                                font = "Calibri 13",
                                wraplength = "250")
        self.n_proxy_val_label = tk.Label(master = self.master,
                                text = "Insert Proxy Optimal Value, f(x\u002A):",
                                font = "Calibri 13",
                                wraplength = "250")
        self.n_proxy_sol_label = tk.Label(master = self.master,
                                text = "Insert Proxy Optimal Solution, x\u002A:",
                                font = "Calibri 13",
                                wraplength = "250")


        # t = ["x","f(x)"]
        self.n_proxy_sol_entry = ttk.Entry(master=self.master, textvariable = self.proxy_sol, justify = tk.LEFT, width=8)
        self.n_proxy_val_entry = ttk.Entry(master=self.master, textvariable = self.proxy_var, justify = tk.LEFT, width=8)
        self.n_initial_entry = ttk.Entry(master=self.master, textvariable = self.init_var, justify = tk.LEFT, width=10)

        self.n_crn_label = tk.Label(master = self.master,
                                text = "CRN for x\u2080 and Optimal x\u002A?",
                                font = "Calibri 13",
                                wraplength = "310")
        self.n_crn_checkbox = tk.Checkbutton(self.master,text="",variable=self.check_var)


        self.n_postreps_init_opt_label = tk.Label(master = self.master,
                                text = "Number of Post-Normalizations at x\u2080 and x\u002A:",
                                font = "Calibri 13",
                                wraplength = "310")

        self.n_postreps_init_opt_var = tk.StringVar(self.master)
        self.n_postreps_init_opt_entry = ttk.Entry(master=self.master, textvariable = self.n_postreps_init_opt_var, justify = tk.LEFT, width=15)
        self.n_postreps_init_opt_entry.insert(index=tk.END, string="200")

        self.post_processing_run_label = tk.Label(master=self.master, # window label is used for
                        text = "Click to Post-Normalize the Problem-Solver Pairs",
                        font = "Calibri 13",
                        wraplength = "300")

        self.post_processing_run_button = ttk.Button(master=self.master, # window button is used in
                        # aesthetic of button and specific formatting options
                        text = "Post-Normalize",
                        width = 15, # width of button
                        command = self.post_norm_run_function) # if command=function(), it will only work once, so cannot call function, only specify which one, activated by left mouse click


        self.title.place(x=75, y=15)

        self.n_init_label.place(x=10, y=70)

        self.n_opt_label.place(x=10,y=90)

        # self.n_proxy_label.place(x=10, y=200)
        self.n_proxy_val_label.place(x=10,y=190)
        self.n_proxy_sol_label.place(x=325,y=190)
        self.n_proxy_val_entry.place(x=220, y=190)
        self.n_proxy_sol_entry.place(x=530, y=190)

        self.n_crn_label.place(x=10, y=230)
        self.n_crn_checkbox.place(x=325, y=230)
        #default to selected
        self.n_crn_checkbox.select()

        self.n_postreps_init_opt_label.place(x=10, y=270)
        self.n_postreps_init_opt_entry.place(x=325, y=270)


        self.post_processing_run_label.place(x=10, y=310)
        self.post_processing_run_button.place(x=325, y=310)

        self.frame.pack(side="top", fill="both", expand=True)

    def post_norm_run_function(self):

        self.experiment_list = []

        # if self.n_postreps_entry.get().isnumeric() != False and self.n_postreps_init_opt_entry.get().isnumeric() != False and self.crn_across_budget_var.get() in self.crn_across_budget_list and self.crn_across_macroreps_var.get() in self.crn_across_macroreps_list:
        if self.n_postreps_init_opt_entry.get().isnumeric() != False :
            n_postreps_init_opt = int(self.n_postreps_init_opt_entry.get())
            crn = self.check_var.get()
            proxy_val = None
            proxy_sol = None
            if self.proxy_sol.get() != "":
                proxy_sol = ast.literal_eval(self.proxy_sol.get())
            if self.proxy_var.get() != "":
                proxy_val = ast.literal_eval(self.proxy_var.get())
            post_normalize(self.post_norm_exp_list, n_postreps_init_opt, crn_across_init_opt=crn, proxy_init_val=None, proxy_opt_val=proxy_val, proxy_opt_x=proxy_sol)
            # self.master.destroy()
            self.post_processed_bool = True

            self.postrep_window = tk.Toplevel()
            self.postrep_window.geometry("1000x800")
            self.postrep_window.title("Plotting Page")
            self.master.destroy()
            Plot(self.postrep_window, self.main_window, experiment_list = self.post_norm_exp_list)

            return

        elif self.n_postreps_init_opt_entry.get().isnumeric() == False:
            message = "Please enter a valid value for the number of postreplications at each recommended solution."
            tk.messagebox.showerror(title="Error Window", message=message)

            self.n_postreps_entry.delete(0, len(self.n_postreps_entry.get()))
            self.n_postreps_entry.insert(index=tk.END, string="100")

    def test_function2(self, *args):
        print("connection enabled")
