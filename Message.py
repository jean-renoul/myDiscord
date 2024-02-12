from Db import db

class message:
    def __init__(self):
        self.table = 'message'
        self.db = db('82.165.185.52', 'jean-renoul', 'patesaup0ulet', 'jean-renoul_discord')

    def create(self, texte, auteur, heure):
        querry = f'INSERT INTO {self.table} (texte, auteur, heure) VALUES (%s, %s, %s)'
        params = (texte, auteur, heure)
        self.db.executeQuery(querry, params)
    
    def read(self):
        querry = f'SELECT * FROM {self.table}'
        return self.db.fetch(querry)
    
    def update(self, id, texte, auteur, heure):
        querry = f'UPDATE {self.table} SET texte = %s, auteur = %s, heure = %s WHERE id = %s'
        params = (texte, auteur, heure, id)
        self.db.executeQuery(querry, params)

    def delete(self, id):
        querry = f'DELETE FROM {self.table} WHERE id = %s'
        params = (id,)
        self.db.executeQuery(querry, params)

    