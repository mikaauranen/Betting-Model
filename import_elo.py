import json
import re

DB_FILE = "cs_database.json"
RANKING_FILE = "hltv_ranking.txt"

def update_elo_by_roster():
    print("🔄 Analysoidaan HLTV-kokoonpanoja ja lasketaan aggressiivisia eliitti-ELO-lukuja...")
    
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
    except FileNotFoundError:
        print(f"❌ Tietokantaa {DB_FILE} ei löytynyt.")
        return

    try:
        with open(RANKING_FILE, "r", encoding="utf-8") as f:
            ranking_text = f.read()
    except FileNotFoundError:
        print(f"❌ Tiedostoa {RANKING_FILE} ei löytynyt.")
        return

    blocks = ranking_text.split("Ranking details")
    
    rank = 1
    teams_updated = 0
    
    for block in blocks:
        tokens = block.split()
        if not tokens:
            continue
            
        player_candidates = []
        for token in tokens:
            clean_token = re.sub(r'[^a-z0-9-]', '', token.lower().strip())
            if clean_token and clean_token not in ["hltv", "team", "profile", "bet", "now", "vs", "ranking", "details", "world", "on", "june", "points"]:
                player_candidates.append(clean_token)
        
        if not player_candidates:
            continue
            
        best_match_team_id = None
        max_matches = 0
        
        for t_id, t_data in db["teams"].items():
            matches = 0
            for p in t_data.get("roster", []):
                if p.lower().strip() in player_candidates:
                    matches += 1
            
            if matches > max_matches and matches >= 2: 
                max_matches = matches
                best_match_team_id = t_id
                
        if best_match_team_id:
            t_data = db["teams"][best_match_team_id]
            
            # --- UUSI AGGRESSIIVINEN JA JYRKÄ ELO-KAAVA ---
            if rank == 1:
                calculated_elo = 2150
            elif rank == 2:
                calculated_elo = 2080
            elif rank == 3:
                calculated_elo = 2020
            # Sijat 4-10: Jyrkkä pudotus (25 pistettä per sija)
            elif rank <= 10:
                calculated_elo = 2020 - ((rank - 3) * 25)
            # Sijat 11-30: Tasainen Tier 1 -lasku (12 pistettä per sija)
            elif rank <= 30:
                calculated_elo = 1845 - ((rank - 10) * 12)
            # Sijat 31-100: Loiva Tier 2 -häntä, joka päättyy 1500 pisteeseen
            else:
                calculated_elo = 1605 - int((rank - 30) * 1.5)
                
            calculated_elo = max(1500, calculated_elo)
            
            t_data["elo"] = calculated_elo
            teams_updated += 1
            print(f"  🏆 Sija #{rank}: Tunnistettu {t_data['name']} -> Asetettu {calculated_elo} ELO ({max_matches} pelaajaa täsmäsi)")
            rank += 1
        else:
            if len(player_candidates) >= 3:
                rank += 1

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

    print("-" * 40)
    print(f"✅ Valmista! Päivitettiin {teams_updated} joukkueen ELO-luvut jyrkällä eliittiasetuksella.")

if __name__ == "__main__":
    update_elo_by_roster()