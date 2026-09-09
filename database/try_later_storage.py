import sqlite3

class TryLaterStorage:

    def __init__(self, connection):
        self.connection = connection

    def insert(self, name):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO try_later (name) VALUES (?)", (name,))
        self.connection.commit()

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM try_later")
        rows = cursor.fetchall()
        return [name for (name,) in rows]

    def get(self, name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM try_later WHERE name = ?", (name,))
        row = cursor.fetchone()
        return row[0] if row else None

    def delete(self, name):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM try_later WHERE name = ?", (name,))
        self.connection.commit()