r"""As formas que a mudança tem: o banco de provas de qualquer vigia.

A pergunta deste projeto é o que se pode garantir, medir e otimizar quando o mundo não para
de mudar. Medir um vigia sobre o mercado não responde essa pergunta sozinho, porque no
mercado **não se sabe quando o mundo mudou**: a latência precisa de uma data, e a data só
existe em quem pôs a mudança no mundo.

É o que este módulo faz, e nada além disso: devolve séries sintéticas em que a mudança foi
posta de propósito, com forma e data conhecidas. São quatro formas, e elas não são
sinônimos:

1. **a média se desloca** (\texttt{deriva}) — o mundo fica pior todo dia, um pouco de cada
   vez, sem nenhum dia memorável;
2. **a cauda se abre de uma vez** (\texttt{degrau}) — um dia o mundo passa a oscilar o dobro,
   e a partir dali fica assim;
3. **a cauda se aproxima devagar** (\texttt{rampa}) — a oscilação cresce ao longo de meses,
   de modo que nenhum dia isolado é extraordinário;
4. **nada muda** (\texttt{estavel}) — o controle, sem o qual nenhuma das outras três vale:
   todo alarme que ele produz é alarme falso, e é ele que diz quanto o vigia gasta à toa.

**Simulação não vira resultado sobre o mundo** (AGENTS.md §8.5). O que se mede aqui é uma
propriedade do instrumento: quanto tempo ele leva para ver uma mudança de forma e tamanho
declarados. O número que sai daqui não é uma afirmação sobre o mercado.

Toda função recebe o gerador \texttt{rng} por parâmetro e não toca a semente global
(AGENTS.md §8).
"""
import numpy as np

SIGMA_PADRAO = 0.01        # a oscilação diária de um mundo calmo: 1%
FATOR_PADRAO = 2.0         # a mudança dobra a oscilação
QUANDO_PADRAO = 1500       # o dia em que a mudança entra, contado do começo da série
DIAS_DE_RAMPA = 250        # quantos dias a rampa leva para chegar ao fator
PASSO_PADRAO = -0.0005     # o deslocamento diário da média, em unidades de retorno

__all__ = ["SIGMA_PADRAO", "FATOR_PADRAO", "QUANDO_PADRAO", "DIAS_DE_RAMPA",
           "PASSO_PADRAO", "estavel", "degrau", "rampa", "deriva", "dependencia"]


def dependencia(n: int, rng: np.random.Generator, sigma: float = SIGMA_PADRAO,
                rho_antes: float = 0.2, rho_depois: float = 0.8,
                quando: int = QUANDO_PADRAO) -> tuple:
    r"""Duas series em que **só o par** muda: cada margem e identica do comeco ao fim.

    A quarta forma, e a unica que nao aparece em serie nenhuma. As duas pernas saem da mesma lei
    e com o mesmo tamanho; o que muda no dia da mudanca e a correlacao entre elas. Nenhum
    instrumento que leia uma perna por vez tem o que ver --- nao ha nada para ver ---, e e por
    isso que a mudanca precisa de um instrumento que leia as duas ao mesmo tempo.
    """
    _confere(n, quando)
    for rho in (rho_antes, rho_depois):
        if not -1.0 < rho < 1.0:
            raise ValueError("as correlacoes precisam estar entre -1 e 1")
    z = rng.normal(0.0, 1.0, (n, 2))
    rho = np.where(np.arange(n) < quando, rho_antes, rho_depois)
    z[:, 1] = rho * z[:, 0] + np.sqrt(1.0 - rho * rho) * z[:, 1]
    return sigma * z[:, 0], sigma * z[:, 1]


def _confere(n: int, quando: int) -> None:
    if n < 3:
        raise ValueError("a serie precisa de pelo menos tres dias")
    if not 1 <= quando < n:
        raise ValueError("a mudanca precisa cair dentro da serie (1 <= quando < %d)" % n)


def estavel(n: int, rng: np.random.Generator, sigma: float = SIGMA_PADRAO) -> np.ndarray:
    r"""Um mundo que nunca muda: retornos independentes, sempre com a mesma lei.

    É o controle de tudo o que este livro mede. Sem ele, um alarme não é nem acerto nem
    erro — é só um dia em que a linha foi cruzada.
    """
    return rng.normal(0.0, sigma, n)


def degrau(n: int, rng: np.random.Generator, sigma: float = SIGMA_PADRAO,
           fator: float = FATOR_PADRAO, quando: int = QUANDO_PADRAO) -> np.ndarray:
    r"""A cauda se abre de uma vez: a oscilação passa a \emph{fator} vezes a antiga.

    O dia da mudança é o primeiro dia já mudado, e é essa convenção que dá sentido à
    latência medida depois: um alarme no próprio dia da mudança tem latência zero.
    """
    _confere(n, quando)
    if fator <= 0:
        raise ValueError("o fator precisa ser positivo")
    serie = rng.normal(0.0, sigma, n)
    serie[quando:] *= fator
    return serie


def rampa(n: int, rng: np.random.Generator, sigma: float = SIGMA_PADRAO,
          fator: float = FATOR_PADRAO, quando: int = QUANDO_PADRAO,
          dias: int = DIAS_DE_RAMPA) -> np.ndarray:
    r"""A cauda se aproxima devagar: a oscilação cresce até \emph{fator} ao longo de dias.

    A diferença para o degrau não é de tamanho, é de forma: aqui nenhum dia isolado é
    extraordinário, e é isso que separa um vigia que olha o dia de um vigia que olha o
    trecho.
    """
    _confere(n, quando)
    if fator <= 0:
        raise ValueError("o fator precisa ser positivo")
    if dias < 2:
        raise ValueError("a rampa precisa de pelo menos dois dias")
    serie = rng.normal(0.0, sigma, n)
    fim = min(quando + dias, n)
    serie[quando:fim] *= np.linspace(1.0, fator, fim - quando)
    serie[fim:] *= fator
    return serie


def deriva(n: int, rng: np.random.Generator, sigma: float = SIGMA_PADRAO,
           passo: float = PASSO_PADRAO, quando: int = QUANDO_PADRAO) -> np.ndarray:
    r"""A média se desloca: a partir do dia da mudança, todo dia carrega \emph{passo} a mais.

    É a mudança mais comum das séries de verdade e a mais difícil de ver: nenhum dia é
    grande, o mundo só deixa de ser simétrico. A oscilação continua exatamente a mesma, o
    que faz dela o caso em que um vigia de cauda não tem o que olhar.
    """
    _confere(n, quando)
    serie = rng.normal(0.0, sigma, n)
    serie[quando:] += passo
    return serie
