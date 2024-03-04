from Channel import Channel
import socket
import threading
from Db import Db


class Server:
    def __init__(self):
        self.channels = {}
        self.clientSockets = set()
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(('127.0.0.1', 8080))
        self.serverSocket.listen(5)
        self.Db = Db('82.165.185.52', 'jean-renoul', 'patesaup0ulet', 'jean-renoul_discord')
        self.separator_token = "<SEP>"    

    def listenForClients(self, clientSocket):
        while True:
            try:
                message = clientSocket.recv(1024).decode()
                print (message)
            except UnicodeDecodeError:
                print(f"Received non-text data.")
                continue
            except Exception as e:
                # client no longer connected
                # remove it from the set
                print(f"[!] Error: {e}")
                self.clientSockets.remove(clientSocket)
                break
            else:
                message = message.replace (self.separator_token, ': ')
                channelName, messageDate, clientFirstName, clientLastName,  messageContent= message.split(': ')
                message = f"{messageDate}: {clientFirstName} {clientLastName}: {messageContent}"

                if "<COMMAND>switch" in messageContent:
                    self.joinChannel(channelName, clientSocket)
                    self.getPreviousMessages(channelName, clientSocket)
                elif "<COMMAND>create_channel" in messageContent:
                    newChannelName = messageContent.split("|")[1]
                    print(f"New channel created: {newChannelName}")
                    self.channels[newChannelName] = Channel(newChannelName)
                    for clientSocket in self.clientSockets:
                        clientSocket.send(b"<COMMAND>refresh")
                elif "<COMMAND>refresh" in messageContent:
                    for clientSocket in self.clientSockets:
                        clientSocket.send(b"<COMMAND>refresh")
                else:
                    self.sendToChannel(channelName, message)
                    self.Db.executeQuery("INSERT INTO message (texte, auteur, heure, channel) VALUES (%s, %s, %s, %s)", (messageContent, clientFirstName + " " + clientLastName, messageDate, channelName))



    def start(self):
        self.getChannels()
        while True:
            clientSocket, clientAdress = self.serverSocket.accept()
            print(f"[+] {clientSocket} | {clientAdress} connected.")
            self.clientSockets.add(clientSocket)
            self.joinChannel('general', clientSocket)
            self.getPreviousMessages('general', clientSocket)
            clientThread = threading.Thread(target=self.listenForClients, args=(clientSocket,))
            clientThread.start()

    def getChannels(self):
        channelNames = self.Db.fetch("SELECT name FROM channel")
        channelNames = [channelName[0] for channelName in channelNames]
        for channelName in channelNames:
            self.channels[channelName] = Channel(Channel)

    def joinChannel(self, channelName, clientSocket):
        for channel in self.channels:
            if clientSocket in self.channels[channel].users:
                self.channels[channel].removeUser(clientSocket)
                print (f"[-] {clientSocket} left {channel} channel.")
        self.channels[channelName].addUser(clientSocket)
        print (f"[+] {clientSocket} joined {channelName} channel.")

    def getPreviousMessages(self, channelName, clientSocket):
        previous_messages = self.Db.fetch("SELECT * FROM message WHERE channel = %s", (channelName,))
        for message in previous_messages:
            message = f'{message[3]}: {message[2]}: {message[1]}\n'
            clientSocket.send(message.encode())

    def sendToChannel(self, channelName, message):
        toSend = f"{message}"
        self.channels[channelName].sendMessage(toSend)
        notification_message = f"<COMMAND>notification|{channelName}"
        for channel_name, channel_object in self.channels.items():
            if channel_name != channelName:
                channel_object.sendMessage(notification_message)


if __name__ == "__main__":
    server1 = Server()
    server1.start()

