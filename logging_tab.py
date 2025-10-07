from tkinter import ttk, Text, StringVar
from datetime import datetime
from data_loader import save_entry # type: ignore # 
from miscallaenousHelper import MoodMap, shift_page, calendarcreator, notANestedCallback, select_mood, save_log_entry

from typing import Any

shared_state : dict[str, Any]= {}

def date_selection(date : datetime):
    shared_state["selDate"].set(date.strftime('%Y-%m-%d'))

def build_logging_tab(Ltab : ttk.Frame):
    shared_state["selDate"] = StringVar()
    selected_mood = StringVar()
    emoji_buttons : list[ttk.Button] = []
    state : dict[str, datetime] = {'center_date' : datetime.today()}

    # Calendar Grid
    calFrame = ttk.Frame(Ltab, relief = 'sunken', borderwidth = 2, padding = 5)
    calFrame.pack(fill = 'both', expand = True)
    calendarcreator(parent = calFrame, selDate = shared_state['selDate'], function = date_selection)
    
    ttk.Button(Ltab, text ="Previous 28 DAYS", command = notANestedCallback([(shift_page, [], {'state' : state, 'callerID' : ('left', 'logger')}), (calendarcreator, [], {'parent' : calFrame, 'selDate' : shared_state['selDate'], 'function' : date_selection})])).pack(side = 'left', padx = 5)
    ttk.Button(Ltab, text ="Next 28 DAYS", command = notANestedCallback([(shift_page, [], {'state' : state, 'callerID' : ('right', 'logger')}), (calendarcreator, [], {'parent' : calFrame, 'selDate' : shared_state['selDate'], 'function' : date_selection})])).pack(side = 'right', padx = 5)
    
    # Confirmation label showing whether both mood and date are selected
    confirmation_label = ttk.Label(Ltab, text="Nothing New Saved Yet")
    confirmation_label.pack(side = 'bottom', padx = 1, pady = 1)
    
    # Mood Selection
    emoji_frame = ttk.Frame(Ltab, relief = 'sunken', borderwidth = 2)
    ttk.Label(emoji_frame, text="Select Mood:").pack(pady=5)
    emoji_frame.pack(fill = 'both', side = 'left', padx = 10)
    for emoji in MoodMap:
        btn = ttk.Button(emoji_frame, text=emoji, command = notANestedCallback([(select_mood, [emoji, emoji_buttons, selected_mood], {})])) 
        btn.pack(side = 'right' ,padx=5)
        emoji_buttons.append(btn)
    # Journal Entry
    journalFrame = ttk.Frame(Ltab, relief = 'sunken', borderwidth = 2)
    ttk.Label(journalFrame, text="Journal Entry:").pack(pady=5)
    journalFrame.pack(fill = 'both', side = 'right', padx = 10)
    journal = Text(journalFrame, height=5, width=50)
    journal.pack(padx = 10)

    # Save Button + Confirmation
    ttk.Button(Ltab, text="Save Entry", command = notANestedCallback([(save_log_entry, [selected_mood, journal, shared_state['selDate'], confirmation_label], {})])).pack(side = 'left', padx = 1)
    confirmation_label.pack()
