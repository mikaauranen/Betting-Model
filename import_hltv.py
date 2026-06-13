import database

def update_from_hltv():
    print("Haetaan pelaajia tietokannasta ja päivitetään ratingit...")
    
    # 1. Luetaan HLTV:n raakadata
    try:
        with open("hltv_data.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("❌ Virhe: Tiedostoa 'hltv_data.txt' ei löytynyt.")
        return

    # 2. Avataan tietokantayhteys
    conn = database.get_connection()
    cursor = conn.cursor()

    # 3. Haetaan pelaajat tietokannasta
    cursor.execute("SELECT name FROM players")
    players = cursor.fetchall()

    players_updated = 0

    # 4. Käydään jokainen pelaaja läpi
    for (p_name,) in players:
        p_name_lower = p_name.lower()
        
        # Etsitään oikea rivi tekstitiedostosta
        for line in lines:
            parts = line.split()
            if not parts:
                continue
                
            # Esim: "Russiadonk" tai "FranceZywOo". Pelaajan nimi on aina tämän sanan lopussa.
            first_word = parts[0].lower()
            
            # Jos sana päättyy pelaajan nimeen (esim "russiadonk" päättyy "donk")
            if first_word.endswith(p_name_lower):
                try:
                    # HLTV:n taulukossa rating on AINA rivin viimeinen luku
                    new_rating = float(parts[-1])
                    
                    # Päivitetään tietokanta
                    cursor.execute("UPDATE players SET rating = ? WHERE name = ?", (new_rating, p_name))
                    players_updated += 1
                    print(f" + Päivitetty: {p_name.capitalize()} -> {new_rating}")
                    break # Siirrytään seuraavaan pelaajaan heti kun löytyi
                except ValueError:
                    pass

    # 5. Tallennetaan muutokset
    conn.commit()
    conn.close()

    print("-" * 40)
    print(f"✅ Valmista! Päivitettiin onnistuneesti {players_updated} pelaajan HLTV-rating tietokantaan.")

if __name__ == "__main__":
    update_from_hltv()