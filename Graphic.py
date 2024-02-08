import tkinter as tk

class Graphic:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("D")
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

    def afficher(self):
        self.root.mainloop()

# Instanciation de la classe et appel de la méthode pour afficher la fenêtre
app = Graphic()
app.afficher()

