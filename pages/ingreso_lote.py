import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from db import execute_query, execute_non_query

def crear_ingreso_lote(parent, conn):
    frame = tk.Frame(parent, bg='#9A9898')
    frame.place(relwidth=1, relheight=1)  # Expandir el frame al tamaño completo del contenedor
    tk.Label(frame, text="Ingreso de nuevos lotes", font=('Arial', 18), bg='#9A9898').place(relx=0.4, rely=0.03)

    # Crear elementos de entrada (Drop-downs y selector de fecha)
    tk.Label(frame, text="Numero de lote", bg='#9A9898').place(relx=0.005, rely=0.15)
    text6 = ttk.Entry(frame)
    text6.place(relx=0.095, rely=0.15, relwidth=0.2)

    tk.Label(frame, text="Sector", bg='#9A9898').place(relx=0.005, rely=0.2)
    text1 = ttk.Entry(frame)
    text1.place(relx=0.095, rely=0.2, relwidth=0.2)

    tk.Label(frame, text="Area", bg='#9A9898').place(relx=0.005, rely=0.25)
    text2 = ttk.Entry(frame)
    text2.place(relx=0.095, rely=0.25, relwidth=0.2)

    tk.Label(frame, text="Terreno", bg='#9A9898').place(relx=0.005, rely=0.3)
    text3 = ttk.Entry(frame)
    text3.place(relx=0.095, rely=0.3, relwidth=0.2)

    tk.Label(frame, text="Valor", bg='#9A9898').place(relx=0.005, rely=0.35)
    text4 = ttk.Entry(frame)
    text4.place(relx=0.095, rely=0.35, relwidth=0.2)

    tk.Label(frame, text="Enganche", bg='#9A9898').place(relx=0.005, rely=0.4)
    text5 = ttk.Entry(frame)
    text5.place(relx=0.095, rely=0.4, relwidth=0.2)


    #Checkbox
    #tk.Label(frame, text="Disponible", bg='#9A9898').place(relx=0.005, rely=0.45)
    checkbox_var = tk.BooleanVar(value=False)
    checkbox = tk.Checkbutton(frame, variable=checkbox_var, bg='#9A9898')
    #checkbox.place(relx=0.095, rely=0.45)

    # Botón para ingresar datos
    submit_button = tk.Button(frame, text="Ingresar Datos", 
                              command=lambda: ingresar_datos(conn, text6, text1, text2, text3, text4, text5, checkbox_var, frame, parent))
    submit_button.place(relx=0.005, rely=0.85)

    return frame

def ingresar_datos(conn, num, sector, area, terreno, valor, enganche, disponible, frame, parent):
    try:
        num_val = int(num.get())
        sector_val = int(sector.get())
        area_val = int(area.get())
        terreno_val = int(terreno.get())
        valor_val = int(valor.get())
        enganche_val = int(enganche.get())
        disponible_val = disponible.get()
        execute_non_query(conn, "INSERT INTO lotes(lote_id, sector, area, valor, enganche, terreno, disponible) VALUES(%s, %s, %s, %s, %s, %s, 1)", (num_val, sector_val, area_val, valor_val, enganche_val, terreno_val))

        frame.destroy()  # Destruye el frame actual (página actual)
        crear_ingreso_lote(parent, conn)

    except:
        tk.messagebox.showerror(title="Error", message="Campo invalido")