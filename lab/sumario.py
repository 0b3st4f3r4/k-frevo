
r"""O sumário completo, no fim do livro: uma copia do .toc da compilacao anterior.

**Por que uma copia, e nao um segundo \tableofcontents.** O LaTeX abre o .toc para escrita no
comeco da compilacao e o le de novo quando encontra um \tableofcontents --- e no fim do documento
o arquivo ainda esta pela metade: o segundo sumario sai **vazio**, conferido na pagina. Copiar o
.toc da compilacao anterior resolve, e nao custa passada extra: o sumario completo e a ultima
coisa do livro, de modo que as paginas que ele cita nao se movem quando ele entra.

Uso: .venv/bin/python lab/sumario.py   (depois de compilar o livro pelo menos uma vez)
"""
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
TOC = RAIZ / "livro" / "livro.toc"
DESTINO = RAIZ / "livro" / "sumario.tex"

# Os niveis que entram: parte, capitulo e secao. Subsecao nao existe no livro, e se aparecer
# fica de fora por decisao --- o sumario do fim serve para achar capitulo e secao.
NIVEIS = ("part", "chapter", "section")


def gera() -> int:
    if not TOC.exists():
        print("o livro ainda nao foi compilado: falta %s" % TOC.name)
        return 1
    linhas = []
    for linha in TOC.read_text(encoding="utf-8").splitlines():
        achado = re.match(r"\\contentsline \{(part|chapter|section)\}", linha)
        if achado:
            linhas.append(linha)
    if not linhas:
        print("o .toc nao tem entradas: compile o livro antes")
        return 1
    DESTINO.write_text(
        "% GERADO POR lab/sumario.py — NÃO EDITE À MÃO.\n"
        "% Uma cópia do livro.toc da compilação anterior: o segundo \\tableofcontents no fim\n"
        "% do documento sai vazio, porque o arquivo ainda está sendo escrito.\n"
        + "\n".join(linhas) + "\n", encoding="utf-8")
    print("sumário completo: %d entradas em %s" % (len(linhas), DESTINO.relative_to(RAIZ)))
    return 0


if __name__ == "__main__":
    sys.exit(gera())
