import database
import calculator

def main():
    database.init_db()  # Alustetaan kanta heti alussa
    print("=== CS2 PRO PREDICTOR (SQL Edition) ===")

    while True:
        print("\n" + "-" * 50)
        input_home = input("Kotijoukkue (tai 'q' lopettaaksesi): ").strip()
        if input_home.lower() == 'q':
            break

        team_home = database.get_team(input_home)
        if not team_home:
            print("❌ Joukkuetta ei löytynyt.")
            continue
        
        home_id, home_name, home_elo = team_home

        input_away = input("Vierasjoukkue: ").strip()
        team_away = database.get_team(input_away)
        if not team_away:
            print("❌ Joukkuetta ei löytynyt.")
            continue
        
        away_id, away_name, away_elo = team_away

        # Haetaan rosterit SQL-kannasta
        home_roster_data = database.get_roster(home_id)
        away_roster_data = database.get_roster(away_id)

        # Laskenta
        home_ratings = [p[1] for p in home_roster_data]
        away_ratings = [p[1] for p in away_roster_data]

        adj_elo_home, _ = calculator.get_adjusted_elo_from_ratings(home_elo, home_ratings)
        adj_elo_away, _ = calculator.get_adjusted_elo_from_ratings(away_elo, away_ratings)

        print(f"\nAnalyysi valmis:")
        print(f"{home_name} (Adj. ELO: {adj_elo_home:.1f}) vs {away_name} (Adj. ELO: {adj_elo_away:.1f})")

if __name__ == "__main__":
    main()