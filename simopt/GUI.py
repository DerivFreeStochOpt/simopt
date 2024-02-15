# Import other windows
import simopt.windows.main_menu as window_main_menu
# Import tkinter library
import tkinter as tk
from tkinter import ttk

# sys.path.append(o.abspath(o.join(o.dirname(sys.modules[__name__].__file__), "..")))

def main():
    # Create the root window
    root = tk.Tk()
    # Set the style of the window
    style = ttk.Style()
    style.theme_use('clam')
    # Create the main menu window
    app = window_main_menu.Main_Menu(root)
    # Run the main loop
    root.mainloop()

if __name__ == '__main__':
    main()
