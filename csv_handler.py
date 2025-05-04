import unicodedata
import csv
from tkinter import filedialog, messagebox
import customtkinter as ctk
from date_extractor import extract_dates
from address_parser import extract_street_and_number

input_file = ""  # Globale Variable für den Dateipfad
selected_dates = []  # Globale Liste für die ausgewählten Daten

def replace_invalid_characters(text):
    """
    Ersetzt nicht darstellbare Zeichen in einem Text durch ein '?'.
    """
    if not text:
        return ""
    return text.encode("ISO-8859-1", errors="replace").decode("ISO-8859-1")

def load_csv(date_frame, convert_button):
    global input_file
    file_path = filedialog.askopenfilename(
        title="CSV-Datei auswählen", 
        filetypes=[("CSV-Dateien", "*.csv")]
    )
    if file_path and file_path.endswith(".csv"):
        input_file = file_path
        dates = extract_dates(file_path)  # Extrahiere Daten aus der CSV-Datei

        # Entferne alte Checkboxen
        for widget in date_frame.winfo_children():
            widget.destroy()

        # Füge neue Checkboxen hinzu
        for date in dates:
            var = ctk.StringVar(value="off")
            checkbox = ctk.CTkCheckBox(date_frame, text=date, variable=var, onvalue=date, offvalue="off")
            checkbox.pack(anchor="w", pady=2)

        # Aktiviere den Konvertieren-Button
        convert_button.configure(state="normal")
    else:
        messagebox.showerror("Fehler", "Bitte eine gültige CSV-Datei auswählen.")

def save_selected_dates(date_frame):
    """
    Speichert die ausgewählten Daten aus den Checkboxen in der globalen Liste `selected_dates`.
    """
    global selected_dates
    selected_dates = []  # Zurücksetzen der Liste
    for widget in date_frame.winfo_children():
        if isinstance(widget, ctk.CTkCheckBox) and widget.cget("variable").get() != "off":
            selected_dates.append(widget.cget("variable").get())

def get_selected_dates():
    """
    Gibt die Liste der ausgewählten Daten zurück.
    """
    return selected_dates

def convert_csv():
    global input_file, selected_dates
    if not input_file:
        messagebox.showerror("Fehler", "Es wurde keine CSV-Datei geladen.")
        return

    if not selected_dates:
        messagebox.showerror("Fehler", "Es wurden keine Daten ausgewählt.")
        return

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
                    if row.get("Sale Date", "") not in selected_dates:
                        continue
                    
                    street, house_number = extract_street_and_number(row.get("Street 1", ""), row.get("Street 2", ""))
                    
                    writer.writerow({
                        "Sendungsreferenz": "",
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
                        "Empfänger Name 1": replace_invalid_characters(row.get("Full Name", "")),
                        "Empfänger Name 2 / Postnummer": "",
                        "Empfänger Name 3": "",
                        "Empfänger Straße": street,
                        "Empfänger Hausnummer": house_number,
                        "Empfänger PLZ": row.get("Ship Zipcode", ""),
                        "Empfänger Ort": row.get("Ship City", ""),
                        "Empfänger Provinz": row.get("Ship State", ""),
                        "Empfänger Land": "DEU",
                        "Empfängerreferenz": "",
                        "Empfänger E-Mail-Adresse": "",
                        "Empfänger Telefonnummer": ""
                    })
                    has_data = True

                if not has_data:
                    messagebox.showwarning("Keine Daten", "Es wurden keine Sendungsdaten für die ausgewählten Daten gefunden.")
                else:
                    messagebox.showinfo("Erfolg", "Die CSV-Datei wurde erfolgreich erstellt!")
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {str(e)}")