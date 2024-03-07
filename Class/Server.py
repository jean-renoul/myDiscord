from Channel import Channel
import socket
import threading
from Db import Db

class Server:
    def __init__(self):
        self.channels = {}  # Dictionnaire pour stocker les canaux
        self.clientSockets = set()
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crée un socket serveur
        self.serverSocket.bind(('127.0.0.1', 8080))  # Associe l'adresse IP et le port au socket serveur
        self.serverSocket.listen(5)  # Met le socket en mode écoute pour accepter un maximum de 5 connexions
        self.Db = Db('82.165.185.52', 'jean-renoul', 'patesaup0ulet', 'jean-renoul_discord')  # Initialise la base de données
        self.separator_token = "<SEP>"  # Jeton de séparation des messages

    def listenForClients(self, clientSocket):
        while True:
            try:
                message = clientSocket.recv(1024).decode()  # Reçoit et décode les messages des clients
                print(message)
            except Exception as e:
                print(f"[!] Error: {e}")  # Affiche une erreur en cas de problème
                self.clientSockets.remove(clientSocket)  # Supprime le client de l'ensemble des sockets
                break
            else:
                message = message.replace(self.separator_token, ': ')  # Remplace le jeton de séparation dans le message
                channelName, messageDate, clientFirstName, clientLastName, messageContent = message.split(': ')  # Divise le message en parties
                message = f"{messageDate}: {clientFirstName} {clientLastName}: {messageContent}"  # Formatte le message

                if "<COMMAND>switch" in messageContent:  # Si le message contient une commande pour changer de canal
                    self.joinChannel(channelName, clientSocket)  # Rejoint le nouveau canal
                    self.getPreviousMessages(channelName, clientSocket)  # Récupère les messages précédents
                elif "<COMMAND>create_channel" in messageContent:  # Si le message contient une commande pour créer un canal
                    newChannelName = messageContent.split("|")[1]  # Extrait le nom du nouveau canal
                    self.channels[newChannelName] = Channel(newChannelName)  # Crée un nouvel objet de canal
                    for clientSocket in self.clientSockets:
                        clientSocket.send(b"<COMMAND>refresh")  # Envoie une commande de rafraîchissement à chaque client
                elif "<COMMAND>refresh" in messageContent:
                    for clientSocket in self.clientSockets:
                        clientSocket.send(b"<COMMAND>refresh")  # Envoie une commande de rafraîchissement à chaque client
                else:
                    # Si le message n'est pas une commande
                    self.sendToChannel(channelName, message)  # Envoie le message au canal correspondant
                    self.Db.executeQuery("INSERT INTO message (texte, auteur, heure, channel) VALUES (%s, %s, %s, %s)", (messageContent, clientFirstName + " " + clientLastName, messageDate, channelName))  # Exécute une requête pour enregistrer le message dans la base de données

    def start(self):
        self.getChannels()  # Récupère les canaux existants depuis la base de données
        while True:
            clientSocket, clientAdress = self.serverSocket.accept()  # Accepte la connexion d'un client
            print(f"[+] {clientSocket} | {clientAdress} connected.")  # Affiche la connexion du client
            self.clientSockets.add(clientSocket)  # Ajoute le socket client à l'ensemble des sockets clientes
            self.joinChannel('general', clientSocket)  # Rejoint le canal général par défaut
            self.getPreviousMessages('general', clientSocket)  # Récupère les messages précédents du canal général
            clientThread = threading.Thread(target=self.listenForClients, args=(clientSocket,))  # Crée un nouveau thread pour gérer le client
            clientThread.start()  # Lance le thread

    def getChannels(self):
        channelNames = self.Db.fetch("SELECT name FROM channel")  # Récupère les noms des canaux depuis la base de données
        channelNames = [channelName[0] for channelName in channelNames]  # Liste les noms des canaux
        for channelName in channelNames:
            self.channels[channelName] = Channel(Channel)  # Crée un objet de canal pour chaque nom de canal

    def joinChannel(self, channelName, clientSocket):
        for channel in self.channels:  # Pour chaque canal existant
            if clientSocket in self.channels[channel].users:  # Si le client est dans le canal
                self.channels[channel].removeUser(clientSocket)  # Retire le client du canal
                print(f"[-] {clientSocket} left {channel} channel.")  # Affiche le départ du client du canal
        self.channels[channelName].addUser(clientSocket)  # Ajoute le client au canal spécifié
        print(f"[+] {clientSocket} joined {channelName} channel.")  # Affiche l'arrivée du client dans le canal spécifié

    def getPreviousMessages(self, channelName, clientSocket):
        previous_messages = self.Db.fetch("SELECT * FROM message WHERE channel = %s", (channelName,))  # Récupère les messages précédents depuis la base de données
        for message in previous_messages:
            message = f'{message[3]}: {message[2]}: {message[1]}\n'  # Formatte les messages
            clientSocket.send(message.encode())  # Envoie les messages au client

    def sendToChannel(self, channelName, message):
        toSend = f"{message}"  # Message à envoyer
        self.channels[channelName].sendMessage(toSend)  # Envoie le message au canal spécifié
        notification_message = f"<COMMAND>notification|{channelName}"  # Message de notification
        for channel_name, channel_object in self.channels.items():  # Pour chaque canal existant
            if channel_name != channelName:  # Si ce n'est pas le canal actuel
                channel_object.sendMessage(notification_message)  # Envoie le message de notification

if __name__ == "__main__":
    server1 = Server()  # Crée une instance de serveur
    server1.start()  # Lance le serveur