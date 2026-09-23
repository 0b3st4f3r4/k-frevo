"""O estilo do texto: as marcas que a humanizacao corta, medidas antes de cortar.

Protocolo, e nao portao (AGENTS.md 9): nada aqui reprova nada. O que a ferramenta faz e
contar, para que a reescrita de voz parta de numero e nao de impressao -- e para que a
proxima sessao possa comparar o antes com o depois em vez de confiar na memoria.

As cinco marcas sao as que apareceram medidas no capitulo 1 da primeira versao:

  1. a **definicao por negacao** -- "nao ... : ...", a negacao virando definicao;
  2. a **definicao por antitese** -- "e o que", "e a pergunta que";
  3. o **epigrama em italico fechando secao** -- a frase de efeito no fim de cada secao;
  4. a **metafora unica** -- a palavra de conteudo que mais se repete, conduzida pelo texto;
  5. o **meta-comentario** -- o texto falando de si mesmo ("este livro", "neste capitulo").

A ferramenta automatica de estilo do ambiente nao substitui isto: o catalogo dela e de padroes
em ingles e chines, e a deteccao de idioma classifica qualquer texto latino como ingles --
"no mundo atual, e importante notar que" passa limpo, com aiScore 0. Medido, nao suposto.
"""
import pathlib
import re
import statistics as st
import sys

LIVRO = pathlib.Path("livro")
PARADAS = set("""a o as os um uma de do da das dos em no na nos nas por para com sem sob sobre
e ou mas que se como quando onde qual quais seu sua seus suas este esta estes estas esse essa
isso isto aquele aquela ao aos ja nao nem mais menos muito pouco todo toda todos todas entre
pelo pela pelos pelas ser sao foi era serao tem tinha ter ha havia pode podem poder fazer faz
feito cada outro outra mesmo mesma ainda tambem so apenas entao assim porque pois""".split())

MARCAS = (
    ("definicao por negacao", r"n[ãa]o\s[^.:]{0,70}:"),
    ("definicao por antitese", r"\b[EÉeé]\s(?:o|a)\s(?:que|pergunta|instrumento|conta|medida)\b"),
    ("meta-comentario sobre o livro", r"\b(?:este livro|neste cap[íi]tulo|ao longo deste|deste cap[íi]tulo)\b"),
)


def prosa(caminho: pathlib.Path) -> str:
    """O texto do capítulo sem comentários, sem matemática e sem comandos."""
    linhas = [re.sub(r"(?<!\\)%.*", "", l) for l in caminho.read_text(encoding="utf-8").splitlines()]
    t = "\n".join(linhas)
    t = re.sub(r"\\\[.*?\\\]", " ", t, flags=re.S)
    t = re.sub(r"\$[^$]*\$", " ", t)
    t = re.sub(r"\\includegraphics(?:\[[^]]*\])?\{[^}]+\}", " ", t)
    for _ in range(4):
        t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?\{([^{}]*)\}", r"\2", t)
    t = re.sub(r"\\[a-zA-Z]+\*?", " ", t)
    return re.sub(r"\s+", " ", re.sub(r"[{}~]", " ", t)).strip()


def epigrama(caminho: pathlib.Path) -> int:
    """Quantas seções fecham com uma frase em itálico: a batida de efeito no fim."""
    linhas = [re.sub(r"(?<!\\)%.*", "", l) for l in caminho.read_text(encoding="utf-8").splitlines()]
    dentro, fechos, ultimo = False, 0, ""
    for linha in linhas:
        if linha.startswith("\\section"):
            if re.match(r"\s*\\emph\{", ultimo):
                fechos += 1
            ultimo = ""
            continue
        if linha.strip():
            ultimo = linha
    if re.match(r"\s*\\emph\{", ultimo):
        fechos += 1
    return fechos


def medida(caminho: pathlib.Path) -> dict:
    texto = prosa(caminho)
    frases = [f for f in re.split(r"(?<=[.!?])\s+", texto) if len(f.split()) > 2]
    tamanhos = sorted(len(f.split()) for f in frases) or [0]
    palavras = re.findall(r"[a-záàâãéêíóôõúç]{4,}", texto.lower())
    contagem = {}
    for p in palavras:
        if p not in PARADAS:
            contagem[p] = contagem.get(p, 0) + 1
    return {
        "capitulo": caminho.stem,
        "palavras": len(texto.split()),
        "frases": len(frases),
        "palavras por frase": round(st.mean(tamanhos), 1),
        "mediana": int(st.median(tamanhos)),
        "ate cinco palavras (%)": round(100 * sum(1 for t in tamanhos if t <= 5) / len(tamanhos), 1),
        "negacao (%)": round(100 * len(re.findall(MARCAS[0][1], texto, flags=re.I)) / max(len(frases), 1), 1),
        "antitese": len(re.findall(MARCAS[1][1], texto, flags=re.I)),
        "meta": len(re.findall(MARCAS[2][1], texto, flags=re.I)),
        "epigrama de fecho": epigrama(caminho),
        "palavra condutora": (max(contagem, key=contagem.get), max(contagem.values())) if contagem else ("-", 0),
    }


def main(argumentos: list) -> int:
    alvos = [pathlib.Path(a) for a in argumentos] or sorted(LIVRO.glob("capitulos/*.tex"))
    if not alvos:
        print("nenhum capítulo encontrado")
        return 1
    linhas = [medida(a) for a in alvos]
    larguras = {"capitulo": 26, "palavra condutora": 22}
    for chave in linhas[0]:
        larguras[chave] = max(larguras.get(chave, len(chave)), *(len(str(l[chave])) for l in linhas))
    print(" | ".join(k.ljust(larguras[k]) for k in linhas[0]))
    for l in linhas:
        print(" | ".join(str(l[k]).ljust(larguras[k]) for k in l))
    print()
    print("protocolo, não portão: nada aqui reprova. O que reprova é a leitura — e o que a")
    print("leitura precisa é de número para saber onde olhar.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
