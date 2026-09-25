r"""A janela que se escolhe sozinha: o tamanho da memória decidido pelo dado, dia a dia.

O capítulo do esquecimento mediu que nenhuma escolha fixa serve aos dois mundos: no que dobra, a
janela curta ganha; no que não muda, a longa quase não erra --- e o sistema não sabe em que mundo
está. Este módulo fecha essa conta com o teste das metades cite{gavalda2007learning,gama2004learning}:
a janela guarda os últimos dias (até um máximo declarado); quando a média da metade nova discorda
da metade velha além de um limiar, a metade velha cai --- e o tamanho que sobra é o que o dado
escolheu.

**O limiar é decisão, não ajuste.** Ele é calibrado no mundo parado, antes de qualquer medição no
mundo que muda, para respeitar um orçamento de encolhimentos falsos por ano --- a mesma unidade em
que o capítulo do orçamento do alarme conta os seus alarmes. Com limiar infinito a janela é
exatamente a fixa do tamanho máximo, dia a dia: é o controle estrutural desta família.

**O limite declarado (§8.5).** A janela que se encolhe é instrumento: o que ela mede é o preço de
deixar o dado escolher, não uma afirmação sobre qual mundo está do lado de fora.
"""
import numpy as np

MINIMA_PADRAO = 21
MAXIMA_PADRAO = 1008

__all__ = ["MINIMA_PADRAO", "MAXIMA_PADRAO", "nivel", "falsos_por_ano"]


def nivel(serie, limiar: float, minima: int = MINIMA_PADRAO, maxima: int = MAXIMA_PADRAO) -> dict:
    r"""A estimativa do nível com o tamanho da janela escolhido pelo dado, dia a dia.

    A cada dia a janela cobre os últimos dias até \texttt{maxima}. Enquanto a metade nova e a
    metade velha discordarem além do 	exttt{limiar} --- e o tamanho permitir o corte ---, a metade
    velha cai. A estimativa do dia é a média da janela que sobrou, e o registro guarda cada
    encolhimento: o dia, o tamanho antes e o tamanho depois.
    """
    x = np.asarray(serie, dtype=float)
    if x.ndim != 1 or x.size < 1:
        raise ValueError("a série precisa ser unidimensional e não vazia")
    if minima < 1 or maxima < 2 * minima:
        raise ValueError("a máxima precisa ser pelo menos o dobro da mínima")
    if not limiar > 0.0:
        raise ValueError("o limiar precisa ser positivo (use um valor enorme para o controle)")
    pre = np.concatenate(([0.0], np.cumsum(x)))
    n = x.size
    est = np.empty(n)
    tamanhos = np.empty(n, dtype=int)
    encolhimentos = []
    inicio = 0
    for t in range(n):
        if t - maxima + 1 > inicio:
            inicio = t - maxima + 1
        while True:
            k = t - inicio + 1
            if k < 2 * minima:
                break
            meio = inicio + k // 2
            media_velha = (pre[meio] - pre[inicio]) / (meio - inicio)
            media_nova = (pre[t + 1] - pre[meio]) / (t + 1 - meio)
            if abs(media_nova - media_velha) > limiar:
                encolhimentos.append((t, k, t - meio + 1))
                inicio = meio
            else:
                break
        est[t] = (pre[t + 1] - pre[inicio]) / (t - inicio + 1)
        tamanhos[t] = t - inicio + 1
    return {"estimativa": est, "encolhimentos": encolhimentos, "tamanhos": tamanhos}


def falsos_por_ano(encolhimentos, dias: int, dias_uteis: int = 252) -> float:
    r"""A cadência de encolhimentos em falsos por ano --- a unidade do orçamento de alarme.

    No mundo que não muda, todo encolhimento é falso: a janela jogou fora dias que eram iguais aos
    que ficaram. Contar esses eventos por ano é a mesma conta que o capítulo do orçamento faz com
    os seus alarmes no mundo parado.
    """
    if dias <= 0 or dias_uteis <= 0:
        raise ValueError("os dias precisam ser positivos")
    return len(list(encolhimentos)) * dias_uteis / float(dias)

def limiar_do_orcamento(serie, orcamento_falsos_por_ano: float = 1.0,
                        minima: int = MINIMA_PADRAO, maxima: int = MAXIMA_PADRAO,
                        dias_uteis: int = 252, passos: int = 40) -> float:
    r"""O limiar que entrega o orçamento declarado no pedaço em que ele é calibrado.

    A contagem de encolhimentos cai quando o limiar sobe, e a bisseção acha o limiar que a põe no
    orçamento. É decisão declarada, e não ajuste: ela é tomada antes de medir o mundo que muda, e é
    sempre sobre o pedaço que serve de calibração.
    """
    if orcamento_falsos_por_ano < 0.0:
        raise ValueError("o orcamento nao pode ser negativo")
    x = np.asarray(serie, dtype=float)
    if x.ndim != 1 or x.size < 2 * maxima:
        raise ValueError("a calibragem precisa de pelo menos duas janelas maximas")
    baixo, alto = 1e-9, 10.0
    for _ in range(int(passos)):
        meio = 0.5 * (baixo + alto)
        saida = nivel(x, meio, minima, maxima)
        cadencia = falsos_por_ano(saida["encolhimentos"], x.size, dias_uteis)
        if cadencia > orcamento_falsos_por_ano:
            baixo = meio
        else:
            alto = meio
    return float(alto)


def nivel_recalibrado(serie, orcamento_falsos_por_ano: float = 1.0, passo: float = 0.05,
                      minima: int = MINIMA_PADRAO, maxima: int = MAXIMA_PADRAO,
                      dias_uteis: int = 252, calibragem: float = 0.4) -> dict:
    r"""O mesmo laco das metades, com o LIMIAR DE ESTADO: o limiar sobe no dia em que houve corte e
    derrete nos dias em que nao houve, sempre contra o orcamento diario declarado.

    O limiar de partida e o do orcamento, medido no pedaco de calibragem; a partir dele, o proprio
    corte de cada dia move o limiar --- e e ele que decide o corte do dia seguinte. O observavel e o
    CORTE, e nao o falso: falsidade so existe nos mundos sinteticos, e e la que o caderno mede. O
    preco da obediencia aparece no tamanho da janela depois da mudanca: obedecer ao orcamento e
    segurar o corte, e segurar o corte envelhece a janela.
    """
    x = np.asarray(serie, dtype=float)
    if x.ndim != 1 or x.size < 2 * maxima:
        raise ValueError("a recalibragem precisa de pelo menos duas janelas maximas")
    if not 0.0 < passo <= 1.0:
        raise ValueError("o passo da recalibragem precisa ficar em (0; 1]")
    if not 0.0 < calibragem < 1.0:
        raise ValueError("a fracao de calibragem precisa ficar em (0; 1)")
    corte_calibragem = int(x.size * calibragem)
    limiar_orcado = limiar_do_orcamento(x[:corte_calibragem], orcamento_falsos_por_ano,
                                        minima, maxima, dias_uteis)
    orcamento_dia = orcamento_falsos_por_ano / float(dias_uteis)
    pre = np.concatenate(([0.0], np.cumsum(x)))
    n = x.size
    est = np.empty(n)
    tamanhos = np.empty(n, dtype=int)
    encolhimentos, limiares = [], []
    limiar = float(limiar_orcado)
    desvio = 0.0
    inicio = 0
    for t in range(n):
        if t - maxima + 1 > inicio:
            inicio = t - maxima + 1
        cortou = False
        while True:
            k = t - inicio + 1
            if k < 2 * minima:
                break
            meio = inicio + k // 2
            velha = (pre[meio] - pre[inicio]) / (meio - inicio)
            nova = (pre[t + 1] - pre[meio]) / (t + 1 - meio)
            if abs(nova - velha) > limiar:
                encolhimentos.append((t, k, t - meio + 1))
                inicio = meio
                cortou = True
            else:
                break
        corte_hoje = 1.0 if cortou else 0.0
        desvio += corte_hoje - orcamento_dia
        limiar = float(max(limiar + passo * limiar_orcado * (corte_hoje - orcamento_dia), 1e-9))
        limiares.append((t, limiar, desvio))
        est[t] = (pre[t + 1] - pre[inicio]) / (t - inicio + 1)
        tamanhos[t] = t - inicio + 1
    return {"estimativa": est, "tamanhos": tamanhos, "encolhimentos": encolhimentos,
            "limiar_orcado": float(limiar_orcado), "limiares": limiares,
            "desvio": float(desvio), "orcamento_dia": float(orcamento_dia)}


def e_das_metades(serie, minima: int = MINIMA_PADRAO, maxima: int = MAXIMA_PADRAO,
                  kapa: float = 0.5) -> dict:
    r"""O e-valor do dia: o p-valor do teste das metades, convertido pelo calibrador da aposta.

    O teste é o das metades da janela corrente --- o mesmo do módulo, com o sinal trocado: aqui o
    que interessa é o valor-p da discordância, e não o corte. A conversão é o calibrador do
    capítulo da aposta, de média um sob a uniforme e sem exigir independência.
    """
    from . import aposta
    from . import promessa as _promessa  # noqa: F401  (a casa do teste t)
    x = np.asarray(serie, dtype=float)
    if x.ndim != 1 or x.size < 2 * maxima:
        raise ValueError("o e-valor do dia precisa de pelo menos duas janelas maximas")
    if not 0.0 < kapa < 1.0:
        raise ValueError("o kapa do calibrador tem de ficar em (0; 1)")
    p_valores = np.ones(x.size)
    for t in range(2 * minima, x.size):
        inicio = max(0, t - maxima + 1)
        k = t - inicio + 1
        meio = inicio + k // 2
        velha, nova = x[inicio:meio], x[meio:t + 1]
        if velha.size < 2 or nova.size < 2:
            continue
        var_velha = float(np.var(velha, ddof=1)) / velha.size
        var_nova = float(np.var(nova, ddof=1)) / nova.size
        erro = float(np.sqrt(var_velha + var_nova))
        if erro <= 0.0:
            p_valores[t] = 1.0
            continue
        z = abs(float(np.mean(nova) - np.mean(velha))) / erro
        p_valores[t] = float(2.0 * (1.0 - 0.5 * (1.0 + np.math.erf(z / np.sqrt(2.0))))) \
            if hasattr(np, "math") else float(2.0 * (1.0 - 0.5 * (1.0 + __import__("math").erf(z / np.sqrt(2.0)))))
    return {"p": p_valores, "e": aposta.e_calibrado(p_valores, kapa)}
