#!/usr/bin/env python3
"""Costruisce il rapporto di una pagina, l'allegato, la sintesi e la versione in testo da un report.json valido.

Uso: python3 build_report.py report.json --out-dir out [--no-csp] [--testo]

Scrive quattro file nella cartella di uscita:
  ai-privacy-check.html   il rapporto di una pagina: si può, non si può, da fare. Si stampa su un foglio A4
  dettaglio.html          l'allegato: ruoli, nota e fonte di ogni azione, alternative, costi, fonti con link
  sintesi.md              le stesse voci del rapporto, da riportare in chat
  pagina.txt              rapporto e allegato in testo semplice, per rileggerli senza un browser

Le due pagine sono autonome: nessuno script e nessuna richiesta esterna.
--testo stampa anche pagina.txt a schermo.
--no-csp toglie l'intestazione Content-Security-Policy, utile solo per pubblicare le pagine
dentro un visualizzatore che ne imposta una propria.
"""
import argparse
import os
import sys

from apc_lib import carica_json, costruisci_dettaglio, costruisci_html, costruisci_sintesi, costruisci_testo, scrivi_sicuro, valida


def main(argv=None):
    parser = argparse.ArgumentParser(description="Costruisce il rapporto di ai-privacy-check")
    parser.add_argument("report")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--no-csp", action="store_true")
    parser.add_argument("--testo", action="store_true")
    args = parser.parse_args(argv)

    if not args.out_dir.strip():
        print("ERRORE: --out-dir è vuoto. Indica la cartella di lavoro del caso")
        return 1
    try:
        report = carica_json(args.report)
    except (OSError, ValueError, RecursionError) as exc:
        print("ERRORE: non riesco a leggere %s: %s" % (args.report, type(exc).__name__ if isinstance(exc, RecursionError) else exc))
        return 1
    errori, avvisi = valida(report)
    if errori:
        for err in errori:
            print("ERRORE: " + err)
        print("Il report non è valido: il rapporto non viene costruito.")
        return 1
    for a in avvisi:
        print("AVVISO: " + a)

    out_dir = os.path.abspath(args.out_dir)
    if os.path.islink(out_dir):
        print("ERRORE: la cartella di uscita è un collegamento simbolico")
        return 1
    # Prima si costruisce tutto in memoria, poi si scrive: un errore a metà non lascia file misti.
    try:
        testo = costruisci_testo(report)
        uscite = (("ai-privacy-check.html", costruisci_html(report, csp=not args.no_csp)),
                  ("dettaglio.html", costruisci_dettaglio(report, csp=not args.no_csp)),
                  ("sintesi.md", costruisci_sintesi(report)),
                  ("pagina.txt", testo))
        for _, contenuto in uscite:
            contenuto.encode("utf-8")
    except Exception as exc:
        print("ERRORE: non riesco a costruire il rapporto (%s). Nessun file scritto." % type(exc).__name__)
        return 1
    try:
        os.makedirs(out_dir, mode=0o700, exist_ok=True)
        for nome, contenuto in uscite:
            scrivi_sicuro(os.path.join(out_dir, nome), contenuto)
    except (OSError, ValueError) as exc:
        print("ERRORE: %s" % exc)
        return 1
    for nome, _ in uscite:
        print("Scritto: %s" % os.path.join(out_dir, nome))
    if args.testo:
        print()
        print(testo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
