import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, name text, url text, username text, password text)")
        self.conn.commit()


    def fetch(self):
        self.cur.execute("SELECT * FROM passwords")
        rows = self.cur.fetchall()
        return rows

    def insert(self, name, url, username, password):
        self.cur.execute("INSERT INTO passwords VALUES (NULL, ?, ?, ?, ?)", (name, url, username, password))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM passwords WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, name, url,username, password):
        self.cur.execute("UPDATE passwords SET name=?, url=?, username=?, password=? WHERE id=?", (name, url, username, password, id))
        self.conn.commit()
        
    def __del__(self):
        self.conn.close()


#db = Database('swiftpass.db')
#db.insert("YouTube", "www.youtube.com", "jared", "password123")
