import database

def nayta_ranking():
    conn = database.get_connection()
    cursor = conn.cursor()
    
    # Haetaan 30 parasta joukkuetta ELO-järjestyksessä (suurimmasta pienimpään)
    cursor.execute("SELECT name, elo FROM teams ORDER BY elo DESC LIMIT 30")
    tiimit = cursor.fetchall()
    
    print("\n🏆 --- TOP 30 JOUKKUEET ELO-JÄRJESTYKSESSÄ ---")
    print(f"{'Sija':<5} | {'Joukkue':<20} | {'Base ELO'}")
    print("-" * 45)
    
    for i, (nimi, elo) in enumerate(tiimit, start=1):
        print(f"#{i:<3} | {nimi:<20} | {elo}")
        
    conn.close()

if __name__ == "__main__":
    nayta_ranking()