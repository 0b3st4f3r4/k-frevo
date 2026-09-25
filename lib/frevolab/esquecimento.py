r"""O esquecimento: aprender é apagar, e apagar tem taxa.

A atualização do capítulo anterior é, no fundo, um esquecimento: cada vez que a escala é refeita, o
passado cede lugar ao presente. Este módulo mede o que essa troca custa e onde ela para de valer,
varrendo a taxa de esquecimento dos dois extremos para o meio.

A forma mais simples de esquecer é a **mistura exponencial**: a estimativa de hoje é uma mistura da
estimativa de ontem com o dia de hoje, com peso \emph{taxa} para o presente. A memória efetiva é
\emph{1/taxa} dias. A forma declarada como referência a bater é a **janela deslizante**: a média dos
últimos \emph{n} dias, que lembra exatamente \emph{n} dias e não lembra nada antes disso.

**O defeito que este módulo torna impossível.** Escolher a memória pelo gosto, ou copiar a janela de
um ano do primeiro capítulo para um lugar onde ela é cega. Uma janela de um ano não vê uma mudança
dentro de um ano: ela carrega os dias velhos com o mesmo peso dos novos até o dia em que eles caem
fora de uma vez. A medição mostra as duas pontas da troca e onde fica o meio.

A proposição que sustenta a conta está no \texttt{auto\_teste}: depois de um degrau, o desvio da
mistura exponencial decai exatamente como \emph{(1-taxa) elevado a t}, de modo que cruzar até uma
tolerância \emph{eps} leva \emph{log(eps)/log(1-taxa)} dias.
"""
import numpy as np

TAXA_PADRAO = 0.048
JANELA_PADRAO = 21
HORIZONTE_PADRAO = 250
# A tolerancia deste modulo tem UMA unidade declarada, e e a do NIVEL novo: o erro medido e a
# distancia relativa media entre a estimativa e a verdade, dia a dia. A proposicao da meia-vida
# fala em tolerancia do DEGRAU, que e outra unidade: num mundo que dobra de uma vez o degrau e
# metade do nivel, de modo que 0,15 do nivel e 0,30 do degrau. Enquanto as duas foram o mesmo
# 0,15, a prosa do capitulo 12 dizia uma unidade e o criterio media na outra (2026-09-24).
TOLERANCIA = 0.15
FATOR_PADRAO = 2.0
TOLERANCIA_DEGRAU = TOLERANCIA / (1.0 - 1.0 / FATOR_PADRAO)

__all__ = ["TAXA_PADRAO", "JANELA_PADRAO", "HORIZONTE_PADRAO", "FATOR_PADRAO", "TOLERANCIA",
           "TOLERANCIA_DEGRAU", "exponencial",
           "janela", "memoria", "meia_vida", "dias_para_tolerancia", "erro", "erro_medio",
           "erro_varios", "limiar", "reverter", "erro_do_inverso", "erro_do_otimo", "horizonte",
           # a divida do capitulo 19, paga: as tres funcoes da idade ja existiam e nao estavam na
           # lista, de modo que "from frevolab.esquecimento import *" nao as via (2026-09-25)
           "memoria_da_idade", "dias_da_idade", "media_acumulada",
           "acumulada_com_reset", "dias_ate_dentro", "piso_exponencial", "plasticidade"]


def exponencial(serie: np.ndarray, taxa: float) -> np.ndarray:
    r"""A estimativa que mistura ontem com hoje, com peso \emph{taxa} para hoje.

    A primeira estimativa é o primeiro dia, de modo que a série de estimativas não tem dias de
    graça. Com \emph{taxa} perto de zero a estimativa quase não se move; com \emph{taxa} igual a um
    ela é o próprio dia, e não há estimativa nenhuma.
    """
    s = np.asarray(serie, dtype=float)
    if s.size < 2:
        raise ValueError("a serie precisa de pelo menos dois dias")
    if not 0.0 < taxa <= 1.0:
        raise ValueError("a taxa de esquecimento precisa estar entre zero e um")
    saida = np.empty(s.size)
    saida[0] = s[0]
    for t in range(1, s.size):
        saida[t] = (1.0 - taxa) * saida[t - 1] + taxa * s[t]
    return saida


def janela(serie: np.ndarray, dias: int) -> np.ndarray:
    r"""A média dos últimos \emph{dias} dias, sem olhar para a frente.

    Os primeiros \emph{dias} dias ficam sem estimativa, e não com uma estimativa feita de menos
    dias: uma janela que se completa sozinha esconde justamente o começo.
    """
    s = np.asarray(serie, dtype=float)
    if dias < 1:
        raise ValueError("a janela precisa de pelo menos um dia")
    if s.size < dias:
        raise ValueError("a serie precisa ser maior que a janela")
    acumulado = np.concatenate([[0.0], np.cumsum(s)])
    saida = np.full(s.size, np.nan)
    saida[dias:] = (acumulado[dias:-1] - acumulado[:-(dias + 1)]) / dias
    return saida


def memoria(taxa: float) -> float:
    r"""A memória efetiva de uma taxa de esquecimento, em dias."""
    if not 0.0 < taxa <= 1.0:
        raise ValueError("a taxa de esquecimento precisa estar entre zero e um")
    return 1.0 / taxa


def meia_vida(taxa: float) -> float:
    r"""Quantos dias a estimativa leva para cruzar metade de um degrau.

    Com a taxa igual a um não há estimativa nenhuma a cruzar: a estimativa é o próprio dia, e a
    meia-vida é zero.
    """
    if not 0.0 < taxa <= 1.0:
        raise ValueError("a taxa precisa estar entre zero e um")
    if taxa == 1.0:
        return 0.0
    return float(np.log(0.5) / np.log(1.0 - taxa))


def dias_para_tolerancia(taxa: float, tolerancia: float = TOLERANCIA_DEGRAU) -> float:
    r"""Quantos dias a estimativa leva para chegar a \emph{tolerancia} do degrau.

    É a conta da proposição: o desvio decai como \emph{(1-taxa) elevado a t}, de modo que cruzar
    até \emph{eps} do degrau leva \emph{log(eps)/log(1-taxa)} dias. A tolerância aqui é fração do
    DEGRAU --- o tamanho do salto ---, e não do nível novo: quem declara a tolerância em fração do
    nível converte por \emph{TOLERANCIA_DEGRAU}, que já traz a conta feita para o fator do mundo.
    Confundir as duas unidades dá uma coluna de dias certa pela metade, que é o defeito que esta
    rodada consertou. É essa conta que decide se uma taxa ainda aprende dentro do horizonte.
    """
    if not 0.0 < taxa <= 1.0:
        raise ValueError("a taxa precisa estar entre zero e um")
    if not 0.0 < tolerancia < 1.0:
        raise ValueError("a tolerancia precisa estar entre zero e um")
    if taxa == 1.0:
        return 0.0
    return float(np.log(tolerancia) / np.log(1.0 - taxa))


def erro(estimativa: np.ndarray, verdade: np.ndarray, inicio: int = 0,
         horizonte: int = HORIZONTE_PADRAO) -> float:
    r"""O erro relativo médio da estimativa contra a verdade declarada, dia a dia.

    A verdade entra como série, e não como número: num mundo que muda, a verdade de hoje não é a
    verdade de ontem, e comparar tudo com um alvo só mediria a distância até o alvo errado.
    """
    e = np.asarray(estimativa, dtype=float)
    v = np.asarray(verdade, dtype=float)
    if e.shape != v.shape:
        raise ValueError("a estimativa e a verdade precisam ter o mesmo comprimento")
    if inicio + horizonte > e.size:
        raise ValueError("a avaliacao nao cabe na serie")
    trecho_e = e[inicio:inicio + horizonte]
    trecho_v = v[inicio:inicio + horizonte]
    if not np.all(np.isfinite(trecho_e)):
        raise ValueError("a estimativa tem dias sem valor na janela avaliada")
    return float(np.mean(np.abs(trecho_e - trecho_v) / trecho_v))


def erro_medio(series, estimador, parametro, verdade, inicio: int = 0,
               horizonte: int = HORIZONTE_PADRAO) -> tuple:
    r"""O erro de um estimador entre mundos sorteados, com a dispersão.

    Uma taxa medida num mundo só não é uma medida: o erro varia de sorteio para sorteio mais do que
    varia entre taxas vizinhas, e a mesma regra dos capítulos anteriores vale aqui.
    """
    series = [np.asarray(s, dtype=float) for s in series]
    if not series:
        raise ValueError("a medicao precisa de pelo menos uma serie")
    valores = np.array([erro(estimador(s, parametro), verdade, inicio, horizonte) for s in series])
    if valores.size == 1:
        return float(valores[0]), 0.0
    return float(valores.mean()), float(valores.std(ddof=1))


def erro_varios(estimativas, verdade, inicio: int = 0,
               horizonte: int = HORIZONTE_PADRAO) -> tuple:
    r"""O erro de várias estimativas já prontas, com a dispersão.

    Serve para avaliar o mesmo punhado de estimativas em horizontes diferentes sem refazer a conta
    que as produziu --- o horizonte muda a leitura, não o estimador.
    """
    estimativas = [np.asarray(e, dtype=float) for e in estimativas]
    if not estimativas:
        raise ValueError("a medicao precisa de pelo menos uma estimativa")
    valores = np.array([erro(e, verdade, inicio, horizonte) for e in estimativas])
    if valores.size == 1:
        return float(valores[0]), 0.0
    return float(valores.mean()), float(valores.std(ddof=1))


def reverter(serie: np.ndarray, a: float, dias: int) -> np.ndarray:
    r"""A reconstrução pelo mapa inverso: anda emph{dias} passos para trás dividindo por emph{a}.

    É o que se tenta primeiro, e é uma armadilha: o ruído que entrou em cada passo é desconhecido,
    e dividir por emph{a} o amplifica junto com o sinal. O erro dessa reconstrução cresce como
    emph{1/a} elevado aos dias, sem teto.
    """
    s = np.asarray(serie, dtype=float)
    if dias < 0:
        raise ValueError("os dias para tras nao podem ser negativos")
    if not 0.0 < a < 1.0:
        raise ValueError("o a do processo precisa estar entre zero e um")
    return s / (a ** dias)


def erro_do_inverso(a: float, dias: int, sigma: float = 1.0) -> float:
    r"""O erro exato do mapa inverso, em forma fechada.

    Sai da recursão do erro: cada passo para trás divide o erro acumulado por emph{a} e soma o
    ruído desconhecido do passo, também dividido por emph{a}. A soma geométrica dá
    emph{sigma vezes raiz de (1 - a elevado a 2k) / (1 - a ao quadrado), tudo sobre a elevado a k}.
    """
    if not 0.0 < a < 1.0:
        raise ValueError("o a do processo precisa estar entre zero e um")
    if dias < 0:
        raise ValueError("os dias para tras nao podem ser negativos")
    if dias == 0:
        return 0.0
    return float(sigma * np.sqrt((1.0 - a ** (2 * dias)) / (1.0 - a ** 2)) / a ** dias)


def erro_do_otimo(a: float, dias: int, sigma: float = 1.0) -> float:
    r"""O erro da melhor reconstrução possível: a esperança condicional.

    Dado só o estado de hoje, o melhor palpite para o valor de emph{k} dias atrás é emph{a elevado
    a k} vezes o estado de hoje, e o erro dele é emph{sigma_x vezes raiz de 1 - a elevado a 2k}.
    Esse erro não cresce sem teto: ele sobe até a dispersão do próprio processo, que é o erro de
    quem não olha para nada. É por isso que o passado não se perde num ponto, ele **desbota**.
    """
    if not 0.0 < a < 1.0:
        raise ValueError("o a do processo precisa estar entre zero e um")
    if dias < 0:
        raise ValueError("os dias para tras nao podem ser negativos")
    sigma_x = sigma / np.sqrt(1.0 - a ** 2)
    return float(sigma_x * np.sqrt(1.0 - a ** (2 * dias)))


def horizonte(a: float, tolerancia: float = 0.5) -> float:
    r"""Quantos dias atrás ainda se recupera o passado, para uma tolerância declarada.

    A tolerância é a fração da dispersão do processo que se aceita errar. Sai da conta do erro
    ótimo: emph{log(1 - t ao quadrado) / (2 log a)} dias. Não é o mesmo número que a memória do
    processo, emph{1/(1-a)}: são duas medidas diferentes, e o caderno mostra as duas.
    """
    if not 0.0 < a < 1.0:
        raise ValueError("o a do processo precisa estar entre zero e um")
    if not 0.0 < tolerancia < 1.0:
        raise ValueError("a tolerancia precisa estar entre zero e um")
    return float(np.log(1.0 - tolerancia ** 2) / (2.0 * np.log(a)))


def limiar(series, taxas, verdade, inicio: int = 0, horizonte: int = HORIZONTE_PADRAO,
           tolerancia_nivel: float = TOLERANCIA, fator: float = FATOR_PADRAO,
           estimador=None) -> dict:
    r"""O esquecimento **mínimo** que ainda aprende dentro do horizonte declarado.

    Varre as taxas da mais lenta para a mais rápida e devolve a primeira que fica dentro da
    tolerância, com o erro que ela entrega e os dias que a proposição previa. A tolerância entra
    como fração do NÍVEL novo, que é a unidade do erro medido aqui, e os dias previstos, que são da
    proposição, saem na unidade do DEGRAU: a conversão é feita com \emph{fator}, o quanto o mundo
    dobra de uma vez. Sem ela, o mesmo 0,15 valia como duas coisas diferentes --- o defeito que a
    prosa do capítulo 13 e o critério de viabilidade tinham, cada um com a sua unidade. É a
    resposta em forma de número à pergunta da travessia: abaixo dessa taxa o sistema lembra demais
    para aprender.
    """
    if fator <= 1.0:
        raise ValueError("o fator do mundo precisa ser maior que um")
    if estimador is None:
        estimador = exponencial
    tolerancia_degrau = tolerancia_nivel / (1.0 - 1.0 / fator)
    for taxa in sorted(taxas):
        media, dispersao = erro_medio(series, estimador, taxa, verdade, inicio, horizonte)
        if media <= tolerancia_nivel:
            return {"taxa": float(taxa), "memoria": float(memoria(taxa)), "erro": media,
                    "dispersao": dispersao, "horizonte": int(horizonte),
                    "tolerancia_nivel": float(tolerancia_nivel),
                    "tolerancia_degrau": float(tolerancia_degrau),
                    "dias_previstos": dias_para_tolerancia(taxa, tolerancia_degrau)}
    raise ValueError("nenhuma taxa da varredura aprende dentro do horizonte declarado")

def memoria_da_idade(idade: int) -> float:
    """A taxa de quem nunca esquece: a media de tudo tem memoria igual a sua propria idade.

    A media acumulada de \emph{t} dias da o mesmo peso a todos eles, e essa mistura tem taxa
    \emph{1/t} --- de modo que quanto mais o sistema viu, mais lento ele aprende. E o caso que a
    proposicao da meia-vida preve sem que ninguem o tenha escolhido.
    """
    if int(idade) < 1:
        raise ValueError("a idade precisa de pelo menos um dia")
    return 1.0 / float(idade)


def dias_da_idade(idade: int, tolerancia: float = None) -> float:
    """Os dias que a memoria da idade leva para cruzar a tolerancia --- a conta da prop. 14.1."""
    tol = TOLERANCIA_DEGRAU if tolerancia is None else float(tolerancia)
    return dias_para_tolerancia(memoria_da_idade(idade), tol)

def media_acumulada(serie) -> "np.ndarray":
    """A media de tudo ate hoje: a estimativa que da o mesmo peso a todos os dias ja vistos.

    E o estimador mais antigo que existe, e o unico que ninguem escolhe: ele cai de graca de quem
    nao quer decidir. A memoria dele e a propria idade --- no dia t, a taxa e 1/t ---, de modo que
    um sistema que nunca esquece aprende cada vez mais devagar.
    """
    import numpy as np
    x = np.asarray(serie, dtype=float)
    vistas = np.arange(1, x.size + 1, dtype=float)
    return np.cumsum(x) / vistas

def acumulada_com_reset(serie, resets) -> np.ndarray:
    r"""A média acumulada que recomeça a idade em cada dia declarado.

    Entre um dia declarado e o seguinte a estimativa é a \emph{media\_acumulada} do pedaço; no
    próprio dia declarado ela recomeça do dia sozinho. O reset zera a idade, e não os dados: o
    passado continua existindo, só deixa de entrar na conta --- e é isso que o recomeço do
    capítulo 19 pressupõe, o dia da mudança declarado por quem a pôs no mundo. Sem nenhum dia
    declarado, o recomeço é a própria média acumulada.
    """
    x = np.asarray(serie, dtype=float)
    if x.size < 1:
        raise ValueError("a serie precisa de pelo menos um dia")
    marcas = [int(r) for r in resets]
    if len(set(marcas)) != len(marcas):
        raise ValueError("os dias declarados nao podem se repetir")
    if any(not 0 <= r < x.size for r in marcas):
        raise ValueError("os dias declarados precisam cair dentro da serie")
    bordas = [0] + sorted(marcas) + [x.size]
    saida = np.empty(x.size)
    for inicio, fim in zip(bordas[:-1], bordas[1:]):
        saida[inicio:fim] = media_acumulada(x[inicio:fim])
    return saida


def dias_ate_dentro(estimativa, verdade, inicio: int,
                    tolerancia_nivel: float = TOLERANCIA) -> float:
    r"""O primeiro dia, contado de \emph{inicio}, em que a estimativa entra na tolerância do nível.

    A tolerância é fração do NÍVEL novo --- a unidade do erro medido no capítulo ---, e a ponte
    para a fração do DEGRAU é a de sempre: num mundo que dobra, a mesma fronteira vale o dobro
    em degrau, e é ela que a proposição da meia-vida conta. Se a estimativa nunca entra, o dia é
    \emph{nan} --- como a latência sem alarme: o dia que não chega é resultado declarado, e não
    zero.
    """
    e = np.asarray(estimativa, dtype=float)
    v = np.asarray(verdade, dtype=float)
    if e.shape != v.shape:
        raise ValueError("a estimativa e a verdade precisam ter o mesmo comprimento")
    if not 0 <= int(inicio) < e.size:
        raise ValueError("o inicio precisa cair dentro da serie")
    if not 0.0 < tolerancia_nivel < 1.0:
        raise ValueError("a tolerancia precisa estar entre zero e um")
    if not np.all(np.isfinite(e[inicio:])):
        raise ValueError("a estimativa tem dias sem valor a partir do inicio")
    if not np.all(v[inicio:] > 0.0):
        raise ValueError("a tolerancia do nivel pede nivel positivo")
    desvio = np.abs(e[inicio:] - v[inicio:]) / v[inicio:]
    dentro = np.flatnonzero(desvio <= tolerancia_nivel)
    return float(dentro[0]) if dentro.size else float("nan")


def piso_exponencial(taxa: float, sigma_x: float) -> float:
    r"""O piso da taxa no mundo que não muda: \emph{sigma\_x} vezes a raiz de taxa sobre dois menos taxa.

    A variância da mistura é a soma dos pesos ao quadrado, e a soma geométrica dos
    \emph{(1-taxa)} ao quadrado dá \emph{taxa/(2-taxa)} --- de modo que a FORMA é livre da lei
    dos dias: qualquer mundo com dias independentes paga o mesmo fator, e só o desvio do mundo
    conhece a distribuição. É o preço declarado de fixar a taxa: o que ela ganha em dias paga em
    piso.
    """
    if not 0.0 < taxa <= 1.0:
        raise ValueError("a taxa precisa estar entre zero e um")
    if sigma_x < 0.0:
        raise ValueError("o desvio do mundo nao pode ser negativo")
    return float(sigma_x * np.sqrt(taxa / (2.0 - taxa)))


def plasticidade(series, degraus, verdade, horizonte: int = HORIZONTE_PADRAO,
                 taxa: float = TAXA_PADRAO) -> dict:
    r"""A plasticidade de três braços no mundo que muda de novo: quem volta, e em quantos dias.

    Os braços são a média de tudo (que nunca escolheu taxa), o recomeço (que zera a idade nos
    dias declarados) e a taxa fixa. Para cada degrau, na ordem, devolve o erro na janela de
    leitura e os dias até a tolerância --- mediana e dispersão entre mundos, e o número de
    mundos em que o dia não chegou. O dia que não chega é resultado: a média de tudo aprende o
    primeiro degrau e para, e é isso que a medição declara em vez de esconder no zero.
    """
    series = [np.asarray(s, dtype=float) for s in series]
    if not series:
        raise ValueError("a medicao precisa de pelo menos uma serie")
    n = series[0].size
    if any(s.size != n for s in series):
        raise ValueError("os mundos precisam ter o mesmo comprimento")
    v = np.asarray(verdade, dtype=float)
    if v.shape != (n,):
        raise ValueError("a verdade precisa ter o comprimento dos mundos")
    dias = [int(d) for d in degraus]
    if not dias:
        raise ValueError("declare pelo menos um dia de degrau")
    if len(set(dias)) != len(dias) or any(b <= a for a, b in zip(dias, dias[1:])):
        raise ValueError("os dias de degrau precisam crescer, sem repeticao")
    if any(not 1 <= d < n for d in dias):
        raise ValueError("os degraus precisam cair dentro da serie")
    if dias[-1] + horizonte > n:
        raise ValueError("a janela de leitura nao cabe depois do ultimo degrau")
    if not 0.0 < taxa <= 1.0:
        raise ValueError("a taxa precisa estar entre zero e um")
    bracos = {"acumulada": [media_acumulada(s) for s in series],
              "recomeco": [acumulada_com_reset(s, dias) for s in series],
              "exponencial": [exponencial(s, taxa) for s in series]}
    caixa = {"degraus": tuple(dias), "horizonte": int(horizonte), "taxa": float(taxa),
             "tolerancia_nivel": float(TOLERANCIA), "por_braco": {}}
    for nome, estimativas in bracos.items():
        linhas = []
        for dia in dias:
            erros = np.array([erro(e, v, dia, horizonte) for e in estimativas])
            voltas = np.array([dias_ate_dentro(e, v, dia, TOLERANCIA) for e in estimativas])
            voltaram = voltas[np.isfinite(voltas)]
            linhas.append({"erro_mediana": float(np.median(erros)),
                           "erro_dispersao": float(erros.std(ddof=1)) if erros.size > 1 else 0.0,
                           "dias_mediana": float(np.median(voltaram)) if voltaram.size else float("nan"),
                           "dias_dispersao": float(voltaram.std(ddof=1)) if voltaram.size > 1 else 0.0,
                           "mundos_sem_volta": int(voltas.size - voltaram.size)})
        caixa["por_braco"][nome] = linhas
    return caixa
