# Segnali e livello di attenzione

Il livello non è un giudizio di legalità. Dice quanta cura serve prima di partire, o di continuare.

## I nove segnali

Ogni segnale è vero o falso.

Accendi un segnale quando il caso lo dice o lo rende probabile. Se non lo sai, chiedi. Se non puoi chiedere, hai due strade: lasciarlo spento e scrivere la domanda tra i punti aperti, oppure accenderlo e metterlo in `segnali_da_confermare`, così la pagina lo mostra come "da confermare". Non accendere un segnale solo per prudenza generica: ogni segnale acceso obbliga a una riga, e una riga forzata confonde chi legge.

| Segnale | Quando è vero | Quando non lo è |
|---|---|---|
| `dati_personali` | Passa dall'IA un dato riferito a una persona identificata o identificabile. Dati senza nome ma riconducibili a una persona contano. | Testi generici, modelli, bozze senza persone. |
| `dati_particolari` | Salute, opinioni politiche, convinzioni religiose, sindacato, vita sessuale, dati genetici o biometrici (art. 9 GDPR), anche quando emergono in modo indiretto. | |
| `dati_giudiziari` | Condanne, reati, misure di sicurezza, fascicoli penali (art. 10 GDPR). | Cause civili senza profili penali. |
| `lavoratori` | L'oggetto del lavoro sono dati di dipendenti o collaboratori (paghe, personale), oppure lo strumento seleziona, valuta o controlla persone al lavoro. | Il solo fatto che il personale usi lo strumento non lo accende. |
| `minori` | Persone sotto i 18 anni tra gli interessati (pazienti, persone nominate nei documenti) o tra gli utenti dello strumento. | |
| `decisioni_su_persone` | L'IA decide, o chi decide segue quasi sempre il suo risultato, e l'esito pesa su una persona. | L'IA prepara una bozza che una persona rilegge e firma. |
| `portali_di_terzi` | Un agente o uno script entra in un sistema di altri con credenziali. | Una password condivisa tra colleghi non lo accende: è un problema di sicurezza (art. 32 GDPR) e di termini del fornitore. |
| `fuori_ue` | Un fornitore ha sede o server fuori dall'UE, o qualcuno accede ai dati da un paese terzo. | Fornitore e trattamento restano in UE, verificato sul contratto. |
| `dialoga_con_persone` | Un chatbot o un assistente risponde direttamente a clienti, pazienti, dipendenti o pubblico. | L'IA è usata solo da chi lavora nello studio. |

## Il livello minimo

| Livello | Scatta quando | Cosa vuol dire |
|---|---|---|
| **alta** | È vero almeno uno tra `dati_particolari`, `dati_giudiziari`, `lavoratori`, `minori`, `decisioni_su_persone`, `portali_di_terzi` | Non si parte senza ruoli scritti, valutazione d'impatto valutata per iscritto e un canale tecnico adatto. Serve un legale privacy. |
| **media** | È vero `dati_personali`, `fuori_ue` o `dialoga_con_persone`, e nessuno dei segnali sopra | Servono contratto con il fornitore, informativa aggiornata, account commerciali. |
| **bassa** | Nessun segnale | Nessun dato personale passa dall'IA. Restano gli obblighi di informazione e di formazione. |

Puoi alzare il livello se il caso lo merita, per esempio per la scala o per la fragilità delle persone coinvolte. Non puoi abbassarlo: il validatore lo impedisce.

## Copertura obbligatoria

Per ogni segnale vero, almeno un'azione del rapporto, di qualunque tipo, deve citare la norma indicata, scritta con il nome dell'atto. Il validatore distingue gli atti: "c.p.c. art. 96" non vale come "GDPR art. 9".

| Segnale | Almeno un'azione deve citare |
|---|---|
| `dati_personali` | GDPR art. 28 (ruoli e contratto) |
| `dati_particolari` | GDPR art. 9 e GDPR art. 35 (categorie particolari e valutazione d'impatto) |
| `dati_giudiziari` | GDPR art. 10 |
| `lavoratori` | D.Lgs. 152/1997 oppure L. 300/1970 |
| `minori` | Codice Privacy art. 2-quinquies, oppure L. 132/2025 art. 4, oppure WP248, oppure Garante provv. 467/2018. Le prime due riguardano i minori come utenti; le altre due i minori come persone vulnerabili di cui si trattano i dati |
| `decisioni_su_persone` | GDPR art. 22 |
| `portali_di_terzi` | Codice penale art. 615-ter |
| `fuori_ue` | GDPR art. 44 e seguenti (trasferimenti) |
| `dialoga_con_persone` | AI Act art. 50 (chi parla con un'IA deve saperlo) |
| settore commercialisti o avvocati | L. 132/2025 art. 13 (informazione al cliente) |
| settore sanità | L. 132/2025 art. 7 (informazione al paziente, decisione al medico) |

Se lo strumento è già in uso (`caso.gia_in_uso` vero) serve almeno un'azione `da_fare` con `quando` uguale a `subito`.

La copertura è un minimo. Un rapporto buono aggiunge le regole di settore, la sicurezza, la formazione e ciò che è specifico del caso.

## Frasi che il rapporto non afferma

"Rischio zero", "pienamente conforme", "GDPR compliant", "dati anonimi", "è anonimo", e ogni affermazione del tipo "lo studio è conforme", "siete a posto", "risulta a norma". Il validatore le rifiuta, salvo quando sono tra virgolette perché il testo dice di non usarle. "Non è conforme" si può scrivere, ma di solito è meglio dire cosa manca.
