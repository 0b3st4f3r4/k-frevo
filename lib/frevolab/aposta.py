r"""A aposta: o orçamento que sobrevive a ser lido todo dia.

O vigia do capítulo do orçamento foi calibrado para **uma** leitura. Ele declara que soa uma vez a
cada tantos anos de mundo parado, e essa conta vale para quem pergunta no fim. Quem olha o alarme
todo dia e age na primeira vez que ele soa gasta o orçamento muitas vezes --- é o teto da união,
agora no tempo, e ele passa de cem por cento do mesmo jeito que passava entre limiares.

A saída não é olhar menos: é trocar o limiar por um **capital**. Em cada bloco de dias conta-se
quantas violações houve, e o bloco vale a razão de verossimilhanças

    e_t = (p1/p0)^L_t * ((1-p1)/(1-p0))^(bloco - L_t),

entre o mundo que mudou (taxa \emph{p1}) e o mundo parado (taxa \emph{p0}). O capital é o produto
dessas razões: ele não é um teste, é uma **aposta** que se refaz a cada bloco, e sob o mundo parado
o capital é uma martingala --- cada bloco vale um em média, e o produto de médias um tem média um.
A desigualdade de Ville dá então o orçamento de uma vez para **todos** os instantes:

    P(algum instante tem capital >= 1/alfa) <= alfa.

É essa a diferença que este módulo mede: com o limiar, o orçamento se gasta a cada olhada; com o
capital, ele é um só, e vale para sempre. E o preço aparece do outro lado, na latência --- o capital
leva alguns blocos para crescer, e o limiar soa no primeiro bloco que o alcança.

**O defeito que este módulo torna impossível.** Achar que o orçamento declarado para um limiar
sobrevive a ser consultado todo dia. Ele não sobrevive, e o número que o capítulo da troca imprime
--- a raridade do falso alarme --- é de quem olha uma vez.
"""
import numpy as np

ALFA_PADRAO = 0.05
P_NULO_PADRAO = 0.05
P_ALTERNATIVO_PADRAO = 0.10
BLOCO_PADRAO = 60
DIAS_UTEIS = 252

__all__ = ["ALFA_PADRAO", "P_NULO_PADRAO", "P_ALTERNATIVO_PADRAO", "BLOCO_PADRAO", "DIAS_UTEIS",
           "contagens_por_bloco", "razao", "capital", "primeiro_cruzamento", "orcamento_de_ville"]


def contagens_por_bloco(violacoes, bloco: int = BLOCO_PADRAO) -> np.ndarray:
    """As violações somadas em blocos que NÃO se sobrepõem.

    A sobreposição é o que o capítulo usa para ler o pior bloco, e é ela que estraga o produto: os
    blocos precisam ser independentes para o capital ser martingala. O resto da série é descartado,
    e o descarte é declarado porque ele encurta a conta.
    """
    v = np.asarray(violacoes, dtype=float).ravel()
    b = int(bloco)
    if b < 1:
        raise ValueError("o bloco precisa de ao menos um dia")
    quantos = v.size // b
    if quantos < 1:
        raise ValueError("a série não tem um bloco inteiro: %d dias para blocos de %d" % (v.size, b))
    return v[:quantos * b].reshape(quantos, b).sum(axis=1)


def razao(contagens, bloco: int = BLOCO_PADRAO, p_nulo: float = P_NULO_PADRAO,
          p_alternativo: float = P_ALTERNATIVO_PADRAO) -> np.ndarray:
    """O que cada bloco vale a favor do mundo que mudou, contra o mundo parado.

    O coeficiente binomial cancela: as duas hipóteses são a MESMA contagem com taxas diferentes,
    de modo que a razão é potência de potência e nada mais.
    """
    l = np.asarray(contagens, dtype=float)
    if not 0.0 < float(p_nulo) < 1.0 or not 0.0 < float(p_alternativo) < 1.0:
        raise ValueError("as duas taxas têm de estar entre zero e um")
    if np.any(l < 0) or np.any(l > int(bloco)):
        raise ValueError("contagem fora do bloco")
    return (float(p_alternativo) / float(p_nulo)) ** l * \
           ((1.0 - float(p_alternativo)) / (1.0 - float(p_nulo))) ** (int(bloco) - l)


def capital(contagens, bloco: int = BLOCO_PADRAO, p_nulo: float = P_NULO_PADRAO,
            p_alternativo: float = P_ALTERNATIVO_PADRAO, eixo: int = None) -> np.ndarray:
    """O capital acumulado: o produto das razões, lido em qualquer instante.

    Com o eixo dado, o produto corre ao longo dele e uma matriz de mundos por blocos devolve uma
    matriz de caminhos, um por mundo. Sem ele, o produto é sobre a série achatada.
    """
    return np.cumprod(razao(contagens, bloco, p_nulo, p_alternativo), axis=eixo)


def primeiro_cruzamento(caminho, limiar: float) -> dict:
    """O primeiro índice em que o caminho alcança o limiar, e o valor que ele tinha lá."""
    c = np.asarray(caminho, dtype=float)
    acima = np.where(c >= float(limiar))[0]
    if acima.size == 0:
        return {"cruzou": False, "indice": -1,
                "valor": float(c[-1]) if c.size else float("nan")}
    i = int(acima[0])
    return {"cruzou": True, "indice": i, "valor": float(c[i])}


def orcamento_de_ville(alfa: float = ALFA_PADRAO) -> float:
    """O capital que assina a taxa alfa em qualquer instante: um sobre alfa."""
    if not 0.0 < float(alfa) < 1.0:
        raise ValueError("a taxa tem de estar entre zero e um")
    return 1.0 / float(alfa)
