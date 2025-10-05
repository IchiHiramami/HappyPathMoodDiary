import csv
from tkinter import Text
from tkinter import ttk, StringVar, Entry, Text, Canvas
from collections import defaultdict
from typing import Any
from data_loader import load_entries, delete_entry #type: ignore
from datetime import datetime, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.axes import Axes
from collections.abc import Callable

# for entry list color coding and emoji display
mdcolor : dict[int, tuple[str,str]] = {
    1 : ("#dd3a3a", "😄"),
    2 : ("#e0b049", "🙂"),
    3 : ("#E3EC60", "😐"),
    4 : ("#A6F051", "😟"),
    5 : ("#3BD64F", "😭"),
}

# for entry logging
MoodMap : dict[str,int] = { 
    "😄": 5,
    "🙂": 4, 
    "😐": 3, 
    "😟": 2, 
    "😭": 1
}

pointOfReferenceDate : datetime = datetime.today()

def overwrite_entry(date: str, target_index: int, mood: int, jText: Text):
    """
    Updates entries already in mood_data.csv. Entries are identifable by its date and the index (in case of similarities of date)
    """
    journal :str = jText.get('0.1','end-1c')
    with open("mood_data.csv", "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        entries = list(reader)

    checkedEntries = 0
    for _, row in enumerate(entries):
        if row["date"] == date:
            if checkedEntries == target_index:
                row["mood"] = str(mood)
                row["journal"] = journal
                break
            checkedEntries += 1

    with open("mood_data.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["date", "mood", "journal"])
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerows(entries)

def render_entries(container : ttk.Frame):
    """
    Renders the entries tab, callable via lambda (button) or direct approach
    """
    style = ttk.Style() 
    
    for widget in container.winfo_children():
        widget.destroy()

    #sample data: [{'mood': 2, 'journal': 'Felt anxious in the morning'}]
    entries: defaultdict[str, list[dict[str, Any]]] = load_entries() # type: ignore
    if not entries:
        ttk.Label(container, text="No entries found.").pack(pady=10)
        return

    date : str
    for date in entries.keys():
        ttk.Label(container, text=f"📅 {date}", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        for i, entry in enumerate(entries[date]):
            mood = entry["mood"]
            journal = str(entry["journal"])

            displayEntryFrame = ttk.Frame(container, padding=5)
            displayEntryFrame.pack(fill="x", padx=20, pady=2)

            mood_int = entry.get("mood", 1)
            x = mdcolor.get(mood_int, "#f0f0f0")
            bg_color = x[0]
            memoji = x[1]

            displayEntryFrame.config(style=f"Mood{mood_int}.TFrame")
            style.configure(f"Mood{mood_int}.TFrame", background=bg_color) #type: ignore

            jMoodvar = StringVar(value = mood)
            jMoodentry = Entry(displayEntryFrame, textvariable = jMoodvar, width = 5)
            jMoodentry.pack(side = 'left')

            jMoodEmoji = StringVar(value = memoji)
            jMoodLabel = Entry(displayEntryFrame, textvariable = jMoodEmoji, width = 5)
            jMoodLabel.pack(side = 'left')

            jtext = Text(displayEntryFrame, height = 4, wrap = "word", width = 40)
            jtext.insert("1.0", journal) # .insert takes (text (index format: (y.x)), target)
            jtext.pack(side = 'left', fill = 'x', expand = True)

            def call_delete_entry(d : str =date, idx : int =i):
                return lambda: (
                    delete_entry(d, idx),
                    render_entries(container)
                )

            ttk.Button(displayEntryFrame, text="🗑️ Delete", command=call_delete_entry()).pack(side='right', padx=5)
            ttk.Button(displayEntryFrame, text = "Update Changes", command = lambda date = date, tindex = i, mood = mood, jText = jtext: overwrite_entry(date, tindex, mood, jText)).pack(side = 'right', padx = 5)

def calendarcreator(
        parent : ttk.Frame, 
        selDate : StringVar, 
        function : Callable[[datetime], None],
        ):
    
    """
    Builds out the custom calendar for the logging Tab. Destroys all widgets (if any) before redrawing. Creates a Frame wherein a 4 rows x 7 column grid is displayed. Each calendar cell is its own individual Frame
    """
    for wid in parent.winfo_children():
        wid.destroy()

    global pointOfReferenceDate
    PORdate = pointOfReferenceDate

    ttk.Label(parent, text="Select Date:").pack(pady=5)

    selDateLabel = ttk.Label(parent, textvariable = selDate)
    selDateLabel.pack(pady = 5)

    calendarContainer = ttk.Frame(parent, borderwidth=2, relief="ridge", padding=10)
    calendarContainer.pack(pady=10, fill="both", expand = True)
    
    rows, columns = 4, 7
    relXPos, relYPos = 1 / columns, 1 / rows
    """
    for i in range(columns):
        day_date = PORdate + timedelta(i)
        dayOfTheWeek = day_date.strftime("%A")
        ttk.Label(calendarContainer, text = dayOfTheWeek, padding = 5, relief = "groove", borderwidth = 2).place(
                relx=(i + 0.5) * relXPos,
                relwidth=relXPos,
                relheight= 0.05,
                anchor="center"
        )"""

    for j in range(rows):
        for i in range(columns):
            day_date : datetime = PORdate + timedelta(days = i + j * columns)
            cellLabel = day_date.strftime("%B %d, %Y")

            dateContainer = ttk.Frame(calendarContainer, padding=5, relief="groove", borderwidth = 2) #relief -> visual border style
            dateContainer.place(
                relx=(i + 0.5) * relXPos,
                rely=(j + 0.5) * relYPos,
                relwidth=relXPos,
                relheight= 0.1 + relYPos,
                anchor="center"
            )
            ttk.Label(dateContainer, text = cellLabel, justify = 'center').pack()
            ttk.Button(dateContainer, text="Select", command=lambda d=day_date: function(d)).pack()

def middle_Mood(entries: defaultdict[str, list[dict[str, Any]]], cD: datetime):# type: ignore
    avgScore : dict[str, float | None] = {}
    for delta in range(-4,3):
        x = (cD + timedelta(days = delta)).strftime("%Y-%m-%d")
        y : list[int] = []
        for row in entries.get(x, []):
            raw_mood = row.get("mood", "")
            moodInt = int(raw_mood)
            y.append(moodInt)

        avgScore[x] = sum(y) / len(y) if y else None

    return avgScore

def get_dynamic_figsize(widget : Canvas, dpi : int = 100) -> tuple[float, float]:
    width_px : float = widget.winfo_width()
    height_px  : float = widget.winfo_height()
    width_in  : float = max(width_px / dpi, 4)   # clamp to minimum size
    height_in  : float = max(height_px / dpi, 2)
    return (width_in, height_in)

def plot_mood_chart(
        
        entries : Any ,
        canvas : FigureCanvasTkAgg ,
        plotStatus : ttk.Frame, 
        chart : Axes, 
        calDate : list[str], 
        score : list[ float | int | None]
        
    ):
    """
    Sets up the plot using matplotlib. Uses Dates as x-axis. Y axis is restricted from y = 0 to y = 5. 
    """
    if not entries:
        ttk.Label(plotStatus, text="Nothing to plot here! Enter something first at the logging tab!").pack(pady=10)
        return

    chart.clear()
    chart.plot(calDate, score, marker="o")                                                   #type: ignore
    chart.set_title("Average Mood")                                                          #type: ignore
    chart.set_ylabel("Mood Score")                                                           #type: ignore
    chart.set_ylim(0,5)                                                                      #type: ignore
    chart.grid(True)                                                                         #type: ignore
    chart.set_xticks(range(len(calDate)))                                                    #type: ignore
    chart.set_xticklabels(calDate)                                                           #type: ignore

    chart.axhspan(0, 1, facecolor="#dd3a3a", alpha=0.1)                                    #type: ignore
    chart.axhspan(1, 2, facecolor="#e0b049", alpha=0.1)                                    #type: ignore
    chart.axhspan(2, 3, facecolor="#E3EC60", alpha=0.1)                                    #type: ignore
    chart.axhspan(3, 4, facecolor="#A6F051", alpha=0.1)                                    #type: ignore
    chart.axhspan(4, 5, facecolor="#3BD64F", alpha=0.1)                                    #type: ignore

    # Annotate each point
    for i, val in enumerate(score):
        chart.annotate(f"{val:.1f}", (i, val), textcoords="offset points", xytext=(0, 5),    #type: ignore
                        ha='center', fontsize=8)

    canvas.draw()

# Refresh logic
def refresh(
        
        entries : Any ,
        canvas : FigureCanvasTkAgg ,
        plotStatus : ttk.Frame, 
        chart : Axes, 
        state : dict[str, datetime],
        
    ):  
    averageMood = middle_Mood(entries, state["center_date"])
    calDate = list(averageMood.keys())
    score = [averageMood[d] if averageMood[d] is not None else 0 for d in calDate]
    plot_mood_chart(entries ,canvas, plotStatus, chart, calDate, score)

def shift_page(
        state : dict[str, datetime],
        callerID : tuple[str, str],
        entries : Any | None = None,
        canvas : FigureCanvasTkAgg | None = None,
        plotStatus : ttk.Frame | None = None, 
        chart : Axes | None = None

    ):
    print(callerID)
    if callerID[0] == 'left':
        state["center_date"] -= timedelta(days = (1 if callerID[1] == 'Plot' else 28)) # center date is adjusted by 1 if called from the plot tab and 28 if otherwise
    elif callerID[0] == 'right':
        state["center_date"] += timedelta(days = (1 if callerID[1] == 'Plot' else 28) )

    if callerID[1] == 'Plot':
        refresh(entries = entries ,canvas = canvas, plotStatus = plotStatus, chart = chart, state = state) #type: ignore
        return
    global pointOfReferenceDate
    pointOfReferenceDate = state["center_date"]
    return 