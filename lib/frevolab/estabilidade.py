r"""Estabilidade: a estatística que estima é a mesma que anuncia a quebra?

Família A/B, a volta 2. A pergunta que este módulo serve é uma só, e ela é a do fecho do
capítulo 5: a estatística que responde "que conjunto ainda vale" e a que responde "em que
instante ele deixou de valer" são a mesma, lida ao contrário?

O instrumento é pequeno: a **correlação de posto** entre um sinal que olha para trás e o que
acontece depois, e o **perfil por décimo**, que mostra a forma da relação em vez de resumi-la
num número. O posto é escolha, e não preguiça: nada aqui supõe que a relação seja linear, e a
cauda é justamente onde ela deixa de ser.

**O defeito que este módulo torna impossível.** Ler o poder de um sinal sem o controle de um
mundo em que não há nada a prever. Um corte erguido numa janela e um alvo contado com cortes que
carregam pedaço da mesma janela se sobrepõem, e a sobreposição sozinha produz correlação — no
caderno do capítulo 6, o nível do corte dá +0,414 num mundo sorteado independente, onde não há
nada para anunciar. Quem mede sinal sem medir o chão mede aritmética e chama de descoberta.
"""
import numpy as np
import pandas as pd

__all__ = ["janelas", "por_janela", "resumo", "banda_independente", "posto", "perfil_por_decimo"]


def janelas(tamanho: int, pedaco: int, passo: int = None) -> list:
    r"""As fatias da série, do começo ao fim, sem sobreposição por padrão.

    Devolve os índices de cada pedaço. Com 	exttt{passo} menor que 	exttt{pedaco} os pedaços se
    sobrepõem, e a sobreposição é declarada porque ela muda o que a dispersão entre pedaços quer
    dizer: pedaços que compartilham dias não são respostas independentes.
    """
    if pedaco < 1 or tamanho < pedaco:
        raise ValueError("o pedaco precisa caber na serie")
    if passo is None:
        passo = pedaco
    if passo < 1:
        raise ValueError("o passo precisa ser de pelo menos um dia")
    fatias = []
    inicio = 0
    while inicio + pedaco <= tamanho:
        fatias.append(slice(inicio, inicio + pedaco))
        inicio += passo
    return fatias


def por_janela(serie, medidor, pedaco: int, passo: int = None) -> np.ndarray:
    r"""A mesma pergunta respondida em cada pedaço.

    O medidor é o que responde à pergunta --- a entrega do corte, o excesso conjunto, a curtose ---,
    e ele é aplicado a cada fatia. O que sai é a lista das respostas, e não a resposta.
    """
    s = serie if hasattr(serie, "iloc") else np.asarray(serie, dtype=float)
    respostas = [medidor(s[fatia]) for fatia in janelas(len(s), pedaco, passo)]
    if not respostas:
        raise ValueError("nao ha pedaco nenhum para medir")
    return np.array(respostas, dtype=float)


def resumo(valores: np.ndarray, alvo: float = None, banda: float = None) -> dict:
    r"""A dispersão das respostas entre pedaços: o que se reporta em lugar de uma resposta só.

    Devolve o menor, o maior, o desvio entre pedaços e a razão entre o maior e o menor. Quando um
    alvo e uma banda são declarados, devolve também a fração de pedaços que ficam fora da banda ---
    é a conta que diz se a resposta de um pedaço só teria enganado quem a lesse.
    """
    v = np.asarray(valores, dtype=float)
    if v.size == 0:
        raise ValueError("nao ha resposta para resumir")
    saida = {"pedacos": int(v.size), "menor": float(v.min()), "maior": float(v.max()),
             "media": float(v.mean()), "dispersao": float(v.std(ddof=1)) if v.size > 1 else 0.0,
             "razao": float(v.max() / v.min()) if v.min() != 0.0 else float("nan")}
    if alvo is not None and banda is not None:
        saida["fora_da_banda"] = float((np.abs(v - alvo) > banda).mean())
        saida["alvo"] = float(alvo)
        saida["banda"] = float(banda)
    return saida


def banda_independente(taxa: float, dias: int) -> float:
    r"""O desvio que a conta independente prevê para uma taxa medida em emph{dias} dias.

    É a conta de sempre --- emph{raiz de p(1-p)/n} ---, e ela supõe que cada dia é um sorteio
    independente. Onde o mundo tem agrupamento, a dispersão medida entre pedaços é maior do que
    ela, e é essa diferença que o caderno mede.
    """
    if not 0.0 < taxa < 1.0:
        raise ValueError("a taxa precisa estar entre zero e um")
    if dias < 1:
        raise ValueError("os dias precisam ser pelo menos um")
    return float(np.sqrt(taxa * (1.0 - taxa) / dias))


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
