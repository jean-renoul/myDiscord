import tkinter as tk
from tkinter import *
from tkinter import messagebox

class Graphic:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Discord")
        self.root.geometry("900x540")

        # Création d'un widget Canvas pour afficher l'image de fond
        self.canvas = tk.Canvas(self.root, width=900, height=540, bg="#2c2f33")  # Changer la couleur de fond ici
        self.canvas.pack()

        # Chargement de l'autre image
        self.image_haut_milieu = tk.PhotoImage(file="images/Titre.png")

        # Affichage de l'autre image en haut au milieu
        self.canvas.create_image(450, 0, anchor=tk.N, image=self.image_haut_milieu)

        # Création des boutons
        self.button_textuel = Button(self.canvas, text="Salons Textuels", width=15, borderwidth=0, bg="#7289da", fg="white", font=("Segoe UI", 15), command=self.show_textual_rooms)
        self.button_vocal = Button(self.canvas, text="Salons Vocaux", width=15, borderwidth=0, bg="#7289da", fg="white", font=("Segoe UI", 15), command=self.show_vocal_rooms)

        # Placement des boutons
        self.canvas.create_window(25, 80, anchor=tk.NW, window=self.button_textuel)
        self.canvas.create_window(25, 150, anchor=tk.NW, window=self.button_vocal)

        # Création de la zone de chat
        self.chat_text = Text(self.canvas, bg="grey", fg="black", font=("Segoe UI", 12), bd=0, width=50, height=18)
        self.chat_text_window = self.canvas.create_window(450, 270, anchor=tk.CENTER, window=self.chat_text)

        # Création de la barre de saisie de message
        self.message_entry = Entry(self.canvas, bg="grey", fg="black", font=("Segoe UI", 12), bd=0, width=50)
        self.message_entry_window = self.canvas.create_window(450, 510, anchor=tk.CENTER, window=self.message_entry)

        # Création du bouton d'envoi
        self.send_button = Button(self.canvas, text="Envoyer", bg="#7289da", fg="white", borderwidth=0, font=("Segoe UI", 12), command=self.send_message)
        self.send_button_window = self.canvas.create_window(720, 510, anchor=tk.CENTER, window=self.send_button)

    def show_textual_rooms(self):
        # Création de la fenêtre modale pour afficher les salons textuels
        self.textual_window = tk.Toplevel(self.root)
        self.textual_window.title("Salons Textuels")
        self.textual_window.geometry("300x200")

        # Liste des salons textuels existants
        textual_rooms = ["Salon 1", "Salon 2", "Salon 3"]

        # Création de la liste déroulante pour les salons textuels
        selected_room = tk.StringVar(self.textual_window)
        selected_room.set(textual_rooms[0])  # Valeur par défaut

        room_menu = OptionMenu(self.textual_window, selected_room, *textual_rooms)
        room_menu.pack(pady=10)

        # Bouton pour créer un nouveau salon
        create_button = Button(self.textual_window, text="Créer un nouveau salon", command=self.create_new_room)
        create_button.pack(pady=10)

    def show_vocal_rooms(self):
        # Création de la fenêtre modale pour afficher les salons vocaux
        self.vocal_window = tk.Toplevel(self.root)
        self.vocal_window.title("Salons Vocaux")
        self.vocal_window.geometry("300x200")

        # Liste des salons vocaux existants
        vocal_rooms = ["Salon vocal A", "Salon vocal B", "Salon vocal C"]

        # Création de la liste déroulante pour les salons vocaux
        selected_room = tk.StringVar(self.vocal_window)
        selected_room.set(vocal_rooms[0])  # Valeur par défaut

        room_menu = OptionMenu(self.vocal_window, selected_room, *vocal_rooms)
        room_menu.pack(pady=10)

        # Bouton pour créer un nouveau salon vocal
        create_button = Button(self.vocal_window, text="Créer un nouveau salon vocal", command=self.create_new_vocal_room)
        create_button.pack(pady=10)

    def create_new_room(self):
        # Fonction à exécuter lors de la création d'un nouveau salon
        messagebox.showinfo("Nouveau salon créé", "Vous avez créé un nouveau salon !")

    def create_new_vocal_room(self):
        # Fonction à exécuter lors de la création d'un nouveau salon vocal
        messagebox.showinfo("Nouveau salon vocal créé", "Vous avez créé un nouveau salon vocal !")

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