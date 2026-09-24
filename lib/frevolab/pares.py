r"""Pares: a concordância dia a dia, e o preço de contar só uma parte deles.

O capítulo do dia em que tudo cai mede a dependência com uma contagem de DIAS --- quantos dias as
duas pernas rompem juntas ---, e essa conta custa uma passada sobre seis mil e duzentos dias. A
pergunta "os dois mercados andam juntos?" tem outra resposta possível, e ela não olha o dia: olha o
PAR de dias. Dois dias concordam quando os dois mercados andam para o mesmo lado, e a medida é a
fração de pares concordantes menos a de discordantes --- a concordância de Kendall.

O custo muda de natureza. Sobre \emph{n} dias há \emph{n(n-1)/2} pares: com os seis mil duzentos e
quatro dias que o capítulo usa, dezenove milhões, duzentos e quarenta e um mil, quatrocentos e seis
pares. Contar todos é o gesto caro; contar uma fração deles é o gesto econômico, e a economia cobra
em variância --- o que Blom mediu para a U-estatística incompleta.

**Duas barras diferentes, e é a confusão entre elas que este módulo desfaz.** A primeira é a barra
do SORTEIO: quanta precisão se perde por olhar \emph{m} pares em vez de todos. Os pares sorteados
são independentes uns dos outros, de modo que a covariância entre dois deles é zero --- a
sobreposição de dias que existe entre pares distintos da população não entra nessa conta ---, e o
que sobra é a lei de sempre, \emph{sigma^2/m}, com o kernel binário de variância exata
\emph{sigma^2 = 1 - tau^2}. A segunda é a barra do DADO: quanto a resposta inteira se mexe de
amostra para amostra de mercado, que é a fórmula de Hoeffding para a U-estatística completa,
\emph{(2 (n-2) sigma_1^2 + sigma^2) / C}, com \emph{C = n(n-1)/2} e \emph{sigma_1^2} a covariância
entre dois pares que compartilham um dia --- esta sim estimada por trios.

Somadas na ordem certa, as duas dizem o que a economia de pares custa de verdade: no centésimo dos
pares a barra do sorteio é dez vezes maior e ainda assim menor que a barra do dado, e é por isso que
contar dezenove milhões de pares nunca foi necessário.

**O defeito que este módulo torna impossível.** Achar que contar pares é o único jeito de ver todos
eles. A concordância exata sai de ordenar as duas séries, e não de enumerar os pares: os dezenove
milhões nunca foram necessários --- necessários são os postos.
"""
import numpy as np
import pandas as pd
from scipy.stats import kendalltau

FRAcoes_PADRAO = (1.0, 0.5, 0.1, 0.01)
SEMENTE_PADRAO = 53

__all__ = ["FRAcoes_PADRAO", "SEMENTE_PADRAO", "dias_comuns", "pares", "concordancia",
           "concordancia_amostrada", "momentos_do_kernel", "variancia_amostral",
           "variancia_do_completo", "varredura"]


def dias_comuns(serie_a, serie_b):
    """As duas séries alinhadas nos dias em que as duas existem, em ordem de data."""
    indice = serie_a.index.intersection(serie_b.index)
    a = np.asarray(serie_a.loc[indice], dtype=float)
    b = np.asarray(serie_b.loc[indice], dtype=float)
    return a, b


def pares(dias: int) -> int:
    """Quantos pares de dias distintos existem: n(n-1)/2."""
    n = int(dias)
    if n < 2:
        raise ValueError("são precisos ao menos dois dias para haver um par")
    return n * (n - 1) // 2


def concordancia(serie_a, serie_b) -> dict:
    """A concordância exata, de todos os pares --- sem enumerar nenhum deles.

    A conta sai de ordenar as duas séries: o número de pares concordantes é o de inversões de uma
    permutação, e inversões se contam em n log n. O número de pares existe, e é impresso; o que não
    existe é a lista deles.
    """
    a, b = dias_comuns(serie_a, serie_b)
    resultado = kendalltau(a, b)
    tau = float(resultado.statistic)
    if np.isnan(tau):
        raise ValueError("a concordância não é definida com uma das séries constante")
    n = a.size
    return {"tau": tau, "dias": int(n), "pares": pares(n), "sigma_2": 1.0 - tau ** 2}


def concordancia_amostrada(serie_a, serie_b, quantos: int, rng: np.random.Generator) -> dict:
    """A concordância com uma parte dos pares: a U-estatística incompleta.

    Os pares são sorteados com os dois índices independentes e descartando o caso degenerado em que
    os dois são o mesmo dia --- que não é um par.
    """
    a, b = dias_comuns(serie_a, serie_b)
    n = a.size
    m = int(quantos)
    if m < 1:
        raise ValueError("a amostra precisa de ao menos um par")
    if m > pares(n):
        raise ValueError("não há tantos pares quanto se pede: %d contra %d" % (m, pares(n)))
    i = rng.integers(0, n, size=m)
    j = rng.integers(0, n, size=m)
    vale = i != j
    i, j = i[vale], j[vale]
    kernel = np.sign((a[i] - a[j]) * (b[i] - b[j]))
    return {"tau": float(kernel.mean()), "pares": int(i.size), "amostrados": m, "sigma_2": None}


def momentos_do_kernel(serie_a, serie_b, trios: int = 200000,
                       rng: np.random.Generator = None) -> dict:
    """Os dois números que a variância precisa: sigma^2 exato, sigma_1^2 estimado por trios.

    sigma^2 é a variância do kernel binário, e vale 1 - tau^2 sem estimativa nenhuma. sigma_1^2 é a
    covariância entre dois pares que compartilham um dia, e sai da média do produto dos dois kernels
    de um trio de dias distintos, menos o quadrado da concordância.
    """
    if rng is None:
        rng = np.random.default_rng(SEMENTE_PADRAO)
    a, b = dias_comuns(serie_a, serie_b)
    tau = float(kendalltau(a, b).statistic)
    n = a.size
    i = rng.integers(0, n, size=int(trios))
    j = rng.integers(0, n, size=int(trios))
    k = rng.integers(0, n, size=int(trios))
    vale = (i != j) & (i != k) & (j != k)
    i, j, k = i[vale], j[vale], k[vale]
    h_ij = np.sign((a[i] - a[j]) * (b[i] - b[j]))
    h_ik = np.sign((a[i] - a[k]) * (b[i] - b[k]))
    produto = float(np.mean(h_ij * h_ik))
    return {"tau": tau, "sigma_2": 1.0 - tau ** 2, "sigma_1_2": produto - tau ** 2,
            "trios": int(i.size), "dias": int(n)}


def variancia_amostral(sigma_2: float, quantos: int) -> float:
    """A barra do SORTEIO: quanto custa olhar m pares em vez de todos.

    Os pares sorteados são independentes entre si, e a variância da média é sigma^2/m --- sem
    correção de sobreposição, porque não há sobreposição no sorteio.
    """
    m = int(quantos)
    if m < 1:
        raise ValueError("a amostra precisa de ao menos um par")
    return float(sigma_2) / m


def variancia_do_completo(dias: int, sigma_2: float, sigma_1_2: float) -> float:
    """A barra do DADO: quanto a resposta se mexe de amostra para amostra (Hoeffding, ordem dois)."""
    n = int(dias)
    C = pares(n)
    return (2.0 * (n - 2) * float(sigma_1_2) + float(sigma_2)) / C


def varredura(serie_a, serie_b, fracoes=FRAcoes_PADRAO, mundos: int = 40,
              rng: np.random.Generator = None) -> list:
    """A concordância com uma fração dos pares, contra o que as duas fórmulas preveem.

    Devolve uma linha por fração: o desvio medido entre os mundos, o previsto pela fórmula
    incompleta, e o que a fórmula completa promete com todos os pares.
    """
    if rng is None:
        rng = np.random.default_rng(SEMENTE_PADRAO)
    exato = concordancia(serie_a, serie_b)
    numeros = momentos_do_kernel(serie_a, serie_b, rng=rng)
    C = exato["pares"]
    linhas = []
    for fracao in fracoes:
        m = max(1, int(round(fracao * C)))
        taus = np.array([concordancia_amostrada(serie_a, serie_b, m, rng)["tau"]
                         for _ in range(int(mundos))])
        linhas.append({
            "fracao": float(fracao), "pares": m, "tau_medio": float(taus.mean()),
            "desvio_medido": float(taus.std(ddof=1)),
            "desvio_previsto": float(np.sqrt(variancia_amostral(numeros["sigma_2"], m))),
            "desvio_do_dado": float(np.sqrt(variancia_do_completo(
                exato["dias"], numeros["sigma_2"], numeros["sigma_1_2"]))),
            "exato": exato["tau"],
        })
    return linhas
