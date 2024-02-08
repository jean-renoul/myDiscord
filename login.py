import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

class Login:
    def __init__(self):
        self.windows = tk.Tk()  # Création de l'objet Tk
        self.windows.title("Login")
        self.windows.geometry("600x300")
        self.windows.resizable(False, False)

        # Ajout de la couleur de fond
        frame = Frame(self.windows, width=600, height=300, bg="#2c2f33", bd=5)
        frame.place(x=0, y=0)

        # Mail
        Logo_Mail = Image.open("images/logo_mail.png")
        Logo_Mail = Logo_Mail.resize((50, 50), Image.LANCZOS)
        self.logo_mail_image = ImageTk.PhotoImage(Logo_Mail)
        emailLabel = Label(frame, text="Email :", image=self.logo_mail_image, compound="left", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        emailLabel.place(x=10, y=100)

        # Password
        Logo_Password = Image.open("images/logo_password.png")
        Logo_Password = Logo_Password.resize((50, 50), Image.LANCZOS)
        self.logo_password_image = ImageTk.PhotoImage(Logo_Password)
        passwordLabel = Label(frame, text="Password :", image=self.logo_password_image, compound="left", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        passwordLabel.place(x=10, y=150)

        # Les entrées
        email_entry = Entry(frame, width=30)
        email_entry.place(x=150, y=100)

        password_entry = Entry(frame, width=30, show="*")
        password_entry.place(x=150, y=150)

if __name__ == "__main__":
    app = Login()  # Création de l'instance de la classe Login
    app.windows.mainloop()  # Lancement de la boucle principale
