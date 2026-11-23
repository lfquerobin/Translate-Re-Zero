"""Casos de regressão editorial, sem acesso à rede ou aos capítulos reais."""
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest

from verificar_projeto import conferir_anonimos, main, verificar_texto


TITULO = "Arco 1, Capítulo 1 – “Teste”"
ARQUIVO = "Arco 1/002. " + TITULO + ".md"
CAPITULO = {
    "id": "A01-C01", "arco": 1, "capitulo": 1, "arquivo": ARQUIVO,
    "fontes": {"japones": "https://example.org/jp/2/", "ingles": "https://example.org/en/1/", "publicacao_ingles": "2021-05-19"},
    "revisoes": {e: {"estado": "pendente", "data": None} for e in ("fidelidade", "naturalidade", "falantes", "formato")},
}
CAPITULO["revisoes"]["falantes"] = {"estado": "conferida", "data": "2026-11-01"}


def texto(corpo="Subaru: [Olá.]", titulo=TITULO):
    return (f"**Título: {titulo}**  \n"
            "**Link: [Fonte](https://example.org/en/1/)**  \n"
            "**Data de publicação: 19 de maio de 2021**  \n"
            "**Traduzido por: Tradutor da fonte; revisão do projeto**\n\n"
            "※　※　※\n\n" + corpo + "\n\n※　※　※\n")


def codigos(s, cap=None, variantes=None):
    return {a.codigo for a in verificar_texto(s, ARQUIVO, cap or CAPITULO, variantes or [])}


class RegrasEditoriais(unittest.TestCase):
    def test_fala_simultanea_citacao_interna_e_fala_incorporada(self):
        s = texto('Rom e Felt: [Ah!]\n\nSubaru: [Ela disse “não”.]\n\nRom perguntou, “Quer beber?”\n\n[N/T: Um exemplo.]')
        self.assertEqual(codigos(s), set())

    def test_cabecalho_incompleto_e_titulo_divergente(self):
        self.assertIn("cabecalho", codigos(texto().replace("**Traduzido por:", "Traduzido por:")))
        self.assertIn("titulo_arquivo", codigos(texto(titulo="Outro título")))

    def test_aspas_retas_permitidas_apenas_no_nome_windows(self):
        self.assertNotIn("titulo_arquivo", codigos(texto(titulo=TITULO.replace("“", chr(34)).replace("”", chr(34)))))

    def test_fonte_e_data_divergentes(self):
        self.assertIn("link_fonte", codigos(texto().replace("https://example.org/en/1/", "https://example.org/en/9/")))
        self.assertIn("data_fonte", codigos(texto().replace("19 de maio", "20 de maio")))

    def test_data_nao_informada_nao_e_inventada(self):
        c = deepcopy(CAPITULO); c["fontes"]["publicacao_ingles"] = None
        self.assertNotIn("data_fonte", codigos(texto().replace("19 de maio de 2021", "Não informada na fonte"), c))

    def test_colchetes_e_separador_ausentes(self):
        self.assertIn("colchete", codigos(texto("Subaru: [Fala sem fechar.")))
        self.assertIn("colchete", codigos(texto("Subaru: [Fala.]]")))
        self.assertIn("limites_capitulo", codigos(texto().rstrip().removesuffix("※　※　※")))

    def test_rotulo_repetido_na_narracao_e_marcacao_suspeita(self):
        self.assertIn("rotulo_incorporado", codigos(texto("Subaru: [Olá.]\n\nEnquanto o outro observava, o rapaz resolveu continuar a conversa: Subaru: [Certo.]")))
        self.assertIn("marcacao_suspeita", codigos(texto("Subaru: [— ―Certo.]")))

    def test_variantes_sao_alertas_com_limites_de_palavra(self):
        regra = [{"adotado": "Satella", "variantes": ["Satela"]}]
        self.assertIn("variante_termo", codigos(texto("Subaru: [SATELA!]"), variantes=regra))
        self.assertNotIn("variante_termo", codigos(texto("Subaru: [Satelas.]\n[N/T: Satela na referência.]"), variantes=regra))

    def test_anonimato_exige_classificacao_sem_impedir_revisao(self):
        registro = {"capitulos": [CAPITULO], "ocorrencias_anonimas": [{"capitulo_id": "A01-C01", "trecho": "Quem?", "tipo": "anonimato_narrativo"}]}
        textos = {"A01-C01": texto("???: [Quem?]")}
        self.assertEqual(conferir_anonimos(registro, textos), [])
        registro["ocorrencias_anonimas"] = []
        self.assertEqual(conferir_anonimos(registro, textos)[0].codigo, "anonimo_sem_registro")

    def test_pendencia_aberta_nao_pode_constar_como_falantes_conferidos(self):
        registro = {"capitulos": [CAPITULO], "ocorrencias_anonimas": [{"capitulo_id": "A01-C01", "trecho": "Quem?", "tipo": "atribuicao_pendente", "estado": "aberta"}]}
        achados = conferir_anonimos(registro, {"A01-C01": texto("???: [Quem?]")})
        self.assertEqual([a.codigo for a in achados], ["estado_falantes"])

    def test_cli_detecta_indice_desatualizado_e_nao_edita_capitulo(self):
        with tempfile.TemporaryDirectory(prefix="rezero-verificador-") as pasta:
            raiz = Path(pasta).resolve()
            self.assertTrue(raiz.is_relative_to(Path(tempfile.gettempdir()).resolve()))
            p = raiz / ARQUIVO; p.parent.mkdir(); p.write_text(texto(), encoding="utf-8")
            original = p.read_bytes()
            (raiz / "GLOSSÁRIO.md").write_text("# Glossário", encoding="utf-8")
            config = {"schema": 1, "versao": "web novel", "capitulos": [CAPITULO], "ocorrencias_anonimas": [], "variantes_terminologicas": []}
            (raiz / "projeto.json").write_text(json.dumps(config, ensure_ascii=False), encoding="utf-8")
            with redirect_stdout(StringIO()):
                self.assertEqual(main(["--raiz", str(raiz), "--atualizar-indices", "--estrito"]), 0)
                self.assertEqual(main(["--raiz", str(raiz), "--estrito"]), 0)
                (raiz / "ACOMPANHAMENTO.md").write_text("alteração manual", encoding="utf-8")
                self.assertEqual(main(["--raiz", str(raiz)]), 2)
                self.assertEqual(main(["--raiz", str(raiz), "--atualizar-indices"]), 0)
            self.assertEqual(p.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
