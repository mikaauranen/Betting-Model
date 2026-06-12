import sqlite3

DB_NAME = "cs2.db"

def get_connection():
    # SQLite on vain yksi tiedosto kovalevyllä
    return sqlite3.connect(DB_NAME)

def init_db():
    """Luo SQL-tietokannan taulut, jos niitä ei ole."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Luodaan tiimien taulu
        cursor.execute('''CREATE TABLE IF NOT EXISTS teams 
                          (id INTEGER PRIMARY KEY, name TEXT UNIQUE, elo INTEGER)''')
        # Luodaan pelaajien taulu (team_id linkittää pelaajan tiimiin)
        cursor.execute('''CREATE TABLE IF NOT EXISTS players 
                          (id INTEGER PRIMARY KEY, name TEXT UNIQUE, rating REAL, team_id INTEGER,
                           FOREIGN KEY(team_id) REFERENCES teams(id))''')
        conn.commit()

def get_team(name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teams WHERE name = ?", (name,))
        return cursor.fetchone()

def get_roster(team_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, rating FROM players WHERE team_id = ?", (team_id,))
        return cursor.fetchall()