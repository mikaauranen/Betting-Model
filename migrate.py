import json
import sqlite3
import database

def migrate():
    # 1. Avataan ja ladataan vanha JSON-tiedosto
    try:
        with open('cs_database.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Tiedostoa 'cs_database.json' ei löytynyt.")
        return

    # 2. Varmistetaan, että tietokanta on alustettu
    database.init_db()
    conn = database.get_connection()
    cursor = conn.cursor()

    # 3. Haetaan JSON-rakenteesta 'teams' ja 'players' osiot
    teams_dict = data.get('teams', {})
    players_dict = data.get('players', {})

    print(f"Aloitetaan migraatio: {len(teams_dict)} tiimiä löytyi.")

    # 4. Käydään tiimit läpi
    for team_id_str, team_info in teams_dict.items():
        name = team_info.get('name')
        elo = team_info.get('elo', 1500)
        roster_names = team_info.get('roster', [])

        # Lisätään tiimi kantaan
        try:
            cursor.execute("INSERT OR IGNORE INTO teams (name, elo) VALUES (?, ?)", (name, elo))
            cursor.execute("SELECT id FROM teams WHERE name = ?", (name,))
            db_team_id = cursor.fetchone()[0]

            # Lisätään pelaajat ja haetaan heidän ratinginsa players_dictistä
            for p_name in roster_names:
                p_data = players_dict.get(p_name, {})
                rating = p_data.get('rating', 1.0)
                
                cursor.execute("INSERT OR IGNORE INTO players (name, rating, team_id) VALUES (?, ?, ?)", 
                               (p_name, rating, db_team_id))
        except Exception as e:
            print(f"Virhe tiimin {name} kohdalla: {e}")
    
    conn.commit()
    conn.close()
    print("✅ Migraatio valmis! Kaikki data on nyt SQLite-tietokannassa.")

if __name__ == "__main__":
    migrate()