from Channel import Channel
import socket
import threading
from Db import Db
import pyaudio

class Server:
    def __init__(self):
        self.channels = {}
        self.clientSockets = set()
        self.serverSocket = socket.socket()
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind(('127.0.0.1', 8080))
        self.serverSocket.listen(5)
        self.Db = Db('82.165.185.52', 'jean-renoul', 'patesaup0ulet', 'jean-renoul_discord')

    def listenForClients(self, clientSocket):
        while True:
            try:
                message = clientSocket.recv(1024).decode()
                print (message)
            except Exception as e:
                # client no longer connected
                # remove it from the set
                print(f"[!] Error: {e}")
                self.clientSockets.remove(clientSocket)
                break
            else:
                message = message.replace ('<SEP>', ': ')
                channelName, messageDate, clientFirstName, clientLastName,  messageContent= message.split(': ')
                message = f"{messageDate}: {clientFirstName} {clientLastName}: {messageContent}"
                channelName = channelName.strip()
                messageDate = messageDate.strip()

                if "<COMMAND>switch" in messageContent:
                    channelName = channelName.strip()
                    self.joinChannel(channelName, clientSocket)
                    self.getPreviousMessages(channelName, clientSocket)
                elif "<COMMAND>create_channel | " in messageContent:
                    newChannelName = messageContent.split('| ')[1].strip()
                    print(f"New channel created: {newChannelName}")
                    self.channels[newChannelName] = Channel(newChannelName)
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
        toSend = f"{message}\n"
        self.channels[channelName].sendMessage(toSend)

if __name__ == "__main__":
    server1 = Server()
    server1.start()

