#!/usr/bin/env python3
"""Cerca nella base delle affermazioni verificate, senza caricarla tutta.

Uso:
  python3 fonti.py norma "GDPR art. 28"        le affermazioni su quell'articolo di quell'atto
  python3 fonti.py cerca "conservazione zero"  tutte le parole devono comparire, in qualunque ordine
  python3 fonti.py cerca "DPA" --dominio vendors --breve
  python3 fonti.py elenco prof                 id e tema di un dominio, per orientarsi
  python3 fonti.py id eu-28 san-27             le affermazioni con questi id
  python3 fonti.py json eu-08 it-15            i blocchi "fonte" pronti da incollare in report.json
  python3 fonti.py aperti sanita               cosa non è stato verificato in un dominio
  python3 fonti.py domini                      elenco dei domini

La ricerca guarda tema, testo, punto della fonte e note del secondo controllo.
Se non trova nulla lo dice ed esce con 0: vuol dire che la cosa non è nella base.
"""
import argparse
import json
import os
import re
import sys

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "affermazioni.json")
# Un nome di settore puo' aprire piu' domini della base.
ALIAS = {"sanita": ("san", "audio", "v2legal"), "sanità": ("san", "audio", "v2legal"), "medici": ("san", "audio", "v2legal"),
         "professioni": ("prof", "v2legal"), "commercialisti": ("prof", "v2legal"), "avvocati": ("prof", "v2legal"),
         "consulenti": ("prof", "v2legal"), "fornitori": ("vendors", "audio"), "closed": ("vendors", "audio"),
         "open-source": ("oss", "audio"), "opensource": ("oss", "audio"), "costi": ("oss", "audio"),
         "ue": ("eu",), "italia": ("it",),
         "trascrizione": ("audio",), "legale": ("v2legal",), "gia-in-uso": ("v2legal", "audio")}
# Come gli atti sono scritti nei file di riferimento e come compaiono nella base.
ATTI = {
    "gdpr": ("gdpr", "2016/679"),
    "ai act": ("ai act", "2024/1689", "2026/1744"),
    "codice privacy": ("codice privacy", "196/2003"),
    "l. 132/2025": ("132/2025",),
    "d.lgs. 179/2026": ("179/2026",),
    "d.lgs. 152/1997": ("152/1997",),
    "l. 300/1970": ("300/1970", "statuto dei lavoratori"),
    "codice penale": ("codice penale", "c.p.", "615-ter", "622"),
    "garante": ("garante",),
    "edpb": ("edpb",),
    "cgue": ("cgue", "curia", "c-"),
}


def carica(path=BASE):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def tutto(a):
    return " ".join([a["tema"], a["testo"], a.get("dove", ""), a.get("nota", ""), a.get("nota_controllo", ""), a["url"]]).lower()


def stampa(a, base, breve=False):
    if breve:
        print("[%s] %s | %s" % (a["id"], a["tema"], a["url"]))
        return
    print("[%s] %s | fonte %s | %s" % (a["id"], a["esito"], a["fonte"], a["tema"]))
    print("  " + a["testo"])
    if a.get("dove"):
        print("  Dove: " + a["dove"])
    print("  URL: " + a["url"])
    if a.get("nota_controllo"):
        print("  Secondo controllo: " + a["nota_controllo"])
    print("  Verificato il " + a.get("verificato_il", base["verificato_il"]))


def etichetta(a):
    """Un nome leggibile per la fonte: l'atto e l'articolo quando il tema è generico."""
    tema = re.sub(r"^(Verifica|Strumento già in uso): ", "", a["tema"]).strip()
    dove = re.split(r";| \(", a.get("dove", ""))[0].strip()
    if " - " not in tema and ":" not in tema and "art." in dove and len(dove) <= 80:
        return dove
    return tema[:1].upper() + tema[1:]


def scelti(base, chiave):
    """I domini indicati da una chiave o da un nome di settore. None se sconosciuta."""
    if not chiave:
        return base["domini"]
    chiavi = ALIAS.get(chiave.lower(), (chiave.lower(),))
    trovati = [d for d in base["domini"] if d["chiave"] in chiavi]
    return trovati or None


def per_norma(affermazioni, norma):
    """Filtra per atto e numero di articolo, con il numero isolato."""
    n = norma.lower().strip()
    atto = next((k for k in ATTI if n.startswith(k)), None)
    m = re.search(r"art\.?\s*([0-9]+(?:-[a-z]+)?)", n)
    numero = m.group(1) if m else None
    out = []
    for a in affermazioni:
        t = tutto(a)
        testa = (a["tema"] + " " + a.get("dove", "") + " " + a["testo"]).lower()
        if atto and not any(s in t for s in ATTI[atto]):
            continue
        if numero and not re.search(r"art(?:t)?\.?[^.;]{0,40}?(?<![\d(])" + re.escape(numero) + r"(?![\d])", testa):
            continue
        if not atto and not numero and n not in t:
            continue
        out.append(a)
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description="Cerca nella base di ai-privacy-check")
    sub = parser.add_subparsers(dest="cmd", required=True)
    for nome in ("cerca", "norma"):
        c = sub.add_parser(nome)
        c.add_argument("testo")
        c.add_argument("--dominio")
        c.add_argument("--max", type=int, default=12)
        c.add_argument("--breve", action="store_true")
    el = sub.add_parser("elenco")
    el.add_argument("dominio", nargs="?")
    i = sub.add_parser("id")
    i.add_argument("ids", nargs="+")
    i.add_argument("--breve", action="store_true")
    j = sub.add_parser("json")
    j.add_argument("ids", nargs="+")
    a = sub.add_parser("aperti")
    a.add_argument("dominio")
    sub.add_parser("domini")
    args = parser.parse_args(argv)
    base = carica()
    nomi = ", ".join(x["chiave"] for x in base["domini"])

    if args.cmd == "domini":
        for d in base["domini"]:
            print("%-8s %s (%d affermazioni)" % (d["chiave"], d["nome"], len(d["affermazioni"])))
        return 0

    if args.cmd == "aperti":
        domini = scelti(base, args.dominio)
        if domini is None:
            print("Dominio sconosciuto. Usa: " + nomi + ", oppure un settore: commercialisti, sanita, avvocati, fornitori, costi")
            return 1
        for d in domini:
            print("## %s, %s" % (d["chiave"], d["nome"]))
            print("NON VERIFICATO")
            for g in d["non_verificato"]:
                print(" - " + g)
            print("SEGNALAZIONI DEL SECONDO CONTROLLO")
            for g in d["segnalazioni"]:
                print(" - " + g)
        return 0

    if args.cmd == "elenco":
        domini = scelti(base, args.dominio)
        if domini is None:
            print("Dominio sconosciuto. Usa: " + nomi)
            return 1
        for d in domini:
            print("## %s, %s" % (d["chiave"], d["nome"]))
            for aff in d["affermazioni"]:
                print("%s  %s" % (aff["id"], aff["tema"]))
        return 0

    if args.cmd in ("id", "json"):
        per_id = {aff["id"]: aff for d in base["domini"] for aff in d["affermazioni"]}
        mancanti = [x for x in args.ids if x not in per_id]
        if args.cmd == "json":
            blocchi = [{"id": x, "fonte": {"stato": "base", "data": per_id[x].get("verificato_il", base["verificato_il"]),
                                           "url": per_id[x]["url"], "etichetta": etichetta(per_id[x])}}
                       for x in args.ids if x in per_id]
            print(json.dumps(blocchi, ensure_ascii=False, indent=1))
        else:
            for x in args.ids:
                if x in per_id:
                    stampa(per_id[x], base, args.breve)
        if mancanti:
            print("Id non presenti nella base: " + ", ".join(mancanti))
            return 1
        return 0

    domini = scelti(base, args.dominio)
    if domini is None:
        print("Dominio sconosciuto. Usa: " + nomi)
        return 1
    affermazioni = [aff for d in domini for aff in d["affermazioni"]]
    if args.cmd == "norma":
        trovate = per_norma(affermazioni, args.testo)
    else:
        parole = [p for p in re.split(r"\s+", args.testo.lower().strip()) if p]
        trovate = [aff for aff in affermazioni if all(p in tutto(aff) for p in parole)]
    for aff in trovate[: args.max]:
        stampa(aff, base, args.breve)
    if not trovate:
        print("Nessun risultato per \"%s\": questa cosa non è nella base. Trattala come non verificata, o verificala online." % args.testo)
        return 0
    if len(trovate) > args.max:
        print("... altri %d risultati: restringi la ricerca, usa --max o --breve." % (len(trovate) - args.max))
    return 0


if __name__ == "__main__":
    sys.exit(main())
