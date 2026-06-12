import database
import calculator

def main():
    database.init_db()
    print("=== CS2 PRO PREDICTOR (Form & SQL Edition) ===")

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

        # 1. Haetaan rosterit ja ratingit
        home_roster_data = database.get_roster(home_id)
        away_roster_data = database.get_roster(away_id)
        home_ratings = [p[1] for p in home_roster_data]
        away_ratings = [p[1] for p in away_roster_data]

        # 2. Haetaan 3kk otteluhistoria kuntopuntaria varten
        home_matches = database.get_recent_matches(home_id)
        away_matches = database.get_recent_matches(away_id)

        # 3. Lasketaan matemaattiset bonukset
        form_bonus_home = calculator.calculate_form_bonus(home_id, home_matches)
        form_bonus_away = calculator.calculate_form_bonus(away_id, away_matches)

        adj_elo_home, avg_rating_home = calculator.get_adjusted_elo_from_ratings(home_elo, home_ratings)
        adj_elo_away, avg_rating_away = calculator.get_adjusted_elo_from_ratings(away_elo, away_ratings)

        # 4. Lasketaan lopullinen ELO yhdistämällä kaikki vivut
        final_elo_home = adj_elo_home + form_bonus_home
        final_elo_away = adj_elo_away + form_bonus_away

        # 5. Voittotodennäköisyys BO3-ottelulle
        prob_home = calculator.calculate_win_probability(final_elo_home, final_elo_away, is_bo1=False)
        prob_away = 1 - prob_home

        # Tulostetaan ammattimainen analyysiraportti
        print(f"\n📊 --- ANALYYSI: {home_name} vs {away_name} ---")
        print(f"🏠 {home_name}:")
        print(f"  - Base ELO: {home_elo}")
        print(f"  - Pelaajien ka. rating: {avg_rating_home:.2f}")
        print(f"  - Kuntopuntari (3kk, {len(home_matches)} peliä): {form_bonus_home:+.1f} ELO")
        print(f"  - 🚀 LOPULLINEN ELO: {final_elo_home:.1f}")
        print(f"  - Voittotodennäköisyys: {prob_home*100:.1f}%")
        
        print(f"\n🚀 {away_name}:")
        print(f"  - Base ELO: {away_elo}")
        print(f"  - Pelaajien ka. rating: {avg_rating_away:.2f}")
        print(f"  - Kuntopuntari (3kk, {len(away_matches)} peliä): {form_bonus_away:+.1f} ELO")
        print(f"  - 🚀 LOPULLINEN ELO: {final_elo_away:.1f}")
        print(f"  - Voittotodennäköisyys: {prob_away*100:.1f}%")

if __name__ == "__main__":
    main()