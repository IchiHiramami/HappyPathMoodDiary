from tkinter import ttk, Text, StringVar
from datetime import datetime
from data_loader import save_entry # type: ignore # 
from miscallaenousHelper import MoodMap, shift_page, calendarcreator

def build_logging_tab(Ltab : ttk.Frame):
    selDate = StringVar()

    selected_mood = StringVar()
    confirmation_label = ttk.Label(Ltab, text="")
    emoji_buttons : list[ttk.Button] = []

    state : dict[str, datetime] = {'center_date' : datetime.today()}

    def select_mood(m: str):
        selected_mood.set(m)
        for btn in emoji_buttons:
            btn.configure(style="TButton")
        emoji_buttons[MoodMap[m]-1].configure(style="Selected.TButton")

    def save_log_entry(calendarMode : bool):
        if calendarMode:
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
        else:
            pass

    def date_selection(date : datetime):
        selDate.set(date.strftime('%Y-%m-%d'))

    # Calendar Grid
    calFrame = ttk.Frame(Ltab, padding = 10)
    calFrame.pack(fill = 'both', expand = True)
    calendarcreator(parent = calFrame, selDate = selDate, function = date_selection)
    
    ttk.Button(Ltab, text ="Previous 28 DAYS", command = lambda: [shift_page(state = state ,callerID = ('left', 'logger')), calendarcreator(parent = calFrame, selDate = selDate, function = date_selection)]).pack(side = 'left', padx = 5)
    ttk.Button(Ltab, text ="Next 28 DAYS", command = lambda: [shift_page(state = state ,callerID = ('right', 'logger')), calendarcreator(parent = calFrame, selDate = selDate, function = date_selection)]).pack(side = 'right', padx = 5)
    
    # Mood Selection
    emoji_frame = ttk.Frame(Ltab)
    ttk.Label(emoji_frame, text="Select Mood:").pack(pady=5)
    emoji_frame.pack(side = 'left', padx = 10)
    for emoji in MoodMap:
        btn = ttk.Button(emoji_frame, text=emoji, command=lambda e=emoji: select_mood(e))
        btn.pack(side = 'right' ,padx=5)
        emoji_buttons.append(btn)

    # Journal Entry
    journalFrame = ttk.Frame(Ltab)
    ttk.Label(journalFrame, text="Journal Entry:").pack(pady=5)
    journalFrame.pack(side = 'right', padx = 10)
    journal = Text(journalFrame, height=5, width=50)
    journal.pack(padx = 10)

    # Save Button + Confirmation
    ttk.Button(Ltab, text="Save Entry", command = lambda: save_log_entry(calendarMode = True)).pack(side = 'bottom', pady=10)
    confirmation_label.pack()
