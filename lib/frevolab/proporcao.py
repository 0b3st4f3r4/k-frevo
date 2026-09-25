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

**A extensão: a barra sem a lei.** A conta mínima pede a lei (`p`) na mão, e a lei é o que
não se tem quando o mundo muda. A reamostragem ergue a barra com a amostra sozinha:
re-sortear os próprios dias, com reposição, e ler a dispersão dos re-sorteios. O defeito
que ela torna impossível é anunciar uma entrega sem barra --- ou com a barra de uma lei que
ninguém verificou. E o `bloco` é a memória do gesto: re-sortear dia a dia trata o
calendário como ruído, e o capítulo dos blocos mostrou que ele não é.
"""
__all__ = ["indicadores", "variacao", "fracao", "barra", "mundos", "janelas",
           "reamostragens", "barra_reamostrada", "cobertura"]

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


def reamostragens(serie, quantos: int, rng, bloco: int = 1) -> np.ndarray:
    r"""As frações de `quantos` re-sorteios da amostra, com reposição.

    O gesto é o da urna com devolução: cada re-sorteio devolve o número de dias da
    amostra, sorteados dela mesma, e a fração é a média do que saiu. Com `bloco=1` os
    dias são re-sorteados um a um; com `bloco=N`, blocos inteiros de `N` dias ---
    porque o dia tem data, e o que vem junto no calendário tem de continuar junto no
    re-sorteio. O resto final, quando não cabe um bloco inteiro, é descartado: é o mesmo
    critério das contagens em blocos do capítulo do alarme.

    A reposição é o que faz o gesto valer: sem ela, cada re-sorteio é a amostra em outra
    ordem, a fração é sempre a mesma e a barra colapsa --- e é essa a mutação que o teste
    de propriedade tem de acusar.

    O sorteio entra por parâmetro (o `rng`), e nunca pela semente global: dois cadernos
    que sorteiam na mesma sessão não podem mexer um no outro.
    """
    valores = np.asarray(serie, dtype=float)
    if valores.ndim != 1 or valores.size == 0:
        raise ValueError("a amostra tem de ser unidimensional e não vazia")
    if quantos < 1:
        raise ValueError("não há re-sorteio de %r amostras" % quantos)
    if bloco < 1:
        raise ValueError("bloco de %r dias" % bloco)
    n_blocos = valores.size // bloco
    if n_blocos < 1:
        raise ValueError("a amostra de %d dias não tem um bloco inteiro de %d dias"
                         % (valores.size, bloco))
    # A fração de uma amostra em blocos é a soma das somas dos blocos sorteados sobre os
    # dias sorteados: somar os blocos primeiro é o que faz o re-sorteio de dias e o de
    # blocos serem o mesmo código, com o bloco de um dia como caso particular.
    somas = valores[: n_blocos * bloco].reshape(n_blocos, bloco).sum(axis=1)
    dias = n_blocos * bloco
    fracoes = np.empty(quantos, dtype=float)
    # O lote existe para o re-sorteio de dias não montar a matriz inteira na memória: dez
    # mil re-sorteios de seis mil dias são sessenta milhões de índices, e um lote de poucos
    # milhões cabe sem espremer a máquina.
    lote = max(1, 2_000_000 // n_blocos)
    feitos = 0
    while feitos < quantos:
        tamanho = min(lote, quantos - feitos)
        sorteados = rng.integers(0, n_blocos, size=(tamanho, n_blocos))
        fracoes[feitos: feitos + tamanho] = somas[sorteados].sum(axis=1) / dias
        feitos += tamanho
    return fracoes


def barra_reamostrada(serie, confianca: float = 0.95, quantos: int = 2000, *, rng,
                      bloco: int = 1) -> tuple:
    r"""A barra erguida pelos re-sorteios da própria amostra: o par de quantis.

    É a barra da raiz sem a fórmula: em vez de `sqrt(p(1-p)/n)` com a lei na mão, os
    quantis da confiança declarada sobre as frações dos re-sorteios. A barra diz de quanto
    a fração se mexeria se os dias fossem outros --- e ela é barra, não promessa de
    cobertura: quem confere a promessa é o exame de cobertura, com a verdade na mão.
    """
    if not 0.0 < confianca < 1.0:
        raise ValueError("confiança de %r não está entre zero e um" % confianca)
    fracoes = reamostragens(serie, quantos, rng, bloco=bloco)
    alfa = 1.0 - confianca
    inferior, superior = np.quantile(fracoes, [alfa / 2.0, 1.0 - alfa / 2.0])
    return (float(inferior), float(superior))


def cobertura(amostras, verdade, confianca: float = 0.95, quantos: int = 1000, *, rng,
              bloco: int = 1) -> float:
    r"""A fração de mundos cuja barra reamostrada contém a verdade.

    É o exame que a barra não faz sozinha: cada linha de `amostras` é um mundo medido
    uma vez, a barra de cada mundo é erguida por re-sorteios dele mesmo, e o número
    devolvido diz em que fração dos mundos a verdade conhecida caiu dentro. O `rng` é um
    só e corre os mundos em ordem, de modo que dois exames com o mesmo estado de sorteio
    devolvem o mesmo número.
    """
    matriz = np.asarray(amostras, dtype=float)
    if matriz.ndim != 2:
        raise ValueError("cobertura quer uma matriz: uma linha por mundo, uma coluna por dia")
    if matriz.shape[0] < 1 or matriz.shape[1] < 1:
        raise ValueError("não há exame de %s mundos" % (matriz.shape,))
    if not 0.0 < confianca < 1.0:
        raise ValueError("confiança de %r não está entre zero e um" % confianca)
    if quantos < 1:
        raise ValueError("não há exame com %r re-sorteios" % quantos)
    dentro = 0
    for mundo in matriz:
        inferior, superior = barra_reamostrada(mundo, confianca=confianca, quantos=quantos,
                                               rng=rng, bloco=bloco)
        dentro += int(inferior <= verdade <= superior)
    return dentro / matriz.shape[0]
