# Python Developer - Assignment

L'esercizio consiste due fasi: importare dati in un database relazionale ed esporli tramite API REST.

Il file dataset.csv contiene report giornalieri:

| date       | restaurant  | planned_hours | actual_hours | budget  | sells   |
|------------|-------------|---------------|--------------|---------|---------|
| 2016-01-01 | Copacabana  | 141           | 176          | 4025.65 | 2801.33 |
| 2016-01-01 | Noodle Bar  | 108           | 76           | 2455.75 | 3875.81 |
| 2016-01-01 | Jack Rabbit | 30            | 156          | 116.99  | 3967.95 |
| 2016-01-02 | Copacabana  | 189           | 135          | 611.8   | 197.57  |
| 2016-01-02 | Noodle Bar  | 136           | 205          | 684.13  | 1720.22 |
| ...        | ...         | ...           | ...          | ...     | ...     |

* **date**: Data del report
* **restaurant**: Nome del ristorante
* **planned_hours**: Ore di lavoro pianificate
* **actual_hours**: Ore di lavoro effettuate
* **budget**: Fatturato giornaliero stimato
* **sells**: Fatturato giornaliero reale

# Esercizio di Sviluppo per Python Developer

Questo esercizio è diviso in due parti: una **Parte Principale** obbligatoria e una **Parte Opzionale** che offre la possibilità di esplorare funzionalità avanzate. Si consiglia di completare prima la Parte Principale e, solo se il tempo lo permette, di procedere con la Parte Opzionale.

## Parte Principale
### Obiettivo
Creare una solida base funzionale per l'importazione di dati e la loro esposizione tramite API REST.

### Compiti
1. **Importazione dei Dati**:
   - Implementare una procedura di importazione per il file `dataset.csv` che possa essere avviata in qualsiasi momento con un comando.
   - Calcolare la differenza tra `planned_hours` e `actual_hours`, e tra `budget` e `sells`.

2. **API REST**:
   - Sviluppare una API REST che esponga i dati importati.
   - Implementare funzionalità di filtro per ristorante e raggruppamento di dati per data e ristorante, con applicazione della funzione SQL di aggregazione *SUM*.

### Criteri di Valutazione
- Correttezza della procedura di importazione.
- Funzionalità e design dell'API.
- Codice pulito e ben organizzato.

## Parte Opzionale
### Obiettivo
Estendere l'applicazione con funzionalità avanzate che migliorano l'interattività e la personalizzazione dell'API.

### Compiti
1. **Funzionalità Avanzate dell'API**:
   - Aggiungere il filtraggio per range di date (`date__lte`, `date__gte`).
   - Implementare l'ordinamento per ogni campo disponibile, incluso i delta calcolati, sia in ordine crescente che decrescente.

2. **Test Automatici**:
   - Scrivere test automatici per verificare la funzionalità e la robustezza dell'API.

### Criteri di Valutazione
- Implementazione delle funzionalità avanzate.
- Copertura e qualità dei test automatici.
- Capacità di ottimizzazione e miglioramento del codice esistente.

## Note Generali
- Si raccomanda di utilizzare Git per il versionamento del codice durante lo sviluppo dell'esercizio.