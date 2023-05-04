import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_user_table()

    def create_user_table(self):
        # Create user table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, username TEXT)''')
        self.conn.commit()

    def insert_user(self, user_id, name, username):
        # Insert a new user into the user table
        self.cursor.execute('INSERT INTO users VALUES (?, ?, ?)', (user_id, name, username))
        self.conn.commit()

    def get_user_by_id(self, user_id):
        # Get a user by their ID
        self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return self.cursor.fetchone()

    def get_user_by_username(self, username):
        # Get a user by their username
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone()