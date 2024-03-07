import tkinter as tk
from tkinter import *
from tkinter import messagebox
from Class.Db import *

class Register:
    def __init__(self):
        self.db_instance = Db('82.165.185.52', 'jean-renoul', 'patesaup0ulet', 'jean-renoul_discord') # Connexion à la base de données
        self.userInfo = [] # Liste pour stocker les informations de l'utilisateur

        self.windows = tk.Tk() # Création de la fenêtre
        self.windows.title("Register")
        self.windows.geometry("900x540") 
        self.windows.resizable(False, False) # Empêche le redimensionnement de la fenêtre

        frame = Frame(self.windows, width=900, height=540, bg="#2c2f33", bd=5) # Création d'un cadre pour la fenêtre
        frame.place(x=0, y=0) # Positionnement du cadre

        heading = Label(frame, text="S'inscrire sur Discord", fg="white", bg="#2c2f33", font=("Segoe UI", 30))
        heading.place(x=250, y=10)

        self.firstname = Label(frame, text="Prénom :", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        self.firstname.place(x=340, y=100)
        self.firstname_entry = Entry(frame, width=30) # Création d'un champ de saisie pour le prénom
        self.firstname_entry.place(x=342, y=140)

        self.lastname = Label(frame, text="Nom :", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        self.lastname.place(x=340, y=170)
        self.lastname_entry = Entry(frame, width=30) # Création d'un champ de saisie pour le nom
        self.lastname_entry.place(x=342, y=210)

        self.email = Label(frame, text="Email :", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        self.email.place(x=340, y=240)
        self.email_entry = Entry(frame, width=30) # Création d'un champ de saisie pour l'email
        self.email_entry.place(x=342, y=280)

        self.password = Label(frame, text="Mot de passe :", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        self.password.place(x=340, y=310)
        self.password_entry = Entry(frame, width=30, show="*") # Création d'un champ de saisie pour le mot de passe
        self.password_entry.place(x=342, y=350)

        register_button = Button(frame, text="Valider l'inscription", width=20, borderwidth=0, bg="#7289da", fg="white", font=("Segoe UI", 15), command=self.submit)
        register_button.place(x=325, y=400)

    def submit(self):
        firstname = self.firstname_entry.get() # Récupération du prénom
        lastname = self.lastname_entry.get() # Récupération du nom
        email = self.email_entry.get() # Récupération de l'email
        password = self.password_entry.get() # Récupération du mot de passe

        if firstname == "" or lastname == "" or email == "" or password == "": # Vérification si tous les champs sont remplis
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
        else:
            params = (firstname, lastname, email, password) # Création d'un tuple pour stocker les informations de l'utilisateur
            self.db_instance.executeQuery("INSERT INTO users (prenom, nom, email, mdp) VALUES (%s, %s, %s, %s)", params) # Requête pour insérer les informations de l'utilisateur dans la base de données
            users = self.db_instance.fetch("SELECT users FROM channel WHERE name = %s", ("general",)) # Récupération des utilisateurs du channel général
            users = users[0][0] # Récupération de la liste des utilisateurs
            users = users + email + "," # Ajout du nouvel utilisateur à la liste
            self.db_instance.executeQuery("UPDATE channel SET users = %s WHERE name = %s", (users,"general")) # Mise à jour de la liste des utilisateurs
            self.userInfo = [firstname, lastname, email, password] # Ajout des informations de l'utilisateur à la liste
            messagebox.showinfo("Succès", "Inscription réussie") # Affichage d'un message de succès
            self.windows.destroy() # Ferme la fenêtre d'inscription

#if __name__ == "__main__":
#    app = Register()
#    app.windows.mainloop()