import csv
from collections import defaultdict

CSV_FILE = "mood_data.csv"

def load_entries():
    """Loads entries from the CSV file and returns a dictionary with dates as keys."""
    entries = defaultdict(list)
    try:
        with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            reader.fieldnames = [f.strip() for f in reader.fieldnames]
            for row in reader:
                try:
                    mood = int(row["mood"])
                    if mood < 1 or mood > 5:
                        continue
                    entries[row["date"].strip()].append({
                        "mood": mood,
                        "journal": row.get("journal", "").strip()
                    })
                except (ValueError, KeyError):
                    continue
    except FileNotFoundError:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["date","mood","journal"])
            writer.writeheader()
    return entries

def save_entry(date, mood, journal):
    """Saves a new entry to the CSV file."""
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["date","mood","journal"])
        writer.writerow({"date": date, "mood": mood, "journal": journal})

def delete_entry(date, index):
    """
    Deletes the entry at the given index for the specified date.
    """
    entries = load_entries()
    if date in entries and 0 <= index < len(entries[date]):
        entries[date].pop(index)
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["date","mood","journal"])
            writer.writeheader()
            for d, lst in entries.items():
                for e in lst:
                    writer.writerow({"date": d, "mood": e["mood"], "journal": e["journal"]})
        return True
    return False
