# Import time
import time

from scipy.stats import linregress

# Import tkinter library
import tkinter as tk
from tkinter import ttk

class Status_Window(tk.Toplevel):
    def __init__(self, n_macroreps):
        self.n_macroreps = n_macroreps
        self.status_window = tk.Toplevel()
        self.status_window.title("Status")
        self.status_window.geometry("400x100")
        self.status_window.resizable(False, False)

        # Set the window to be in the center of the screen
        self.status_window.withdraw()
        self.status_window.update_idletasks()
        x = (self.status_window.winfo_screenwidth() - self.status_window.winfo_reqwidth()) / 2
        y = (self.status_window.winfo_screenheight() - self.status_window.winfo_reqheight()) / 2
        self.status_window.geometry("+%d+%d" % (x, y))
        self.status_window.deiconify()

        # Set the window to be the topmost window
        self.status_window.attributes("-topmost", True)
        self.status_window.update()

        # Create a grid to hold the widgets
        self.status_window.grid_rowconfigure(0, weight=1)
        self.status_window.grid_rowconfigure(1, weight=1)
        self.status_window.grid_rowconfigure(2, weight=1)
        self.status_window.grid_columnconfigure(0, weight=1)
        
        # Set the progress bar to be at 0
        self.progress = tk.IntVar()
        self.progress.set(0)

        # Create a style for the progress bar
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TProgressbar", foreground="green", background="green")

        # Create a progress bar
        self.progress_bar = ttk.Progressbar(
            self.status_window,
            orient="horizontal",
            mode="determinate",
            maximum=self.n_macroreps,
            variable=self.progress,
            style="TProgressbar")
        self.progress_bar.grid(row=2, column=0, padx=20, sticky="ew")

        # Add a label for time elapsed
        self.time_elapsed_label = tk.Label(self.status_window, text="Time Elapsed: 0.0 seconds")
        self.time_elapsed_label.grid(row=1, column=0, padx=20, sticky="w")
        
        # Add a label for time remaining
        self.time_remaining_label = tk.Label(self.status_window, text="Time Remaining: calculating...")
        self.time_remaining_label.grid(row=0, column=0, padx=20, sticky="w")

        # Set the time the window was opened
        self.window_open_time = time.time()

    def on_closing(self):
        self.status_window.destroy()

    def update_time_elapsed(self):
        # If the window is closed, don't update the time elapsed
        if self.status_window.winfo_exists() == 0:
            return
        # Update the time elapsed
        time_elapsed = time.time() - self.window_open_time
        self.time_elapsed_label.config(text=f"Time Elapsed: {time_elapsed:.0f} seconds")

    def update_progress(self, macroreps_completed):
        # If the window is closed, don't update the progress bar
        if self.status_window.winfo_exists() == 0:
            return
        self.update_time_elapsed()
        # If the macroreps_completed is equal to the number of macroreps, then close the window
        if macroreps_completed == self.progress_bar["maximum"]:
            self.status_window.destroy()
        else:
            # Otherwise, update the progress bar
            self.progress.set(macroreps_completed)
            self.progress_bar.update()
        
    def update_time_remaining(self, timing_dict):
        # If the window is closed, don't update the time remaining
        if self.status_window.winfo_exists() == 0:
            return
        self.update_time_elapsed()
        # If there is only one time recorded, don't update the time remaining
        if (len(timing_dict) < 2):
            return
        # Copy the dictionary
        time_dict = timing_dict.copy()
        # Extract the keys and values from the dictionary
        keys = list(time_dict.keys())
        values = list(time_dict.values())
        # Use linear regression to estimate the time remaining
        slope, intercept, r_value, p_value, std_err = linregress(keys, values)
        estimated_time_of_last_mrep = slope * self.n_macroreps + intercept + self.window_open_time
        time_remaining = estimated_time_of_last_mrep - time.time()
        # Prevent it from printing negative numbers (that can't be right)
        if time_remaining < 0:
            time_remaining = 0

        # Update the label
        self.time_remaining_label.config(text=f"Time Remaining: {time_remaining:.0f} seconds")