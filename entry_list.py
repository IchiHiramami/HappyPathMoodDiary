from tkinter import ttk, Canvas, Event

from miscallaenousHelper import render_entries, notANestedCallback

def resize_container(event: Event, canvas: Canvas, container_window: int):
    canvas.itemconfig(container_window, width = event.width)

def build_entries_tab(tab_entries: ttk.Frame):
    """
    Build out the entry list tab of the app inside of a Frame. Starts by creating a container inside of a canvas in the parent widget
    """
    # basically create a frame inside canvas inside tab_entries to make a scrollable frame inside canvas
    canvas = Canvas(tab_entries) 
    canvas.place(relx = 0, rely = 0, relwidth = 0.98, relheight = 0.8)

    scrollbar = ttk.Scrollbar(tab_entries, orient = 'vertical', command = canvas.yview) #type: ignore
    container: ttk.Frame = ttk.Frame(canvas)
    container.bind('<Configure>', lambda e: canvas.config(scrollregion = canvas.bbox('all')))

    container_window = canvas.create_window((0, 0), window = container, anchor = 'nw')

    canvas.bind("<Configure>", lambda e: resize_container(e, canvas, container_window))

    canvas.config(yscrollcommand = scrollbar.set)
    scrollbar.place(relx = 0.98, rely = 0, relheight = 0.9)

    ttk.Button(tab_entries, text = "Refresh Entries", command = notANestedCallback([(render_entries, [container], {})])).place(rely = 0.9, relx = 0.5, anchor = 'center')

    render_entries(container)
