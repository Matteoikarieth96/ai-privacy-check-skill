import os
import re
import subprocess
import sys
import tempfile
import unittest

from helpers import ESEMPIO, ROOT, esempio

import apc_lib


class PaginaTest(unittest.TestCase):
    def test_contenuto_ostile_viene_neutralizzato(self):
        r = esempio()
        r["meta"]["titolo"] = "<script>alert(1)</script>"
        r["righe"][0]["azione"] = "<img src=x onerror=alert(1)>"
        r["righe"][0]["nota"] = "<iframe src=x>"
        r["caso"]["descrizione"] = "\"><svg onload=alert(1)>"
        for pagina in (apc_lib.costruisci_html(r), apc_lib.costruisci_dettaglio(r)):
            self.assertNotIn("<script", pagina)
            self.assertNotIn("<img", pagina)
            self.assertNotIn("<svg", pagina)
            self.assertNotIn("<iframe", pagina)
            self.assertIn("&lt;script&gt;", pagina)

    def test_nessuna_risorsa_esterna(self):
        for pagina in (apc_lib.costruisci_html(esempio()), apc_lib.costruisci_dettaglio(esempio())):
            self.assertNotIn("<link", pagina)
            self.assertNotIn("<script", pagina)
            self.assertNotIn("src=", pagina)
            self.assertNotIn("@import", pagina)
            self.assertNotIn("url(", pagina)

    def test_solo_link_http(self):
        r = esempio()
        r["fonti"][0]["url"] = "javascript:alert(1)"
        r["righe"][0]["altre_fonti"][0]["url"] = "data:text/html,x"
        r["righe"][1]["fonte"]["url"] = "javascript:alert(2)"
        for pagina in (apc_lib.costruisci_html(r), apc_lib.costruisci_dettaglio(r)):
            self.assertIn("href=", pagina)
            for href in re.findall(r'href="([^"]*)"', pagina):
                self.assertTrue(href.startswith("http://") or href.startswith("https://"), href)

    def test_csp(self):
        for costruisci in (apc_lib.costruisci_html, apc_lib.costruisci_dettaglio):
            self.assertIn("Content-Security-Policy", costruisci(esempio()))
            self.assertNotIn("Content-Security-Policy", costruisci(esempio(), csp=False))

    def test_avviso_base_vecchia_in_pagina(self):
        r = esempio()
        self.assertNotIn('class="banner"', apc_lib.costruisci_html(r))
        r["meta"]["data"] = "2027-03-01"
        self.assertIn('class="banner"', apc_lib.costruisci_html(r))

    def test_rapporto_di_una_pagina(self):
        r = esempio()
        pagina = apc_lib.costruisci_html(r)
        for titolo in ("Si può", "Non si può", "Da fare", "Soluzione consigliata", "Punti aperti"):
            self.assertIn("<h2>%s</h2>" % titolo, pagina)
        self.assertLess(pagina.index("<h2>Si può</h2>"), pagina.index("<h2>Non si può</h2>"))
        self.assertLess(pagina.index("<h2>Non si può</h2>"), pagina.index("<h2>Da fare</h2>"))
        self.assertEqual(pagina.count("<li>"), len(r["righe"]) + apc_lib.APERTI_IN_PAGINA)
        for x in r["righe"]:
            self.assertIn(x["azione"].replace("'", "&#x27;"), pagina)
            self.assertIn(x["norme"][0], pagina)
        self.assertLess(pagina.index("Subito"), pagina.index("Prima di continuare"))
        self.assertLess(pagina.index("Prima di continuare"), pagina.index("Entro 30 giorni"))
        self.assertIn("Non basta per questi dati", pagina)
        self.assertIn("Altri 3 nel dettaglio", pagina)
        self.assertIn("size:A4", pagina)
        self.assertNotIn("<table", pagina)

    def test_azione_non_verificata_segnata_nel_rapporto(self):
        r = esempio()
        self.assertNotIn("da verificare", apc_lib.costruisci_html(r))
        r["righe"][2]["fonte"] = {"stato": "non_verificata"}
        self.assertIn("da verificare", apc_lib.costruisci_html(r))

    def test_allegato_di_dettaglio(self):
        pagina = apc_lib.costruisci_dettaglio(esempio())
        for titolo in ("Chi fa cosa", "Si può", "Non si può", "Da fare", "Soluzioni possibili", "Costi a listino", "Fonti", "Cosa si rischia"):
            self.assertIn("<h2>%s</h2>" % titolo, pagina)
        self.assertIn("Non basta per questi dati", pagina)
        self.assertIn("(da confermare)", pagina)
        self.assertIn("Dalla base del 13 ottobre 2026", pagina)
        self.assertNotIn("Cosa fare, in ordine", pagina)

    def test_sintesi_usabile(self):
        sintesi = apc_lib.costruisci_sintesi(esempio())
        self.assertNotIn(".;", sintesi)
        self.assertNotIn("..", sintesi)
        for titolo in ("Si può:", "Non si può:", "Da fare:"):
            self.assertIn(titolo, sintesi)
        self.assertIn("1. Subito: ", sintesi)

    def test_testo_completo(self):
        r = esempio()
        testo = apc_lib.costruisci_testo(r)
        self.assertNotIn("..", testo)
        for x in r["righe"]:
            self.assertIn(x["fonte"]["url"], testo)
        self.assertIn("NOTA: ", testo)
        self.assertIn("PRO: ", testo)
        self.assertIn("CONTRO: ", testo)

    def test_dichiara_che_non_e_un_parere(self):
        self.assertIn("Non è un parere legale", apc_lib.costruisci_html(esempio()))
        self.assertIn("Non è un parere legale", apc_lib.costruisci_dettaglio(esempio()))
        self.assertIn("Non è un parere legale", apc_lib.costruisci_sintesi(esempio()))


class ScriptTest(unittest.TestCase):
    def run_build(self, *args):
        return subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build_report.py")] + list(args),
                              capture_output=True, text=True)

    def test_costruisce_esempio(self):
        with tempfile.TemporaryDirectory() as tmp:
            res = self.run_build(ESEMPIO, "--out-dir", os.path.join(tmp, "out"))
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
            for nome in ("ai-privacy-check.html", "dettaglio.html", "sintesi.md", "pagina.txt"):
                self.assertTrue(os.path.exists(os.path.join(tmp, "out", nome)), nome)
            with open(os.path.join(tmp, "out", "pagina.txt"), encoding="utf-8") as fh:
                testo = fh.read()
            self.assertIn("NON SI PUÒ", testo)
            self.assertIn("PUNTI APERTI", testo)

    def test_non_scrive_su_collegamento_simbolico(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "out")
            os.makedirs(out)
            bersaglio = os.path.join(tmp, "bersaglio.txt")
            with open(bersaglio, "w") as fh:
                fh.write("intatto")
            os.symlink(bersaglio, os.path.join(out, "ai-privacy-check.html"))
            res = self.run_build(ESEMPIO, "--out-dir", out)
            self.assertEqual(res.returncode, 1)
            with open(bersaglio) as fh:
                self.assertEqual(fh.read(), "intatto")

    def test_collegamento_fisico_non_seguito_e_permessi(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "out")
            os.makedirs(out)
            bersaglio = os.path.join(tmp, "bersaglio.txt")
            with open(bersaglio, "w") as fh:
                fh.write("intatto")
            os.link(bersaglio, os.path.join(out, "pagina.txt"))
            res = self.run_build(ESEMPIO, "--out-dir", out)
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
            with open(bersaglio) as fh:
                self.assertEqual(fh.read(), "intatto")
            for nome in ("ai-privacy-check.html", "dettaglio.html", "sintesi.md", "pagina.txt"):
                self.assertEqual(os.stat(os.path.join(out, nome)).st_mode & 0o777, 0o600, nome)
            self.assertEqual([n for n in os.listdir(out) if n.startswith(".apc-")], [])

    def test_out_dir_vuota_rifiutata(self):
        with tempfile.TemporaryDirectory() as tmp:
            res = subprocess.run([sys.executable, "-B", os.path.join(ROOT, "scripts", "build_report.py"), ESEMPIO, "--out-dir", ""],
                                 capture_output=True, text=True, cwd=tmp)
            self.assertEqual(res.returncode, 1)
            self.assertEqual(os.listdir(tmp), [])

    def test_fonte_non_verificata_non_diventa_un_link(self):
        r = esempio()
        r["righe"][0]["fonte"] = {"stato": "non_verificata", "url": "https://esempio.eu/non-letta"}
        r["righe"][0]["altre_fonti"] = []
        for pagina in (apc_lib.costruisci_html(r), apc_lib.costruisci_dettaglio(r), apc_lib.costruisci_testo(r)):
            self.assertNotIn("esempio.eu/non-letta", pagina)

    def test_soluzione_consigliata_solo_se_true(self):
        r = esempio()
        non_basta = next(s for s in r["setup"] if s.get("regge") is False)
        non_basta["consigliato"] = 1
        r["setup"].sort(key=lambda s: s is not non_basta)
        self.assertNotIn("Soluzione consigliata: " + non_basta["nome"], apc_lib.costruisci_sintesi(r))

    def test_report_non_valido_non_costruisce(self):
        with tempfile.TemporaryDirectory() as tmp:
            rotto = os.path.join(tmp, "report.json")
            with open(rotto, "w") as fh:
                fh.write("{}")
            res = self.run_build(rotto, "--out-dir", os.path.join(tmp, "out"))
            self.assertEqual(res.returncode, 1)
            self.assertFalse(os.path.exists(os.path.join(tmp, "out")))

    def test_pagina_di_esempio_aggiornata(self):
        attesi = (("ai-privacy-check.html", apc_lib.costruisci_html), ("dettaglio.html", apc_lib.costruisci_dettaglio),
                  ("sintesi.md", apc_lib.costruisci_sintesi), ("pagina.txt", apc_lib.costruisci_testo))
        for nome, costruisci in attesi:
            with open(os.path.join(ROOT, "examples", "fictional", "out", nome), encoding="utf-8") as fh:
                self.assertEqual(fh.read(), costruisci(esempio()), nome)


if __name__ == "__main__":
    unittest.main()
