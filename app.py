import customtkinter as ctk
from csv_handler import load_csv, convert_csv, save_selected_dates, get_orders_for_date, save_selected_orders

def start_app():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("CSV-Konverter")
    root.geometry("500x550")

    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    title_label = ctk.CTkLabel(frame, text="CSV-Konverter", font=("Arial", 18, "bold"))
    title_label.pack(pady=10)

    # WICHTIG: date_frame und convert_button werden an load_csv übergeben!
    date_frame = ctk.CTkScrollableFrame(frame, width=450, height=200)
    date_frame.pack(pady=10, fill="both", expand=True)

    convert_button = ctk.CTkButton(
        frame,
        text="CSV konvertieren",
        command=lambda: handle_conversion(date_frame),
        state="disabled",
        height=40
    )
    convert_button.pack(pady=20, fill="x")

    select_button = ctk.CTkButton(frame, text="CSV-Datei auswählen", command=lambda: load_csv(date_frame, convert_button, on_date_checkbox), height=40)
    select_button.pack(pady=10, fill="x")

    date_label = ctk.CTkLabel(frame, text="Daten auswählen:")
    date_label.pack(pady=5)

    copyright_label = ctk.CTkLabel(root, text="© HaiX blyat", font=("Arial", 10))
    copyright_label.pack(pady=5)

    root.mainloop()

def on_date_checkbox(date, var):
    if var.get():
        show_order_selection_window(date)

def show_order_selection_window(date):
    orders = get_orders_for_date(date)  # Liste der Besteller für das Datum
    order_window = ctk.CTkToplevel()
    order_window.title(f"Bestellungen am {date}")
    order_window.geometry("370x440")

    label = ctk.CTkLabel(order_window, text=f"Bestellungen am {date}", font=("Arial", 14, "bold"))
    label.pack(pady=10)

    # Hinweis-Label (zunächst versteckt)
    hint_var = ctk.StringVar(value="")
    hint_label = ctk.CTkLabel(order_window, textvariable=hint_var, font=("Arial", 11), text_color="#888888")
    hint_label.pack(pady=(0, 5))

    # Scrollbarer Frame für die Checkboxen und Gewichtsfelder
    scroll_frame = ctk.CTkScrollableFrame(order_window, width=340, height=280)
    scroll_frame.pack(padx=10, pady=5, fill="both", expand=True)

    order_vars = {}
    weight_vars = {}
    for order in orders:
        row_frame = ctk.CTkFrame(scroll_frame)
        row_frame.pack(fill="x", padx=5, pady=2)

        var = ctk.BooleanVar(value=True)
        cb = ctk.CTkCheckBox(row_frame, text=order, variable=var)
        cb.pack(side="left", padx=(0, 10))

        weight_var = ctk.StringVar()
        weight_entry = ctk.CTkEntry(row_frame, width=60, textvariable=weight_var, placeholder_text="Gewicht")
        weight_entry.pack(side="left")

        # Callback für Hinweis beim Fokussieren
        def show_hint(event, entry=weight_entry):
            hint_var.set("Tipp bei Thermobecher/Tassen: (Anzahl x 0,5) - 0,01\nBeispiel: 3 Produkte → (3 x 0,5) - 0,01 = 1,49 kg")
        def hide_hint(event):
            hint_var.set("")

        weight_entry.bind("<FocusIn>", show_hint)
        weight_entry.bind("<FocusOut>", hide_hint)

        order_vars[order] = var
        weight_vars[order] = weight_var

    def save_and_close():
        selected_orders = []
        weights = {}
        for order, v in order_vars.items():
            if v.get():
                selected_orders.append(order)
                w = weight_vars[order].get().strip()
                weights[order] = w if w else ""
        save_selected_orders(date, selected_orders, weights)
        order_window.destroy()

    save_button = ctk.CTkButton(order_window, text="Speichern", command=save_and_close)
    save_button.pack(pady=15)

def handle_conversion(date_frame):
    save_selected_dates(date_frame)
    convert_csv()