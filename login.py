import tkinter as tk
from tkinter import messagebox
from db import execute_query, execute_non_query

class LoginPage(tk.Frame):
    def __init__(self, parent, conn, on_login_success):
        self.parent = parent
        self.on_login_success = on_login_success

        # Configurar el tamaño y centrar el contenido de la ventana de login

        # Frame para contener los campos de login y centrarlos
        login_frame = tk.Frame(self.parent)
        login_frame.pack(expand=True)  # Expand para centrar en la ventana

        # Crear los campos de entrada con pack() para un diseño centrado
        tk.Label(login_frame, text="Usuario:").pack(anchor="w", pady=5)
        self.username_entry = tk.Entry(login_frame)
        self.username_entry.pack(fill="x", pady=5)

        tk.Label(login_frame, text="Contraseña:").pack(anchor="w", pady=5)
        self.password_entry = tk.Entry(login_frame, show="*")
        self.password_entry.pack(fill="x", pady=5)

        # Botón de login
        self.login_button = tk.Button(login_frame, text="Iniciar Sesión", command=self.verify_credentials())
        self.login_button.pack(pady=10)

        # Asegurarse de que el botón responda al presionar 'Enter'
        self.username_entry.bind("<Return>", lambda event: self.verify_credentials())
        self.password_entry.bind("<Return>", lambda event: self.verify_credentials())

    def verify_credentials(self):
        # Lógica de verificación de credenciales
        username = self.username_entry.get()
        password = self.password_entry.get()

        #result = execute_query(conn, 'SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s', (username, password))

        # Validación simple de credenciales
        if username == "admin" and password == "password" or username == "" and password == "":
            self.on_login_success()
        else:
            self.show_error("Credenciales incorrectas")

    def show_error(self, message):
        # Mostrar el mensaje de error
        messagebox.showinfo("Error", message)

