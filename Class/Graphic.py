import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os
import customtkinter

class Graphic:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Discord")
        self.root.geometry("900x540")
        self.root.resizable(False, False)



        # Création d'un widget Canvas avec un fond rouge
        self.canvas = tk.Canvas(self.root, width=900, height=540, bg="#2c2f33")

        # Charger l'image Titre.png
        self.image_haut_milieu = tk.PhotoImage(file="images/Titre.png")

        # Afficher l'image au centre en haut
        self.canvas.create_image(450, 0, anchor=tk.N, image=self.image_haut_milieu)
        self.canvas.pack()  # N'oubliez pas d'emballer le canvas

        # Création du bouton de déconnexion
        self.button_logout = Button(self.canvas, text="Se déconnecter", width=15, borderwidth=0, bg="#7289da", fg="white", font=("Segoe UI", 15), command=self.logout)
        self.canvas.create_window(25, 450, anchor=tk.NW, window=self.button_logout)

        # Création de la zone de chat
        self.chat_text = Text(self.canvas, bg="grey", fg="black", font=("Segoe UI", 12), bd=0, width=50, height=18, state="disabled")
        self.chat_text_window = self.canvas.create_window(450, 270, anchor=tk.CENTER, window=self.chat_text)

        # Création de la barre de saisie de message
        self.message_entry = Entry(self.canvas, bg="grey", fg="black", font=("Segoe UI", 12), bd=0, width=50)
        self.message_entry_window = self.canvas.create_window(450, 510, anchor=tk.CENTER, window=self.message_entry)

        # Création du bouton d'envoi
        self.send_button = Button(self.canvas, text="Envoyer", bg="#7289da", fg="white", borderwidth=0, font=("Segoe UI", 12), command=self.send_message)
        self.send_button_window = self.canvas.create_window(720, 510, anchor=tk.CENTER, window=self.send_button)

        # Création de la barre de défilement
        self.scrollbar = Scrollbar(self.canvas, orient="vertical", command=self.chat_text.yview)
        self.scrollbar_window = self.canvas.create_window(694, 270, anchor=tk.E, window=self.scrollbar, height=380)

        Salons_textuels = ["Salon 1", "Salon 2", "Salon 3"]  # Suppression de "Salons textuels" de la liste déroulante

        my_option = customtkinter.CTkOptionMenu(self.root, values=Salons_textuels)
        my_option.set("Salons textuels")  # Définition de "Salons textuels" comme valeur par défaut

        # Décalage des menus déroulants vers la gauche
        my_option.place(relx=0.025, rely=0.15)  # Réglez relx et rely selon vos besoins
        Salons_vocaux = ["Salon vocal A", "Salon vocal B", "Salon vocal C"]  # Suppression de "Salons textuels" de la liste déroulante

        my_option2 = customtkinter.CTkOptionMenu(self.root, values=Salons_vocaux)
        my_option2.set("Salons vocaux")  # Définition de "Salons textuels" comme valeur par défaut
        my_option2.place(relx=0.025, rely=0.5)  # Réglez relx et rely selon vos besoins
        # Connecter la barre de défilement à la zone de texte
        self.chat_text.config(yscrollcommand=self.scrollbar.set)

        self.update_gui()

    def update_gui(self):
        self.root.update_idletasks()
        self.root.update()

    def logout(self):
        self.root.destroy()
        os.system('python Class/login.py')

    def send_message(self):
        message = self.message_entry.get()
        if message:
            # Activer la zone de chat pour ajouter le message
            self.chat_text.config(state="normal")

            # Ajout du message à la zone de chat
            self.chat_text.insert(tk.END, message + "\n")
            self.message_entry.delete(0, tk.END)

            # Désactiver la zone de chat à nouveau
            self.chat_text.config(state="disabled")
            return message


    def receive_message(self, message):
        # Activer la zone de chat pour ajouter le message
        self.chat_text.config(state="normal")

        # Ajout du message à la zone de chat
        self.chat_text.insert(tk.END, message + "\n")

        # Désactiver la zone de chat à nouveau
        self.chat_text.config(state="disabled")

    def afficher(self):
        self.root.mainloop()

    

    

# Instanciation de la classe et appel de la méthode pour afficher la fenêtre
#app = Graphic()
#app.afficher()
