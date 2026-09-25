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

    A cada dia a janela cobre os últimos dias até 	exttt{maxima}. Enquanto a metade nova e a
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