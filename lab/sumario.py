r"""O mapa do fim do livro: o sumario completo e os enunciados formais.

**Por que uma copia, e nao um segundo \tableofcontents.** O LaTeX le o .toc **antes** de abri-lo
para escrita, e o \tableofcontents do comeco ja o truncou: no fim do documento o arquivo tem so o
que a execucao atual escreveu ate ali. Um segundo \tableofcontents sai **vazio** --- conferido na
pagina. Copiar o .toc da compilacao anterior resolve, e nao custa passada extra: o sumario
completo e a ultima coisa do livro, de modo que as paginas que ele cita nao se movem.

**Os enunciados formais** saem do .aux, que e onde o LaTeX guarda o numero, a pagina e o titulo de
cada rotulo; a especie (proposicao, definicao) sai do fonte do capitulo, porque o .aux nao a diz.
O arquivo gerado e incluido com \input, e o portao o trata como gerado --- nao se edita a mao.

Uso: .venv/bin/python lab/sumario.py   (depois de compilar o livro pelo menos uma vez)
"""
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
LIVRO = RAIZ / "livro"
TOC = LIVRO / "livro.toc"
AUX = LIVRO / "livro.aux"
DESTINO = LIVRO / "sumario.tex"
DESTINO_ENUNCIADOS = LIVRO / "proposicoes.tex"

# Os niveis que entram no sumario completo. Subsecao nao existe no livro.
NIVEIS = ("part", "chapter", "section")

# As duas especies que o livro numera. Elas compartilham o contador, de modo que a numeracao e
# continua entre as duas --- e e isso que a lista mostra.
ESPECIES = {"proposicao": "Proposição", "definicao": "Definição", "teorema": "Teorema",
            "corolario": "Corolário", "lema": "Lema", "exemplo": "Exemplo",
            "observacao": "Observação"}


def capitulos() -> list:
    fonte = (LIVRO / "livro.tex").read_text(encoding="utf-8")
    nomes = [re.sub(r"\.tex$", "", n)
             for n in re.findall(r"\\input\{capitulos/([^}]+)\}", fonte)]
    return [LIVRO / "capitulos" / (n + ".tex") for n in nomes]


def sumario() -> int:
    if not TOC.exists():
        print("o livro ainda nao foi compilado: falta %s" % TOC.name)
        return 1
    linhas = [l for l in TOC.read_text(encoding="utf-8").splitlines()
              if re.match(r"\\contentsline \{(part|chapter|section)\}", l)]
    if not linhas:
        print("o .toc nao tem entradas: compile o livro antes")
        return 1
    DESTINO.write_text(
        "% GERADO POR lab/sumario.py — NÃO EDITE À MÃO.\n"
        "% Uma cópia do livro.toc da compilação anterior: o \\tableofcontents não pode ser\n"
        "% repetido no fim do documento, porque o arquivo ainda está sendo escrito.\n"
        + "\n".join(linhas) + "\n", encoding="utf-8")
    print("sumário completo: %d entradas em %s" % (len(linhas), DESTINO.relative_to(RAIZ)))
    return 0


def enunciados() -> int:
    r"""A lista dos enunciados numerados, na ordem em que o leitor os encontra."""
    if not AUX.exists():
        print("falta %s: compile o livro antes de gerar os enunciados" % AUX.name)
        return 1
    rotulos = {}
    for linha in AUX.read_text(encoding="utf-8", errors="replace").splitlines():
        achado = re.match(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}\{(.*)\}\{", linha)
        if achado:
            rotulos[achado.group(1)] = (achado.group(2), achado.group(3), achado.group(4))
    ordem, entradas = [], []
    for caminho in capitulos():
        fonte = caminho.read_text(encoding="utf-8")
        for achado in re.finditer(
                r"\\begin\{(%s)\}(?:\[([^\]]*)\])?((?:(?!\\end\{).)*?)\\end\{" % "|".join(ESPECIES),
                fonte, flags=re.S):
            especie, titulo, corpo = achado.group(1), achado.group(2), achado.group(3)
            alvo = re.search(r"\\label\{([^}]+)\}", corpo)
            if not alvo:
                continue
            rotulo = alvo.group(1)
            if rotulo not in rotulos:
                continue
            numero, pagina, titulo_no_aux = rotulos[rotulo]
            titulo = (titulo or titulo_no_aux or "").strip()
            ordem.append(rotulo)
            entradas.append((especie, numero, titulo, rotulo))
    if not entradas:
        print("nenhum enunciado numerado encontrado")
        return 1
    linhas = ["% GERADO POR lab/sumario.py — NÃO EDITE À MÃO.",
              "% Os enunciados numerados do livro, na ordem em que aparecem: número, título e página",
              "% saem do livro.aux da compilação anterior; a espécie sai do fonte do capítulo.", ""]
    for especie, numero, titulo, rotulo in entradas:
        nome = ESPECIES[especie]
        texto = "%s %s" % (nome, numero)
        if titulo:
            texto += " --- %s" % titulo
        linhas.append("\\noindent\\hyperref[%s]{\\textbf{%s}}\\dotfill\\ \\pageref{%s}\\par"
                      % (rotulo, texto, rotulo))
    DESTINO_ENUNCIADOS.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print("enunciados: %d em %s" % (len(entradas), DESTINO_ENUNCIADOS.relative_to(RAIZ)))
    return 0


def main() -> int:
    for passo in (sumario, enunciados):
        codigo = passo()
        if codigo:
            return codigo
    return 0


if __name__ == "__main__":
    sys.exit(main())
