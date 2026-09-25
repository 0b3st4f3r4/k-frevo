r"""O laço: a série que o instrumento produz quando o instrumento age sobre ela.

O capítulo da partilha fechou com o limite honesto: a escala é a que precisa ser atualizada
sempre, e a atualização \emph{é} uma decisão sobre o mundo. Este módulo fecha essa conta no
formato dela: o rompimento do corte dispara a ação declarada --- vender uma fração da posição
---, a venda devolve parte da oscilação ao dia do atraso, e a série que sobra é a que o corte
seguinte vai ler \cite{perdomo2020performative}.

**A reação, declarada.** Um rompimento no dia \texttt{t} (retorno abaixo do corte que a janela
ergueu) amortece o dia \texttt{t + atraso}: o retorno realizado dele vem multiplicado por
\texttt{(1 - fracao)}. Dois rompimentos que alimentam o mesmo dia amortecem uma vez só --- a
posição não fica negativa e o amortecimento não compõe no mesmo dia. Fração nula é o controle
da transformação neutra \cite{ng1999policy}: o laço devolve o mundo intacto, dia por dia, e é
contra ele que qualquer diferença se declara como efeito do mundo e não defeito do instrumento.

**O limite declarado (§8.5).** O mundo que reage é família declarada, não mercado: a medição diz
o que a família faz com o corte, e não que o mercado obedece à família.
"""
import numpy as np
import pandas as pd

from . import promessa

FRACAO_PADRAO = 0.1
ATRASO_PADRAO = 1

__all__ = ["FRACAO_PADRAO", "ATRASO_PADRAO", "reage", "recalibra", "entregas"]


def reage(retornos, cortes, fracao: float = FRACAO_PADRAO, atraso: int = ATRASO_PADRAO) -> np.ndarray:
    r"""A série realizada: o dia do atraso de cada rompimento, amortecido pela fração vendida.

    Os cortes entram como a linha que o próprio módulo de promessas ergue --- a mesma do capítulo
    da raiz, com os dias sem corte declarados sem valor: rompimento só existe onde havia barra.
    """
    x = np.asarray(retornos, dtype=float)
    c = np.asarray(cortes, dtype=float)
    if x.ndim != 1 or c.shape != x.shape:
        raise ValueError("os retornos e os cortes precisam ter o mesmo comprimento")
    if not 0.0 <= fracao <= 1.0:
        raise ValueError("a fração vendida vive entre zero e um")
    atraso = int(atraso)
    if atraso < 0:
        raise ValueError("o atraso não pode ser negativo")
    valido = np.isfinite(c)
    rompe = np.zeros(x.size, dtype=bool)
    rompe[valido] = x[valido] < c[valido]
    alvo = np.zeros(x.size, dtype=bool)
    for t in np.flatnonzero(rompe):
        d = t + atraso
        if d < x.size:
            alvo[d] = True
    y = x.copy()
    y[alvo] *= (1.0 - fracao)
    return y


def recalibra(retornos, janela: int, posto_k: int, ciclos: int = 5,
              fracao: float = FRACAO_PADRAO, atraso: int = ATRASO_PADRAO) -> dict:
    r"""O laço inteiro: corte, reação, e a série que sobra --- ciclo a ciclo, sem peça nova.

    Cada ciclo ergue o corte da raiz (o \texttt{posto_k}-ésimo pior da \texttt{janela} que
    termina ontem) sobre a série corrente, aplica a reação declarada, e guarda três coisas: o
    corte do último dia do ciclo (a calibragem mais recente), a entrega da barreira recalibrada,
    e a série realizada. A primeira série é o mundo sorteado; as seguintes são o que o laço
    produziu \cite{mendlerdunner2020stochastic}.
    """
    s = pd.Series(np.asarray(retornos, dtype=float))
    historico = {"cortes": [], "entregas": [], "series": [s.to_numpy().copy()]}
    corrente = s
    for _ in range(int(ciclos)):
        linha = promessa.corte_no_posto(corrente, int(janela), int(posto_k))
        historico["cortes"].append(float(linha.iloc[-1]))
        taxa = float(promessa.violacoes_no_posto(corrente, int(janela), int(posto_k)).mean())
        historico["entregas"].append(taxa)
        corrente = pd.Series(reage(corrente.to_numpy(), linha.to_numpy(),
                                   fracao=fracao, atraso=atraso))
        historico["series"].append(corrente.to_numpy().copy())
    return historico


def entregas(series_por_ciclo, janela: int, posto_k: int) -> list:
    r"""A entrega de cada série do laço contra o corte que a própria série ergue.

    É a pergunta do capítulo dita em número: depois de \emph{j} voltas do laço, quanto vale a
    promessa medida --- e é a mesma pergunta para a série de controle, que nunca mudou.
    """
    fora = []
    for s in series_por_ciclo:
        corrente = pd.Series(np.asarray(s, dtype=float))
        fora.append(float(promessa.violacoes_no_posto(corrente, int(janela), int(posto_k)).mean()))
    return fora
