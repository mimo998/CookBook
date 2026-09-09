import sqlite3

class RestaurantStorage:

    def __init__(self, connection):
        self.connection = connection

    def insert(self, name, rank):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO restaurants (name, rank) VALUES (?, ?)",
            (name, rank)
        )
        self.connection.commit()

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, rank FROM restaurants")
        rows = cursor.fetchall()
        return {name: rank for name, rank in rows}

    def get(self, name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT rank FROM restaurants WHERE name = ?", (name,))
        row = cursor.fetchone()
        return row[0] if row else None

    def update_rank(self, name, rank):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE restaurants SET rank = ? WHERE name = ?",
            (rank, name)
        )
        self.connection.commit()

    def delete(self, name):
        cursor = self.connection.cursor()
        cursor.execute(
            "DELETE FROM restaurants WHERE name = ?",
            (name,)
        )
        self.connection.commit()