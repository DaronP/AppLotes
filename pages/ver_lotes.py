import tkinter as tk
from tkinter import ttk
from db import execute_query, execute_non_query

def crear_ver_lotes(parent, conn):
    page_bg = "#9A9898"

    frame = tk.Frame(parent, bg=page_bg)
    frame.place(relwidth=1, relheight=1)  # Expandir el frame al tamaño completo del contenedor
    tk.Label(frame, text="Ver lotes", font=('Arial', 18), bg='#9A9898').place(relx=0.4, rely=0.03)

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


    # Definir las columnas que se van a mostrar
    columnas = ("lote_id", "sector", "area", "valor", "enganche", "terreno", "disponible", "propietario")

    # Crear el Treeview
    tree = ttk.Treeview(frame, columns=columnas, show='headings', style="Custom.Treeview")
    tree.place(relwidth=1, relheight=1)  # Ocupa todo el espacio del frame

    # Configurar los encabezados de columna
    tree.heading("lote_id", text="No. Lote")
    tree.heading("sector", text="Sector")
    tree.heading("area", text="Área")
    tree.heading("valor", text="Valor")
    tree.heading("enganche", text="Enganche")
    tree.heading("terreno", text="Terreno")
    tree.heading("disponible", text="Disponible")
    tree.heading("propietario", text="Propietario")

    # Opcional: ajustar el ancho de cada columna
    # Por ejemplo, ancho fijo:
    tree.column("lote_id", width=40, anchor="center")
    tree.column("sector", width=50, anchor="center")
    tree.column("area", width=80, anchor="center")
    tree.column("valor", width=100, anchor="center")
    tree.column("enganche", width=100, anchor="center")
    tree.column("terreno", width=100, anchor="center")
    tree.column("disponible", width=40, anchor="center")
    tree.column("propietario", width=200, anchor="center")

    # Cargar los datos automáticamente al crear la página
    cargar_datos(conn, tree)


    return frame


def cargar_datos(conn, tree):
    # Limpiar la tabla
    for row in tree.get_children():
        tree.delete(row)

    # Consulta para obtener los datos (ajusta el nombre de la tabla y columnas según tu esquema)
    resultados = execute_query(conn, "SELECT lote_id, sector, area, valor, enganche, terreno, disponible, propietario FROM lotes")

    # Insertar los datos en el Treeview
    for fila in resultados:
        # Asumiendo que fila sea un dict o tuple
        lote_id = fila['lote_id'] if isinstance(fila, dict) else fila[0]
        sector = fila['sector'] if isinstance(fila, dict) else fila[1]
        area = fila['area'] if isinstance(fila, dict) else fila[2]
        valor = fila['valor'] if isinstance(fila, dict) else fila[3]
        enganche = fila['enganche'] if isinstance(fila, dict) else fila[4]
        terreno = fila['terreno'] if isinstance(fila, dict) else fila[5]
        disponible = fila['disponible'] if isinstance(fila, dict) else fila[6]
        propietario = fila['propietario'] if isinstance(fila, dict) else fila[7]
        
        try:
            propietario_nombre = execute_query(conn, 'SELECT nombre FROM clientes WHERE cliente_id = %s', (propietario))
            propietario_nombre = propietario_nombre[0]['valor'] if isinstance(propietario_nombre[0], dict) else propietario_nombre[0][0]
        except:
            propietario_nombre = "-"

        if disponible == 1:
            disponible = 'Si'
        else:
            disponible = 'No'

        tree.insert("", tk.END, values=(lote_id, sector, area, valor, enganche, terreno, disponible, propietario_nombre))
