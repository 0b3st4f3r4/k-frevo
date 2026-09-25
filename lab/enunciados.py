r"""Os enunciados formais do livro: numero, titulo e pagina, na ordem de leitura.

**O sumario completo do fim saiu, e o motivo e a duplicata.** Ele era uma copia do .toc da
compilacao anterior, porque um segundo \tableofcontents no fim do documento sai vazio (o LaTeX
abre o .toc para escrita no comeco e o le de novo quando o comando aparece). O sumario do comeco
ja carrega o livro inteiro --- o .toc acumula as entradas do documento todo, Referencias e listas
incluidas ---, de modo que a copia do fim era o mesmo mapa impresso duas vezes.

**Os enunciados formais** saem do .aux, que e onde o LaTeX guarda o numero, a pagina e o titulo de
cada rotulo; a especie (proposicao, definicao) sai do fonte do capitulo, porque o .aux nao a diz.
O arquivo gerado e incluido com \input, e o portao o trata como gerado --- nao se edita a mao.

Uso: .venv/bin/python lab/enunciados.py   (depois de compilar o livro pelo menos uma vez)
"""
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
LIVRO = RAIZ / "livro"
AUX = LIVRO / "livro.aux"
DESTINO = LIVRO / "proposicoes.tex"

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
    linhas = ["% GERADO POR lab/enunciados.py — NÃO EDITE À MÃO.",
              "% Os enunciados numerados do livro, na ordem em que aparecem: número, título e página",
              "% saem do livro.aux da compilação anterior; a espécie sai do fonte do capítulo.", ""]
    for especie, numero, titulo, rotulo in entradas:
        nome = ESPECIES[especie]
        texto = "%s %s" % (nome, numero)
        if titulo:
            texto += " --- %s" % titulo
        linhas.append("\\noindent\\hyperref[%s]{\\textbf{%s}}\\dotfill\\ \\pageref{%s}\\par"
                      % (rotulo, texto, rotulo))
    DESTINO.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print("enunciados: %d em %s" % (len(entradas), DESTINO.relative_to(RAIZ)))
    return 0


def main() -> int:
    return enunciados()


if __name__ == "__main__":
    sys.exit(main())
