from Channel import channel
import socket
import threading

class server:
    def __init__(self):
        self.channels = {}
        self.clientSockets = set()
        self.serverSocket = socket.socket()
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind(('127.0.0.1', 8080))
        self.serverSocket.listen(5)

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
                print (message)
                channelName, messageDate, clientName,  messageContent= message.split(': ')
                print (channelName, messageDate, clientName, messageContent)
                messageContent = f"{messageDate}: {clientName}: {messageContent}"
                print (messageContent)
                channelName = channelName.strip()
                if channelName not in self.channels:
                    message = f"[!] Error: Channel {channelName} does not exist."
                    clientSocket.send(message.encode()) 
                else:
                    self.joinChannel(channelName, clientSocket)
                    self.sendToChannel(channelName, messageContent)
            

    def start(self):
        while True:
            clientSocket, clientAdress = self.serverSocket.accept()
            print(f"[+] {clientSocket} | {clientAdress} connected.")
            self.clientSockets.add(clientSocket)
            clientThread = threading.Thread(target=self.listenForClients, args=(clientSocket,))
            clientThread.start()

    def createChannel(self, channelName):
        self.channels[channelName] = channel(channelName)

    def joinChannel(self, channelName, clientSocket):
        self.channels[channelName].addUser(clientSocket)

    def sendToChannel(self, channelName, message):
        self.channels[channelName].sendMessage(message)

server1 = server()
server1.createChannel('general')
server1.start()

