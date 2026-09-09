import sqlite3

class RankingStorage:
    def __init__(self, connection):
        self.connection = connection

    def insert(self, name, rank):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO food_ranking (name, rank) VALUES (?, ?)",
            (name, rank)
        )
        self.connection.commit()

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, rank FROM food_ranking")
        rows = cursor.fetchall()
        return {name: rank for name, rank in rows}

    def get(self, name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT rank FROM food_ranking WHERE name = ?", (name,))
        row = cursor.fetchone()
        return row[0] if row else None

    def update_rank(self, name, rank):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE food_ranking SET rank = ? WHERE name = ?",
            (rank, name)
        )
        self.connection.commit()

    def delete(self, name):
        cursor = self.connection.cursor()
        cursor.execute(
            "DELETE FROM food_ranking WHERE name = ?",
            (name,)
        )
        self.connection.commit()