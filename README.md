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
TerrenoDatabase
TerrenoDatabase è una classe Python progettata per interagire con un database MongoDB per la gestione e la ricerca di terreni. La classe include metodi per caricare dati iniziali, trovare un terreno tramite coordinate geografiche e trovare terreni per proprietario.

Requisiti
- Python 3.x
- Libreria pymongo

Installazione
Per installare le dipendenze necessarie, puoi usare il comando pip per installare pymongo. Assicurati inoltre di avere un'istanza di MongoDB in esecuzione. Di default, la classe si connette a localhost sulla porta 27017.

Metodi
Caricamento dei dati iniziali
Il metodo carica_dati_iniziali consente di caricare i dati iniziali da un file JSON nella collezione terreni.

Ricerca di un terreno tramite coordinate
Il metodo find_terreno_by_point permette di trovare un terreno specifico utilizzando le coordinate geografiche di latitudine e longitudine.

Ricerca di terreni tramite codice fiscale del proprietario
Il metodo find_terreni_by_proprietario consente di trovare terreni specifici utilizzando il codice fiscale del proprietario.

Indicizzazione
La collezione terreni utilizza un indice geospaziale sul campo coordinate per supportare query geospaziali efficienti. Questo indice viene creato automaticamente quando viene inizializzata un'istanza di TerrenoDatabase.


