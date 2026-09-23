r"""Estabilidade: a estatística que estima é a mesma que anuncia a quebra?

Família A/B, a volta 2. A pergunta que este módulo serve é uma só, e ela é a do fecho do
capítulo 4: a estatística que responde "que conjunto ainda vale" e a que responde "em que
instante ele deixou de valer" são a mesma, lida ao contrário?

O instrumento é pequeno: a **correlação de posto** entre um sinal que olha para trás e o que
acontece depois, e o **perfil por décimo**, que mostra a forma da relação em vez de resumi-la
num número. O posto é escolha, e não preguiça: nada aqui supõe que a relação seja linear, e a
cauda é justamente onde ela deixa de ser.

**O defeito que este módulo torna impossível.** Ler o poder de um sinal sem o controle de um
mundo em que não há nada a prever. Um corte erguido numa janela e um alvo contado com cortes que
carregam pedaço da mesma janela se sobrepõem, e a sobreposição sozinha produz correlação — no
caderno do capítulo 5, o nível do corte dá +0,414 num mundo sorteado independente, onde não há
nada para anunciar. Quem mede sinal sem medir o chão mede aritmética e chama de descoberta.
"""
import numpy as np
import pandas as pd

__all__ = ["posto", "perfil_por_decimo"]


def posto(sinal, alvo, n_partes: int = 10) -> float:
    r"""A correlação de posto entre o sinal e o alvo, sem supor relação linear."""
    a = np.asarray(sinal, dtype=float)
    b = np.asarray(alvo, dtype=float)
    if a.size != b.size:
        raise ValueError("o sinal e o alvo precisam do mesmo tamanho (%d e %d)" % (a.size, b.size))
    if a.size < 3:
        raise ValueError("precisa de pelo menos tres pontos")
    if n_partes < 2:
        raise ValueError("precisa de pelo menos duas partes")
    if np.all(a == a[0]) or np.all(b == b[0]):
        return float("nan")
    return float(np.corrcoef(pd.Series(a).rank(), pd.Series(b).rank())[0, 1])


def perfil_por_decimo(sinal, alvo, n_partes: int = 10) -> list:
    r"""O alvo médio em cada parte do sinal, da menor para a maior.

    É o que a correlação esconde: um posto alto com perfil plano quer dizer outra coisa que um
    posto médio com perfil que só sobe no fim, e é o perfil que diz qual das duas.
    """
    a = np.asarray(sinal, dtype=float)
    b = np.asarray(alvo, dtype=float)
    if a.size != b.size:
        raise ValueError("o sinal e o alvo precisam do mesmo tamanho")
    if a.size < n_partes:
        raise ValueError("menos pontos que partes: %d para %d" % (a.size, n_partes))
    ordem = np.argsort(a)
    return [float(b[parte].mean()) for parte in np.array_split(ordem, n_partes)]
