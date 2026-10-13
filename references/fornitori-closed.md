# Fornitori closed

Base verificata il 13 ottobre 2026 su fonti aperte quel giorno. Non è un parere legale. Le fonti di ogni affermazione si cercano con `scripts/fonti.py`.


## Confronto

| Canale | Addestra sui tuoi dati? | Conservazione | Dati sensibili nel contratto | Dati in UE? | Listino |
|---|---|---|---|---|---|
| **Claude, piani personali** (Free, Pro, Max) Non per lavoro | Sì, salvo opt-out. Il feedback addestra sempre. | Fino a 5 anni se l'addestramento è attivo. Chat cancellate rimosse entro 30 giorni. | Nessun DPA. Uso professionale vietato dai termini. | No | Pro 20 $ al mese, Max da 100 $ |
| **Claude Team** | No. Eccezione: il feedback con il pollice, che il proprietario può spegnere. | Finché l'utente cancella, poi 30 giorni. Nessuna opzione a conservazione zero. | "None" alla voce categorie particolari | No: dati negli USA | 25 $ a posto al mese (20 $ annuale). Premium 125 $ (100 $). Da 2 a 150 posti |
| **Claude Enterprise** | No | Personalizzabile, minimo 30 giorni | "None" | No | 20 $ a posto al mese più i consumi. Minimo 20 posti in self-service, 50 con vendita assistita |
| **Claude, API diretta** | No | 30 giorni. Conservazione zero su richiesta e approvazione. Esclusi i modelli Fable e Mythos. | "None" | No: solo "us" o "global" | Per milione di token, ingresso e uscita: Sonnet 5.5 2 $ e 10 $; Opus 5.5 4 $ e 20 $; Haiku 5.5 0,10 $ e 0,50 $ |
| **Claude su Amazon Bedrock o Google Cloud, regione UE** Per dati delicati | No. Su Bedrock il produttore del modello non vede prompt e risposte. | Dipende dal cloud. Fable e Mythos restano a 30 giorni ovunque. | AWS: non le esclude. Google: le include. | Sì, con profilo o endpoint UE | 10% in più del prezzo globale. Sonnet 5.5 su Google Cloud UE: 2,20 $ e 11,00 $ |
| **ChatGPT, piani individuali** Non per dati di clienti | Sì, salvo opt-out | Non verificata | Nessun DPA sui piani individuali | No | Non verificato |
| **ChatGPT Business** | No di default | La gestisce l'amministratore | "Non previsti", salvo inserimento imprevisto | Non verificato per questo piano | 25 $ a posto al mese (20 $ annuale). Da 2 a 200 posti |
| **API OpenAI** | No di default | Log antiabuso fino a 30 giorni. Conservazione zero con approvazione. | "Non previsti" | Sì, su richiesta e approvazione, 10% in più | gpt-6.1-sol 2 $ e 10 $; gpt-6-luna 0,10 $ e 0,50 $ |
| **Azure OpenAI** (Microsoft Foundry) | No senza permesso. OpenAI non vede i dati. | Un campione può essere rivisto per abusi. Esenzione su approvazione. | DPA Microsoft non letto | Sì, con deployment "Data Zone" UE | Non letto |
| **Microsoft 365 Copilot** Controlla il tenant | No | Si governa con Purview | DPA Microsoft non letto | Di norma sì. Ma il "flex routing" può elaborare fuori UE nei picchi: è attivo di default sui tenant creati dopo il 25 marzo 2026 e l'amministratore può spegnerlo. Da luglio 2026 anche OpenAI è sub-responsabile. | 30 $ a utente al mese, oltre alla licenza Microsoft 365. Copilot Business 21 $ |
| **Gemini in Google Workspace** | No senza permesso | App Gemini: 18 mesi di default, regolabile a 3 o 36 | Incluse nel contratto | Regione dati solo in alcune edizioni. Perimetro per Gemini non verificato. | Business Standard 13,60 € a utente al mese |
| **Gemini su Vertex AI** | No senza permesso | Conservazione zero solo con più passi: cache spenta, eccezione al monitoraggio, niente Grounding | Incluse | Sì, endpoint multi-regione UE, 10% in più | Gemini 3.8 Flash in UE: 0,825 $ e 4,125 $ |
| **App Gemini con account personale** Non per lavoro | Sì, con "Keep Activity" attiva. Revisori umani. | Chat riviste fino a 3 anni | Google chiede di non inserire informazioni riservate | No | Non rilevato |
| **Mistral Vibe** (prima Le Chat) | Sì di default, con opt-out | Finché l'utente cancella | "None" | Sì di default | Team 24,99 $ a utente al mese |
| **API Mistral** | Default non chiaro per l'API a pagamento: fai l'opt-out | 30 giorni. Conservazione zero su richiesta. | "None" | Sì di default | Small 4: 0,15 $ e 0,60 $. Medium 3.5: 1,50 $ e 7,50 $ |


## Attenzioni

- **Il feedback scavalca il piano.** Su Claude il pollice su o giù fa conservare la conversazione fino a 5 anni e la rende usabile per l'addestramento, anche sui piani commerciali. Si spegne da Organization settings, Data and Privacy, Rate chats.
- **Non tutti i modelli ammettono la conservazione zero.** I modelli Fable e Mythos di Anthropic richiedono 30 giorni di conservazione, anche su Bedrock e Google Cloud. Con dati personali meglio Opus, Sonnet o Haiku.
- **Chi è il responsabile cambia col canale.** Su Amazon Bedrock e Google Cloud il responsabile del trattamento è il cloud. Su Microsoft Foundry, per i modelli Claude, è Anthropic, e c'è solo la zona dati USA.
- **"Regione UE" non vuol dire "dati solo in UE".** Spesso account, assistenza e telemetria escono dalla regione. Va letto fornitore per fornitore.
- **Agenti che vedono lo schermo.** Anthropic sconsiglia con forza Claude in Chrome per informazioni mediche, documenti legali, conti finanziari e siti con dati personali altrui.
- **Usi ad alto rischio nelle policy dei fornitori.** Anthropic chiede la revisione di un professionista qualificato per usi legali, sanitari, assicurativi e finanziari. OpenAI vieta consulenze legali o mediche personalizzate senza un professionista abilitato e decisioni critiche senza revisione umana.


Tra parentesi quadre gli id delle affermazioni nella base: `python3 -B scripts/fonti.py id <id>` ne dà testo, fonte e limiti.

## Account personali: tre cose in più

- **Le credenziali non si condividono.** I termini consumer di Anthropic vietano di condividere i dati di accesso e di rendere l'account disponibile ad altri. Le condizioni d'uso di OpenAI per l'Europa dicono lo stesso [au-26, au-27].
- **Quello che è già servito all'addestramento resta.** Se spegni l'addestramento o cancelli una chat, Anthropic non usa quei dati per addestramenti futuri, ma restano negli addestramenti già avviati e nei modelli già addestrati. OpenAI non promette di rimuovere ciò che ha già usato [au-28, au-29].
- **Prezzi dei piani personali**, solo per confronto: Claude Pro 20 $ al mese, Max 100 o 200 $; ChatGPT Go 8 €, Plus 23 €, Pro da 103 € [au-22, au-23].

## Trascrizione dai fornitori closed

Prezzi e condizioni sono in [open-source.md](open-source.md), sezione "Trascrizione vocale", insieme alle alternative europee.
