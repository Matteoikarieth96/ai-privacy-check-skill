import contextlib
import io
import os
import re
import unittest

from helpers import ROOT

import fonti


def esegui(*args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        codice = fonti.main(list(args))
    return codice, buf.getvalue()


class FontiTest(unittest.TestCase):
    def test_cerca(self):
        codice, out = esegui("cerca", "615-ter")
        self.assertEqual(codice, 0)
        self.assertIn("URL: https://", out)

    def test_cerca_senza_risultati(self):
        codice, out = esegui("cerca", "stringa che non esiste nella base")
        self.assertEqual(codice, 0)
        self.assertIn("non verificata", out)

    def test_cerca_piu_parole_in_qualunque_ordine(self):
        codice, out = esegui("cerca", "zero conservazione", "--breve")
        self.assertEqual(codice, 0)
        self.assertIn("[ven-", out)

    def test_norma(self):
        codice, out = esegui("norma", "GDPR art. 28", "--breve", "--max", "50")
        self.assertIn("[eu-08]", out)
        self.assertNotIn("81/2008", out)
        codice, out = esegui("norma", "GDPR art. 9", "--breve", "--max", "50")
        self.assertIn("[eu-03]", out)
        self.assertNotIn("art. 96", out)

    def test_json_etichette_leggibili(self):
        import json
        codice, out = esegui("json", "it-34", "vl-27", "eu-08")
        etichette = {b["id"]: b["fonte"]["etichetta"] for b in json.loads(out)}
        self.assertEqual(etichette["it-34"], "L. 300/1970, art. 4, commi 1 e 2")
        self.assertFalse(etichette["vl-27"].startswith("Verifica"))
        self.assertIn("GDPR art. 28", etichette["eu-08"])

    def test_json_pronto_per_il_rapporto(self):
        import json
        codice, out = esegui("json", "eu-08", "it-31")
        blocchi = json.loads(out)
        self.assertEqual([b["id"] for b in blocchi], ["eu-08", "it-31"])
        self.assertEqual(blocchi[0]["fonte"]["stato"], "base")
        self.assertRegex(blocchi[0]["fonte"]["url"], r"^https://")

    def test_elenco_e_alias(self):
        for alias in ("commercialisti", "avvocati", "sanita", "fornitori"):
            codice, out = esegui("elenco", alias)
            self.assertEqual(codice, 0, alias)
            self.assertIn("##", out)
        codice, out = esegui("aperti", "commercialisti")
        self.assertEqual(codice, 0)
        self.assertIn("## prof", out)
        self.assertIn("## v2legal", out)
        codice, out = esegui("cerca", "whisper", "--dominio", "sanita", "--breve")
        self.assertIn("[au-", out)

    def test_id_citati_nei_riferimenti_esistono(self):
        import re
        base = fonti.carica()
        ids = {a["id"] for d in base["domini"] for a in d["affermazioni"]}
        for nome in os.listdir(os.path.join(ROOT, "references")):
            with open(os.path.join(ROOT, "references", nome), encoding="utf-8") as fh:
                for blocco in re.findall(r"\[((?:[a-z0-9]+-\d+)(?:, [a-z0-9]+-\d+)*)\]", fh.read()):
                    for cid in blocco.split(", "):
                        self.assertIn(cid, ids, "%s cita %s" % (nome, cid))

    def test_id(self):
        codice, out = esegui("id", "eu-28")
        self.assertEqual(codice, 0)
        self.assertIn("[eu-28]", out)

    def test_aperti_con_alias(self):
        codice, out = esegui("aperti", "sanita")
        self.assertEqual(codice, 0)
        self.assertIn("NON VERIFICATO", out)

    def test_base_ben_formata(self):
        base = fonti.carica()
        self.assertRegex(base["verificato_il"], r"^\d{4}-\d{2}-\d{2}$")
        ids = set()
        for d in base["domini"]:
            for a in d["affermazioni"]:
                self.assertRegex(a["url"], r"^https?://")
                self.assertIn(a["esito"], ("confermata", "corretta", "smentita", "non verificabile"))
                self.assertNotRegex(a["url"], r"[\s'\"<>]")
                self.assertNotIn(a["id"], ids)
                ids.add(a["id"])
        self.assertGreater(len(ids), 300)


class RepositoryPulitoTest(unittest.TestCase):
    """La base e' pubblica: niente percorsi locali ne' indirizzi email."""

    def test_nessun_residuo_di_lavoro_interno(self):
        # La base contiene solo fatti pubblici: niente rimandi a documenti interni o appunti di sessione.
        with open(os.path.join(ROOT, "data", "affermazioni.json"), encoding="utf-8") as fh:
            testo = fh.read()
        for parola in (r"\bmanuale\b", r"tool-results", r"WebFetch", r"tabella richiesta", r"clienti politici", r"cartella della sessione"):
            self.assertIsNone(re.search(parola, testo), parola)

    def test_nessun_percorso_locale_o_email(self):
        for cartella in ("data", "references", "templates", "examples"):
            for radice, _, files in os.walk(os.path.join(ROOT, cartella)):
                for nome in files:
                    with open(os.path.join(radice, nome), encoding="utf-8") as fh:
                        testo = fh.read()
                    self.assertNotRegex(testo, r"/Users/[A-Za-z]", nome)
                    self.assertNotRegex(testo, r"/private/tmp/", nome)
                    self.assertEqual(re.findall(r"[\w.+-]+@[\w-]+\.(?:com|it|org|net|eu)\b", testo), [], nome)


if __name__ == "__main__":
    unittest.main()
