#!/usr/bin/env python3
r"""O aterramento: onde cada objeto do livro é construído, e a fila do que ainda falta.

O §3.4 do contrato pede **definição, intuição e exemplo numérico mínimo, nesta ordem, em toda
seção**; o §3.5 proíbe símbolo antes de ter nome, motivo e exemplo. As duas regras valem desde o
começo do projeto e nunca tiveram portão --- e sem portão elas derivam em silêncio, que é o que
aconteceu com o `Figure` em inglês, com o dígito digitado e com o `\cref` que imprimia o nome
errado.

O que a varredura mostrou, e é o motivo desta ferramenta existir: o livro mede com máquinas que
nunca constrói. Ele sorteia mundos inteiros, tira média de muitos sorteios, usa decaimento
geométrico, ponto fixo, variância e curtose --- e `variável aleatória`, `densidade`,
`covariância`, `lei dos grandes números`, `teorema central do limite`, `derivada`, `integral`,
`simulação` e `semente` não aparecem em página nenhuma. A `esperança` entra no capítulo 17,
dentro da recursão do GARCH; a `variância` no 11, dentro da proposição do piso; a `curtose` no 18, em cabeçalho de tabela.

**O registro.** `dados/aterramento.tsv` é curadoria manual, como o corpus de fontes: uma linha
por objeto, e nada mais que id, nome, tipo, padrão de busca, onde aterrou, o que exige e onde
está o exemplo mínimo. O registro guarda **endereço, nunca definição** --- a prosa vive só no
capítulo, e não existe segunda cópia para divergir (é a mesma razão de o livro citar
`numeros.tex` em vez de digitar o número).

**A âncora.** O objeto aterrado traz, no capítulo declarado, a linha `% aterramento: <id>`.
Uma âncora só e um mecanismo só: dois jeitos de marcar viram dois jeitos de esquecer.

**A fila.** `aterrou` pode ser `-`: o objeto está na fila, ainda sem aterramento declarado. A
fila não é falha e é **aviso em toda execução**, porque o que o portão não pode deixar é o
objeto aparecer no livro sem estar nem aterrado nem declarado na fila --- que é o estado em que
o livro passou vinte capítulos.

**A ordem de leitura não é a ordem dos arquivos.** A nota de abertura e as notas de parte vivem
em `livro.tex`, e a nota de cada parte fica **antes** do primeiro capítulo dela e **depois** do
último do anterior. Tratar `livro.tex` inteiro como anterior a tudo daria falso positivo no
objeto que a nota da parte cita já aterrado muitos capítulos antes. Por isso a leitura é fatiada
na ordem dos `\input`: cada pedaço de `livro.tex` entra na posição em que o leitor o encontra.

**Portão e medidor, e a divisão importa.** O portão mora em `lab/executar.py`
(`conferir_aterramento`) e chama `conferir()` daqui; o medidor é o `--medir`, que **não reprova
nada** (irmão do `lab/estilo.py`): a contagem diz onde olhar, e a leitura decide.
"""
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
LIVRO = RAIZ / "livro"
CAPITULOS = LIVRO / "capitulos"
REGISTRO = RAIZ / "dados" / "aterramento.tsv"

COLUNAS = ("id", "nome", "tipo", "padrao", "aterrou", "exige", "exemplo")
TIPOS = ("simbolo", "termo")

# Os comandos de matemática que são **operação** ou tipografia, e não objeto do livro. A lista é
# declarada, e não implícita: um comando novo que não esteja nem aqui nem no registro aparece na
# varredura, que é o único jeito de ele não entrar em silêncio.
OPERADORES = {
    r"\dfrac", r"\frac", r"\tfrac", r"\sqrt", r"\log", r"\ln", r"\exp", r"\to", r"\cdot",
    r"\cdots", r"\ldots", r"\dots", r"\geq", r"\leq", r"\ge", r"\le", r"\neq", r"\pm",
    r"\Big", r"\big", r"\Bigl", r"\Bigr", r"\bigl", r"\bigr", r"\left", r"\right",
    r"\text", r"\mathrm", r"\mathbb", r"\mathcal", r"\operatorname", r"\hat", r"\bar",
    r"\tilde", r"\widehat", r"\widetilde", r"\sum", r"\prod", r"\int", r"\infty",
    r"\approx", r"\sim", r"\equiv", r"\times", r"\div", r"\quad", r"\qquad", r"\hspace",
    r"\phantom", r"\ensuremath", r"\ast", r"\star",
    # \begin e \end sao ESTRUTURA, e nao simbolo: um ambiente de matriz nao pede
    # aterramento. Sem esta linha, \begin{pmatrix} reprovava como simbolo nao registrado.
    # \bm e negrito de matematica, e \in e o sinal de pertinencia: os dois sao notacao, e nao
    # objeto do livro. A lista abaixo e a mesma familia de \mathbb e \mathrm.
    r"\bm", r"\in",
    r"\begin", r"\end",
}

# O que aparece em modo matemático e **não é matemática**: rótulo, citação, nome de arquivo e
# grandeza medida. A grandeza medida entra aqui de propósito --- ela é número com nome, e quem
# manda nela é o `numeros.tex`. O `\num` sai com ou sem chaves, porque o livro usa os dois.
NAO_MATEMATICA = re.compile(
    r"\\(?:label|cref|Cref|ref|eqref|cite|citep|citet|includegraphics)(?:\[[^\]]*\])?\{[^}]*\}"
)
GRANDEZA = re.compile(r"\\num[A-Za-z]*(?:\[[^\]]*\])?(?:\{[^}]*\})?")

MATH = re.compile(r"\$[^$]*\$|\\\[.*?\\\]", re.S)
MARCADOR = "%% aterramento: %s"


def trechos() -> list:
    r"""A ordem de leitura: cada pedaço de `livro.tex` na posição em que o leitor o encontra.

    Devolve `(rótulo, texto)`: o rótulo é o nome do capítulo ou `livro.tex`. O pedaço de
    `livro.tex` que vem antes do primeiro `\input` traz o preâmbulo, a folha de rosto, o sumário
    e a nota de abertura; os outros trazem a nota da parte que abre cada movimento.
    """
    fonte = (LIVRO / "livro.tex").read_text(encoding="utf-8")
    pedacos = re.split(r"\\input\{capitulos/([^}]+)\}", fonte)
    saida = [("livro.tex", pedacos[0])]
    for i in range(1, len(pedacos), 2):
        nome = re.sub(r"\.tex$", "", pedacos[i])
        saida.append((nome, (CAPITULOS / (nome + ".tex")).read_text(encoding="utf-8")))
        saida.append(("livro.tex", pedacos[i + 1]))
    return saida


def capitulos() -> list:
    r"""Os capítulos na ordem de leitura, que é a ordem do `\input` e não a do nome do arquivo."""
    return [rotulo for rotulo, _ in trechos() if rotulo != "livro.tex"]


def indice_do_capitulo(numero: int) -> int:
    """O trecho do capítulo de número impresso `numero` (1 é o primeiro)."""
    vistos = 0
    for indice, (rotulo, _) in enumerate(trechos()):
        if rotulo == "livro.tex":
            continue
        vistos += 1
        if vistos == numero:
            return indice
    raise IndexError("o livro não tem capítulo %d" % numero)


def sem_comentario(texto: str) -> str:
    return "\n".join(re.sub(r"(?<!\\)%.*", "", linha) for linha in texto.splitlines())


# O que esta dentro de um \text{} e prosa: em "$\text{a soma das duas}$" o "a" e artigo, e nao
# o simbolo do coeficiente de memoria. Sem esta linha o portao acusava uso antes de aterrar num
# artigo de duas letras.
PROSA_NA_MATEMATICA = re.compile(r"\\text\{[^}]*\}")


def sem_matematica(linha: str) -> str:
    return PROSA_NA_MATEMATICA.sub(" ", GRANDEZA.sub(" ", NAO_MATEMATICA.sub(" ", linha)))


def linha_limpa(linha: str) -> str:
    """A linha sem comentário, sem matemática e sem os comandos que nomeiam objeto.

    É mais estreita que o `prosa()` do `lab/estilo.py` de propósito: aqui a posição na linha
    importa, e é ela que decide se o objeto aparece antes ou depois da âncora. O desembrulho de
    argumento que o medidor de voz faz não muda onde o termo está.
    """
    return sem_matematica(MATH.sub(" ", re.sub(r"(?<!\\)%.*", "", linha)))


def simbolos(texto: str) -> set:
    """Todo símbolo de matemática do texto: letra solta, letra grega e comando não-operador."""
    achados = set()
    for trecho in MATH.findall(sem_comentario(texto)):
        trecho = sem_matematica(trecho)
        for achado in re.finditer(r"\\[a-zA-Z]+", trecho):
            if achado.group(0) not in OPERADORES:
                achados.add(achado.group(0))
        for achado in re.finditer(r"(?<![\\a-zA-Z])([a-zA-Z])(?![a-zA-Z])", trecho):
            achados.add(achado.group(1))
    return achados


def registro() -> tuple:
    """As linhas do registro, já conferidas na forma. Devolve `(linhas, defeitos)`."""
    if not REGISTRO.exists():
        return [], ["registro ausente: %s" % REGISTRO.relative_to(RAIZ)]
    defeitos, linhas, vistos = [], [], {}
    for numero, linha in enumerate(REGISTRO.read_text(encoding="utf-8").splitlines(), 1):
        if not linha.strip() or linha.lstrip().startswith("#"):
            continue
        campos = linha.split("\t")
        if len(campos) != len(COLUNAS):
            defeitos.append("registro linha %d: %d campos, esperado %d (%s)"
                            % (numero, len(campos), len(COLUNAS), " | ".join(COLUNAS)))
            continue
        item = dict(zip(COLUNAS, (c.strip() for c in campos)))
        if item["id"] in vistos:
            defeitos.append("registro linha %d: id repetido (%s, também na linha %d)"
                            % (numero, item["id"], vistos[item["id"]]))
            continue
        vistos[item["id"]] = numero
        if item["tipo"] not in TIPOS:
            defeitos.append("registro linha %d: tipo %r não é símbolo nem termo"
                            % (numero, item["tipo"]))
        if not item["padrao"]:
            defeitos.append("registro linha %d: sem padrão de busca" % numero)
        linhas.append(item)
    return linhas, defeitos


def matematica_por_linha(texto: str) -> dict:
    r"""A matemática de cada linha, com o bloco «\[ ... \]» contado linha por linha.

    A primeira versão desta ferramenta varria a linha isolada e por isso **não via** nada
    dentro de um bloco que atravessa linhas: o «r» do retorno, declarado em três linhas,
    contava como entrada morta e o portão acusava um objeto que está no livro. Cada pedaço do
    bloco é atribuído à linha em que ele está, e não à linha em que o bloco começa --- senão a
    âncora e o uso comparariam posições que o leitor não vê.
    """
    limpo = sem_comentario(texto)
    por_linha = {}
    for achado in MATH.finditer(limpo):
        base = limpo.count("\n", 0, achado.start())
        for deslocamento, pedaco in enumerate(achado.group(0).splitlines()):
            por_linha.setdefault(base + deslocamento + 1, []).append(pedaco)
    return por_linha


def casa_simbolo(matematicos: list, padrao: str) -> bool:
    """O símbolo aparece **em modo matemático** aqui? Em prosa, `a` é artigo."""
    limpos = [sem_matematica(t) for t in matematicos]
    if padrao.startswith("\\"):
        return any(padrao in t for t in limpos)
    return any(re.search(r"(?<![\\a-zA-Z])%s(?![a-zA-Z])" % re.escape(padrao), t)
               for t in limpos)


def primeira_ocorrencia(padrao: str, tipo: str):
    """A primeira aparição do objeto na ordem de leitura: `(trecho, linha, rótulo)`.

    Símbolo é procurado como símbolo e termo como texto: procurar símbolo em prosa casaria `a`
    em qualquer artigo, e procurar termo em matemática não casaria nada.
    """
    for indice, (rotulo, texto) in enumerate(trechos()):
        matematicos = matematica_por_linha(texto)
        for numero, linha in enumerate(texto.splitlines(), 1):
            achou = (casa_simbolo(matematicos.get(numero, []), padrao) if tipo == "simbolo"
                     else re.search(padrao, linha_limpa(linha), flags=re.I) is not None)
            if achou:
                return indice, numero, rotulo
    return None


def posicao_marcador(ident: str, numero_capitulo: int):
    """A linha da âncora do objeto, no capítulo declarado."""
    texto = trechos()[indice_do_capitulo(numero_capitulo)][1]
    alvo = MARCADOR % ident
    for numero, linha in enumerate(texto.splitlines(), 1):
        if linha.strip() == alvo:
            return numero
    return None


def capitulo_do_trecho(indice: int):
    """O número impresso do capítulo que ocupa este trecho; `None` se o trecho é do livro.tex."""
    vistos = 0
    for i, (rotulo, _) in enumerate(trechos()):
        if rotulo == "livro.tex":
            continue
        vistos += 1
        if i == indice:
            return vistos
    return None


def conferir(falhas: list, avisos: list) -> None:
    r"""O portão: o objeto não aparece antes de aterrar, nem aparece sem estar declarado.

    Cinco ramos, e cada um existe porque o contrário é defeito de página: símbolo sem registro
    (o §3.5 rompido em silêncio), entrada morta (registro que mente sobre o objeto), uso antes da
    âncora (o §4 rompido), pré-requisito fora de ordem (o capítulo constrói com o que não tem) e
    numeração fora de lugar (o nome do arquivo deixou de dizer onde o capítulo está).
    """
    linhas, defeitos = registro()
    falhas += defeitos
    por_id = {l["id"]: l for l in linhas}

    conhecidos = set(OPERADORES)
    for item in linhas:
        if item["tipo"] == "simbolo":
            conhecidos.add(item["padrao"])

    vistos_no_livro = set()
    for _, texto in trechos():
        vistos_no_livro |= simbolos(texto)
    for simbolo in sorted(vistos_no_livro - conhecidos):
        falhas.append("símbolo %s aparece no livro e não está no registro (§3.5): declare o nome, "
                      "o motivo e o exemplo" % simbolo)

    # Ramo da renumeração: o número no nome do arquivo é a posição do capítulo no livro.
    # Ele existe porque inserir um capítulo antes da raiz move todos os outros uma casa, e o
    # deslocamento deixa nome antigo para trás em silêncio --- foi assim que o capítulo 2 virou
    # dois e os capítulos 3 a 19 andaram uma casa sem que nada conferisse.
    for posicao, nome in enumerate(capitulos(), 1):
        achado = re.match(r"^(\d+)_", nome)
        if achado is None:
            falhas.append("numeração: %s não tem número no nome — o nome do arquivo é a posição "
                          "do capítulo na ordem de leitura" % nome)
        elif int(achado.group(1)) != posicao:
            falhas.append("numeração fora de lugar: %s é o capítulo %d da ordem de leitura e o "
                          "nome diz %s" % (nome, posicao, achado.group(1)))

    na_fila, ativos = [], []
    for item in linhas:
        achado = primeira_ocorrencia(item["padrao"], item["tipo"])
        if achado is None:
            falhas.append("registro: %s (%s) não aparece no livro — entrada morta mente sobre o "
                          "objeto" % (item["id"], item["padrao"]))
            continue
        if item["aterrou"] == "-":
            na_fila.append(item)
            continue
        if not item["aterrou"].isdigit():
            falhas.append("registro: %s tem aterrou=%r, que não é número nem '-'"
                          % (item["id"], item["aterrou"]))
            continue
        numero_capitulo = int(item["aterrou"])
        if not 1 <= numero_capitulo <= len(capitulos()):
            falhas.append("registro: %s declara aterrar no capítulo %s, e o livro tem %d capítulos"
                          % (item["id"], item["aterrou"], len(capitulos())))
            continue
        linha_marcador = posicao_marcador(item["id"], numero_capitulo)
        if linha_marcador is None:
            falhas.append("registro: %s declara aterrar no capítulo %s e a âncora %r não está lá"
                          % (item["id"], item["aterrou"], MARCADOR % item["id"]))
            continue
        posicao_ancora = (indice_do_capitulo(numero_capitulo), linha_marcador)
        # A ordem conferida é a de **capítulo**, e não a de linha dentro dele. O §4 manda cada
        # capítulo abrir num fracasso concreto, e o fracasso nomeia o objeto antes de construí-lo
        # --- «a média diz 42,86% aqui e 54,76% ali» abre o capítulo que depois define a média.
        # Isso é a forma do livro, não defeito dele; o que o portão não pode deixar passar é o
        # objeto usado num capítulo **anterior** ao que o aterrou.
        if achado[2] == "livro.tex":
            # A nota de abertura e as notas de parte nomeiam o que vem: elas não constroem nada,
            # e por isso o portão não cobra delas a ordem. O que ele cobra é que os **capítulos**
            # respeitem a ordem --- é neles que o objeto ganha nome, motivo e exemplo.
            pass
        elif achado[0] < posicao_ancora[0]:
            falhas.append("uso antes de aterrar: %s aparece em %s linha %d e só é aterrado em %s, "
                          "mais adiante (§4)" % (item["id"], achado[2], achado[1],
                                                 capitulos()[numero_capitulo - 1]))
        ativos.append((item, posicao_ancora))

    for item, posicao_ancora in ativos:
        for exigido in [e.strip() for e in item["exige"].split(",") if e.strip()]:
            outro = por_id.get(exigido)
            if outro is None:
                falhas.append("registro: %s exige %s, que não está no registro"
                              % (item["id"], exigido))
                continue
            if outro["aterrou"] == "-":
                falhas.append("registro: %s exige %s, que está na fila" % (item["id"], exigido))
                continue
            outro_capitulo = int(outro["aterrou"])
            # A comparação é de capítulo, pela mesma razão do uso: dois objetos do mesmo capítulo
            # se aterram na ordem em que o texto os constrói, e a linha exata disso é do autor.
            if indice_do_capitulo(outro_capitulo) > posicao_ancora[0]:
                falhas.append("pré-requisito fora de ordem: %s aterrou antes de %s, que ele exige"
                              % (item["id"], exigido))

    if na_fila:
        # A fila inteira em toda execução afogaria o resto do log; o que não pode é ela passar
        # em silêncio, então o aviso traz o tamanho, os primeiros nomes e o que ficou de fora.
        nomes = [i["id"] for i in na_fila]
        mostrados = ", ".join(nomes[:8])
        if len(nomes) > 8:
            mostrados += " (e mais %d)" % (len(nomes) - 8)
        avisos.append("aterramento: %d objeto(s) na fila, ainda sem âncora declarada: %s"
                      % (len(na_fila), mostrados))
    print("aterramento: %d objetos no registro (%d aterrados, %d na fila)"
          % (len(linhas), len(ativos), len(na_fila)))


def inventario() -> int:
    """O que o livro usa, trecho por trecho, e onde cada objeto cai na ordem de leitura."""
    linhas, defeitos = registro()
    for defeito in defeitos:
        print(defeito)
    por_trecho = {}
    for item in linhas:
        achado = primeira_ocorrencia(item["padrao"], item["tipo"])
        if achado is not None:
            por_trecho.setdefault(achado[0], []).append((achado[1], item))
    for indice, (rotulo, texto) in enumerate(trechos()):
        print("\n== %2d %s — %d símbolo(s) de matemática" % (indice, rotulo, len(simbolos(texto))))
        for numero, item in sorted(por_trecho.get(indice, [])):
            estado = ("aterrado no cap. %s" % item["aterrou"]) if item["aterrou"] != "-" else "NA FILA"
            print("   L%-5d %-26s %-18s %s" % (numero, item["id"], estado, item["nome"]))
    return 0


def medir() -> int:
    r"""O medidor: o que cada capítulo carrega, sem reprovar nada.

    O que ele conta é objetivo: quantos objetos o capítulo aterrou, quantos ele usa sem
    aterramento, e por seção se há definição, proposição e número medido. É a mesma divisão do
    medidor de voz do `lab/estilo.py`: a contagem diz onde olhar, a leitura decide o que fazer.
    """
    linhas, _ = registro()
    ancoras, fila = {}, {}
    for item in linhas:
        if item["aterrou"] != "-":
            ancoras.setdefault(int(item["aterrou"]), []).append(item["id"])
            continue
        achado = primeira_ocorrencia(item["padrao"], item["tipo"])
        if achado is not None:
            numero = capitulo_do_trecho(achado[0])
            if numero:
                fila.setdefault(numero, []).append(item["id"])
    print("%-38s %6s %6s %6s %6s %6s %6s %6s"
          % ("capítulo", "pala", "seç", "aterr", "fila", "defin", "prop", "medid"))
    for numero, rotulo in enumerate(capitulos(), 1):
        fonte = trechos()[indice_do_capitulo(numero)][1]
        secoes = re.split(r"\\section\{", fonte)[1:]
        print("%-38s %6d %6d %6d %6d %6d %6d %6d"
              % (rotulo[:38], len(fonte.split()), len(secoes),
                 len(ancoras.get(numero, [])), len(fila.get(numero, [])),
                 sum(1 for s in secoes if r"\begin{definicao}" in s),
                 sum(1 for s in secoes if r"\begin{proposicao}" in s),
                 sum(1 for s in secoes if re.search(r"\\num[A-Za-z]", s) or re.search(r"\d,\d", s))))
    print()
    print("medidor, não portão: nada aqui reprova. A contagem diz onde olhar; a leitura decide.")


def main(argumentos: list) -> int:
    if "--inventario" in argumentos:
        return inventario()
    return medir()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
