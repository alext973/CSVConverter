import csv
from tkinter import filedialog, messagebox
import customtkinter as ctk
from date_extractor import extract_dates
from address_parser import extract_street_and_number

input_file = ""  # Globale Variable für den Dateipfad
selected_dates = []  # Globale Liste für die ausgewählten Daten
selected_orders_per_date = {}  # speichert ausgewählte Besteller pro Datum
all_orders_per_date = {}  # speichert alle Besteller pro Datum
weights_per_date = {}          # speichert Gewichte pro Datum und Bestellung

def replace_invalid_characters(text):
    if not text:
        return ""
    return text.encode("ISO-8859-1", errors="replace").decode("ISO-8859-1")

def load_csv(date_frame, convert_button, on_date_checkbox_callback):
    global input_file, all_orders_per_date
    file_path = filedialog.askopenfilename(
        title="CSV-Datei auswählen", 
        filetypes=[("CSV-Dateien", "*.csv")]
    )
    if file_path and file_path.endswith(".csv"):
        input_file = file_path
        dates = extract_dates(file_path)
        all_orders_per_date = extract_orders_per_date(file_path, dates)

        # Entferne alte Checkboxen
        for widget in date_frame.winfo_children():
            widget.destroy()

        # Füge neue Checkboxen mit Callback hinzu
        for date in dates:
            var = ctk.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(
                date_frame,
                text=date,
                variable=var,
                command=lambda d=date, v=var: on_date_checkbox_callback(d, v)
            )
            cb.pack(anchor="w", padx=10, pady=2)

        convert_button.configure(state="normal")
    else:
        messagebox.showerror("Fehler", "Bitte eine gültige CSV-Datei auswählen.")

def extract_orders_per_date(file_path, dates):
    orders_per_date = {date: [] for date in dates}
    try:
        with open(file_path, mode="r", encoding="utf-8", errors="replace") as infile:
            reader = csv.DictReader(infile, delimiter=",")
            for row in reader:
                date = row.get("Sale Date", "")
                name = row.get("Full Name", "")
                if date in orders_per_date and name and name not in orders_per_date[date]:
                    orders_per_date[date].append(name)
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Lesen der Besteller: {str(e)}")
    return orders_per_date

def save_selected_dates(date_frame):
    global selected_dates
    selected_dates = []
    for widget in date_frame.winfo_children():
        if isinstance(widget, ctk.CTkCheckBox):
            var_obj = widget._variable if hasattr(widget, "_variable") else None
            if var_obj and var_obj.get():
                selected_dates.append(widget.cget("text"))

def get_selected_dates():
    return selected_dates

def get_orders_for_date(date):
    if date == "all_dates":
        return list(all_orders_per_date.keys())
    return all_orders_per_date.get(date, [])

def save_selected_orders(date, orders):
    selected_orders_per_date[date] = orders

def get_selected_orders(date):
    return selected_orders_per_date.get(date, [])

def save_selected_orders(date, orders, weights=None):
    global selected_orders_per_date, weights_per_date
    selected_orders_per_date[date] = orders
    if weights is not None:
        if date not in weights_per_date:
            weights_per_date[date] = {}
        weights_per_date[date].update(weights)

def get_weight_for_order(date, order):
    return weights_per_date.get(date, {}).get(order, "")

def convert_csv():
    global input_file, selected_dates, selected_orders_per_date, weights_per_date
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
                    "Empfängerreferenz", "Empfänger E-Mail-Adresse", "Empfänger Telefonnummer", "Gewicht"
                ]
                writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=";")
                writer.writeheader()

                has_data = False
                for row in reader:
                    date = row.get("Sale Date", "")
                    name = row.get("Full Name", "")
                    if date not in selected_dates:
                        continue
                    selected_orders = selected_orders_per_date.get(date)
                    if selected_orders is not None and name not in selected_orders:
                        continue

                    street, house_number = extract_street_and_number(row.get("Street 1", ""), row.get("Street 2", ""))
                    gewicht = get_weight_for_order(date, name)

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
                        "Empfänger Name 1": replace_invalid_characters(name),
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
                        "Empfänger Telefonnummer": "",
                        "Gewicht": gewicht
                    })
                    has_data = True

                if not has_data:
                    messagebox.showwarning("Keine Daten", "Es wurden keine Sendungsdaten für die ausgewählten Daten/Besteller gefunden.")
                else:
                    messagebox.showinfo("Erfolg", "Die CSV-Datei wurde erfolgreich erstellt!")
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {str(e)}")