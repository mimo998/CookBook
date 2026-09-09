import sqlite3

DB_PATH = "cookbook.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def setup_database(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_ranking (
            name TEXT PRIMARY KEY,
            rank REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            name TEXT PRIMARY KEY,
            rank REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            name TEXT PRIMARY KEY,
            time TEXT,
            instructions TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_name TEXT,
            name TEXT,
            amount TEXT,
            calories REAL,
            unit TEXT,
            description TEXT,
            FOREIGN KEY (recipe_name) REFERENCES recipes(name)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS try_later (
            name TEXT PRIMARY KEY
        )
    """)
    connection.commit()
