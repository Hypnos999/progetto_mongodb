import pymongo
import json

def main(
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
    
    data = collection.find_one({"_id": data_id.inserted_id})
    print(json.dumps({k:v for k,v in data.items() if k != '_id'}, indent=2))
    
if __name__ == '__main__':
    main(port=8081)