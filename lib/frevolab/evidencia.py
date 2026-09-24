r"""A evidência: quantas explicações cabem, e com que folga cada uma cabe.

O capítulo da tolerância responde **quantas** peças da família reproduzem as quatro estatísticas
do dado. Ele não responde **quanto** cada uma tem a favor: duas peças que cabem dentro da mesma
tolerância são apresentadas como empatadas, e o leitor fica sem saber se o empate é exato ou se uma
delas está na borda.

Este módulo mede a folga. Cada peça é medida contra o dado estatística por estatística, na unidade
da tolerância daquela estatística --- de modo que a distância 1 é exatamente a fronteira da
tolerância, e 0,5 é metade do que se aceita. A peça que fica mais perto tem mais a favor, e a razão
entre as duas primeiras folgas é o que o capítulo não imprimia.

**O defeito que este módulo torna impossível.** Chamar de empate o que é uma ordem com folga
pequena --- ou, o que é pior, apresentar como empatadas duas peças que estão uma na fronteira e
outra no meio da região.

**O que este módulo NÃO é.** Ele não é um fator de Bayes. Um peso no sentido bayesiano exigiria a
distribuição amostral das estatísticas sob cada peça --- quantas vezes cada peça produziria os
números que o dado mostrou ---, e essa distribuição vive numa replicação que o caderno da família
não faz. O que se mede aqui é a folga dentro do critério declarado, e é isso que a seção declara.
"""
import numpy as np
import pandas as pd

from . import dados, regimes, volatilidade

SERIE_PADRAO = "sp500.csv"
JANELA_PADRAO, POSTO_PADRAO, BLOCO_PADRAO = 252, 13, 60
GRADE_P_PADRAO = (0.02, 0.05, 0.08, 0.12, 0.18, 0.25)
GRADE_RAZAO_PADRAO = (1.5, 2.0, 2.5, 3.0, 3.5, 4.0)
GRADE_PERMANENCIA_PADRAO = (1.0, 10.0, 30.0, 60.0, 120.0)
TOLERANCIA_PADRAO = {"taxa": 0.002, "pior": 2.0, "mediana": 1.0, "acima_do_dobro": 0.03}
CHAVES_PADRAO = ("taxa", "pior", "mediana", "acima_do_dobro")
SEMENTE_PADRAO = 131

__all__ = ["familia", "margens", "as_que_cabem", "SERIE_PADRAO", "CHAVES_PADRAO",
           "TOLERANCIA_PADRAO", "GRADE_P_PADRAO", "GRADE_RAZAO_PADRAO",
           "GRADE_PERMANENCIA_PADRAO", "JANELA_PADRAO", "POSTO_PADRAO", "BLOCO_PADRAO",
           "SEMENTE_PADRAO"]


def familia(serie: str = SERIE_PADRAO, semente: int = SEMENTE_PADRAO,
            grade_p=GRADE_P_PADRAO, grade_razao=GRADE_RAZAO_PADRAO,
            grade_permanencia=GRADE_PERMANENCIA_PADRAO) -> tuple:
    """A família persistente do capítulo, e as quatro estatísticas do dado.

    A conta é a mesma do caderno do condicionamento: uma peça por combinação, medida na série do
    primeiro mercado, com a semente declarada.
    """
    retornos = volatilidade.retornos_log(dados.carregar_serie(serie))
    x = retornos.to_numpy()
    sigma = float(x.std(ddof=1))
    real = regimes.estatisticas(x, JANELA_PADRAO, POSTO_PADRAO, BLOCO_PADRAO)
    sorteio = np.random.default_rng(int(semente))
    pecas = []
    for p in grade_p:
        for razao in grade_razao:
            for permanencia in grade_permanencia:
                e = regimes.estatisticas(
                    regimes.persistente(len(x), sorteio, sigma, p, razao, permanencia),
                    JANELA_PADRAO, POSTO_PADRAO, BLOCO_PADRAO)
                d = {k: abs(e[k] - real[k]) / TOLERANCIA_PADRAO[k] for k in CHAVES_PADRAO}
                pecas.append({"p": p, "razao": razao, "permanencia": permanencia,
                              "folga": float(max(d.values())),
                              "quem_manda": max(d, key=d.get),
                              **{"dist_" + k: float(v) for k, v in d.items()}})
    return pecas, real


def as_que_cabem(pecas: list, tolerancia: float = 1.0) -> list:
    """As peças cuja pior estatística ainda está dentro da tolerância --- as que o capítulo conta."""
    return [c for c in pecas if c["folga"] <= float(tolerancia)]


def margens(pecas: list, quantas: int = 5) -> list:
    """As peças mais próximas do dado, da mais próxima para a mais distante."""
    return sorted(pecas, key=lambda c: c["folga"])[:int(quantas)]

def contagem(dias: int, grade_p=GRADE_P_PADRAO, grade_razao=GRADE_RAZAO_PADRAO,
             grade_permanencia=GRADE_PERMANENCIA_PADRAO, serie: str = SERIE_PADRAO,
             semente: int = SEMENTE_PADRAO) -> dict:
    """Quantas pecas da familia cabem, numa grade e num comprimento de serie declarados.

    A pergunta do capitulo da tolerancia --- quantas explicacoes reproduzem o dado --- depende de
    DUAS coisas que ele nao varia: quantas pecas foram tentadas e quantos dias foram vistos. Esta
    funcao varia as duas, e a contagem sai com elas.
    """
    retornos = volatilidade.retornos_log(dados.carregar_serie(serie))
    x = retornos.to_numpy()[:int(dias)]
    sigma = float(x.std(ddof=1))
    real = regimes.estatisticas(x, JANELA_PADRAO, POSTO_PADRAO, BLOCO_PADRAO)
    sorteio = np.random.default_rng(int(semente))
    pecas = []
    for p in grade_p:
        for razao in grade_razao:
            for permanencia in grade_permanencia:
                e = regimes.estatisticas(
                    regimes.persistente(len(x), sorteio, sigma, p, razao, permanencia),
                    JANELA_PADRAO, POSTO_PADRAO, BLOCO_PADRAO)
                pecas.append({k: abs(e[k] - real[k]) <= TOLERANCIA_PADRAO[k] for k in CHAVES_PADRAO})
    cabem = sum(1 for c in pecas if all(c.values()))
    return {"dias": int(dias), "tentadas": len(pecas), "cabem": int(cabem),
            "fracao_pct": 100.0 * cabem / max(1, len(pecas))}
