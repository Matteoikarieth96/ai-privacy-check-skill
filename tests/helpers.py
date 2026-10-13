"""Supporto ai test: percorso degli script e copia dell'esempio inventato."""
import copy
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

ESEMPIO = os.path.join(ROOT, "examples", "fictional", "report.json")


def esempio():
    with open(ESEMPIO, encoding="utf-8") as fh:
        return copy.deepcopy(json.load(fh))
