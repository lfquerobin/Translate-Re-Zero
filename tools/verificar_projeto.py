"""Confere estrutura editorial e gera vistas do registro; não avalia tradução."""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import date
import json
from pathlib import Path
import re
import sys


@dataclass
class Achado:
    nivel: str
    codigo: str
    arquivo: str
    linha: int
    mensagem: str


ROTULO = re.compile(r"^(?:\?\?\?|[^:\[\]\n,.!?;]{1,60}): \[")
PREFIXO_ARQUIVO = re.compile(r"^\d{3}\.\s+")
ESTADOS = {"pendente", "iniciada", "registrada", "concluida", "conferida", "com_pendencias", "ajustado"}
CAMPOS = ("Título", "Link", "Data de publicação", "Traduzido por")
VISTAS = ("ACOMPANHAMENTO.md", "PENDÊNCIAS.md")


def verificar_texto(texto: str, arquivo: str, capitulo: dict, variantes: list) -> list[Achado]:
    achados = []

    def add(nivel, codigo, linha, mensagem):
        achados.append(Achado(nivel, codigo, arquivo, linha, mensagem))

    linhas = texto.splitlines()
    cabecalho = {}
    for n, campo in enumerate(CAMPOS, 1):
        linha = linhas[n - 1] if len(linhas) >= n else ""
        match = re.fullmatch(r"\*\*" + re.escape(campo) + r": (.+)\*\*\s*", linha)
        if not match or not match[1].strip() or re.search(r"<[^>]+>", match[1]):
            add("ERRO", "cabecalho", n, f"Preencher a linha inteira em negrito: {campo}.")
        else:
            cabecalho[campo] = match[1].strip()
            if n < len(CAMPOS) and not linha.endswith("  "):
                add("ERRO", "quebra_cabecalho", n, "Terminar a linha com dois espaços para a quebra em Markdown.")
    titulo = cabecalho.get("Título")
    if titulo:
        # Só as aspas retas duplas admitem substituição no nome do arquivo Windows.
        partes = titulo.split(chr(34))
        titulo_windows = "".join(parte + ("“" if i % 2 == 0 else "”") for i, parte in enumerate(partes[:-1])) + partes[-1]
        nome = PREFIXO_ARQUIVO.sub("", Path(arquivo).stem)
        if nome != titulo_windows:
            add("ERRO", "titulo_arquivo", 1, "O título do cabeçalho difere do nome do arquivo.")
    link = re.fullmatch(r"\[[^\[\]]+\]\((https?://[^)\s]+)\)", cabecalho.get("Link", ""))
    if not link or link[1] != capitulo["fontes"]["ingles"]:
        add("ERRO", "link_fonte", 2, "Usar um link Markdown que corresponda à fonte inglesa registrada.")
    if "Data de publicação" in cabecalho:
        meses = ("janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro").split()
        publicacao = capitulo["fontes"].get("publicacao_ingles")
        if publicacao is None:
            confere = bool(re.search(r"não.*informad", cabecalho["Data de publicação"], re.IGNORECASE))
        else:
            dt = date.fromisoformat(publicacao)
            esperado = f"{dt.day} de {meses[dt.month - 1]} de {dt.year}"
            confere = cabecalho["Data de publicação"] == esperado
        if not confere:
            add("ERRO", "data_fonte", 3, "A data do cabeçalho difere da publicação inglesa registrada.")
    conteudo = [(n, l) for n, l in enumerate(linhas, 1) if n > 4 and l.strip()]
    if not conteudo or not conteudo[0][1].startswith("※") or not conteudo[-1][1].startswith("※"):
        add("ERRO", "limites_capitulo", 5, "Conferir os separadores inicial e final do capítulo.")
    elif len(conteudo) > 1 and conteudo[-1][0] == conteudo[-2][0] + 1:
        add("ERRO", "limites_capitulo", conteudo[-1][0], "Deixar uma linha em branco antes do separador final.")
    aberturas = []
    for n, linha in enumerate(linhas, 1):
        if "\ufffd" in linha:
            add("ERRO", "codificacao", n, "Caractere de substituição: conferir a codificação UTF-8.")
        if n <= 4:
            continue
        # Os links Markdown do cabeçalho não fazem parte dos delimitadores de diálogo.
        for match in re.finditer(r"(?<!\\)[\[\]]", linha):
            if match[0] == "[":
                aberturas.append(n)
            elif aberturas:
                aberturas.pop()
            else:
                add("ERRO", "colchete", n, "Colchete de fechamento sem abertura.")
        if ROTULO.match(linha) and not re.search(r"\]\s*(?:[,.;!?].*)?$", linha):
            add("ERRO", "fim_dialogo", n, "Conferir o fechamento da fala identificada.")
        if re.search(r"““|””|—\s*―|―\s*—", linha):
            add("AVISO", "marcacao_suspeita", n, "Possível duplicação; conferir a fonte antes de corrigir.")
        if re.fullmatch(r"“.+”", linha):
            add("AVISO", "fala_sem_rotulo", n, "Trecho isolado entre aspas: verificar se é fala ou pensamento/citação.")
        if ROTULO.match(linha) and re.search(r": \[“.*”\]", linha):
            add("AVISO", "aspas_externas", n, "Aspas dentro dos colchetes podem duplicar a marcação externa.")
        if ": [" in linha and not ROTULO.match(linha):
            add("AVISO", "rotulo_incorporado", n, "Possível rótulo dentro da narração: conferir a exceção editorial.")
        if linha.startswith("[N"):
            continue  # Notas da fonte podem citar a grafia inglesa deliberadamente.
        for regra in variantes:
            for variante in regra["variantes"]:
                if re.search(r"(?<!\w)" + re.escape(variante) + r"(?!\w)", linha, re.IGNORECASE):
                    add("AVISO", "variante_termo", n, f"Possível variante {variante!r}; conferir a adoção de {regra['adotado']!r} no glossário.")
    for n in aberturas:
        add("ERRO", "colchete", n, "Colchete de abertura sem fechamento.")
    return achados


def validar_registro(dados: dict, raiz: Path) -> list[Achado]:
    achados = []

    def erro(msg):
        achados.append(Achado("ERRO", "registro", "projeto.json", 1, msg))

    if dados.get("schema") != 1 or not isinstance(dados.get("capitulos"), list) or not dados["capitulos"]:
        erro("Registro deve ter schema 1 e uma lista não vazia de capítulos.")
        return achados
    ids, arquivos = set(), set()
    for c in dados["capitulos"]:
        try:
            if c["id"] in ids or c["arquivo"] in arquivos:
                erro("ID ou arquivo de capítulo duplicado.")
            ids.add(c["id"]); arquivos.add(c["arquivo"])
            alvo = (raiz / c["arquivo"]).resolve()
            if not alvo.is_relative_to(raiz.resolve()) or not alvo.is_file():
                erro(f"Arquivo ausente ou fora do projeto: {c['arquivo']}")
            if not all(re.fullmatch(r"https://[^\s]+", c["fontes"][k]) for k in ("japones", "ingles")):
                erro(f"Fontes inválidas em {c['id']}.")
            if c["fontes"]["publicacao_ingles"] is not None:
                date.fromisoformat(c["fontes"]["publicacao_ingles"])
            for etapa in ("fidelidade", "naturalidade", "falantes", "formato"):
                rev = c["revisoes"][etapa]
                if rev["estado"] not in ESTADOS:
                    erro(f"Estado de revisão inválido em {c['id']}: {etapa}.")
                if rev["estado"] != "pendente" and not rev.get("data"):
                    erro(f"Registrar a data da etapa {etapa} em {c['id']}.")
                if rev.get("data"):
                    date.fromisoformat(rev["data"])
            if c["revisoes"]["fidelidade"]["estado"] == "registrada" and not c["revisoes"]["fidelidade"].get("observacao"):
                erro(f"Explicar a evidência histórica em {c['id']}.")
        except (KeyError, TypeError, ValueError):
            erro("Capítulo com campos obrigatórios ausentes ou dados inválidos.")
    vistos, pendencias = set(), set()
    por_id = {c["id"]: c for c in dados["capitulos"] if "id" in c}
    for o in dados.get("ocorrencias_anonimas", []):
        try:
            if o["id"] in vistos or o["capitulo_id"] not in ids:
                erro("Ocorrência anônima duplicada ou com capítulo inexistente.")
            vistos.add(o["id"])
            if not o["trecho"] or not o["motivo"] or o["referencia_japonesa"] != por_id[o["capitulo_id"]]["fontes"]["japones"]:
                erro(f"Conferir trecho, motivo e referência de {o['id']}.")
            if o["tipo"] == "atribuicao_pendente":
                if o["pendencia_id"] in pendencias:
                    erro("ID de pendência duplicado.")
                pendencias.add(o["pendencia_id"])
                if o["estado"] not in ("aberta", "resolvida") or len(o["interpretacoes"]) < 2 or not o["original_japones"] or not o["proximo_passo"]:
                    erro(f"Completar a investigação de {o['id']}.")
                if o["estado"] == "resolvida" and not o.get("resolucao"):
                    erro(f"Registrar evidência da resolução de {o['id']}.")
            elif o["tipo"] != "anonimato_narrativo":
                erro(f"Classificação inválida em {o['id']}.")
        except (KeyError, TypeError):
            erro("Ocorrência anônima incompleta.")
    glossario = (raiz / "GLOSSÁRIO.md").read_text(encoding="utf-8")
    for regra in dados.get("variantes_terminologicas", []):
        if not regra.get("adotado") or not regra.get("variantes") or regra["adotado"].casefold() not in glossario.casefold():
            erro("Regra terminológica precisa de variantes explícitas e termo existente no glossário.")
    return achados


def conferir_anonimos(dados: dict, textos: dict[str, str]) -> list[Achado]:
    achados, presentes, esperados = [], Counter(), Counter()
    for cid, texto in textos.items():
        for n, linha in enumerate(texto.splitlines(), 1):
            if linha.startswith("???: [") and linha.endswith("]"):
                presentes[cid, linha[6:-1]] += 1
    for o in dados["ocorrencias_anonimas"]:
        if o.get("estado") != "resolvida":
            esperados[o["capitulo_id"], o["trecho"]] += 1
    por_id = {c["id"]: c for c in dados["capitulos"]}
    for (cid, trecho), count in (presentes - esperados).items():
        achados.append(Achado("ERRO", "anonimo_sem_registro", por_id[cid]["arquivo"], 1, f"Classificar {count} ocorrência(s) de ???: {trecho[:65]}"))
    for (cid, trecho), count in (esperados - presentes).items():
        achados.append(Achado("ERRO", "registro_sem_anonimo", "projeto.json", 1, f"Conferir {count} registro(s) sem ocorrência correspondente em {cid}: {trecho[:65]}"))
    for cid, c in por_id.items():
        aberto = any(o["capitulo_id"] == cid and o["tipo"] == "atribuicao_pendente" and o["estado"] == "aberta" for o in dados["ocorrencias_anonimas"])
        if aberto != (c["revisoes"]["falantes"]["estado"] == "com_pendencias"):
            achados.append(Achado("ERRO", "estado_falantes", "projeto.json", 1, f"Estado dos falantes incompatível com as pendências de {cid}."))
    return achados


def celula(texto):
    return str(texto).replace("|", r"\|").replace("\n", " ")


def link_capitulo(c):
    titulos_especiais = {0: "Prólogo", "interludio": "Interlúdio"}
    titulo = titulos_especiais.get(c["capitulo"], f"Capítulo {c['capitulo']}")
    return f"[{titulo}](<{c['arquivo']}>)"


def etapa(revisao):
    nomes = {"registrada": "Registrada no histórico", "pendente": "Pendente", "conferida": "Conferida", "com_pendencias": "Com pendência", "ajustado": "Ajustado", "concluida": "Concluída", "iniciada": "Iniciada"}
    valor = nomes[revisao["estado"]]
    if revisao.get("data"):
        valor += " · " + date.fromisoformat(revisao["data"]).strftime("%d/%m/%Y")
    return valor


def gerar_vistas(dados: dict, textos: dict[str, str]) -> dict[str, str]:
    caps = dados["capitulos"]; por_id = {c["id"]: c for c in caps}
    anonimos = [o for o in dados["ocorrencias_anonimas"] if o["tipo"] == "anonimato_narrativo"]
    pendentes = [o for o in dados["ocorrencias_anonimas"] if o["tipo"] == "atribuicao_pendente"]
    abertos = [o for o in pendentes if o["estado"] == "aberta"]
    indice = ["# Acompanhamento da tradução", "", "Gerado de [projeto.json](projeto.json). Atualizar o registro e executar `python tools/verificar_projeto.py --atualizar-indices`; não editar esta vista à mão.", "", f"Versão da obra: **{dados['versao']}**. As datas das colunas abaixo indicam quando cada etapa foi conferida.", "", "As dúvidas de falante e as ocorrências de anonimato narrativo estão documentadas em [PENDÊNCIAS.md](PENDÊNCIAS.md).", "", "| Arco / capítulo | Fontes | Fidelidade | Naturalidade | Falantes | Formato |", "| --- | --- | --- | --- | --- | --- |"]
    for c in caps:
        fontes = f"[JP]({c['fontes']['japones']}) / [EN]({c['fontes']['ingles']})"
        valores = [f"{c['arco']} / {link_capitulo(c)}", fontes] + [etapa(c["revisoes"][e]) for e in ("fidelidade", "naturalidade", "falantes", "formato")]
        indice.append("| " + " | ".join(celula(v) for v in valores) + " |")
    falta = sum(c["revisoes"]["naturalidade"]["estado"] == "pendente" for c in caps)
    indice += ["", "## Trabalho em aberto", "", f"- {falta} capítulos/textos aguardam registro de releitura contínua final.", f"- {len(abertos)} atribuições de fala em investigação; consultar [PENDÊNCIAS.md](PENDÊNCIAS.md).", f"- {len(anonimos)} ocorrências de `???` preservam anonimato da narrativa e estão documentadas separadamente.", "", "A aprovação estrutural do verificador não conclui nenhuma etapa editorial. Registrar data, escopo e evidência após executar a revisão correspondente.", ""]
    pend = ["# Pendências e anonimato de falantes", "", "Vista gerada de [projeto.json](projeto.json). O capítulo conserva `???` nos dois casos abaixo; a distinção existe somente neste registro interno.", "", "- **Atribuição pendente:** falta evidência suficiente para escolher o falante; exige investigação e indicação na entrega.", "- **Anonimato narrativo:** o texto ainda não permite revelar a identidade naquele ponto; não constitui erro nem tarefa de descobrir o nome.", "", "As referências respeitam a web novel. Uma atribuição de outra versão não resolve automaticamente a dúvida desta versão.", "", "## Atribuições em investigação", ""]
    for o in pendentes:
        c = por_id[o["capitulo_id"]]
        pend += [f"### {o['pendencia_id']} — {'aberta' if o['estado'] == 'aberta' else 'resolvida'}", "", f"Capítulo: {link_capitulo(c)}. Registrada em {o['registrada_em']}.", "", f"Português: {o['trecho']}", "", f"Original japonês: {o['original_japones']}", "", f"Contexto: {o['motivo']}", "", "Interpretações possíveis: " + "; ".join(o["interpretacoes"]) + ".", "", f"Próximo passo: {o['proximo_passo']}", "", f"Fontes: [japonês]({c['fontes']['japones']}) e [fonte inglesa]({c['fontes']['ingles']}).", ""]
        if o.get("resolucao"):
            pend += ["Resolução e evidência: " + o["resolucao"], ""]
    pend += ["## Anonimato preservado na narrativa", "", "Os trechos abaixo são âncoras de localização. A eventual identificação posterior não autoriza revelar o nome antecipadamente.", "", "| Ocorrência | Capítulo / linha atual | Trecho | Motivo | Fonte |", "| --- | --- | --- | --- | --- |"]
    for o in anonimos:
        c = por_id[o["capitulo_id"]]
        linha = next((n for n, l in enumerate(textos[c["id"]].splitlines(), 1) if l == "???: [" + o["trecho"] + "]"), "—")
        trecho = o["trecho"] if len(o["trecho"]) <= 85 else o["trecho"][:82] + "…"
        valores = [o["id"], f"{link_capitulo(c)} · {linha}", trecho, o["motivo"], f"[JP]({o['referencia_japonesa']})"]
        pend.append("| " + " | ".join(celula(v) for v in valores) + " |")
    pend += ["", "Não encerrar pendências escolhendo um candidato apenas para remover `???`. Se houver evidência nova, registrar a resolução e sua fonte antes de atualizar a fala e as etapas de revisão.", ""]
    return dict(zip(VISTAS, ("\n".join(indice), "\n".join(pend))))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raiz", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--atualizar-indices", action="store_true", help="regenera somente ACOMPANHAMENTO.md e PENDÊNCIAS.md")
    parser.add_argument("--estrito", action="store_true", help="retorna 1 também quando houver avisos estruturais ou terminológicos")
    args = parser.parse_args(argv); raiz = args.raiz.resolve()
    try:
        dados = json.loads((raiz / "projeto.json").read_text(encoding="utf-8"))
        achados = validar_registro(dados, raiz)
        if achados:
            for a in achados:
                print(f"{a.nivel} [{a.codigo}] {a.arquivo}:{a.linha}: {a.mensagem}")
            return 2
        textos = {c["id"]: (raiz / c["arquivo"]).read_text(encoding="utf-8") for c in dados["capitulos"]}
        for c in dados["capitulos"]:
            achados += verificar_texto(textos[c["id"]], c["arquivo"], c, dados["variantes_terminologicas"])
        registrados = {c["arquivo"] for c in dados["capitulos"]}
        for p in raiz.rglob("*.md"):
            if any(parte in {".git", ".obsidian", "tools"} for parte in p.relative_to(raiz).parts):
                continue
            if p.read_text(encoding="utf-8").startswith("**Título: ") and p.relative_to(raiz).as_posix() not in registrados:
                achados.append(Achado("ERRO", "capitulo_sem_registro", str(p), 1, "Adicionar o capítulo ao acompanhamento."))
        achados += conferir_anonimos(dados, textos)
        if not any(a.nivel == "ERRO" for a in achados):
            for nome, conteudo in gerar_vistas(dados, textos).items():
                alvo = raiz / nome
                if args.atualizar_indices:
                    alvo.write_text(conteudo, encoding="utf-8", newline="\n")
                elif not alvo.is_file() or alvo.read_text(encoding="utf-8") != conteudo:
                    achados.append(Achado("ERRO", "vista_desatualizada", nome, 1, "Regenerar com --atualizar-indices."))
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
        print(f"ERRO [leitura_registro] {exc}")
        return 2
    for a in achados:
        print(f"{a.nivel} [{a.codigo}] {a.arquivo}:{a.linha}: {a.mensagem}")
    erros = sum(a.nivel == "ERRO" for a in achados); avisos = sum(a.nivel == "AVISO" for a in achados)
    abertas = sum(o["tipo"] == "atribuicao_pendente" and o["estado"] == "aberta" for o in dados["ocorrencias_anonimas"])
    releituras = sum(c["revisoes"]["naturalidade"]["estado"] == "pendente" for c in dados["capitulos"])
    print(f"{len(textos)} textos: {erros} erro(s), {avisos} aviso(s). Pendências editoriais registradas: {abertas} atribuições e {releituras} releituras.")
    print("A conferência estrutural não valida sentido, qualidade ou identidade de falantes.")
    return 2 if erros else (1 if avisos and args.estrito else 0)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
