import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from Class.Db import *
import os

class Login:
    def __init__(self):
        self.db_instance = Db('82.165.185.52', 'jean-renoul', 'patesaup0ulet', 'jean-renoul_discord')
        self.userInfo = []
        self.windows = tk.Tk()
        self.windows.title("Login")
        self.windows.geometry("600x300")
        self.windows.resizable(False, False)       

        frame = Frame(self.windows, width=600, height=300, bg="#2c2f33", bd=5)
        frame.place(x=0, y=0)

        heading = Label(frame, text="Se connecter", fg="white", bg="#2c2f33", font=("Segoe UI", 30))
        heading.place(x=180, y=10)

        Logo_Mail = Image.open("images/logo_mail.png")
        Logo_Mail = Logo_Mail.resize((30, 30), Image.LANCZOS)
        self.logo_mail_image = ImageTk.PhotoImage(Logo_Mail)
        emailLabel = Label(frame, text="Email :", image=self.logo_mail_image, compound="left", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        emailLabel.place(x=100, y=100)

        Logo_Password = Image.open("images/logo_password.png")
        Logo_Password = Logo_Password.resize((30, 30), Image.LANCZOS)
        self.logo_password_image = ImageTk.PhotoImage(Logo_Password)
        passwordLabel = Label(frame, text="Password :", image=self.logo_password_image, compound="left", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        passwordLabel.place(x=100, y=150)

        self.email_entry = Entry(frame, width=30)
        self.email_entry.place(x=250, y=110)

        self.password_entry = Entry(frame, width=30, show="*")
        self.password_entry.place(x=250, y=160)

        login_button = Button(frame, text="connexion", width=20, borderwidth=0, bg="#7289da", fg="white", font=("Segoe UI", 15), command=self.check_login)
        login_button.place(x=340, y=240)

        donthaveaccount = Label (frame, text="Je n'ai pas de compte", fg="white", bg="#2c2f33", font=("Segoe UI", 10))
        donthaveaccount.place(x=110, y=230)
        donthaveaccount_button = Button(frame, text="S'inscrire", width=10, borderwidth=0, bg="#7289da", fg="white", font=("Segoe UI", 10), command=lambda: self.newone())
        donthaveaccount_button.place(x=130, y=260)

    def newone(self):
        self.windows.destroy()
        #os.system('python Class/register.py')

    def check_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Requête pour vérifier les informations de connexion dans la base de données
        query = "SELECT * FROM users WHERE email = %s AND mdp = %s"
        result = self.db_instance.fetch(query, (email, password))

        if result:
            messagebox.showinfo("Succès", "Vous êtes connecté avec succès!")
            self.windows.destroy()  # Ferme la fenêtre de connexion
            self.userInfo = result[0]
            #os.system('python Class/Graphic.py')  # Lance la page Graphic.py
        else:
            messagebox.showerror("Erreur", "Adresse e-mail ou mot de passe incorrect")


if __name__ == "__main__":
    app = Login()
    app.windows.mainloop()