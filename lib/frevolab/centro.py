r"""O centro: o instrumento que vê a mudança que não engorda a cauda.

O vigia do capítulo anterior conta rompimentos da linha, e rompimento é uma medida de
\emph{escala}: ele vê o mundo começar a oscilar mais. Este módulo mede a outra metade ---
onde está o meio ---, e existe porque as duas mudanças são de naturezas diferentes e um
instrumento cego para uma delas não é um instrumento pior: é um instrumento de outra forma.

A estatística é a mais velha que existe para essa pergunta: a média dos últimos dias, medida
em erros-padrão dela mesma,
\[
  t = \frac{\bar r}{s/\sqrt{n}},
\]
com $\bar r$ e $s$ tirados da mesma janela que termina hoje. Ela responde "o centro andou mais
do que o próprio barulho do centro explica?", e a resposta não depende da escala do mundo:
dobrar a oscilação dobra $s$ e dobra o desvio da média, deixando $t$ onde estava.

Essa última frase é a proposição do capítulo, e é também o defeito do instrumento: **um
mundo que passa a oscilar o dobro tem o mesmo $t$** — o centro não se moveu, a escala se
moveu. Os dois instrumentos juntos cobrem as duas formas; nenhum dos dois cobre as duas.

A janela vale para trás, como tudo neste livro: o valor em \emph{t} usa os \emph{n} dias que
terminam em \emph{t}, e nada depois.
"""
import numpy as np
import pandas as pd

JANELA_PADRAO = 60

__all__ = ["JANELA_PADRAO", "media_padronizada", "dispara", "limiar_do_orcamento"]


def media_padronizada(retornos: pd.Series, janela: int = JANELA_PADRAO) -> pd.Series:
    r"""A média da janela em erros-padrão dela mesma, dia a dia, sem olhar para a frente.

    O valor em \emph{t} usa \emph{t-janela+1} a \emph{t}. Os primeiros \emph{janela-1} dias
    ficam sem estatística, e é isso que o \texttt{NaN} declara: quem consome respeita o vazio
    em vez de tratá-lo como zero. Janela de desvio nulo devolve \texttt{NaN}, porque um mundo
    sem barulho não tem erro-padrão por onde medir o centro.
    """
    if janela < 2:
        raise ValueError("a janela precisa de pelo menos dois dias")
    media = retornos.rolling(janela).mean()
    desvio = retornos.rolling(janela).std(ddof=1)
    # Janela sem barulho não tem erro-padrão por onde medir o centro, e sem isto a divisão
    # devolve infinito --- que num vigia dispara todos os dias, porque |t| >= limiar. A
    # docstring já prometia o vazio; agora o código o entrega.
    return (media / (desvio / np.sqrt(janela))).where(desvio > 0.0).rename("centro")


def dispara(retornos: pd.Series, janela: int = JANELA_PADRAO,
            limiar: float = 3.0) -> pd.Series:
    r"""O dia em que o centro andou mais que o \emph{limiar} permite: $|t| \geq$ limiar.

    Devolve verdadeiro/falso pelos mesmos dias do corte do capítulo anterior ---
    \texttt{len(retornos) - janela + 1} entradas ---, para que a latência e o gasto dos dois
    instrumentos sejam medidos sobre a mesma lista de dias e possam ser comparados.
    """
    if limiar <= 0:
        raise ValueError("o limiar precisa ser positivo")
    estatistica = media_padronizada(retornos, janela)
    existe = estatistica.notna().to_numpy()
    acima = np.abs(estatistica.to_numpy()) >= limiar
    return pd.Series(acima[existe], index=retornos.index[existe], name="centro")


def limiar_do_orcamento(estatistica_nula, taxa: float) -> float:
    r"""O limiar cujo gasto diário é a \emph{taxa} declarada, medido em mundos parados.

    A taxa é o orçamento na unidade em que ele se declara: alarmes por dia. O limiar é o
    quantil dela na estatística de um mundo que nunca muda, e é assim que dois instrumentos
    de formas diferentes ficam comparáveis --- mesmo orçamento, mesma lista de dias, e a
    única diferença que sobra é a forma que cada um consegue ver.
    """
    if not 0.0 < taxa < 1.0:
        raise ValueError("a taxa precisa estar entre 0 e 1 por dia")
    valores = np.abs(np.asarray(estatistica_nula, dtype=float))
    valores = valores[~np.isnan(valores)]
    if valores.size == 0:
        raise ValueError("não há estatística nula para calibrar")
    return float(np.quantile(valores, 1.0 - taxa))
