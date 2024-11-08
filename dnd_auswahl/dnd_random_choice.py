import urllib.request
import datetime
import json
import os
import random

class Character:
    def __init__(self, name, race, character_class, timestamp):
        # Initialisiert die Charaktereigenschaften
        self.name = name
        self.race = race
        self.character_class = character_class
        self.strenth = random.randint(1, 50)
        self.intelligence = random.randint(1, 50)
        self.dexterity = random.randint(1, 50)
        self.timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    
    def save_character_to_json(self):
        # Speichert den Charakter in einer JSON-Datei
        character_data = {
            "name": self.name,
            "race": self.race,
            "class": self.character_class,
            "strenth": self.strenth,
            "intelligence": self.intelligence,
            "dexterity": self.dexterity,
            "timestamp": self.timestamp
        }
        
        try:
            # Überprüft, ob die Datei existiert und Daten enthält
            if os.path.exists("character.json") and os.path.getsize("character.json") > 0:
                with open("character.json", "r+") as file:
                    # Fügt den neuen Charakter zur bestehenden Datei hinzu
                    file.seek(0, os.SEEK_END)
                    file.seek(file.tell() - 1, os.SEEK_SET)
                    file.truncate()
                    file.write(",\n")
                    json.dump(character_data, file, indent=4)
                    file.write("\n]")
            else:
                # Erstellt eine neue Datei und speichert den Charakter
                with open("character.json", "w") as file:
                    file.write("[\n")
                    json.dump(character_data, file, indent=4)
                    file.write("\n]")
        except (OSError, IOError) as e:
            print(f"Fehler beim Speichern des Charakters: {e}")

def fetch_random_data(url):
    # Ruft zufällige Daten von der angegebenen URL ab
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())["results"]
            return random.choice(data)["name"]
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"Fehler beim Abrufen der Daten von {url}: {e}")
        return None

# URLs für Rassen und Klassen
race_url = "https://www.dnd5eapi.co/api/races"
class_url = "https://www.dnd5eapi.co/api/classes"            
timestamp = datetime.datetime.now()

# Zufällige Rasse und Klasse abrufen
random_race = fetch_random_data(race_url)
random_class = fetch_random_data(class_url)

if random_race and random_class:
    # Charakter erstellen und speichern
    charakter = Character(input("Gib hier den Namen des Charakters ein "), random_race, random_class, timestamp)
    charakter.save_character_to_json()
else:
    print("Fehler beim Erstellen des Charakters aufgrund fehlender Daten.")
