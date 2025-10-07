import csv

from tkinter import Text
from tkinter import ttk, StringVar, Entry, Text, Canvas

from datetime import datetime, timedelta

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.axes import Axes

from typing import Any
from collections import defaultdict
from collections.abc import Callable

from data_loader import load_entries, delete_entry , save_entry#type: ignore

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

# ============== Entry List Tab Functions ============== #
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
    for date in sorted(entries.keys(), reverse = True):
        ttk.Label(container, text=f"📅 {date}", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        for i, entry in enumerate(entries[date]):
            mood = entry["mood"]
            journal = str(entry["journal"])

            displayEntryFrame = ttk.Frame(container, padding=5)
            displayEntryFrame.pack(fill="x", padx=20, pady=2)

            mood_int = entry.get("mood", 1)
            x = mdcolor.get(mood_int,( "#f0f0f0", 'X'))
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

            ttk.Button(displayEntryFrame, text= "Delete", command = notANestedCallback([(delete_entry, [date, i], {}),(render_entries, [container], {})])).pack(side='right', padx=5) #type: ignore
            ttk.Button(displayEntryFrame, text = "Update Changes", command = notANestedCallback([(overwrite_entry, [date, i, mood, jtext], {})])).pack(side = 'right', padx = 5)

# ============== Mood Logger Tab Functions ============== #

def select_mood(m: str, emojiButtons : list[ttk.Button], selected_mood : StringVar):
    """
    Creates the buttons for selecting the mood based on the emoji
    """
    selected_mood.set(m)
    for btn in emojiButtons:
        btn.configure(style="TButton")
    emojiButtons[MoodMap[m]-1].configure(style="Selected.TButton")

def save_log_entry(selected_mood : StringVar, journal : Text, selDate : StringVar, confirmation_label : ttk.Label):
    """
    Prepares the mood, score, and journal to be written to the csv file, checks if either mood or date is missing before saving.
    """
    mood = selected_mood.get()
    score : int = MoodMap.get(mood,0)
    note = journal.get("1.0", "end").strip()
    date = selDate.get()
    if not mood:
        confirmation_label.config(text = "Please select a mood before saving.")
        return
    if not date:
        confirmation_label.config(text = "Please select a date before saving")
        return
    save_entry(date, score, note)
    confirmation_label.config(text="Entry saved!")

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

    calendarContainer = ttk.Frame(parent, borderwidth=2, relief = 'solid', padding=10)
    calendarContainer.pack(pady=10, fill="both", expand = True)
    
    rows, columns = 4, 7
    relXPos, relYPos = 1 / columns, 1 / rows
    
    for i in range(columns):
        day_date = PORdate + timedelta(i)
        dayOfTheWeek = day_date.strftime("%A")
        ttk.Label(calendarContainer, text = dayOfTheWeek, justify = 'center', padding = 5).place(
                relx=(i + 0.5) * relXPos,
                relwidth=relXPos,
                relheight= 0.1,
                anchor="center"
        )

    for j in range(rows):
        for i in range(columns):
            day_date : datetime = PORdate + timedelta(days = i + j * columns)
            cellLabel = day_date.strftime("%B %d, %Y")

            dateContainer = ttk.Frame(calendarContainer, padding=5, relief = 'sunken', borderwidth = 2) #relief -> visual border style
            dateContainer.place(
                relx=(i + 0.5) * relXPos,
                rely= 0.05 + (j + 0.5) * relYPos,
                relwidth=relXPos,
                relheight=relYPos,
                anchor="center"
            )

            ttk.Label(dateContainer, text = cellLabel, justify = 'center').pack()
            ttk.Button(dateContainer, text="Select", command = notANestedCallback([(function, [day_date], {})])).pack()

# ============== Plot Chart Tab Functions ============== #

def middle_Mood(cD: datetime):      
    """
    Loads 7 entries to be plotted in the chart tab. Middles the current day.
    """
    entries: defaultdict[str, list[dict[str, Any]]] = load_entries() #type: ignore
    print(entries)
    """sample entries: {'2025-10-06' : [
    {
        'mood': 2, 
        'journal': 'stringhere'
    }
    ]}""" 
    avgScore : dict[str, float] = {}
    for delta in range(-4,3):
        xAxisPlot = (cD + timedelta(days = delta)).strftime("%Y-%m-%d") # 
        y : list[int] = []
        for row in entries.get(xAxisPlot, []):
            raw_mood = row.get("mood")
            moodInt = int(raw_mood) # pyright: ignore[reportArgumentType]
            y.append(moodInt)
        avgScore[xAxisPlot] = sum(y) / len(y) if y else 0.0
    return avgScore

def get_dynamic_figsize(widget : Canvas, dpi : int = 100) -> tuple[float, float]:
    """
    Resizes the plot figsize depending on current px of the window
    """
    width_px : float = widget.winfo_width()
    height_px  : float = widget.winfo_height()
    width_in  : float = max(width_px / dpi, 4)   # clamp to minimum size
    height_in  : float = max(height_px / dpi, 2)
    return (width_in, height_in)

def plot_mood_chart(
        
        entries : Any,
        canvas : FigureCanvasTkAgg ,
        plotStatus : ttk.Frame, 
        chart : Axes, 
        calDate : list[str], 
        score : list[ float | int ]
        
    ):
    """
    Sets up the plot using matplotlib. Uses Dates as x-axis. Y axis is restricted from y = 0 to y = 5. 
    """
    if not entries:
        chart.clear()
        canvas.draw()
        return
    
    chart.clear()   
    chart.plot(calDate, score, marker="o")                                                   # pyright: ignore[reportUnknownMemberType]
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
        chart.annotate(f"{val:.1f}", (i, val), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8)    #type: ignore

    canvas.draw()

# ============== Shared Functions ============== #
def refresh(
        
        canvas : FigureCanvasTkAgg ,
        plotStatus : ttk.Frame, 
        chart : Axes, 
        state : dict[str, datetime],
        
    ):  
    """
    Refresh button logic, readies/remakes the values for the plotting function
    """
    entries: defaultdict[str, list[dict[str, Any]]] = load_entries() #type: ignore
    averageMood = middle_Mood(state["center_date"])
    print('Middle Mood was triggered by refresh!')
    calDate = list(averageMood.keys())
    score = [averageMood[d] for d in calDate]
    print(averageMood)
    plot_mood_chart(entries ,canvas, plotStatus, chart, calDate, score)

def shift_page(
        state : dict[str, datetime],
        callerID : tuple[str, str],
        entries : Any | None = None,
        canvas : FigureCanvasTkAgg | None = None,
        plotStatus : ttk.Frame | None = None, 
        chart : Axes | None = None

    ):
    """
    Date adjusment function. Depending on the caller, timedelta is either 1 (if called from plot) or 28 (if called from calendar). Call from plot also invokes refresh() function. Updates the global point of reference date
    """
    print(callerID)
    if callerID[0] == 'left':
        state["center_date"] -= timedelta(days = (1 if callerID[1] == 'Plot' else 28)) # center date is adjusted by 1 if called from the plot tab and 28 if otherwise
    elif callerID[0] == 'right':
        state["center_date"] += timedelta(days = (1 if callerID[1] == 'Plot' else 28) )

    if callerID[1] == 'Plot':
        refresh(canvas = canvas, plotStatus = plotStatus, chart = chart, state = state) #type: ignore
        return
    
    global pointOfReferenceDate
    pointOfReferenceDate = state["center_date"]
    return 

def notANestedCallback(
        funcAndArgList: list[
            tuple[
                Callable[..., Any], 
                list[Any], 
                dict[str, Any]
                 ]
            ]) -> Callable[[], Any | None]:
    """
    Button logic to avoid nesting inside buttons, takes a list of tuples containing a pair of a callable functio, list of positional arguments OR dictionary of keyword arguments.
    """
    def callableFunction():
        for func, args, kwargs in funcAndArgList:
            func(*args, **kwargs)
    
    return callableFunction