import pymongo
import json
import os

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


    def find_terreno_by_point(self, lat, lon):
        point = {"type": "Point", "coordinates": [lon, lat]}
        terreno = self.terreni.find_one({"coordinate": {"$geoIntersects": {"$geometry": point}}})
        return terreno

    def find_terreni_by_proprietario(self, codice_fiscale):
        terreni = self.terreni.find({"proprietario": codice_fiscale})
        return list(terreni)

    def find_terreni_by_strada(self, strada_coordinate):
        strada_geometria = {
            "type": "LineString",
            "coordinates": strada_coordinate
        }
        terreni = self.terreni.find({
            "coordinate": {
                "$geoIntersects": {
                    "$geometry": strada_geometria
                }
            }
        })

        return list(terreni)

    def aggiungi_terreno(self, terreno):
        self.terreni.insert_one(terreno)
        
    def check_terreno_occupato(self, cordinate_nuovo_terreno):
        for new_cord in cordinate_nuovo_terreno:
            if self.terreni.find_one({ "coordinate": { "$geoIntersects": {"$geometry": new_cord }}}):
                return True
            else: return False

    def find_terreni(self):
        terreni = self.terreni.find()
        print(terreni)
        return list(terreni)

if __name__ == '__main__':
    db = TerrenoDatabase(port=27017)

    while True:
        ## pulisce il terminale
        if os.name == 'nt':
            # Per Windows
            os.system('cls')
        else:
            # Per Unix/Linux/macOS
            os.system('clear')


        print("Applicazione per il censimento dei terreni, a cura di FLavio Manna, Michele Potsios, Mirko La Rocca\n")
        print("1. Cerca terreno per punto geografico")
        print("2. Cerca terreni per codice fiscale")
        print("3. Cerca terreni coinvolti da una nuova strada")
        print("4. Aggiungi nuovo terreno")
        print("5. Visualizza tutti i terreni")
        print("q. Esci")

        scelta = input("\nScegli un'opzione: ").lower().strip()


        if scelta == 'q': break

        try:
            scelta = int(scelta)
            assert scelta <= 5
        except:
            continue

        ## cerca terreno per un punto geografico
        if scelta == 1:
            print('Inserisci q per terminare il processo\n')

            lat = input("Inserisci la latitudine: ").lower().strip()
            if lat != 'q':

                lon = input("Inserisci la longitudine: ").lower().strip()
                if lon != 'q':
                    try:
                        lat, lon = float(lat), float(lon)

                        # Utilizza il metodo find_terreno_by_point per cercare il terreno
                        terreno = db.find_terreno_by_point(lat, lon)

                        print("\nTerreno trovato:")
                        for k, v in terreno.items():
                            if k in ["_id", 'type']:
                                continue
                            if k == 'coordinate':
                                print(f'{k}: {v["coordinates"]}')
                                continue
                            print(f'{k}: {v}')
                    except:
                        print('Inserisci valori validi')

            input('\nPremi invio per continuare')


        elif scelta == 2:
            codice_fiscale = input("Inserisci il codice fiscale: ").strip()
            terreni = db.find_terreni_by_proprietario(codice_fiscale)

            if terreni:
                print("\nTerreni trovati:")
                for terreno in terreni:
                    print('')
                    for k, v in terreno.items():
                        if k in ["_id", 'type']:
                            continue
                        if k == 'coordinate':
                            print(f'{k}: {v["coordinates"]}')
                            continue
                        print(f'{k}: {v}')
            else:
                print('Nessun terrreno trovato')

            input('\nPremi invio per continuare')

        ## trova terreni per strada
        ## la strada puo' essere formata da piu' punti
        ## l'idea di utilizzare gli id della strada penso abbia senso
        ## solo se aggiungiamo un opzione a parte per salavare le strade
        elif scelta == 3:
            i = 1
            cord = []
            while True:
                lat = input(f"Latitudine {i}° punto: ").lower().strip()
                if lat == 'q': break

                lon = input(f"Longitudine {i}° punto: ").lower().strip()
                if lon == 'q': break

                cord.append([float(lon), float(lat)])

                i += 1

            if i < 3:
                print('Inserisci almeno 2 punti')
            else:
                terreni = db.find_terreni_by_strada(cord)

                if terreni:
                    print("\nTerreni trovati:")
                    for terreno in terreni:
                        for k, v in terreno.items():
                            if k in ["coordinate", "_id", 'type']:
                                continue
                            print(f'{k}: {v}')
                        print('')

                else:
                    print('\nNessun terreno trovato.')

            input('\nPremi invio per continuare...')

        ## aggiungi terreno
        elif scelta == 4:
            while True:    
                print('Inserisci i punti geografici del terreno (minimo 3), \ninserisci q per passare al prossimo step\n')
                i = 1
                cord = []
                try:
                    while True:
                        lat = input(f"Latitudine {i}° punto: ").lower().strip()
                        if lat == 'q': break

                        lon = input(f"Longitudine {i}° punto: ").lower().strip()
                        if lon == 'q': break

                        cord.append([float(lon), float(lat)])

                        i += 1

                    if len(cord) >= 3:
                        cord = cord + [cord[0]]  # Chiude il poligono
                        proprietario = input("Codice fiscale del proprietario: ")
                        descrizione = input("Descrizione: ")

                        terreno = {
                            "coordinate": {
                                "type": "Polygon",
                                "coordinates": [cord],
                            },
                            "proprietario": proprietario,
                            "descrizione": descrizione,
                        }

                        if db.check_terreno_occupato(cord):
                            print("\nIl terreno è già occupato. Impossibile caricare i dati sul database")
                            break
                        else:
                            db.aggiungi_terreno(terreno)
                            break
                    else: break

                except: 
                    print("Errore coordinate non valide, riprovare")
            input('\nPremi invio per continuare...')

        elif scelta == 5:
            for terreno in db.find_terreni():
                for k, v in terreno.items():
                    if k in ["_id", 'type']:
                        continue
                    if k == 'coordinate':
                        print(f'{k}: {v["coordinates"]}')
                        continue
                    print(f'{k}: {v}')
                print('')

            input('\nPremi invio per continuare...')
