# Sicurezza

## Modello di minaccia

La skill tratta due tipi di input non fidato e un tipo di input sensibile.

| Input | Rischio |
|---|---|
| La descrizione del caso scritta dall'utente | Finisce nel rapporto e nella pagina: iniezione di markup, percorsi di file |
| Pagine di norme, siti dei fornitori e risultati di ricerca letti nel ricontrollo | Testo che dà istruzioni all'agente, indirizzi ostili (`javascript:`), valori con markup |
| Dati personali veri o nomi di clienti incollati per errore | Finiscono in un file, in una pagina condivisa o in un repository |

Cosa si protegge: chi apre la pagina (nessuno script eseguito), le persone i cui dati potrebbero essere incollati, la riservatezza del caso, il file system locale, e chi legge il rapporto da conclusioni più rassicuranti di quanto le fonti permettano.

## Misure

| Misura | Dove |
|---|---|
| Il contenuto letto online è un dato: le istruzioni che contiene si citano all'utente e non si seguono | `SKILL.md`, regola 1 |
| La skill chiede di descrivere il caso senza incollare dati veri, e si ferma se li riceve | `SKILL.md`, regola 4; `references/intake.md` |
| Ogni testo viene sottoposto a escape prima di entrare nel rapporto e nell'allegato | `scripts/apc_lib.py` (`e`, `costruisci_html`, `costruisci_dettaglio`) |
| `sintesi.md` e `pagina.txt` non hanno escape: per questo il validatore ammette solo testo semplice su una riga, senza a capo, markup Markdown o HTML, caratteri di controllo o invisibili | `scripts/apc_lib.py` (`controlli_preliminari`) |
| Solo indirizzi `http` e `https`, senza utente nell'indirizzo, diventano link, e solo per fonti lette o prese dalla base; il validatore rifiuta gli altri | `scripts/apc_lib.py` (`url_ok`, `link`, `valida`) |
| Le pagine non hanno script né risorse esterne e dichiarano una Content-Security-Policy restrittiva | `scripts/apc_lib.py` (`CSP`) |
| Ogni campo ha una lunghezza massima, controllata prima di qualunque espressione regolare; un rapporto malformato dà un errore, non una traccia | `scripts/apc_lib.py` (`controlli_preliminari`, `valida`) |
| I file di uscita sono costruiti in memoria, poi scritti con permessi 0600 su un file nuovo che prende il posto della destinazione: un collegamento simbolico o fisico al posto del file non viene seguito. La cartella di uscita, se è un collegamento simbolico, viene rifiutata; se è nuova nasce con permessi 0700 | `scripts/build_report.py`, `scripts/apc_lib.py` (`scrivi_sicuro`) |
| Il validatore impone il livello minimo di attenzione, la copertura delle norme e rifiuta frasi come "rischio zero" o "dati anonimi" | `scripts/apc_lib.py` (`valida`) |
| Ciò che non è stato verificato resta scritto come non verificato | `SKILL.md`, regola 3; `references/ricontrollo.md` |
| Rapporti e pagine sono esclusi dal repository, con qualunque nome di cartella; si traccia solo l'esempio inventato. La skill lavora in una cartella privata fuori da ogni repository | `.gitignore`, `SKILL.md` passo 2 |
| Nelle ricerche online non entrano nomi di clienti o dettagli del caso | `references/ricontrollo.md` |
| Gli script non fanno richieste di rete | `scripts/` |
| I test controllano escape, link, CSP, collegamenti simbolici e l'assenza di percorsi locali e indirizzi email nei dati | `tests/` |

## Limiti noti

- Il validatore controlla la forma e alcune regole minime. Non può sapere se un'azione è giusta per il caso, né se un "si può" o un "non si può" è fondato: quello resta al modello e a chi rilegge.
- La base di conoscenza ha una data e può essere superata. Il ricontrollo è mirato, non completo.
- `--no-csp` toglie la Content-Security-Policy dalla pagina. Va usato solo per pubblicarla dentro un visualizzatore che ne imposta una propria.
- Il controllo sulle frasi che promettono troppo è una rete a maglie larghe: una frase riformulata o messa tra virgolette passa. Resta la rilettura.
- Gli script non controllano le cartelle sopra quella di uscita: se un tratto del percorso è un collegamento simbolico creato da altri, i file finiscono dove punta. Usa la cartella privata indicata dalla skill.
- Il testo visibile di un link è l'etichetta della fonte, non l'indirizzo: prima di fidarti di una fonte letta online guarda dove porta.
- Una revisione di sicurezza indipendente è stata fatta il 13 ottobre 2026 sulla versione 0.3; i punti trovati sono corretti o elencati qui.

## Segnalare un problema

Usa la segnalazione privata delle vulnerabilità di GitHub su questo repository. Non aprire una issue pubblica per un problema di sicurezza.
