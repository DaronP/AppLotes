import tkinter as tk
from login import LoginPage
import pages.ingreso_pago as p
import pages.ingreso_comisionista as c 
import pages.ingreso_lote as l
import pages.ver_lotes as vl

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1280x720')
        self.title('App con Expandable Menu')
        self.center_window()

        self.menu_colapsado = False

        # Mostrar la pantalla de Login primero
        self.show_login()

    def center_window(self):
        self.update_idletasks()
        width = 1280
        height = 720
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def show_login(self):
        self.login_page = LoginPage(self, self.on_login_success)
        self.login_page.pack(fill="both", expand=True)

    def on_login_success(self):
        self.login_page.destroy()
        self.create_main_app()

    def create_main_app(self):
        # Configurar las columnas del grid
        self.grid_columnconfigure(0, weight=0)  # Menú
        self.grid_columnconfigure(1, weight=1)  # Contenido

        # Frame del menú expandible
        self.menu_frame = tk.Frame(self, bg="lightgrey")
        self.menu_frame.grid(row=0, column=0, sticky='ns')  # Expande el menú de arriba a abajo
        self.menu_frame.grid_propagate(False)
        self.menu_frame.config(width=150, height=720)

        # Crear un grid layout para el menú
        self.menu_frame.grid_rowconfigure(0, weight=0)  # Botón de expandir/colapsar menú
        self.menu_frame.grid_rowconfigure(1, weight=0)
        self.menu_frame.grid_rowconfigure(2, weight=0)
        self.menu_frame.grid_rowconfigure(3, weight=0)
        self.menu_frame.grid_rowconfigure(4, weight=0)
        self.menu_frame.grid_rowconfigure(5, weight=1)  # Rellena el espacio vertical
        self.menu_frame.grid_rowconfigure(6, weight=0)  # Botón de cerrar sesión

        # Botón de colapsar/expandir menú
        self.btn_toggle_menu = tk.Button(self.menu_frame, text='<<', command=self.toggle_menu)
        self.btn_toggle_menu.grid(row=0, column=0, pady=10, sticky="w")

        # Botones de navegación del menú
        self.btn_page1 = tk.Button(self.menu_frame, text="Página 1", command=self.mostrar_pagina1)
        self.btn_page1.grid(row=1, column=0, pady=10, sticky="w")
        self.btn_page2 = tk.Button(self.menu_frame, text="Página 2", command=self.mostrar_pagina2)
        self.btn_page2.grid(row=2, column=0, pady=10, sticky="w")
        self.btn_page3 = tk.Button(self.menu_frame, text="Página 3", command=self.mostrar_pagina3)
        self.btn_page3.grid(row=3, column=0, pady=10, sticky="w")
        self.btn_page4 = tk.Button(self.menu_frame, text="Página 4", command=self.mostrar_pagina4)  # Botón de la página 4
        self.btn_page4.grid(row=4, column=0, pady=10, sticky="w")

        # Botón de cerrar sesión, anclado al fondo
        self.btn_logout = tk.Button(self.menu_frame, text="Cerrar Sesión", command=self.logout)
        self.btn_logout.grid(row=6, column=0, pady=10, sticky="s")  # Anclado al fondo con sticky='s'

        # Frame del contenido donde se cargarán las páginas
        self.contenido_frame = tk.Frame(self)
        self.contenido_frame.grid(row=0, column=1, sticky='nsew')
        self.contenido_frame.columnconfigure(0, weight=1)

        self.mostrar_pagina1()

    def toggle_menu(self):
        if self.menu_colapsado:
            self.menu_frame.config(width=200)
            self.btn_toggle_menu.config(text='<<')
            self.btn_page1.config(text="Página 1")
            self.btn_page2.config(text="Página 2")
            self.btn_page3.config(text="Página 3")
            self.btn_page4.config(text="Página 4")  # Expandir texto de página 4
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
        p.crear_ingreso_pago(self.contenido_frame)

    def mostrar_pagina2(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        c.crear_ingreso_comisionista(self.contenido_frame)

    def mostrar_pagina3(self):
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        l.crear_ingreso_lote(self.contenido_frame)

    def mostrar_pagina4(self):  # Función para cargar la página 4
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        vl.crear_ver_lotes(self.contenido_frame)

    def logout(self):
        self.destroy()
        self.__init__()

if __name__ == "__main__":
    app = App()
    app.mainloop()
