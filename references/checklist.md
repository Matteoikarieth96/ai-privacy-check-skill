# Check-list e frasi da evitare

Base verificata il 13 ottobre 2026 su fonti aperte quel giorno. Non è un parere legale. Le fonti di ogni affermazione si cercano con `scripts/fonti.py`.


## Per chi usa l'IA nel proprio studio

Usa questa per non dimenticare un'azione da fare quando il caso è uno studio, una clinica o un'azienda che usa l'IA per sé. Entra nel rapporto solo ciò che ha una norma da citare.

- Elenca gli strumenti di IA già in uso e chi li usa.
- Chiudi gli account personali usati per lavoro. Un account per ogni persona.
- Scegli lo strumento in base ai dati: piano commerciale per i dati comuni, canale separato per i dati delicati.
- Leggi il contratto sui dati del fornitore, soprattutto alla voce dati sensibili, conservazione e addestramento.
- Scrivi una pagina di regole: quali strumenti, quali dati non ci entrano, chi autorizza uno strumento nuovo.
- Dai a chi lavora sui dati una lettera con le istruzioni.
- Di' a clienti, pazienti o dipendenti che usi l'IA, e aggiorna l'informativa privacy.
- Valuta per iscritto se serve la valutazione d'impatto.
- Cifra i dischi, attiva l'accesso a due fattori.
- Fai formazione, con programma e firme.
- Fai rileggere contratti, informativa e valutazione d'impatto a un legale privacy.

## Check-list per chi prende un incarico da un cliente

Usa questa quando chi chiede è un consulente o uno sviluppatore che lavorerà sui dati di un cliente.

**Alla prima call**

- Che dati vedremo? Ci sono salute, politica, sindacato, condanne o reati?
- Chi è il titolare? Ha un consulente privacy o un DPO?
- Che account di IA usano oggi, e chi li condivide?
- Su quali piani girano i loro servizi?

**Prima di toccare un dato vero**

- NDA firmato da tutte e due le parti, con la clausola che blocca i dati veri fino all'atto ex art. 28.
- Atto ex art. 28 con finalità, categorie di dati, durata e sub-responsabili.
- Autorizzazioni nominative per chi lavora sui dati.
- Solo account commerciali, nessuno strumento fuori elenco.
- Disco cifrato sui computer coinvolti.
- Cartella dei dati veri fuori da git e da ogni sincronizzazione.
- Lista "cosa non mandarci" inviata al cliente prima del kickoff.

**Se c'è un prodotto**

- Servizi intestati al cliente, con contratto sui dati, nelle regioni dichiarate.
- Ambiente di prova separato, con dati sintetici.
- Informativa e contratti del prodotto controllati riga per riga contro la realtà tecnica.
- Valutazione d'impatto chiesta al titolare, con la bozza tecnica preparata da noi.
- Residenza UE quotata come opzione esplicita.


## Cosa non dire e cosa dire

| Non lo diciamo | Perché | Cosa diciamo invece |
|---|---|---|
| "Compliant", "rischio zero" | Nessuno può garantirlo | "Abbiamo un metodo scritto e lo applichiamo" |
| "Anonimo" | Senza nomi il dato resta personale | "Dati di esempio o sintetici" |
| "Server in UE, quindi a posto" | Account, assistenza e casa madre possono stare fuori | "Ecco dove sta ogni pezzo" |
| "È europeo, quindi è conforme" | Anche un fornitore europeo può addestrare di default | "Ecco cosa dice il suo contratto" |
| "Col modello locale siete a posto" | Restano sicurezza, documenti e informazione | "Togliamo i trasferimenti, il resto lo facciamo insieme" |
| "Breach a 96 ore" | È ancora una proposta | "72 ore, art. 33 GDPR" |

