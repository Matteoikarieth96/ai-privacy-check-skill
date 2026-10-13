# Modelli open source

Base verificata il 13 ottobre 2026 su fonti aperte quel giorno. Non è un parere legale. Le fonti di ogni affermazione si cercano con `scripts/fonti.py`.


## Modelli e licenze

| Modello | Licenza | Va bene per uno studio italiano? | Memoria a 4 bit |
|---|---|---|---|
| **Llama 4** (Meta) | Llama 4 Community | No La policy nega la licenza a chi ha sede nell'UE per i modelli multimodali, e i modelli della famiglia lo sono. | Non rilevante |
| **Llama 3.3 70B** (Meta) | Llama 3.3 Community: uso commerciale con condizioni | Sì Italiano tra le lingue supportate. Solo testo. | File da 43 GB |
| **Mistral Small 4** | Apache 2.0 | Solo via API Italiano supportato, ma con 119 miliardi di parametri non è da PC di studio. | Non dichiarata |
| **Mistral Medium 3.5** | "Modified MIT": serve una licenza commerciale sopra 20 milioni di dollari di ricavi mensili | Sì Per uno studio la soglia non è un ostacolo. Non è open source in senso stretto. | Non dichiarata |
| **Qwen 3.8 27B, Qwen 3.6 35B** (Alibaba) | Apache 2.0 | Da provare Le schede non dichiarano l'italiano. | Circa 17 GB per la taglia 27B |
| **Gemma 4** (Google): 12B, 26B, 31B | Apache 2.0 | Da provare Oltre 35 lingue, elenco non pubblicato. | 6,7 GB, 14,4 GB, 17,5 GB, solo pesi |
| **gpt-oss 20b e 120b** (OpenAI) | Apache 2.0 | Da provare Italiano non dichiarato. | 16 GB per il 20b. Il 120b sta in una GPU da 80 GB (file da 65 GB) |
| **DeepSeek V4.1 Flash** | MIT | Solo via API 552 miliardi di parametri. | Non rilevante |
| **Phi-4** (Microsoft) | MIT | Sconsigliato Centrato sull'inglese, rende peggio nelle altre lingue. | Non rilevata |


## Dove farli girare

| Setup | Listino | Cosa ci gira | Fornitore nella catena | Attenzioni |
|---|---|---|---|---|
| **Mac mini** M5 Pro, 64 GB | 3.129 € IVA inclusa, circa 2.565 € senza | Modelli da 27 a 31 miliardi di parametri. Il 70B è al limite. | Nessuno | Consumo massimo dichiarato 155 W |
| **Mac Studio** M5 Max, 128 GB | 5.909 € IVA inclusa, circa 4.843 € senza | Fino a gpt-oss 120b | Nessuno | Consumo massimo dichiarato 480 W |
| **Mac Studio** M5 Ultra, 256 GB | 11.099 € IVA inclusa | Modelli più grandi o più utenti insieme | Nessuno | La versione da 512 GB non ha ancora un prezzo |
| **Workstation con RTX 5090**, 32 GB | 2.099 € la sola scheda, prezzo consigliato. Il resto della macchina non è a listino. | Modelli da 27 a 31 miliardi di parametri | Nessuno | 575 W la sola scheda, alimentatore da almeno 1.000 W. Più manutenzione di un Mac. |
| **Workstation con RTX PRO 6000**, 96 GB | Nessun listino ufficiale. Un comparatore tedesco indica tra 8.550 e 16.719 € negli ultimi 12 mesi. | Fino a gpt-oss 120b | Nessuno | Prezzo molto instabile |
| **Server GPU in affitto**, Hetzner | GEX45 (GPU da 24 GB) 214 € al mese più 209 € di attivazione. GEX63 (GPU da 96 GB) 999 € al mese più 999 €. IVA esclusa. | Dal 27B al 120b secondo il modello | Hetzner, Germania | Il contratto sul trattamento dei dati non è automatico: va attivato dall'account prima di caricare dati di clienti |
| **Server GPU in affitto**, Scaleway e OVHcloud | Scaleway a Parigi: 24 GB a 0,79 € l'ora (circa 575 € al mese), 48 GB a 1,47 € l'ora (circa 1.073 € al mese). OVHcloud: 24 GB da 0,75 € l'ora, 48 GB da 1,40 € l'ora. | Dal 27B al 70B | Scaleway, Francia, gruppo iliad. OVHcloud, Francia; in Italia OVH Srl. | Testi dei contratti sui dati non letti |
| **API di modelli open in UE** | gpt-oss 120b per milione di token, ingresso e uscita: OVHcloud 0,08 e 0,40 €; Scaleway 0,15 e 0,60 €; IONOS 0,15 e 0,65 €; Regolo.ai 1,00 e 4,20 €. Llama 3.3 70B: IONOS 0,65 e 0,65 €; OVHcloud 0,67 e 0,67 €; Scaleway 0,90 e 0,90 €. | Quello che offre il catalogo | Torna un fornitore, quindi serve il contratto | Scaleway: nessuna conservazione di default, fino a due settimane in caso di abuso. OVHcloud: "zero retention" dichiarata. IONOS: prompt non registrati, datacenter in Germania, nessun sub-responsabile. Regolo.ai: contratto non verificato. |


## Attenzioni

- **Il modello locale toglie i trasferimenti, non il resto.** Sicurezza, valutazione d'impatto, informazione a clienti e pazienti restano dovute. Senza fornitore esterno, accessi alla macchina, cifratura del disco, backup e log sono tutti a carico dello studio.
- **Attenzione alla rete.** Ollama ascolta di default solo sulla macchina locale e non ha autenticazione integrata. Se lo apri alla rete dello studio servono firewall o un proxy con autenticazione.
- **Spegni le funzioni cloud.** In Ollama con OLLAMA_NO_CLOUD=1. vLLM raccoglie statistiche d'uso anonime di default: si spengono con VLLM_NO_USAGE_STATS=1. LM Studio è gratuito anche per lavoro ma non è open source.
- **Open source non vuol dire senza regole.** L'AI Act esclude i sistemi con licenza libera, ma non se sono ad alto rischio o rientrano negli artt. 5 e 50. Gli obblighi di chi usa il sistema restano.
- **Nessun obbligo di server in Italia per i privati.** La legge 132/2025 prevede solo una preferenza negli acquisti della pubblica amministrazione.
- **I prezzi non sono confrontabili così come sono.** Apple include l'IVA, i provider europei no, Nvidia non lo precisa. Riportali al netto prima di confrontare.


Tra parentesi quadre gli id delle affermazioni nella base: `python3 -B scripts/fonti.py id <id>` ne dà testo, fonte e limiti.

## Trascrizione vocale

Per trascrivere riunioni o visite servono modelli diversi da quelli di testo.

| Modello | Licenza | Italiano | Memoria indicata |
|---|---|---|---|
| **Whisper** (OpenAI), large e turbo | MIT per codice e pesi | Sì | Circa 10 GB per large, circa 6 GB per turbo; con whisper.cpp circa 3,9 GB per large [au-01, au-04] |
| **Voxtral Realtime** (Mistral) | Apache 2.0 | Sì, tra 13 lingue | GPU da almeno 16 GB [au-02] |
| **Voxtral Mini 3B e Small 24B** (Mistral, 2025) | Apache 2.0 | Sì, tra 8 lingue | Circa 9,5 GB e circa 55 GB [au-02] |
| **Parakeet TDT 0.6B v3 e Canary 1B v2** (NVIDIA) | CC-BY-4.0, uso commerciale ammesso con attribuzione | Sì, tra 25 lingue europee | Almeno 2 GB e almeno 6 GB di RAM [au-03] |

Per eseguirli in locale: whisper.cpp, faster-whisper e mlx-whisper hanno licenza MIT. Gli ultimi due scaricano il modello da internet al primo uso, salvo indicare una cartella locale [au-04]. MacWhisper è un'app commerciale per Mac che trascrive in locale, ma offre anche servizi cloud facoltativi che portano i dati fuori: vanno lasciati spenti [au-05].

**Attenzione.** La scheda ufficiale di Whisper avverte che il modello può scrivere testo mai pronunciato e ne sconsiglia l'uso in contesti ad alto rischio. Chi trascrive deve rileggere.

Trascrizione a consumo, prezzo per minuto di audio (i listini usano unità diverse: qui sono convertiti):

| Servizio | Prezzo | Dati |
|---|---|---|
| Whisper large-v3 su OVHcloud | circa 0,0025 € al minuto | In UE, nessuna conservazione dichiarata salvo la fatturazione [au-14] |
| Whisper large-v3 su Scaleway | 0,003 € al minuto | Parigi, nessuna conservazione di default, niente addestramento [au-13] |
| faster-whisper su Regolo.ai | 0,009 € al minuto | Fornitore italiano, conservazione zero dichiarata, contratto non verificato [au-15] |
| Voxtral Mini Transcribe 2 via Mistral | 0,003 $ al minuto | In UE di default; l'esclusione dall'addestramento va attivata [au-10] |
| gpt-4o-transcribe via OpenAI | 0,006 $ al minuto | Residenza UE e conservazione zero solo su approvazione [au-06, au-07] |
| Azure Speech, regione UE | 0,88 € l'ora, circa 0,015 € al minuto | Elaborazione nella regione scelta; contratto Microsoft non letto [au-08] |
| Google Speech-to-Text V2 | 0,016 $ al minuto | Multi-regione UE; prezzo da ricontrollare [au-09] |
| ElevenLabs Scribe v2 | 0,22 $ l'ora | Residenza UE solo per i clienti Enterprise [au-11] |

## Un'interfaccia di chat per un modello via API o locale

Le soluzioni che reggono per i dati delicati chiedono quasi sempre un'interfaccia da installare. È il lavoro vero, più del consumo.

| Strumento | Licenza | Più utenti con account separati | Da spegnere |
|---|---|---|---|
| **Open WebUI** | Licenza propria: uso commerciale ammesso, ma vieta di togliere il marchio oltre 50 utenti senza permesso | Sì, con ruoli e gruppi | Controllo degli aggiornamenti; `OFFLINE_MODE` lo azzera [au-18, au-19] |
| **LibreChat** | MIT | Sì | Nulla dichiarato nelle pagine lette [au-20] |
| **AnythingLLM** | MIT | Sì, nella versione Docker | Telemetria anonima, con `DISABLE_TELEMETRY=true` [au-20] |
| **Jan** | Apache 2.0 | No: è un'app per una persona | Analitiche solo se l'utente acconsente [au-21] |
| **LM Studio** | Proprietaria, gratuita anche per lavoro | No: è un'app per una persona | Contatta i server per aggiornamenti e ricerca dei modelli [au-21] |

Installazione, manutenzione e assistenza non hanno un listino: nel rapporto scrivi "da preventivo" e dillo tra i contro.
