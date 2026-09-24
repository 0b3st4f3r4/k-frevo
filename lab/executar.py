#!/usr/bin/env python3
"""O laboratório: executa os cadernos de experimento e amarra o que eles medem ao livro.

**Um experimento é um caderno**, em `lab/experimentos/`, executável sozinho e com os
parâmetros no topo marcados `# <- brinque com:`. O caderno termina gravando
`lab/resultados/<id>.json` — um objeto por grandeza — e cada figura em dois formatos:
`.pdf` para o livro e `.png` para inspeção visual.

Este runner faz três coisas:

  (padrão)    executa os cadernos cuja fonte mudou e regenera numeros.tex
  --tudo      executa todos, mesmo os que estão em dia
  --check     não executa: falha se algum caderno estiver com resultado obsoleto

O critério de execução é o **hash da fonte das células de código** gravado em
`metadata.execucao_hash` do caderno, e não a presença de output: um output antigo tem a
mesma cara de um atual, e editar uma célula de markdown (o comentário sobre a figura, por
exemplo) não invalida nada. O diretório de trabalho do kernel é a raiz do projeto, então
os caminhos dentro do caderno são relativos à raiz.
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EXPERIMENTOS = RAIZ / "lab" / "experimentos"
RESULTADOS = RAIZ / "lab" / "resultados"
NUMEROS = RAIZ / "livro" / "numeros.tex"
FIGURAS = RAIZ / "livro" / "figuras"
LIVRO = RAIZ / "livro"
CONTRATO = RAIZ / "AGENTS.md"
GERADOS = {"numeros.tex", "fontes.tex"}

# Quirks do ambiente, herdados do arquivo: matplotlib não escreve em ~/.config, o cache do
# uv é read-only, e o espec de kernel chama "python" pelado — então o venv vai à frente.
os.environ.setdefault("MPLCONFIGDIR", "/tmp/mplcfg")
os.environ.setdefault("UV_CACHE_DIR", "/tmp/uv-cache")
os.environ["PATH"] = str(Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", "")
os.chdir(RAIZ)

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError


def hash_fonte(nb) -> str:
    fonte = "\n".join(c.source for c in nb.cells if c.cell_type == "code")
    return hashlib.sha256(fonte.encode("utf-8")).hexdigest()[:12]


def cadernos() -> list:
    if not EXPERIMENTOS.is_dir():
        return []
    return sorted(EXPERIMENTOS.glob("*.ipynb"))


def precisa(nb) -> bool:
    if nb.metadata.get("execucao_hash") != hash_fonte(nb):
        return True
    return any(c.get("execution_count") is None for c in nb.cells if c.cell_type == "code")


def executa(caminho: Path, nb) -> None:
    cliente = NotebookClient(nb, timeout=1800, kernel_name="python3",
                             resources={"metadata": {"path": str(RAIZ)}})
    cliente.execute()
    nb.metadata["execucao_hash"] = hash_fonte(nb)
    nbformat.write(nb, caminho)


def formata(valor) -> str:
    """Número em português: vírgula decimal, notação científica em LaTeX."""
    if isinstance(valor, bool):
        return "sim" if valor else "não"
    if isinstance(valor, dict) and "valor" in valor:
        corpo = formata(valor["valor"])
        if "erro" in valor:
            # o \pm sai em modo matematico proprio, de proposito: dentro de um $...$ maior
            # o comma ganha espaco de pontuacao e o valor vira "5, 139 +-" no papel, que
            # nao e como se escreve numero em portugues.
            corpo += " $\\pm$ " + formata(valor["erro"])
        return corpo
    if isinstance(valor, int):
        return "%d" % valor
    if isinstance(valor, float):
        texto = "%.4g" % valor
        if "e" in texto:
            # A notação científica sai em \ensuremath, e não em modo matemático cru: o livro cita
            # a grandeza no meio de uma frase, e um \times solto derruba a compilação. Defeito que
            # só apareceu quando a primeira grandeza pequena foi medida.
            mantissa, expoente = texto.split("e")
            return ("\\ensuremath{%s \\times 10^{%d}}"
                    % (mantissa.replace(".", ","), int(expoente)))
        return texto.replace(".", ",")
    return str(valor)


def comando(nome: str) -> str:
    r"""Nome de comando LaTeX para uma grandeza. Só letras, e por um motivo do TeX.

    O TeX termina o nome de um controle no primeiro caractere que não é letra: a chave
    "troca_t8_anos" viraria \numTrocaT8Anos, que o TeX lê como \numTrocaT seguido do texto
    "8Anos" — e o documento não compila. Um número dentro do nome tem de ser escrito por
    extenso ("troca_oito_anos"), e é isso que a recusa abaixo exige.
    """
    partes = [p for p in re.split(r"[^0-9A-Za-z]+", nome) if p]
    gerado = "num" + "".join(p[:1].upper() + p[1:] for p in partes)
    if not gerado.isalpha():
        raise ValueError("chave que vira %r não serve como comando LaTeX: o nome tem de ser "
                         "extenso (oito, nove, dois_mil_e_vinte)" % nome)
    return "\\num" + "".join(p[:1].upper() + p[1:] for p in partes)


def colhe() -> int:
    medidas, origem = {}, {}
    for caminho in sorted(RESULTADOS.glob("*.json")) if RESULTADOS.is_dir() else []:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        if not isinstance(dados, dict):
            print("%s: o resultado tem de ser um objeto JSON" % caminho.name)
            return 1
        for chave, valor in dados.items():
            if chave in medidas:
                print("chave repetida entre experimentos: %s (%s e %s)"
                      % (chave, origem[chave], caminho.stem))
                return 1
            medidas[chave], origem[chave] = valor, caminho.stem
    LIVRO.mkdir(exist_ok=True)
    linhas = ["% GERADO POR lab/executar.py — NÃO EDITE À MÃO.",
              "% Uma grandeza por caderno em lab/experimentos/; o livro cita, não digita.",
              ""]
    for chave in sorted(medidas):
        try:
            nome = comando(chave)
        except ValueError as erro:
            print("%s: %s" % (caminho.name, erro))
            return 1
        linhas.append("\\newcommand{%s}{%s}" % (nome, formata(medidas[chave])))
    NUMEROS.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print("experimentos: %d | grandezas: %d | %s escrito"
          % (len(cadernos()), len(medidas), NUMEROS.relative_to(RAIZ)))
    return 0


def roda(forcar: bool) -> int:
    for caminho in cadernos():
        nb = nbformat.read(caminho, as_version=4)
        if forcar or precisa(nb):
            print("executando %s" % caminho.name)
            try:
                executa(caminho, nb)
            except CellExecutionError as erro:
                print("caderno quebrou: %s" % caminho.name)
                print(str(erro).strip().splitlines()[-1][:200])
                return 1
        else:
            print("em dia     %s" % caminho.name)
    return colhe()


def arquivos_do_livro() -> list:
    """Toda fonte do livro, inclusive os capítulos em livro/capitulos/.

    Recursivo de propósito: enquanto capítulo e número moravam no mesmo nível, um glob de
    primeiro nível bastava. Com os capítulos em subpasta, ele deixa de conferir número,
    figura e dígito dentro deles — e deixa em silêncio, que é o pior jeito de deixar.
    """
    return [p for p in sorted(LIVRO.rglob("*.tex")) if p.name not in GERADOS]


def conferir_frescor(falhas: list) -> None:
    for caminho in cadernos():
        nb = nbformat.read(caminho, as_version=4)
        if precisa(nb):
            falhas.append("caderno com resultado obsoleto: %s — rode lab/executar.py"
                          % caminho.name)
        if not (RESULTADOS / (caminho.stem + ".json")).exists():
            falhas.append("caderno sem resultado gravado: %s" % caminho.name)


def conferir_numeros(avisos: list, falhas: list) -> None:
    definidos = set()
    if NUMEROS.exists():
        definidos = set(re.findall(r"\\newcommand\{\\(num[0-9A-Za-z]+)\}",
                                   NUMEROS.read_text(encoding="utf-8")))
    usados = {}
    for caminho in arquivos_do_livro():
        for n, linha in enumerate(caminho.read_text(encoding="utf-8").splitlines(), start=1):
            for nome in re.findall(r"\\(num[0-9A-Za-z]+)", linha):
                usados.setdefault(nome, []).append(
                    "%s:%d" % (caminho.relative_to(LIVRO).as_posix(), n))
    for nome, onde in sorted(usados.items()):
        if nome not in definidos:
            falhas.append("número citado e não medido: \\%s em %s" % (nome, ", ".join(onde)))
    for nome in sorted(definidos - set(usados)):
        avisos.append("medido e não citado: \\%s" % nome)


def conferir_comandos_orfaos(falhas: list) -> None:
    r"""Nome de comando sem a barra vira texto no papel, e ninguém reclama.

    O defeito nasce fora do LaTeX: quem monta o texto num idioma que interpreta \texttt{\textbackslash n}
    escreve \texttt{\textbackslash numAlgumaCoisa} e a barra some, deixando \texttt{umAlgumaCoisa} no lugar.
    O PDF sai, o log fica limpo, o portão da compilação passa e a frase impressa mostra o nome
    do comando em vez do número. Aconteceu três vezes nesta árvore, e a única linha de defesa
    que funcionou foi ler o texto depois de compilar. Esta conferência faz isso antes: nome com
    maiúscula no meio, seguido de chaves e sem barra antes, é comando órfão.
    """
    padrao = re.compile(r"(?<!\\)\b[a-z]+[A-Z][A-Za-z]*\{\}")
    for caminho in arquivos_do_livro():
        for n, linha in enumerate(caminho.read_text(encoding="utf-8").splitlines(), start=1):
            for achado in padrao.findall(linha):
                falhas.append("comando órfão, sem a barra, em %s:%d — %s"
                              % (caminho.relative_to(LIVRO).as_posix(), n, achado))


def conferir_rotulos(falhas: list) -> None:
    r"""Rótulo repetido quebra a referência sem quebrar a compilação, e é por isso que ele é portão.

    Com \texttt{\textbackslash label\{fig:formas\}} em dois lugares, o \texttt{\textbackslash cref} aponta para o
    último e o leitor é mandado para a figura errada. Nada falha: o log escreve "multiply
    defined", o PDF sai, e o portão de compilação --- que olha erro e referência indefinida ---
    não vê nada. Aconteceu de verdade: duas figuras de formas no mesmo capítulo, uma delas
    acrescentada depois, e só o log sabia.
    """
    vistos = {}
    for caminho in arquivos_do_livro():
        for n, linha in enumerate(caminho.read_text(encoding="utf-8").splitlines(), start=1):
            for rotulo in re.findall(r"\\label\{([^}]*)\}", linha):
                onde = "%s:%d" % (caminho.relative_to(LIVRO).as_posix(), n)
                if rotulo in vistos:
                    falhas.append("rótulo repetido: %s em %s e em %s"
                                  % (rotulo, vistos[rotulo], onde))
                vistos[rotulo] = onde


def conferir_marcacao(falhas: list) -> None:
    r"""Marcação de outro idioma vaza para o LaTeX e sai impressa, sem nada reclamar.

    O negrito de markdown, \texttt{**assim**}, é a forma de quem escreve texto em caderno ou em
    conversa. Dentro de um \texttt{.tex} ele não é marcação de nada: o LaTeX imprime os quatro
    asteriscos, no meio da frase, e o leitor recebe isso. Foram 51 pares em 14 capítulos antes
    desta conferência existir, e nenhum portão viu: a compilação sai limpa, não há referência
    indefinida, não há caixa estourada, o dígito digitado não tem a ver, e o comando órfão olha
    barra perdida, não asterisco. O defeito só apareceu quando o texto do PDF foi lido.

    A família é a mesma e vale inteira: crase de código, título de markdown, link em colchete
    e parêntese, riscado. Comentário fica de fora --- ali a marcação é do autor, e não do livro.
    """
    padroes = (
        ("negrito de markdown", r"\*\*"),
        ("crase de código", chr(96)),
        ("título de markdown", r"(?m)^\s*\#{1,6}\s"),
        ("link de markdown", r"\[[^\]]+\]\([^)]+\)"),
        ("riscado de markdown", r"~~"),
    )
    for caminho in arquivos_do_livro():
        texto = caminho.read_text(encoding="utf-8")
        linhas = [re.sub(r"(?<!\\)%.*", " ", l) for l in texto.splitlines()]
        onde = caminho.relative_to(LIVRO).as_posix()
        for _n, linha in enumerate(linhas, start=1):
            for nome, padrao in padroes:
                for achado in re.findall(padrao, linha):
                    falhas.append("%s em %s:%d — %s"
                                  % (nome, onde, _n, achado.strip()[:40]))


def conferir_figuras(avisos: list, falhas: list) -> None:
    citadas = set()
    for caminho in arquivos_do_livro():
        texto = caminho.read_text(encoding="utf-8")
        for valor in re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", texto):
            citadas.add(valor)
            if not (LIVRO / valor).exists():
                falhas.append("figura citada e inexistente: %s" % valor)
    geradas = set()
    if FIGURAS.is_dir():
        geradas = {p.relative_to(LIVRO).as_posix() for p in FIGURAS.glob("*.pdf")}
    for nome in sorted(geradas - citadas):
        avisos.append("figura medida e não citada: %s" % nome)
    for nome in sorted(citadas - geradas):
        avisos.append("figura citada que nenhum caderno gera: %s" % nome)


def conferir_nomes(falhas: list) -> None:
    r"""Sem babel, o LaTeX cunha os nomes em inglês e ninguém reclama.

    A distribuição local não traz os arquivos de idioma do português, então os nomes
    que o LaTeX e o cleveref inventam saem no idioma padrão: o livro imprimia
    \texttt{Figure 3.2:} em cima de legenda escrita em português, \texttt{Table 3.2}
    dentro de uma frase, e \texttt{September 24, 2026} na folha de rosto. Foram 43
    "Figure", 36 "Table" e a data inteira em inglês, em 110 páginas, com a compilação
    limpa e todos os portões satisfeitos.

    A troca à mão resolve o presente e não o futuro: um \texttt{\textbackslash cref} novo
    para um tipo que ninguém nomeou volta a imprimir em inglês, em silêncio. Esta
    conferência exige que todo tipo referenciado tenha nome declarado, e que os nomes
    fixos da classe estejam trocados.
    """
    fixos = ("contentsname", "chaptername", "bibname", "proofname", "figurename", "tablename")
    bruto = (LIVRO / "livro.tex").read_text(encoding="utf-8")
    fonte = "\n".join(re.sub(r"(?<!\\)%.*", " ", l) for l in bruto.splitlines())
    for nome in fixos:
        if not re.search(r"\\renewcommand\{\\%s\}" % nome, fonte):
            falhas.append("nome não trocado: \\%s sai em inglês" % nome)
    if re.search(r"\\today\b", fonte):
        falhas.append("\\today sem babel escreve o mês em inglês: use \\mesEmPortugues")

    tipos = {"fig": "figure", "tab": "table", "cap": "chapter", "sec": "section",
             "eq": "equation", "prop": "proposicao", "teo": "teorema", "lem": "lema",
             "cor": "corolario", "def": "definicao", "ex": "exemplo", "obs": "observacao"}
    usados = set()
    for caminho in arquivos_do_livro():
        for chaves in re.findall(r"\\[cC]ref\{([^}]*)\}", caminho.read_text(encoding="utf-8")):
            for chave in chaves.split(","):
                prefixo = chave.strip().split(":")[0]
                if prefixo:
                    usados.add(prefixo)
    for prefixo in sorted(usados):
        tipo = tipos.get(prefixo)
        if tipo is None:
            falhas.append("referência \\cref{%s:...} com prefixo desconhecido: "
                          "declare o tipo e o nome em livro.tex" % prefixo)
        else:
            # As duas formas são declarações separadas: o cleveref usa \crefname
            # para \cref e \Crefname para \Cref. Ter só uma deixa a outra em inglês.
            for forma in ("crefname", "Crefname"):
                if not re.search(r"\\%s\{%s\}" % (forma, tipo), fonte):
                    falhas.append("\\cref{%s:...} imprimiria o nome em inglês: "
                                  "falta \\%s{%s} em livro.tex" % (prefixo, forma, tipo))


def conferir_digitos(avisos: list) -> None:
    r"""Dígito no corpo do livro vira aviso: grandeza medida se cita, não se digita.

    A conferência precisa de três faxinas antes de olhar, senão acusa notação em vez de
    dado. Sai o argumento opcional (o 1,5em de um itemize), sai o comando que nomeia
    arquivo (\input, \includegraphics, que carregam "01" no nome) e sai o que está entre
    cifrões, onde $n+1$ é símbolo e não medição.

    O modo matemático não sai inteiro, porém: dele ainda se cobra o decimal com vírgula,
    que é justamente como este livro escreve grandeza medida. Sem isso, um número digitado
    à mão se esconderia entre cifrões — e o portão é para pegá-lo, não para ficar bonito.
    Quando o dígito é legítimo (exemplo mínimo, nome próprio), a própria linha o declara
    com "numeros-ok", de modo que a exceção fica escrita no lugar onde ela vale.
    """
    for caminho in arquivos_do_livro():
        linhas = caminho.read_text(encoding="utf-8").splitlines()
        # arquivo sem \begin{document} é fragmento de capítulo: tudo nele está dentro
        dentro = not any("\\begin{document}" in l for l in linhas)
        em_mostrador = False
        for n, linha in enumerate(linhas, start=1):
            if "\\begin{document}" in linha:
                dentro = True
                continue
            if not dentro or "numeros-ok" in linha:
                continue
            corpo = re.sub(r"(?<!\\)%.*", "", linha)
            corpo = re.sub(r"\\(num[0-9A-Za-z]+)", "", corpo)
            corpo = re.sub(r"\\includegraphics(?:\[[^]]*\])?\{[^}]+\}", "", corpo)
            corpo = re.sub(r"\\(?:input|include)\{[^}]+\}", "", corpo)
            # a chave de citação carrega o ano (oconnell2026extreme) e não é dígito digitado
            corpo = re.sub(r"\\cite[tp]?\{[^}]+\}", "", corpo)
            # rótulo de figura, tabela e equação nomeia objeto, não digita número
            corpo = re.sub(r"\\(?:label|ref|cref|Cref|eqref|autoref)\{[^}]+\}", "", corpo)

            abre, fecha = "\\[" in corpo, "\\]" in corpo
            if em_mostrador or abre:
                matematicas.append(corpo)
                corpo = ""
            else:
                matematicas = re.findall(r"\$[^$]*\$", corpo)
                corpo = re.sub(r"\$[^$]*\$", "", corpo)
            em_mostrador = (em_mostrador or abre) and not fecha

            digitos = len(re.findall(r"\d", re.sub(r"\[[^]]*\]", "", corpo)))
            dentro_da_matematica = sum(len(re.findall(r"\d+,\d+", m)) for m in matematicas)
            if digitos or dentro_da_matematica:
                avisos.append("dígito digitado à mão: %s:%d — %s"
                              % (caminho.relative_to(LIVRO).as_posix(), n, corpo.strip()[:80]
                                 or "no modo matemático"))


def conferir_cadernos_sem_algoritmo(avisos: list) -> None:
    """O caderno chama a biblioteca; se ele define função, o algoritmo ficou no lugar errado."""
    for caminho in cadernos():
        nb = nbformat.read(caminho, as_version=4)
        for n, celula in enumerate(nb.cells, start=1):
            if celula.cell_type != "code":
                continue
            achado = re.search(r"^\s*(def|class)\s+(\w+)", celula.source, flags=re.M)
            if achado:
                avisos.append("caderno %s define %s na célula %d — algoritmo mora em lib/frevolab/"
                              % (caminho.name, achado.group(2), n))


def conferir_perguntas(falhas: list) -> None:
    if not CONTRATO.exists():
        falhas.append("contrato ausente: AGENTS.md")
        return
    texto = CONTRATO.read_text(encoding="utf-8").splitlines()
    inicio = next((i for i, l in enumerate(texto) if l.startswith("### 5.2")), None)
    fim = next((i for i, l in enumerate(texto) if l.startswith("## 6.")), len(texto))
    if inicio is None:
        falhas.append("contrato sem a seção 5.2: não há lista de perguntas para conferir")
        return
    blocos, atual = {}, None
    for linha in texto[inicio:fim]:
        achado = re.match(r"^- \*\*([A-F][0-9]) — ", linha)
        if achado:
            atual = achado.group(1)
            blocos[atual] = linha
        elif atual:
            blocos[atual] += "\n" + linha
    for ident, corpo in blocos.items():
        for parte, padrao in (("medição", r"\*medição:\*"),
                              ("refuta", r"\*refuta(:| a construir:)\*"),
                              ("bate", r"\*bate:\*")):
            if not re.search(padrao, corpo):
                falhas.append("pergunta %s sem %s" % (ident, parte))
    print("perguntas no contrato: %d" % len(blocos))


def conferir_biblioteca(falhas: list) -> None:
    sys.path.insert(0, str(RAIZ / "lib"))
    try:
        import frevolab
    except Exception as erro:  # a biblioteca tem de importar antes de qualquer outra conta
        falhas.append("biblioteca não importa: %s" % erro)
        return
    problemas = frevolab.auto_teste()
    print("biblioteca frevolab %s | auto_teste: %s"
          % (frevolab.VERSAO, "limpo" if not problemas else "%d problema(s)" % len(problemas)))
    for problema in problemas:
        falhas.append("biblioteca: %s" % problema)


def check() -> int:
    avisos, falhas = [], []
    conferir_biblioteca(falhas)
    conferir_frescor(falhas)
    conferir_numeros(avisos, falhas)
    conferir_figuras(avisos, falhas)
    conferir_rotulos(falhas)
    conferir_comandos_orfaos(falhas)
    conferir_marcacao(falhas)
    conferir_nomes(falhas)
    conferir_digitos(avisos)
    conferir_cadernos_sem_algoritmo(avisos)
    conferir_perguntas(falhas)
    for a in avisos:
        print("  aviso: %s" % a)
    if falhas:
        print("auditoria: %d falha(s)" % len(falhas))
        for f in falhas:
            print("  - %s" % f)
        return 1
    print("auditoria: limpa")
    return 0


def main(argv: list) -> int:
    if "--check" in argv:
        return check()
    return roda(forcar="--tudo" in argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
