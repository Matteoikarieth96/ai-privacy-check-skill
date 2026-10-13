#!/usr/bin/env python3
"""Calcola i costi mensili a listino per un caso.

Uso:
  python3 costi.py --persone 5 --token-in 20 --token-out 4
  python3 costi.py --persone 6 --pagine-in 8000 --pagine-out 1500 --solo-delicati
  python3 costi.py --minuti-audio 9000 --solo-delicati
  python3 costi.py --persone 3 --token-in 20 --token-out 2 --prezzo "Modello X su provider Y|0.50|1.50|EUR|https://esempio.eu/prezzi"
  python3 costi.py --elenco

--token-in e --token-out sono milioni di token al mese, per le voci a consumo.
--pagine-in e --pagine-out sono pagine di testo al mese: vengono convertite in token con la stima
  scritta in data/listini.json. È una stima: dichiarala nel rapporto.
--minuti-audio sono minuti di registrazione al mese, per le voci di trascrizione.
--prezzo aggiunge una voce a consumo con un prezzo letto oggi: nome|ingresso|uscita|valuta|indirizzo.
I prezzi vengono da data/listini.json, con la data di lettura: vanno riaperti prima di citarli.
"""
import argparse
import json
import math
import os
import re
import sys

LISTINI = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "listini.json")
SIMBOLO = {"USD": "$", "EUR": "€"}


def carica(path=LISTINI):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def num(valore):
    """Numero in formato italiano, senza zeri inutili."""
    if valore == int(valore):
        testo = str(int(valore))
    elif abs(valore) < 0.1:
        testo = ("%.5f" % valore).rstrip("0")
    else:
        testo = "%.2f" % valore
    return testo.replace(".", ",")


def costo_mensile(voce, persone, token_in, token_out, listini, minuti_audio=0.0):
    """Restituisce (importo mensile, spiegazione). None se la voce non si applica ai volumi dati."""
    tipo = voce["tipo"]
    if tipo == "posto":
        return voce["prezzo"] * persone, "%d posti a %s" % (persone, num(voce["prezzo"]))
    if tipo == "api":
        return voce["in"] * token_in + voce["out"] * token_out, "%s milioni di token in ingresso e %s in uscita" % (num(token_in), num(token_out))
    if tipo == "audio":
        return voce["prezzo_minuto"] * minuti_audio, "%s minuti di audio a %s al minuto" % (num(minuti_audio), num(voce["prezzo_minuto"]))
    if tipo == "mensile":
        return voce["prezzo"], "canone, più %s di attivazione" % num(voce.get("attivazione", 0))
    if tipo == "una_tantum":
        mesi = listini["mesi_ammortamento"]
        energia = voce.get("watt_medi", 0) / 1000 * 24 * 365 / 12 * listini["energia_eur_kwh"]
        return voce["prezzo"] / mesi + energia, "%s senza IVA su %d mesi, più energia per %d W medi" % (num(voce["prezzo"]), mesi, voce.get("watt_medi", 0))
    raise ValueError("tipo di voce sconosciuto: %s" % tipo)


def formatta(importo, valuta):
    return "%s %s" % (("%.2f" % importo).replace(".", ","), SIMBOLO.get(valuta, valuta))


def quantita(testo):
    """Un numero finito e non negativo, con virgola o punto."""
    try:
        valore = float(str(testo).replace(",", "."))
    except ValueError:
        raise argparse.ArgumentTypeError("serve un numero, non \"%s\"" % str(testo)[:20])
    if not math.isfinite(valore) or valore < 0 or valore > 1e12:
        raise argparse.ArgumentTypeError("serve un numero finito, non negativo e ragionevole")
    return valore


def voce_libera(testo):
    parti = [p.strip() for p in testo.split("|")]
    if len(parti) != 5:
        raise ValueError("--prezzo vuole cinque parti separate da |: nome|ingresso|uscita|valuta|indirizzo")
    nome, pin, pout, valuta, url = parti
    nome = re.sub(r"[\x00-\x1f\x7f-\x9f]", " ", nome)[:80].strip()
    if not nome:
        raise ValueError("--prezzo: manca il nome")
    if len(url) > 600 or not re.fullmatch(r"https?://[^\s<>\"'\\@]+", url):
        raise ValueError("--prezzo: l'indirizzo deve cominciare con http o https")
    if valuta not in SIMBOLO:
        raise ValueError("--prezzo: valuta EUR o USD")
    try:
        pin, pout = quantita(pin), quantita(pout)
    except argparse.ArgumentTypeError as exc:
        raise ValueError("--prezzo: %s" % exc)
    return {"id": "prezzo-di-oggi", "nome": nome, "tipo": "api", "in": pin, "out": pout,
            "valuta": valuta, "nota": "Prezzo letto oggi, non dal listino incluso.", "dati_delicati": None, "fonte": url, "letto_oggi": True}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Costi a listino per ai-privacy-check")
    parser.add_argument("--persone", type=int, default=1)
    parser.add_argument("--token-in", type=quantita, default=0.0)
    parser.add_argument("--token-out", type=quantita, default=0.0)
    parser.add_argument("--pagine-in", type=quantita, default=0.0)
    parser.add_argument("--pagine-out", type=quantita, default=0.0)
    parser.add_argument("--token-per-pagina", type=quantita)
    parser.add_argument("--minuti-audio", type=quantita, default=0.0)
    parser.add_argument("--solo", help="id separati da virgola")
    parser.add_argument("--solo-delicati", action="store_true", help="solo le voci adatte a dati delicati")
    parser.add_argument("--prezzo", action="append", default=[], help="nome|ingresso|uscita|valuta|indirizzo")
    parser.add_argument("--elenco", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.persone < 1 or min(args.token_in, args.token_out, args.pagine_in, args.pagine_out, args.minuti_audio) < 0:
        print("ERRORE: persone almeno 1, volumi non negativi")
        return 1

    listini = carica()
    voci = list(listini["voci"])
    if args.elenco:
        for v in voci:
            print("%-22s %-11s %-3s %s" % (v["id"], v["tipo"], "sì" if v.get("dati_delicati") else "no", v["nome"]))
        print("Colonne: id, tipo, adatto a dati delicati, nome.")
        return 0

    stime = listini.get("stime", {})
    token_in, token_out, ipotesi = args.token_in, args.token_out, []
    if args.pagine_in or args.pagine_out:
        tpp = args.token_per_pagina or stime.get("token_per_pagina")
        if not tpp:
            print("ERRORE: per convertire le pagine serve --token-per-pagina (il listino non ha una stima)")
            return 1
        token_in += args.pagine_in * tpp / 1e6
        token_out += args.pagine_out * tpp / 1e6
        ipotesi.append("%s pagine lette e %s scritte al mese, a %s token per pagina (stima)" % (num(args.pagine_in), num(args.pagine_out), num(tpp)))
    if token_in or token_out:
        ipotesi.append("%s milioni di token in ingresso e %s in uscita al mese" % (num(token_in), num(token_out)))
    if args.minuti_audio:
        ipotesi.append("%s minuti di audio al mese" % num(args.minuti_audio))

    try:
        voci += [voce_libera(p) for p in args.prezzo]
    except ValueError as exc:
        print("ERRORE: %s" % exc)
        return 1
    if args.solo:
        scelti = [s.strip() for s in args.solo.split(",") if s.strip()]
        sconosciuti = [s for s in scelti if s not in {v["id"] for v in voci}]
        if sconosciuti:
            print("ERRORE: voci sconosciute: %s. Usa --elenco." % ", ".join(sconosciuti))
            return 1
        voci = [v for v in voci if v["id"] in scelti or v.get("letto_oggi")]
    if args.solo_delicati:
        voci = [v for v in voci if v.get("dati_delicati") or v.get("letto_oggi")]

    righe = []
    for v in voci:
        if v["tipo"] == "audio" and not args.minuti_audio:
            continue
        if v["tipo"] == "api" and not (token_in or token_out):
            continue
        importo, come = costo_mensile(v, args.persone, token_in, token_out, listini, args.minuti_audio)
        righe.append({"id": v["id"], "voce": v["nome"], "importo_mensile": round(importo, 2), "valuta": v["valuta"],
                      "importo": formatta(importo, v["valuta"]) + " al mese", "come": come, "nota": v.get("nota", ""),
                      "adatto_a_dati_delicati": v.get("dati_delicati"), "per_lavoro": v.get("per_lavoro", True),
                      "fonte": v["fonte"], "letto_il": "oggi" if v.get("letto_oggi") else listini["letto_il"]})
    if args.json:
        print(json.dumps({"letto_il": listini["letto_il"], "avvertenza": listini["avvertenza"], "ipotesi": ipotesi, "righe": righe}, ensure_ascii=False, indent=1, allow_nan=False))
        return 0
    print("Costi mensili a listino, letti il %s. %s" % (listini["letto_il"], listini["avvertenza"]))
    if ipotesi:
        print("Ipotesi: " + "; ".join(ipotesi) + ".")
    for r in righe:
        delicati = {True: "adatto a dati delicati", False: "NON per dati delicati", None: "idoneità ai dati delicati da verificare"}[r["adatto_a_dati_delicati"]]
        lavoro = "" if r["per_lavoro"] else " NON per uso professionale."
        print("- %s: %s (%s). %s.%s %s" % (r["voce"], r["importo"], r["come"], delicati, lavoro, r["nota"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
