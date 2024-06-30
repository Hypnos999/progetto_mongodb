import pymongo
import json

class TerrenoDatabase:
    def __init__(
            self,
            host='0.0.0.0',
            port=27017,
            db_name="catasto_terreni"
    ):
        self.client = pymongo.MongoClient(port=port, host=host)
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
        
    def check_terreno_occupato(self, cordinate_nuovo_terreno):
        for new_cord in cordinate_nuovo_terreno:
            if self.terreni.find_one({ "coordinate": { "$geoIntersects": {"$geometry": new_cord }}}):
                return True
            else: return False

if __name__ == '__main__':
    db = TerrenoDatabase(port=27017)

    while True:
        print("Applicazione per il censimento dei terreni, a cura di FLavio Manna, Michele Potsios, Mirko La Rocca\n")
        print("1. Cerca terreno per punto geografico")
        print("2. Cerca terreni per codice fiscale")
        print("3. Cerca terreni coinvolti da una nuova strada")
        print("4. Aggiungi nuovo terreno")
        print("q. Esci")

        scelta = input("\nScegli un'opzione: ").lower().strip()


        if scelta == 'q': break

        try:
            scelta = int(scelta)
            assert scelta <= 4
        except:
            continue

        ## cerca terreno per un punto geografico
        if scelta == 1:
            print('Inserisci q per passare al prossimo step\n')

            lat = float(input("Inserisci la latitudine: "))
            lon = float(input("Inserisci la longitudine: "))

            terreno = db.find_terreno_by_point(lat, lon)

            print("\nTerreno trovato:")
            for k, v in terreno.items():
                if k in ["coordinate", "_id", 'type']:
                    continue
                print(f'{k}: {v}')

            input('\nPremi invio per continuare')

        elif scelta == 2:
            codice_fiscale = input("Inserisci il codice fiscale: ")
            terreni = db.find_terreni_by_proprietario(codice_fiscale)

            if terreni:
                print("\nTerreni trovati:")
                for terreno in terreni:
                    print('')
                    for k, v in terreno.items():
                        if k in ["coordinate", "_id", 'type']:
                            continue
                        print(f'{k}: {v}')
            else:
                print('Nessun terrreno trovato')

            input('\nPremi invio per continuare')


        ## aggiungi terreno
        elif scelta == 4:
            print('Inserisci i punti geografici del terreno (minimo 3), \ninserisci q per passare al prossimo step\n')

            i = 1
            cord = []
            while True:
                lat = input(f"Latitudine {i}° punto: ").lower().strip()
                if lat == 'q': break

                lon = input(f"Longitudine {i}° punto: ").lower().strip()
                if lon == 'q': break

                cord.append([float(lon), float(lat)])

                i += 1

            proprietario = input("Codice fiscale del proprietario: ")
            descrizione = input("Descrizione: ")

            # Questi dati sono futili o li chiediamo all'utente?
            # id_terreno = input("ID del terreno: ")
            strade_intersezioni = input("ID delle strade intersecate (separate da virgola): ").split(",")

            terreno = {
                "type": "Polygon",
                "coordinates": [cord],
                "proprietario": proprietario,
                "descrizione": descrizione,
                # "id_terreno": id_terreno,
                "strade_intersezioni": strade_intersezioni
            }

            if db.check_terreno_occupato(cord):
                print("Il terreno è già occupato. Impossibile occuparlo")
            else: db.aggiungi_terreno(terreno)