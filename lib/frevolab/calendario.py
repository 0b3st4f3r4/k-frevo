r"""O calendário: a mesma série lida na célula a que o dia pertence.

Família A — a forma que o relógio desenha. O capítulo anterior deixou um instrumento que
vigia uma série sozinha, e a proposição em que ele se apoia supõe que os dias são
\emph{trocáveis}: qualquer ordem é igualmente provável. Num domingo de consumo de energia
elétrica essa hipótese não é verdadeira nem por acidente --- ela é falsa de forma
\emph{predizível}, o que é pior para um vigia. O domingo não é um dia em que o mundo mudou; é
o domingo.

**O que este módulo faz.** Trata o calendário como uma partição dos dias em \emph{células} e
ergue o corte \emph{dentro} de cada célula: cada dia é comparado com os seus iguais. O
argumento é o da proposição do capítulo 3, aplicado uma célula por vez --- e dele sai o preço,
que é o que este módulo mede junto:

    com uma janela de n dias e C células, cada célula recebe n/C dias, e o alarme mais raro
    que ela consegue declarar é 1/(n/C + 1). Ler o calendário divide a memória por C e
    multiplica o orçamento por C.

**O defeito que este módulo torna impossível.** Comparar um domingo com sábados e segundas. Um
vigia que faz isso dispara em todo fim de semana e chama isso de mundo --- o defeito não é do
alarme, é de quem o lê. E o inverso também é defeito: condicionar onde não há calendário. O
instrumento de medir isso é \texttt{amplitude}, que diz o tamanho do perfil em desvios-padrão
do dia: vale 1,47 na carga dinamarquesa e 0,04 no índice americano, e é essa razão de trinta
que decide se vale a pena pagar pela partição.
"""
import numpy as np
import pandas as pd

DIAS_DA_SEMANA = ("segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo")

__all__ = ["DIAS_DA_SEMANA", "unica", "semana", "semana_e_trimestre", "semana_e_mes",
           "perfil", "amplitude", "orcamento_por_celula", "vigia_por_celula"]


def unica(indice: pd.DatetimeIndex) -> np.ndarray:
    r"""Uma célula só: todos os dias são iguais, que é a leitura dos capítulos anteriores."""
    return np.zeros(len(indice), dtype=int)


def semana(indice: pd.DatetimeIndex) -> np.ndarray:
    r"""Sete células, uma por dia da semana."""
    return indice.dayofweek.to_numpy()


def semana_e_trimestre(indice: pd.DatetimeIndex) -> np.ndarray:
    r"""Vinte e oito células: o dia da semana cruzado com a estação do ano.

    O calendário não tem uma célula, tem as que o mundo tiver. Quem lê só o dia da semana
    ainda compara um domingo de janeiro com um domingo de julho, e o inverno cobra a
    diferença.
    """
    return indice.dayofweek.to_numpy() * 4 + indice.quarter.to_numpy() - 1


def semana_e_mes(indice: pd.DatetimeIndex) -> np.ndarray:
    r"""Oitenta e quatro células: o dia da semana cruzado com o mês."""
    return indice.dayofweek.to_numpy() * 12 + indice.month.to_numpy() - 1


def perfil(serie: pd.Series, celula=semana) -> pd.Series:
    r"""O nível médio de cada célula: é isto que o calendário desenha na série."""
    if serie.empty:
        raise ValueError("serie vazia: nao ha perfil a medir")
    return serie.groupby(celula(serie.index)).mean().sort_index()


def amplitude(serie: pd.Series, celula=semana) -> float:
    r"""O tamanho do calendário, em desvios-padrão do dia.

    A distância entre a célula mais alta e a mais baixa, dividida pelo desvio-padrão da
    série. É o número que decide se vale pagar pela partição: perfil grande significa que o
    vigia cru vai gastar os seus alarmes no relógio; perfil pequeno significa que condicionar
    só encarece.
    """
    desvio = float(serie.std(ddof=1))
    if desvio == 0:
        raise ValueError("serie constante: nao ha amplitude a medir")
    valores = perfil(serie, celula)
    return float((valores.max() - valores.min()) / desvio)


def orcamento_por_celula(janela: int, n_celulas: int, dias_no_ano: int = 365) -> float:
    r"""O alarme mais raro que sobra para cada célula: C/(n + C), por dia.

    A conta é a do orçamento mínimo do capítulo anterior, com a memória já dividida: a célula
    recebe n/C dias, e o alarme mais raro que ela compra é 1/(n/C + 1). Não é uma
    recomendação nem um ajuste --- é o que a janela deixa, e cresce linearmente com o número de
    células que se decide ler.
    """
    if janela < 1:
        raise ValueError("a janela precisa de pelo menos um dia")
    if n_celulas < 1:
        raise ValueError("precisa de pelo menos uma celula")
    return n_celulas / (janela + n_celulas)


def vigia_por_celula(serie: pd.Series, janela: int, celula=semana, posto: int = 1) -> pd.Series:
    r"""O alarme do capítulo anterior, mas erguido dentro da célula a que o dia pertence.

    Cada célula recebe \texttt{m = janela // C} dias de memória, e o corte dela é o
    \emph{posto}-ésimo pior desses \emph{m} dias --- os \emph{m} dias da mesma célula que
    terminaram ontem. Os primeiros \emph{m} dias de cada célula ficam sem corte e não entram na
    série devolvida: são os dias de graça, e um dia em que não havia barra não é um dia em que
    a barra resistiu.

    Com \texttt{celula=unica} isto é exatamente o vigia do capítulo anterior, porque a célula
    única recebe a janela inteira. Não é coincidência: é a mesma regra, com a partição
    declarada.
    """
    valores = np.asarray(serie, dtype=float)
    if valores.size <= janela:
        raise ValueError("a serie precisa ser maior que a janela (%d dias)" % janela)
    rotulos = np.asarray(celula(serie.index))
    n_celulas = int(np.unique(rotulos).size)
    m = max(1, janela // n_celulas)
    if posto < 1 or posto > m:
        raise ValueError("o posto precisa estar entre 1 e a memoria da celula (%d)" % m)

    saida = pd.Series(False, index=serie.index)
    sem_corte = pd.Series(False, index=serie.index)
    for rotulo in np.unique(rotulos):
        posicoes = np.flatnonzero(rotulos == rotulo)
        if posicoes.size <= m:
            sem_corte.iloc[posicoes] = True
            continue
        janelas = np.lib.stride_tricks.sliding_window_view(valores[posicoes], m)
        limiares = np.partition(janelas, posto - 1, axis=1)[:, posto - 1]
        # o corte de hoje é erguido com os m dias que terminaram ontem
        dias = posicoes[m:]
        saida.iloc[dias] = valores[dias] < limiares[:-1]
        sem_corte.iloc[posicoes[:m]] = True
    return saida[~sem_corte]
