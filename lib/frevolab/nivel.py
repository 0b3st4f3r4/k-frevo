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

**A inclinação da banda em toda escala.** O passo médio do caminho --- quanto o nível andou
em `k` dias, em média, sobre todas as janelas --- cresce com o atraso, e o crescimento tem
inclinação: o expoente do caminho, lido como a rampa do log-passo contra o log-atraso, e a
dimensão do caminho, que é a mesma reta lida do outro lado, dois menos o expoente. **O
defeito que este instrumento torna impossível:** comparar inclinações medidas com atrasos
diferentes e janelas contadas diferentes --- aqui os atrasos são argumento, a regra de
janelas é uma só, e tudo que se compara passa pela mesma conta.
"""
__all__ = ["soma_das_variacoes", "produto_das_variacoes", "soma_dos_logs", "contas_do_pedaco",
           "desvio_do_nivel", "mundos_do_passeio", "mudancas_de_nivel", "passo_do_caminho",
           "expoente_do_caminho", "dimensao_do_caminho", "expoente_do_baralhado"]

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


def passo_do_caminho(precos, atrasos) -> dict:
    r"""O passo médio do caminho em cada atraso: quanto o nível andou em `k` dias, em média.

    Para cada atraso `k`, a média de `|log p_{t+k} - log p_t|` sobre todas as janelas da
    série, sobrepostas --- e sem normalização por `k`, o que é declaração e não acidente:
    o passo médio cresce com o atraso, e é o crescimento dele que o expoente lê. É o mesmo
    objeto da `mudancas_de_nivel`, agora no valor absoluto e em todas as escalas de uma vez.
    """
    niveis = np.log(np.asarray(precos, dtype=float))
    n = niveis.size
    saida = {}
    for atraso in atrasos:
        k = int(atraso)
        if k < 1 or k >= n:
            raise ValueError("atraso de %r dias numa série de %d: não há janela" % (k, n))
        saida[k] = float(np.mean(np.abs(niveis[k:] - niveis[:n - k])))
    return saida


def expoente_do_caminho(precos, atrasos, janelas_minimas: int = 30) -> float:
    r"""A inclinação do passo médio contra o atraso: a rampa em log-log, por mínimos quadrados.

    Só entram no ajuste os atrasos com pelo menos `janelas_minimas` janelas de sobra ---
    quem não sustenta um ponto da reta fica de fora, e com menos de dois atrasos válidos o
    expoente é `nan`, o «não tem sentido» do precedente `profundidade.expoente`. Na série
    plana o passo é zero em todo atraso e expoente declarado é zero: é o caminho que não
    alarga em escala nenhuma.
    """
    if janelas_minimas < 1:
        raise ValueError("não há regra de %r janelas mínimas" % janelas_minimas)
    n = np.asarray(precos, dtype=float).size
    validos = list(dict.fromkeys(int(k) for k in atrasos if n - int(k) >= janelas_minimas))
    if not validos:
        return float("nan")
    passos = passo_do_caminho(precos, validos)
    pontos = [(k, passos[k]) for k in validos if passos[k] > 0.0]
    if not pontos:
        return 0.0
    if len(pontos) < 2:
        return float("nan")
    xs = np.log(np.asarray([float(k) for k, _ in pontos]))
    ys = np.log(np.asarray([v for _, v in pontos]))
    return float(np.polyfit(xs, ys, 1)[0])


def dimensao_do_caminho(precos, atrasos, janelas_minimas: int = 30) -> float:
    r"""A dimensão do caminho: a mesma reta lida do outro lado, dois menos o expoente.

    No passeio puro o expoente é meio e a dimensão, três meios; quanto mais liso o caminho,
    mais perto de um fica o expoente --- e de um, a dimensão. É a leitura de Higuchi
    \cite{higuchi1988approach}: a inclinação é um número repetível, e um número só
    caracteriza a série inteira.
    """
    return 2.0 - expoente_do_caminho(precos, atrasos, janelas_minimas)


def expoente_do_baralhado(retornos, atrasos, sorteios: int, rng, janelas_minimas: int = 30) -> dict:
    r"""O controle de ordem: o expoente dos mesmos retornos, baralhados `sorteios` vezes.

    Baralhar guarda cada retorno e destrói só a ordem --- o passeio reconstruído com os
    mesmos dias em outra ordem é o nulo contra o qual o expoente da série se lê: se a
    inclinação da série fosse obra dos tamanhos dos dias, o baralhado a reproduziria. O
    loop mora aqui, e o sorteio entra por `rng`. O dicionário traz a média, a dispersão e
    quantos expoentes deram número, os expoentes em si e a mediana do passo por atraso ---
    os dois últimos são o que a figura precisa, e é por isso que o loop não fica no caderno.
    """
    r = np.array(retornos, dtype=float)
    if sorteios < 1:
        raise ValueError("não há controle com %r sorteios" % sorteios)
    gammas, curvas = [], []
    for _ in range(sorteios):
        rng.shuffle(r)
        precos_b = np.exp(np.concatenate([[0.0], np.cumsum(r)]))
        curvas.append(passo_do_caminho(precos_b, atrasos))
        gammas.append(expoente_do_caminho(precos_b, atrasos, janelas_minimas))
    validos = [float(g) for g in gammas if np.isfinite(g)]
    mediana = ({k: float(np.median([c[k] for c in curvas])) for k in curvas[0]}
               if curvas else {})
    return {
        "media": float(np.mean(validos)) if validos else float("nan"),
        "dispersao": float(np.std(validos, ddof=1)) if len(validos) > 1 else float("nan"),
        "quantos": len(validos),
        "gammas": validos,
        "passo_mediana": mediana,
    }
