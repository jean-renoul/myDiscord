class Channel:
    def __init__(self, name):
        self.name = name
        self.users = set()

    def addUser(self, clientSocket):
        self.users.add(clientSocket)

    def removeUser(self, user):
        self.users.remove(user)

    def sendMessage(self, message):
        for clientSocket in self.users:
            clientSocket.send(message.encode())

    