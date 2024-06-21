# progetto_mongodb
Consegna: 1 Luglio

Gruppo di lavoro: 
- Manna Flavio 
- Potsios Michele
- La Rocca Mirko

Opzioni:
1. Gestore di vendita dei biglietti pe concerti
2. Gestore di catasti e coordinate (vedere slide)

La seconda opzione è la più valida, è più completa e include dei tipi di dati (GEOjson) che non sono presenti nel primo progetto.
La seconda opzione è più difficile ma ne vale la pena.


spiegazione geoJson: https://www.mongodb.com/docs/v3.0/reference/geojson/

Opzioni dell'utente
1. trovare i terreni in base ad un CF (query classiche)
2. trovare il terreno in base ad una coordinata (query $geoWithin)
3. trovare i terreni attraversati da una strada, la strada dovrà essere inserita dall'utente o già caricata come gli altri dati, e dovrà essere una linea non per forza rezza (utilizziamo la query $geoIntersects. per troare i terreni attraversati)