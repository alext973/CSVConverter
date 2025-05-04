import csv
from tkinter import filedialog, messagebox
from date_extractor import extract_dates
from address_parser import extract_street_and_number

input_file = ""  # Globale Variable für den Dateipfad

def load_csv(date_dropdown, convert_button):
    global input_file
    file_path = filedialog.askopenfilename(
        title="CSV-Datei auswählen", 
        filetypes=[("CSV-Dateien", "*.csv")]
    )
    if file_path and file_path.endswith(".csv"):
        input_file = file_path
        date_dropdown.set("Bitte Datum auswählen")
        date_dropdown.configure(values=extract_dates(file_path))
        convert_button.configure(state="normal")
    else:
        messagebox.showerror("Fehler", "Bitte eine gültige CSV-Datei auswählen.")

def convert_csv(date_dropdown):
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
                    if row.get("Sale Date", "") != selected_date:
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
                        "Empfänger Name 1": row.get("Full Name", ""),
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
                    messagebox.showwarning("Keine Daten", "Es wurden keine Sendungsdaten für das ausgewählte Datum gefunden.")
                else:
                    messagebox.showinfo("Erfolg", "Die CSV-Datei wurde erfolgreich erstellt!")
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {str(e)}")