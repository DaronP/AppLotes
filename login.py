import tkinter as tk
from tkinter import messagebox

class LoginPage(tk.Frame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.on_login_success = on_login_success
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.label_user = tk.Label(self, text="Usuario:")
        self.label_user.grid(row=0, column=0, padx=10, pady=10)
        self.entry_user = tk.Entry(self)
        self.entry_user.grid(row=0, column=1, padx=10, pady=10)

        self.label_password = tk.Label(self, text="Contraseña:")
        self.label_password.grid(row=1, column=0, padx=10, pady=10)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        self.login_button = tk.Button(self, text="Login", command=self.check_credentials)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Login on pressing Enter
        self.entry_password.bind('<Return>', lambda event: self.check_credentials())

    def check_credentials(self):
        # Dummy credentials
        username = self.entry_user.get()
        password = self.entry_password.get()
        if username == "admin" and password == "admin123" or username == "" and password == "":
            self.on_login_success()
        else:
            messagebox.showerror("Error", "Credenciales Incorrectas")

# main_app.py can call `LoginPage` before opening the rest of the app.
