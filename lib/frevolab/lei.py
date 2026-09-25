r"""A lei que anda: a família localmente estacionária e o orçamento da sua variação.

A porta que o capítulo de ver mundos deixou aberta tem nome na literatura: processos
\textbf{localmente estacionários} --- séries cuja lei muda, mas devagar o bastante para que cada
pedaço pareça estacionário \cite{dahlhaus1997estimation,dahlhaus2012locally}. Este módulo traz o
mínimo declarado para atravessar essa porta:

- \texttt{coeficiente\_rolante}: a curva do coeficiente auto-regressivo de ordem um, janela a
  janela, pela autocorrelação dentro da janela (Yule-Walker, o estimador mais simples que existe
  --- declarado simples de propósito);

- \texttt{orcamento\_variacao}: quanto a lei andou --- a soma dos passos absolutos da curva. É a
  versão da casa da medida de variação que orça o movimento de parâmetros \cite{chen2018stationary}:
  uma moeda para dizer \emph{quanto} a lei anda em cada mercado, e não apenas que ela anda;

- \texttt{simular}: mundos da família --- o retorno de hoje puxado pelo de ontem com o coeficiente
  de hoje, e o resto sorteio na escala de hoje, que entra fixa ou como curva (a lei que anda da
  escala, com os primeiros dias sem valor recebendo o primeiro que existe). O coeficiente é cortado
  em novecentos e nove milésimos: estacionário por pedaço, que mundo que explode não é lei que
  anda, é lei que acabou (regra declarada). O sorteio é gaussiano; com \texttt{cauda} declarada, é
  um \emph{t} de Student padronizado --- a mesma escala, a cauda mais pesada;

- \texttt{fracao\_na\_tolerancia}: a fração dos dias em que o erro da estimativa cabe na
  tolerância declarada --- a moeda da varredura de janelas.

**O limite declarado (§8.5).** Ajustar uma família a um dado e simular dela não é afirmar que o
mundo é a família: é medir o que a família reproduz e o que ela não reproduz --- e é isso que o
caderno dele tira daqui.
"""
import numpy as np

from .esquecimento import HORIZONTE_PADRAO

LIMITE_DO_COEFICIENTE = 0.999

__all__ = ["LIMITE_DO_COEFICIENTE", "coeficiente_rolante", "orcamento_variacao", "simular",
           "fracao_na_tolerancia"]


def coeficiente_rolante(retornos: np.ndarray, janela: int) -> np.ndarray:
    r"""A curva do coeficiente AR(1), uma janela por vez, do primeiro dia em que ela existe.

    Cada janela entrega a autocorrelação de defasagem um dos seus dias --- o Yule-Walker de ordem
    um, com a média da janela tirada antes. O dia a que a curva pertence é o último da janela; os
    primeiros \texttt{janela - 1} dias ficam sem valor, porque sem janela não há lei.
    """
    x = np.asarray(retornos, dtype=float)
    if x.ndim != 1 or x.size < 2:
        raise ValueError("a curva quer uma série de retornos, um dia por posição")
    janela = int(janela)
    if janela < 3 or janela > x.size:
        raise ValueError("a janela da curva vive entre três dias e a série inteira")
    curva = np.full(x.size, np.nan)
    for fim in range(janela, x.size + 1):
        trecho = x[fim - janela:fim]
        centro = trecho - trecho.mean()
        denominador = float(np.sum(centro * centro))
        if denominador <= 0.0:
            raise ValueError("uma janela inteira parada não tem lei a medir")
        curva[fim - 1] = float(np.sum(centro[1:] * centro[:-1]) / denominador)
    return curva


def orcamento_variacao(curva: np.ndarray) -> float:
    r"""Quanto a lei andou: a soma dos passos absolutos da curva, do primeiro dia com valor ao último.

    Curva parada, orçamento zero --- e é esse o chão contra o qual o andar de cada mercado se
    declara. Os dias sem valor do começo não entram: não são calma, são janela que ainda não existe.
    """
    c = np.asarray(curva, dtype=float)
    validos = c[np.isfinite(c)]
    if validos.size < 2:
        return 0.0
    return float(np.sum(np.abs(np.diff(validos))))


def simular(coeficientes: np.ndarray, sigma, rng: np.random.Generator,
            cauda: float = None) -> np.ndarray:
    r"""Um mundo da família: o de hoje puxado pelo de ontem com a lei de hoje, na escala de hoje.

    A curva entra com o comprimento do mundo que se quer; os dias sem valor do começo recebem o
    primeiro valor que existe (declaração: antes da primeira janela, a lei é a primeira medida). O
    coeficiente é cortado em módulo no limite declarado. A escala entra fixa ou como curva do mesmo
    comprimento --- a lei que anda da escala, com a mesma regra de preencher o começo. O sorteio é
    gaussiano; com \texttt{cauda} declarada (graus de liberdade, maiores que dois), é um \emph{t}
    de Student padronizado para variância um.
    """
    a = np.asarray(coeficientes, dtype=float).copy()
    if a.ndim != 1 or a.size < 3:
        raise ValueError("a simulação quer a curva com o comprimento do mundo")
    escala = np.full(a.size, float(sigma)) if np.isscalar(sigma) else np.asarray(sigma, dtype=float).copy()
    if escala.shape != a.shape:
        raise ValueError("a curva de escala tem de ter o comprimento do mundo")
    if np.any(~np.isfinite(escala)) and np.isscalar(sigma):
        raise ValueError("a escala não pode ter dias sem valor")
    if not np.isscalar(sigma):
        validos_s = np.flatnonzero(np.isfinite(escala))
        if validos_s.size == 0:
            raise ValueError("a curva de escala toda está sem valor")
        escala[:validos_s[0]] = escala[validos_s[0]]
    if np.any(escala <= 0.0) or not np.all(np.isfinite(escala)):
        raise ValueError("a escala de cada dia tem de ser finita e positiva")
    if cauda is not None and cauda <= 2.0:
        raise ValueError("a cauda do t precisa de graus demais: variância finita")
    validos = np.flatnonzero(np.isfinite(a))
    if validos.size == 0:
        raise ValueError("a curva toda está sem valor: não há lei para simular")
    a[:validos[0]] = a[validos[0]]
    a = np.clip(a, -LIMITE_DO_COEFICIENTE, LIMITE_DO_COEFICIENTE)
    if cauda is None:
        z = rng.normal(0.0, 1.0, a.size)
    else:
        z = rng.standard_t(float(cauda), a.size) / np.sqrt(float(cauda) / (float(cauda) - 2.0))
    r = np.empty(a.size)
    r[0] = escala[0] * z[0]
    for t in range(1, a.size):
        r[t] = a[t] * r[t - 1] + escala[t] * z[t]
    return r


def fracao_na_tolerancia(estimativa: np.ndarray, verdade: np.ndarray, tolerancia: float,
                         inicio: int = 0, horizonte: int = HORIZONTE_PADRAO) -> float:
    r"""A fração dos dias em que o erro relativo da estimativa cabe na tolerância declarada.

    É a moeda da varredura: o erro médio esconde quantos dias estavam bons e quantos estavam
    quebrados, e a fração mostra os dois. A verdade entra como série, pelo mesmo motivo do erro
    médio: num mundo que muda, a verdade de hoje não é a de ontem.
    """
    e = np.asarray(estimativa, dtype=float)
    v = np.asarray(verdade, dtype=float)
    if e.shape != v.shape:
        raise ValueError("a estimativa e a verdade precisam ter o mesmo comprimento")
    if tolerancia <= 0.0:
        raise ValueError("a tolerância tem de ser positiva")
    if inicio + horizonte > e.size:
        raise ValueError("a avaliação não cabe na série")
    te, tv_ = e[inicio:inicio + horizonte], v[inicio:inicio + horizonte]
    if not np.all(np.isfinite(te)):
        raise ValueError("a estimativa tem dias sem valor na janela avaliada")
    return float(np.mean(np.abs(te - tv_) / tv_ <= tolerancia))
