# Medici e strutture sanitarie

Base verificata il 13 ottobre 2026 su fonti aperte quel giorno. Non è un parere legale. Le fonti di ogni affermazione si cercano con `scripts/fonti.py`.


## Regole di settore

| Problema | Cosa fare | Norme |
|---|---|---|
| **Base giuridica.** Serve il consenso per trattare i dati? | Per la cura no: il professionista tenuto al segreto non chiede il consenso per i trattamenti necessari alla prestazione. Serve un'altra base, spesso il consenso, per ciò che non è strettamente cura: promozione, fidelizzazione, app non di telemedicina. | GDPR art. 9(2)(h), 9(3); Garante provv. 55/2019 |
| **Dire al paziente che usi l'IA.** | Il paziente ha diritto di essere informato sull'impiego di tecnologie di IA. Mettilo nell'informativa e rendilo visibile in studio. L'IA è un supporto: la decisione resta sempre al medico. I sistemi vanno verificati e aggiornati periodicamente. | L. 132/2025 art. 7 c. 3, 5, 6 |
| **Dati dei pazienti in un modello di IA.** | Non sui piani a posti. Serve un'applicazione sulle API con il modello in regione UE, contratto che non esclude i dati sanitari, nessuna conservazione dei contenuti, account cloud della struttura. Oppure un modello locale. Il Garante ha messo in guardia anche i pazienti dal caricare referti nei chatbot. | GDPR art. 9; Codice Privacy art. 2-septies; Garante comunicato 30/7/2025 |
| **"Anonimizziamo prima di inviare."** | Quasi mai è vero. Un codice paziente stabile e un raggruppamento parziale non rendono anonimi i dati: sanzione di 7 milioni nel 2026. Usare dati pseudonimizzati per addestrare un algoritmo senza informativa adeguata: 21.000 euro nel 2025. | GDPR art. 4(5); Garante provv. 710/2026; Garante provv. 287/2025 |
| **Registro, DPO, valutazione d'impatto.** | Registro: sempre, anche per il singolo professionista. DPO: non obbligatorio per il singolo professionista; di regola sì per ospedali privati, case di cura e RSA. Valutazione d'impatto: sì quando porti l'IA sui dati dei pazienti. | GDPR art. 30, 35, 37; Garante provv. 55/2019; Garante provv. 467/2018 |
| **Il software suggerisce diagnosi o terapie.** | È un dispositivo medico, almeno di classe IIa: serve un fabbricante con marcatura CE e, dal 2 agosto 2028, vale come sistema ad alto rischio. Un software che archivia, comunica o fa ricerche semplici non lo è. Un dispositivo di classe I senza organismo notificato non è alto rischio per l'AI Act. | Reg. (UE) 2017/745 allegato VIII regola 11; MDCG 2019-11 rev.1; AIB 2025-1 / MDCG 2025-6; AI Act art. 6(1) |
| **Il fornitore del gestionale.** | È responsabile del trattamento e paga in proprio per la sicurezza. Nel 2026: 10.000 euro a un fornitore di gestionali dopo un ransomware (utenze amministrative condivise, niente autenticazione a più fattori, firewall non aggiornato) e 16.000 euro a un produttore di apparecchi (credenziali condivise, dati non cifrati). Chiedi account nominativi, autenticazione a più fattori, log, cifratura. | GDPR art. 28, 32; Garante provv. 460/2026; Garante provv. 525/2026 |
| **Chi installa e assiste i sistemi.** | È amministratore di sistema: designazione individuale con ambiti definiti, registrazione degli accessi conservata almeno sei mesi, verifica almeno annuale. | Garante provv. 27/11/2008 |
| **Registrare e trascrivere le visite.** | Non esiste oggi un'indicazione del Garante o dell'EDPB. Prassi prudente: informa il paziente e chiedi il permesso, canale UE senza conservazione o modello locale, audio cancellato appena c'è il testo, rilettura del medico, valutazione d'impatto. | L. 132/2025 art. 7 c. 3; GDPR art. 13, 35 |
| **Portali di fondi e assicurazioni.** | Ok scritto del gestore prima di automatizzare: per i sistemi sanitari l'accesso abusivo è punito da tre a dieci anni. Sulla base giuridica per comunicare i dati del paziente al fondo non abbiamo trovato indicazioni ufficiali successive al GDPR: va chiesto a un legale. | Codice penale art. 615-ter; Garante provv. 55/2019 |
| **Ricerca con dati sanitari.** | Per enti pubblici, enti senza scopo di lucro e IRCCS la ricerca su sistemi di IA è di rilevante interesse pubblico: va comunicata al Garante e può partire dopo 30 giorni. Per la ricerca medica senza consenso servono comitato etico e valutazione d'impatto. | L. 132/2025 art. 8; Codice Privacy art. 110 |
| **Formazione.** | L'IA entra nella formazione continua (ECM) dei professionisti sanitari. La quota sarà fissata dalla Commissione nazionale entro sei mesi dal 23 ottobre 2026. | D.Lgs. 179/2026 art. 51; AI Act art. 4 |
| **Psicologi.** | Il Consiglio nazionale ha chiesto di comunicare al paziente ogni uso dell'IA, anche marginale, e di non inserire nei chatbot dati identificativi o sensibili. Omettere l'informativa può essere violazione deontologica. | Newsletter CNOP 13/1/2026; L. 132/2025 art. 13 |


## Domande frequenti


**D. Posso usare ChatGPT o Claude per referti e lettere con i dati del paziente?**

In breve: Non con un piano a posti, nemmeno commerciale. Serve un canale costruito apposta.

Il contratto di Anthropic indica "None" alla voce categorie particolari, e i dati di Team ed Enterprise stanno negli USA. Il contratto di OpenAI dice che l'invio di dati sensibili non è previsto.

Il setup minimo è un'applicazione sulle API, con il modello su un cloud in regione UE il cui contratto non esclude i dati sanitari, senza conservazione dei contenuti, nell'account cloud della struttura. Oppure un modello locale. In ogni caso con valutazione d'impatto.

Per quello che non contiene pazienti, come modelli di lettera e protocolli, un piano commerciale va bene.

Norme: GDPR art. 9; DPA Anthropic Schedule 1 B.3; DPA OpenAI allegato 1; Google CDPA sez. 2.1; DPA AWS


**D. Se tolgo nome e cognome è anonimo?**

In breve: No. Resta un dato sanitario.

Basta poco per risalire alla persona: data di nascita, data della visita, una patologia rara. Nel settembre 2026 il Garante ha sanzionato una società per 7 milioni: sosteneva che i dati dei pazienti di circa 800 medici di base fossero anonimi, ma un codice paziente stabile e un raggruppamento parziale non bastavano.

Nel 2025 un'altra società ha preso 21.000 euro per aver addestrato un algoritmo con dati sanitari pseudonimizzati senza un'informativa adeguata.

Di' "dati di esempio" o "dati sintetici".

Norme: GDPR art. 4(5); Garante provv. 710/2026; Garante provv. 287/2025; CGUE C-413/23 P


**D. Devo chiedere il consenso al paziente per usare l'IA?**

In breve: Per la cura non serve il consenso privacy. Serve però dire al paziente che usi l'IA.

Il Garante nel 2019 ha chiarito che il professionista sanitario tenuto al segreto non chiede il consenso per i trattamenti necessari alla cura. Serve un'altra base, spesso il consenso, per ciò che non è strettamente cura: promozione, app, fidelizzazione.

La legge 132/2025 dà al paziente il diritto di sapere che si usano tecnologie di IA. Scrivilo nell'informativa e rendilo visibile in studio.

Attenzione alla deontologia. Dal nostro controllo, gli indirizzi applicativi dell'art. 78 del codice dei medici chiedono il consenso quando si usano strumenti informatici. Non abbiamo letto il testo per intero: verificalo con l'Ordine. Il nuovo codice, che tratterà anche l'IA, è atteso nel 2027.

Norme: GDPR art. 9(2)(h), 9(3); Garante provv. 55/2019; L. 132/2025 art. 7 c. 3


**D. L'IA può proporre diagnosi o terapie?**

In breve: Solo come supporto, e quel software è un dispositivo medico.

La legge dice che l'IA in sanità è un supporto e che la decisione resta sempre al medico. Un software che dà informazioni usate per decisioni diagnostiche o terapeutiche è un dispositivo medico almeno di classe IIa. Serve un fabbricante con marcatura CE e, dal 2 agosto 2028, vale come sistema ad alto rischio per l'AI Act.

Un software che si limita ad archiviare, comunicare o fare ricerche semplici non è un dispositivo. Agenda, solleciti e bozze amministrative restano fuori.

Norme: L. 132/2025 art. 7 c. 5; Reg. (UE) 2017/745 allegato VIII regola 11; MDCG 2019-11 rev.1; AIB 2025-1 / MDCG 2025-6; AI Act art. 6(1)


**D. Posso registrare la visita e farla trascrivere dall'IA?**

In breve: Non c'è ancora una regola italiana. Si può fare, con prudenza.

Né il Garante né l'EDPB hanno dato indicazioni specifiche. In Francia una bozza di guida delle autorità chiede un'informazione leale con diritto di opposizione, e il consenso per registrare la voce. Non è una regola italiana.

La prassi prudente: informa il paziente e chiedi il permesso, usa un canale UE senza conservazione o un modello locale, cancella l'audio appena c'è il testo, rileggi prima di mettere in cartella, fai la valutazione d'impatto. Mai con un'app personale sul telefono.

Norme: L. 132/2025 art. 7 c. 3; GDPR art. 13; GDPR art. 35


**D. Il fornitore dice "server in Europa" e "non addestriamo". Basta?**

In breve: No. Chiedi anche della sicurezza, perché è lì che arrivano le sanzioni.

Nel 2026 il Garante ha sanzionato due fornitori di strutture sanitarie come responsabili del trattamento. Il primo, 10.000 euro dopo un ransomware sul gestionale: utenze amministrative condivise, niente autenticazione a più fattori, firewall non aggiornato. Il secondo, 16.000 euro: credenziali generiche condivise, niente autenticazione a più fattori, dati non cifrati.

Cinque domande da fare. Gli account sono nominativi? C'è l'autenticazione a più fattori? Ci sono i log degli accessi? I dati sono cifrati a riposo? Chi può accedere da fuori UE?

E ricorda che "regione UE" non vuol dire "dati solo in UE": spesso account, assistenza e telemetria escono.

Norme: GDPR art. 28; GDPR art. 32; Garante provv. 460/2026; Garante provv. 525/2026


**D. Sono uno studio piccolo. Registro, DPO e valutazione d'impatto valgono anche per me?**

In breve: Registro sì. DPO no, se sei un singolo professionista. Valutazione d'impatto sì, quando porti l'IA sui dati dei pazienti.

Il Garante nel 2019 ha chiarito che il registro è obbligatorio anche per il singolo professionista sanitario, che invece non deve nominare il DPO. Ospedali privati, case di cura e RSA di regola sì.

La valutazione d'impatto è dovuta quando si sommano due criteri di rischio. Dati sanitari, pazienti e tecnologia nuova ne fanno tre.

Norme: GDPR art. 30, 35, 37; Garante provv. 55/2019; Garante provv. 467/2018; WP248 rev.01


## Caso di esempio, inventato


### Caso 2. Poliambulatorio Beta, sanità

**Scenario inventato.** Dodici persone: quattro medici, due odontoiatri, due igienisti, quattro in segreteria. Vuole usare l'IA per tre cose: scrivere lettere e relazioni per i pazienti, trascrivere le visite, compilare le richieste di rimborso sui portali dei fondi sanitari.

| Problema | Cosa fare | Norme |
|---|---|---|
| Lettere e relazioni contengono dati sanitari identificabili. | Niente piani a posti. Un'applicazione sulle API con il modello in regione UE, contratto che non esclude i dati sanitari, nessuna conservazione, account cloud della struttura. Oppure un modello locale. | GDPR art. 9; GDPR art. 28; GDPR art. 44-46 |
| I pazienti non sanno dell'IA. | Informativa aggiornata e avviso in sala d'attesa. La lettera la firma il medico dopo averla riletta. | L. 132/2025 art. 7 c. 3, 5; GDPR art. 13 |
| Trascrizione delle visite. | Non c'è una regola italiana. Prassi prudente: permesso del paziente, audio cancellato dopo la trascrizione, rilettura del medico. | L. 132/2025 art. 7; GDPR art. 35 |
| I portali dei fondi chiedono un login. | Ok scritto di ogni gestore. Il modello prepara la pratica, uno script a passi fissi compila e si ferma prima dell'invio, una persona controlla e invia. Credenziali in un archivio protetto della struttura, mai nel modello. | Codice penale art. 615-ter; GDPR art. 32 |
| Chi installa e assiste il sistema ha accesso ai dati. | Diventa responsabile del trattamento e amministratore di sistema: contratto, account nominativi, autenticazione a più fattori, log per sei mesi, verifica annuale. | GDPR art. 28, 32; Garante provv. 27/11/2008; Garante provv. 460/2026 |
| Qualcuno propone di aggiungere un "suggeritore di diagnosi". | Fuori perimetro: sarebbe un dispositivo medico. | Reg. (UE) 2017/745 allegato VIII regola 11 |
| Documenti. | Registro, valutazione d'impatto prima di partire, valutazione scritta sull'obbligo di DPO. | GDPR art. 30, 35, 37; Garante provv. 55/2019 |

**Setup.** Si parte a gradini: prima senza dati, poi dati sintetici, poi dati reali oscurati dalla struttura, poi pseudonimizzati con la chiave alla struttura, infine reali con contratto, valutazione d'impatto e supervisione.

**Costo a listino.** Il consumo di un modello di fascia media in regione UE, con le nostre ipotesi, sta tra circa 90 e 440 dollari al mese. A questo si aggiungono lo sviluppo dell'applicazione e i documenti.


Tra parentesi quadre gli id delle affermazioni nella base: `python3 -B scripts/fonti.py id <id>` ne dà testo, fonte e limiti.

## Righe che la tabella sopra non ha

| Problema | Cosa fare | Norme |
|---|---|---|
| **Tra i pazienti ci sono minori.** | Trattali come persone vulnerabili: è uno dei criteri che fanno scattare la valutazione d'impatto. L'informativa va data a chi esercita la responsabilità genitoriale, in parole comprensibili. | GDPR art. 35; WP248 rev.01; Garante provv. 467/2018 [eu-15, it-37] |
| **Registrando la visita si registra anche chi lavora.** | Informa medici e personale. La registrazione non deve diventare uno strumento per valutarli o controllarli: servirebbero accordo sindacale o autorizzazione dell'Ispettorato. | L. 300/1970 art. 4; D.Lgs. 152/1997 art. 1-bis [it-34, it-36] |
| **La deontologia chiede il consenso per gli strumenti informatici.** | L'art. 78 del codice dei medici e i suoi indirizzi applicativi chiedono il consenso al trattamento dei dati con qualsiasi strumento informatico. È una regola deontologica, diversa dalla lettura del Garante per cui la cura non richiede consenso privacy. Dillo nel rapporto e fai chiedere all'Ordine. | Codice di deontologia medica art. 78 [vl-26]; Garante provv. 55/2019 [san-01] |
| **Il software trascrive e poi scrive la bozza del referto.** | La sola trascrizione è trattata dalla guida europea come sistema di comunicazione. Un software che elabora e riassume dati del paziente per decisioni di cura può essere un dispositivo medico: conta lo scopo dichiarato dal produttore. Chiedi al fornitore come ha qualificato il prodotto. | Reg. (UE) 2017/745 allegato VIII regola 11; MDCG 2019-11 rev.1 [au-30, au-31] |
| **Chi installa o assiste è amministratore di sistema?** | Sì se gestisce e mantiene in modo stabile i sistemi con cui si trattano i dati. No se interviene solo occasionalmente, per un guasto. Il titolare che è anche unico amministratore, in realtà piccolissime, è esentato da verifica annuale e registrazione degli accessi. | Garante provv. 27/11/2008 e FAQ [vl-31, vl-32] |

## Trascrivere le visite: cosa c'è nella base

Non esiste una guida europea o italiana dedicata agli "scribi" clinici con IA [au-32]. L'autorità svedese nel 2026 ha scritto che un sistema che elabora e riassume dati del paziente usati per decisioni di cura probabilmente rientra nelle regole sui dispositivi medici: è la posizione di un'autorità nazionale, non una regola italiana.

Whisper, il modello di trascrizione più diffuso, può scrivere testo che nessuno ha pronunciato: la sua scheda ufficiale ne sconsiglia l'uso in contesti ad alto rischio. Vale anche per i servizi che lo rivendono. La rilettura del medico non è un'opzione.

Modelli, strumenti e prezzi sono in [open-source.md](open-source.md), sezione "Trascrizione vocale". I costi si calcolano con `costi.py --minuti-audio`.

## Domande da fare al fornitore di un software sanitario

1. Come avete qualificato il prodotto: è un dispositivo medico? Di che classe?
2. Quale modello di IA usate, e chi lo eroga? Elenco dei sub-responsabili.
3. Dove vengono elaborati e conservati audio, trascrizioni e referti? Chi può accedere da fuori UE?
4. Per quanto tempo restano l'audio e il testo? Si può avere la conservazione zero?
5. I nostri dati vengono usati per addestrare o migliorare il sistema?
6. Il vostro contratto sui dati copre i dati sanitari?
7. Account nominativi, accesso a due fattori, registro degli accessi, dati cifrati a riposo?
8. Avete già fatto una valutazione d'impatto che possiamo usare come base?

## Portali di fondi e assicurazioni: una cautela

La tabella dice che per i sistemi sanitari l'accesso abusivo è punito da tre a dieci anni. La formula della legge parla di sistemi "relativi alla sanità" o "comunque di interesse pubblico" [vl-27]. Non risulta una decisione sul se il portale di un fondo sanitario o di un'assicurazione privata vi rientri [vl-28]. Scrivi che il reato base c'è comunque (fino a tre anni) e metti l'aggravante tra i punti aperti.
