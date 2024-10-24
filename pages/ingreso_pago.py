import tkinter as tk
from tkcalendar import DateEntry

def crear_ingreso_pago(parent):
    frame = tk.Frame(parent)

    tk.Label(frame, text="Ingreso de Pago", font=('Arial', 18)).grid(row=0, column=1, padx=10, pady=5, sticky="e")

    tk.Label(frame, text="Seleccione opción 1:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    opciones1 = ["Opción A", "Opción B", "Opción C"]
    seleccion1 = tk.StringVar(value=opciones1[0])
    dropdown1 = tk.OptionMenu(frame, seleccion1, *opciones1)
    dropdown1.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tk.Label(frame, text="Seleccione opción 2:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    opciones2 = ["Opción X", "Opción Y", "Opción Z"]
    seleccion2 = tk.StringVar(value=opciones2[0])
    dropdown2 = tk.OptionMenu(frame, seleccion2, *opciones2)
    dropdown2.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    tk.Label(frame, text="Seleccione una fecha:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    date_entry = DateEntry(frame)
    date_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    tk.Button(frame, text="Ingresar Datos", command=lambda: print(f"Datos: {seleccion1.get()}, {seleccion2.get()}, {date_entry.get_date()}")).grid(row=4, column=0, columnspan=2, pady=10)

    frame.pack(fill="both", expand=True)
