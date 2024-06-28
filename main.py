import pymongo
import json

def get_db(
    host='127.0.0.1',
    port=21017 ## porta base di mongodb
):
    ## connessione al database
    client = pymongo.MongoClient(
        host=host,
        port=port
    )
    
    ## creazione/reset dell collection
    db = client.test
    client.drop_database(db)
    collection = db.test
    
    data_id = collection.insert_one({
        "name": "test",
        "project": "mongodb",
        "team":  ['Flavio', 'Mirko', 'Michele']
    })
    
    #data = collection.find_one({"_id": data_id.inserted_id})
    #print(json.dumps({k:v for k,v in data.items() if k != '_id'}, indent=2))

    return collection
    
if __name__ == '__main__':
    db = get_db(port=8081)

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