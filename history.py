import database
import random
from datetime import datetime, timedelta

def simulate_matches_fair():
    conn = database.get_connection()
    cursor = conn.cursor()

    # Haetaan kaikki tiimit
    cursor.execute("SELECT id, elo FROM teams WHERE elo > 0")
    teams = cursor.fetchall()

    if len(teams) < 2:
        print("❌ Ei tarpeeksi tiimejä tietokannassa!")
        return

    # Tyhjennetään vanhat kokeilut
    cursor.execute("DELETE FROM matches")

    print(f"Lasketaan jokaiselle {len(teams)} tiimille 25 peliä. Odota hetki...")

    matches_to_insert = []
    tana_an = datetime.now()

    # Käydään JOKAINEN tiimi läpi ja pakotetaan niille 25 peliä
    for t1_id, t1_elo in teams:
        # Valitaan tälle tiimille 25 satunnaista vastustajaa
        opponents = random.sample([t for t in teams if t[0] != t1_id], 25)
        
        for t2_id, t2_elo in opponents:
            # Sama todennäköisyysmatematiikka
            elo_diff = t2_elo - t1_elo
            prob_t1_wins = 1 / (1 + 10 ** (elo_diff / 700))

            if random.random() < prob_t1_wins:
                home_score, away_score = 2, random.randint(0, 1)
            else:
                home_score, away_score = random.randint(0, 1), 2

            random_days = random.randint(0, 90)
            match_date = (tana_an - timedelta(days=random_days)).strftime("%Y-%m-%d")

            matches_to_insert.append((t1_id, t2_id, home_score, away_score, match_date))

    # Käytetään executemany-komentoa, joka on 100x nopeampi ison datan syötössä
    cursor.executemany('''INSERT INTO matches (home_team_id, away_team_id, home_score, away_score, date) 
                          VALUES (?, ?, ?, ?, ?)''', matches_to_insert)

    conn.commit()
    conn.close()
    print(f"✅ Simulointi valmis! Tietokantaan lisättiin kerralla {len(matches_to_insert)} ottelua.")

if __name__ == "__main__":
    simulate_matches_fair()