import json
import re

DB_FILE = "cs_database.json"
HLTV_FILE = "hltv_data.txt"

def update_from_hltv():
    print("🔄 Luetaan HLTV-dataa ja etsitään pelaajia...")
    
    # Ladataan tietokanta
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
    except FileNotFoundError:
        print(f"❌ Tietokantaa {DB_FILE} ei löytynyt.")
        return

    # Ladataan kopioitu teksti
    try:
        with open(HLTV_FILE, "r", encoding="utf-8") as f:
            hltv_text = f.read()
    except FileNotFoundError:
        print(f"❌ Tiedostoa {HLTV_FILE} ei löytynyt. Luo se ja liitä HLTV:n teksti sinne.")
        return

    # Siivotaan rivinvaihdot ja välilyönnit, jotta teksti on yhtenäinen pötkö
    hltv_text = hltv_text.replace("\n", "").replace(" ", "")

    players_updated = 0

    # Käydään läpi kaikki tietokannan pelaajat
    for p_name in db["players"].keys():
        # Regex etsii pelaajan nimen, jota seuraa kartat, kierrokset, K-D diff (+/-), K/D ja lopuksi Rating
        # Esim. regex lukee: zywoo -> 851857 -> +616 -> 1.61 -> nappaa (1.39)
        pattern = re.compile(re.escape(p_name) + r"\d+[+-]\d+\d\.\d{2}(\d\.\d{2})", re.IGNORECASE)
        match = pattern.search(hltv_text)
        
        if match:
            new_rating = float(match.group(1))
            db["players"][p_name]["rating"] = new_rating
            players_updated += 1
            print(f"  + Päivitetty: {p_name.capitalize()} -> {new_rating}")

    # Tallennetaan päivitetyt tiedot
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

    print("-" * 40)
    print(f"✅ Valmista! Päivitettiin onnistuneesti {players_updated} pelaajan HLTV-rating tietokantaan.")

if __name__ == "__main__":
    update_from_hltv()