import tkinter as tk

def crear_ingreso_lote(contenido_frame):
    pagina3 = tk.Frame(contenido_frame)
    pagina3.grid(row=0, column=0, sticky='nsew')
    tk.Label(pagina3, text="Ingreso de nuevos lotes", font=('Arial', 18)).pack(pady=20)

    # Etiqueta y campo de entrada para la primera entrada
    tk.Label(pagina3, text="Ingrese dato 1:").pack(pady=10)
    entry1 = tk.Entry(pagina3)
    entry1.pack(pady=10)
    
    # Etiqueta y campo de entrada para la segunda entrada
    tk.Label(pagina3, text="Ingrese dato 2:").pack(pady=10)
    entry2 = tk.Entry(pagina3)
    entry2.pack(pady=10)

    # Botón para ingresar datos
    btn_ingresar = tk.Button(pagina3, text="Ingresar Datos", command=lambda: ingresar_datos(entry1.get(), entry2.get()))
    btn_ingresar.pack(pady=20)

    return pagina3

def ingresar_datos(dato1, dato2):
    print(f"Dato 1: {dato1}, Dato 2: {dato2}")  # Aquí puedes manejar los datos como necesites