#!/usr/bin/env python3
"""O corpus de fontes: migração, bibliografia e conferência.

O corpus vive em `dados/fontes.tsv`, uma linha por fonte, e o número da linha é o
identificador (RF###, herdando a numeração do arquivo para que a procedência de
qualquer empréstimo seja rastreável). Este script faz três coisas:

  --migrar    lê `.old/dados/references.tsv` e escreve `dados/fontes.tsv` limpo
  (padrão)    gera `livro/fontes.tex` — o ambiente thebibliography do livro, só com
            as fontes citadas, na ordem de primeira aparição no texto (NBR 10520)
  --check     confere chaves únicas e que toda citação do livro existe no corpus

A chave de citação é derivada mecanicamente: sobrenome do primeiro autor + ano +
primeira palavra significativa do título. Colisões recebem sufixo b, c, ...
"""
import csv
import os
import re
import sys
import unicodedata
from pathlib import Path

ARQUIVO = ".old/dados/references.tsv"
TSV = "dados/fontes.tsv"
BIB = "livro/fontes.tex"
LIVRO = "livro"

CABECALHO = ["id", "chave", "autores", "titulo", "ano", "veiculo", "link", "area", "tema"]

# palavras que não identificam um título
VAZIAS = {
    "the", "of", "and", "for", "with", "from", "into", "onto", "over", "under",
    "a", "an", "on", "in", "to", "at", "by", "as", "is", "are", "be", "it", "its",
    "de", "da", "do", "das", "dos", "e", "em", "para", "por", "com", "sobre",
    "um", "uma", "que", "nao", "not", "new", "using", "toward", "towards",
    "via", "about", "between", "through", "across", "their", "this", "that",
}


def dobra(texto: str) -> str:
    """Minúsculas sem acento, para chave de citação."""
    plano = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in plano if not unicodedata.combining(c)).lower()


def limpa(texto: str) -> str:
    """Uma célula de TSV não pode ter tabulação nem quebra de linha."""
    return re.sub(r"\s+", " ", texto.replace("\t", " ").replace("\n", " ")).strip()


ESPECIAIS = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
             "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}",
             "^": r"\textasciicircum{}", "\\": r"\textbackslash{}"}


ACENTOS = "áàâãäéèêëíìîïóòôõöúùûüçñÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇÑ"
SEGUROS = ACENTOS + "–—‘’“”…°±×÷"


def tex(texto: str) -> str:
    """Escapa o título para o LaTeX, deixando intacto o que vier entre cifrões.

    Um título de artigo carrega notação que não se escreve em texto corrido: um
    "L_{p,q}" de medida de variação, por exemplo. Escapado, isso imprime chaves e
    sublinhado, e o leitor recebe o código em vez da notação. O cifrão é a
    declaração de que aquele trecho é matemática: ele sai como está, e o resto
    continua escapado. Cifrão ímpar não declara nada --- e aí o texto inteiro é
    escapado, como antes.
    """
    if texto.count("$") % 2:
        return _escapa(texto)
    partes, dentro = [], False
    for pedaco in texto.split("$"):
        if dentro:
            partes.append("$" + pedaco + "$")
        else:
            partes.append(_escapa(pedaco))
        dentro = not dentro
    return "".join(partes)


def _escapa(texto: str) -> str:
    """Escapa o que o LaTeX interpretaria e translitera o que ele não aceita.

    Um "&" cru derruba a compilação; um caractere matemático alfanumérico
    (o "𝐿" de um título colado de PDF) também. O segundo caso se resolve
    decompondo: o bloco matemático tem forma canônica em letras comuns.
    """
    saida = []
    for c in texto:
        if ord(c) < 128 or c in SEGUROS:
            saida.append(c)
            continue
        plano = unicodedata.normalize("NFKD", c)
        plano = "".join(x for x in plano if not unicodedata.combining(x))
        saida.append(plano if plano.isascii() and plano.strip() else "")
    return "".join(ESPECIAIS.get(c, c) for c in "".join(saida))


def sobrenome(autores: str) -> str:
    primeiro = autores.split(",")[0].strip()
    tokens = [t for t in re.split(r"[\s.]+", primeiro) if t]
    return dobra(tokens[-1]) if tokens else "anon"


def palavra_titulo(titulo: str) -> str:
    for bruto in re.split(r"[^0-9A-Za-zÀ-ÿ]+", dobra(titulo)):
        if len(bruto) >= 4 and bruto not in VAZIAS and not bruto.isdigit():
            return bruto
    return "obra"


def ano(de) -> str:
    achado = re.search(r"(1[5-9][0-9]{2}|20[0-9]{2})", de or "")
    return achado.group(1) if achado else "s.d."


def autores_abnt(autores: str) -> str:
    r"""SOBRENOME, Nome; SOBRENOME, Nome --- a NBR 6023 pede o sobrenome em caixa alta na frente.

    O corpus guarda os autores na ordem natural ("G. A. Carpenter, S. Grossberg"), e a entrada
    impressa os repetia assim. A conversao sobe o ultimo token de cada autor para a caixa alta e
    deixa as iniciais depois da virgula; nome de uma palavra so (instituicao, ou autor que assina
    com um nome unico) passa inteiro.
    """
    blocos = [b.strip() for b in autores.split(";")] if ";" in autores else [b.strip() for b in autores.split(",")]
    saida = []
    for bloco in blocos:
        tokens = [tk for tk in bloco.split() if tk]
        if len(tokens) >= 2 and not tokens[-1].endswith("."):
            saida.append("%s, %s" % (dobra(tokens[-1]).upper(), " ".join(tokens[:-1])))
        else:
            saida.append(bloco)
    return "; ".join(saida)


def chave_de(autores: str, titulo: str, ano_: str) -> str:
    bruta = re.sub(r"[^a-z0-9]", "", sobrenome(autores) + ano_ + palavra_titulo(titulo))
    return bruta[:40]


def migrar() -> int:
    with open(ARQUIVO, encoding="utf-8") as fh:
        linhas = list(csv.reader(fh, delimiter="\t"))
    cabeca, dados = linhas[0], linhas[1:]
    idx = {nome: i for i, nome in enumerate(cabeca)}
    vistos: dict = {}
    saida = [CABECALHO]
    for n, linha in enumerate(dados, start=1):
        if len(linha) < 11 or not linha[0].strip():
            continue
        autores = limpa(linha[idx["Autores/Pesquisadores"]])
        titulo = limpa(linha[idx["Título do Artigo"]])
        ano_ = ano(linha[idx["Data de Publicação"]])
        chave = chave_de(autores, titulo, ano_)
        if chave in vistos:
            vistos[chave] += 1
            chave = chave + chr(ord("a") + vistos[chave])
        else:
            vistos[chave] = 0
        tema = limpa(linha[idx["Principais Conceitos de IA"]])[:160]
        saida.append([
            "RF%03d" % n, chave, autores, titulo, ano_,
            limpa(linha[idx["Instituição/Afiliação"]]) or "—",
            limpa(linha[idx["Link"]]) or "—",
            limpa(linha[idx["Área CNPq"]]) or "—",
            tema or "—",
        ])
    os.makedirs(os.path.dirname(TSV), exist_ok=True)
    with open(TSV, "w", encoding="utf-8", newline="") as fh:
        csv.writer(fh, delimiter="\t", lineterminator="\n").writerows(saida)
    print("migradas %d fontes de %s para %s" % (len(saida) - 1, ARQUIVO, TSV))
    return 0


def carregar() -> list:
    with open(TSV, encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def gerar_bibliografia() -> int:
    ordem = citacoes_ordenadas()
    por_chave = {f["chave"]: f for f in carregar()}
    ausentes = [k for k in ordem if k not in por_chave]
    if ausentes:
        raise SystemExit("citadas e ausentes do corpus: %s" % ", ".join(ausentes))
    fontes = [por_chave[k] for k in ordem]
    linhas = [
        "% GERADO POR lab/fontes.py — NÃO EDITE À MÃO.",
        "\\begin{thebibliography}{%d}" % (len(fontes) + 1),
        # A entrada no sumário sai daqui, e não do livro.tex: assim ela fica na página em
        # que a lista começa, e o gerador não deixa a entrada para trás quando reescreve.
        "\\addcontentsline{toc}{chapter}{\\bibname}",
        "",
    ]
    for f in fontes:
        linhas.append("  \\bibitem{%s}" % f["chave"])
        nome = autores_abnt(tex(f["autores"]))
        linhas.append("  %s%s" % (nome, "" if nome.endswith(".") else "."))
        linhas.append("  \\newblock \\textbf{%s}." % tex(f["titulo"]))
        if f["veiculo"] and f["veiculo"] != "—":
            veiculo = tex(f["veiculo"])
            # o ano ja mora dentro do veiculo em parte do corpus (o periodico o carrega):
            # imprimi-lo de novo punha "2007, 2007" em 52 entradas.
            linhas.append("  \\newblock %s." % (veiculo if f["ano"] in veiculo
                                                else "%s, %s" % (veiculo, f["ano"])))
        else:
            linhas.append("  \\newblock %s." % f["ano"])
        if f["link"] and f["link"] != "—":
            linhas.append("  \\newblock \\url{%s}" % f["link"])
        linhas.append("")
    linhas.append("\\end{thebibliography}")
    os.makedirs(LIVRO, exist_ok=True)
    with open(BIB, "w", encoding="utf-8") as fh:
        fh.write("\n".join(linhas) + "\n")
    print("bibliografia: %d fontes citadas, em ordem de aparição, em %s" % (len(fontes), BIB))
    return 0


def citacoes() -> set:
    chaves = set()
    if not os.path.isdir(LIVRO):
        return chaves
    # recursivo de propósito: o livro passou a ter capítulos em livro/capitulos/, e um
    # gerador que só olha o primeiro nível para de conferir citação sem avisar.
    for caminho in sorted(Path(LIVRO).rglob("*.tex")):
        texto = caminho.read_text(encoding="utf-8")
        for grupo in re.findall(r"\\cite\{([^}]+)\}", texto):
            for chave in grupo.split(","):
                chaves.add(chave.strip())
    return chaves


def citacoes_ordenadas() -> list:
    r"""As chaves citadas, na ordem de PRIMEIRA APARIÇÃO no texto do livro.

    A NBR 10520 pede que, no sistema numérico, a lista siga a ordem em que as fontes
    aparecem citadas --- e a aparição é a dos capítulos na ordem de leitura (o número
    do arquivo é a posição, conferida por portão). As notas de parte do livro.tex não
    citam nada, mas o gerador as lê na frente por segurança: se um dia citarem, a
    ordem continua certa.
    """
    arquivos = [Path(LIVRO) / "livro.tex"]
    capitulos = Path(LIVRO) / "capitulos"
    if capitulos.is_dir():
        arquivos += sorted(capitulos.glob("*.tex"))
    else:
        arquivos += sorted(Path(LIVRO).glob("*.tex"))
    ordem, vistas = [], set()
    for caminho in arquivos:
        if not caminho.exists():
            continue
        for grupo in re.findall(r"\\cite\{([^}]+)\}", caminho.read_text(encoding="utf-8")):
            for chave in grupo.split(","):
                k = chave.strip()
                if k and k not in vistas:
                    vistas.add(k)
                    ordem.append(k)
    return ordem


def check() -> int:
    avisos = []
    fontes = carregar()
    if not fontes:
        avisos.append("corpus vazio: %s" % TSV)
    ids, chaves = set(), set()
    for f in fontes:
        if f["id"] in ids:
            avisos.append("id repetido: %s" % f["id"])
        ids.add(f["id"])
        if f["chave"] in chaves:
            avisos.append("chave repetida: %s" % f["chave"])
        chaves.add(f["chave"])
        for campo in ("autores", "titulo", "ano"):
            if not f[campo] or f[campo] == "—":
                avisos.append("%s sem %s" % (f["id"], campo))
    for chave in sorted(citacoes()):
        if chave not in chaves:
            avisos.append("citação sem fonte no corpus: %s" % chave)
    if os.path.exists(BIB):
        impressas = set(re.findall(r"\\bibitem\{([^}]+)\}",
                                   open(BIB, encoding="utf-8").read()))
        if impressas != citacoes():
            so_impressas = sorted(impressas - citacoes())
            so_citadas = sorted(citacoes() - impressas)
            avisos.append("bibliografia desatualizada: gere de novo com lab/fontes.py"
                          + ("; saiu: %s" % ", ".join(so_impressas) if so_impressas else "")
                          + ("; entrou: %s" % ", ".join(so_citadas) if so_citadas else ""))
    print("corpus: %d fontes | %d citações no livro | %d impressas" % (len(fontes), len(citacoes()), len(impressas) if os.path.exists(BIB) else 0))
    if avisos:
        print("auditoria: %d aviso(s)" % len(avisos))
        for a in avisos:
            print("  -", a)
        return 1
    print("auditoria: limpa")
    return 0


def main(argv: list) -> int:
    if "--migrar" in argv:
        return migrar()
    if "--check" in argv:
        return check()
    return gerar_bibliografia()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
