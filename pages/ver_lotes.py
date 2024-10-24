import tkinter as tk

def crear_ver_lotes(contenido_frame):
    pagina4 = tk.Frame(contenido_frame, bg="white")
    pagina4.grid(row=0, column=0, sticky='nsew')
    tk.Label(pagina4, text="Página 4: Ayuda", font=('Arial', 18)).pack(pady=20)
    return pagina4