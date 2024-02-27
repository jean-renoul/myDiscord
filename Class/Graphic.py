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
        self.image_haut_milieu = tk.PhotoImage(file="assets/images/Titre.png")
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

        emoji_data = [('assets/emojis/u0001f44a.png', '\U0001F44A'), ('assets/emojis/u0001f44c.png', '\U0001F44C'), ('assets/emojis/u0001f44d.png', '\U0001F44D'),
                      ('assets/emojis/u0001f495.png', '\U0001F495'), ('assets/emojis/u0001f496.png', '\U0001F496'), ('assets/emojis/u0001f4a6.png', '\U0001F4A6'),
                      ('assets/emojis/u0001f4a9.png', '\U0001F4A9'), ('assets/emojis/u0001f4af.png', '\U0001F4AF'), ('assets/emojis/u0001f595.png', '\U0001F595'),
                      ('assets/emojis/u0001f600.png', '\U0001F600'), ('assets/emojis/u0001f602.png', '\U0001F602'), ('assets/emojis/u0001f603.png', '\U0001F603'),
                      ('assets/emojis/u0001f605.png', '\U0001F605'), ('assets/emojis/u0001f606.png', '\U0001F606'), ('assets/emojis/u0001f608.png', '\U0001F608'),
                      ('assets/emojis/u0001f60d.png', '\U0001F60D'), ('assets/emojis/u0001f60e.png', '\U0001F60E'), ('assets/emojis/u0001f60f.png', '\U0001F60F'),
                      ('assets/emojis/u0001f610.png', '\U0001F610'), ('assets/emojis/u0001f618.png', '\U0001F618'), ('assets/emojis/u0001f61b.png', '\U0001F61B'),
                      ('assets/emojis/u0001f61d.png', '\U0001F61D'), ('assets/emojis/u0001f621.png', '\U0001F621'), ('assets/emojis/u0001f624.png', '\U0001F621'),
                      ('assets/emojis/u0001f631.png', '\U0001F631'), ('assets/emojis/u0001f632.png', '\U0001F632'), ('assets/emojis/u0001f634.png', '\U0001F634'),
                      ('assets/emojis/u0001f637.png', '\U0001F637'), ('assets/emojis/u0001f642.png', '\U0001F642'), ('assets/emojis/u0001f64f.png', '\U0001F64F'),
                      ('assets/emojis/u0001f920.png', '\U0001F920'), ('assets/emojis/u0001f923.png', '\U0001F923'), ('assets/emojis/u0001f928.png', '\U0001F928')]

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



        self.text_rooms = self.get_channels()
        self.voice_rooms = self.get_vocal_channel()

        self.text_rooms_menu = customtkinter.CTkOptionMenu(self.root, values=self.text_rooms, command=self.select_channel)
        self.text_rooms_menu.set("Salons textuels")
        self.text_rooms_menu.place(relx=0.025, rely=0.15)

        my_option2 = customtkinter.CTkOptionMenu(self.root, values=self.voice_rooms)
        my_option2.set("Salons vocaux")
        my_option2.place(relx=0.025, rely=0.5)

        self.voice_rooms_menu = my_option2

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
        text_rooms = self.db_instance.fetch("SELECT name FROM channel")
        text_rooms = [salon[0] for salon in text_rooms]
        return text_rooms
    

    def get_vocal_channel(self):
        voice_rooms = self.db_instance.fetch("SELECT name FROM vocal_channel")
        voice_rooms = [salon[0] for salon in voice_rooms]
        return voice_rooms
    
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
            self.update_option_menu()        
        return new_channel_name


    def update_option_menu(self):
        # Clear the existing OptionMenu
        self.text_rooms_menu.destroy()
        self.Salons_textuels = self.get_channels()
        # Create a new OptionMenu with the updated list of channels
        self.text_rooms_menu = customtkinter.CTkOptionMenu(self.root, values=self.Salons_textuels, command=self.select_channel)
        self.text_rooms_menu.set("Salons textuels")
        self.text_rooms_menu.place(relx=0.025, rely=0.15)
        self.new_channel_entry.delete(0, tk.END)
        self.update_gui()
    
    def create_voice_channel(self):
        new_channel_name = self.new_voice_channel_entry.get()
        if new_channel_name:
            print(f"Salon vocal créé : {new_channel_name}")
            self.voice_rooms_menu.add_command(label=new_channel_name, command=lambda: self.select_channel(new_channel_name))
            self.new_voice_channel_entry.delete(0, tk.END)

    def select_channel(self, channel_name):
        #delete all messages
        self.chat_text.config(state="normal")
        self.chat_text.delete(1.0, tk.END)
        self.chat_text.config(state="disabled")
        print (channel_name)    
        return channel_name
    
    def logout(self):
            self.root.destroy()
            os.system('python client.py')
    def show(self):
        self.root.mainloop()


# Instanciation de la classe et appel de la méthode pour afficher la fenêtre
if __name__ == "__main__":
    app = Graphic()
    app.show()
