

## 📘 Mood Diary & Charting App

A modular, emoji-powered mood tracking app built with Python, Tkinter, and Matplotlib. Log your daily mood, visualize trends over time, and enjoy a playful, annotated UI that scales beautifully across screen sizes.

---

### 🚀 Features

- 📝 **Mood Logging Tab**  
  Log your daily mood using emoji-based inputs. Supports journaling, timestamping, and future extensibility.

- 📊 **Chart Tab**  
  Visualizes average mood scores over a 7-day window using Matplotlib. Includes:
  - Dynamic resizing and fullscreen support
  - Emoji-based annotations and mood zones
  - Navigation buttons to shift date windows
  - Debounced resize logic for smooth UX

- 🧠 **Modular Architecture**  
  - `data_loader.py`: Handles entry loading and parsing  
  - `miscellaneousHelper.py`: Provides helpers like `middle_Mood()` and `get_dynamic_figsize()`  
  - `chart_tab.py`: Encapsulates chart rendering logic  
  - `logging_tab.py`: Manages mood entry UI

---

### 🧩 Mood Mapping

```python
MoodMap = {
    "😄": 5,
    "🙂": 4,
    "😐": 3,
    "😟": 2,
    "😭": 1
}
```

Each emoji maps to a numeric score used for charting and averaging.

---

### 📦 Dependencies

- Python ≥ 3.10
- Tkinter (built-in)
- Matplotlib

---

### 📁 File Structure

```
mood-diary/
├── main.py
├── chart_tab.py
├── logging_tab.py
├── data_loader.py
├── miscellaneousHelper.py
├── assets/
│   └── icons, emoji, etc.
└── README.md
```

---

### 🧠 How It Works

- `middle_Mood()` computes average mood scores over a 7-day window centered on a given date.
- Chart tab uses `FigureCanvasTkAgg` and `NavigationToolbar2Tk` for interactive plotting.
- Resize events are debounced to avoid redraw spam.
- Navigation buttons shift the date window left/right by 1 day (or 28 days if called from logging tab).

---

### ✨ Future Plans

- Add emoji tooltips and journal previews on hover
- Export mood trends to PDF or image
- Add calendar view and weekly summaries

---
