from tkinter import * # Import tkinter

windows = Tk() # Creation de la fenetre tkinter
windows.title("Register") # Titre de la fenetre
windows.geometry("900x540") # Taille de la fenetre
windows.resizable(False, False) # Taille de la fenetre non modifiable

# Ajout de la couleur de fond
frame = Frame(windows, width=900, height=540, bg="#2c2f33", bd=5)
frame.place(x=0, y=0)

windows.mainloop() # Boucle principale