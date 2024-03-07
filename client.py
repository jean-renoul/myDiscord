import socket
from datetime import datetime
from threading import Thread
from Class.User import User
from Class.Login import Login
from Class.Register import Register
from Class.Graphic import Graphic
from plyer import notification
import pyaudio

# Addresses IPs et ports des serveurs
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080
VOCAL_PORT = 8081
separator_token = "<SEP>" # séparateurs pour les messages

# Initialisation des sockets
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
vocalSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Initialisation de PyAudio
audio = pyaudio.PyAudio()

# Paramètres audio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Ouvrir les flux audio
input_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
output_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

new_user = False

# Connection au serveur
try:
    clientSocket.connect((SERVER_HOST, SERVER_PORT))
    print("[+] Connected.")
except Exception as e:
    print(f"Error connecting to the server: {e}")
    exit()

# Initialisation de l'interface graphique
app = Login() # On lance d'abord la page de connexion
app.windows.mainloop()
user_info = app.userInfo
if user_info == []:
    app = Register() # Si l'utilisateur le choisit, on lance la page d'inscription
    app.windows.mainloop()
    user_info = app.userInfo
    client = User(user_info[0], user_info[1], user_info[2], user_info[3]) # Instantiation de l'objet User
    new_user = True
    app = Graphic(client) # On lance l'interface graphique du chat
    
else:
    client = User(user_info[2], user_info[1], user_info[3], user_info[4]) # Instantiation de l'objet User
    new_user = False
    app = Graphic(client)

# Attribue le socket client à l'objet User
client.clientSocket = clientSocket

# Fonction pour écouter les messages
def listen_for_messages():
    try:
        while True:
            message = clientSocket.recv(1024).decode()
            if not message:
                break
            # Si le message est une commande
            if "<COMMAND>notification" in message:
                message_parts = message.split('|')
                notification.notify(
                    title=message_parts[1],
                    message="Nouveau message dans le salon " + message_parts[1],
                    timeout=10
                )
            elif "<COMMAND>refresh" in message:
                app.update_option_menu()
                app.text_rooms_menu.configure(command=handle_switch_channel)  # Comme text_rooms_menu est détruit pour être recréé, on doit reconfigurer la commande
            # Si le message n'est pas une commande, on l'affiche dans la zone de chat
            else:
                app.receive_message(message)
    except Exception as e:
        print(f"Error occurred while listening for messages: {e}")

# Fonction pour envoyer des messages
def send_message(message):
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Le message est envoyé segmenté, pour indiquer le salon, la date, le prénom et le nom de l'utilisateur, ainsi que le message
    to_send = f"{client.channel}{separator_token}{date_now}{separator_token}{client.firstname}{separator_token}{client.lastname}{separator_token}{message}"
    clientSocket.send(to_send.encode())

# Fonction pour gérer l'envoi de messages
def handle_send_button():
    message = app.send_message()
    send_message(message)

# Fonction pour gérer le changement de salon
def handle_switch_channel(channel_name):
    channel_name = app.select_channel(channel_name)
    if channel_name is not None:
        client.joinChannel(channel_name)
        send_message("<COMMAND>switch")

# Fonction pour gérer la création de salon
def handle_create_channel():
    new_channel_name = app.create_channel()
    if new_channel_name:
        send_message(f"<COMMAND>create_channel|{new_channel_name}")
        handle_switch_channel(new_channel_name)
        app.text_rooms_menu.configure(command=handle_switch_channel)  # On reconfigure à nouveau la commande pour le menu des salons
        app.text_rooms_menu.set(new_channel_name)

# Fonction pour envoyer les données audio
def send_audio():
    while True:
        try:
            data = input_stream.read(CHUNK)
            vocalSocket.sendall(data)
        except Exception as e:
            print(f"Error occurred while sending audio: {e}")
            break

# Fonction pour lire les données audio
def play_audio():
    while True:
        try:
            data = vocalSocket.recv(CHUNK)
            if not data:
                break
            output_stream.write(data)
        except Exception as e:
            print(f"Error occurred while playing audio: {e}")
            break

# Fonction pour rejoindre le chat vocal
def join_voice_chat():
    try:
        vocalSocket.connect((SERVER_HOST, VOCAL_PORT)) # On se connecte au serveur vocal
        send_audio_thread = Thread(target=send_audio) # On lance un thread pour envoyer les données audio
        send_audio_thread.start()
        play_audio_thread = Thread(target=play_audio) # On lance un thread pour lire les données audio
        play_audio_thread.start()
    except Exception as e:
        print(f"Error occurred while joining voice chat: {e}")

# Fonction pour quitter le chat vocal
def quit_voice_chat():
    try:
        vocalSocket.close()
        input_stream.stop_stream()
        input_stream.close()
        output_stream.stop_stream()
        output_stream.close()
        audio.terminate()
    except Exception as e:
        print(f"Error occurred while quitting voice chat: {e}")


# Lance le thread pour écouter les messages
t1 = Thread(target=listen_for_messages)
t1.start()

# Configuration des commandes pour les boutons de l'interface graphique
app.send_button.config(command=handle_send_button)
app.text_rooms_menu.configure(command=handle_switch_channel)
app.create_channel_button.config(command=handle_create_channel)
app.join_voice_button.config(command=join_voice_chat)
app.quit_voice_button.config(command=quit_voice_chat)

# Si l'utilisateur est nouveau, on envoie une commande pour rafraîchir les salons et les utilisateurs
if new_user == True:
    send_message("<COMMAND>refresh")

# Affiche l'interface graphique
app.show()



# Fermeture des sockets
clientSocket.close()
vocalSocket.close()