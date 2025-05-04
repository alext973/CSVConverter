import customtkinter as ctk
from tkinter import filedialog, messagebox
from csv_handler import load_csv, convert_csv

def start_app():
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
    select_button = ctk.CTkButton(frame, text="CSV-Datei auswählen", command=lambda: load_csv(date_dropdown, convert_button), height=40)
    select_button.pack(pady=10, fill="x")

    # Datum Dropdown
    date_label = ctk.CTkLabel(frame, text="Datum auswählen:")
    date_label.pack(pady=5)

    date_dropdown = ctk.CTkComboBox(frame, values=["Bitte eine CSV-Datei auswählen"], height=30)
    date_dropdown.pack(pady=10, fill="x")

    # Konvertieren Button
    convert_button = ctk.CTkButton(frame, text="CSV konvertieren", command=lambda: convert_csv(date_dropdown), state="disabled", height=40)
    convert_button.pack(pady=20, fill="x")

    # Copyright Label
    copyright_label = ctk.CTkLabel(root, text="© 2024 HaiX", font=("Arial", 10))
    copyright_label.pack(pady=5)

    root.mainloop()