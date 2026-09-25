r"""As duas famílias que podem ter gerado a cauda.

O livro mediu a cauda dos mercados várias vezes --- o recorde que não cai por pouco, o dia em que
as pernas rompem juntas --- sem nunca perguntar de onde ela vem. Este módulo traz duas respostas
possíveis, declaradas como geradores, para o caderno medir qual delas reproduz o que o dado faz:

- a família que \textbf{sorteia}: dias independentes de uma lei de cauda pesada (o \emph{t} de
  Student), onde o pior dia é um sorteio azarado e o seguinte é outro, sem memória entre eles;

- a família que \textbf{se reproduz}: cada dia ruim gera dias ruins --- ramificação crítica em
  ambiente aleatório, a forma que a literatura da cauda propõe para o contagio de eventos ---,
  onde os dias grandes chegam em cacho porque um gerou o outro.

**A regra de calibração.** Cada mundo sai padronizado em unidades de desvio-padrão; o caderno
multiplica pela escala do mercado que estiver julgando. As assinaturas medidas --- a razão entre
o pior e o segundo pior dia, o número de recordes --- não dependem da escala, e é por isso que a
calibração pode se dar por ela.

**O limite declarado.** Gerador é família, não mundo: o que estes geradores medem é qual das duas
histórias reproduce as assinaturas, não qual delas é verdadeira --- isto é um pedaço do que o
fecho do livro guarda para si.
"""
import numpy as np

NU_PADRAO = 3.0
PHI_PADRAO = 0.0
TAU_PADRAO = 0.5

__all__ = ["NU_PADRAO", "PHI_PADRAO", "TAU_PADRAO", "independente", "critica", "extremos"]


def independente(n: int, rng: np.random.Generator, nu: float = NU_PADRAO) -> np.ndarray:
    r"""A família que sorteia: \emph{n} dias independentes de cauda pesada.

    O sorteio é o \emph{t} de Student com \texttt{nu} graus de liberdade, padronizado para
    variância um --- o que exige \texttt{nu > 2}. Com os graus declarados no padrão, a cauda decai
    como a quarta potência do retorno: pior dia grande, segundo pior do mesmo sorteio, e nenhum
    dia sabendo do outro.
    """
    if int(n) < 3:
        raise ValueError("a familia independente precisa de pelo menos tres dias")
    if nu <= 2.0:
        raise ValueError("o t de Student precisa de variância finita: nu maior que dois")
    z = rng.standard_t(nu, size=int(n))
    return z / np.sqrt(nu / (nu - 2.0))


def critica(n: int, rng: np.random.Generator, phi: float = PHI_PADRAO,
            tau: float = TAU_PADRAO) -> np.ndarray:
    r"""A família que se reproduz: ramificação crítica em ambiente aleatório.

    A população de dias ruins segue $Z_{t+1} = \mathrm{Poisson}(Z_t\,e_t)$, com o ambiente
    $e_t = \exp(x_t)$: $x_t$ é um processo auto-regressivo de ordem um, estacionário, com
    persistência \texttt{phi}, desvio-padrão estacionário \texttt{tau} e média $-\tau^2/2$ ---
    de modo que $\mathbb{E}[e_t] = 1$ e a ramificação é crítica em média. O padrão é o ambiente
    \emph{sem memória entre os dias} (\texttt{phi} nulo), o cenário clássico da ramificação
    crítica em ambiente aleatório: o logaritmo da população caminha com deriva para baixo e teto
    estocástico --- a cauda pesada vem daí. Persistência positiva faz o ambiente ficar tempo demais
    do lado bom e a população explode, e é por isso que ela não é o padrão. Extinta a população,
    um imigrante repõe um dia ruim no próprio dia: o processo não morre, e a regra está declarada.

    O retorno do dia é a população inteira, com sinal trocado --- dia ruim é dia de população alta
    ---, padronizado em unidades de desvio-padrão da própria amostra.
    """
    if int(n) < 3:
        raise ValueError("a familia que se reproduz precisa de pelo menos tres dias")
    if not 0.0 <= phi < 1.0:
        raise ValueError("a persistência do ambiente vive entre zero e um")
    if tau <= 0.0:
        raise ValueError("o desvio do ambiente tem de ser positivo")
    n = int(n)
    media = -0.5 * tau * tau
    ruido = tau * np.sqrt(1.0 - phi * phi)
    x = np.empty(n)
    z = np.empty(n)
    x[0] = media + rng.normal(0.0, ruido)
    z[0] = 1.0
    for t in range(1, n):
        x[t] = media + phi * (x[t - 1] - media) + rng.normal(0.0, ruido)
        filhos = rng.poisson(z[t - 1] * float(np.exp(x[t])))
        z[t] = 1.0 if filhos == 0 else float(filhos)
    if np.any(z < 0.0) or not np.all(np.isfinite(z)):
        raise AssertionError("a população não pode ser negativa")
    return -z / z.std()


def extremos(serie: np.ndarray) -> dict:
    r"""O pior dia, o segundo pior e a razão entre eles, do lado da queda.

    A razão é a assinatura que separa as histórias da cauda: se o pior dia é um sorteio solto, a
    razão tem a distribuição de uma lei sem memória; se o pior dia veio de um cacho, o segundo
    pior conta a mesma história outra vez. Exige um segundo pior que seja queda de verdade.
    """
    s = np.asarray(serie, dtype=float)
    if s.size < 2:
        raise ValueError("extremos exigem pelo menos dois dias")
    dois_piores = np.sort(s)[:2]
    pior, segundo = -dois_piores[0], -dois_piores[1]
    if segundo <= 0.0:
        raise ValueError("o segundo pior dia tem de ser uma queda")
    return {"pior": float(pior), "segundo": float(segundo), "razao": float(pior / segundo)}
