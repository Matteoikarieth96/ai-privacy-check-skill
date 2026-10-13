"""Funzioni condivise di ai-privacy-check: regole, validazione e costruzione del rapporto.

Solo libreria standard, Python 3.9+.
"""
import datetime
import html
import json
import os
import re
import tempfile
import unicodedata

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(SKILL_DIR, "data")

SETTORI = ("commercialisti", "sanita", "avvocati", "altro")
LIVELLI = ("bassa", "media", "alta")
QUANDO = ("subito", "prima", "entro_30_giorni", "dopo")
# Ogni riga del rapporto è un'azione di uno di questi tre tipi.
TIPI = ("si_puo", "non_si_puo", "da_fare")
ETICHETTE_TIPO = {"si_puo": "Si può", "non_si_puo": "Non si può", "da_fare": "Da fare"}
# Il rapporto deve stare in una pagina: questi limiti servono a questo.
TIPO_MAX = {"si_puo": 4, "non_si_puo": 4, "da_fare": 7}
DA_FARE_MIN = 2
AZIONE_MAX = 110
NOTA_MAX = 320
TITOLO_MAX = 80
DESCRIZIONE_MAX = 320
MOTIVO_MAX = 110
APERTO_MAX = 200
APERTI_IN_PAGINA = 3
# Limiti della soluzione consigliata, l'unica che compare nel rapporto di una pagina.
SCELTA_MAX = {"nome": 90, "per_cosa": 220, "costo": 110, "condizione": 150}
STATI_RIGA = ("ricontrollata", "base", "non_verificata")
STATI_FONTE = ("ricontrollata", "base")
SEGNALI = (
    "dati_personali",
    "dati_particolari",
    "dati_giudiziari",
    "lavoratori",
    "minori",
    "decisioni_su_persone",
    "portali_di_terzi",
    "fuori_ue",
    "dialoga_con_persone",
)
# Segnali che portano da soli il livello di attenzione ad "alta".
SEGNALI_ALTA = ("dati_particolari", "dati_giudiziari", "lavoratori", "minori", "decisioni_su_persone", "portali_di_terzi")
SEGNALI_MEDIA = ("dati_personali", "fuori_ue", "dialoga_con_persone")

RIGHE_MIN, RIGHE_MAX = 6, 14
SETUP_MIN, SETUP_MAX = 2, 4
MOTIVI_MAX = 3


def _atto_art(atto, numero):
    """Norma di un atto preciso, con il numero dell'articolo isolato.

    "GDPR art. 9(2)(h)" vale per l'art. 9; "c.p.c. art. 96" e "GDPR art. 28(9)" no.
    """
    return re.compile(re.escape(atto) + r"[^;|]{0,40}?art\.[^;|]{0,60}?(?<![\d(.])(?<!c\. )(?<!comma )(?:" + numero + r")(?!\d)")


def _testo(frammento):
    return re.compile(re.escape(frammento))


# Per ogni segnale acceso, per ogni gruppo almeno una riga deve citare una delle norme indicate.
COPERTURA = {
    "dati_personali": [[("GDPR art. 28", _atto_art("GDPR", "28"))]],
    "dati_particolari": [[("GDPR art. 9", _atto_art("GDPR", "9"))], [("GDPR art. 35", _atto_art("GDPR", "35"))]],
    "dati_giudiziari": [[("GDPR art. 10", _atto_art("GDPR", "10"))]],
    "lavoratori": [[("D.Lgs. 152/1997", _testo("152/1997")), ("L. 300/1970", _testo("300/1970"))]],
    "minori": [[("Codice Privacy art. 2-quinquies", _testo("2-quinquies")), ("L. 132/2025 art. 4", _atto_art("L. 132/2025", "4")),
                ("WP248", _testo("WP248")), ("Garante provv. 467/2018", _testo("467/2018"))]],
    "decisioni_su_persone": [[("GDPR art. 22", _atto_art("GDPR", "22"))]],
    "portali_di_terzi": [[("Codice penale art. 615-ter", _testo("615-ter"))]],
    "fuori_ue": [[("GDPR art. 44 e seguenti", _atto_art("GDPR", "4[4-9]"))]],
    "dialoga_con_persone": [[("AI Act art. 50", _atto_art("AI Act", "50"))]],
}
COPERTURA_SETTORE = {
    "commercialisti": ("L. 132/2025 art. 13", _atto_art("L. 132/2025", "13")),
    "avvocati": ("L. 132/2025 art. 13", _atto_art("L. 132/2025", "13")),
    "sanita": ("L. 132/2025 art. 7", _atto_art("L. 132/2025", "7")),
}

# Frasi che il rapporto non deve mai affermare. Sono ammesse solo tra virgolette,
# cioe' quando il testo le cita per dire di non usarle.
FRASI_VIETATE = (
    "rischio zero",
    "pienamente conforme",
    "100% conforme",
    "gdpr compliant",
    "dati anonimi",
    "è anonimo",
    "sono anonimi",
    "completamente anonim",
    "totalmente anonim",
)
# Affermazioni di conformita': "lo studio è conforme", "siete a posto", "risulta a norma".
AFFERMAZIONE_VIETATA = re.compile(
    r"(?<!non )\b(?:è|e'|sono|siete|sei|siamo|risulta|risultano|sarete|sarà)\s+"
    r"(?:(?:pienamente|del tutto|già|ora|quindi|così)\s+)?(conform[ei]|a norma|in regola|a posto)\b"
)
SOGLIA_BASE_VECCHIA = 90  # giorni
# Limiti generali: nessun testo del rapporto ha bisogno di più, e senza limiti
# un testo costruito apposta può tenere occupato il validatore per minuti.
STRINGA_MAX = 2000
NORMA_MAX = 200
URL_MAX = 600
URL_RE = re.compile(r"https?://[^\s<>\"'\\@]+")
DATA_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
# Segni che in sintesi.md diventerebbero immagini, link o markup.
MARKUP_RE = re.compile(r"!\[|\]\(|<[A-Za-z/!?]")

ETICHETTE_SETTORE = {
    "commercialisti": "Commercialisti e consulenti del lavoro",
    "sanita": "Medici e strutture sanitarie",
    "avvocati": "Avvocati e studi legali",
    "altro": "Altro settore",
}
ETICHETTE_SEGNALI = {
    "dati_personali": "Dati personali",
    "dati_particolari": "Dati su salute, opinioni politiche, sindacato o altre categorie particolari",
    "dati_giudiziari": "Dati su condanne e reati",
    "lavoratori": "Dati o decisioni che riguardano lavoratori",
    "minori": "Minori",
    "decisioni_su_persone": "Decisioni che pesano su una persona",
    "portali_di_terzi": "Accesso automatico a portali di terzi",
    "fuori_ue": "Dati che escono dall'UE",
    "dialoga_con_persone": "L'IA parla direttamente con le persone",
}


def parse_date(value):
    if not isinstance(value, str) or not DATA_RE.fullmatch(value):
        return None
    try:
        return datetime.date.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def data_it(value):
    d = parse_date(value)
    mesi = "gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre dicembre".split()
    return "%d %s %d" % (d.day, mesi[d.month - 1], d.year) if d else str(value or "")


def url_ok(value):
    """Solo http e https, senza utente nell'indirizzo, senza barre rovesciate, senza spazi."""
    return isinstance(value, str) and len(value) <= URL_MAX and URL_RE.fullmatch(value) is not None


def chiave_sicura(key):
    """Le chiavi del JSON finiscono nei messaggi di errore: niente caratteri di controllo a schermo."""
    return re.sub(r"[^\w-]", "?", str(key))[:40]


def tutte_le_stringhe(node, path="report"):
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from tutte_le_stringhe(v, "%s.%s" % (path, chiave_sicura(k)))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from tutte_le_stringhe(v, "%s[%d]" % (path, i))


def senza_citazioni(text):
    """Toglie le parti tra virgolette, dove una frase vietata puo' essere citata."""
    return re.sub(r"\"[^\"]{0,400}\"|“[^”]{0,400}”|«[^»]{0,400}»", " ", text)


def normalizza(text):
    """Forma su cui cercare le frasi vietate: niente spazi doppi né varianti tipografiche."""
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text))


def carattere_invisibile(text):
    """Il primo carattere di controllo, di formato o surrogato trovato, oppure None.

    Sono vietati anche a capo e tabulazioni: ogni campo del rapporto è una riga sola.
    """
    for ch in text:
        if unicodedata.category(ch) in ("Cc", "Cf", "Cs"):
            return ch
    return None


def controlli_preliminari(report):
    """Controlli fatti prima di ogni espressione regolare: lunghezze e caratteri."""
    errori = []
    for path, text in tutte_le_stringhe(report):
        if len(text) > STRINGA_MAX:
            errori.append("%s: %d caratteri, il massimo per qualunque campo è %d" % (path, len(text), STRINGA_MAX))
            continue
        ch = carattere_invisibile(text)
        if ch is not None:
            errori.append("%s: contiene un carattere di controllo o invisibile (U+%04X). Ogni campo è una riga sola di testo semplice" % (path, ord(ch)))
        elif MARKUP_RE.search(text):
            errori.append("%s: contiene segni di markup (\"![\", \"](\" o un tag). Scrivi testo semplice" % path)
    return errori


def livello_minimo(segnali):
    if any(segnali.get(k) for k in SEGNALI_ALTA):
        return "alta"
    if any(segnali.get(k) for k in SEGNALI_MEDIA):
        return "media"
    return "bassa"


_URLS_BASE = None


def urls_della_base():
    """Indirizzi presenti nella base inclusa (affermazioni e listini)."""
    global _URLS_BASE
    if _URLS_BASE is None:
        urls = set()
        try:
            base = carica_json(os.path.join(DATA_DIR, "affermazioni.json"))
            for d in base.get("domini", []):
                for a in d.get("affermazioni", []):
                    urls.add(a.get("url"))
            listini = carica_json(os.path.join(DATA_DIR, "listini.json"))
            urls.add(listini.get("energia_fonte"))
            for v in listini.get("voci", []):
                urls.add(v.get("fonte"))
        except (OSError, ValueError):
            pass
        urls.discard(None)
        _URLS_BASE = urls
    return _URLS_BASE


def fonti_di_riga(riga):
    """La fonte principale di una riga e le eventuali altre."""
    fonte = riga.get("fonte") if isinstance(riga.get("fonte"), dict) else {}
    altre = [f for f in (riga.get("altre_fonti") or []) if isinstance(f, dict)]
    return fonte, altre


def valida(report, urls_base=None):
    """Restituisce (errori, avvisi). Ogni messaggio nomina il campo da correggere."""
    if not isinstance(report, dict):
        return ["report: deve essere un oggetto JSON"], []
    try:
        errori = controlli_preliminari(report)
        if errori:
            return errori, []
        return _valida(report, urls_base)
    except RecursionError:
        return ["report: struttura troppo annidata"], []
    except Exception as exc:  # un rapporto malformato non deve mai far uscire una traccia
        return ["report: struttura non valida (%s). Riparti dal modello in templates/" % type(exc).__name__], []


def elenco_di_testi(value):
    return isinstance(value, list) and all(isinstance(x, str) and x for x in value)


def _valida(report, urls_base=None):
    errori, avvisi = [], []
    if urls_base is None:
        urls_base = urls_della_base()

    def campo(obj, key, where, tipo=str, vuoto_ok=False):
        v = obj.get(key) if isinstance(obj, dict) else None
        if not isinstance(v, tipo) or (not vuoto_ok and tipo in (str, list) and not v):
            errori.append("%s.%s: manca o è vuoto" % (where, key))
            return None
        return v

    meta = report.get("meta") if isinstance(report.get("meta"), dict) else {}
    titolo = campo(meta, "titolo", "meta")
    if titolo and len(titolo) > TITOLO_MAX:
        errori.append("meta.titolo: %d caratteri, il massimo è %d" % (len(titolo), TITOLO_MAX))
    for k in ("data", "base_verificata_il"):
        if parse_date(meta.get(k)) is None:
            errori.append("meta.%s: serve una data nel formato AAAA-MM-GG" % k)
    if not isinstance(meta.get("settore"), str) or meta.get("settore") not in SETTORI:
        errori.append("meta.settore: usa uno tra %s" % ", ".join(SETTORI))
    if meta.get("ricontrollo") not in ("online", "nessuno"):
        errori.append("meta.ricontrollo: usa \"online\" o \"nessuno\"")

    caso = report.get("caso") if isinstance(report.get("caso"), dict) else {}
    descrizione = campo(caso, "descrizione", "caso")
    if descrizione and len(descrizione) > DESCRIZIONE_MAX:
        errori.append("caso.descrizione: %d caratteri, il massimo è %d. Due o tre frasi: il rapporto sta in una pagina" % (len(descrizione), DESCRIZIONE_MAX))
    campo(caso, "obiettivi", "caso", list)
    for k in ("obiettivi", "strumenti"):
        if k in caso and not elenco_di_testi(caso[k]):
            errori.append("caso.%s: deve essere un elenco di frasi" % k)
    if not isinstance(caso.get("gia_in_uso"), bool):
        errori.append("caso.gia_in_uso: serve true o false (lo strumento è già usato sui dati veri?)")

    segnali = report.get("segnali") if isinstance(report.get("segnali"), dict) else {}
    for k in SEGNALI:
        if not isinstance(segnali.get(k), bool):
            errori.append("segnali.%s: serve true o false" % k)
    da_confermare = report.get("segnali_da_confermare") or []
    if not isinstance(da_confermare, list) or any(k not in SEGNALI or not segnali.get(k) for k in da_confermare):
        errori.append("segnali_da_confermare: elenca solo segnali esistenti e accesi")

    att = report.get("attenzione") if isinstance(report.get("attenzione"), dict) else {}
    livello = att.get("livello")
    if livello not in LIVELLI:
        errori.append("attenzione.livello: usa uno tra %s" % ", ".join(LIVELLI))
    else:
        minimo = livello_minimo(segnali)
        if LIVELLI.index(livello) < LIVELLI.index(minimo):
            errori.append("attenzione.livello: con questi segnali il livello minimo è \"%s\"" % minimo)
    motivi = campo(att, "motivi", "attenzione", list) or []
    if motivi and not elenco_di_testi(motivi):
        errori.append("attenzione.motivi: deve essere un elenco di frasi")
        motivi = []
    if len(motivi) > MOTIVI_MAX:
        errori.append("attenzione.motivi: al massimo %d motivi, i più importanti" % MOTIVI_MAX)
    for i, m in enumerate(motivi):
        if isinstance(m, str) and len(m) > MOTIVO_MAX:
            errori.append("attenzione.motivi[%d]: %d caratteri, il massimo è %d" % (i, len(m), MOTIVO_MAX))

    if "ruoli" in report and not (isinstance(report["ruoli"], list) and all(isinstance(r, dict) for r in report["ruoli"])):
        errori.append("ruoli: deve essere un elenco di voci con ruolo, chi e documento")
    ruoli = [r for r in report.get("ruoli", []) if isinstance(r, dict)] if isinstance(report.get("ruoli"), list) else []
    for i, r in enumerate(ruoli):
        for k in ("ruolo", "chi", "documento"):
            campo(r, k, "ruoli[%d]" % i)
    if segnali.get("dati_personali") and not any("titolare" in str(r.get("ruolo", "")).lower() for r in ruoli if isinstance(r, dict)):
        errori.append("ruoli: con dati personali serve indicare chi è il titolare")

    def controlla_fonte(f, where, stati, principale=False):
        stato = f.get("stato")
        if stato not in stati:
            errori.append("%s.stato: usa uno tra %s" % (where, ", ".join(stati)))
            return None
        if "nota" in f and not isinstance(f["nota"], str):
            errori.append("%s.nota: deve essere un testo" % where)
        if stato == "non_verificata":
            if f.get("url") or f.get("data"):
                errori.append("%s: una fonte non verificata non ha indirizzo né data. Toglili, o segna la fonte per quello che è" % where)
            return stato
        if not url_ok(f.get("url")):
            errori.append("%s.url: serve un indirizzo http o https" % where)
        elif stato == "base" and f.get("url") not in urls_base:
            errori.append("%s.url: questo indirizzo non è nella base. Usa quello dato da fonti.py, oppure segna la fonte come ricontrollata se l'hai aperta oggi" % where)
        attesa = meta.get("base_verificata_il") if stato == "base" else meta.get("data")
        if parse_date(f.get("data")) is None:
            errori.append("%s.data: serve la data di lettura della fonte" % where)
        elif attesa and f.get("data") != attesa:
            errori.append("%s.data: con stato \"%s\" la data deve essere %s" % (where, stato, attesa))
        if not principale and not (isinstance(f.get("etichetta"), str) and f.get("etichetta")):
            errori.append("%s.etichetta: manca o è vuota" % where)
        return stato

    righe = report.get("righe") if isinstance(report.get("righe"), list) else []
    if not RIGHE_MIN <= len(righe) <= RIGHE_MAX:
        errori.append("righe: servono da %d a %d azioni, ora sono %d. Scegli quelle che contano per il caso" % (RIGHE_MIN, RIGHE_MAX, len(righe)))
    norme_citate = []
    ricontrollate = non_verificate = 0
    quando_usati = set()
    per_tipo = {t: 0 for t in TIPI}
    for i, r in enumerate(righe):
        where = "righe[%d]" % i
        if not isinstance(r, dict):
            errori.append("%s: deve essere un oggetto" % where)
            continue
        if "azione" not in r and ("problema" in r or "cosa_fare" in r):
            errori.append("%s: usa il formato a azioni, con \"tipo\" e \"azione\" al posto di \"problema\" e \"cosa_fare\"" % where)
            continue
        tipo = r.get("tipo")
        if tipo not in TIPI:
            errori.append("%s.tipo: usa uno tra %s" % (where, ", ".join(TIPI)))
        else:
            per_tipo[tipo] += 1
        azione = campo(r, "azione", where)
        if azione and len(azione) > AZIONE_MAX:
            errori.append("%s.azione: %d caratteri, il massimo è %d. Una riga sola: il resto va in \"nota\"" % (where, len(azione), AZIONE_MAX))
        if "nota" in r and not (isinstance(r["nota"], str) and len(r["nota"]) <= NOTA_MAX):
            errori.append("%s.nota: deve essere un testo di al massimo %d caratteri" % (where, NOTA_MAX))
        norme = campo(r, "norme", where, list) or []
        if not all(isinstance(n, str) and 0 < len(n) <= NORMA_MAX for n in norme):
            errori.append("%s.norme: ogni norma è un testo di al massimo %d caratteri" % (where, NORMA_MAX))
            norme = []
        norme_citate.extend(norme)
        if "altre_fonti" in r and not (isinstance(r["altre_fonti"], list) and all(isinstance(f, dict) for f in r["altre_fonti"])):
            errori.append("%s.altre_fonti: deve essere un elenco di fonti" % where)
            r = dict(r, altre_fonti=[])
        if not isinstance(r.get("fonte"), dict):
            errori.append("%s.fonte: manca la fonte principale" % where)
        if tipo == "da_fare":
            if not isinstance(r.get("quando"), str) or r.get("quando") not in QUANDO:
                errori.append("%s.quando: usa uno tra %s" % (where, ", ".join(QUANDO)))
            if isinstance(r.get("quando"), str):
                quando_usati.add(r["quando"])
        elif "quando" in r:
            errori.append("%s.quando: si usa solo con tipo \"da_fare\"" % where)
        fonte, altre = fonti_di_riga(r)
        stato = controlla_fonte(fonte, where + ".fonte", STATI_RIGA, principale=True)
        ricontrollate += stato == "ricontrollata"
        non_verificate += stato == "non_verificata"
        for j, f in enumerate(altre):
            controlla_fonte(f, "%s.altre_fonti[%d]" % (where, j), STATI_FONTE)

    for tipo, massimo in TIPO_MAX.items():
        if per_tipo[tipo] > massimo:
            errori.append("righe: le azioni \"%s\" sono %d, il massimo è %d. Il rapporto sta in una pagina: tieni le più importanti"
                          % (tipo, per_tipo[tipo], massimo))
    if righe and per_tipo["si_puo"] < 1:
        errori.append("righe: serve almeno un'azione \"si_puo\": cosa si può fare, e a quali condizioni")
    if righe and per_tipo["da_fare"] < DA_FARE_MIN:
        errori.append("righe: servono almeno %d azioni \"da_fare\"" % DA_FARE_MIN)
    if righe and per_tipo["non_si_puo"] < 1 and any(segnali.get(k) for k in SEGNALI):
        errori.append("righe: con questi segnali serve almeno un'azione \"non_si_puo\": cosa la norma vieta nel caso")

    for segnale, gruppi in COPERTURA.items():
        if segnali.get(segnale):
            for alternative in gruppi:
                if not any(rx.search(n) for _, rx in alternative for n in norme_citate):
                    errori.append("righe: il segnale \"%s\" è acceso ma nessuna riga cita %s"
                                  % (segnale, " oppure ".join(nome for nome, _ in alternative)))
    if isinstance(meta.get("settore"), str) and meta["settore"] in COPERTURA_SETTORE:
        nome, rx = COPERTURA_SETTORE[meta["settore"]]
        if not any(rx.search(n) for n in norme_citate):
            errori.append("righe: per questo settore serve una riga sull'informazione a clienti o pazienti che citi %s" % nome)
    if caso.get("gia_in_uso") is True and "subito" not in quando_usati:
        errori.append("righe: lo strumento è già in uso, serve almeno un'azione \"da_fare\" con quando \"subito\" (cosa fermare o sistemare adesso)")

    setup = report.get("setup") if isinstance(report.get("setup"), list) else []
    if not SETUP_MIN <= len(setup) <= SETUP_MAX:
        errori.append("setup: servono da %d a %d soluzioni, ora sono %d" % (SETUP_MIN, SETUP_MAX, len(setup)))
    for i, s in enumerate(setup):
        if not isinstance(s, dict):
            errori.append("setup[%d]: deve essere un oggetto" % i)
            continue
        for k in ("nome", "per_cosa", "costo"):
            campo(s, k, "setup[%d]" % i)
        for k in ("consigliato", "regge"):
            if k in s and not isinstance(s[k], bool):
                errori.append("setup[%d].%s: serve true o false" % (i, k))
        for k in ("pro", "contro"):
            if k in s and not (isinstance(s[k], list) and all(isinstance(x, str) for x in s[k])):
                errori.append("setup[%d].%s: deve essere un elenco di frasi" % (i, k))
        if "condizione" in s and not isinstance(s["condizione"], str):
            errori.append("setup[%d].condizione: deve essere un testo" % i)
        if isinstance(s, dict) and s.get("consigliato") is True and s.get("regge") is False:
            errori.append("setup[%d]: una soluzione che non regge per i dati del caso non può essere quella consigliata" % i)
        if isinstance(s, dict) and s.get("consigliato") is True:
            for k, massimo in SCELTA_MAX.items():
                if isinstance(s.get(k), str) and len(s[k]) > massimo:
                    errori.append("setup[%d].%s: %d caratteri, il massimo per la soluzione consigliata è %d (compare nel rapporto di una pagina)"
                                  % (i, k, len(s[k]), massimo))
    if setup and sum(1 for s in setup if isinstance(s, dict) and s.get("consigliato") is True) != 1:
        errori.append("setup: una e una sola soluzione deve avere \"consigliato\": true")

    costi = report.get("costi") if isinstance(report.get("costi"), dict) else {}
    campo(costi, "ipotesi", "costi")
    for i, v in enumerate(campo(costi, "voci", "costi", list) or []):
        for k in ("voce", "importo"):
            campo(v, k, "costi.voci[%d]" % i)
        if isinstance(v, dict) and "nota" in v and not isinstance(v["nota"], str):
            errori.append("costi.voci[%d].nota: deve essere un testo" % i)

    if "passi" in report and not (isinstance(report["passi"], list) and all(isinstance(x, str) and x for x in report["passi"])):
        errori.append("passi: se c'è, deve essere un elenco di frasi (facoltativo: l'ordine lo danno le azioni \"da_fare\")")
    aperti = report.get("aperti")
    if not isinstance(aperti, list):
        errori.append("aperti: serve l'elenco dei punti aperti (anche vuoto, se davvero non ce ne sono)")
        aperti = []
    for i, a in enumerate(aperti):
        if not isinstance(a, str) or not a:
            errori.append("aperti[%d]: deve essere una frase" % i)
        elif len(a) > APERTO_MAX:
            errori.append("aperti[%d]: %d caratteri, il massimo è %d. Una domanda per punto" % (i, len(a), APERTO_MAX))
    if non_verificate > len(aperti):
        errori.append("aperti: ci sono %d righe non verificate, ognuna va riportata anche tra i punti aperti" % non_verificate)
    if meta.get("ricontrollo") == "nessuno" and not any(re.search(r"riapert|ricontroll|online", str(a).lower()) for a in aperti):
        errori.append("aperti: senza ricontrollo online serve una voce che lo dica, per esempio \"Nessuna fonte è stata riaperta online\"")
    for chiave in ("rischi",):
        if chiave in report and not (isinstance(report[chiave], list) and all(isinstance(x, str) and x for x in report[chiave])):
            errori.append("%s: deve essere un elenco di frasi" % chiave)

    fonti = report.get("fonti", [])
    if not isinstance(fonti, list):
        errori.append("fonti: deve essere un elenco (può essere vuoto: la pagina prende le fonti dalle righe)")
        fonti = []
    for i, f in enumerate(fonti):
        if not isinstance(f, dict):
            errori.append("fonti[%d]: deve essere un oggetto" % i)
            continue
        controlla_fonte(f, "fonti[%d]" % i, STATI_FONTE)

    for path, text in tutte_le_stringhe(report):
        if "—" in text or "–" in text:
            errori.append("%s: contiene un trattino lungo, usa virgole o due punti" % path)
        pulito = senza_citazioni(normalizza(text)).lower()
        for frase in FRASI_VIETATE:
            if frase in pulito:
                errori.append("%s: non affermare \"%s\"; scrivi cosa è stato fatto e cosa resta" % (path, frase))
        m = AFFERMAZIONE_VIETATA.search(pulito)
        if m:
            errori.append("%s: non affermare che qualcosa \"%s\"; scrivi cosa dice la norma e cosa resta da fare" % (path, m.group(0)))

    if meta.get("ricontrollo") == "online" and ricontrollate == 0 and righe:
        avvisi.append("meta.ricontrollo dice \"online\" ma nessuna riga ha la fonte ricontrollata")
    d1, d0 = parse_date(meta.get("data")), parse_date(meta.get("base_verificata_il"))
    if d1 and d0 and (d1 - d0).days > SOGLIA_BASE_VECCHIA and ricontrollate == 0:
        avvisi.append("la base ha più di %d giorni e nessuna fonte è stata ricontrollata" % SOGLIA_BASE_VECCHIA)
    return errori, avvisi


# ------------------------------------------------- rapporto di una pagina e allegato

_CHIARI = ("--bg:#F3F5F9;--surface:#FFFFFF;--ink:#141A2A;--muted:#566079;--line:#D5DAE5;--accent:#2438B8;--accent-soft:#E4E8FA;"
           "--ok:#1B6E48;--ok-soft:#DDF1E6;--warn:#8A5200;--warn-soft:#FAEBCF;--stop:#A8231C;--stop-soft:#FADFDC")
_SCURI = ("--bg:#0E121B;--surface:#161B27;--ink:#E6E9F2;--muted:#9BA4BA;--line:#2B3246;--accent:#9AAAFF;--accent-soft:#1D2548;"
          "--ok:#63C898;--ok-soft:#12301F;--warn:#E5AC55;--warn-soft:#3A2A0C;--stop:#F38C84;--stop-soft:#3D1614;color-scheme:dark")
_TEMI = (":root{" + _CHIARI + "}\n"
         "@media (prefers-color-scheme: dark){:root:not([data-theme=\"light\"]){" + _SCURI + "}}\n"
         ":root[data-theme=\"dark\"]{" + _SCURI + "}\n")

# Il rapporto di una pagina: A4 in stampa, una colonna sul telefono.
CSS_PAGINA = _TEMI + """
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Helvetica Neue",Arial,sans-serif;font-size:13.5px;line-height:1.4}
.page{max-width:210mm;margin:24px auto;padding:11mm 12mm 9mm;background:var(--surface);border:1px solid var(--line);display:grid;gap:1em}
header{display:grid;gap:.45em}
h1{margin:0;font-size:1.7em;line-height:1.15;letter-spacing:-0.01em;text-wrap:balance}
h2{margin:0;font-size:.95em;line-height:1.2;letter-spacing:.05em;text-transform:uppercase}
p{margin:0}
a{color:inherit;text-decoration:underline;text-decoration-color:var(--line);text-underline-offset:2px}
.eyebrow{font-size:.78em;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
.caso{color:var(--muted);font-size:.93em}
.level{padding:.5em .75em;background:var(--bg);border-left:5px solid var(--muted);font-size:.93em}
.level.alta{border-left-color:var(--stop)}.level.media{border-left-color:var(--warn)}.level.bassa{border-left-color:var(--ok)}
.banner{padding:.45em .75em;background:var(--warn-soft);color:var(--warn);font-size:.9em}
.due{display:grid;grid-template-columns:1fr 1fr;gap:1.1em;align-items:start}
.blocco{display:grid;gap:.55em;align-content:start;border-top:4px solid var(--line);padding-top:.55em;min-width:0}
.blocco.si{border-top-color:var(--ok)}.blocco.si h2{color:var(--ok)}
.blocco.no{border-top-color:var(--stop)}.blocco.no h2{color:var(--stop)}
.blocco.fare{border-top-color:var(--accent)}.blocco.fare h2{color:var(--accent)}
ul,ol{margin:0;padding:0;list-style:none;display:grid;gap:.5em}
li{break-inside:avoid}
.si li,.no li,.ap li{padding-left:1em;position:relative}
.si li::before,.no li::before,.ap li::before{content:"";position:absolute;left:0;top:.5em;width:.42em;height:.42em;border-radius:50%;background:var(--ok)}
.no li::before{background:var(--stop)}
.ap li::before{background:var(--muted)}
.fare ol{display:block;columns:2;column-gap:1.1em;counter-reset:n}
.fare li{counter-increment:n;position:relative;padding-left:1.75em;margin-bottom:.5em}
.fare li::before{content:counter(n);position:absolute;left:0;top:.1em;width:1.6em;height:1.6em;border-radius:50%;background:var(--accent);color:var(--surface);font-size:.74em;font-weight:700;line-height:1.6em;text-align:center}
.q{font-weight:700;font-size:.78em;letter-spacing:.04em;text-transform:uppercase;color:var(--accent);margin-right:.25em}
.q.subito{color:var(--stop)}
.n{color:var(--muted);font-size:.82em}
.nv{font-size:.72em;font-weight:700;text-transform:uppercase;color:var(--warn);background:var(--warn-soft);padding:0 .45em;border-radius:3px;white-space:nowrap}
.note{color:var(--muted);font-size:.86em}
footer{font-size:.78em;color:var(--muted);border-top:1px solid var(--line);padding-top:.6em}
@media (max-width:640px){.page{margin:0;border:0;padding:20px 16px}.due{grid-template-columns:1fr}.fare ol{columns:1}}
@media print{
:root,:root:not([data-theme="light"]),:root[data-theme="dark"]{""" + _CHIARI + """;color-scheme:light}
@page{size:A4;margin:0}
body{background:#fff;font-size:11.6px}
.page{margin:0;border:0;max-width:none;width:210mm;padding:9mm 12mm 7mm;gap:.85em}
a{text-decoration:none}
}
"""

# L'allegato di dettaglio: tabelle, fonti con link, alternative e costi.
CSS = _TEMI + """
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:Georgia,"Times New Roman",serif;font-size:17px;line-height:1.6}
.wrap{max-width:58rem;margin-inline:auto;padding-inline:20px;padding-block:36px 64px;display:grid;gap:36px}
section{display:grid;gap:14px;min-width:0}
h1,h2,h3,th,.pill,.eyebrow,.k{font-family:"Helvetica Neue",Arial,sans-serif}
h1{margin:0;font-size:clamp(1.9rem,5vw,2.8rem);line-height:1.05;letter-spacing:-0.02em;text-wrap:balance}
h2{margin:0;font-size:1.45rem;line-height:1.2}
p{margin:0;max-width:68ch}
a{color:var(--accent)}
.eyebrow{font-size:.74rem;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
.note{font-size:.92rem;color:var(--muted)}
.level{display:grid;gap:8px;padding:16px 18px;background:var(--surface);border:1px solid var(--line);border-left:6px solid var(--muted)}
.level.alta{border-left-color:var(--stop)}.level.media{border-left-color:var(--warn)}.level.bassa{border-left-color:var(--ok)}
.level strong{font-family:"Helvetica Neue",Arial,sans-serif;font-size:1.15rem}
.banner{padding:10px 14px;background:var(--warn-soft);color:var(--warn);font-size:.95rem}
ul,ol{margin:0;padding-left:1.2rem;display:grid;gap:6px;max-width:70ch}
.scroll{overflow-x:auto;border:1px solid var(--line);background:var(--surface)}
table{border-collapse:collapse;width:100%;font-size:.92rem;line-height:1.45}
th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--line)}
tr:last-child td{border-bottom:0}
th{font-size:.76rem;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);background:var(--bg)}
table.righe{min-width:760px}
table.righe td:first-child{width:30%;font-weight:600}
.f{display:grid;gap:6px}
.cite{display:inline-block;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.72rem;padding:0 6px;margin:0 4px 4px 0;border:1px solid var(--line);border-radius:3px;color:var(--muted)}
.pill{display:inline-block;font-weight:700;font-size:.74rem;padding:1px 8px;border-radius:99px;white-space:nowrap;justify-self:start}
.pill.ok{color:var(--ok);background:var(--ok-soft)}.pill.warn{color:var(--warn);background:var(--warn-soft)}.pill.stop{color:var(--stop);background:var(--stop-soft)}
.pill.info{color:var(--accent);background:var(--accent-soft)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(16rem,1fr));gap:14px}
.card{display:grid;gap:8px;align-content:start;padding:14px 16px;background:var(--surface);border:1px solid var(--line);min-width:0}
.card.pick{border-color:var(--accent);box-shadow:inset 0 3px 0 var(--accent)}
.card.no{border-style:dashed}
.card h3{margin:0;font-size:1.05rem}
.k{font-size:.74rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
footer{color:var(--muted);font-size:.88rem}
@media print{
:root,:root:not([data-theme="light"]),:root[data-theme="dark"]{""" + _CHIARI + """;color-scheme:light}
@page{size:A4;margin:14mm}
body{background:#fff;font-size:10.5pt}
.wrap{max-width:none;padding:0;gap:22px}
.scroll{overflow:visible}
table.righe{min-width:0}
tr,.card{break-inside:avoid}
}
"""

CSP = "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'"
NON_PARERE = "Non è un parere legale: contratti, informative e valutazione d'impatto vanno riletti da un legale privacy."


def e(value):
    return html.escape(str(value if value is not None else ""), quote=True)


def link(url, label):
    if not url_ok(url):
        return e(label)
    return '<a href="%s" rel="noopener noreferrer" target="_blank">%s</a>' % (e(url), e(label))


def testo_stato(fonte):
    stato = (fonte or {}).get("stato")
    if stato == "ricontrollata":
        return "ok", "Ricontrollata il %s" % data_it(fonte.get("data"))
    if stato == "base":
        return "warn", "Dalla base del %s" % data_it(fonte.get("data"))
    return "stop", "Non verificata"


def lista(items, ordered=False):
    tag = "ol" if ordered else "ul"
    return "<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % e(x) for x in items or []), tag)


def senza_punto(text):
    return str(text or "").strip().rstrip(".")


def azioni(report, tipo):
    """Le azioni di un tipo, nell'ordine del rapporto; le "da_fare" in ordine di urgenza."""
    righe = [r for r in report.get("righe", []) if isinstance(r, dict) and r.get("tipo") == tipo]
    if tipo == "da_fare":
        righe.sort(key=lambda r: QUANDO.index(r["quando"]) if r.get("quando") in QUANDO else len(QUANDO))
    return righe


def etichetta_quando(report, quando):
    gia = report.get("caso", {}).get("gia_in_uso") is True
    return {"subito": "Subito",
            "prima": "Prima di continuare" if gia else "Prima di partire",
            "entro_30_giorni": "Entro 30 giorni",
            "dopo": "In seguito"}.get(quando, "")


def elenco_fonti(report):
    """Fonti del rapporto: quelle delle azioni, piu' le eventuali extra, senza doppioni."""
    viste, out = set(), []

    def aggiungi(f, etichetta):
        url = f.get("url")
        if f.get("stato") in STATI_FONTE and url_ok(url) and url not in viste:
            viste.add(url)
            out.append({"etichetta": f.get("etichetta") or etichetta, "url": url, "stato": f["stato"], "data": f.get("data")})

    for r in report.get("righe", []):
        fonte, altre = fonti_di_riga(r)
        aggiungi(fonte, (r.get("norme") or ["fonte"])[0])
        for f in altre:
            aggiungi(f, "fonte")
    for f in report.get("fonti") or []:
        if isinstance(f, dict):
            aggiungi(f, "fonte")
    return out


def conteggi(report):
    righe = report.get("righe", [])
    stati = [fonti_di_riga(r)[0].get("stato") for r in righe]
    return len(righe), stati.count("ricontrollata"), stati.count("non_verificata")


def _testa(titolo, css, csp):
    out = ["<!doctype html>", '<html lang="it">', "<head>", '<meta charset="utf-8">',
           '<meta name="viewport" content="width=device-width, initial-scale=1">']
    if csp:
        out.append('<meta http-equiv="Content-Security-Policy" content="%s">' % e(CSP))
    return out + ["<title>%s</title>" % e(titolo), "<style>%s</style>" % css, "</head>", "<body>"]


def _banner(report):
    meta = report["meta"]
    d1, d0 = parse_date(meta["data"]), parse_date(meta["base_verificata_il"])
    giorni = (d1 - d0).days if d1 and d0 else 0
    if giorni > SOGLIA_BASE_VECCHIA and conteggi(report)[1] == 0:
        return ('<p class="banner">La base di conoscenza è del %s, %d giorni prima di questa analisi, e nessuna fonte è stata ricontrollata. Norme e listini possono essere cambiati.</p>'
                % (e(data_it(meta["base_verificata_il"])), giorni))
    return ""


def _voce(report, r):
    """Una riga del rapporto di una pagina: azione, norme, eventuale avviso."""
    fonte = fonti_di_riga(r)[0]
    norme = "; ".join(str(n) for n in r.get("norme") or [])
    pezzi = []
    if r.get("tipo") == "da_fare":
        pezzi.append('<span class="q%s">%s</span>' % (" subito" if r.get("quando") == "subito" else "", e(etichetta_quando(report, r.get("quando")))))
    pezzi.append(e(senza_punto(r.get("azione"))))
    if norme:
        collegabile = fonte.get("stato") in STATI_FONTE and url_ok(fonte.get("url"))
        pezzi.append('<span class="n">%s</span>' % (link(fonte.get("url"), norme) if collegabile else e(norme)))
    if fonte.get("stato") == "non_verificata":
        pezzi.append('<span class="nv">da verificare</span>')
    return "<li>%s</li>" % " ".join(pezzi)


def costruisci_html(report, csp=True):
    """Il rapporto di una pagina: si può, non si può, da fare."""
    meta, caso, att = report["meta"], report["caso"], report["attenzione"]
    totale, ricontrollate, non_verificate = conteggi(report)
    out = _testa(meta["titolo"], CSS_PAGINA, csp) + ['<div class="page">']

    motivi = " ".join(senza_punto(m) + "." for m in att.get("motivi") or [])
    out.append('<header><span class="eyebrow">Privacy e IA · %s · %s</span><h1>%s</h1><p class="caso">%s</p>'
               '<p class="level %s"><strong>Attenzione %s.</strong> %s</p>%s</header>'
               % (e(ETICHETTE_SETTORE.get(meta["settore"], meta["settore"])), e(data_it(meta["data"])), e(meta["titolo"]),
                  e(caso["descrizione"]), e(att["livello"]), e(att["livello"]), e(motivi), _banner(report)))

    def blocco(tipo, classe):
        voci = "".join(_voce(report, r) for r in azioni(report, tipo))
        return '<section class="blocco %s"><h2>%s</h2><ul>%s</ul></section>' % (classe, e(ETICHETTE_TIPO[tipo]), voci or "<li>Nessuna voce.</li>")

    out.append('<div class="due">%s%s</div>' % (blocco("si_puo", "si"), blocco("non_si_puo", "no")))
    out.append('<section class="blocco fare"><h2>%s</h2><ol>%s</ol></section>'
               % (e(ETICHETTE_TIPO["da_fare"]), "".join(_voce(report, r) for r in azioni(report, "da_fare"))))

    scelta = next((s for s in report["setup"] if s.get("consigliato") is True), report["setup"][0])
    sol = ["<p><strong>%s</strong></p>" % e(senza_punto(scelta["nome"])), "<p>%s</p>" % e(scelta["per_cosa"]),
           "<p>Costo: %s.</p>" % e(senza_punto(scelta["costo"]))]
    if scelta.get("condizione"):
        sol.append('<p class="note">A condizione che: %s.</p>' % e(senza_punto(scelta["condizione"])))
    non_basta = [senza_punto(s["nome"]) for s in report["setup"] if s.get("regge") is False]
    if non_basta:
        sol.append('<p class="note">Non basta per questi dati: %s.</p>' % e("; ".join(non_basta)))

    aperti = list(report.get("aperti") or [])
    ap = [lista(aperti[:APERTI_IN_PAGINA]) if aperti else "<p>Nessun punto aperto segnalato.</p>"]
    if len(aperti) > APERTI_IN_PAGINA:
        ap.append('<p class="note">Altri %d nel dettaglio.</p>' % (len(aperti) - APERTI_IN_PAGINA))
    out.append('<div class="due"><section class="blocco"><h2>Soluzione consigliata</h2>%s</section>'
               '<section class="blocco ap"><h2>Punti aperti</h2>%s</section></div>' % ("".join(sol), "".join(ap)))

    out.append("<footer><p>Analisi preliminare del %s su fonti pubbliche, base del %s. Azioni con la fonte riaperta in questa analisi: %d su %d; non verificate: %d. "
               "Ruoli, alternative, costi e fonti con link sono nell'allegato dettaglio.html. %s</p></footer>"
               % (e(data_it(meta["data"])), e(data_it(meta["base_verificata_il"])), ricontrollate, totale, non_verificate, e(NON_PARERE)))
    out += ["</div>", "</body>", "</html>"]
    return "\n".join(out) + "\n"


def costruisci_dettaglio(report, csp=True):
    """L'allegato: ruoli, azioni con nota e fonte, alternative, costi, punti aperti, fonti."""
    meta, caso, att = report["meta"], report["caso"], report["attenzione"]
    segnali = report["segnali"]
    totale, ricontrollate, non_verificate = conteggi(report)
    out = _testa("Dettaglio: " + meta["titolo"], CSS, csp) + ['<div class="wrap">']

    out.append('<header><section><span class="eyebrow">Privacy e IA · %s · %s · allegato di dettaglio</span><h1>%s</h1><p>%s</p>'
               '<p class="note">Analisi preliminare su fonti pubbliche. %s</p></section></header>'
               % (e(ETICHETTE_SETTORE.get(meta["settore"], meta["settore"])), e(data_it(meta["data"])), e(meta["titolo"]), e(caso["descrizione"]), e(NON_PARERE)))
    out.append(_banner(report))

    incerti = set(report.get("segnali_da_confermare") or [])
    accesi = [ETICHETTE_SEGNALI[k] + (" (da confermare)" if k in incerti else "") for k in SEGNALI if segnali.get(k)]
    out.append('<section><h2>Livello di attenzione</h2><div class="level %s"><strong>Attenzione %s</strong>%s</div>%s</section>'
               % (e(att["livello"]), e(att["livello"]), lista(att.get("motivi")),
                  ('<p class="note">Segnali rilevati: %s.</p>' % e("; ".join(accesi))) if accesi else ""))

    if report.get("rischi"):
        out.append("<section><h2>Cosa si rischia</h2>%s</section>" % lista(report["rischi"]))

    dettagli = []
    if caso.get("gia_in_uso") is True:
        dettagli.append("Lo strumento è già in uso sui dati veri")
    if isinstance(caso.get("persone"), int) and caso["persone"] > 0:
        dettagli.append("Persone che lo usano: %d" % caso["persone"])
    if caso.get("strumenti"):
        dettagli.append("Strumenti previsti o già in uso: %s" % "; ".join(caso["strumenti"]))
    out.append("<section><h2>Cosa si vuole fare</h2>%s%s</section>"
               % (lista(caso.get("obiettivi")), ('<p class="note">%s.</p>' % e(". ".join(dettagli))) if dettagli else ""))

    if report.get("ruoli"):
        rows = "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (e(r["ruolo"]), e(r["chi"]), e(r["documento"])) for r in report["ruoli"])
        out.append('<section><h2>Chi fa cosa</h2><div class="scroll"><table><thead><tr><th>Ruolo</th><th>Chi</th><th>Documento che serve</th></tr></thead><tbody>%s</tbody></table></div></section>' % rows)

    for tipo in TIPI:
        gruppo = azioni(report, tipo)
        if not gruppo:
            continue
        rows = []
        for r in gruppo:
            fonte, altre = fonti_di_riga(r)
            classe, etichetta = testo_stato(fonte)
            celle = []
            if fonte.get("stato") in STATI_FONTE and url_ok(fonte.get("url")):
                celle.append("<span>%s</span>" % link(fonte["url"], fonte.get("etichetta") or "fonte principale"))
            celle.append('<span class="pill %s">%s</span>' % (classe, e(etichetta)))
            if fonte.get("nota"):
                celle.append('<span class="note">%s</span>' % e(fonte["nota"]))
            for f in altre:
                if url_ok(f.get("url")):
                    celle.append("<span>%s</span>" % link(f["url"], f.get("etichetta") or "altra fonte"))
            quando = ('<span class="pill info">%s</span> ' % e(etichetta_quando(report, r.get("quando")))) if tipo == "da_fare" else ""
            rows.append("<tr><td>%s%s</td><td>%s</td><td>%s</td><td><div class=\"f\">%s</div></td></tr>"
                        % (quando, e(r["azione"]), e(r.get("nota") or ""), "".join('<span class="cite">%s</span>' % e(n) for n in r["norme"]), "".join(celle)))
        out.append('<section><h2>%s</h2><div class="scroll"><table class="righe"><thead><tr><th>Azione</th><th>Perché e come</th><th>Norme</th><th>Fonte</th></tr></thead><tbody>%s</tbody></table></div></section>'
                   % (e(ETICHETTE_TIPO[tipo]), "".join(rows)))

    cards = []
    for s in report["setup"]:
        if s.get("consigliato") is True:
            classe, etichetta = " pick", "Consigliata"
        elif s.get("regge") is False:
            classe, etichetta = " no", "Non basta per questi dati"
        else:
            classe, etichetta = "", "Alternativa"
        cards.append('<div class="card%s"><span class="k">%s</span><h3>%s</h3><p>%s</p>%s%s%s<p><span class="k">Costo</span><br>%s</p></div>'
                     % (classe, etichetta, e(s["nome"]), e(s["per_cosa"]),
                        ('<p class="note">A condizione che: %s</p>' % e(s["condizione"])) if s.get("condizione") else "",
                        ('<p><span class="k">Pro</span></p>' + lista(s.get("pro"))) if s.get("pro") else "",
                        ('<p><span class="k">Contro</span></p>' + lista(s.get("contro"))) if s.get("contro") else "",
                        e(s["costo"])))
    out.append('<section><h2>Soluzioni possibili</h2><div class="cards">%s</div></section>' % "".join(cards))

    costi = report["costi"]
    rows = "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (e(v.get("voce")), e(v.get("importo")), e(v.get("nota"))) for v in costi["voci"])
    out.append('<section><h2>Costi a listino</h2><p>%s</p><div class="scroll"><table><thead><tr><th>Voce</th><th>Importo</th><th>Nota</th></tr></thead><tbody>%s</tbody></table></div></section>' % (e(costi["ipotesi"]), rows))

    if report.get("passi"):
        out.append("<section><h2>Cosa fare, in ordine</h2>%s</section>" % lista(report["passi"], ordered=True))

    aperti = list(report.get("aperti") or [])
    nota = "Azioni con la fonte principale riaperta in questa analisi: %d su %d. Non verificate: %d. Base di conoscenza del %s." % (
        ricontrollate, totale, non_verificate, data_it(meta["base_verificata_il"]))
    if meta.get("ricontrollo_dettaglio"):
        nota += " " + str(meta["ricontrollo_dettaglio"])
    out.append("<section><h2>Punti aperti e cose non verificate</h2>%s<p class=\"note\">%s</p></section>"
               % (lista(aperti) if aperti else "<p>Nessun punto aperto segnalato.</p>", e(nota)))

    fonti = "".join("<li>%s <span class=\"note\">(%s il %s)</span></li>"
                    % (link(f["url"], f["etichetta"]), "ricontrollata" if f["stato"] == "ricontrollata" else "dalla base", e(data_it(f["data"])))
                    for f in elenco_fonti(report))
    out.append("<section><h2>Fonti</h2><ul>%s</ul></section>" % fonti)
    out.append("<footer><p>Generato con ai-privacy-check. Analisi preliminare, non un parere legale.</p></footer>")
    out += ["</div>", "</body>", "</html>"]
    return "\n".join(x for x in out if x) + "\n"


def _riga_testo(report, r, numero=None):
    norme = "; ".join(str(n) for n in r.get("norme") or [])
    quando = (etichetta_quando(report, r.get("quando")) + ": ") if r.get("tipo") == "da_fare" else ""
    testa = ("%d. " % numero) if numero else "- "
    return "%s%s%s%s" % (testa, quando, senza_punto(r.get("azione")), (" (%s)" % norme) if norme else "")


def costruisci_sintesi(report):
    """La sintesi per la chat: le stesse voci del rapporto di una pagina."""
    meta, att = report["meta"], report["attenzione"]
    scelta = next((s for s in report["setup"] if s.get("consigliato") is True), report["setup"][0])
    aperti = list(report.get("aperti") or [])
    righe = ["# %s" % meta["titolo"], "", "Attenzione %s:" % att["livello"]] + ["- " + senza_punto(m) for m in att.get("motivi") or []]
    for tipo in ("si_puo", "non_si_puo"):
        righe += ["", ETICHETTE_TIPO[tipo] + ":"] + [_riga_testo(report, r) for r in azioni(report, tipo)]
    righe += ["", ETICHETTE_TIPO["da_fare"] + ":"] + [_riga_testo(report, r, i) for i, r in enumerate(azioni(report, "da_fare"), 1)]
    righe += ["", "Soluzione consigliata: %s. Costo: %s." % (senza_punto(scelta["nome"]), senza_punto(scelta["costo"]))]
    if scelta.get("condizione"):
        righe.append("A condizione che: %s." % senza_punto(scelta["condizione"]))
    non_basta = [senza_punto(s["nome"]) for s in report["setup"] if s.get("regge") is False]
    if non_basta:
        righe.append("Non basta per questi dati: %s." % "; ".join(non_basta))
    if report.get("rischi"):
        righe += ["", "Cosa si rischia:"] + ["- " + senza_punto(x) for x in report["rischi"]]
    righe += ["", "Punti aperti:"] + ["- " + senza_punto(a) for a in (aperti[:APERTI_IN_PAGINA] or ["nessuno segnalato"])]
    if len(aperti) > APERTI_IN_PAGINA:
        righe.append("- e altri %d nel dettaglio" % (len(aperti) - APERTI_IN_PAGINA))
    righe += ["", "Analisi preliminare del %s, base del %s. Non è un parere legale." % (data_it(meta["data"]), data_it(meta["base_verificata_il"]))]
    return "\n".join(righe) + "\n"


def costruisci_testo(report):
    """Rapporto e allegato in testo semplice, per rileggerli senza un browser."""
    meta, caso, att = report["meta"], report["caso"], report["attenzione"]
    out = [meta["titolo"].upper(), caso["descrizione"], "", "ATTENZIONE %s" % att["livello"].upper()] + ["- " + m for m in att.get("motivi") or []]
    for tipo in TIPI:
        out += ["", ETICHETTE_TIPO[tipo].upper()]
        for i, r in enumerate(azioni(report, tipo), 1):
            fonte, altre = fonti_di_riga(r)
            out.append(_riga_testo(report, r, i if tipo == "da_fare" else None))
            if r.get("nota"):
                out.append("  NOTA: " + r["nota"])
            stato = testo_stato(fonte)[1]
            if fonte.get("stato") in STATI_FONTE and url_ok(fonte.get("url")):
                out.append("  FONTE: %s, %s. %s" % (fonte.get("etichetta") or "fonte principale", stato, fonte["url"]))
            else:
                out.append("  FONTE: " + stato)
            if fonte.get("nota"):
                out.append("  NOTA SULLA FONTE: " + fonte["nota"])
            for f in altre:
                out.append("  ALTRA FONTE: %s. %s" % (f.get("etichetta"), f.get("url")))
    if report.get("rischi"):
        out += ["", "COSA SI RISCHIA"] + ["- " + x for x in report["rischi"]]
    out += ["", "CHI FA COSA"] + ["- %s: %s. Documento: %s" % (r["ruolo"], senza_punto(r["chi"]), r["documento"]) for r in report.get("ruoli", [])]
    out += ["", "SOLUZIONI"]
    for s in report["setup"]:
        tipo = "consigliata" if s.get("consigliato") is True else ("non basta" if s.get("regge") is False else "alternativa")
        out.append("- [%s] %s: %s Costo: %s" % (tipo, s["nome"], s["per_cosa"], s["costo"]))
        if s.get("condizione"):
            out.append("  A CONDIZIONE CHE: " + s["condizione"])
        if s.get("pro"):
            out.append("  PRO: " + "; ".join(s["pro"]))
        if s.get("contro"):
            out.append("  CONTRO: " + "; ".join(s["contro"]))
    out += ["", "COSTI", report["costi"]["ipotesi"]] + ["- %s: %s. %s" % (v.get("voce"), v.get("importo"), v.get("nota", "")) for v in report["costi"]["voci"]]
    if report.get("passi"):
        out += ["", "COSA FARE, IN ORDINE"] + ["%d. %s" % (i, p) for i, p in enumerate(report["passi"], 1)]
    out += ["", "PUNTI APERTI"] + ["- " + a for a in (report.get("aperti") or ["nessuno segnalato"])]
    if meta.get("ricontrollo_dettaglio"):
        out += ["", "RICONTROLLO", str(meta["ricontrollo_dettaglio"])]
    out += ["", "FONTI"] + ["- %s (%s): %s" % (f["etichetta"], f["stato"], f["url"]) for f in elenco_fonti(report)]
    return "\n".join(out) + "\n"


def carica_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def scrivi_sicuro(path, text):
    """Scrive un file senza seguire collegamenti, con permessi 0600 e in modo atomico.

    Il testo va in un file temporaneo nuovo nella stessa cartella, che poi prende il posto
    della destinazione: un collegamento simbolico o fisico messo lì da altri non viene seguito.
    """
    dati = text.encode("utf-8")
    if os.path.islink(path):
        raise OSError("rifiuto di scrivere su un collegamento simbolico: %s" % path)
    fd, tmp = tempfile.mkstemp(prefix=".apc-", dir=os.path.dirname(os.path.abspath(path)))
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(dati)
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
