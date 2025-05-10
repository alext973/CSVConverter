import customtkinter as ctk
from tkinter import filedialog, messagebox
from csv_handler import load_csv, convert_csv, save_selected_dates

def start_app():
    ctk.set_appearance_mode("dark")  # Setze den Dark Mode
    ctk.set_default_color_theme("blue")  # Setze das Standardfarbthema

    root = ctk.CTk()  # Verwende customtkinter anstelle von tkinter
    root.title("CSV-Konverter")
    root.geometry("500x400")  # Standardgröße des Fensters

    # Frame für die Inhalte
    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Titel
    title_label = ctk.CTkLabel(frame, text="CSV-Konverter", font=("Arial", 18, "bold"))
    title_label.pack(pady=10)

    # CSV auswählen Button
    select_button = ctk.CTkButton(frame, text="CSV-Datei auswählen", command=lambda: load_csv_and_resize(date_frame, root, convert_button), height=40)
    select_button.pack(pady=10, fill="x")

    # Datum Auswahl Label
    date_label = ctk.CTkLabel(frame, text="Daten auswählen:")
    date_label.pack(pady=5)

    # Frame für die Checkboxen
    date_frame = ctk.CTkScrollableFrame(frame, width=450, height=200)  # Setze Breite und Höhe
    date_frame.pack(pady=10, fill="both", expand=True)

    # Konvertieren Button
    convert_button = ctk.CTkButton(
        frame,
        text="CSV konvertieren",
        command=lambda: handle_conversion(date_frame),
        state="disabled",
        height=40
    )
    convert_button.pack(pady=20, fill="x")

    # Copyright Label
    copyright_label = ctk.CTkLabel(root, text="v1.0.1", font=("Arial", 10))
    copyright_label.pack(pady=5)

    root.mainloop()

def load_csv_and_resize(date_frame, root, convert_button):
    """
    Lädt die CSV-Datei und passt die Fenstergröße basierend auf der Anzahl der Checkboxen an.
    """
    load_csv(date_frame, convert_button)  # Lädt die Checkboxen in das Frame
    num_dates = len(date_frame.winfo_children())  # Anzahl der Checkboxen
    new_height = 300 + (num_dates * 30)  # Berechne die neue Fensterhöhe (30px pro Checkbox)
    max_height = 1170  # Begrenze die maximale Fensterhöhe
    root.geometry(f"500x{min(new_height, max_height)}")  # Setze die neue Fenstergröße

def handle_conversion(date_frame):
    """
    Speichert die ausgewählten Daten und startet die Konvertierung.
    """
    save_selected_dates(date_frame)  # Speichert die ausgewählten Daten in csv_handler.py
    convert_csv()  # Führt die Konvertierung basierend auf den gespeicherten Daten durch