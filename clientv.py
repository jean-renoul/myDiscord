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
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Fonction pour envoyer l'audio au serveur
def send_audio():
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    try:
        while True:
            data = stream.read(CHUNK)
            client_socket.sendall(data)
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        stream.stop_stream()
        stream.close()

# Envoyer l'audio au serveur
try:
    send_audio()
finally:
    client_socket.close()
