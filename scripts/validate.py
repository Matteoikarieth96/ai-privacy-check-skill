#!/usr/bin/env python3
"""Controlla un report.json prima di costruire la pagina.

Uso: python3 validate.py report.json
Esce con 1 se ci sono errori. Gli avvisi non bloccano.
"""
import sys

from apc_lib import carica_json, valida


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip())
        return 2
    try:
        report = carica_json(argv[1])
    except (OSError, ValueError, RecursionError) as exc:
        print("ERRORE: non riesco a leggere %s: %s" % (argv[1], type(exc).__name__ if isinstance(exc, RecursionError) else exc))
        return 1
    errori, avvisi = valida(report)
    for a in avvisi:
        print("AVVISO: " + a)
    for err in errori:
        print("ERRORE: " + err)
    if errori:
        print("%d errori. Correggi i campi indicati e riprova." % len(errori))
        return 1
    print("OK: report valido (%d avvisi)." % len(avvisi))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
