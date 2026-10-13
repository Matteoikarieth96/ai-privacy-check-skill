# Formato di report.json

Parti da `templates/report.template.json`. Il validatore nomina ogni campo sbagliato.

Da `report.json` lo script costruisce il **rapporto di una pagina**: tre blocchi di azioni (si può, non si può, da fare), la soluzione consigliata e i primi punti aperti. Tutto il resto (ruoli, note, fonti con link, alternative, costi) va nell'allegato `dettaglio.html`. I limiti di lunghezza qui sotto servono a far stare il rapporto su un foglio A4: se il validatore dice che un testo è troppo lungo, accorcialo, non spezzarlo in due righe.

Ogni testo del rapporto è una riga sola di testo semplice, al massimo 2.000 caratteri: niente a capo, tabulazioni, markup (`![`, `](`, tag) o caratteri invisibili. Gli indirizzi cominciano con `http` o `https` e non contengono `@`. Il validatore rifiuta il resto, perché gli stessi testi finiscono in `sintesi.md`, che viene riportata in chat.

## Campi

| Campo | Contenuto |
|---|---|
| `meta.titolo` | Il caso in poche parole, per esempio "IA sui cedolini, Studio Alfa". Niente nomi di persone. Al massimo 80 caratteri. |
| `meta.data` | Data dell'analisi, AAAA-MM-GG. |
| `meta.settore` | `commercialisti`, `sanita`, `avvocati` o `altro`. |
| `meta.base_verificata_il` | Il valore `verificato_il` di `data/affermazioni.json`. |
| `meta.ricontrollo` | `online` se hai fatto il passo 4, altrimenti `nessuno`. |
| `meta.ricontrollo_dettaglio` | Facoltativo. Una frase: quante pagine hai aperto e quali non si sono lette. |
| `caso.descrizione` | Due o tre frasi: chi è, cosa fa, cosa vuole. Al massimo 320 caratteri. |
| `caso.obiettivi` | Elenco, uno per cosa che l'IA deve fare. |
| `caso.strumenti` | Strumenti e account in uso o previsti. Può essere vuoto. |
| `caso.persone` | Quante persone lo useranno. |
| `caso.gia_in_uso` | `true` se lo strumento è già usato sui dati veri. Obbliga ad almeno un'azione `da_fare` con `quando` uguale a `subito`. |
| `segnali` | I nove segnali di [livelli.md](livelli.md), tutti presenti, `true` o `false`. |
| `segnali_da_confermare` | Facoltativo. I segnali accesi senza certezza: l'allegato li marca "da confermare". |
| `attenzione.livello` | `bassa`, `media` o `alta`. Mai sotto il minimo dato dai segnali. |
| `attenzione.motivi` | Da uno a tre motivi concreti, riferiti al caso. Senza punto finale, al massimo 110 caratteri l'uno. |
| `rischi` | Facoltativo. Da usare quando l'utente chiede "cosa rischio": frasi brevi su sanzioni e conseguenze, prese dalla base, ognuna con la sua norma nel testo. Compare nell'allegato e nella sintesi per la chat, non nel rapporto di una pagina. Le fonti vanno in `fonti`. |
| `ruoli` | Una voce per anello della catena: `ruolo`, `chi`, `documento` che serve. Se oggi un documento manca, scrivilo: "Oggi nessun contratto: serve...". |
| `righe` | Le azioni: il cuore del rapporto. Da 6 a 14. Vedi sotto. |
| `setup` | Da due a quattro soluzioni. Una sola con `"consigliato": true`: è quella che compare nel rapporto. |
| `costi.ipotesi` | Persone e volumi usati per il calcolo, detti come ipotesi. |
| `costi.voci` | `voce`, `importo`, `nota`. Gli importi vengono da `scripts/costi.py`. Per un fornitore senza listino pubblico scrivi "Da preventivo" e dillo nella nota. |
| `aperti` | Punti aperti e cose non verificate. Una domanda per punto, al massimo 200 caratteri. I primi tre compaiono nel rapporto: metti in testa i più importanti. |
| `fonti` | Facoltativo. L'allegato costruisce da solo l'elenco delle fonti a partire dalle azioni. Qui metti solo fonti in più, per esempio quelle di rischi, soluzioni e costi. |

## Le azioni

Ogni riga è un'azione di uno di tre tipi. Chi legge il rapporto deve poter dire, in un minuto: questo si può, questo no, questo va fatto.

| `tipo` | Cosa dice | Come si scrive | Quante |
|---|---|---|---|
| `si_puo` | Cosa il caso può fare, e a quale condizione | Verbo all'infinito, si legge dopo "Si può": "Usare...", "Far leggere...". La condizione sta nella stessa riga. | Da 1 a 4 |
| `non_si_puo` | Cosa la norma vieta nel caso, così come è fatto o pensato oggi | Verbo all'infinito, si legge dopo "Non si può": "Caricare...", "Decidere...". | Fino a 4. Almeno 1 se c'è un segnale acceso |
| `da_fare` | Un obbligo da adempiere, con la sua scadenza | Verbo all'imperativo, dice chi fa cosa: "Firma...", "Chiedi...". Usa il "tu"; se il rapporto è per un terzo usa il "voi". | Da 2 a 7 |

```json
{
  "tipo": "si_puo",
  "azione": "Trattare i cedolini con l'IA su un canale in UE senza conservazione, o con i campi sensibili oscurati",
  "nota": "Nei cedolini ci sono malattia, permessi e trattenute sindacali: sono dati su salute e sindacato.",
  "norme": ["GDPR art. 9", "Garante provv. 146/2019"],
  "fonte": {"stato": "base", "data": "2026-10-13", "url": "https://...", "etichetta": "Garante, provv. 146/2019"},
  "altre_fonti": [{"etichetta": "GDPR, art. 9", "url": "https://...", "stato": "base", "data": "2026-10-13"}]
}
```

```json
{
  "tipo": "da_fare",
  "quando": "prima",
  "azione": "Chiedi alle 25 aziende l'autorizzazione scritta, con il fornitore di IA indicato per nome",
  "norme": ["GDPR art. 28(2), 28(4)"],
  "fonte": {"stato": "base", "data": "2026-10-13", "url": "https://...", "etichetta": "GDPR, art. 28"}
}
```

- `azione`: una riga sola, al massimo 110 caratteri, senza punto finale. È l'unico testo dell'azione che compare nel rapporto: deve reggersi da sola.
- `nota`: facoltativa, al massimo 320 caratteri. Il perché o il come, in una o due frasi. Compare solo nell'allegato.
- `norme`: scritte con il nome dell'atto, come nella base: "GDPR art. 28(3)", "L. 132/2025 art. 13", "Codice penale art. 615-ter", "AI Act art. 50". Per termini e pagine dei fornitori: "Anthropic Consumer Terms sez. 11", "Privacy Center Anthropic". Almeno una, di solito non più di tre.
- `quando`: solo per `da_fare`. `subito` (lo strumento è già in uso: cosa fermare o sistemare adesso), `prima` (prima di toccare un dato vero, o prima di caricarne altri), `entro_30_giorni`, `dopo`. Il rapporto ordina e numera le azioni per urgenza.
- `fonte`: la fonte principale, quella che regge il cuore dell'azione, con lo stato deciso nel passo 4. `etichetta` dice quale norma o documento è. Con `ricontrollata` e `base` servono indirizzo e data. Con `non_verificata` lascia fuori indirizzo e data: il rapporto marca l'azione "da verificare".
- `altre_fonti`: facoltativo, per le altre norme dell'azione.

### Scegliere e scrivere le azioni

- **Un'azione, una norma che la regge.** Ogni azione dice cosa una norma permette, vieta o richiede in questo caso. Un consiglio di buon senso senza una norma da citare non è un'azione: al più è una `nota`.
- **"Si può" porta sempre la sua condizione.** "Usare un fornitore americano, se il contratto ha le clausole tipo" è un'azione. "Usare un fornitore americano" no. "Si può" non vuol dire "è a posto": il validatore rifiuta le promesse di conformità.
- **"Non si può" solo quando la norma lo dice.** Se le fonti lasciano il dubbio, non è un "non si può": va tra i punti aperti, con al più un'azione `da_fare` prudente ("Fai valutare a un legale se..."). Tre casi tipici di dubbio: se un fatto sia una violazione da notificare; il "None" alla voce categorie particolari nel contratto di un fornitore (non si sa se è un divieto: la soluzione va segnata `"regge": false` e il dubbio tra i punti aperti); una regola di categoria che la base riporta come prassi e non come norma.
- **"Si può" su una norma incerta si dichiara.** Se la condizione che rende lecita l'azione poggia su un punto aperto, scrivilo nella `nota` e metti quel punto tra i primi tre punti aperti.
- **Parti da ciò che l'utente vuole fare.** Ogni obiettivo del caso trova la sua risposta in un "si può" (come farlo) o in un "non si può" (perché no, e allora cosa). Chi ha chiesto "posso?" deve trovare la risposta.
- **Divieto e rimedio non si ripetono.** Se un "non si può" e un "da fare" dicono la stessa cosa, tieni il "da fare" e usa il "non si può" per un altro divieto. Possono stare insieme quando il "da fare" aggiunge il come: "non si può caricare dati di clienti su un account personale" e "smetti di caricarli ed elenca cosa è stato caricato" sono due informazioni diverse.
- **Se gli obblighi sono più di sette**, tieni come azioni quelli che bloccano gli altri e sposta il resto nella `nota` dell'azione più vicina. Non fondere due obblighi in una riga sola.
- **Le tabelle dei file di riferimento sono in forma problema e soluzione.** Trasformale: il problema diventa di solito un "non si può" o la `nota`, la soluzione un "da fare" o la condizione di un "si può". Non copiare le righe: riscrivile sul caso.
- **La copertura delle norme vale su tutte le azioni insieme**, di qualunque tipo: con il segnale `dati_particolari` acceso, per esempio, almeno un'azione cita GDPR art. 9 e almeno una GDPR art. 35.

Gli indirizzi non si scrivono a memoria. Per le fonti dalla base:

```bash
python3 -B "$SKILL_DIR/scripts/fonti.py" json eu-08 prof-18
```

stampa i blocchi `fonte` pronti, con un'etichetta leggibile. Il validatore rifiuta un indirizzo con stato `base` che non sia nella base, una data che non corrisponda allo stato, e un'azione `non_verificata` che non abbia il suo punto aperto.

## Le soluzioni

```json
{
  "nome": "Modello in regione UE via API",
  "per_cosa": "Il flusso sui cedolini, che contiene dati sensibili.",
  "pro": ["Dati elaborati in UE", "Nessuna conservazione dei contenuti"],
  "contro": ["Va costruita una piccola applicazione"],
  "costo": "Circa 88 $ al mese a listino, con l'ipotesi di consumo dichiarata",
  "consigliato": true,
  "condizione": "il fornitore conferma per iscritto che il contratto copre i dati sanitari"
}
```

- Spesso la risposta giusta è una combinazione: un piano a posti per il lavoro senza dati delicati e un canale separato per il resto. Scrivila come un'unica soluzione consigliata.
- La soluzione consigliata compare nel rapporto di una pagina, quindi ha dei limiti: `nome` 90 caratteri, `per_cosa` 220, `costo` 110, `condizione` 150. Pro e contro vanno nell'allegato.
- `condizione`: facoltativo. Usalo quando la soluzione consigliata regge solo se si verifica qualcosa.
- `"regge": false`: per la soluzione che l'utente si aspetta ma che non basta per i dati del caso, per esempio "passare al piano a pagamento". Il rapporto la nomina come "Non basta per questi dati" e nell'allegato il `per_cosa` spiega perché. Non può essere quella consigliata.
- Le soluzioni che reggono per i dati delicati chiedono quasi sempre di costruire o installare qualcosa: dillo nei contro e, se lo sai, nel costo.

## Scrivere bene

- Frasi brevi. Un'azione, una cosa sola.
- Niente "conforme", "a posto", "rischio zero", "anonimo": di' cosa dice la norma e cosa resta.
- Ogni cifra viene dallo script dei costi o da una fonte, con la data.
- I punti aperti non sono una formalità: sono la parte che protegge chi legge.
- I casi di esempio nei file di settore servono a capire tono e contenuto. Non copiarne le righe: riscrivi sul caso.
