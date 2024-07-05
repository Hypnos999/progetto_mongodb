import pymongo
import os

class TerrenoDatabase:
    def __init__(
            self,
            host,
            port,
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
        return list(terreni)


if __name__ == '__main__':
    while True:
        try:
            host = input('Inserisci l\'host a cui connettersi (lascia vuoto per 0.0.0.0): ').strip()
            port = input('Inserisci la porta (lascia vuoto per 27017): ').strip()

            if host == '':
                host = '0.0.0.0'
            if port == '':
                port = 27017

            db = TerrenoDatabase(host=host, port=int(port))

            break
        except Exception as e:
            print(e)
            print("Errore, riprova")



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
            print('\nInserisci le coordinate geografiche del punto (lat [-90, 90], lon [-180, 180])')
            print('Inserisci q per terminare il processo')

            while True:
                lat = input("Inserisci la latitudine: ").lower().strip()
                if lat == 'q': break

                lon = input("Inserisci la longitudine: ").lower().strip()
                if lon == 'q': break

                try:
                    lat, lon = float(lat), float(lon)

                    # Utilizza il metodo find_terreno_by_point per cercare il terreno
                    terreno = db.find_terreno_by_point(lat, lon)

                    if terreno:
                        print("\nTerreno trovato:")
                        for k, v in terreno.items():
                            if k in ["_id", 'type']:
                                continue
                            if k == 'coordinate':
                                print(f'{k}: {v["coordinates"]}')
                                continue
                            print(f'{k}: {v}')
                    else:
                        print('\nNessun terreno presente')
                    break
                except:
                    print('Coordinate non valide')

            input('\nPremi invio per continuare...')


        elif scelta == 2:
            codice_fiscale = input("\nInserisci il codice fiscale: ").strip()
            terreni = db.find_terreni_by_proprietario(codice_fiscale)

            if terreni:
                print("\nTerreni trovati:")
                for terreno in terreni:
                    for k, v in terreno.items():
                        if k in ["_id", 'type']:
                            continue
                        if k == 'coordinate':
                            print(f'{k}: {v["coordinates"]}')
                            continue
                        print(f'{k}: {v}')
                    print('')

            else:
                print('\nNessun terrreno trovato\n')

            input('Premi invio per continuare...')

        ## trova terreni per strada
        ## la strada puo' essere formata da piu' punti
        ## l'idea di utilizzare gli id della strada penso abbia senso
        ## solo se aggiungiamo un opzione a parte per salavare le strade
        elif scelta == 3:
            i = 1
            cord = []
            print('\nInserisci i punti geografici della strada (minimo 2, lat [-90, 90], lon [-180, 180]), \ninserisci q per passare al prossimo step')

            lat = lon = ''
            while True:
                lat = input(f"Latitudine {i}° punto: ").lower().strip()
                if lat == 'q' and i > 2: break

                lon = input(f"Longitudine {i}° punto: ").lower().strip()
                if lon == 'q' and i > 2: break

                try:
                    lon = float(lon)
                    lat = float(lat)
                    assert lon > -180 and lon < 180
                    assert lat > -90 and lat < 90
                    cord.append([lon, lat])
                    i += 1
                except:
                    print('Coordinate non valide')

            if i < 3: print('')
            else:
                terreni = db.find_terreni_by_strada(cord)

                if terreni:
                    print("\nTerreni trovati:")
                    for terreno in terreni:
                        for k, v in terreno.items():
                            if k in [ "_id", 'type']:
                                continue

                            if k == 'coordinate':
                                print(f'{k}: {v["coordinates"]}')
                                continue
                            print(f'{k}: {v}')
                        print('')

                else:
                    print('\nNessun terreno trovato.\n')

            input('Premi invio per continuare...')

        ## aggiungi terreno
        elif scelta == 4:
            while True:    
                print('\nInserisci le coordinate geografiche degli angoli del terreno (minimo 3, lat [-90, 90], lon [-180, 180]), \ninserisci q per passare al prossimo step')
                i = 1
                cord = []
                try:
                    while True:
                        lat = input(f"Latitudine {i}° punto: ").lower().strip()
                        if lat == 'q': break

                        lon = input(f"Longitudine {i}° punto: ").lower().strip()
                        if lon == 'q': break

                        try:
                            lon = float(lon)
                            lat = float(lat)
                            cord.append([lon, lat])
                            i += 1
                        except:
                            print('Coordinate non valide')


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

                except Exception as e:
                    print("Errore coordinate non valide, riprovare")
            input('\nPremi invio per continuare...')

        ## Visualizza tutti i terreni
        elif scelta == 5:
            print('')
            terreni = db.find_terreni()

            if terreni:
                for terreno in terreni:
                    for k, v in terreno.items():
                        if k in ["_id", 'type']:
                            continue
                        if k == 'coordinate':
                            print(f'{k}: {v["coordinates"]}')
                            continue
                        print(f'{k}: {v}')
                    print('')
            else:
                print('Nessun terreno inserito\n')

            input('Premi invio per continuare...')
