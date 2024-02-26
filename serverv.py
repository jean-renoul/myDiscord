import socket
import pyaudio

# Configuration du serveur
HOST = '127.0.0.1'
PORT = 12345

# Paramètres audio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Initialisation de PyAudio
audio = pyaudio.PyAudio()

# Création du socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)  # Attente d'une seule connexion

print("Serveur en attente de connexions...")

# Fonction pour gérer les clients
def handle_client(client_socket):
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            stream.write(data)
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        client_socket.close()

# Attente des connexions clientes
try:
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connexion établie avec {addr}")
        handle_client(client_socket)
finally:
    server_socket.close()
