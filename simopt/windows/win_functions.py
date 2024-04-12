# import tkinter as tk
import tkinter as tk

# DEBUG flag
DEBUG = True

def on_canvas_configure(event, window):
    # Get the canvas size
    c_width = window.scrollable_canvas.winfo_width()

    # Get the frame size
    f_width = window.frame.winfo_width()

    # Get current canvas location
    x = window.scrollable_canvas.canvasx(0)
    y = window.scrollable_canvas.canvasy(0)

    new_x = x

    # If the frame is smaller than the canvas
    if c_width > f_width:
        new_x = c_width / 2 + x
    
    # Move the frame
    window.scrollable_canvas.coords(window.frame_id, new_x, y)

    window.scrollable_canvas.configure(scrollregion=window.scrollable_canvas.bbox("all"))

# Collection of useful functions for windows
def get_frame(window):
    # Create the outer frame
    # This just the main canvas/frame and scrollbars
    window.window_frame = tk.Frame(window.master)
    window.window_frame.pack(fill="both", expand=True)

    # Create and add the canvas
    if (DEBUG):
        window.scrollable_canvas = tk.Canvas(window.window_frame, bg="yellow")
    else:
        window.scrollable_canvas = tk.Canvas(window.window_frame)
    window.scrollable_canvas.grid(row=0, column=0, sticky="nsew")
    # Create and add the scrollbars
    window.vsb = tk.Scrollbar(window.window_frame, orient="vertical", command=window.scrollable_canvas.yview)
    window.scrollable_canvas.configure(yscrollcommand=window.vsb.set)
    window.vsb.grid(row=0, column=1, sticky="ns")

    window.hsb = tk.Scrollbar(window.window_frame, orient="horizontal", command=window.scrollable_canvas.xview)
    window.scrollable_canvas.configure(xscrollcommand=window.hsb.set)
    window.hsb.grid(row=1, column=0, sticky="ew")

    # At this point, the scrollbars aren't locked to the sides of the window
    # We need to add some weights to the rows and columns
    window.window_frame.grid_rowconfigure(0, weight=1)
    window.window_frame.grid_columnconfigure(0, weight=1)

    # Create a frame for the window
    if (DEBUG):
        window.frame = tk.Frame(window.scrollable_canvas, bg="blue")
    else:
        window.frame = tk.Frame(window.scrollable_canvas)
    window.frame_id = window.scrollable_canvas.create_window((0, 0), window=window.frame, anchor="center")

    # Bind the scrollbars to the canvas and frame
    window.scrollable_canvas.bind("<Configure>", lambda e: on_canvas_configure(e, window))
    window.frame.bind("<Configure>", lambda e: window.scrollable_canvas.configure(scrollregion=window.scrollable_canvas.bbox("all")))
