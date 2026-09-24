r"""O nível e a soma dos incrementos: por que porcentagem não se soma.

A raiz do livro, segunda peça. O capítulo anterior mediu o dia --- a média, a barra, o
tamanho típico do que ele anda. Este módulo trata do que acontece quando os dias se
empilham: o nível.

**O fracasso que ele abre.** Somar as variações diárias de um índice e comparar com o que o
índice de fato andou. Num mês as duas contas quase coincidem; em vinte e seis anos a soma
das porcentagens entrega menos da metade da variação real, e nada na conta avisa. A razão é
a mais velha que existe: porcentagem multiplica, e multiplicação não se soma.

**A conta mínima.** O logaritmo troca multiplicação por soma, de modo que a soma dos
logaritmos é exatamente o logaritmo do quociente --- e é por isso que o livro mede em
logaritmo. E a variância da soma de incrementos independentes é a soma das variâncias, de
modo que o desvio do nível cresce com a raiz do horizonte: `sigma raiz de h`. É a previsão que o
`auto_teste` confere contra a dispersão medida em mundos sorteados.
"""
__all__ = ["soma_das_variacoes", "produto_das_variacoes", "soma_dos_logs", "contas_do_pedaco",
           "desvio_do_nivel", "mundos_do_passeio", "mudancas_de_nivel"]

import numpy as np
import pandas as pd

from . import proporcao, volatilidade


def contas_do_pedaco(precos, dias=None) -> dict:
    r"""As três contas do capítulo, em cima do mesmo pedaço de série, em porcentagem.

    A soma crua das variações, a variação que de fato aconteceu e a soma dos logaritmos. Elas
    moram aqui, e não no caderno, porque conta dentro de caderno não é testável nem reusável
    --- e esta é a conta que o capítulo inteiro discute.
    """
    serie = pd.Series(precos, dtype=float)
    if dias is not None:
        serie = serie.tail(dias + 1)
    if len(serie) < 2:
        raise ValueError("pedaço de %d dia(s): não há conta a fazer" % len(serie))
    variacoes = proporcao.variacao(serie)
    retornos = volatilidade.retornos_log(serie)
    return {
        "dias": int(len(variacoes)),
        "soma das porcentagens (%)": 100 * soma_das_variacoes(variacoes),
        "variação real (%)": 100 * (float(serie.iloc[-1]) / float(serie.iloc[0]) - 1),
        "soma dos logaritmos (%)": 100 * soma_dos_logs(retornos),
        "log do quociente (%)": 100 * float(np.log(float(serie.iloc[-1]) / float(serie.iloc[0]))),
    }


def soma_das_variacoes(variacoes) -> float:
    r"""A soma crua das variações em porcentagem: a conta que todo mundo faz primeiro.

    Ela é a errada, e é por isso que ela mora aqui: para o capítulo poder mostrar o tamanho
    do erro, ele precisa poder calcular o erro.
    """
    return float(np.asarray(variacoes, dtype=float).sum())


def produto_das_variacoes(variacoes) -> float:
    r"""A variação que de fato aconteceu: `produto de (1 + r) menos um`.

    É a conta certa em porcentagem --- cada dia multiplica o nível ---, e ela não se escreve
    como soma. É o que o logaritmo desfaz.
    """
    return float(np.prod(1.0 + np.asarray(variacoes, dtype=float)) - 1.0)


def soma_dos_logs(retornos) -> float:
    r"""A soma dos logaritmos do dia: igual ao logaritmo do quociente entre o fim e o começo.

    É a ponte do capítulo. No logaritmo, empilhar dias é somar, e a soma de nada dá zero: um
    preço que desce e volta ao mesmo lugar tem soma exatamente zero.
    """
    return float(np.asarray(retornos, dtype=float).sum())


def desvio_do_nivel(desvio_diario: float, dias: int) -> float:
    r"""O desvio do nível depois de `dias`: o desvio de um dia vezes a raiz dos dias.

    A variância de uma soma de incrementos independentes é a soma das variâncias --- `dias`
    parcelas iguais ---, e a raiz disso é a previsão. Ela cresce com a raiz do horizonte, e não
    com o horizonte: dobrar o tempo multiplica o desvio por raiz de dois.
    """
    if dias < 1:
        raise ValueError("não há horizonte de %r dias" % dias)
    if desvio_diario < 0:
        raise ValueError("desvio negativo: %r" % desvio_diario)
    return float(desvio_diario * np.sqrt(dias))


def mundos_do_passeio(desvio_diario: float, dias: int, mundos: int, rng) -> np.ndarray:
    r"""O nível depois de `dias` em `mundos` sorteados, começando em zero.

    O desvio de cada mundo é a `soma de `dias` incrementos independentes`: é o mesmo objeto
    do capítulo anterior, agora empilhado. O sorteio entra por parâmetro (o `rng`), e nunca
    pela semente global.
    """
    if dias < 1 or mundos < 1:
        raise ValueError("passeio de %r dias, %r mundos" % (dias, mundos))
    return rng.normal(0.0, desvio_diario, size=(mundos, dias)).sum(axis=1)


def mudancas_de_nivel(precos, dias: int) -> np.ndarray:
    r"""As mudanças de nível em `dias` na série real, em logaritmo, sobrepostas.

    É a leitura honesta do dado: em vez de escolher um pedaço, mede-se a dispersão de todas as
    janelas do mesmo tamanho. Se o mundo fosse feito de incrementos independentes com a mesma
    lei, essa dispersão seria o desvio de um dia vezes a raiz dos dias.
    """
    if dias < 1:
        raise ValueError("janela de %r dias" % dias)
    niveis = np.log(pd.Series(precos, dtype=float))
    return niveis.diff(dias).dropna().to_numpy()
