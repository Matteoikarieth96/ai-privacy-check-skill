# Regole generali, Italia e UE

Base verificata il 13 ottobre 2026 su fonti aperte quel giorno. Non è un parere legale. Le fonti di ogni affermazione si cercano con `scripts/fonti.py`.


## Le norme che valgono per tutti

| Norma | In vigore da | Cosa regola in pratica |
|---|---|---|
| **GDPR**, Reg. (UE) 2016/679 | 25 maggio 2018 | Ogni dato personale, con o senza IA: ruoli, basi giuridiche, sicurezza, trasferimenti, diritti delle persone. |
| **Codice Privacy**, D.Lgs. 196/2003 | Testo adeguato al GDPR dal 19 settembre 2018 | Regole italiane: persone autorizzate, garanzie per dati sanitari e giudiziari, marketing, reato di trattamento illecito. |
| **AI Act**, Reg. (UE) 2024/1689, modificato dal Reg. (UE) 2026/1744 | A scaglioni. Divieti e formazione dal 2 febbraio 2025. Trasparenza dal 2 agosto 2026. Alto rischio dal 2 dicembre 2027 (allegato III) e dal 2 agosto 2028 (prodotti regolati) | Obblighi per chi fornisce e per chi usa sistemi di IA. Chi li usa nel lavoro si chiama "deployer". |
| **Legge 132/2025** | 10 ottobre 2025 | Regole italiane su sanità, lavoro, professioni, giustizia e minori: dire che si usa l'IA e lasciare la decisione a una persona. Non aggiunge obblighi a quelli dell'AI Act. |
| **D.Lgs. 179/2026** | 23 ottobre 2026 | Autorità di vigilanza (ACN, AgID, Garante per i suoi ambiti), sanzioni, decisioni sul lavoro, formazione negli ordini, equo compenso. |
| **D.Lgs. 160/2026** | 30 settembre 2026 | Responsabilità civile e penale. Nuovo reato (art. 437-bis c.p.) per chi omette misure di sicurezza o di controllo umano su sistemi ad alto rischio, se ne nasce un pericolo per le persone. |
| **Codice penale, art. 615-ter** | Pene aumentate dal 17 luglio 2024 | Accesso abusivo a un sistema informatico. Riguarda gli agenti che entrano nei portali con credenziali altrui. |


## Problemi e soluzioni

| Problema | Cosa fare | Norme |
|---|---|---|
| **Non è chiaro chi risponde dei dati.** | Scrivi la catena prima di toccare un dato vero. Il cliente che decide perché e come si trattano i dati è **titolare**. Chi li tratta per suo conto è **responsabile** e gli serve un contratto scritto. Ogni fornitore aggiunto dal responsabile è un **sub-responsabile**: serve l'autorizzazione scritta del titolare, che deve conoscerli tutti per nome. Chi usa i dati per scopi propri diventa titolare. | GDPR art. 28(2), 28(3), 28(4), 28(10); GDPR art. 29; Codice Privacy art. 2-quaterdecies; EDPB Linee guida 07/2020; EDPB Parere 22/2024 |
| **In studio si usa un account personale di IA per lavorare.** | Passa a un piano commerciale con contratto sul trattamento dei dati (DPA), un posto per persona. I termini consumer di Anthropic vietano l'uso professionale. Quelli di OpenAI non lo vietano, ma i piani individuali addestrano i modelli salvo opt-out e il DPA è legato ai contratti Business, Enterprise e API. | GDPR art. 28; GDPR art. 32; Anthropic Consumer Terms sez. 11; OpenAI Condizioni d'uso Europa |
| **Nei documenti ci sono dati su salute, opinioni politiche, sindacato, condanne o reati.** | Trattali su un canale separato. Leggi il DPA del fornitore: quelli di Anthropic e Mistral indicano "None" alla voce categorie particolari; quello di OpenAI dice che non se ne prevede l'invio; quelli di Google Cloud e AWS non le escludono. Senza una conferma scritta: dati sintetici, modello su cloud UE con DPA adatto, oppure modello locale. | GDPR art. 9; GDPR art. 10; Codice Privacy art. 2-septies, 2-octies; DPA Anthropic Schedule 1 B.3; DPA Mistral Exhibit 1; DPA OpenAI allegato 1; Google CDPA sez. 2.1; DPA AWS |
| **Il fornitore è americano o i dati escono dall'UE.** | Usa le clausole contrattuali tipo e valuta per iscritto il trasferimento. Il Data Privacy Framework è in vigore ma sotto esame, e vale solo per le società iscritte nella lista: oggi ci sono Google, Microsoft e Amazon, non risultano Anthropic e OpenAI. Anche l'assistenza da remoto da un paese terzo è un trasferimento. Non scrivere "dati solo in UE" se non è vero. | GDPR art. 44-46; Decisione (UE) 2021/914; Decisione (UE) 2023/1795; EDPB Raccomandazioni 01/2020; EDPB Linee guida 05/2021; CGUE C-311/18 |
| **"Ho tolto i nomi, quindi è anonimo."** | Non lo è. Senza nomi il dato è al massimo pseudonimizzato e resta personale per chi può risalire alla persona. Nel 2026 il Garante ha sanzionato per 7 milioni una società che riteneva anonimi dati sanitari protetti solo da un codice sostitutivo. Scrivi "dati di esempio" o "dati sintetici", mai "anonimi". | GDPR art. 4(5); CGUE C-413/23 P; Garante provv. 710/2026; EDPB Linee guida 01/2025 (bozza); EDPB Linee guida 02/2026 (bozza) |
| **Introduci l'IA su dati delicati o su persone fragili.** | Fai la valutazione d'impatto (DPIA) prima di partire. Come regola pratica serve quando ricorrono due criteri tra: dati sensibili, persone vulnerabili (dipendenti, pazienti, minori), tecnologia nuova, larga scala. L'elenco del Garante cita proprio l'IA, quando c'è almeno un altro criterio. | GDPR art. 35; WP248 rev.01; Garante provv. 467/2018 voce 7 |
| **Manca il registro dei trattamenti.** | Tienilo, come titolare e come responsabile. L'esenzione sotto i 250 dipendenti non vale se il trattamento non è occasionale o riguarda dati degli artt. 9 e 10. La soglia potrebbe cambiare: una modifica va al voto a fine novembre 2026. | GDPR art. 30(2), 30(5); procedura 2025/0130(COD) |
| **L'IA decide, o pesa molto, su una decisione che riguarda una persona.** | Fai decidere una persona che può davvero cambiare l'esito, e sappi spiegare la decisione. Vale anche per un punteggio automatico, se chi decide lo segue quasi sempre. | GDPR art. 22; GDPR art. 15(1)(h); CGUE C-634/21; CGUE C-203/22; AI Act art. 86 |
| **Non hai detto a clienti, pazienti o dipendenti che usi l'IA.** | Dillo, con parole semplici. È un obbligo distinto dall'informativa privacy: per i professionisti verso il cliente, in sanità verso il paziente, per il datore verso i lavoratori. Aggiorna anche l'informativa privacy con il fornitore tra i destinatari e gli eventuali trasferimenti. Un sistema che dialoga con le persone deve far sapere che è un'IA. | L. 132/2025 art. 7, 11, 13; D.Lgs. 152/1997 art. 1-bis; GDPR art. 13-14; AI Act art. 50 |
| **Un chatbot o un assistente risponde direttamente a clienti, pazienti o dipendenti.** | Fai sapere subito a chi scrive che sta parlando con un'IA, salvo che sia ovvio. Prevedi il passaggio a una persona e non far uscire risposte che pesano su qualcuno senza controllo. Se metti il sistema a disposizione col tuo nome, per la legge europea sull'IA puoi essere tu il fornitore: decidilo nel contratto con chi lo sviluppa. | AI Act art. 50; AI Act art. 3(3), 3(4); L. 132/2025 art. 13 |
| **Il personale usa l'IA senza formazione e senza regole.** | Organizza la formazione e scrivi una regola interna di una pagina: quali strumenti, quali dati non ci entrano, chi autorizza uno strumento nuovo. La norma europea chiede misure per sostenere le competenze, non un livello garantito. Per gli iscritti agli ordini l'IA entra nella formazione obbligatoria. | AI Act art. 4 (testo dal 27/7/2026); D.Lgs. 179/2026 art. 47 |
| **Qualcosa va storto: dati persi, rubati o mandati alla persona sbagliata.** | Il responsabile avvisa il titolare senza ritardo. Il titolare notifica al Garante entro 72 ore, con la procedura online, salvo che il rischio sia improbabile, e avvisa le persone se il rischio è elevato. Decidi prima chi chiama chi. | GDPR art. 33; GDPR art. 34; Garante provv. 209/2021 |
| **Un agente entra in un portale con le credenziali di un'altra persona.** | Non farlo senza aver letto le condizioni del portale e senza un ok scritto del gestore. È accesso abusivo anche quello di chi è abilitato ma viola i limiti posti dal titolare del sistema. Le pene sono più alte per i sistemi sanitari e di interesse pubblico. Il portale INPS, per esempio, scrive che le credenziali sono personali e che non si possono usare robot. | Codice penale art. 615-ter; Cass. SS.UU. 4694/2012; Cass. SS.UU. 41210/2017; avvertenze di accesso INPS |
| **L'IA serve a selezionare, valutare o controllare lavoratori.** | Informa prima i lavoratori. Se lo strumento permette un controllo a distanza serve l'accordo sindacale o l'autorizzazione dell'Ispettorato. Le decisioni finali su assunzione, modifica e fine del rapporto le prende una persona, altrimenti sono nulle. Riconoscere le emozioni sul lavoro è vietato. | L. 300/1970 art. 4, art. 8; D.Lgs. 152/1997 art. 1-bis; L. 132/2025 art. 11; D.Lgs. 179/2026 art. 41, 42; AI Act art. 5(1)(f); AI Act allegato III punto 4 |
| **Vendi col tuo marchio uno strumento di IA costruito da altri.** | Per l'AI Act chi immette un sistema sul mercato a proprio nome è fornitore, anche se lo ha sviluppato un altro. Chi lo usa nel lavoro è deployer. Decidilo nel contratto, prima. | AI Act art. 3(3), 3(4); AI Act art. 25 |
| **Quanto si rischia.** | GDPR: fino a 10 milioni o 2% del fatturato per gli obblighi di titolare e responsabile; fino a 20 milioni o 4% per principi, basi giuridiche, diritti e trasferimenti. AI Act: fino a 35 milioni o 7% per le pratiche vietate, 15 milioni o 3% per gli altri obblighi; per le PMI vale l'importo più basso. Il trattamento illecito fatto per profitto o per danneggiare può essere reato. | GDPR art. 83; AI Act art. 99; D.Lgs. 179/2026 art. 23; Codice Privacy art. 167 |


## Scadenze in arrivo

- **23 ottobre 2026.** Entra in vigore il D.Lgs. 179/2026: decisioni sul lavoro, formazione negli ordini, sanzioni nazionali per l'AI Act.
- **30 ottobre 2026.** Si chiudono le consultazioni EDPB sulle linee guida per anonimizzazione (02/2026) e web scraping (03/2026).
- **12 novembre 2026.** Nuova versione della Usage Policy di Anthropic, con più aree considerate ad alto rischio.
- **23 novembre 2026.** Voto indicativo in plenaria sulla modifica che tocca la soglia del registro dei trattamenti.
- **2 dicembre 2026.** Fine della tolleranza sulla marcatura dei contenuti generati per i sistemi già sul mercato. Nuovi divieti dell'AI Act su immagini intime non consensuali.
- **26 marzo 2027.** Inizia ad applicarsi lo Spazio europeo dei dati sanitari. Le parti operative arrivano nel 2029 e nel 2031.
- **23 aprile 2027.** Termine, calcolato da noi, entro cui i consigli nazionali degli ordini adeguano i regolamenti sulla formazione in materia di IA.
- **2 dicembre 2027.** AI Act, obblighi per i sistemi ad alto rischio dell'allegato III: lavoro, credito, assicurazioni, giustizia.
- **2 agosto 2028.** AI Act, alto rischio per i prodotti regolati, dispositivi medici compresi.


## La catena dei ruoli

Ogni anello ha un documento che lo lega al precedente. Senza quel documento il passaggio di dati non è coperto.

| Anello | Chi è | Documento che serve |
|---|---|---|
| Titolare | Chi decide perché e come si usano i dati: lo studio, la clinica, l'azienda | Base giuridica, informativa, registro, valutazione d'impatto quando serve |
| Responsabile | Chi tratta i dati per conto del titolare con accesso sistematico: il fornitore del gestionale, chi eroga il servizio, chi installa e assiste | Contratto scritto ex art. 28 GDPR, firmato prima dei dati |
| Sub-responsabile | Ogni fornitore che il responsabile aggiunge: il modello di IA, il cloud, il database | Autorizzazione scritta del titolare, che lo conosce per nome e può rifiutarlo; stessi obblighi a cascata |
| Persone autorizzate | Chi, dentro ogni organizzazione, tocca davvero i dati | Lettera nominativa con le istruzioni: cosa si può caricare e cosa no |

Chi usa i dati per scopi propri, anche solo per addestrare un modello, esce dal ruolo e diventa titolare. Chi ha accesso solo incidentale non è responsabile.

## Se lo strumento è già in uso

Capita spesso: lo studio usa l'IA da mesi, magari con un account personale condiviso, e chiede cosa rischia. In questo caso `caso.gia_in_uso` è vero e le prime azioni da fare del rapporto hanno `quando` uguale a `subito`. L'ordine conta, perché cancellare subito tutto distrugge ciò che serve a capire cosa è successo.

1. **Ferma.** Smetti di caricare dati veri sullo strumento che non regge: account personale, piano gratuito, strumento senza contratto. Se la password è condivisa, cambiala.
2. **Ricostruisci.** Fai l'elenco di cosa è stato caricato, da chi, da quando, e di quali persone parlano quei documenti. Guarda se l'uso dei testi per l'addestramento era attivo.
3. **Valuta.** Con l'elenco in mano, chiedi a un legale privacy se quanto accaduto è una violazione da notificare al Garante e se vanno avvisate le persone. I termini sono stretti: 72 ore da quando il titolare lo viene a sapere.
4. **Rimedia.** Spegni l'addestramento nelle impostazioni, cancella le conversazioni, e solo dopo passa allo strumento adatto.
5. **Sistema il resto.** Ruoli scritti, contratti, informazione a clienti o pazienti, come in ogni altro caso.

Cosa dice la base, con gli id per recuperare le fonti:

| Tema | Cosa risulta | Dove |
|---|---|---|
| Account personale e credenziali | I termini consumer di Anthropic e di OpenAI vietano di condividere le credenziali. Quelli di Anthropic vietano anche l'uso professionale. | [ven-01, au-26, au-27] |
| Testi già usati per l'addestramento | Spegnere l'addestramento o cancellare le chat vale per il futuro: ciò che è già entrato in un addestramento resta. | [au-28, au-29] |
| Fornitore senza contratto | Per il Garante trattare dati tramite un fornitore senza atto ex art. 28 è un trattamento illecito: sanzioni da 30.000 e 40.000 euro nel 2022. | GDPR art. 5, 6, 28 [vl-09] |
| È una violazione da notificare? | Le linee guida europee definiscono violazione ogni divulgazione non autorizzata, ma parlano di incidenti di sicurezza. Nessun atto italiano dice che caricare dati su un account personale lo sia. L'autorità olandese lo ha affermato per il dipendente che agisce contro le regole interne. | GDPR art. 4(12), 33, 34; EDPB Linee guida 9/2022 [vl-07, vl-08, vl-10] |
| Risarcimento | Chi subisce un danno, anche non patrimoniale, per una violazione del GDPR può chiedere il risarcimento. La sola violazione non basta: serve un danno. Anche il timore di un uso abusivo dei dati può esserlo. | GDPR art. 82; CGUE C-300/21, C-340/21 [vl-11, vl-12] |
| Responsabilità di chi decide | Il titolare deve poter dimostrare di aver adottato misure adeguate. | GDPR art. 5(2), 24 [vl-13, vl-14] |

Non spetta alla skill dire se una violazione c'è stata: descrivi i fatti, indica la norma e rimanda al legale. Scrivilo tra i punti aperti.

## Quando l'IA parla con le persone

L'obbligo di far sapere che risponde un'IA grava su chi fornisce il sistema, che deve progettarlo così; l'informazione va data in modo chiaro al più tardi alla prima interazione [vl-29]. Si applica dal 2 agosto 2026. La Commissione ha pubblicato linee guida il 20 luglio 2026 e un codice di buone pratiche volontario il 10 giugno 2026 [vl-30]. Chi sviluppa in casa un chatbot e lo mette in servizio a proprio nome va trattato come fornitore: chiariscilo nel contratto con chi lo costruisce.

## Altre norme utili

- **Contitolari.** Due soggetti che decidono insieme finalità e mezzi devono ripartire le responsabilità con un accordo. GDPR art. 26 [vl-15].
- **Consultazione preventiva.** Se la valutazione d'impatto indica un rischio elevato che non si riesce ad attenuare, il titolare consulta il Garante prima di partire. GDPR art. 36 [vl-16].
