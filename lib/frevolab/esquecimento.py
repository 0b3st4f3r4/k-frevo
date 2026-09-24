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
TOLERANCIA = 0.15

__all__ = ["TAXA_PADRAO", "JANELA_PADRAO", "HORIZONTE_PADRAO", "TOLERANCIA", "exponencial",
           "janela", "memoria", "meia_vida", "dias_para_tolerancia", "erro", "erro_medio",
           "erro_varios", "limiar", "reverter", "erro_do_inverso", "erro_do_otimo", "horizonte"]


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


def dias_para_tolerancia(taxa: float, tolerancia: float = TOLERANCIA) -> float:
    r"""Quantos dias a estimativa leva para chegar a \emph{tolerancia} do degrau.

    É a conta da proposição: o desvio decai como \emph{(1-taxa) elevado a t}, de modo que cruzar
    até \emph{eps} do degrau leva \emph{log(eps)/log(1-taxa)} dias. É essa conta que decide se uma
    taxa ainda aprende dentro do horizonte que se tem.
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
           tolerancia: float = TOLERANCIA, estimador=None) -> dict:
    r"""O esquecimento **mínimo** que ainda aprende dentro do horizonte declarado.

    Varre as taxas da mais lenta para a mais rápida e devolve a primeira que fica dentro da
    tolerância, com o erro que ela entrega e os dias que a proposição previa. É a resposta em forma
    de número à pergunta da travessia: abaixo dessa taxa o sistema lembra demais para aprender.
    """
    if estimador is None:
        estimador = exponencial
    for taxa in sorted(taxas):
        media, dispersao = erro_medio(series, estimador, taxa, verdade, inicio, horizonte)
        if media <= tolerancia:
            return {"taxa": float(taxa), "memoria": float(memoria(taxa)), "erro": media,
                    "dispersao": dispersao, "horizonte": int(horizonte),
                    "tolerancia": float(tolerancia),
                    "dias_previstos": dias_para_tolerancia(taxa, tolerancia)}
    raise ValueError("nenhuma taxa da varredura aprende dentro do horizonte declarado")
