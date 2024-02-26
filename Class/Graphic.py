import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import customtkinter
from Class.Db import *

class Graphic:
    def __init__(self, email):
        self.email = email
        self.root = tk.Tk()
        self.root.title("Discord")
        self.root.geometry("900x540")
        self.root.resizable(False, False)
        self.db_instance = Db('82.165.185.52', 'jean-renoul', 'patesaup0ulet', 'jean-renoul_discord')



        self.canvas = tk.Canvas(self.root, width=900, height=540, bg="#2c2f33")
        self.image_haut_milieu = tk.PhotoImage(file="images/Titre.png")
        self.canvas.create_image(450, 0, anchor=tk.N, image=self.image_haut_milieu)
        self.canvas.pack()

        self.button_logout = Button(self.canvas, text="Se déconnecter", width=15, borderwidth=0, bg="#7289da", fg="white", font=("Segoe UI", 15), command=self.logout)
        self.canvas.create_window(25, 450, anchor=tk.NW, window=self.button_logout)

        self.chat_text = Text(self.canvas, bg="grey", fg="black", font=("Segoe UI", 12), bd=0, width=50, height=18, state="disabled")
        self.chat_text_window = self.canvas.create_window(450, 270, anchor=tk.CENTER, window=self.chat_text)

        self.message_entry = Entry(self.canvas, bg="grey", fg="black", font=("Segoe UI", 12), bd=0, width=50)
        self.message_entry_window = self.canvas.create_window(450, 510, anchor=tk.CENTER, window=self.message_entry)

        self.send_button = Button(self.canvas, text="Envoyer", bg="#7289da", fg="white", borderwidth=0, font=("Segoe UI", 12), command=self.send_message)
        self.send_button_window = self.canvas.create_window(720, 510, anchor=tk.CENTER, window=self.send_button)

        emoji_data = [('emojis/u0001f44a.png', '\U0001F44A'), ('emojis/u0001f44c.png', '\U0001F44C'), ('emojis/u0001f44d.png', '\U0001F44D'),
                      ('emojis/u0001f495.png', '\U0001F495'), ('emojis/u0001f496.png', '\U0001F496'), ('emojis/u0001f4a6.png', '\U0001F4A6'),
                      ('emojis/u0001f4a9.png', '\U0001F4A9'), ('emojis/u0001f4af.png', '\U0001F4AF'), ('emojis/u0001f595.png', '\U0001F595'),
                      ('emojis/u0001f600.png', '\U0001F600'), ('emojis/u0001f602.png', '\U0001F602'), ('emojis/u0001f603.png', '\U0001F603'),
                      ('emojis/u0001f605.png', '\U0001F605'), ('emojis/u0001f606.png', '\U0001F606'), ('emojis/u0001f608.png', '\U0001F608'),
                      ('emojis/u0001f60d.png', '\U0001F60D'), ('emojis/u0001f60e.png', '\U0001F60E'), ('emojis/u0001f60f.png', '\U0001F60F'),
                      ('emojis/u0001f610.png', '\U0001F610'), ('emojis/u0001f618.png', '\U0001F618'), ('emojis/u0001f61b.png', '\U0001F61B'),
                      ('emojis/u0001f61d.png', '\U0001F61D'), ('emojis/u0001f621.png', '\U0001F621'), ('emojis/u0001f624.png', '\U0001F621'),
                      ('emojis/u0001f631.png', '\U0001F631'), ('emojis/u0001f632.png', '\U0001F632'), ('emojis/u0001f634.png', '\U0001F634'),
                      ('emojis/u0001f637.png', '\U0001F637'), ('emojis/u0001f642.png', '\U0001F642'), ('emojis/u0001f64f.png', '\U0001F64F'),
                      ('emojis/u0001f920.png', '\U0001F920'), ('emojis/u0001f923.png', '\U0001F923'), ('emojis/u0001f928.png', '\U0001F928')]

        emoji_x_pos = 720
        emoji_y_pos = 310
        for Emoji in emoji_data:
            emojis = Image.open(Emoji[0])
            emojis = emojis.resize((20, 20))
            emojis = ImageTk.PhotoImage(emojis)

            emoji_unicode = Emoji[1]
            emoji_label = tk.Label(self.canvas, image=emojis, text=emoji_unicode, bg="#2c2f33", cursor="hand2")
            emoji_label.image = emojis
            emoji_label.place(x=emoji_x_pos, y=emoji_y_pos)
            emoji_label.bind('<Button-1>', lambda x: self.insert_emoji(x))

            emoji_x_pos += 25
            cur_index = emoji_data.index(Emoji)
            if (cur_index + 1) % 6 == 0:
                emoji_y_pos += 25
                emoji_x_pos = 720

        self.scrollbar = Scrollbar(self.canvas, orient="vertical", command=self.chat_text.yview)
        self.scrollbar_window = self.canvas.create_window(694, 270, anchor=tk.E, window=self.scrollbar, height=380)
        self.chat_text.config(yscrollcommand=self.scrollbar.set)



        self.Salons_textuels = self.get_channels()
        self.Salons_vocaux = ["Salon vocal A", "Salon vocal B", "Salon vocal C"]

        my_option = customtkinter.CTkOptionMenu(self.root, values=self.Salons_textuels, command=self.select_channel)
        my_option.set("Salons textuels")
        my_option.place(relx=0.025, rely=0.15)

        my_option2 = customtkinter.CTkOptionMenu(self.root, values=self.Salons_vocaux)
        my_option2.set("Salons vocaux")
        my_option2.place(relx=0.025, rely=0.5)

        self.salons_textuels_menu = my_option
        self.salons_vocaux_menu = my_option2

        self.new_channel_entry = Entry(self.root, width=20, font=("Segoe UI", 12))
        self.new_channel_entry.place(relx=0.025, rely=0.3)

        self.create_channel_button = Button(self.root, text="Créer un salon", bg="#7289da", fg="white", font=("Segoe UI", 12), command=self.create_channel)
        self.create_channel_button.place(relx=0.025, rely=0.35)

        self.new_voice_channel_entry = Entry(self.root, width=20, font=("Segoe UI", 12))
        self.new_voice_channel_entry.place(relx=0.025, rely=0.65)

        self.create_voice_channel_button = Button(self.root, text="Créer un salon vocal", bg="#7289da", fg="white", font=("Segoe UI", 12), command=self.create_voice_channel)
        self.create_voice_channel_button.place(relx=0.025, rely=0.7)
        self.update_gui()
        

    def update_gui(self):
        self.root.update_idletasks()
        self.root.update()  

    def get_channels(self):
        salons_textuels = self.db_instance.fetch("SELECT name FROM channel")
        salons_textuels = [salon[0] for salon in salons_textuels]
        return salons_textuels
    
    def set_channels(self, salons_textuels):
        self.salons_textuels = salons_textuels
    
    def get_admin(self):
        admin = self.db_instance.fetch("SELECT admin FROM users WHERE email = %s", (self.email,))
        admin = admin[0][0]
        if admin == "True":
            return True
        else:
            return False

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.chat_text.config(state="normal")

            # Ajout du message à la zone de chat
            self.message_entry.delete(0, tk.END)
            self.chat_text.config(state="disabled")

            # Désactiver la zone de chat à nouveau
            self.chat_text.config(state="disabled")
            return message


    def receive_message(self, message):
        # Activer la zone de chat pour ajouter le message
        self.chat_text.config(state="normal")

        # Ajout du message à la zone de chat
        self.chat_text.insert(tk.END, message)

        # Désactiver la zone de chat à nouveau
        self.chat_text.config(state="disabled")

    def insert_emoji(self, event):
        emoji_unicode = event.widget['text']
        self.message_entry.insert(tk.END, emoji_unicode)
    
    def create_channel(self):
        new_channel_name = self.new_channel_entry.get()
        authorization = self.get_admin()
        if authorization == False and new_channel_name:
            messagebox.showerror("Erreur", "Vous n'avez pas les droits pour créer un salon.")
        elif authorization == True and new_channel_name:
            messagebox.showinfo("Succès", f"Salon textuel créé : {new_channel_name}")
            self.db_instance.executeQuery("INSERT INTO channel (name) VALUES (%s)", (new_channel_name,))
            self.salons_textuels = self.get_channels()
            self.update_option_menu()
        self.new_channel_entry.delete(0, tk.END)

            #self.salons_textuels_menu.add_command(label=new_channel_name, command=lambda: self.select_channel(new_channel_name))

    def update_option_menu(self):
        # Clear the existing OptionMenu
        self.salons_textuels_menu.destroy()

        # Create a new OptionMenu with the updated list of channels
        self.salons_textuels_menu = customtkinter.CTkOptionMenu(self.root, values=self.salons_textuels, command=self.select_channel)
        self.salons_textuels_menu.set("Salons textuels")
        self.salons_textuels_menu.place(relx=0.025, rely=0.15)
        
        #if new_channel_name:
            #print(f"Salon textuel créé : {new_channel_name}")
            #self.salons_textuels_menu.add_command(label=new_channel_name, command=lambda: self.select_channel(new_channel_name))
            #self.new_channel_entry.delete(0, tk.END)
    
    def create_voice_channel(self):
        new_channel_name = self.new_voice_channel_entry.get()
        if new_channel_name:
            print(f"Salon vocal créé : {new_channel_name}")
            self.salons_vocaux_menu.add_command(label=new_channel_name, command=lambda: self.select_channel(new_channel_name))
            self.new_voice_channel_entry.delete(0, tk.END)

    def select_channel(self, channel_name):
        #delete all messages
        self.chat_text.config(state="normal")
        self.chat_text.delete(1.0, tk.END)
        self.chat_text.config(state="disabled")     
        return channel_name
    
    def logout(self):
            self.root.destroy()
            os.system('python client.py')
    def afficher(self):
        self.root.mainloop()


# Instanciation de la classe et appel de la méthode pour afficher la fenêtre
if __name__ == "__main__":
    app = Graphic()
    app.afficher()
