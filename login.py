import tkinter as tk
from tkinter import *

class Login:
    def __init__(self):
        self.windows = tk.Tk()  # Création de l'objet Tk
        self.windows.title("Login")
        self.windows.geometry("600x300")
        self.windows.resizable(False, False)

if __name__ == "__main__":
        app = Login()  # Création de l'instance de la classe Login
        app.windows.mainloop()  # Lancement de la boucle principale