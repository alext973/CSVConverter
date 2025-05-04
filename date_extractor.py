import csv
import datetime
from tkinter import messagebox

def extract_dates(file_path):
    dates = set()
    today = datetime.date.today().strftime("%m/%d/%y")
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%m/%d/%y")
    
    try:
        with open(file_path, mode="r", encoding="utf-8") as infile:
            reader = csv.DictReader(infile, delimiter=",")
            for row in reader:
                sales_date = row.get("Sale Date", "")
                if sales_date:
                    dates.add(sales_date)
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Laden der CSV: {str(e)}")
        return []
    
    sorted_dates = sorted(dates, key=lambda x: datetime.datetime.strptime(x, "%m/%d/%y"))
    formatted_dates = [f"{date} (Heute)" if date == today else f"{date} (Gestern)" if date == yesterday else date for date in sorted_dates]
    return formatted_dates