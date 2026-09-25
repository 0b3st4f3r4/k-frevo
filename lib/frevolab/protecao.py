r"""O capital que cobre a perda no nível prometido --- e o que a dependência cobra por isso.

A pergunta é a da lista viva: quanto custa a proteção que de fato protege? Somar as proteções
marginais é a conta que ignora o junto; calibrar a barreira na dependência medida é a conta que o
capítulo da queda conjunta tornou possível; e a família de choque comum do capítulo da margem é o
laboratório onde o preço anda com o que o segundo momento não vê \cite{taleb2020option}. Com poucos
eventos conjuntos, nenhum destes números vale sem intervalo --- a reamostragem é parte do resultado
\cite{efron1979bootstrap}.

**As moedas são duas e declaradas**: o capital em unidades do nível da carteira, e a fração do
prejuízo conjunto que o capital deixa de cobrir. O refutador da pergunta também é declarado: se a
barreira correta custar o mesmo que a errada, a pergunta cai --- e é isso que as pernas
independentes têm de mostrar.
"""
import numpy as np
import pandas as pd

from . import dependencia, promessa

JANELA_PADRAO = 252
CAUDA_PADRAO = 0.05
PESOS_PADRAO = (0.5, 0.5)
NIVEL_PADRAO = 0.05
BLOCO_PADRAO = 60
REPETICOES_PADRAO = 200

__all__ = ["capital_marginal", "perdas_conjuntas", "capital_conjunto", "descoberto", "intervalo"]


def capital_marginal(retornos_a: pd.Series, retornos_b: pd.Series,
                     janela: int = JANELA_PADRAO, cauda: float = CAUDA_PADRAO,
                     pesos=PESOS_PADRAO) -> float:
    r"""A conta das margens: a soma dos cortes prometidos, na participação da carteira.

    O corte que cada perna promete é o de sempre --- o posto da janela na cauda declarada ---, e o
    capital marginal é a mediana do corte de cada perna participada pelos pesos. É a conta que
    ignora o junto: cobre cada perna no seu nível, e o dia em que as duas caem juntas entra nela
    como se fosse dois dias separados.
    """
    ca = promessa.corte(retornos_a, janela, cauda).abs()
    cb = promessa.corte(retornos_b, janela, cauda).abs()
    comuns = ca.index.intersection(cb.index)
    return float(pesos[0] * ca.loc[comuns].median() + pesos[1] * cb.loc[comuns].median())


def perdas_conjuntas(retornos_a: pd.Series, retornos_b: pd.Series,
                     janela: int = JANELA_PADRAO, cauda: float = CAUDA_PADRAO,
                     pesos=PESOS_PADRAO) -> pd.Series:
    r"""Os dias em que as duas pernas rompem o próprio corte, e a perda da carteira neles.

    O instrumento é o da queda conjunta, re-usado sem peça nova: rompimento é cruzar o próprio
    corte de janela e posto. A perda da carteira é positiva e vem participada pelos pesos.
    """
    rompe_a = dependencia.rompimentos(retornos_a, janela, cauda)
    rompe_b = dependencia.rompimentos(retornos_b, janela, cauda)
    juntos = rompe_a.index.intersection(rompe_b.index)
    mascara = rompe_a.loc[juntos].to_numpy() & rompe_b.loc[juntos].to_numpy()
    dias = juntos[mascara]
    carteira = pesos[0] * retornos_a.loc[dias] + pesos[1] * retornos_b.loc[dias]
    return -carteira


def capital_conjunto(perdas: pd.Series, nivel: float = NIVEL_PADRAO) -> float:
    r"""A conta do junto: o quantil prometido da perda nos dias conjuntos.

    Com poucos eventos este quantil é o que ele é --- a leitura de pouca evidência ---, e é por
    isso que quem o cita viaja com intervalo.
    """
    if len(perdas) < 4:
        raise ValueError("dias conjuntos de menos para ler um quantil")
    return float(np.quantile(np.asarray(perdas, dtype=float), 1.0 - nivel))


def descoberto(capital: float, perdas: pd.Series) -> float:
    r"""A fração do prejuízo conjunto que o capital dado deixa de cobrir.

    É a moeda do capítulo da queda conjunta: de cada perda, o capital absorve o que dá e o resto
    fica descoberto; a fração é a média do resto sobre a média da perda.
    """
    valores = np.asarray(perdas, dtype=float)
    absorvido = np.minimum(valores, capital)
    return float(1.0 - absorvido.mean() / valores.mean())


def intervalo(retornos_a: pd.Series, retornos_b: pd.Series,
              janela: int = JANELA_PADRAO, cauda: float = CAUDA_PADRAO,
              pesos=PESOS_PADRAO, nivel: float = NIVEL_PADRAO,
              bloco: int = BLOCO_PADRAO, repeticoes: int = REPETICOES_PADRAO,
              semente: int = 0) -> dict:
    r"""Os intervalos das três grandezas, por reamostragem em blocos do dia.

    Os dias comuns viajam em blocos inteiros --- as duas pernas juntas --- e a conta inteira corre
    de novo em cada réplica: rompimentos, perdas conjuntas, capitais e descoberto. O intervalo é o
    quantil das réplicas que têm conta (réplica sem dia conjunto nenhum não tem quantil).
    """
    comuns = retornos_a.index.intersection(retornos_b.index)
    a = np.asarray(retornos_a.loc[comuns], dtype=float)
    b = np.asarray(retornos_b.loc[comuns], dtype=float)
    n = comuns.size
    quantos = int(np.ceil(n / bloco))
    cap, des_m, des_c = [], [], []
    for i in range(repeticoes):
        rng = np.random.default_rng(semente + i)
        inicios = rng.integers(0, n - bloco, quantos)
        escolha = np.concatenate([np.arange(ini, min(n, ini + bloco)) for ini in inicios])[:n]
        sa = pd.Series(a[escolha], index=comuns)
        sb = pd.Series(b[escolha], index=comuns)
        perdas = perdas_conjuntas(sa, sb, janela=janela, cauda=cauda, pesos=pesos)
        if len(perdas) < 4:
            continue
        margem = capital_marginal(sa, sb, janela=janela, cauda=cauda, pesos=pesos)
        junto = capital_conjunto(perdas, nivel=nivel)
        cap.append(junto)
        des_m.append(descoberto(margem, perdas))
        des_c.append(descoberto(junto, perdas))
    if len(cap) < 2:
        return {k: (float("nan"), float("nan")) for k in ("capital", "descoberto_marginal", "descoberto_conjunto")}
    saida = {}
    for nome, valores in (("capital", cap), ("descoberto_marginal", des_m), ("descoberto_conjunto", des_c)):
        saida[nome] = (float(np.quantile(valores, 0.025)), float(np.quantile(valores, 0.975)))
    return saida
