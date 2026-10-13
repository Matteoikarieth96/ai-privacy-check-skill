# Costi

Base verificata il 13 ottobre 2026 su fonti aperte quel giorno. Non è un parere legale. Le fonti di ogni affermazione si cercano con `scripts/fonti.py`.


## Tabella di riferimento

Due taglie: uno studio di 4 persone e una struttura di 20. Per le API serve un'ipotesi di consumo, che è nostra e va sostituita con i consumi reali: 20 milioni di token in ingresso e 4 in uscita al mese per lo studio piccolo, 100 e 20 per la struttura media. Prezzi di listino letti il 13 ottobre 2026, tasse escluse.

| Opzione | 4 persone, al mese | 20 persone, al mese | Cosa non è incluso |
|---|---|---|---|
| Claude Team, posto Standard | 100 $ | 500 $ | Non adatto a dati sanitari, politici o giudiziari identificabili |
| ChatGPT Business | 100 $ | 500 $ | Come sopra |
| Mistral Vibe, piano Team | 99,96 $ | 499,80 $ | Opt-out dall'addestramento da fare |
| Google Workspace Business Standard, con Gemini | 54,40 € | 272 € | Include posta e documenti. Impegno annuale |
| Microsoft 365 Copilot | 120 $ | 600 $ | Serve anche la licenza Microsoft 365. Controllo del flex routing |
| API, Claude Sonnet 5.5 in regione UE | 88 $ | 440 $ | L'applicazione va costruita. Contratto con il cloud |
| API, Claude Haiku 5.5 diretta | 4 $ | 20 $ | L'applicazione va costruita. Dati negli USA |
| API, gpt-6.1-sol con residenza UE | 88 $ | 440 $ | Residenza UE su richiesta e approvazione |
| API, Gemini 3.8 Flash in UE | 33 $ | 165 $ | Prezzo introduttivo fino al 31 dicembre 2026 |
| API, Mistral Medium 3.5 | 60 $ | 300 $ | Opt-out dall'addestramento |
| API, modello open in UE (gpt-oss 120b su OVHcloud) | 3,20 € | 16 € | L'applicazione va costruita. Qualità in italiano da provare |
| Mac Studio 128 GB in studio | Circa 163 € | Circa 163 €, ma la capacità per 20 persone va provata | 4.843 € senza IVA divisi su 36 mesi, più energia per 100 W medi. Installazione e manutenzione a parte |
| Server GPU in affitto da 96 GB | 999 € | 999 € | 999 € di attivazione. Gestione del modello a parte |

Come leggere la tabella. Ai volumi di uno studio il consumo delle API costa poco: la spesa vera è costruire e mantenere l'applicazione, e fare i documenti. I piani a posti sono pronti all'uso ma non coprono i dati delicati. L'energia è calcolata a 0,3887 € per kWh, prezzo Eurostat per le piccole utenze non domestiche in Italia nel primo semestre 2026: 100 W sempre accesi costano circa 340 € l'anno.


Tra parentesi quadre gli id delle affermazioni nella base: `python3 -B scripts/fonti.py id <id>` ne dà testo, fonte e limiti.

## Dai volumi ai numeri

`costi.py` vuole milioni di token, pagine o minuti di audio. Nessun fornitore dichiara quanti token occupa una pagina in italiano [au-16, au-17]. Quello che le fonti ufficiali dicono:

- in inglese un token vale circa 4 caratteri, cioè tre quarti di parola; altre lingue possono dare rapporti diversi;
- una pagina PDF di testo occupa di solito da 1.500 a 3.000 token;
- i modelli Claude più recenti producono circa il 30% di token in più per lo stesso testo.

Stime di lavoro, da dichiarare sempre come stime:

| Cosa | Stima | Come usarla |
|---|---|---|
| Una pagina di testo | 2.000 token | `--pagine-in` e `--pagine-out` la applicano da sole; si cambia con `--token-per-pagina` |
| Un documento breve: cedolino, lettera, referto di una pagina | 2.000 token | contalo come una pagina |
| Uno scambio di chat con un documento allegato | il documento, più 500 token di domanda e 500 di risposta | somma a mano e passa i milioni con `--token-in` e `--token-out` |
| Un minuto di audio da trascrivere | si paga al minuto, non a token | `--minuti-audio` |

Prima di promettere un costo a un cliente misura su un campione vero: dieci documenti bastano.

**Volumi e persone.** Il default di 20 milioni di token in ingresso e 4 in uscita vale per uno studio piccolo. Non si scala da solo con il numero di persone: chiedi i volumi.

**Unità e valute.** I listini usano dollari o euro, e prezzi al secondo, al minuto o all'ora, quasi sempre tasse escluse. Lo script li riporta al mese, ma non converte le valute: nel rapporto tieni la valuta del listino.

**Ciò che non è a listino.** Costruire l'applicazione, installare un'interfaccia, scrivere i documenti, il legale. Scrivi "da preventivo" e mettilo tra i contro: per uno studio piccolo è la spesa più grande.
