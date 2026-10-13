# Domande iniziali

Chiedi solo ciò che la richiesta non ha già detto. Due giri al massimo, poi riepilogo e conferma.

Ricorda all'utente di descrivere il caso, non di incollare documenti o nomi veri.

## Le domande di base

| # | Domanda | Perché conta | Default se all'utente non importa |
|---|---|---|---|
| 1 | In che settore siamo? | Decide quale file di settore leggere e quali regole di categoria valgono. | nessuno: serve saperlo. Se non è tra i tre coperti, "altro" |
| 2 | Cosa deve fare l'IA, in una riga per obiettivo? | Da qui si capisce se l'IA prepara, suggerisce o decide, e se tocca persone. Al massimo tre obiettivi per analisi. | nessuno: serve saperlo |
| 3 | Che dati ci passano? Comuni, salute, opinioni politiche o sindacato, condanne e reati, dati di dipendenti, minori? | È la risposta che pesa di più: decide il canale tecnico, la valutazione d'impatto e il livello di attenzione. | se non lo sa: tratta il caso come se ci fossero dati delicati |
| 4 | Di chi sono i dati, e chi decide come usarli? Lavori per te o per conto di un cliente? | Decide chi è titolare e chi responsabile, quindi quali contratti servono e chi autorizza il fornitore di IA. | chi chiede è titolare |
| 5 | Chi costruisce, installa o assiste lo strumento, e con quale accesso ai dati? Come si chiama il fornitore, se c'è? | Chi ha accesso sistematico entra nella catena come responsabile o sub-responsabile. Il nome serve per leggere i suoi termini. | se il caso nomina un fornitore o una macchina da installare, un terzo c'è: chiedi. Altrimenti nessun terzo con accesso |
| 6 | Lo strumento è già in uso sui dati veri? Da quando, cosa è stato caricato, con quale account, e l'uso dei testi per l'addestramento è attivo? | Se è già in uso le prime azioni da fare del rapporto riguardano cosa fermare e come rimediare, non cosa preparare. | non ancora in uso |
| 7 | Quali strumenti e account si usano oggi o si vogliono usare? Piano, fornitore, dove girano. | Account personali, piani gratuiti e regioni fuori UE sono i tre errori più frequenti. | nessuno strumento ancora scelto: la skill propone |
| 8 | L'IA parla direttamente con persone, per esempio un chatbot per clienti o dipendenti? Prende decisioni su persone, o le influenza molto? Entra in siti o portali di altri con le credenziali di qualcuno? | Sono tre segnali che cambiano il rapporto: trasparenza verso chi parla con l'IA, decisioni automatizzate, accesso abusivo. | no a tutte e tre |
| 9 | Quante persone lo useranno, e con che volume? Documenti o pagine al mese, minuti di audio se c'è una trascrizione. | Serve per i costi. Il volume si converte con le stime di [costi.md](costi.md): è un'ipotesi da dichiarare. | 4 persone, 20 milioni di token in ingresso e 4 in uscita al mese. Con più persone i volumi non si scalano da soli: chiedi |
| 10 | Ci sono vincoli? Dati solo in UE, budget, preferenza per un modello locale, fornitori già sotto contratto. | Restringe le soluzioni da proporre. | nessun vincolo |
| 11 | Per chi è il rapporto, e vuoi il ricontrollo online delle fonti? | Un rapporto da girare a un terzo va scritto senza gergo interno e con il "voi". Il ricontrollo allunga i tempi ma aggiorna norme e listini. | uso interno, ricontrollo sì |

## Domande in più per settore

Falle solo se il caso le tocca.

| Settore | Domanda | Perché |
|---|---|---|
| Commercialisti | Sei commercialista o consulente del lavoro? | Le regole deontologiche nella base sono dei commercialisti. Per i consulenti del lavoro vedi il riquadro in [commercialisti.md](commercialisti.md). |
| Commercialisti | Fai le paghe per i clienti? | Per le paghe lo studio è di regola responsabile e il fornitore di IA va autorizzato da ogni cliente. |
| Sanità | Ci sono minori tra i pazienti? | Accende il segnale `minori` e cambia informativa e valutazione d'impatto. |
| Sanità | I medici sono dipendenti o liberi professionisti che usano la struttura? | Decide chi è titolare per le finalità di cura. |
| Sanità | Quali portali, fondi o assicurazioni sono coinvolti? | Ognuno ha le sue condizioni d'uso: serve l'ok scritto di ciascuno. |
| Avvocati | Che materie tratta lo studio? Penale, lavoro, famiglia? | Decide se nei fascicoli ci sono dati su reati, salute, minori e persone terze. |
| Avvocati | Studio associato, società, o professionisti che dividono solo i locali? | Cambia chi è titolare. |

## Dalle risposte ai segnali

Le definizioni complete sono in [livelli.md](livelli.md).

| Risposta | Segnale da accendere |
|---|---|
| Qualunque dato riferito a una persona | `dati_personali` |
| Salute, opinioni politiche, sindacato, religione, orientamento, dati genetici o biometrici | `dati_particolari` |
| Condanne, reati, procedimenti, fascicoli penali | `dati_giudiziari` |
| L'oggetto del lavoro sono dati di dipendenti, oppure lo strumento seleziona, valuta o controlla lavoratori | `lavoratori` |
| Persone sotto i 18 anni tra gli interessati o tra gli utenti | `minori` |
| L'IA decide o pesa molto su una decisione che riguarda una persona | `decisioni_su_persone` |
| Un agente o uno script entra in un sito o portale di terzi con credenziali | `portali_di_terzi` |
| Fornitore con sede o server fuori dall'UE, o assistenza da un paese terzo | `fuori_ue` |
| Un chatbot o un assistente risponde direttamente a clienti, pazienti, dipendenti o pubblico | `dialoga_con_persone` |

Documenti ordinari possono nascondere dati delicati: una dichiarazione dei redditi contiene spese sanitarie e scelte dell'8, 5 e 2 per mille; un cedolino contiene malattia, permessi e trattenute sindacali; un fascicolo civile può contenere perizie mediche. Chiedilo.

## Se non c'è nessuno a cui chiedere

In una prova o in un'automazione le domande non hanno risposta. Usa i default, lascia spenti i segnali di cui il caso non parla, scrivi tra i punti aperti ogni domanda rimasta senza risposta e mostra comunque il riepilogo.

## Il riepilogo di chiusura

Scrivilo come elenco breve e aspetta la conferma:

```
Ecco cosa analizzo:
- Caso: ...
- Settore: ...
- Dati: ...
- Già in uso: sì, da ... / no
- Ruoli, in prima ipotesi: ...
- Strumenti: ...
- Persone e volumi: ...
- Vincoli: ...
- Ricontrollo online: sì / no
- Consegno: rapporto di una pagina (si può, non si può, da fare), allegato di dettaglio e sintesi in chat
Confermi?
```
