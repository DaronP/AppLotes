import tkinter as tk
from tkinter import messagebox
import psycopg2
from login import iniciar_login
from pages.ingreso_pago import crear_ingreso_pago
from pages.ingreso_comisionista import crear_ingreso_comisionista
from pages.ingreso_lote import crear_ingreso_lote
from pages.ver_lotes import crear_ver_lotes


# Función para centrar la ventana en la pantalla
def centrar_ventana(ventana, ancho, alto):
    # Calcular la posición x, y
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

# Función para cambiar entre las páginas
def mostrar_pagina(frame):
    frame.tkraise()  # Mover el frame seleccionado al frente

# Función para cerrar sesión
def cerrar_sesion(ventana_principal):
    ventana_principal.destroy()
    iniciar_login(abrir_menu_principal)

# Función para crear el menú principal colapsable
def abrir_menu_principal():
    ventana_principal = tk.Tk()
    ventana_principal.title('Menú Principal')
    centrar_ventana(ventana_principal, 1280, 720)
    ventana_principal.resizable(False, False)

    # Frame del menú lateral
    menu_frame = tk.Frame(ventana_principal, bg="lightgray", width=200)
    menu_frame.pack(side="left", fill="y")

    # Frame para el botón de colapsar
    btn_frame = tk.Frame(menu_frame, bg="lightgray")
    btn_frame.pack(side="top", fill="x")

    # Botón para colapsar/expandir el menú
    btn_toggle = tk.Button(menu_frame, text="<<", command=lambda: toggle_menu(menu_frame, btn_toggle), width=3)
    btn_toggle.pack(pady=10)

    # Frame contenedor de las páginas
    contenido_frame = tk.Frame(ventana_principal)
    contenido_frame.pack(side="right", expand=True, fill="both")

    # Crear las 4 páginas dentro de frames
    pagina1 = crear_ingreso_pago(contenido_frame)
    pagina2 = crear_ingreso_comisionista(contenido_frame)
    pagina3 = crear_ingreso_lote(contenido_frame)
    pagina4 = crear_ver_lotes(contenido_frame)

    # Mostrar la página 1 al inicio
    mostrar_pagina(pagina1)

    # Botones del menú lateral para cambiar de página
    global btn_pagina1, btn_pagina2, btn_pagina3, btn_pagina4

    btn_pagina1 = tk.Button(menu_frame, text="Página 1", command=lambda: mostrar_pagina(pagina1), width=20)
    btn_pagina1.pack(pady=10)

    btn_pagina2 = tk.Button(menu_frame, text="Página 2", command=lambda: mostrar_pagina(pagina2), width=20)
    btn_pagina2.pack(pady=10)

    btn_pagina3 = tk.Button(menu_frame, text="Página 3", command=lambda: mostrar_pagina(pagina3), width=20)
    btn_pagina3.pack(pady=10)

    btn_pagina4 = tk.Button(menu_frame, text="Página 4", command=lambda: mostrar_pagina(pagina4), width=20)
    btn_pagina4.pack(pady=10)

    # Botón para cerrar sesión
    btn_cerrar_sesion = tk.Button(menu_frame, text="Cerrar Sesión", command=lambda: cerrar_sesion(ventana_principal), width=20, bg="red", fg="white")
    btn_cerrar_sesion.pack(pady=50)

    ventana_principal.mainloop()

# Función para alternar el menú entre colapsado y expandido
def toggle_menu(menu_frame, toggle_button):
    if menu_frame.winfo_width() > 50:  # Si el menú está expandido
        menu_frame.config(width=50)
        toggle_button.config(text=">>")  # Cambiar el texto del botón
        for widget in menu_frame.winfo_children()[1:]:  # Colapsar todos los widgets excepto el botón
            if menu_frame.winfo_children().index(widget) == 1:
                continue

            elif menu_frame.winfo_children().index(widget) == (len(menu_frame.winfo_children()) - 1):
                btnText = 'Salir'

            else:
                btnText = 'P', menu_frame.winfo_children().index(widget) - 1

            widget.config(width=5, text=btnText)  # Hacer los botones más pequeños
            widget.pack(pady=5)
            
    else:  # Si el menú está colapsado
        menu_frame.config(width=200)
        toggle_button.config(text="<<")  # Cambiar el texto del botón
        for widget in menu_frame.winfo_children()[1:]:  # Expandir todos los widgets
            if menu_frame.winfo_children().index(widget) == 1:
                continue

            elif menu_frame.winfo_children().index(widget) == (len(menu_frame.winfo_children()) - 1):
                btnText = 'Cerrar Sesión'

            else:
                btnText = 'Página', menu_frame.winfo_children().index(widget) - 1
            widget.config(width=20, text= btnText)  # Restaurar el ancho original de los botones
            widget.pack(pady=10)

# Iniciar la aplicación desde la ventana de login
iniciar_login(abrir_menu_principal)
