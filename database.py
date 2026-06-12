import sqlite3

DB_NAME = "cs2.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    """Luo SQL-tietokannan taulut, jos niitä ei ole."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS teams 
                          (id INTEGER PRIMARY KEY, name TEXT UNIQUE, elo INTEGER)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS players 
                          (id INTEGER PRIMARY KEY, name TEXT UNIQUE, rating REAL, team_id INTEGER,
                           FOREIGN KEY(team_id) REFERENCES teams(id))''')
        
        # UUSI TAULU: matches (tallentaa otteluhistorian)
        cursor.execute('''CREATE TABLE IF NOT EXISTS matches 
                          (id INTEGER PRIMARY KEY, home_team_id INTEGER, away_team_id INTEGER, 
                           home_score INTEGER, away_score INTEGER, date TEXT,
                           FOREIGN KEY(home_team_id) REFERENCES teams(id),
                           FOREIGN KEY(away_team_id) REFERENCES teams(id))''')
        conn.commit()

def get_team(name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teams WHERE LOWER(name) = LOWER(?)", (name,))
        return cursor.fetchone()

def get_roster(team_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, rating FROM players WHERE team_id = ?", (team_id,))
        return cursor.fetchall()

def get_recent_matches(team_id):
    """Hakee joukkueen kaikki ottelut viimeisen 3 kuukauden ajalta dynaamisesti."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Haetaan ottelut ja liitetään mukaan kummankin joukkueen nykyiset ELO-luvut ja nimet
        cursor.execute('''
            SELECT m.home_team_id, m.away_team_id, m.home_score, m.away_score,
                   t1.elo as home_elo, t2.elo as away_elo, t1.name as home_name, t2.name as away_name
            FROM matches m
            JOIN teams t1 ON m.home_team_id = t1.id
            JOIN teams t2 ON m.away_team_id = t2.id
            WHERE (m.home_team_id = ? OR m.away_team_id = ?)
              AND m.date >= date('now', '-3 months')
            ORDER BY m.date DESC
        ''', (team_id, team_id))
        return cursor.fetchall()