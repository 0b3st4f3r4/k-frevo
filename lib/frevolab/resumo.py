r"""Resumo: o que se guarda do dia, quando não se guarda o dia.

O corte do capítulo 3 é contado com **um número por dia** --- seis mil setecentos e dezoito deles
---, e o pior bloco de sessenta dias é a leitura que destrava as voltas seguintes. Guardar cem
números no lugar de seis mil setecentos e dezoito é o gesto mais natural do mundo, e ele tem preço
tabelado.

O objeto que este módulo mede é o **segundo momento do fluxo**: a soma dos quadrados dos
incrementos, que é a energia do caminho. O esboço de Alon, Matias e Szegedy guarda \emph{k}
contadores e soma cada item a todos eles com um sinal sorteado,

    c_j = soma_i s_ij x_i,   com s_ij em {+1, -1},

e estima a energia pela média dos quadrados, \emph{(1/k) soma_j c_j^2}. O estimador é exato em
esperança --- dois sinais distintos têm produto de esperança zero, e é essa a conta inteira --- e a
variância relativa é \emph{2/k}, de modo que a precisão \emph{eps} custa \emph{k = 2/eps^2}
contadores. Cem compram catorze por cento; dez mil compram um e quatro décimos; e nenhum método
compra mais com menos.

**O defeito que este módulo torna impossível.** Achar que o resumo responde à pergunta do capítulo.
O esboço responde ao segundo momento e a mais nada: ele não vê a ordem dos dias, e a pergunta do
livro --- o pior bloco de sessenta dias, a contagem de explicações que cabem --- é uma pergunta
sobre a ordem. O que a compressão custa não é só o erro: é a pergunta.
"""
from statistics import NormalDist

import numpy as np

CONTADORES_PADRAO = (25, 100, 400, 1600, 10000)
MUNDOS_PADRAO = 40
BLOCO_SORTEIO_PADRAO = 512

__all__ = ["CONTADORES_PADRAO", "MUNDOS_PADRAO", "energia", "contadores_para", "esboco",
           "erro_relativo", "varredura", "corte_normal", "previsao"]


def energia(valores) -> float:
    """A soma dos quadrados, exata. É o que o esboço tenta comprar mais barato."""
    v = np.asarray(valores, dtype=float).ravel()
    return float(np.dot(v, v))


def contadores_para(erro: float) -> int:
    """Quantos contadores compram erro relativo \emph{erro}: o teto de 2/erro^2."""
    if not 0.0 < float(erro) < 1.0:
        raise ValueError("o erro relativo pedido tem de estar entre zero e um: %r" % (erro,))
    return int(np.ceil(2.0 / float(erro) ** 2))


def previsao(contadores: int) -> float:
    """O erro relativo que a teoria promete com k contadores: a raiz de 2/k."""
    if int(contadores) < 1:
        raise ValueError("o esboço precisa de ao menos um contador")
    return float(np.sqrt(2.0 / int(contadores)))


def esboco(valores, contadores: int, rng: np.random.Generator,
           bloco: int = BLOCO_SORTEIO_PADRAO) -> dict:
    """O esboço de segundo momento: k contadores com sinal sorteado, e a estimativa da energia.

    Os sinais saem em blocos, e não numa matriz de k por n, porque a matriz inteira não caberia
    para k = dez mil numa série de seis mil e setecentos dias. O bloco é do sorteio, não do
    estimador: cada contador continua independente dos outros.
    """
    v = np.asarray(valores, dtype=float).ravel()
    k = int(contadores)
    if k < 1:
        raise ValueError("o esboço precisa de ao menos um contador")
    if v.size == 0:
        raise ValueError("o esboço precisa de um fluxo com ao menos um item")
    contagens = np.empty(k)
    for inicio in range(0, k, int(bloco)):
        fim = min(inicio + int(bloco), k)
        sinais = rng.integers(0, 2, size=(fim - inicio, v.size)) * 2.0 - 1.0
        contagens[inicio:fim] = sinais @ v
    exato = energia(v)
    estimativa = float(np.mean(contagens * contagens))
    return {"estimativa": estimativa, "exato": exato, "contadores": k,
            "erro": erro_relativo(estimativa, exato)}


def erro_relativo(estimativa: float, exato: float) -> float:
    """O erro relativo de uma estimativa contra o valor exato."""
    if exato == 0.0:
        raise ValueError("o erro relativo de um exato nulo não é definido")
    return abs(float(estimativa) - float(exato)) / abs(float(exato))


def varredura(valores, contadores: int, mundos: int = MUNDOS_PADRAO,
              rng: np.random.Generator = None) -> dict:
    """O mesmo fluxo, um sorteio de sinais por mundo: a distribuição do erro, medida.

    O mundo é o sorteio do esboço, e não o dado: a mesma série, com outros sinais, dá outra
    estimativa. É isso que separa o erro do estimador do erro do mundo.
    """
    if rng is None:
        rng = np.random.default_rng(20260924)
    erros = np.empty(int(mundos))
    for m in range(int(mundos)):
        erros[m] = esboco(valores, contadores, rng)["erro"]
    return {"contadores": int(contadores), "mundos": int(mundos),
            "erro_medio": float(erros.mean()), "erro_mediano": float(np.median(erros)),
            "erro_p95": float(np.quantile(erros, 0.95)), "previsto": previsao(contadores),
            "erros": erros}


def corte_normal(energia_estimada: float, n: int, cauda: float) -> float:
    """O corte que uma leitura gaussiana compra de um segundo momento estimado.

    É a ponte entre o resumo e a decisão: o alarme precisa de um quantil, o esboço entrega uma
    energia, e a ponte entre os dois supõe simetria. O capítulo mede o que essa suposição cobra.
    """
    if float(energia_estimada) <= 0.0:
        raise ValueError("a energia estimada tem de ser positiva")
    if not 0.0 < float(cauda) < 1.0:
        raise ValueError("a cauda tem de estar entre zero e um")
    sigma = float(np.sqrt(float(energia_estimada) / int(n)))
    return float(NormalDist().inv_cdf(float(cauda)) * sigma)
