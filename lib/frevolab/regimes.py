r"""Regimes: quantas explicações cabem nos mesmos dados.

Volta 3, a geometria do condicionamento. O capítulo 5 deixou a pergunta em termos de informação
--- quanta cabe num pedaço finito de passado ---, e este módulo a torna contável: dada uma
família de explicações e um conjunto de estatísticas medidas no dado, **quantos membros da
família reproduzem todas elas** dentro da tolerância?

A conta é grosseira de propósito. Não é estimação, não é verossimilhança, não é otimização: é
uma grade, um punhado de estatísticas e uma contagem. O que ela mede é a **forma** do conjunto
factível, e é isso que decide duas coisas diferentes que costumam ser confundidas:

1. uma estatística que deixa **região** --- muitas explicações cabem, e o dado não escolhe entre
   elas;
2. uma estatística que corta **a zero** --- nenhuma explicação da família cabe, e o dado refuta
   a família inteira.

**O defeito que este módulo torna impossível.** Dizer "o modelo explica os dados" sem dizer
*qual* dos dois casos é. Uma taxa média é reproduzida por quase toda a família; o agrupamento
dos dias ruins, não. Quem só olha a primeira conclui que encontrou o mecanismo.

Toda função que sorteia recebe o \texttt{rng} por parâmetro e não toca a semente global. A
família tem duas leis --- calma e agitada --- e, na versão persistente, um terceiro parâmetro: a
duração média do regime agitado. Sem ele, o estado é sorteado de novo a cada dia, e é por isso
que a família sem persistência não alcança o agrupamento do dado.
"""
import numpy as np
import pandas as pd

TAXA_PADRAO = 0.05
JANELA_PADRAO = 252
POSTO_PADRAO = 13
BLOCO_PADRAO = 60

__all__ = ["TAXA_PADRAO", "JANELA_PADRAO", "POSTO_PADRAO", "BLOCO_PADRAO", "estatisticas",
           "mistura", "persistente", "cabem"]


def estatisticas(valores, janela: int = JANELA_PADRAO, posto: int = POSTO_PADRAO,
                 bloco: int = BLOCO_PADRAO, taxa: float = TAXA_PADRAO) -> dict:
    r"""As quatro leituras do dado: a taxa, o pior bloco, a mediana e o excesso de blocos cheios.

    A taxa é a leitura que a promessa do capítulo 1 entrega; as outras três são a forma com que
    os rompimentos chegam, e é aí que as famílias se separam.
    """
    v = np.asarray(valores, dtype=float)
    if v.size <= janela + bloco:
        raise ValueError("serie curta demais para a janela e o bloco")
    janelas = np.lib.stride_tricks.sliding_window_view(v, janela)
    corte = np.partition(janelas, posto - 1, axis=1)[:, posto - 1][:-1]
    rompe = (v[janela:] < corte).astype(float)
    blocos = pd.Series(rompe).rolling(bloco).sum().dropna().to_numpy()
    return {
        "taxa": float(rompe.mean()),
        "pior": int(blocos.max()),
        "mediana": float(np.median(blocos)),
        "acima_do_dobro": float((blocos > 2 * bloco * taxa).mean()),
    }


def mistura(n: int, rng: np.random.Generator, sigma: float, p: float, razao: float) -> np.ndarray:
    r"""Duas leis, sorteadas todo dia: o estado de hoje não diz nada sobre o de amanhã.

    A oscilação global é preservada qualquer que seja \emph{p}: a lei calma encolhe para que a
    média das variâncias continue sendo \emph{sigma}, de modo que comparar membros da família
    compare o mecanismo e não o tamanho.
    """
    if not 0.0 < p < 1.0:
        raise ValueError("a probabilidade do regime agitado precisa estar entre 0 e 1")
    if razao <= 1.0:
        raise ValueError("a razao entre as duas leis precisa ser maior que um")
    calma = sigma / np.sqrt(1.0 + p * (razao ** 2 - 1.0))
    agitada = calma * razao
    return rng.normal(0.0, np.where(rng.random(n) < p, agitada, calma))


def persistente(n: int, rng: np.random.Generator, sigma: float, p: float, razao: float,
                permanencia: float) -> np.ndarray:
    r"""As mesmas duas leis, com o estado durando: a permanência é a duração média do regime.

    A cadeia tem dois estados e trocas assimétricas, porque a simétrica não serve: com a mesma
    probabilidade de trocar nos dois sentidos a proporção estacionária fica presa em metade, e
    não em \emph{p}. Dada a duração média do regime agitado, a do regime calmo sai da conta
    \emph{p = d/(d + c)}, que é o que mantém a oscilação global comparável entre os membros da
    família.
    """
    if permanencia < 1.0:
        raise ValueError("a permanencia media precisa ser de pelo menos um dia")
    if not 0.0 < p < 1.0:
        raise ValueError("a probabilidade do regime agitado precisa estar entre 0 e 1")
    calma = sigma / np.sqrt(1.0 + p * (razao ** 2 - 1.0))
    agitada = calma * razao
    dura_calma = permanencia * (1.0 - p) / p
    sai_do_agitado = 1.0 / permanencia
    sai_do_calmo = 1.0 / dura_calma
    estado = np.empty(n, dtype=bool)
    estado[0] = rng.random() < p
    for i in range(1, n):
        troca = sai_do_agitado if estado[i - 1] else sai_do_calmo
        estado[i] = (not estado[i - 1]) if rng.random() < troca else estado[i - 1]
    return rng.normal(0.0, np.where(estado, agitada, calma))


def cabem(candidatos: list, real: dict, tolerancia: dict, chaves) -> list:
    r"""Os candidatos que reproduzem todas as estatísticas pedidas dentro da tolerância."""
    return [c for c in candidatos
            if all(abs(c["estatisticas"][k] - real[k]) <= tolerancia[k] for k in chaves)]
