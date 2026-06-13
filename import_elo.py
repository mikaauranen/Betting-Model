import re
import database

RANKING_FILE = "hltv_ranking.txt"

def update_elo_by_roster():
    print("🔄 Analysoidaan HLTV-kokoonpanoja ja lasketaan aggressiivisia eliitti-ELO-lukuja...")
    
    # 1. Luetaan ranking-tiedosto
    try:
        with open(RANKING_FILE, "r", encoding="utf-8") as f:
            ranking_text = f.read()
    except FileNotFoundError:
        print(f"❌ Tiedostoa {RANKING_FILE} ei löytynyt.")
        return

    # 2. Yhdistetään tietokantaan
    conn = database.get_connection()
    cursor = conn.cursor()

    # 3. Haetaan kaikki tiimit ja niiden pelaajat tietokannasta vertailua varten
    cursor.execute("SELECT id, name FROM teams")
    teams_data = cursor.fetchall()
    
    team_rosters = {}
    for t_id, t_name in teams_data:
        cursor.execute("SELECT name FROM players WHERE team_id = ?", (t_id,))
        players = [row[0].lower().strip() for row in cursor.fetchall()]
        team_rosters[t_id] = {"name": t_name, "roster": players}

    # Pilkotaan teksti "Ranking details" -sanan kohdalta lohkoihin.
    # Yksi lohko sisältää yhden joukkueen pelaajat.
    blocks = ranking_text.split("Ranking details")
    
    rank = 1
    teams_updated = 0
    
    # 4. Käydään läpi jokainen sijoituslohko
    for block in blocks:
        # Puhdistetaan lohko turhasta sälästä.
        # Etsitään vain niitä sanoja, joissa on yksittäisiä heittomerkkejä (esim. 'apEX') 
        # TAI sanoja, jotka yhdistävät maan ja nimen (FranceapEX)
        
        # Helpoin tapa: Etsitään heittomerkkien sisällä olevat sanat (nämä ovat poikkeuksetta nikkejä)
        player_candidates = re.findall(r"'([^']+)'", block)
        
        # Muutetaan pieniksi kirjaimiksi, jotta vertailu onnistuu
        player_candidates = [p.lower() for p in player_candidates]
        
        if not player_candidates:
            continue
            
        best_match_team_id = None
        max_matches = 0
        
        # Verrataan löydettyjä nikkejä tietokannan rostereihin
        for t_id, t_data in team_rosters.items():
            matches = 0
            for p in t_data["roster"]:
                # Pieni "fudge factor" jos nimet eivät ole täysin identtiset (esim. hunter- vs hunter)
                clean_db_name = re.sub(r'[^a-z0-9]', '', p)
                for cand in player_candidates:
                    clean_cand_name = re.sub(r'[^a-z0-9]', '', cand)
                    if clean_db_name == clean_cand_name:
                        matches += 1
                        break # Siirrytään seuraavaan tietokannan pelaajaan
            
            # Vaaditaan vähintään 3 täsmäävää pelaajaa, jotta tunnistus on luotettava
            if matches > max_matches and matches >= 3: 
                max_matches = matches
                best_match_team_id = t_id
                
        if best_match_team_id:
            t_data = team_rosters[best_match_team_id]
            
            # --- UUSI AGGRESSIIVINEN JA JYRKÄ ELO-KAAVA ---
            if rank == 1:
                calculated_elo = 2150
            elif rank == 2:
                calculated_elo = 2080
            elif rank == 3:
                calculated_elo = 2020
            elif rank <= 10:
                calculated_elo = 2020 - ((rank - 3) * 25)
            elif rank <= 30:
                calculated_elo = 1845 - ((rank - 10) * 12)
            else:
                calculated_elo = 1605 - int((rank - 30) * 1.5)
                
            calculated_elo = max(1500, calculated_elo)
            
            # 5. Päivitetään ELO tietokantaan
            cursor.execute("UPDATE teams SET elo = ? WHERE id = ?", (calculated_elo, best_match_team_id))
            teams_updated += 1
            print(f"  🏆 Sija #{rank}: Tunnistettu {t_data['name']} -> Asetettu {calculated_elo} ELO ({max_matches} pelaajaa täsmäsi)")
            rank += 1
        else:
            # Jos tiimiä ei tunnistettu tietokannasta, nostetaan silti rankia, jotta seuraava saa oikean sijoituksen
            if len(player_candidates) >= 3:
                rank += 1

    conn.commit()
    conn.close()

    print("-" * 40)
    print(f"✅ Valmista! Päivitettiin {teams_updated} joukkueen ELO-luvut suoraan SQL-tietokantaan.")

if __name__ == "__main__":
    update_elo_by_roster()