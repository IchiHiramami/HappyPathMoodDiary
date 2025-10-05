from tkinter import ttk, Canvas, Event
from miscallaenousHelper import render_entries

def build_entries_tab(tab_entries: ttk.Frame):
    """
    Build out the entry list tab of the app inside of a Frame. Starts by creating a container inside of a canvas in the parent widget
    """
    # basically create a frame inside canvas inside tab_entries to make a scrollable frame inside canvas
    canvas = Canvas(tab_entries) 
    canvas.place(relx = 0, rely = 0, relwidth = 0.98, relheight = 0.8)

    scrollbar = ttk.Scrollbar(tab_entries, orient = 'vertical', command = canvas.yview)  # type: ignore , scrollbar is part of tab_entries
    container : ttk.Frame = ttk.Frame(canvas)                                            # container is a frame inside canvas
    container.bind('<Configure>', lambda e: canvas.config(scrollregion = canvas.bbox('all')))  # bind container to canvas
    
    def resize_container(event : Event):
        canvas.itemconfig(container_window, width=event.width) # container will adjust to the size of canvas

    def on_mouse_wheel(event : Event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    container_window = canvas.create_window((0, 0), window=container, anchor='nw')
    canvas.bind("<Configure>", resize_container)
    canvas.bind("<MouseWheel>", on_mouse_wheel)

    canvas.config(yscrollcommand = scrollbar.set)
    scrollbar.place(relx = 0.98, rely = 0, relheight = 0.9)

    ttk.Button(tab_entries, text="🔄 Refresh Entries", command=lambda c = container: render_entries(c)).place(rely = 0.9, relx = 0.5, anchor = 'center')

    render_entries(container)
