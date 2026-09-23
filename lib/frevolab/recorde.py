r"""O recorde, e o mundo que não foi observado.

O andar começa pela pergunta mais dura de todas: de que serve uma proteção calibrada no que já se
viu, quando o mundo que decide o prejuízo é o que **não** se viu? Este módulo mede o que se pode
dizer sobre esse mundo sem inventá-lo, e o que se pode dizer é uma probabilidade exata.

**A conta.** Se os \emph{n} dias observados e os \emph{m} dias por vir fossem permutáveis --- o
mesmo mundo, sem mudança nenhuma ---, o maior valor do conjunto inteiro estaria em qualquer das
\emph{n + m} posições com a mesma chance, de modo que a probabilidade de que algum dia futuro supere
o recorde de tudo o que já se viu é \emph{m / (n + m)}. Com um ano de histórico e um ano por vir,
isso é meio. A probabilidade de que o **próximo** dia supere o recorde é \emph{1 / (n + 1)}, que é a
mesma estrutura do corte do primeiro capítulo --- e não é coincidência: é a mesma contagem.

**O defeito que este módulo torna impossível.** Dimensionar a proteção pelo pior dia já visto e
tratar esse número como um teto. O pior dia do índice deste livro é \emph{12,765\%} contra
\emph{9,994\%} do segundo pior: quando o recorde cai, ele não cai por pouco.

E o registro do tamanho do recorde também tem conta: num mundo sem mudança o número esperado de
recordes em \emph{n} dias é o harmônico \emph{H(n)}, que cresce como o logaritmo. Quando o mundo
muda, a conta de permutabilidade deixa de valer, e é isso que o caderno mede.
"""
import numpy as np

LADO_PADRAO = "alto"

__all__ = ["LADO_PADRAO", "recordes", "conta", "esperado", "probabilidade", "do_proximo",
           "superacoes", "faltou"]


def recordes(serie: np.ndarray, lado: str = LADO_PADRAO) -> np.ndarray:
    r"""Marca os dias que são o extremo de tudo o que veio antes.

    Com \texttt{lado="alto"}, marca o dia que é o maior já visto; com \texttt{lado="baixo"}, o
    menor. O primeiro dia é sempre um recorde, porque não há antes dele.
    """
    s = np.asarray(serie, dtype=float)
    if s.size < 1:
        raise ValueError("a serie precisa de pelo menos um dia")
    if lado not in ("alto", "baixo"):
        raise ValueError("o lado do recorde e 'alto' ou 'baixo'")
    saida = np.zeros(s.size, dtype=bool)
    extremo = -np.inf if lado == "alto" else np.inf
    for i, x in enumerate(s):
        if (x > extremo) if lado == "alto" else (x < extremo):
            saida[i] = True
            extremo = x
    return saida


def conta(serie: np.ndarray, lado: str = LADO_PADRAO) -> int:
    r"""Quantos recordes a série fez."""
    return int(recordes(serie, lado).sum())


def esperado(n: int) -> float:
    r"""O número esperado de recordes em \emph{n} dias de um mundo que não muda: o harmônico.

    Sai da soma das probabilidades de cada dia ser recorde, que são \emph{1/k} --- e é por isso que
    o número cresce como o logaritmo, e não como a raiz.
    """
    if n < 1:
        raise ValueError("o numero de dias precisa ser pelo menos um")
    return float(np.sum(1.0 / np.arange(1, n + 1)))


def probabilidade(n: int, m: int) -> float:
    r"""A chance de algum dia dos próximos \emph{m} superar o recorde dos \emph{n} já vistos.

    Vale \emph{m / (n + m)} sob permutabilidade, e a soma dela com a probabilidade contrária é um:
    o maior valor do conjunto está de um lado ou do outro.
    """
    if n < 1 or m < 1:
        raise ValueError("os dois lados precisam de pelo menos um dia")
    return float(m) / float(n + m)


def do_proximo(n: int) -> float:
    r"""A chance de o dia seguinte superar o recorde de \emph{n} dias: um sobre \emph{n + 1}."""
    return probabilidade(n, 1)


def superacoes(serie: np.ndarray, nivel: float) -> float:
    r"""A fração dos dias que passam por cima de um nível dado.

    É a medida do mundo que faltou: um nível calibrado no passado, e os dias que o país do futuro
    passou por cima dele.
    """
    s = np.asarray(serie, dtype=float)
    if s.size < 1:
        raise ValueError("a serie precisa de pelo menos um dia")
    return float((s > nivel).mean())


def faltou(passado: np.ndarray, futuro: np.ndarray, lado: str = LADO_PADRAO) -> dict:
    r"""O que o futuro fez contra o extremo do passado.

    Devolve o extremo do passado, o extremo do futuro, a fração de dias do futuro que passaram por
    cima do extremo do passado e a razão entre os dois extremos. É o número que uma proteção
    calibrada no passado teria deixado passar.
    """
    p = np.asarray(passado, dtype=float)
    f = np.asarray(futuro, dtype=float)
    if p.size < 1 or f.size < 1:
        raise ValueError("os dois lados precisam de pelo menos um dia")
    if lado == "alto":
        extremo_p, extremo_f = float(p.max()), float(f.max())
        fração = float((f > extremo_p).mean())
    elif lado == "baixo":
        extremo_p, extremo_f = float(p.min()), float(f.min())
        fração = float((f < extremo_p).mean())
    else:
        raise ValueError("o lado do recorde e 'alto' ou 'baixo'")
    return {"extremo_passado": extremo_p, "extremo_futuro": extremo_f, "fracao": fração,
            "razao": extremo_f / extremo_p if extremo_p else float("nan")}
