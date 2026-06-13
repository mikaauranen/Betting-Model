import database

def aseta_base_elo():
    print("=== JOUKKUEEN BASE ELO -MUOKKAIN ===")
    tiimin_nimi = input("Minkä joukkueen ELOa haluat muuttaa?: ").strip()
    
    conn = database.get_connection()
    cursor = conn.cursor()
    
    # Tarkistetaan ensin, löytyykö tiimiä
    cursor.execute("SELECT elo FROM teams WHERE LOWER(name) = LOWER(?)", (tiimin_nimi,))
    row = cursor.fetchone()
    
    if not row:
        print(f"❌ Joukkuetta '{tiimin_nimi}' ei löytynyt tietokannasta.")
        conn.close()
        return
        
    vanha_elo = row[0]
    print(f"Joukkueen nykyinen Base ELO on: {vanha_elo}")
    
    try:
        uusi_elo = int(input(f"Syötä uusi Base ELO joukkueelle {tiimin_nimi.capitalize()}: "))
    except ValueError:
        print("❌ Virhe: ELOn täytyy olla kokonaisluku!")
        conn.close()
        return

    # Päivitetään uusi ELO tietokantaan
    cursor.execute("UPDATE teams SET elo = ? WHERE LOWER(name) = LOWER(?)", (uusi_elo, tiimin_nimi))
    conn.commit()
    conn.close()
    
    print(f"✅ Onnistui! {tiimin_nimi.capitalize()} Base ELO muutettu: {vanha_elo} ➡️ {uusi_elo}")

if __name__ == "__main__":
    aseta_base_elo()