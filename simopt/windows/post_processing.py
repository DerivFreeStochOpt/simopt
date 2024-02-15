# Import other windows
import simopt.windows.experiment as window_experiment
# Import tkinter library
import tkinter as tk
from tkinter import ttk

class Post_Processing():
    """
    Postprocessing Page of the GUI

    Arguments
    ----------
    master : tk.Tk
        Tkinter window created from Experiment_Window.run_single_function
    myexperiment : object(Experiment)
        Experiment object created in Experiment_Window.run_single_function
    experiment_list : list
        List of experiment object arguments
    """
    def __init__(self, master, myexperiment, experiment_list, main_window, meta = False):

        self.meta = meta
        self.main_window = main_window
        self.master = master
        self.my_experiment = myexperiment
        #("my exp post pro ", experiment_list)
        self.selected = experiment_list

        self.frame = tk.Frame(self.master)

        self.title = tk.Label(master = self.master,
                                text = "Welcome to the Post-Processing Page",
                                font = "Calibri 15 bold",justify="center")
        if self.meta:
            self.title = tk.Label(master = self.master,
                                text = "Welcome to the Post-Processing \nand Post-Normalization Page",
                                font = "Calibri 15 bold",justify="center")

        self.n_postreps_label = tk.Label(master = self.master,
                                    text = "Number of Postreplications at each Recommended Solution:",
                                    font = "Calibri 13",
                                    wraplength = "250")

        self.n_postreps_var = tk.StringVar(self.master)
        self.n_postreps_entry = ttk.Entry(master=self.master, textvariable = self.n_postreps_var, justify = tk.LEFT, width=15)
        self.n_postreps_entry.insert(index=tk.END, string="100")


        self.crn_across_budget_label = tk.Label(master=self.master,
                                    text = "Use CRN for Postreplications at Solutions Recommended at Different Times?",
                                    font = "Calibri 13",
                                    wraplength = "250")

        self.crn_across_budget_list = ["True", "False"]
        # stays the same, has to change into a special type of variable via tkinter function
        self.crn_across_budget_var = tk.StringVar(self.master)
        # sets the default OptionMenu selection
        # self.crn_across_budget_var.set("True")
        # creates drop down menu, for tkinter, it is called "OptionMenu"
        self.crn_across_budget_menu = ttk.OptionMenu(self.master, self.crn_across_budget_var, "True", *self.crn_across_budget_list)

        self.crn_across_macroreps_label = tk.Label(master=self.master,
                                        text = "Use CRN for Postreplications at Solutions Recommended on Different Macroreplications?",
                                        font = "Calibri 13",
                                        wraplength = "325")

        self.crn_across_macroreps_list = ["True", "False"]
        # stays the same, has to change into a special type of variable via tkinter function
        self.crn_across_macroreps_var = tk.StringVar(self.master)

        self.crn_across_macroreps_menu = ttk.OptionMenu(self.master, self.crn_across_macroreps_var, "False", *self.crn_across_macroreps_list)

        self.crn_norm_budget_label = tk.Label(master=self.master,
                                    text = "Use CRN for Postreplications at x\u2080 and x\u002A?",
                                    font = "Calibri 13",
                                    wraplength = "325")
        self.crn_norm_across_macroreps_var = tk.StringVar(self.master)
        self.crn_norm_across_macroreps_menu = ttk.OptionMenu(self.master, self.crn_norm_across_macroreps_var, "True", *self.crn_across_macroreps_list)

        self.n_norm_label = tk.Label(master = self.master,
                                    text = "Post-Normalization Parameters",
                                    font = "Calibri 14 bold",
                                    wraplength = "300")

        self.n_proc_label = tk.Label(master = self.master,
                                    text = "Post-Processing Parameters",
                                    font = "Calibri 14 bold",
                                    wraplength = "300")

        self.n_norm_ostreps_label = tk.Label(master = self.master,
                                    text = "Number of Postreplications at x\u2080 and x\u002A:",
                                    font = "Calibri 13",
                                    wraplength = "300")

        self.n_norm_postreps_var = tk.StringVar(self.master)
        self.n_norm_postreps_entry = ttk.Entry(master=self.master, textvariable = self.n_norm_postreps_var, justify = tk.LEFT, width=15)
        self.n_norm_postreps_entry.insert(index=tk.END, string="200")

        self.post_processing_run_label = tk.Label(master=self.master, # window label is used for
                        text = "Complete Post-Processing of the Problem-Solver Pairs:",
                        font = "Calibri 13",
                        wraplength = "250")

        if self.meta:
            self.post_processing_run_label = tk.Label(master=self.master, # window label is used for
                            text = "Complete Post-Processing and Post-Normalization of the Problem-Solver Pair(s)",
                            font = "Calibri 13",
                            wraplength = "300")

        self.post_processing_run_button = ttk.Button(master=self.master, # window button is used in
                        # aesthetic of button and specific formatting options
                        text = "Post-Process",
                        width = 15, # width of button
                        command = self.post_processing_run_function) # if command=function(), it will only work once, so cannot call function, only specify which one, activated by left mouse click


        self.title.place(x=145, y=15)

        if not self.meta:
            self.n_postreps_label.place(x=10, y=55)
            self.n_postreps_entry.place(x=300, y=55)

            self.crn_across_budget_label.place(x=10, y=105)
            self.crn_across_budget_menu.place(x=345, y=105)

            self.crn_across_macroreps_label.place(x=10, y=160)
            self.crn_across_macroreps_menu.place(x=345, y=160)

            self.post_processing_run_label.place(x=10, y=233)
            self.post_processing_run_button.place(x=310, y=237)
        else:
            self.n_proc_label.place(x=15, y=65)

            self.n_postreps_label.place(x=10, y=105)
            self.n_postreps_entry.place(x=300, y=105)

            self.crn_across_budget_label.place(x=10, y=155)
            self.crn_across_budget_menu.place(x=300, y=155)

            self.crn_across_macroreps_label.place(x=10, y=205)
            self.crn_across_macroreps_menu.place(x=300, y=205)

            self.n_norm_label.place(x=15, y=265)

            self.crn_norm_budget_label.place(x=10,y=305)
            self.crn_norm_across_macroreps_menu.place(x=300,y=305)

            self.n_norm_ostreps_label.place(x=10, y=355)
            self.n_norm_postreps_entry.place(x=300,y=355)

            self.post_processing_run_label.place(x=10, y=405)
            self.post_processing_run_button.place(x=300, y=405)

        self.frame.pack(side="top", fill="both", expand=True)
        self.run_all = all

    def post_processing_run_function(self):

        self.experiment_list = []
        # self.experiment_list = [self.selected[3], self.selected[4], self.selected[2]]

        # if self.n_postreps_entry.get().isnumeric() != False and self.n_postreps_init_opt_entry.get().isnumeric() != False and self.crn_across_budget_var.get() in self.crn_across_budget_list and self.crn_across_macroreps_var.get() in self.crn_across_macroreps_list:
        if self.n_postreps_entry.get().isnumeric() != False and self.crn_across_budget_var.get() in self.crn_across_budget_list and self.crn_across_macroreps_var.get() in self.crn_across_macroreps_list and (self.meta == True and self.n_norm_postreps_entry.get().isnumeric() or self.meta == False):
            self.experiment_list.append(int(self.n_postreps_entry.get()))
            # self.experiment_list.append(int(self.n_postreps_init_opt_entry.get()))

            # actually adding a boolean value to the list instead of a string
            if self.crn_across_budget_var.get()=="True":
                self.experiment_list.append(True)
            else:
                self.experiment_list.append(False)

            if self.crn_across_macroreps_var.get()=="True":
                self.experiment_list.append(True)
            else:
                self.experiment_list.append(False)

            norm = False
            if self.crn_norm_across_macroreps_var.get() == "True":
                norm = True
            # reset n_postreps_entry
            self.n_postreps_entry.delete(0, len(self.n_postreps_entry.get()))
            self.n_postreps_entry.insert(index=tk.END, string="100")

            # reset crn_across_budget_bar
            self.crn_across_budget_var.set("True")

            # reset crn_across_macroreps_var
            self.crn_across_macroreps_var.set("False")

            self.n_postreps = self.experiment_list[0] # int
            # print("self.n_prostreps", type(self.n_postreps))
            # self.n_postreps_init_opt = self.experiment_list[4] # int
            self.crn_across_budget = self.experiment_list[1] # boolean
            # print("self.n_prostreps", type(self.n_postreps))
            self.crn_across_macroreps = self.experiment_list[2] # boolean

            # print("This is the experiment object", self.my_experiment)
            # print("This is the problem name: ", self.my_experiment.problem.name)
            # print("This is the solver name: ", self.my_experiment.solver.name)
            # print("This is the experiment list", self.selected)
            # print ("This is experiment_list ", self.experiment_list)
            # self, n_postreps, crn_across_budget=True, crn_across_macroreps=False
            self.my_experiment.post_replicate(self.n_postreps, self.crn_across_budget, self.crn_across_macroreps)

            if self.meta:
                self.my_experiment.post_normalize(n_postreps_init_opt=int(self.n_norm_postreps_entry.get()), crn_across_init_opt=norm)

            #(self.experiment_list)
            self.master.destroy()
            self.post_processed_bool = True
            window_experiment.Experiment.post_process_disable_button(self.main_window,self.meta)



            return self.experiment_list

        elif self.n_postreps_entry.get().isnumeric() == False:
            message = "Please enter a valid value for the number of postreplications at each recommended solution."
            tk.messagebox.showerror(title="Error Window", message=message)

            self.n_postreps_entry.delete(0, len(self.n_postreps_entry.get()))
            self.n_postreps_entry.insert(index=tk.END, string="100")

        elif self.crn_across_macroreps_var.get() not in self.crn_across_macroreps_list:
            message = "Please answer the following question: 'Use CRN for postreplications at Solutions Recommended at Different Times?' with True or False."
            tk.messagebox.showerror(title="Error Window", message=message)

            self.crn_across_budget_var.set("----")

        elif self.crn_across_budget_var.get() not in self.crn_across_budget_list:
            message = "Please answer the following question: 'Use CRN for Postreplications at Solutions Recommended on Different Macroreplications?' with True or False."
            tk.messagebox.showerror(title="Error Window", message=message)

            self.crn_across_macroreps_var.set("----")

        else:
            message = "You have not selected all required field! Check for '*' signs near required input boxes."
            tk.messagebox.showerror(title="Error Window", message=message)

            self.n_postreps_init_opt_entry.delete(0, len(self.n_postreps_init_opt_entry.get()))
            self.n_postreps_init_opt_entry.insert(index=tk.END, string="6")

            self.crn_across_budget_var.set("True")

            self.crn_across_macroreps_var.set("False")

    def test_function2(self, *args):
        print("connection enabled")