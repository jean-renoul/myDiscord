import socket
import pyaudio
from concurrent.futures import ThreadPoolExecutor  # Importe ThreadPoolExecutor pour gérer les tâches concurrentes

class VocalServer:
    def __init__(self):        
        # Configuration du serveur
        self.HOST = '127.0.0.1'  # Adresse IP du serveur
        self.PORT = 8081  # Port du serveur

        # Paramètres audio
        self.FORMAT = pyaudio.paInt16  # Format audio
        self.CHANNELS = 1  # Nombre de canaux audio
        self.RATE = 44100  # Taux d'échantillonnage
        self.CHUNK = 1024  # Taille des morceaux de données audio

        # Initialisation de PyAudio
        self.audio = pyaudio.PyAudio()  # Crée une instance de PyAudio

        # Création du socket TCP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crée un socket TCP
        self.server_socket.bind((self.HOST, self.PORT))  # Associe l'adresse IP et le port au socket serveur
        self.server_socket.listen(5)  # Met le socket en mode écoute pour accepter un maximum de 5 connexions
        self.clientSockets = set()  # Ensemble pour stocker les sockets clientes

    # Fonction pour gérer les clients
    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024)  # Reçoit les données du client
                if not data:
                    break
                # Envoie les données à tous les autres clients
                for client in self.clientSockets:
                    if client != client_socket:
                        client.sendall(data)
        except Exception as e:  # En cas d'erreur
            print(f"Erreur : {e}")  # Affiche l'erreur
        finally:
            client_socket.close()  # Ferme le socket client

    # Fonction pour gérer les connexions clientes
    def accept_clients(self):
        with ThreadPoolExecutor(max_workers=10) as executor:  # Utilise ThreadPoolExecutor pour gérer les tâches concurrentes
            while True:
                client_socket, addr = self.server_socket.accept()  # Accepte la connexion d'un client
                self.clientSockets.add(client_socket) # Ajoute le socket client à l'ensemble des sockets clientes
                print(f"Connection established with {addr}")  # Affiche la connexion établie avec le client
                executor.submit(self.handle_client, client_socket)  # Soumet la fonction de gestion du client au ThreadPoolExecutor
                

    def start(self):
        # Attente des connexions clientes
        try:
            self.accept_clients()  # Lance la gestion des connexions clientes
        finally:
            self.server_socket.close()  # Ferme le socket serveur en cas d'erreur ou lorsque la boucle se termine

if __name__ == "__main__":
    server1 = VocalServer()  # Crée une instance de VocalServer
    server1.start()  # Lance le serveur vocal