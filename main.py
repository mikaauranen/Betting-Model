import database
import calculator

def find_team(search_term, teams_db):
    """Etsii tiimin tietokannasta nimen perusteella."""
    for team_id, team_data in teams_db.items():
        if search_term in team_data['name'].lower():
            return team_data
    return None

def main():
    print("=== CS2 PRO PREDICTOR (Adjusted ELO Model) ===")
    
    # 1. Ladataan data database.py -tiedoston avulla
    teams_db, players_db = database.load_data()
    print(f"✅ Ladattu {len(teams_db)} tiimiä tietokannasta.")

    # 2. Aloitetaan pääsilmukka
    while True:
        print("\n" + "-" * 50)
        input_home = input("Kotijoukkue (tai 'q' lopettaaksesi): ").strip().lower()
        if input_home == 'q':
            break

        team_home = find_team(input_home, teams_db)
        if not team_home:
            print("❌ Joukkuetta ei löytynyt.")
            continue

        input_away = input("Vierasjoukkue: ").strip().lower()
        team_away = find_team(input_away, teams_db)
        if not team_away:
            print("❌ Joukkuetta ei löytynyt.")
            continue

        # 3. LASKETAAN ADJUSTED ELO (calculator.py avulla)
        adj_elo_home, rating_home = calculator.get_adjusted_elo(team_home['elo'], team_home.get('roster', []), players_db)
        adj_elo_away, rating_away = calculator.get_adjusted_elo(team_away['elo'], team_away.get('roster', []), players_db)

        # 4. LASKETAAN TODENNÄKÖISYYS
        prob_home = calculator.calculate_win_probability(adj_elo_home, adj_elo_away, is_bo1=False)
        prob_away = 1 - prob_home

        # 5. TULOSTETAAN TULOKSET
        print(f"\n🎮 {team_home['name']} vs {team_away['name']}")
        print(f"📊 Base ELO: {team_home['elo']} vs {team_away['elo']}")
        print(f"🔥 Rating:   {rating_home:.2f} vs {rating_away:.2f}")
        print(f"⚖️ ADJ ELO:  {adj_elo_home:.0f} vs {adj_elo_away:.0f}")
        print(f"📈 TN:       {prob_home*100:.1f}% - {prob_away*100:.1f}%")
        
        fair_odds_home = 1 / prob_home
        fair_odds_away = 1 / prob_away
        print(f"💰 REILU KERROIN: {fair_odds_home:.2f} | {fair_odds_away:.2f}")

if __name__ == "__main__":
    main()