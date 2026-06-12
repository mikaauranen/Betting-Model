import json
import sys

# Tiedostonimi on määritelty vakiona (vakioiden nimet kirjoitetaan ISOLLA)
DB_FILE = "cs_database.json"

def load_data():
    """
    Lataa joukkueet ja pelaajat JSON-tietokannasta.
    Palauttaa kaksi sanakirjaa (teams, players).
    """
    try:
        with open(DB_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data.get("teams", {}), data.get("players", {})
    except FileNotFoundError:
        print(f"❌ Error: Tietokantaa '{DB_FILE}' ei löytynyt kansiosta!")
        sys.exit(1) # Sulkee ohjelman turvallisesti, jos tiedostoa ei ole

def save_data(teams_db, players_db):
    """
    Tallentaa muokatut tiedot takaisin JSON-tiedostoon.
    """
    data_to_save = {
        "teams": teams_db,
        "players": players_db
    }
    with open(DB_FILE, "w", encoding="utf-8") as file:
        # indent=4 tekee tiedostosta ihmisen luettavan
        json.dump(data_to_save, file, indent=4, ensure_ascii=False)