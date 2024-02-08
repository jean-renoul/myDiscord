import tkinter as tk
from tkinter import *
from tkinter import messagebox

class Graphic:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Discord")
        self.root.geometry("900x540")

        # Chargement de l'image de fond
        self.image_fond = tk.PhotoImage(file="myDiscord/fond.png")

        # Création d'un widget Canvas pour afficher l'image de fond
        self.canvas = tk.Canvas(self.root, width=900, height=540)
        self.canvas.pack()

        # Affichage de l'image de fond
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_fond)

        # Chargement de l'autre image
        self.image_haut_milieu = tk.PhotoImage(file="myDiscord/Titre.png")

        # Affichage de l'autre image en haut au milieu
        self.canvas.create_image(450, 0, anchor=tk.N, image=self.image_haut_milieu)

        # Création des boutons
        self.button_textuel = Button(self.canvas, text="Salons Textuels", width=15, borderwidth=0, bg="#7289da", fg="white", font=("Segoe UI", 15), command=self.textual_clicked)
        self.button_vocal = Button(self.canvas, text="Salons Vocaux", width=15, borderwidth=0, bg="#7289da", fg="white", font=("Segoe UI", 15), command=self.vocal_clicked)

        # Placement des boutons plus en haut à gauche avec un espacement
        self.canvas.create_window(25, 75, anchor=tk.NW, window=self.button_textuel)
        self.canvas.create_window(25, 150, anchor=tk.NW, window=self.button_vocal)

        # Création de la zone de chat
        self.chat_text = Text(self.canvas, bg="grey", fg="black", font=("Segoe UI", 12), bd=0, width=50, height=18)
        self.chat_text_window = self.canvas.create_window(450, 270, anchor=tk.CENTER, window=self.chat_text)

        # Création de la barre de saisie de message
        self.message_entry = Entry(self.canvas, bg="grey", fg="black", font=("Segoe UI", 12), bd=0, width=50)
        self.message_entry_window = self.canvas.create_window(450, 510, anchor=tk.CENTER, window=self.message_entry)

        # Création du bouton d'envoi
        self.send_button = Button(self.canvas, text="Envoyer", bg="#7289da", fg="white", font=("Segoe UI", 12), command=self.send_message)
        self.send_button_window = self.canvas.create_window(720, 510, anchor=tk.CENTER, window=self.send_button)

    def textual_clicked(self):
        messagebox.showinfo("Information", "Bouton Salon Textuel cliqué")

    def vocal_clicked(self):
        messagebox.showinfo("Information", "Bouton Salon Vocal cliqué")

    def send_message(self):
        message = self.message_entry.get()
        if message:
            # Ajout du message à la zone de chat
            self.chat_text.insert(tk.END, message + "\n")
            self.message_entry.delete(0, tk.END)

    def afficher(self):
        self.root.mainloop()

# Instanciation de la classe et appel de la méthode pour afficher la fenêtre
app = Graphic()
app.afficher()
