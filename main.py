import tkinter as tk
from login import LoginPage
import pages.ingreso_pago as p
import pages.ingreso_comisionista as c 
import pages.ingreso_lote as l
import pages.ver_lotes as vl
import pages.ver_reportes as vr
import pymysql
from db import execute_query, execute_non_query

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1280x720')
        self.title('Control de lotificacion')
        self.center_window()

        self.login_frame = tk.Frame(self)

        self.menu_colapsado = False

        self.conn = pymysql.connect(
        host="localhost",
        user="root",
        password="admin",
        database="lotificacion",
        charset='utf8mb4'
        )

        '''# Mostrar la pantalla de Login primero
        self.login_frame.pack(fill="both", expand=True)
        self.login_page = LoginPage(self.login_frame, self.conn, self.on_login_success())'''

        self.create_main_app()

    def center_window(self):
        self.update_idletasks()
        width = 1280
        height = 720
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        

    def on_login_success(self):
        self.login_frame.destroy()
        self.create_main_app()

    def create_main_app(self):
        # Configurar las columnas del grid
        self.grid_columnconfigure(0, weight=0)  # Menú
        self.grid_columnconfigure(1, weight=1)  # Contenido

        # Frame del menú expandible
        self.menu_frame = tk.Frame(self, bg='#5C5C5C')
        self.menu_frame.grid(row=0, column=0, sticky='ns')  # Expande el menú de arriba a abajo
        self.menu_frame.grid_propagate(False)
        self.menu_frame.config(width=150, height=720)

        # Crear un grid layout para el menú
        self.menu_frame.grid_rowconfigure(0, weight=0)  # Botón de expandir/colapsar menú
        self.menu_frame.grid_rowconfigure(1, weight=0)
        self.menu_frame.grid_rowconfigure(2, weight=0)
        self.menu_frame.grid_rowconfigure(3, weight=0)
        self.menu_frame.grid_rowconfigure(4, weight=0)
        self.menu_frame.grid_rowconfigure(5, weight=0)  # Rellena el espacio vertical
        self.menu_frame.grid_rowconfigure(6, weight=0)  # Botón de cerrar sesión

        '''# Botón de colapsar/expandir menú
        self.btn_toggle_menu = tk.Button(self.menu_frame, text='<<', command=self.toggle_menu)
        self.btn_toggle_menu.grid(row=0, column=0, pady=10, sticky="w")'''

        # Botones de navegación del menú
        self.btn_page1 = tk.Button(self.menu_frame, text="Ingreso de pago", command=self.mostrar_pagina1)
        self.btn_page1.grid(row=1, column=0, pady=10, sticky="w")
        self.btn_page2 = tk.Button(self.menu_frame, text="Ingreso comisionista", command=self.mostrar_pagina2)
        self.btn_page2.grid(row=2, column=0, pady=10, sticky="w")
        self.btn_page3 = tk.Button(self.menu_frame, text="Ingreso lote", command=self.mostrar_pagina3)
        self.btn_page3.grid(row=3, column=0, pady=10, sticky="w")
        self.btn_page4 = tk.Button(self.menu_frame, text="Ver lotes", command=self.mostrar_pagina4)  # Botón de la página 4
        self.btn_page4.grid(row=4, column=0, pady=10, sticky="w")
        self.btn_page5 = tk.Button(self.menu_frame, text="Reportes", command=self.mostrar_pagina5)  # Botón de la página 5
        self.btn_page5.grid(row=5, column=0, pady=10, sticky="w")

        '''# Botón de cerrar sesión, anclado al fondo
        self.btn_logout = tk.Button(self.menu_frame, text="Cerrar Sesión", command=self.logout)
        self.btn_logout.grid(row=6, column=0, pady=10, sticky="s")  # Anclado al fondo con sticky='s'''

        # Frame del contenido donde se cargarán las páginas
        self.contenido_frame = tk.Frame(self)
        self.contenido_frame.grid(row=0, column=1, sticky='nsew')
        self.contenido_frame.columnconfigure(0, weight=1)

        self.mostrar_pagina1()

    def toggle_menu(self):
        if self.menu_colapsado:
            self.menu_frame.config(width=200)
            self.btn_toggle_menu.config(text='<<')
            self.btn_page1.config(text="Ingreso de pago")
            self.btn_page2.config(text="Ingreso comisionista")
            self.btn_page3.config(text="Ingreso lote")
            self.btn_page4.config(text="Ver lotes")  # Expandir texto de página 4
            self.btn_logout.config(text="Cerrar Sesión")
        else:
            self.menu_frame.config(width=50)
            self.btn_toggle_menu.config(text='>>')
            self.btn_page1.config(text="P1")
            self.btn_page2.config(text="P2")
            self.btn_page3.config(text="P3")
            self.btn_page4.config(text="P4")  # Contraer texto de página 4
            self.btn_logout.config(text="CS")

        self.menu_colapsado = not self.menu_colapsado

    def mostrar_pagina1(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        p.crear_ingreso_pago(self.contenido_frame, self.conn)

    def mostrar_pagina2(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        c.crear_ingreso_comisionista(self.contenido_frame, self.conn)

    def mostrar_pagina3(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        l.crear_ingreso_lote(self.contenido_frame, self.conn)

    def mostrar_pagina4(self):  # Función para cargar la página 4
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        vl.crear_ver_lotes(self.contenido_frame, self.conn)
    
    def mostrar_pagina5(self):  # Función para cargar la página 4
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        vr.mostrar_pagina_reportes(self.contenido_frame, self.conn)

    def logout(self):
        self.destroy()
        self.__init__()

if __name__ == "__main__":
    app = App()
    app.mainloop()
