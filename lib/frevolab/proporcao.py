r"""A proporção: a média de muitos sorteios, e a barra que ela carrega.

A raiz do livro. Antes de medir o que se pode perder, é preciso medir o que anda --- e a
conta mais velha do mundo é a média: some os dias e divida pelo número deles. Este módulo
mede o que essa conta vale, e a resposta é que ela vale, desde que venha com a barra dela.

**O fracasso que ele abre.** A fração de dias de alta do índice nos últimos vinte e um
pregões e nos últimos duzentos e cinquenta e dois são dois números que discordam, e a
aritmética não diz se a diferença é do mundo ou do tamanho da janela. A barra responde: ela
diz de quanto a média se mexe **sozinha**, quando nada no mundo mudou.

**A conta mínima.** Com `n` dias independentes e a mesma probabilidade `p` de alta, a fração
de altas tem média `p` e desvio `sqrt(p(1-p)/n)` --- a barra cai com a raiz do número de
dias. É a previsão que o `auto_teste` confere contra a dispersão medida em mundos sorteados, que é
a propriedade que o capítulo usa.
"""
__all__ = ["indicadores", "variacao", "fracao", "barra", "mundos", "janelas"]

import numpy as np
import pandas as pd


def variacao(serie) -> pd.Series:
    r"""A variação do dia em porcentagem --- a conta deste capítulo, antes de o logaritmo entrar.

    Ela existe para o primeiro capítulo não precisar do logaritmo: o capítulo seguinte mostra
    que somar porcentagens não devolve o lugar, e é aí que o log entra. Aqui a conta é a mais
    crua que existe: o preço de hoje dividido pelo de ontem, menos um.
    """
    precos = pd.Series(serie, dtype=float)
    return precos.pct_change().dropna()


def indicadores(serie) -> np.ndarray:
    r"""O dia vira 1 quando sobe e 0 quando não sobe --- uma série de sorteios de dois valores.

    O nome do objeto é o que ele é: o indicador do dia. A média de uma série de indicadores é
    uma fração, e é por isso que este módulo trata de fração e não de retorno: a fração é a
    média mais simples que existe, e a barra dela se demonstra contando.
    """
    valores = np.asarray(serie, dtype=float)
    return (valores > 0).astype(float)


def fracao(serie) -> float:
    """A fração de dias de alta: a média dos indicadores, e é isso que o capítulo chama de média."""
    valores = np.asarray(serie, dtype=float)
    if valores.size == 0:
        raise ValueError("série vazia: não há fração de nada")
    return float((valores > 0).mean())


def barra(p: float, n: int) -> float:
    r"""A barra da fração: `sqrt(p(1-p)/n)`, o desvio da média de `n` sorteios.

    É a previsão da proposição, escrita uma vez só. Ela vale para a fração; para uma média de
    outra coisa a barra é `s/sqrt(n)`, com `s` o desvio de um dia --- e as duas são a mesma
    conta, com `p(1-p)` no lugar de `s ao quadrado`.
    """
    if not 0.0 <= p <= 1.0:
        raise ValueError("fração fora de zero e um: %r" % p)
    if n < 1:
        raise ValueError("não há média de %r dias" % n)
    return float(np.sqrt(p * (1.0 - p) / n))


def mundos(p: float, n: int, quantos: int, rng) -> np.ndarray:
    r"""A fração medida em `quantos` mundos sorteados de `n` dias com a mesma lei.

    O sorteio entra por parâmetro (o `rng`), e nunca pela semente global: dois cadernos que
    sorteiam na mesma sessão não podem mexer um no outro.
    """
    if n < 1 or quantos < 1:
        raise ValueError("mundo de %r dias, %r mundos" % (n, quantos))
    altas = rng.random((quantos, n)) < p
    return altas.mean(axis=1)


def janelas(serie, tamanho: int) -> np.ndarray:
    r"""A fração de altas em **todas** as janelas móveis de `tamanho` dias.

    É a leitura honesta da série real: em vez de escolher uma janela, mede-se a distribuição
    de todas elas. A dispersão entre janelas é o que se compara com a barra --- se o mundo não
    muda, a dispersão entre janelas é do tamanho da barra, e nada mais.
    """
    if tamanho < 1:
        raise ValueError("janela de %r dias" % tamanho)
    altas = indicadores(serie)
    if altas.size < tamanho:
        raise ValueError("a série tem %d dias e a janela pede %d" % (altas.size, tamanho))
    acumulado = np.concatenate([[0.0], np.cumsum(altas)])
    return (acumulado[tamanho:] - acumulado[:-tamanho]) / tamanho
