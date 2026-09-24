"""O estilo do texto: as marcas que a humanizacao corta, medidas antes de cortar.

Protocolo, e nao portao (AGENTS.md 9): nada aqui reprova nada. O que a ferramenta faz e
contar, para que a reescrita de voz parta de numero e nao de impressao -- e para que a proxima
sessao possa comparar o antes com o depois em vez de confiar na memoria.

Sao dois blocos, e eles medem coisas diferentes.

**As cinco marcas** sao as que apareceram medidas no capitulo 1 da primeira versao, e nenhuma
delas e cliche: sao *estrutura*.

  1. a **definicao por negacao** -- "nao ... : ...", a negacao virando definicao;
  2. a **definicao por antitese** -- "e o que", "e a pergunta que";
  3. o **epigrama em italico fechando secao** -- a frase de efeito no fim de cada secao;
  4. a **metafora unica** -- a palavra de conteudo que mais se repete, conduzida pelo texto;
  5. o **meta-comentario** -- o texto falando de si mesmo ("este livro", "neste capitulo").

**O catalogo de cliches** e o que a ferramenta automatica do ambiente nao tem. Ela casa padroes
em ingles e chines, e a deteccao de idioma dela classifica qualquer texto latino como ingles --
um paragrafo de portugues flagrante ("no mundo atual, e importante notar que... vamos
mergulhar...") passa com aiScore 0. Medido, nao suposto. Entao o catalogo portugues mora aqui,
no repositorio, versionado junto com o livro: as mesmas sete classes que a ferramenta usa
(abertura vazia, cliche, hesitacao, transicao de molde, fecho de resumo, paralelismo mecanico e
explicacao em excesso), escritas em portugues.

Cliche nao e o mesmo que marca: o cliche e a palavra gasta, e a marca e o movimento. Um texto
pode nao ter um unico cliche e ainda assim soar de maquina -- foi o caso do capitulo 1. Mas o
cliche e barato de contar, e um texto que acumula "e importante notar" e "em conclusao" tem
onde se pegar.
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
    # O molde e intra-oracional: a negacao define quando o dois-pontos explica o que ela
    # negou. Atravessar o ponto e virgula casava a negacao de uma oracao com o dois-pontos
    # da seguinte, que nao tem nada a ver com ela.
    ("definicao por negacao", r"n[ãa]o\s[^.;:]{0,70}:"),
    ("definicao por antitese", r"\b[Éé]\s(?:o|a)\s(?:que|pergunta|instrumento|conta|medida)\b"),
    ("meta-comentario sobre o livro", r"\b(?:este livro|neste cap[íi]tulo|ao longo deste|deste cap[íi]tulo)\b"),
)

CLICHES = (
    ("abertura vazia", (
        r"\bno mundo atual\b", r"\bnos dias de hoje\b", r"\bna era digital\b", r"\bem plena era\b",
        r"\bcom o avan[cç]o (?:da|das) tecnologi", r"\bcada vez mais\b", r"\bcomo todos sabem\b",
        r"\bn[ãa]o [ée] segredo que\b", r"\bvamos mergulhar\b", r"\bsem mais delongas\b",
        r"\bd[ií]as atuais\b", r"\bem um mundo cada vez\b",
    )),
    ("cliche de novidade", (
        # "de ponta a ponta" e locucao, e o padrao antigo casava a locucao inteira: contava
        # cliche em dois capitulos que nao tem nenhum. O cliche e "de ponta" sozinho.
        r"\brevolucion\w+", r"\bmudar o jogo\b", r"\bdivisor de [áa]guas\b", r"\bde ponta\b(?!\s+a\s+ponta\b)",
        r"\bestado da arte\b", r"\bsolu[cç][ãa]o robusta\b", r"\babordagem hol[íi]stica\b",
        r"\bsinergia\w*", r"\balavanc(?:ar|ando|agem|aram)\b", r"\bdesvendar o potencial\b", r"\bum marco\b",
        r"\becossistema vibrante\b", r"\bpilar fundamental\b", r"\bprotagonista\b",
    )),
    ("hesitacao", (
        r"\b[ée] importante (?:notar|destacar|ressaltar|salientar|frisar|lembrar)\b",
        r"\bvale (?:notar|destacar|ressaltar|salientar|lembrar|frisar)\b",
        r"\bde certa forma\b", r"\bem certo sentido\b", r"\bat[ée] certo ponto\b",
        r"\bpode-se dizer que\b", r"\bde modo geral\b", r"\bbasicamente\b", r"\bessencialmente\b",
        r"\bsem d[úu]vida\b", r"\b[ée] sabido que\b",
    )),
    ("transicao de molde", (
        r"(?:^|[.;:]\s)al[ée]m disso\b", r"(?:^|[.;:]\s)por outro lado\b", r"\bpor sua vez\b",
        r"(?:^|[.;:]\s)dessa forma\b", r"(?:^|[.;:]\s)sendo assim\b", r"(?:^|[.;:]\s)dessa maneira\b",
        r"(?:^|[.;:]\s)em primeiro lugar\b", r"(?:^|[.;:]\s)primeiramente\b", r"(?:^|[.;:]\s)por fim\b",
        r"(?:^|[.;:]\s)dessa perspectiva\b",
    )),
    ("fecho de resumo", (
        r"\bem conclus[ãa]o\b", r"\bpara concluir\b", r"\bconcluindo\b", r"\bem resumo\b",
        r"\bem s[íi]ntese\b", r"\bcomo vimos\b", r"\bcomo pudemos ver\b", r"\bem [úu]ltima an[áa]lise\b",
        r"\bresumindo\b", r"\bde modo que podemos afirmar\b",
    )),
    ("paralelismo mecanico", (
        r"\bn[ãa]o s[óo]\b[^.]{0,60}\bmas tamb[ée]m\b", r"\bpor um lado\b[^.]{0,80}\bpor outro\b",
        r"\btanto\b[^.]{0,60}\bquanto\b[^.]{0,60}\be ainda\b", r"\bseja\b[^.]{0,40}\bseja\b[^.]{0,40}\bseja\b",
    )),
    ("explicacao em excesso", (
        r"\bou seja,\s", r"\bisto [ée],\s", r"\bem outras palavras,\s", r"\bquer dizer,\s",
        r"\bo que significa que\b", r"\b[ée] importante entender que\b", r"\bem termos pr[áa]ticos,\s",
    )),
)


def prosa(caminho: pathlib.Path) -> str:
    """O texto do capítulo sem comentários, sem matemática e sem comandos."""
    linhas = [re.sub(r"(?<!\\)%.*", "", l) for l in caminho.read_text(encoding="utf-8").splitlines()]
    t = "\n".join(linhas)
    t = re.sub(r"\\\[.*?\\\]", " ", t, flags=re.S)
    t = re.sub(r"\$[^$]*\$", " ", t)
    # Comandos que nomeiam objeto: o nome e rotulo, nao prosa. Despejar o argumento no
    # texto (como o desembrulho generico faz) inventa palavra e chega a inventar marca --
    # "nao ve o que nao esta na serie cap:" era o rotulo cap:dependencia_vigiada.
    t = re.sub(
        r"\\(?:label|cref|Cref|ref|eqref|autoref|cite|citep|citet|citealp|citeauthor|citeyear"
        r"|includegraphics|input|index)(?:\[[^]]*\])?\{[^}]*\}",
        " ",
        t,
    )
    for _ in range(4):
        t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?\{([^{}]*)\}", r"\2", t)
    t = re.sub(r"\\[a-zA-Z]+\*?", " ", t)
    return re.sub(r"\s+", " ", re.sub(r"[{}~]", " ", t)).strip()


def epigrama(caminho: pathlib.Path) -> int:
    """Quantas seções fecham com uma frase em itálico: a batida de efeito no fim."""
    linhas = [re.sub(r"(?<!\\)%.*", "", l) for l in caminho.read_text(encoding="utf-8").splitlines()]
    fechos, ultimo = 0, ""
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


def cliches(texto: str) -> dict:
    """Quantos clichês de cada classe, e quais foram: o leitor decide o que fazer com eles."""
    achados = {}
    for classe, padroes in CLICHES:
        ocorrencias = []
        for padrao in padroes:
            ocorrencias += [m.group(0).lower().strip() for m in re.finditer(padrao, texto, flags=re.I)]
        achados[classe] = ocorrencias
    return achados


def medida(caminho: pathlib.Path) -> dict:
    texto = prosa(caminho)
    frases = [f for f in re.split(r"(?<=[.!?])\s+", texto) if len(f.split()) > 2]
    tamanhos = sorted(len(f.split()) for f in frases) or [0]
    palavras = re.findall(r"[a-záàâãéêíóôõúç]{4,}", texto.lower())
    contagem = {}
    for p in palavras:
        if p not in PARADAS:
            contagem[p] = contagem.get(p, 0) + 1
    achados = cliches(texto)
    return {
        "capitulo": caminho.stem,
        "palavras": len(texto.split()),
        "palavras por frase": round(st.mean(tamanhos), 1),
        "ate cinco palavras (%)": round(100 * sum(1 for t in tamanhos if t <= 5) / len(tamanhos), 1),
        "negacao (%)": round(100 * len(re.findall(MARCAS[0][1], texto, flags=re.I)) / max(len(frases), 1), 1),
        "antitese": len(re.findall(MARCAS[1][1], texto, flags=re.I)),
        "meta": len(re.findall(MARCAS[2][1], texto, flags=re.I)),
        "epigrama": epigrama(caminho),
        "palavra condutora": (max(contagem, key=contagem.get), max(contagem.values())) if contagem else ("-", 0),
        "cliches": sum(len(v) for v in achados.values()),
        "cliches por mil palavras": round(1000 * sum(len(v) for v in achados.values()) / max(len(texto.split()), 1), 1),
        "achados": achados,
    }


def imprime(linhas: list) -> None:
    colunas = ("capitulo", "palavras", "palavras por frase", "ate cinco palavras (%)", "negacao (%)",
               "antitese", "meta", "epigrama", "palavra condutora", "cliches", "cliches por mil palavras")
    larguras = {c: max(len(c), *(len(str(l[c])) for l in linhas)) for c in colunas}
    print(" | ".join(c.ljust(larguras[c]) for c in colunas))
    for l in linhas:
        print(" | ".join(str(l[c]).ljust(larguras[c]) for c in colunas))
    print()
    for l in linhas:
        achados = {c: v for c, v in l["achados"].items() if v}
        if not achados:
            print("%s: nenhum cliche do catalogo" % l["capitulo"])
            continue
        print("%s:" % l["capitulo"])
        for classe, ocorrencias in achados.items():
            distintos = sorted(set(ocorrencias))
            print("   %-22s %d  %s" % (classe, len(ocorrencias), ", ".join(distintos[:8])))
    print()
    print("protocolo, nao portao: nada aqui reprova. O cliche e a palavra gasta; a marca e o")
    print("movimento -- e um texto pode nao ter cliche nenhum e ainda assim soar de maquina.")


def main(argumentos: list) -> int:
    # O livro.tex entra na medida: é onde vivem a introdução, a conclusão e as notas de parte ---
    # o primeiro e o último texto que o leitor encontra, e o único que ficava fora da régua.
    alvos = [pathlib.Path(a) for a in argumentos] or (
        sorted(LIVRO.glob("capitulos/*.tex")) + [LIVRO / "livro.tex"])
    if not alvos:
        print("nenhum capítulo encontrado")
        return 1
    imprime([medida(a) for a in alvos])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
