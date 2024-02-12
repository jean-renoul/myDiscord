class user:
    def __init__(self, firstname, lastname, email, password, channel='general'):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.channel = channel
        self.clientSocket = None

    def joinChannel(self, channel):
        self.channel = channel

