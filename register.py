import tkinter
from tkinter import * # Import tkinter


class Register:
    def __init__(self, windows):
        self.windows = windows
        self.windows.title("Register")
        self.windows.geometry("900x540")
        self.windows.resizable(False, False)

        # Ajout de la couleur de fond
        frame = Frame(windows, width=900, height=540, bg="#2c2f33", bd=5)
        frame.place(x=0, y=0)

        # Titre de la page
        heading = Label(frame, text="S'inscrire sur Discord", fg="white", bg="#2c2f33", font=("Segoe UI", 30))
        heading.place(x=300, y=10)

        # Prénom
        firstname = Label(frame, text="Prénom :", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        firstname.place(x=300, y=100)
        firstname_entry = Entry(frame, width=30,) # border-radius=2 pour arrondir les bords (Windows uniquement)
        firstname_entry.place(x=302, y=140)

        # Nom
        lastname = Label(frame, text="Nom :", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        lastname.place(x=300, y=170)
        lastname_entry = Entry(frame, width=30,)
        lastname_entry.place(x=302, y=210)

        # Email
        email = Label(frame, text="Email :", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        email.place(x=300, y=240)
        email_entry = Entry(frame, width=30,)
        email_entry.place(x=302, y=280)

        # Mot de passe
        password = Label(frame, text="Mot de passe :", fg="#7289da", bg="#2c2f33", font=("Segoe UI", 17))
        password.place(x=300, y=310)
        password_entry = Entry(frame, width=30, show="*") # show="*" pour cacher le mot de passe
        password_entry.place(x=302, y=350)


if __name__ == "__main__":
    windows = Tk()  # Création de l'objet Tk
    app = Register(windows)  # Création de l'instance de la classe Register
    windows.mainloop()  # Boucle principale