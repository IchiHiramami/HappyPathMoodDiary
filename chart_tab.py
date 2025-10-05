from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk

from datetime import datetime

from typing import Any
from collections import defaultdict

from miscallaenousHelper import middle_Mood, get_dynamic_figsize, plot_mood_chart, shift_page, refresh
from data_loader import load_entries

def build_chart_tab(cTab: ttk.Frame):
    plotStatus = ttk.Frame(cTab)
    plotStatus.pack(fill="both", expand=True)

    state = {"center_date": datetime.today()}
    entries: defaultdict[str, list[dict[str, Any]]] = load_entries() #type: ignore

    if not entries:
        ttk.Label(plotStatus, text="Nothing to plot here! Enter something first at the logging tab!").pack(pady=10)
        return

    # Create figure and canvas
    plotSpace = Figure(dpi=100)
    canvas = FigureCanvasTkAgg(plotSpace, master=plotStatus)
    chartCanvas = canvas.get_tk_widget()
    chartCanvas.pack(fill="both", expand=True)

    figsize = get_dynamic_figsize(chartCanvas)
    plotSpace.set_size_inches(*figsize)
    chart: Axes = plotSpace.add_subplot(111)

    # Initial data
    averageMood = middle_Mood(entries, state["center_date"])
    calDate = list(averageMood.keys())
    score : list[float | int | None] = [averageMood[d] if averageMood[d] is not None else 0 for d in calDate]

    plot_mood_chart(entries ,canvas, plotStatus, chart, calDate, score)
    
    #--------------Bottom Row Buttons--------------------
    ttk.Button(cTab, text="⏮️ Prev", command=lambda: shift_page(
        entries = entries, 
        canvas = canvas, 
        plotStatus = plotStatus, 
        chart = chart, 
        state = state, 
        callerID = ('left', 'Plot')
    )).pack(side="left", padx=5)

    ttk.Button(cTab, text="⏭️ Next", command=lambda: shift_page(
        entries = entries, 
        canvas = canvas, 
        plotStatus = plotStatus, 
        chart = chart, 
        state = state, 
        callerID = ('right', 'Plot')
    )).pack(side="left", padx=5)
    
    ttk.Button(cTab, text = "Refresh", command = lambda : refresh(entries = entries, canvas = canvas, plotStatus = plotStatus, chart = chart, state = state)).pack(side="right", padx=5)

    toolBar = NavigationToolbar2Tk(canvas, cTab)
    toolBar.update()

