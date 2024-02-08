import tkinter as tk
from tkinter import *

class Login:
    def __init__(self):
        self.windows = tk.Tk()  # Création de l'objet Tk
        self.windows.title("Login")
        self.windows.geometry("600x300")
        self.windows.resizable(False, False)

        # Ajout de la couleur de fond
        frame = Frame(self.windows, width=600, height=300, bg="#2c2f33", bd=5)
        frame.place(x=0, y=0)

if __name__ == "__main__":
        app = Login()  # Création de l'instance de la classe Login
        app.windows.mainloop()  # Lancement de la boucle principale