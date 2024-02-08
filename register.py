import tkinter as tk
from tkinter import * # Import tkinter
from tkinter import messagebox # Import messagebox

class Register:
    def __init__(self):
        self.windows = tk.Tk()  # Création de l'objet Tk
        self.windows.title("Register")
        self.windows.geometry("900x540")
        self.windows.resizable(False, False)

        # Ajout de la couleur de fond
        frame = Frame(self.windows, width=900, height=540, bg="#2c2f33", bd=5)
        frame.place(x=0, y=0)

        # Titre de la page
        heading = Label(frame, text="S'inscrire sur Discord", fg="white", bg="#2c2f33", font=("Segoe UI", 30))
        heading.place(x=300, y=10)

        # Prénom
        self.firstname = Label(frame, text="Prénom :", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        self.firstname.place(x=300, y=100)
        self.firstname_entry = Entry(frame, width=30,) # border-radius=2 pour arrondir les bords (Windows uniquement)
        self.firstname_entry.place(x=302, y=140)

        # Nom
        self.lastname = Label(frame, text="Nom :", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        self.lastname.place(x=300, y=170)
        self.lastname_entry = Entry(frame, width=30,)
        self.lastname_entry.place(x=302, y=210)

        # Email
        self.email = Label(frame, text="Email :", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        self.email.place(x=300, y=240)
        self.email_entry = Entry(frame, width=30,)
        self.email_entry.place(x=302, y=280)

        # Mot de passe
        self.password = Label(frame, text="Mot de passe :", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        self.password.place(x=300, y=310)
        self.password_entry = Entry(frame, width=30, show="*") # show="*" pour cacher le mot de passe
        self.password_entry.place(x=302, y=350)

        # Bouton d'inscription
        register_button = Button(frame, text="Valider l'inscription", width=20, borderwidth=0, bg="#7289da", fg="white", font=("Segoe UI", 15), command=self.submit)
        register_button.place(x=300, y=400)

    def submit(self):
        if self.firstname_entry.get() == "":
            messagebox.showerror("Erreur", "Veuillez entrer votre prénom")
            return
        elif self.lastname_entry.get() == "":
            messagebox.showerror("Erreur", "Veuillez entrer votre nom")
            return
        elif self.email_entry.get() == "":
            messagebox.showerror("Erreur", "Veuillez entrer votre email")
            return
        elif self.password_entry.get() == "":
            messagebox.showerror("Erreur", "Veuillez entrer votre mot de passe")
            return
        else:
            pass

if __name__ == "__main__":
    app = Register()  # Création de l'instance de la classe Register
    app.windows.mainloop()  # Boucle principale
