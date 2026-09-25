r"""A profundidade do corte como eixo: a taxa com que a junta cai.

O capítulo da queda conjunta mediu uma razão num corte só --- o dado junto contra o que a
independência prevê --- e a proposição do teto disse por onde a conta não passa. Mas quem compra
proteção no corte raso precisa da mesma conta no corte fundo, e um corte só não diz a TAXA com que
a probabilidade conjunta cai quando o corte afunda. Este módulo põe a profundidade no eixo: a razão
em várias profundidades, o expoente lido direto do dado como a inclinação da reta em log-log, e o
intervalo por bootstrap de blocos --- o mesmo bloco e o mesmo número de repetições do capítulo do
orçamento, reamostrando os dias comuns inteiros para que a dependência viaje junto.

**Os controles são estrutura, não ajuste.** A gaussiana e a t entram com a MESMA correlação de posto
do par, para que toda a diferença entre as inclinações seja dependência e nada mais. A gaussiana
tem a inclinação assintótica que a lei da junta anuncia \cite{savage1962mills,hashorva2003multivariate};
a t, com qualquer grau de liberdade, caminha com a margem \cite{taleb2020tail,taleb2018much}. E o
controle negativo é o de sempre: pernas independentes, onde a razão tem de dar um em toda
profundidade --- se o expoente aparecer ali, o defeito é do instrumento.
"""
import numpy as np
import pandas as pd
from scipy import stats as _stats

from . import dependencia, promessa

JANELA_PADRAO = 252
BLOCO_PADRAO = 60
REPETICOES_PADRAO = 200
PROFUNDIDADES_PADRAO = (0.05, 0.02, 0.01, 0.005, 0.0025)

__all__ = ["PROFUNDIDADES_PADRAO", "razoes", "expoente", "intervalo",
           "controle_gaussiano", "controle_t"]


def razoes(retornos_a: pd.Series, retornos_b: pd.Series,
           cortes=PROFUNDIDADES_PADRAO, janela: int = JANELA_PADRAO) -> dict:
    r"""A razão do conjunto contra a independência, em cada profundidade do corte.

    O instrumento é o do capítulo da queda conjunta, sem peça nova: cada perna rompe o próprio
    corte de janela e posto, e o que se conta são os dias em que as duas rompem --- contra o
    produto das frequências realizadas. A profundidade entra pelo posto que a cauda escolhe.
    """
    comuns = retornos_a.index.intersection(retornos_b.index)
    if comuns.size < 10 * janela:
        raise ValueError("o par precisa de dias comuns de sobra")
    a = retornos_a.loc[comuns]
    b = retornos_b.loc[comuns]
    saida = {}
    for cauda in cortes:
        promessa.posto(janela, cauda)
        rompe_a = dependencia.rompimentos(a, janela, cauda)
        rompe_b = dependencia.rompimentos(b, janela, cauda)
        saida[cauda] = dependencia.juntos(rompe_a, rompe_b)
    return saida


def expoente(cortes, caixas: dict, minimo: int = 1) -> float:
    r"""A inclinação que a taxa anuncia: dois menos a rampa da razão contra o inverso da cauda.

    Se a conjunta cai como a marginal elevada a alfa, a razão contra a independência cresce com o
    inverso da cauda na rampa dois menos alfa --- e é esta rampa, lida por mínimos quadrados em
    log-log, que devolve alfa direto do dado. Só entram no ajuste as profundidades com contagem
    conjunta pelo menos \texttt{minimo}: onde nada foi contado, a razão é um limite, não um ponto ---
    e é assim que o controle negativo declara o seu «não tem sentido».
    """
    validos = [(c, float(caixas[c]["excesso"])) for c in cortes
               if int(caixas[c]["juntos"]) >= minimo]
    if len(validos) < 2:
        return float("nan")
    xs = np.log(np.asarray([1.0 / c for c, _ in validos]))
    ys = np.log(np.asarray([e for _, e in validos]))
    rampa = float(np.polyfit(xs, ys, 1)[0])
    return 2.0 - rampa


def intervalo(retornos_a: pd.Series, retornos_b: pd.Series, cortes,
              janela: int = JANELA_PADRAO, bloco: int = BLOCO_PADRAO,
              repeticoes: int = REPETICOES_PADRAO, semente: int = 0) -> tuple:
    r"""O intervalo do expoente por bootstrap de blocos, no desenho do capítulo do orçamento.

    Os dias comuns viajam em blocos inteiros --- as duas pernas juntas, para que a dependência
    sobreviva à reamostragem --- e o instrumento inteiro corre de novo em cada réplica:
    rompimentos, razões e expoente. O intervalo é o quantil das réplicas que têm expoente.
    """
    comuns = retornos_a.index.intersection(retornos_b.index)
    a = np.asarray(retornos_a.loc[comuns], dtype=float)
    b = np.asarray(retornos_b.loc[comuns], dtype=float)
    n = comuns.size
    quantos = int(np.ceil(n / bloco))
    valores = []
    for i in range(repeticoes):
        rng = np.random.default_rng(semente + i)
        inicios = rng.integers(0, n - bloco, quantos)
        escolha = np.concatenate([np.arange(ini, min(n, ini + bloco)) for ini in inicios])[:n]
        caixas = razoes(pd.Series(a[escolha], index=comuns),
                        pd.Series(b[escolha], index=comuns), cortes=cortes, janela=janela)
        valor = expoente(cortes, caixas)
        if np.isfinite(valor):
            valores.append(valor)
    if len(valores) < 2:
        return (float("nan"), float("nan"))
    return (float(np.quantile(valores, 0.025)), float(np.quantile(valores, 0.975)))


def _par_gaussiano(n: int, rng: np.random.Generator, rho: float) -> tuple:
    z = rng.normal(0.0, 1.0, (n, 2))
    z[:, 1] = rho * z[:, 0] + np.sqrt(1.0 - rho * rho) * z[:, 1]
    return z[:, 0], z[:, 1]


def controle_gaussiano(n: int, rng: np.random.Generator, rho_posto: float) -> tuple:
    r"""Um par gaussiano com a correlação de posto pedida, nada mais.

    A correspondência é a fechada da cópula gaussiana: o rho de Pearson que carrega um posto s
    é dois seno de pi s sobre seis. As margens são padrão --- quem rompe o corte e com que
    frequência é do instrumento, não da margem.
    """
    if not -1.0 < rho_posto < 1.0:
        raise ValueError("a correlação de posto precisa estar entre menos um e um")
    rho = 2.0 * np.sin(np.pi * rho_posto / 6.0)
    xa, ya = _par_gaussiano(n, rng, rho)
    return pd.Series(xa), pd.Series(ya)


def controle_t(n: int, rng: np.random.Generator, rho_posto: float, ni: int,
               piloto: int = 20000, tolerancia: float = 0.01) -> tuple:
    r"""Um par t com a correlação de posto pedida e o grau de liberdade declarado.

    A cópula t não tem correspondência fechada: o parâmetro gaussiano de dentro é calibrado por
    bisseção num piloto declarado, até que o posto do par t caia na tolerância. A transformação é
    a clássica: o par gaussiano dividido pela raiz de um qui-quadrado compartilhado sobre os graus
    de liberdade --- e o qui-quadrado compartilhado é o que faz a junta engordar sem mexer na
    margem.
    """
    if ni < 1:
        raise ValueError("os graus de liberdade precisam ser pelo menos um")

    def com_rho(rho):
        xa, ya = _par_gaussiano(piloto, rng, rho)
        raiz = np.sqrt(rng.chisquare(ni, piloto) / ni)
        return float(_stats.spearmanr(xa / raiz, ya / raiz).statistic)

    baixo, alto = -0.99, 0.99
    for _ in range(40):
        meio = 0.5 * (baixo + alto)
        if com_rho(meio) < rho_posto:
            baixo = meio
        else:
            alto = meio
        if alto - baixo < 1e-4:
            break
    rho = 0.5 * (baixo + alto)
    xa, ya = _par_gaussiano(n, rng, rho)
    raiz = np.sqrt(rng.chisquare(ni, n) / ni)
    return pd.Series(xa / raiz), pd.Series(ya / raiz)
