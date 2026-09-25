"""A capacidade de memória: quantos dias do passado o estado devolve.

O estado de uma memória é um vetor que anda com a série; a pergunta da capacidade é quantos dias
individuais do passado esse vetor consegue devolver por leitura linear. A definição é a da
capacidade de memória de Jaeger: para cada atraso k, a fração da variância do dia t-k que o melhor
readout linear extrai do estado em t --- treinado numa metade e medido fora da amostra, porque
capacidade medida dentro da amostra é ajuste, não memória. O teorema da conservação
(dambre2012information): a soma sobre os atrasos não passa do posto da matriz de controlabilidade,
que não passa da dimensão do estado --- a dinâmica distribui a capacidade, não a cria.
"""
import numpy as np
import pandas as pd

__all__ = ["estados_janela", "estados_exponencial", "estados_acumulada",
           "estados_reservatorio", "capacidade_por_lag", "capacidade_total"]


def estados_janela(serie: pd.Series, n: int) -> pd.DataFrame:
    r"""O estado é o próprio passado: os últimos n dias, verbatim --- a memória do capítulo 29 que
    guarda bloco. A linha t carrega os dias t-1 a t-n."""
    cols = {}
    for k in range(1, n + 1):
        cols["lag_%d" % k] = serie.shift(k)
    return pd.DataFrame(cols, index=serie.index).dropna()


def estados_exponencial(serie: pd.Series, alfa: float) -> pd.DataFrame:
    r"""A memória que o capítulo 14 escolheu: um número só, a média que esquece à taxa alfa. O
    estado é escalar --- e um número devolve no máximo uma direção do passado."""
    if not 0.0 < alfa <= 1.0:
        raise ValueError("a taxa de esquecimento tem de ficar em (0; 1]")
    return pd.DataFrame({"media": serie.ewm(alpha=alfa, adjust=False).mean()},
                        index=serie.index)


def estados_acumulada(serie: pd.Series) -> pd.DataFrame:
    r"""A memória que ninguém escolhe: a média acumulada, com o peso de cada dia em um sobre a
    idade --- o estado é uma direção, e direção nenhuma é dia."""
    return pd.DataFrame({"media": serie.expanding().mean()}, index=serie.index)


def estados_reservatorio(serie: pd.Series, n: int = 100, raio: float = 0.95,
                         vizinhos: int = 3, semente: int = 0) -> pd.DataFrame:
    r"""O reservatório linear: estado de n números, matriz esparsa de vizinhos por linha com raio
    espectral normalizado abaixo de um --- a condição de estado de eco (jaeger2001echo), a família
    de maass2002real sem estado estável e o teorema de aproximação de hart2020embedding."""
    if not 0.0 < raio < 1.0:
        raise ValueError("o raio espectral tem de ficar em (0; 1) para haver estado de eco")
    rng = np.random.default_rng(seemente) if False else np.random.default_rng(semente)
    W = np.zeros((n, n))
    for i in range(n):
        alvos = rng.choice(n, size=min(vizinhos, n), replace=False)
        W[i, alvos] = rng.normal(0.0, 1.0, size=alvos.size)
    W *= raio / max(np.abs(np.linalg.eigvals(W)).max(), 1e-12)
    entrada = rng.normal(0.0, 1.0, size=n)
    valores = serie.to_numpy()
    estado = np.zeros(n)
    colunas = np.empty((valores.size, n))
    for t, r in enumerate(valores):
        estado = W @ estado + entrada * r
        colunas[t] = estado
    aquecimento = max(n, 10)
    return pd.DataFrame(colunas[aquecimento:], index=serie.index[aquecimento:])


def capacidade_por_lag(estados: pd.DataFrame, serie: pd.Series, lags: int,
                       fracao_treino: float = 0.5) -> dict:
    r"""A capacidade por atraso, fora da amostra: para cada k, o readout linear que melhor recupera
    o dia t-k do estado em t, ajustado na primeira metade --- e a capacidade é a correlação ao
    quadrado entre o que o readout devolve e o dia, medida na segunda metade. Não-negativa por
    construção, com o zero de chão: estado que não carrega o dia não tem capacidade negativa, tem
    nenhuma. A solução vem por decomposição QR, porque o atraso muda só o alvo."""
    if not 0.0 < fracao_treino < 1.0:
        raise ValueError("a fração de treino tem de ficar em (0; 1)")
    from scipy.linalg import solve_triangular
    comuns = estados.index.intersection(serie.index)
    E = estados.loc[comuns]
    r = serie.loc[comuns].to_numpy()
    X = E.to_numpy()
    pos = int(X.shape[0] * fracao_treino)
    perfil = {}
    for k in range(1, lags + 1):
        if pos - k < 20 or X.shape[0] - pos < 20:
            break
        A = X[k:pos]
        Q, R = np.linalg.qr(A)
        w = solve_triangular(R, Q.T @ r[:pos - k])
        y = r[pos - k:X.shape[0] - k]
        pred = X[pos:] @ w
        sy, sp = float(np.std(y)), float(np.std(pred))
        if sy <= 0 or sp <= 0:
            perfil[k] = 0.0
            continue
        cov = float(np.mean((y - y.mean()) * (pred - pred.mean())))
        perfil[k] = float((cov / (sy * sp)) ** 2)
    return perfil

def capacidade_total(perfil: dict) -> float:
    r"""A conservação em um número: a soma das capacidades por atraso --- que o teorema limita ao
    posto da matriz de controlabilidade, no máximo a dimensão do estado."""
    valores = [v for v in perfil.values() if v == v]
    return float(sum(valores)) if valores else float("nan")
