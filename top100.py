import json

DB_FILE = "cs_database.json"

def show_top_teams(limit=100):
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
    except FileNotFoundError:
        print(f"❌ Tietokantaa '{DB_FILE}' ei löytynyt!")
        return

    teams = db.get("teams", {}).values()
    players = db.get("players", {})

    # Järjestetään tiimit ELO-pisteiden mukaan (suurin ensin)
    sorted_teams = sorted(teams, key=lambda x: x.get("elo", 1500), reverse=True)

    print(f"\n🏆 MAAILMAN TOP {limit} ELO-RANKING 🏆")
    print("-" * 55)
    print(f"{'Sija':<5} | {'Joukkue':<25} | {'ELO':<6} | {'Tulivoima (Skill)'}")
    print("-" * 55)

    for i, t in enumerate(sorted_teams[:limit]):
        # Lasketaan tiimin yksilötaidon keskiarvo
        roster = t.get("roster", [])
        ratings = [players.get(p, {}).get("rating", 1.0) for p in roster]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0.0

        print(f"#{i+1:<4} | {t['name']:<25} | {t.get('elo', 1500):<6} | {avg_rating:.2f}")
    
    print("-" * 55)

if __name__ == "__main__":
    show_top_teams()