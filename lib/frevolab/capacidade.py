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
           "estados_reservatorio", "capacidade_por_lag", "capacidade_total",
           "rademacher_do_readout", "fracao_de_separacoes", "cota_em_bits",
           "teto_depois_do_uso"]


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
    rng = np.random.default_rng(semente)
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


def rademacher_do_readout(estados: pd.DataFrame, sortes: int = 200,
                          semente: int = 0) -> dict:
    r"""A complexidade de Rademacher da classe de leituras lineares do estado.

    Por sorteio de sinais: para cada sorteio $\sigma$ de sinais em $\{-1, +1\}$ sobre os dias, a
    complexidade é $\|X^\top \sigma\|_2 / N$ --- o quanto a classe consegue alinhar ruído puro. O
    raio dos dados entra junto, porque é ele que multiplica a complexidade na cota: aqui ele é a
    maior norma de uma linha do estado.
    """
    if int(sortes) < 1:
        raise ValueError("a complexidade precisa de pelo menos um sorteio")
    X = estados.to_numpy(dtype=float)
    n, d = X.shape
    if n < 2 or d < 1:
        raise ValueError("a matriz de estados precisa de dias e de coordenadas")
    rng = np.random.default_rng(int(semente))
    valores = np.empty(int(sortes))
    for i in range(int(sortes)):
        sigma = rng.choice([-1.0, 1.0], size=n)
        valores[i] = float(np.linalg.norm(X.T @ sigma) / n)
    return {"media": float(valores.mean()), "dispersao": float(valores.std(ddof=1)),
            "raio": float(np.max(np.linalg.norm(X, axis=1))),
            "razao": float(np.max(np.linalg.norm(X, axis=1)) / np.sqrt(n)),
            "dias": int(n), "sortes": int(sortes)}


def fracao_de_separacoes(estados: pd.DataFrame, grade_de_dias, sortes: int = 200,
                         semente: int = 0) -> dict:
    r"""A fração das dicotomias sorteadas que o readout encaixa com erro ZERO.

    É a função de crescimento amostrada: para cada número de dias da grade, sorteiam-se rótulos
    $\pm 1$ e verifica-se se a leitura linear os reproduz exatamente. Enquanto os dias não passam
    do posto do estado, todos os rótulos cabem; depois, a fração desaba --- e é essa queda que dá
    ao teto da promessa a contagem, e não o número de parâmetros.
    """
    X = estados.to_numpy(dtype=float)
    if X.shape[0] < 2:
        raise ValueError("a matriz de estados precisa de pelo menos dois dias")
    if int(sortes) < 1:
        raise ValueError("a fracao precisa de pelo menos um sorteio")
    rng = np.random.default_rng(int(semente))
    saida = {}
    for dias in grade_de_dias:
        dias = int(dias)
        if not 1 <= dias <= X.shape[0]:
            raise ValueError("a grade pede dias entre um e o numero de linhas")
        A = X[:dias]
        exatos = 0
        for _ in range(int(sortes)):
            sigma = rng.choice([-1.0, 1.0], size=dias)
            w, _, _, _ = np.linalg.lstsq(A, sigma, rcond=None)
            ajustado = np.sign(A @ w)
            ajustado[ajustado == 0.0] = 1.0
            exatos += int(np.array_equal(ajustado, sigma))
        saida[dias] = exatos / float(sortes)
    return saida


def cota_em_bits(estados: pd.DataFrame, alvo, sigma: float, sigma_prior: float,
                 delta: float = 0.05, fracao_treino: float = 0.5,
                 sortes: int = 100, semente: int = 0) -> dict:
    r"""O orçamento da promessa: erro na amostra mais o preço em BITS da hipótese escolhida.

    O preço é a divergência entre a hipótese e o prior, em bits --- forma fechada para as duas
    gaussianas ---, e o prior dependente da instância (o que já viu a primeira metade) o abaixa.
    O erro na amostra é o da hipótese perturbada (média de Gibbs), e o erro fora é medido.
    """
    if not 0.0 < delta < 1.0:
        raise ValueError("o delta da confianca precisa estar entre zero e um")
    if sigma <= 0.0 or sigma_prior <= 0.0:
        raise ValueError("os desvios do posterior e do prior precisam ser positivos")
    if not 0.0 < fracao_treino < 1.0:
        raise ValueError("a fracao de treino precisa ficar em (0; 1)")
    X = estados.to_numpy(dtype=float)
    y = np.asarray(alvo, dtype=float)
    if y.shape[0] != X.shape[0]:
        raise ValueError("o alvo precisa de uma entrada por dia de estado")
    pos = int(X.shape[0] * fracao_treino)
    if pos < 10 or X.shape[0] - pos < 10:
        raise ValueError("as duas metades precisam de pelo menos dez dias")
    A, B = X[:pos], X[pos:]
    ya, yb = y[:pos], y[pos:]
    w_amostra, _, _, _ = np.linalg.lstsq(A, ya, rcond=None)
    rng = np.random.default_rng(int(semente))
    d = X.shape[1]

    def avaliar(centro, desvio):
        dentro = np.empty(int(sortes))
        fora = np.empty(int(sortes))
        for i in range(int(sortes)):
            wp = centro + desvio * rng.standard_normal(d)
            dentro[i] = float(np.mean(np.sign(A @ wp) != np.sign(ya)))
            fora[i] = float(np.mean(np.sign(B @ wp) != np.sign(yb)))
        return float(np.mean(dentro)), float(np.mean(fora))

    def kl_bits(centro):
        kl = 0.5 * (d * sigma ** 2 / sigma_prior ** 2
                    + float(centro @ centro) / sigma_prior ** 2 - d
                    + 2.0 * d * np.log(sigma_prior / sigma))
        return float(max(kl, 0.0) / np.log(2.0))

    dentro_zero, fora_zero = avaliar(w_amostra, sigma)
    braco_zero = {"prior": "zero", "kl_bits": kl_bits(w_amostra),
                  "erro_dentro": dentro_zero, "erro_fora": fora_zero}
    w_metade, _, _, _ = np.linalg.lstsq(A[: pos // 2], ya[: pos // 2], rcond=None)
    dentro_metade, fora_metade = avaliar(w_amostra, sigma)
    braco_metade = {"prior": "metade", "kl_bits": kl_bits(w_amostra - w_metade),
                    "erro_dentro": dentro_metade, "erro_fora": fora_metade}
    n = pos
    for braco in (braco_zero, braco_metade):
        braco["cota"] = float(braco["erro_dentro"]
                              + np.sqrt((braco["kl_bits"] * np.log(2.0)
                                         + np.log(2.0 / delta)) / (2.0 * n)))
        braco["folga"] = float(braco["cota"] - braco["erro_fora"])
    return {"dias": int(X.shape[0]), "treino": int(n), "dimensao": int(d),
            "zero": braco_zero, "metade": braco_metade}


def teto_depois_do_uso(serie: pd.Series, blocos: int = 6, n: int = 100, raio: float = 0.95,
                       saturacao: bool = False, realocacao: bool = False,
                       lags: int = 20, semente: int = 0) -> dict:
    r"""O teto de capacidade medido numa sonda fresca depois de cada bloco de uso.

    O reservatório é usado em blocos: ao fim de cada um, uma leitura nova mede a capacidade do
    estado --- e, se \emph{realocacao} for verdadeira, as unidades dormentes (as que saturam em
    quase todos os dias) voltam ao sorteio. É assim que se separa a perda que vem do uso da perda
    que vem da saturação: sem saturação não há dormente, e é o contraste que isola a causa.
    """
    if int(blocos) < 2:
        raise ValueError("a medicao do uso precisa de pelo menos dois blocos")
    valores = serie.dropna()
    if valores.size < 200:
        raise ValueError("a serie do uso precisa de pelo menos duzentos dias")
    tamanho = valores.size // int(blocos)
    rng = np.random.default_rng(int(semente))
    W = np.zeros((int(n), int(n)))
    for i in range(int(n)):
        alvos = rng.choice(int(n), size=min(3, int(n)), replace=False)
        W[i, alvos] = rng.normal(0.0, 1.0, size=alvos.size)
    W *= float(raio) / max(float(np.abs(np.linalg.eigvals(W)).max()), 1e-12)
    entrada = rng.normal(0.0, 1.0, size=int(n))
    estado = np.zeros(int(n))
    saida = {"blocos": [], "teto": [], "dormentes": [], "realocacao": bool(realocacao),
             "saturacao": bool(saturacao), "dimensao": int(n), "lags": int(lags)}
    for b in range(int(blocos)):
        trecho = valores.iloc[b * tamanho:(b + 1) * tamanho]
        linhas = np.empty((trecho.size, int(n)))
        for t, r in enumerate(trecho.to_numpy()):
            estado = W @ estado + entrada * float(r)
            if saturacao:
                estado = np.tanh(estado)
            linhas[t] = estado
        aquecimento = max(int(n), 10)
        estados = pd.DataFrame(linhas[aquecimento:], index=trecho.index[aquecimento:])
        perfil = capacidade_por_lag(estados, trecho, lags)
        saida["blocos"].append(b)
        saida["teto"].append(float(capacidade_total(perfil)))
        if saturacao:
            dormentes = float(np.mean(np.abs(estados.to_numpy()) > 0.95, axis=0).mean())
        else:
            dormentes = 0.0
        saida["dormentes"].append(dormentes)
        if realocacao and saturacao:
            saturadas = np.mean(np.abs(estados.to_numpy()) > 0.95, axis=0) > 0.9
            for i in np.flatnonzero(saturadas):
                alvos = rng.choice(int(n), size=min(3, int(n)), replace=False)
                W[i, :] = 0.0
                W[i, alvos] = rng.normal(0.0, 1.0, size=alvos.size)
                estado[i] = 0.0
            W *= float(raio) / max(float(np.abs(np.linalg.eigvals(W)).max()), 1e-12)
    return saida
