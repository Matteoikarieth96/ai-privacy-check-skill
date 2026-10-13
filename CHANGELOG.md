# Versioni

## 0.3 (13 ottobre 2026)

L'uscita diventa un rapporto di una pagina.

- Le righe del rapporto sono azioni di tre tipi: `si_puo`, `non_si_puo`, `da_fare`. Ognuna è una riga sola con la sua norma. `problema` e `cosa_fare` non esistono più; il perché va nella `nota`.
- `ai-privacy-check.html` è il rapporto di una pagina: si può, non si può, da fare in ordine di urgenza, soluzione consigliata, primi tre punti aperti. Si stampa su un foglio A4.
- `dettaglio.html` è il nuovo allegato: ruoli, nota e fonte di ogni azione, alternative, costi, tutti i punti aperti, fonti con link.
- Il validatore impone i limiti che tengono il rapporto in una pagina: azioni per tipo, lunghezza di azione, titolo, descrizione, motivi, punti aperti e soluzione consigliata.
- Regola nuova: ogni azione dice cosa una norma permette, vieta o richiede. Niente consigli di opportunità senza una norma.
- `sintesi.md` riporta le stesse voci del rapporto. `pagina.txt` ora contiene anche note, fonti con indirizzo, pro e contro.
- `passi` diventa facoltativo: l'ordine lo danno le azioni da fare.
- `fonti.py json` dà etichette leggibili, con atto e articolo.
- `sintesi.md` riporta anche cosa si rischia e la soluzione che non basta.
- Revisione di sicurezza prima del primo commit. Corretti: validatore lento su testi costruiti apposta (limiti di lunghezza prima delle espressioni regolari), testo non neutralizzato in `sintesi.md` (ogni campo è una riga di testo semplice), tipi sbagliati che davano una traccia, `"consigliato": 1` accettato, indirizzi con utente, scrittura dei file (atomica, permessi 0600, collegamenti fisici non seguiti), numeri non validi in `costi.py`, `.gitignore` più largo.
- Base: 334 affermazioni in otto domini; note riscritte in forma neutra.

## 0.2 (13 ottobre 2026)

Nata dalla prova della 0.1 su tre casi.

- Validatore più severo: copertura delle norme con il nome dell'atto, indirizzi che devono venire dalla base, date coerenti con lo stato delle fonti, da 6 a 14 righe, da 2 a 4 soluzioni, un punto aperto per ogni riga non verificata, rifiuto delle affermazioni di conformità.
- Caso "lo stiamo già facendo": domanda iniziale, gruppo "Da fare subito", sezione con l'ordine dei rimedi.
- Nono segnale: l'IA parla direttamente con le persone.
- I segnali non si accendono più nel dubbio: si chiede, o si marcano "da confermare".
- Fonti: ricerca per atto e articolo, più parole, elenco per dominio, blocchi pronti per il rapporto. La pagina costruisce da sola l'elenco delle fonti. Una riga può avere una fonte principale e altre fonti.
- Costi: trascrizione al minuto, Llama 3.3 e altre voci, prezzo letto oggi, conversione da pagine, filtro per i dati delicati.
- Pagina: sezione "Cosa si rischia", soluzioni "Non basta per questi dati", soluzione consigliata "a condizione che", versione in testo semplice, sintesi con le azioni.
- Base: 64 nuove affermazioni verificate su trascrizione vocale, interfacce di chat, consulenti del lavoro, strumenti già in uso, dati nei cedolini, fascicoli penali.
- Riquadro per i consulenti del lavoro: le regole deontologiche dei commercialisti non valgono per loro.

## 0.1 (13 ottobre 2026)

Prima bozza: sette passi, otto segnali, una prima base di affermazioni verificate, validatore, pagina HTML.
