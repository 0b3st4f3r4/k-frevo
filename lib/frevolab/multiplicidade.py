r"""A multiplicidade: quantas barras eu ergui antes de acreditar numa.

O capítulo da estatística que não anuncia compara **quatro sinais dentro de dez faixas**, em cada
série, e julga cada comparação contra uma barra de dois desvios. A barra está certa para UMA
comparação: sob o próprio nulo do capítulo --- nenhuma relação entre o sinal e o futuro ---, a
correlação de posto é ruído simétrico, e dois desvios deixam passar cerca de 4,55% das vezes.

O que o capítulo não faz é a conta da **bateria**: com \emph{m} comparações, a chance de que AO
MENOS UMA cruze a barra por acaso é \emph{1 - (1-alfa)^m}, que em \emph{m = 40} passa de 84%. Um
capítulo que separa os sinais pela barra por comparação está separando por um critério que, no
mundo que não muda, quase sempre acende alguma coisa.

**O defeito que este módulo torna impossível.** Julgar uma bateria pela barra de um.item A barra
da bateria é outra: para manter 5% no conjunto, ela precisa estar em \emph{3,22} desvios quando as
comparações são quarenta.

A bateria medida é a do capítulo --- os quatro sinais do caderno da estabilidade, medidos dentro
de dez faixas de oscilação, contra os rompimentos dos sessenta dias seguintes ---, e ela roda aqui
nos mundos que NUNCA mudam, que é onde o nulo do capítulo vive.
"""
import numpy as np
import pandas as pd

ALFA_PADRAO = 0.05
INFLACAO_PADRAO = 2.0
SINAIS_PADRAO = 4
FAIXAS_PADRAO = 10
DIAS_PADRAO = 3000
JANELA_PADRAO = 252
POSTO_PADRAO = 13
BLOCO_PADRAO = 60
MUNDOS_PADRAO = 200
SEMENTE_PADRAO = 7000

__all__ = ["fwer_exata", "quantil_da_familia", "comparacoes", "bateria", "ALFA_PADRAO",
           "INFLACAO_PADRAO", "SINAIS_PADRAO", "FAIXAS_PADRAO", "MUNDOS_PADRAO"]


def fwer_exata(m: int, alfa: float = ALFA_PADRAO) -> float:
    """A chance de ao menos uma travessia por acaso, com m comparações independentes."""
    return 1.0 - (1.0 - float(alfa)) ** int(m)


def quantil_da_familia(m: int, alfa: float = ALFA_PADRAO) -> float:
    """Quantos desvios a barra precisa ter para a BATERIA ficar em alfa.

    A conta e a de Sidak: a barra de uma comparacao vale 1-(1-alfa)^(1/m) em probabilidade, e o
    quantil sai dela. Com uma comparacao so, devolve os mesmos dois desvios de sempre.
    """
    from math import sqrt
    from scipy.stats import norm
    por_comparacao = 1.0 - (1.0 - float(alfa)) ** (1.0 / int(m))
    return float(norm.isf(por_comparacao / 2.0))


def comparacoes(sinais: int = SINAIS_PADRAO, faixas: int = FAIXAS_PADRAO) -> int:
    """Quantas barras a bateria do capitulo ergue: sinais x faixas."""
    return int(sinais) * int(faixas)


def bateria(mundos: int = MUNDOS_PADRAO, semente: int = SEMENTE_PADRAO,
            dias: int = DIAS_PADRAO, janela: int = JANELA_PADRAO, posto: int = POSTO_PADRAO,
            bloco: int = BLOCO_PADRAO, faixas: int = FAIXAS_PADRAO,
            inflacao: float = INFLACAO_PADRAO, sigma: float = 0.012) -> dict:
    """A bateria do capitulo dentro dos mundos que nunca mudam.

    Cada mundo e uma serie de nivel constante (o mundo parado do capitulo do alarme), e nela os
    quatro sinais do caderno da estabilidade sao medidos contra os rompimentos dos dias seguintes.
    O que se conta por mundo e quantas das comparacoes cruzam a barra --- e quantos mundos tem ao
    menos uma travessia.
    """
    from . import estabilidade, mudanca, promessa

    sorteio = np.random.default_rng(int(semente))
    travessias, primeira = [], []
    for _ in range(int(mundos)):
        x = mudanca.degrau(int(dias), sorteio, fator=1.0)
        serie = pd.Series(np.asarray(x, dtype=float), index=pd.RangeIndex(int(dias)))
        corte = promessa.corte(serie, int(janela), float(posto) / float(janela)).to_numpy()
        serie = serie.to_numpy()
        rompe = (serie < corte).astype(float)
        futuro = np.full(serie.size, np.nan)
        futuro[:-int(bloco)] = (np.nan_to_num(rompe) * 1.0)[int(bloco):]
        contagem = np.full(serie.size, np.nan)
        contagem[int(bloco):] = np.convolve(np.nan_to_num(rompe), np.ones(int(bloco)), "valid")[:serie.size - int(bloco)]
        movimento = np.full(serie.size, np.nan)
        movimento[int(bloco):] = (corte[int(bloco):] - corte[:-int(bloco)]) / np.abs(corte[:-int(bloco)])
        oscilacao = np.full(serie.size, np.nan)
        for k in range(int(bloco), serie.size):
            oscilacao[k] = serie[k - int(bloco):k].std(ddof=1)
        relativo = corte / oscilacao

        quantas, menor = 0, None
        for sinal in (movimento, contagem, corte, relativo):
            util = ~np.isnan(sinal) & ~np.isnan(futuro)
            if util.sum() < 2 * int(faixas):
                continue
            blocos = np.array_split(np.argsort(sinal[util]), int(faixas))
            esperado = float(np.nanmean(futuro[util]))
            desvio = float(np.nanstd(futuro[util], ddof=1)) or 1.0
            for pedaco in blocos:
                z = (float(np.nanmean(futuro[util][pedaco])) - esperado) / (desvio / float(np.sqrt(len(pedaco))))
                if abs(z) >= float(inflacao):
                    quantas += 1
                if menor is None or abs(z) < menor:
                    menor = abs(z)
        travessias.append(quantas)
        primeira.append(menor if menor is not None else np.nan)
    travessias = np.array(travessias)
    return {"mundos": int(mundos), "comparacoes": comparacoes(faixas=faixas),
            "travessias_media": float(travessias.mean()),
            "travessias_maxima": int(travessias.max()),
            "mundos_com_alguma": int((travessias > 0).sum()),
            "taxa_por_comparacao": float(travessias.sum() / (int(mundos) * comparacoes(faixas=faixas))),
            "taxa_da_bateria": float((travessias > 0).mean()),
            "menor_z_media": float(np.nanmean(primeira))}

def selecao_ebh(e_valores, taxa: float = ALFA_PADRAO) -> dict:
    r"""A seleção e-BH: as descobertas escolhidas com a fração de falsos assinada.

    Com os e-valores em ordem decrescente, o procedimento corta no maior $k$ com
    $e_{(k)} \ge m/(taxa\, k)$ --- o análogo do Benjamini--Hochberg para e-valores, e ele controla
    a fração de falsos sob dependência ARBITRÁRIA entre as comparações, porque a média de
    e-valores é e-valor. Devolve quais entram, quantos entraram e o corte em e.
    """
    E = np.asarray(e_valores, dtype=float)
    if E.ndim != 1 or E.size < 1:
        raise ValueError("a selecao quer um vetor de e-valores")
    if not 0.0 < taxa < 1.0:
        raise ValueError("a taxa precisa estar entre zero e um")
    if np.any(E < 0.0):
        raise ValueError("e-valor nao pode ser negativo")
    m = E.size
    ordem = np.argsort(-E)
    ordenados = E[ordem]
    k_maior = 0
    for k in range(1, m + 1):
        if ordenados[k - 1] >= m / (taxa * k):
            k_maior = k
    escolhidos = ordem[:k_maior]
    return {"indices": escolhidos, "quantidade": int(k_maior),
            "corte": float(ordenados[k_maior - 1]) if k_maior else float("inf"),
            "comparacoes": int(m)}
