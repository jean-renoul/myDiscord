import socket
import pyaudio
from concurrent.futures import ThreadPoolExecutor

class VocalServer:
    def __init__(self):        
        # Configuration du serveur
        self.HOST = '127.0.0.1'
        self.PORT = 8081

        # Paramètres audio
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024

        # Initialisation de PyAudio
        self.audio = pyaudio.PyAudio()

        # Création du socket TCP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen(5)  # Attente d'une seule connexion

    # Fonction pour gérer les clients
    def handle_client(self,client_socket):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                client_socket.sendall(data)
        except Exception as e:
            print(f"Erreur : {e}")
        finally:
            client_socket.close()

    # Fonction pour gérer les connexions clientes
    def accept_clients(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                client_socket, addr = self.server_socket.accept()
                print(f"Connection established with {addr}")
                executor.submit(self.handle_client, client_socket)

    def start(self):
        # Attente des connexions clientes
        try:
            self.accept_clients()
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    server1 = VocalServer()
    server1.start()
