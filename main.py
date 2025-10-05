# Main Python File -> Active File
from tkinter import * # pyright: ignore[reportWildcardImportFromLibrary]
from tkinter import ttk
from ttkthemes import ThemedTk

# Imported Functions from [tab]_tab.py
from logging_tab import build_logging_tab as bobthebuilder 
from entry_list import build_entries_tab as mannyhandyman
from chart_tab import build_chart_tab as vickdeforester

# Author's Message to the reader:
# This code is a testament:
# a testament to the suffering that Airam G (1st yr Computer Science student) has caused me by setting up strictTyping for in my python workspace
# and a testament, to the dumb me who couldn't be bothered to perform a clean install of python 3.13

if __name__ == '__main__':
    root = ThemedTk(theme="adapta")
    root.title('Happy Path Mood Diary') 
    
    TabControl = ttk.Notebook(root)                     #notebook tabs similar to MS OneNote Notebooks

    loggingtab = ttk.Frame(TabControl)                  #ttk.Frame -> container for widgets; params -> (parent, opt: padding, width/height (fixed), ttk.Style)
    weeklychart = ttk.Frame(TabControl)
    entriestab = ttk.Frame(TabControl)

    loggingtab.pack(expand = True, fill = 'both')
    weeklychart.pack(expand = True, fill = 'both')
    entriestab.pack(expand = True, fill = "both")

    TabControl.add(loggingtab, text = 'Mood Logger')    #.add -> new frame as tab; params -> (child, text, opt: image, pad)
    TabControl.add(weeklychart, text = 'Weekly Chart')
    TabControl.add(entriestab, text = 'Entries')  

    TabControl.pack(expand = True, fill = 'both')          #.pack -> widget geometry assingment within parent

    bobthebuilder(loggingtab) #build the logging tab
    mannyhandyman(entriestab) #build the entry list tab
    vickdeforester(weeklychart) #builds the plot tab

    quitButton = ttk.Button(root, text = 'Quit', command = root.destroy).pack(side = 'bottom', pady = 3)

    root.mainloop()