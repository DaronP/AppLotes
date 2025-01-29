import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
from db import execute_query, execute_non_query

def crear_ingreso_comisionista(parent, conn):

    # Crear el frame donde estarán los elementos de la página 1
    page_bg = "#9A9898"

    frame = tk.Frame(parent, bg=page_bg)
    frame.place(relwidth=1, relheight=1)  # Expandir el frame al tamaño completo del contenedor
    tk.Label(frame, text="Ingreso de Comisionista", font=('Arial', 18), bg='#9A9898').place(relx=0.4, rely=0.03)


    # Crear un objeto Style
    style = ttk.Style()
    style.theme_use("clam")

    # Configurar el Treeview para que coincida con el color de la página
    style.configure(
        "Custom.Treeview",
        background=page_bg,
        fieldbackground=page_bg,
        foreground="#000000",
        bordercolor=page_bg,
        lightcolor=page_bg,
        darkcolor=page_bg
    )

    style.configure(
        "Custom.Treeview.Heading",
        background=page_bg,
        foreground="#000000",
        borderwidth=0.1,
        font=("Arial", 12, "bold")
    )

    style.map(
        "Custom.Treeview.Heading",
        background=[("active", page_bg), ("pressed", page_bg)]
    )
    
    # Crear el Treeview con el estilo personalizado
    tree = ttk.Treeview(frame, columns=("dpi", "nombre"), show='headings', style="Custom.Treeview")
    tree.place(relx=0.5, rely=0.1, relwidth=0.45, relheight=0.5)

    # Configurar encabezados de columna
    tree.heading("dpi", text="DPI")
    tree.heading("nombre", text="Nombre")

    tree.column("dpi", anchor="center")
    tree.column("nombre", anchor="center")

    # Cargar los datos automáticamente al mostrar la página
    cargar_datos(conn, tree)


    # Crear elementos de entrada (Drop-downs y selector de fecha)
    tk.Label(frame, text="Nombre", bg='#9A9898').place(relx=0.005, rely=0.15)
    text1 = ttk.Entry(frame)
    text1.place(relx=0.095, rely=0.15, relwidth=0.2)

    tk.Label(frame, text="Direccion", bg='#9A9898').place(relx=0.005, rely=0.2)
    text2 = ttk.Entry(frame)
    text2.place(relx=0.095, rely=0.2, relwidth=0.2)

    tk.Label(frame, text="DPI", bg='#9A9898').place(relx=0.005, rely=0.25)
    text3 = ttk.Entry(frame)
    text3.place(relx=0.095, rely=0.25, relwidth=0.2)

    tk.Label(frame, text="Fecha de ingreso", bg='#9A9898').place(relx=0.005, rely=0.3)
    date_selector = DateEntry(frame)
    date_selector.place(relx=0.095, rely=0.3, relwidth=0.2)

    # Botón para ingresar datos
    label6 = tk.Label(frame, text="")
    submit_button = tk.Button(frame, text="Ingresar Datos", 
                              command=lambda: ingresar_datos(conn, text1, text2, text3, date_selector, frame, parent))
    submit_button.place(relx=0.005, rely=0.85)


    return frame


def ingresar_datos(conn, nombre, direccion, dpi, fecha, frame, parent):
    try:
        nombre_val = nombre.get()
        direccion_val = direccion.get()
        dpi_val = int(dpi.get())
        fecha_val = fecha.get_date()
        execute_non_query(conn, "INSERT INTO comisionistas(dpi, nombre, direccion, fecha_ingreso) VALUES(%s, %s, %s, %s)", (dpi_val, nombre_val, direccion_val, fecha_val))

        frame.destroy()  # Destruye el frame actual (página actual)
        crear_ingreso_comisionista(parent, conn)

    except:
        tk.messagebox.showerror(title="Error", message="El numero de DPI es invalido")


def cargar_datos(conn, tree):
    # Limpiar la tabla antes de cargar nuevos datos
    for row in tree.get_children():
        tree.delete(row)

    # Obtener los datos desde la base de datos (asumiendo que tu tabla se llama 'personas' o similar)
    resultados = execute_query(conn, "SELECT dpi, nombre FROM comisionistas")

    # Insertar los datos en el Treeview
    for fila in resultados:
        # Asumiendo que fila es un diccionario o tupla (dpi, nombre)
        dpi = fila['dpi'] if isinstance(fila, dict) else fila[0]
        nombre = fila['nombre'] if isinstance(fila, dict) else fila[1]
        
        tree.insert("", tk.END, values=(dpi, nombre))
    