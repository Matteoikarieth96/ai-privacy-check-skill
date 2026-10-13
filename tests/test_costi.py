import json
import os
import subprocess
import sys
import unittest

from helpers import ROOT

import costi


class CostiTest(unittest.TestCase):
    def setUp(self):
        self.listini = costi.carica()
        self.voci = {v["id"]: v for v in self.listini["voci"]}

    def costo(self, vid, persone=5, tin=20, tout=4):
        return costi.costo_mensile(self.voci[vid], persone, tin, tout, self.listini)[0]

    def test_posti(self):
        self.assertAlmostEqual(self.costo("claude-team"), 125.0)
        self.assertAlmostEqual(self.costo("workspace-standard", persone=20), 272.0)

    def test_api(self):
        self.assertAlmostEqual(self.costo("api-sonnet-ue"), 88.0)
        self.assertAlmostEqual(self.costo("api-open-ovh"), 3.2)
        self.assertAlmostEqual(self.costo("api-haiku", tin=100, tout=20), 20.0)

    def test_una_tantum_con_energia(self):
        self.assertAlmostEqual(self.costo("mac-studio-128"), 4843 / 36 + 0.1 * 730 * 0.3887, places=2)

    def test_canone(self):
        self.assertAlmostEqual(self.costo("hetzner-gex63"), 999.0)

    def test_ogni_voce_ha_fonte_e_tipo(self):
        for v in self.listini["voci"]:
            self.assertRegex(v["fonte"], r"^https://")
            self.assertIn(v["tipo"], ("posto", "api", "audio", "mensile", "una_tantum"))
            costi.costo_mensile(v, 3, 1, 1, self.listini, 60)

    def test_llama_con_italiano_dichiarato(self):
        self.assertAlmostEqual(self.costo("api-llama33-ionos"), 15.6)

    def run_cli(self, *args):
        script = os.path.join(ROOT, "scripts", "costi.py")
        return subprocess.run([sys.executable, "-B", script] + list(args), capture_output=True, text=True)

    def test_prezzo_letto_oggi(self):
        res = self.run_cli("--token-in", "20", "--token-out", "4", "--solo", "api-open-ovh", "--json",
                           "--prezzo", "Modello di prova|0,5|1,5|EUR|https://example.eu/prezzi")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        righe = {r["id"]: r for r in json.loads(res.stdout)["righe"]}
        self.assertEqual(righe["prezzo-di-oggi"]["importo_mensile"], 16.0)
        self.assertEqual(righe["prezzo-di-oggi"]["letto_il"], "oggi")
        res = self.run_cli("--token-in", "1", "--prezzo", "X|1|1|EUR|javascript:alert(1)")
        self.assertEqual(res.returncode, 1)

    def test_pagine_convertite_in_token(self):
        res = self.run_cli("--pagine-in", "10000", "--pagine-out", "2000", "--token-per-pagina", "1000", "--solo", "api-open-ovh", "--json")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        dati = json.loads(res.stdout)
        self.assertAlmostEqual(dati["righe"][0]["importo_mensile"], 10 * 0.08 + 2 * 0.40)
        self.assertIn("stima", dati["ipotesi"][0])

    def test_trascrizione_al_minuto(self):
        self.assertAlmostEqual(costi.costo_mensile(self.voci["audio-scaleway"], 1, 0, 0, self.listini, 9000)[0], 27.0)
        res = self.run_cli("--minuti-audio", "9000", "--solo", "audio-scaleway,api-open-ovh")
        self.assertIn("27,00 €", res.stdout)
        self.assertIn("0,003 al minuto", res.stdout)
        self.assertNotIn("gpt-oss", res.stdout)

    def test_stima_token_per_pagina_dichiarata(self):
        self.assertEqual(self.listini["stime"]["token_per_pagina"], 2000)
        res = self.run_cli("--pagine-in", "1000", "--solo", "api-open-ovh")
        self.assertIn("(stima)", res.stdout)

    def test_solo_delicati_e_testo(self):
        res = self.run_cli("--persone", "5", "--token-in", "20", "--token-out", "4", "--solo-delicati")
        self.assertEqual(res.returncode, 0)
        self.assertNotIn("Claude Team", res.stdout)
        self.assertIn("adatto a dati delicati", res.stdout)
        res = self.run_cli("--persone", "5", "--solo", "claude-pro")
        self.assertIn("NON per uso professionale", res.stdout)

    def test_numeri_non_validi_rifiutati_senza_traccia(self):
        for args in (["--token-in", "nan"], ["--token-in", "inf"], ["--minuti-audio", "inf"], ["--token-in=-1"],
                     ["--pagine-in", "1000", "--token-per-pagina=-2000"]):
            res = self.run_cli(*args)
            self.assertNotEqual(res.returncode, 0, args)
            self.assertNotIn("Traceback", res.stderr, args)
        for prezzo in ("X|-5|-5|EUR|https://esempio.eu/p", "X|nan|nan|EUR|https://esempio.eu/p", "X|inf|1|EUR|https://esempio.eu/p",
                       "X|1|1|EUR|https://utente@esempio.eu/p"):
            res = self.run_cli("--token-in", "1", "--prezzo", prezzo, "--json")
            self.assertEqual(res.returncode, 1, prezzo)
            self.assertNotIn("NaN", res.stdout)
        res = self.run_cli("--token-in", "1", "--solo", "api-open-ovh", "--prezzo", "Nome\x1b[2J\nfinto|1|1|EUR|https://esempio.eu/p")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertNotIn("\x1b", res.stdout)

    def test_riga_di_comando(self):
        script = os.path.join(ROOT, "scripts", "costi.py")
        res = subprocess.run([sys.executable, script, "--persone", "5", "--token-in", "20", "--token-out", "4", "--solo", "claude-team", "--json"],
                             capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertEqual(json.loads(res.stdout)["righe"][0]["importo_mensile"], 125.0)
        res = subprocess.run([sys.executable, script, "--solo", "non-esiste"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 1)


if __name__ == "__main__":
    unittest.main()
