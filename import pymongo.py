import pymongo
import json
from pymongo import MongoClient

class TerrenoDatabase:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="catasto_terreni"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.terreni = self.db["terreni"]

        # Assicura che la collezione utilizzi un indice geospaziale
        self.terreni.create_index([("coordinate", pymongo.GEOSPHERE)])

    def carica_dati_iniziali(self, file_path):
        with open(file_path) as f:
            dati_terreni = json.load(f)
            self.terreni.insert_many(dati_terreni)
            print("Dati iniziali caricati con successo.")

    def find_terreno_by_point(self, lat, lon):
        point = {"type": "Point", "coordinates": [lon, lat]}
        terreno = self.terreni.find_one({"coordinate": {"$geoIntersects": {"$geometry": point}}})
        return terreno

    def find_terreni_by_proprietario(self, codice_fiscale):
        terreni = self.terreni.find({"proprietario": codice_fiscale})
        return list(terreni)

    def find_terreni_by_strada(self, strada_id):
        terreni = self.terreni.find({"strade_intersezioni": strada_id})
        return list(terreni)

    def aggiungi_terreno(self, terreno):
        self.terreni.insert_one(terreno)

def main():
    db = TerrenoDatabase()

    # Usa il percorso assoluto del file JSON
    db.carica_dati_iniziali("/Users/michelepotsios/Desktop/mongo/progetto_mongodb/terreni.json")

    while True:
        print("\nApplicazione per il censimento dei terreni")
        print("1. Cerca terreno per punto geografico")
        print("2. Cerca terreni per codice fiscale")
        print("3. Cerca terreni coinvolti da una nuova strada")
        print("4. Aggiungi nuovo terreno")
        print("5. Esci")

        scelta = input("Scegli un'opzione: ")

        if scelta == "1":
            lat = float(input("Inserisci la latitudine: "))
            lon = float(input("Inserisci la longitudine: "))
            terreno = db.find_terreno_by_point(lat, lon)
            print("Terreno trovato:", terreno)
        elif scelta == "2":
            codice_fiscale = input("Inserisci il codice fiscale: ")
            terreni = db.find_terreni_by_proprietario(codice_fiscale)
            print("Terreni trovati:", terreni)
        elif scelta == "3":
            strada_id = input("Inserisci l'ID della strada: ")
            terreni = db.find_terreni_by_strada(strada_id)
            print("Terreni trovati:", terreni)
        elif scelta == "4":
            id_terreno = input("ID del terreno: ")
            lat = float(input("Latitudine: "))
            lon = float(input("Longitudine: "))
            proprietario = input("Codice fiscale del proprietario: ")
            descrizione = input("Descrizione: ")
            strade_intersezioni = input("ID delle strade intersecate (separate da virgola): ").split(",")
            terreno = {
                "id_terreno": id_terreno,
                "coordinate": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "proprietario": proprietario,
                "descrizione": descrizione,
                "strade_intersezioni": strade_intersezioni
            }
            db.aggiungi_terreno(terreno)
            print("Terreno aggiunto con successo!")
        elif scelta == "5":
            break
        else:
            print("Opzione non valida. Riprova.")

if __name__ == "__main__":
    main()
