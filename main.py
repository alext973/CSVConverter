import os
import csv
import datetime
import re
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Globale Variable für den Dateipfad
input_file = ""

def extract_street_and_number(street, street2):
    match = re.search(r"^(\D*?)(\d.*)?$", street.strip())
    if match:
        street_name = match.group(1).strip()
        house_number = match.group(2).strip() if match.group(2) else ""
        
        if street2 and re.fullmatch(r"\d+.*", street2.strip()):
            house_number = street2.strip()
        
        return street_name, house_number
    return street, street2 if street2 and re.fullmatch(r"\d+.*", street2.strip()) else ""

def load_csv():
    global input_file
    file_path = filedialog.askopenfilename(
        title="CSV-Datei auswählen", 
        filetypes=[("CSV-Dateien", "*.csv")]
    )
    if file_path and file_path.endswith(".csv"):
        input_file = file_path  # Globale Variable setzen
        date_dropdown.set("Bitte Datum auswählen")  # Dropdown zurücksetzen
        date_dropdown.configure(values=extract_dates(file_path))
        convert_button.configure(state="normal")
    else:
        messagebox.showerror("Fehler", "Bitte eine gültige CSV-Datei auswählen.")

def extract_dates(file_path):
    dates = set()
    today = datetime.date.today().strftime("%m/%d/%y")
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%m/%d/%y")
    
    try:
        with open(file_path, mode="r", encoding="utf-8") as infile:
            reader = csv.DictReader(infile, delimiter=",")
            for row in reader:
                sales_date = row.get("Verkaufsdatum", "")
                if sales_date:
                    dates.add(sales_date)
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Laden der CSV: {str(e)}")
        return []
    
    sorted_dates = sorted(dates, key=lambda x: datetime.datetime.strptime(x, "%m/%d/%y"))
    formatted_dates = [f"{date} (Heute)" if date == today else f"{date} (Gestern)" if date == yesterday else date for date in sorted_dates]
    return formatted_dates

def convert_csv():
    global input_file
    if not input_file:
        messagebox.showerror("Fehler", "Es wurde keine CSV-Datei geladen.")
        return

    selected_date = date_dropdown.get().split(" ")[0]  # Nur das Datum extrahieren
    
    output_file = filedialog.asksaveasfilename(
        title="Speichern unter", defaultextension=".csv", filetypes=[("CSV-Dateien", "*.csv")]
    )
    if not output_file:
        messagebox.showerror("Kein Speicherort ausgewählt", "Bitte wählen Sie einen Speicherort aus.")
        return
    
    try:
        with open(input_file, mode="r", encoding="utf-8", errors="replace") as infile:
            reader = csv.DictReader(infile, delimiter=",")
            with open(output_file, mode="w", encoding="ISO-8859-1", newline="") as outfile:
                fieldnames = [
                    "Sendungsreferenz", "Sendungsdatum", "Absender Name 1", "Absender Name 2", "Absender Name 3",
                    "Absender Straße", "Absender Hausnummer", "Absender PLZ", "Absender Ort", "Absender Provinz",
                    "Absender Land", "Absenderreferenz", "Absender E-Mail-Adresse", "Absender Telefonnummer",
                    "Empfänger Name 1", "Empfänger Name 2 / Postnummer", "Empfänger Name 3", "Empfänger Straße",
                    "Empfänger Hausnummer", "Empfänger PLZ", "Empfänger Ort", "Empfänger Provinz", "Empfänger Land",
                    "Empfängerreferenz", "Empfänger E-Mail-Adresse", "Empfänger Telefonnummer"
                ]
                writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=";")
                writer.writeheader()

                has_data = False
                for row in reader:
                    if row.get("Verkaufsdatum", "") != selected_date:
                        continue
                    
                    street, house_number = extract_street_and_number(row.get("Strasse 1", ""), row.get("Strasse 2", ""))
                    
                    writer.writerow({
                        "Sendungsreferenz":"",
                        "Sendungsdatum": "",
                        "Absender Name 1": "VERDRUCKT",
                        "Absender Name 2": "",
                        "Absender Name 3": "",
                        "Absender Straße": "Oskar-Ursinus-Str.",
                        "Absender Hausnummer": "3",
                        "Absender PLZ": "36041",
                        "Absender Ort": "Fulda",
                        "Absender Provinz": "",
                        "Absender Land": "DEU",
                        "Absenderreferenz": "",
                        "Absender E-Mail-Adresse": "hello@verdruckt.com",
                        "Absender Telefonnummer": "",
                        "Empfänger Name 1": row.get("Name", ""),
                        "Empfänger Name 2 / Postnummer": "",
                        "Empfänger Name 3": "",
                        "Empfänger Straße": street,
                        "Empfänger Hausnummer": house_number,
                        "Empfänger PLZ": row.get("Versand-Postleitzahl", ""),
                        "Empfänger Ort": row.get("Stadt des Versands", ""),
                        "Empfänger Provinz": row.get("Bundesland des Versands", ""),
                        "Empfänger Land": "DEU",
                        "Empfängerreferenz": "",
                        "Empfänger E-Mail-Adresse": "",
                        "Empfänger Telefonnummer": ""
                    })
                    has_data = True

                if not has_data:
                    messagebox.showwarning("Keine Daten", "Es wurden keine Sendungsdaten für das ausgewählte Datum gefunden.")
                else:
                    messagebox.showinfo("Erfolg", "Die CSV-Datei wurde erfolgreich erstellt!")
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {str(e)}")

# --- GUI ---
ctk.set_appearance_mode("dark")  # Setze den Dark Mode
ctk.set_default_color_theme("blue")  # Setze das Standardfarbthema

root = ctk.CTk()  # Verwende customtkinter anstelle von tkinter
root.title("CSV-Konverter")
root.geometry("500x350")

# Frame für die Inhalte
frame = ctk.CTkFrame(root, corner_radius=15)
frame.pack(padx=20, pady=20, fill="both", expand=True)

# Titel
title_label = ctk.CTkLabel(frame, text="CSV-Konverter", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# CSV auswählen Button
select_button = ctk.CTkButton(frame, text="CSV-Datei auswählen", command=load_csv, height=40)
select_button.pack(pady=10, fill="x")

# Datum Dropdown
date_label = ctk.CTkLabel(frame, text="Datum auswählen:")
date_label.pack(pady=5)

date_dropdown = ctk.CTkComboBox(frame, values=["Bitte eine CSV-Datei auswählen"], height=30)
date_dropdown.pack(pady=10, fill="x")

# Konvertieren Button
convert_button = ctk.CTkButton(frame, text="CSV konvertieren", command=convert_csv, state="disabled", height=40)
convert_button.pack(pady=20, fill="x")

# Copyright Label
copyright_label = ctk.CTkLabel(root, text="© 2024 HaiX", font=("Arial", 10))
copyright_label.pack(pady=5)

root.mainloop()