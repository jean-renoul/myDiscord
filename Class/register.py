import tkinter as tk
from tkinter import *
from tkinter import messagebox
from Class.Db import *

class Register:
    def __init__(self):
        self.db_instance = Db('82.165.185.52', 'jean-renoul', 'patesaup0ulet', 'jean-renoul_discord')
        self.userInfo = []

        self.windows = tk.Tk()
        self.windows.title("Register")
        self.windows.geometry("900x540")
        self.windows.resizable(False, False)

        frame = Frame(self.windows, width=900, height=540, bg="#2c2f33", bd=5)
        frame.place(x=0, y=0)

        heading = Label(frame, text="S'inscrire sur Discord", fg="white", bg="#2c2f33", font=("Segoe UI", 30))
        heading.place(x=250, y=10)

        self.firstname = Label(frame, text="Prénom :", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        self.firstname.place(x=340, y=100)
        self.firstname_entry = Entry(frame, width=30)
        self.firstname_entry.place(x=342, y=140)

        self.lastname = Label(frame, text="Nom :", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        self.lastname.place(x=340, y=170)
        self.lastname_entry = Entry(frame, width=30)
        self.lastname_entry.place(x=342, y=210)

        self.email = Label(frame, text="Email :", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        self.email.place(x=340, y=240)
        self.email_entry = Entry(frame, width=30)
        self.email_entry.place(x=342, y=280)

        self.password = Label(frame, text="Mot de passe :", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        self.password.place(x=340, y=310)
        self.password_entry = Entry(frame, width=30, show="*")
        self.password_entry.place(x=342, y=350)

        register_button = Button(frame, text="Valider l'inscription", width=20, borderwidth=0, bg="#7289da", fg="white", font=("Segoe UI", 15), command=self.submit)
        register_button.place(x=325, y=400)

    def submit(self):
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if firstname == "" or lastname == "" or email == "" or password == "":
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
        else:
            params = (firstname, lastname, email, password)
            self.db_instance.executeQuery("INSERT INTO users (prenom, nom, email, mdp) VALUES (%s, %s, %s, %s)", params)
            self.userInfo = [firstname, lastname, email, password]
            messagebox.showinfo("Succès", "Inscription réussie")
            self.windows.destroy()

#if __name__ == "__main__":
#    app = Register()
#    app.windows.mainloop()