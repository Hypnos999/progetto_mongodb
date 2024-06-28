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

    # Define a terrain using a GeoJSON Polygon
    geojson_polygon = {
        "type": "Polygon",
        "coordinates": [
            [
                [-73.856077, 40.848447],
                [-73.856147, 40.848477],
                [-73.856117, 40.848407],
                [-73.856077, 40.848447]  # Closing the polygon
            ]
        ]
    }

    document = {
        "name": "Sample Terrain",
        "terrain": geojson_polygon
    }

    # Insert the document
    collection.insert_one(document)

    # Create a 2dsphere index on the terrain field
    collection.create_index([("terrain", pymongo.GEOSPHERE)])

    # Define the point to search for
    search_point = {
        "type": "Point",
        "coordinates": [-73.856077, 40.848447]
    }

    # Query for terrains that intersect with the search point
    query = {
        "terrain": {
            "$geoIntersects": {
                "$geometry": search_point
            }
        }
    }

    results = collection.find(query)

    for result in results:
        print(result)

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