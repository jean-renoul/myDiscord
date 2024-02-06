import mysql.connector

class db:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()

    def executeQuery(self, query, params=None):
        self.connect()
        self.cursor.execute(query, params or ())
        self.connection.commit()
        self.disconnect()

    def fetch(self, query, params=None):
        self.connect()
        self.cursor.execute(query, params or ())
        result = self.cursor.fetchall()
        self.disconnect()
        return result

db = db('82.165.185.52', 'jean-renoul', 'patesaup0ulet', 'jean-renoul_discord')
#db.executeQuery('CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT)')
#db.executeQuery('INSERT INTO message ( texte, auteur, heure) VALUES (%s, %s, %s)', ("Salut", "Jean", "2021-01-01 00:00:00"))