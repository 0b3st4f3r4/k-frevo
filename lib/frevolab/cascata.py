"""A perna que falta: a cascata calibrada contra o choque comum.

O capítulo do relógio separou relógio de causa com o terceiro que puxa os dois --- o choque comum.
Sobrou a perna que essa família não constrói: o dia em que B rompeu PORQUE A rombeu, na cascata
(buldyrev2010catastrophic) --- a cascata sem designer de bak1987self e a que o próprio projeto
fabrica em carlson1999highly. Dois mundos, calibrados para a mesma contagem conjunta na janela de
alinhamento e para as mesmas taxas marginais declaradas: no choque, um fator comum rompe as duas
pernas no mesmo dia; na cascata, A rompe por conta própria e transmite a B depois de um lag
declarado. O alinhamento vê o atraso; a fração de B que depende de A --- o número que quantifica a
dependência --- nenhuma leitura observacional devolve: só a intervenção que bloqueia A.
"""
import numpy as np

__all__ = ["mundo_choque", "mundo_cascata", "pares_de_alinhamento",
           "calibra_transmissao", "bloqueia_a"]


def mundo_choque(dias: int, taxa_conjunta: float, marg_a: float, marg_b: float,
                 semente: int = 0) -> dict:
    r"""O mundo do fator comum: no dia de fator, as duas pernas rombem juntas (lag zero); fora
    dele, cada perna rompe sozinha na taxa condicional que faz a MARGINAL declarada dar certo ---
    porque marginais diferentes fazem acidentais diferentes, e os mundos têm de casar na margem
    para só diferir na perna que importa."""
    if not 0.0 <= taxa_conjunta <= min(marg_a, marg_b):
        raise ValueError("a taxa conjunta nao pode passar das marginais declaradas")
    rng = np.random.default_rng(semente)
    fator = rng.random(dias) < taxa_conjunta
    proprio_a = rng.random(dias) < (marg_a - taxa_conjunta) / (1.0 - taxa_conjunta)
    proprio_b = rng.random(dias) < (marg_b - taxa_conjunta) / (1.0 - taxa_conjunta)
    romp_a = fator | proprio_a
    romp_b = fator | proprio_b
    return {"romp_a": romp_a, "romp_b": romp_b,
            "b_por_cascata": np.zeros(dias, dtype=bool),
            "semente": semente}


def mundo_cascata(dias: int, marg_a: float, taxa_b_proprio: float, lags,
                  transmissao: float, semente: int = 0) -> dict:
    r"""O mundo da propagação: A rompe por conta própria na marginal declarada; cada rompimento
    de A transmite a B com a probabilidade dada, depois de um lag sorteado dentre os declarados; B
    também rompe sozinho na taxa própria. A marcação causal guarda quais rompimentos de B vieram
    de A --- é ela que a intervenção lê, e nenhuma leitura observacional vê."""
    if not 0.0 <= transmissao <= 1.0:
        raise ValueError("a probabilidade de transmissao tem de ficar em [0; 1]")
    lags = sorted(set(int(k) for k in lags))
    if not lags or min(lags) < 0:
        raise ValueError("os lags declarados tem de ser inteiros nao negativos")
    rng = np.random.default_rng(semente)
    dias_a = np.flatnonzero(rng.random(dias) < marg_a)
    transmite = rng.random(dias_a.size) < transmissao
    lag_sorteado = np.array(lags)[rng.integers(0, len(lags), size=dias_a.size)]
    b_por_cascata = np.zeros(dias, dtype=bool)
    for dia, passa, lag in zip(dias_a, transmite, lag_sorteado):
        if passa and dia + lag < dias:
            b_por_cascata[dia + lag] = True
    proprio_b = rng.random(dias) < taxa_b_proprio
    romp_a = np.zeros(dias, dtype=bool)
    romp_a[dias_a] = True
    romp_b = b_por_cascata | proprio_b
    return {"romp_a": romp_a, "romp_b": romp_b,
            "b_por_cascata": b_por_cascata,
            "semente": semente}


def pares_de_alinhamento(mundo: dict, janela: int = 3) -> np.ndarray:
    r"""Os pares de alinhamento na janela declarada: para cada rompimento de B, o rompimento de A
    mais próximo dentro da janela, com o lag com sinal --- positivo é A puxando (A rompeu antes),
    zero é junto, negativo é B puxando. É a leitura observacional do capítulo: vê o atraso, e não
    vê a fração que depende de A."""
    dias = mundo["romp_a"].size
    dias_a = np.flatnonzero(mundo["romp_a"])
    lags = []
    for dia_b in np.flatnonzero(mundo["romp_b"]):
        if dias_a.size == 0:
            break
        dist = int(dia_b) - dias_a
        dentro = np.flatnonzero(np.abs(dist) <= janela)
        if dentro.size:
            lags.append(int(dist[dentro[np.argmin(np.abs(dist[dentro]))]]))
    return np.array(lags, dtype=int)


def calibra_transmissao(dias: int, marg_a: float, taxa_b_proprio: float, lags,
                        alvo_conjuntas: int, janela: int = 3, semente: int = 0) -> float:
    r"""Bisseção na probabilidade de transmissao ate a contagem de pares de alinhamento do mundo
    da cascata igualar a do mundo de choque --- com o teto de um: se a cascata nao alcanca o alvo
    nem transmitindo sempre, devolve o teto e a tolerancia declarada decide."""
    def conta(q):
        mundo = mundo_cascata(dias, marg_a, taxa_b_proprio, lags, q, semente=semente)
        return pares_de_alinhamento(mundo, janela).size
    if conta(1.0) < alvo_conjuntas:
        return 1.0
    baixo, alto = 0.0, 1.0
    for _ in range(40):
        meio = 0.5 * (baixo + alto)
        if conta(meio) < alvo_conjuntas:
            baixo = meio
        else:
            alto = meio
    return 0.5 * (baixo + alto)


def bloqueia_a(mundo: dict) -> dict:
    r"""A intervencao: bloqueia os rompimentos de A e devolve o mundo sem eles --- na cascata, os
    rompimentos de B que A transmitiu morrem junto (estao marcados); no choque, nada muda, porque
    nenhuma perna deve nada a outra. E o unico instrumento da casa que ve a perna faltante."""
    return {"romp_a": np.zeros_like(mundo["romp_a"]),
            "romp_b": mundo["romp_b"] & ~mundo["b_por_cascata"],
            "b_por_cascata": np.zeros_like(mundo["b_por_cascata"]),
            "semente": mundo["semente"]}
