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
  tolerância declarada --- a moeda da varredura de janelas;

- \texttt{regua}: as três réguas com que duas leis se comparam --- a variação total em células
  partilhadas, a divergência de Kullback--Leibler com o piso declarado e a de Wasserstein pela
  grade de quantis --- com as duas amarras que limitam até onde as réguas podem discordar
  \cite{gibbs2002choosing};

- \texttt{andar\_da\_lei}: quanto a lei de uma série andou, janela a janela, nas três réguas. O
  orçamento da variação mede o andar do parâmetro; este mede o andar da lei inteira, cauda
  junto --- e é na moeda da lei que a promessa do corte é calibrada.

**O limite declarado (§8.5).** Ajustar uma família a um dado e simular dela não é afirmar que o
mundo é a família: é medir o que a família reproduz e o que ela não reproduz --- e é isso que o
caderno dele tira daqui.
"""
import numpy as np

from .esquecimento import HORIZONTE_PADRAO

LIMITE_DO_COEFICIENTE = 0.999

__all__ = ["LIMITE_DO_COEFICIENTE", "coeficiente_rolante", "orcamento_variacao", "simular",
           "fracao_na_tolerancia", "regua", "andar_da_lei"]


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


def _w1(x: np.ndarray, y: np.ndarray) -> float:
    r"""A régua de Wasserstein em uma dimensão: a integral da diferença absoluta dos quantis.

    A integral dos quantis é feita pela varredura equivalente das funções de repartição ---
    em uma dimensão as duas contas dão o mesmo número, e a varredura é exata nas medidas
    empíricas: entre dois valores consecutivos da amostra reunida, cada repartição é degrau,
    e a área é o degrau da diferença vezes o vão. Com amostras do mesmo tamanho, o resultado
    é a conta fechada da média das diferenças entre ordenados. É conta interna: quem quer a
    régua chama \texttt{regua}.
    """
    reunidos = np.concatenate((x, y))
    ordem = np.argsort(reunidos, kind="mergesort")
    veio_de_x = ordem < x.size
    # a repartição de cada amostra no vão que abre depois de cada ponto da reunião
    fx = np.cumsum(veio_de_x) / float(x.size)
    fy = np.cumsum(~veio_de_x) / float(y.size)
    vazoes = reunidos[ordem]
    return float(np.sum(np.abs(fx[:-1] - fy[:-1]) * np.diff(vazoes)))


def regua(x, y, celulas: int = 20) -> dict:
    r"""Duas amostras lidas nas três réguas: variação total, Kullback--Leibler e Wasserstein.

    A variação total é medida em células partilhadas --- os limites vêm da amostra reunida, de
    modo que as duas leis são lidas na mesma grade --- e vale metade da soma das diferenças
    absolutas de massa por célula. A divergência de Kullback--Leibler é a conta de massa com
    um piso declarado: a célula da segunda amostra entra com o mínimo de uma observação
    (\texttt{1/n}, renormalizada depois), porque célula vazia não assina divergência infinita.
    A de Wasserstein é exata em uma dimensão, pela grade de quantis --- e o quantil é o
    instrumento do capítulo do posto, chamado aqui para o que ele sabe fazer.

    As duas amarras vêm junto, porque são elas que dizem até onde as réguas podem discordar:
    \texttt{razao\_pinsker} é a variação total contra a raiz da metade da divergência, e
    \texttt{razao\_diametro} é a Wasserstein contra o diâmetro do suporte --- a amplitude da
    amostra reunida, declarada --- multiplicado pela variação total. Nas leis verdadeiras as
    duas razões valem no máximo um \cite{gibbs2002choosing}; nas estimadas elas podem passar,
    e o que passou é o fumo da célula e do piso, que o caderno declara.
    """
    a = np.asarray(x, dtype=float)
    b = np.asarray(y, dtype=float)
    if a.ndim != 1 or b.ndim != 1 or a.size < 2 or b.size < 2:
        raise ValueError("a régua quer duas amostras de dias, com pelo menos dois dias cada")
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):
        raise ValueError("a régua não lê dia sem valor: preencha ou corte antes")
    celulas = int(celulas)
    if celulas < 2:
        raise ValueError("a régua precisa de pelo menos duas células")
    reunida = np.concatenate((a, b))
    minimo, maximo = float(reunida.min()), float(reunida.max())
    if not maximo > minimo:
        raise ValueError("a régua quer amostras com variação: amostra parada não tem lei a ler")
    arestas = np.linspace(minimo, maximo, celulas + 1)
    contagens_a, _ = np.histogram(a, bins=arestas)
    contagens_b, _ = np.histogram(b, bins=arestas)
    p = contagens_a / float(a.size)
    # o piso da segunda amostra: uma observação por célula vazia, renormalizada --- o infinito
    # da célula vazia é artefato de grade, não de lei
    q = np.maximum(contagens_b / float(b.size), 1.0 / float(b.size))
    q = q / q.sum()
    tv = 0.5 * float(np.abs(p - q).sum())
    kl = float(np.sum(p[p > 0.0] * np.log(p[p > 0.0] / q[p > 0.0])))
    w1 = _w1(a, b)
    diametro = maximo - minimo
    return {
        "tv": tv,
        "kl": kl,
        "wasserstein": w1,
        "razao_pinsker": float(tv / np.sqrt(kl / 2.0)) if kl > 0.0 else float("nan"),
        "razao_diametro": float(w1 / (diametro * tv)) if tv > 0.0 else float("nan"),
    }


def andar_da_lei(serie, janela: int, celulas: int = 20) -> dict:
    r"""Quanto a lei de uma série andou: a soma dos passos, janela a janela, nas três réguas.

    Cada passo compara a janela que sai com a que chega --- dois pedaços que dividem todos os
    dias menos um, lidos nas células partilhadas do próprio passo --- e o andar é a soma dos
    passos, do primeiro dia em que a janela existe ao último. É o orçamento da variação na
    moeda da lei: o coeficiente rolante mede o andar de um parâmetro; aqui quem anda é a lei
    inteira, e o número muda com a régua que mede. O passo de um dia troca dois pontos em
    \emph{janela}, e é por isso que cada régua tem o seu chão de sorteio --- o caderno mede os
    mundos parados para dizer quanto do andar é lei, e quanto é sorte.
    """
    x = np.asarray(serie, dtype=float)
    if x.ndim != 1:
        raise ValueError("o andar quer uma série, um dia por posição")
    janela = int(janela)
    if janela < 3 or janela >= x.size:
        raise ValueError("a janela do andar vive entre três dias e a série inteira menos um")
    if not np.all(np.isfinite(x)):
        raise ValueError("o andar não lê dia sem valor: preencha ou corte antes")
    tv = kl = w1 = 0.0
    for fim in range(janela, x.size):
        passo = regua(x[fim - janela:fim], x[fim - janela + 1:fim + 1], celulas)
        tv += passo["tv"]
        kl += passo["kl"]
        w1 += passo["wasserstein"]
    return {"tv": tv, "kl": kl, "wasserstein": w1, "passos": int(x.size - janela)}
