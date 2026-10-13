import unittest

from helpers import esempio

import apc_lib


class ValidaTest(unittest.TestCase):
    def errori(self, report):
        return apc_lib.valida(report)[0]

    def senza_norma(self, r, frammento):
        for x in r["righe"]:
            x["norme"] = [n for n in x["norme"] if frammento not in n] or ["Regola interna"]
        return r

    def test_esempio_valido(self):
        errori, avvisi = apc_lib.valida(esempio())
        self.assertEqual(errori, [])
        self.assertEqual(avvisi, [])

    def test_livello_non_si_abbassa(self):
        r = esempio()
        r["attenzione"]["livello"] = "media"
        self.assertTrue(any("livello minimo" in e for e in self.errori(r)))

    def test_livello_minimo(self):
        vuoti = {k: False for k in apc_lib.SEGNALI}
        self.assertEqual(apc_lib.livello_minimo(vuoti), "bassa")
        for k in apc_lib.SEGNALI_MEDIA:
            self.assertEqual(apc_lib.livello_minimo(dict(vuoti, **{k: True})), "media")
        for k in apc_lib.SEGNALI_ALTA:
            self.assertEqual(apc_lib.livello_minimo(dict(vuoti, **{k: True})), "alta")

    def test_copertura_portali(self):
        r = self.senza_norma(esempio(), "615-ter")
        self.assertTrue(any("portali_di_terzi" in e for e in self.errori(r)))

    def test_copertura_dati_particolari_chiede_dpia(self):
        r = self.senza_norma(esempio(), "GDPR art. 35")
        self.assertTrue(any("GDPR art. 35" in e for e in self.errori(r)))

    def test_copertura_non_si_inganna_con_un_altro_atto(self):
        # "c.p.c. art. 96" non vale come GDPR art. 9, "Codice deontologico art. 28" non vale come GDPR art. 28
        r = self.senza_norma(self.senza_norma(esempio(), "GDPR art. 9"), "GDPR art. 28")
        r["righe"][0]["norme"] += ["c.p.c. art. 96", "AI Act art. 99", "Codice deontologico forense art. 28", "GDPR art. 30(9)"]
        errori = self.errori(r)
        self.assertTrue(any("GDPR art. 9" in e for e in errori))
        self.assertTrue(any("GDPR art. 28" in e for e in errori))

    def test_copertura_riconosce_le_forme_usate_nella_base(self):
        for norma, atto, numero in (("GDPR art. 9(2)(h), 9(3)", "GDPR", "9"), ("GDPR art. 28(2), 28(4)", "GDPR", "28"),
                                    ("GDPR art. 44-46", "GDPR", "4[4-9]"), ("L. 132/2025 art. 7 c. 3, 5", "L. 132/2025", "7"),
                                    ("L. 132/2025 art. 7, 11, 13", "L. 132/2025", "13")):
            self.assertTrue(apc_lib._atto_art(atto, numero).search(norma), norma)
        self.assertFalse(apc_lib._atto_art("L. 132/2025", "4").search("L. 132/2025 art. 13 c. 4"))
        self.assertFalse(apc_lib._atto_art("GDPR", "10").search("GDPR art. 28(10)"))

    def test_settore_chiede_la_norma_giusta(self):
        r = self.senza_norma(esempio(), "L. 132/2025 art. 13")
        r["righe"][0]["norme"].append("L. 132/2025 art. 11")
        self.assertTrue(any("L. 132/2025 art. 13" in e for e in self.errori(r)))
        r = esempio()
        r["meta"]["settore"] = "sanita"
        self.assertTrue(any("L. 132/2025 art. 7" in e for e in self.errori(r)))

    def test_ia_che_parla_con_le_persone(self):
        r = esempio()
        r["segnali"]["dialoga_con_persone"] = True
        self.assertTrue(any("AI Act art. 50" in e for e in self.errori(r)))
        r["righe"][0]["norme"].append("AI Act art. 50")
        self.assertEqual(self.errori(r), [])

    def test_frase_vietata(self):
        r = esempio()
        r["righe"][0]["azione"] = "Caricare pure i file: sono dati anonimi"
        self.assertTrue(any("dati anonimi" in e for e in self.errori(r)))

    def test_affermazioni_di_conformita(self):
        for frase in ("Lo studio è conforme e a norma.", "Con questo siete a posto.", "Il sistema risulta in regola."):
            r = esempio()
            r["righe"][0]["nota"] = frase
            self.assertTrue(any("non affermare" in e for e in self.errori(r)), frase)
        r = esempio()
        r["righe"][0]["nota"] = "Oggi lo studio non è conforme: mancano i contratti."
        self.assertEqual(self.errori(r), [])

    def test_frase_vietata_tra_virgolette_ammessa(self):
        r = esempio()
        r["righe"][0]["nota"] = "Scrivi \"dati di esempio\", mai \"dati anonimi\" o \"siamo a norma\"."
        self.assertEqual(self.errori(r), [])

    def test_trattino_lungo(self):
        r = esempio()
        r["caso"]["descrizione"] += " Uno studio — piccolo."
        self.assertTrue(any("trattino lungo" in e for e in self.errori(r)))

    def test_url_non_http(self):
        r = esempio()
        r["righe"][0]["fonte"]["url"] = "javascript:alert(1)"
        r["fonti"][0]["url"] = "file:///etc/passwd"
        errori = self.errori(r)
        self.assertTrue(any("righe[0].fonte.url" in e for e in errori))
        self.assertTrue(any("fonti[0].url" in e for e in errori))

    def test_indirizzo_inventato_con_stato_base(self):
        r = esempio()
        r["righe"][1]["fonte"]["url"] = "https://example.com/inventato"
        self.assertTrue(any("non è nella base" in e for e in self.errori(r)))
        r["righe"][1]["fonte"].update(stato="ricontrollata", data=r["meta"]["data"])
        self.assertEqual(self.errori(r), [])

    def test_date_delle_fonti(self):
        r = esempio()
        r["righe"][1]["fonte"]["data"] = "2026-01-01"
        self.assertTrue(any("la data deve essere" in e for e in self.errori(r)))

    def test_riga_non_verificata_va_tra_i_punti_aperti(self):
        r = esempio()
        r["righe"][-1]["fonte"] = {"stato": "non_verificata"}
        self.assertEqual(self.errori(r), [])
        r["aperti"] = []
        errori = self.errori(r)
        self.assertTrue(any("non verificate" in e for e in errori))
        self.assertTrue(any("senza ricontrollo online" in e for e in errori))

    def test_numero_di_righe_e_soluzioni(self):
        r = esempio()
        r["righe"] = r["righe"][:5]
        self.assertTrue(any("da 6 a 14 azioni" in e for e in self.errori(r)))
        r = esempio()
        r["righe"] = r["righe"] + r["righe"]
        self.assertTrue(any("da 6 a 14 azioni" in e for e in self.errori(r)))
        r = esempio()
        r["setup"] = r["setup"][:1]
        self.assertTrue(any("da 2 a 4 soluzioni" in e for e in self.errori(r)))

    def test_un_solo_consigliato_e_deve_reggere(self):
        r = esempio()
        for s in r["setup"]:
            s["consigliato"] = True
        self.assertTrue(any("una e una sola" in e for e in self.errori(r)))
        r = esempio()
        for s in r["setup"]:
            if s.get("consigliato"):
                s["regge"] = False
        self.assertTrue(any("non regge" in e for e in self.errori(r)))

    def test_gia_in_uso_chiede_una_riga_subito(self):
        r = esempio()
        for x in r["righe"]:
            if x.get("quando") == "subito":
                x["quando"] = "prima"
        self.assertTrue(any("già in uso" in e for e in self.errori(r)))
        r["caso"]["gia_in_uso"] = False
        self.assertEqual(self.errori(r), [])

    def test_tipi_di_azione(self):
        r = esempio()
        r["righe"][0]["tipo"] = "consiglio"
        self.assertTrue(any("righe[0].tipo" in e for e in self.errori(r)))
        r = esempio()
        r["righe"] = [x for x in r["righe"] if x["tipo"] != "si_puo"]
        self.assertTrue(any("si_puo" in e for e in self.errori(r)))
        r = esempio()
        r["righe"] = [x for x in r["righe"] if x["tipo"] != "non_si_puo"]
        self.assertTrue(any("non_si_puo" in e for e in self.errori(r)))
        r = esempio()
        fare = [x for x in r["righe"] if x["tipo"] == "da_fare"]
        r["righe"] = [x for x in r["righe"] if x["tipo"] != "da_fare"] + fare[:1]
        self.assertTrue(any("almeno 2 azioni" in e for e in self.errori(r)))

    def test_quando_solo_per_le_azioni_da_fare(self):
        r = esempio()
        r["righe"][0]["quando"] = "prima"
        self.assertTrue(any("righe[0].quando" in e for e in self.errori(r)))
        r = esempio()
        fare = next(x for x in r["righe"] if x["tipo"] == "da_fare")
        del fare["quando"]
        self.assertTrue(any(".quando: usa uno tra" in e for e in self.errori(r)))

    def test_limiti_per_stare_in_una_pagina(self):
        r = esempio()
        r["righe"][0]["azione"] = "x" * (apc_lib.AZIONE_MAX + 1)
        self.assertTrue(any("righe[0].azione" in e for e in self.errori(r)))
        r = esempio()
        da_fare = [x for x in r["righe"] if x["tipo"] == "da_fare"]
        r["righe"] = [x for x in r["righe"] if x["tipo"] == "si_puo"][:1] + [x for x in r["righe"] if x["tipo"] == "non_si_puo"][:1] + da_fare + da_fare[:1]
        self.assertTrue(any("il massimo è 7" in e for e in self.errori(r)))
        r = esempio()
        r["caso"]["descrizione"] = "x" * (apc_lib.DESCRIZIONE_MAX + 1)
        r["aperti"][1] = "x" * (apc_lib.APERTO_MAX + 1)
        r["attenzione"]["motivi"] = ["uno", "due", "tre", "quattro"]
        errori = self.errori(r)
        self.assertTrue(any("caso.descrizione" in e for e in errori))
        self.assertTrue(any("aperti[1]" in e for e in errori))
        self.assertTrue(any("attenzione.motivi" in e for e in errori))
        r = esempio()
        scelta = next(x for x in r["setup"] if x.get("consigliato"))
        scelta["per_cosa"] = "x" * (apc_lib.SCELTA_MAX["per_cosa"] + 1)
        self.assertTrue(any(".per_cosa" in e for e in self.errori(r)))

    def test_formato_vecchio_spiegato(self):
        r = esempio()
        r["righe"][0] = {"problema": "Un problema.", "cosa_fare": "Fai qualcosa.", "norme": ["GDPR art. 28"], "quando": "prima",
                         "fonte": {"stato": "non_verificata"}}
        self.assertTrue(any("formato a azioni" in e for e in self.errori(r)))

    def test_passi_facoltativi(self):
        r = esempio()
        self.assertNotIn("passi", r)
        r["passi"] = ["Primo passo.", "Secondo passo."]
        self.assertEqual(self.errori(r), [])
        r["passi"] = "tutto insieme"
        self.assertTrue(any("passi" in e for e in self.errori(r)))

    def test_segnali(self):
        r = esempio()
        del r["segnali"]["minori"]
        self.assertTrue(any("segnali.minori" in e for e in self.errori(r)))
        r = esempio()
        r["segnali_da_confermare"] = ["minori"]
        self.assertTrue(any("segnali_da_confermare" in e for e in self.errori(r)))

    def test_titolare_richiesto(self):
        r = esempio()
        r["ruoli"] = [x for x in r["ruoli"] if "titolare" not in x["ruolo"]]
        self.assertTrue(any("titolare" in e for e in self.errori(r)))

    def test_fonti_extra_facoltative(self):
        r = esempio()
        del r["fonti"]
        self.assertEqual(self.errori(r), [])
        urls = [f["url"] for f in apc_lib.elenco_fonti(r)]
        self.assertEqual(len(urls), len(set(urls)))
        self.assertGreaterEqual(len(urls), 8)

    def test_avviso_base_vecchia(self):
        r = esempio()
        r["meta"]["data"] = "2027-03-01"
        errori, avvisi = apc_lib.valida(r)
        self.assertEqual(errori, [])
        self.assertTrue(any("90 giorni" in a for a in avvisi))

    def test_non_un_oggetto(self):
        self.assertTrue(self.errori([]))


class RobustezzaTest(unittest.TestCase):
    """Regressioni dalla revisione di sicurezza: input ostili o malformati."""

    def errori(self, report):
        return apc_lib.valida(report)[0]

    def test_testi_lunghi_rifiutati_prima_delle_espressioni_regolari(self):
        import time
        r = esempio()
        r["righe"][0]["norme"].insert(0, "GDPR art. " * 1200)
        r["caso"]["obiettivi"].append("«" * 160000)
        inizio = time.time()
        errori = self.errori(r)
        self.assertLess(time.time() - inizio, 2)
        self.assertTrue(any("il massimo per qualunque campo" in e for e in errori))
        r = esempio()
        r["righe"][0]["norme"].insert(0, "GDPR art. " * 150)
        inizio = time.time()
        self.assertTrue(any("norme: ogni norma" in e for e in self.errori(r)))
        self.assertLess(time.time() - inizio, 2)

    def test_una_riga_sola_e_niente_markup(self):
        for campo, valore in (("titolo", "Studio Alfa\n\nAttenzione bassa:\n- Nessun dato delicato"), ("titolo", "Studio\tAlfa")):
            r = esempio()
            r["meta"][campo] = valore
            self.assertTrue(any("carattere di controllo" in e for e in self.errori(r)), valore)
        for valore in ("Usare l'IA ![ ](https://esempio.eu/p.gif)", "Leggi [qui](javascript:alert(1))", "Trattare <img src=https://esempio.eu/b.gif>"):
            r = esempio()
            r["righe"][0]["azione"] = valore
            self.assertTrue(any("markup" in e for e in self.errori(r)), valore)
        r = esempio()
        r["aperti"][0] = "Soglia < 250 dipendenti: nessuna fonte è stata riaperta online."
        self.assertEqual(self.errori(r), [])

    def test_caratteri_invisibili(self):
        for valore in ("rischio\u200b zero", "dati ano\u00adnimi", "testo \u202e rovesciato", "campanello \u009b", "fine \u007f"):
            r = esempio()
            r["righe"][0]["nota"] = valore
            self.assertTrue(any("invisibile" in e for e in self.errori(r)), repr(valore))

    def test_frasi_vietate_con_spazi_e_apostrofo(self):
        for valore in ("Qui il rischio  zero è garantito", "Rischio\u00a0zero", "Lo studio e' conforme al GDPR"):
            r = esempio()
            r["righe"][0]["nota"] = valore
            self.assertTrue(any("non affermare" in e for e in self.errori(r)), repr(valore))

    def test_tipi_sbagliati_danno_errori_non_eccezioni(self):
        def cambia(f):
            r = esempio()
            f(r)
            return r
        casi = [
            lambda r: r["meta"].update(settore=[]),
            lambda r: r["meta"].update(data=20261013),
            lambda r: r["meta"].update(data="20261013"),
            lambda r: next(x for x in r["righe"] if x["tipo"] == "da_fare").update(quando=["subito"]),
            lambda r: r["righe"][0].update(altre_fonti=5),
            lambda r: r["righe"][0].update(fonte="x"),
            lambda r: r["righe"][0]["fonte"].update(nota=5),
            lambda r: r["righe"][0].update(norme=[1, 2]),
            lambda r: r["attenzione"].update(motivi=[None]),
            lambda r: r["caso"].update(strumenti=[1, 2]),
            lambda r: r["setup"][0].update(pro=5),
            lambda r: r["setup"][0].update(condizione=5),
            lambda r: r["setup"].append("x"),
            lambda r: r.update(ruoli="titolare"),
            lambda r: r["costi"]["voci"][0].update(nota=5),
        ]
        for i, f in enumerate(casi):
            errori = self.errori(cambia(f))
            self.assertTrue(errori, "caso %d accettato" % i)
            self.assertFalse(any("struttura non valida" in e for e in errori), "caso %d: eccezione interna %s" % (i, errori))

    def test_struttura_troppo_annidata(self):
        r = esempio()
        nodo = r
        for _ in range(5000):
            nodo["x"] = {}
            nodo = nodo["x"]
        self.assertTrue(self.errori(r))

    def test_consigliato_e_regge_sono_booleani(self):
        r = esempio()
        non_basta = next(s for s in r["setup"] if s.get("regge") is False)
        non_basta["consigliato"] = 1
        self.assertTrue(any("serve true o false" in e for e in self.errori(r)))

    def test_indirizzi(self):
        for url in ("https://www.garanteprivacy.it@esempio.eu/docweb", "https://esempio.eu\\@www.garanteprivacy.it/", "https://esempio.eu/a\n", "https://esempio.eu/" + "a" * 700):
            self.assertFalse(apc_lib.url_ok(url), repr(url))
        self.assertTrue(apc_lib.url_ok("https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/9124510"))
        r = esempio()
        r["righe"][-1]["fonte"] = {"stato": "non_verificata", "url": "https://esempio.eu/pagina"}
        self.assertTrue(any("non verificata non ha indirizzo" in e for e in self.errori(r)))

    def test_chiavi_ostili_non_arrivano_a_schermo(self):
        r = esempio()
        r["note\u001b[2J\nOK: report valido"] = "testo — con trattino"
        errori = self.errori(r)
        self.assertTrue(errori)
        self.assertFalse(any("\u001b" in e or "\n" in e for e in errori))


if __name__ == "__main__":
    unittest.main()
