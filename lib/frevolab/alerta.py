r"""O alerta que todo mundo usa: a receita clássica, submetida ao par declarado.

A prática vigia a mudança que ainda vem com uma receita que tem nome e literatura: olhar a
variância e a autocorrelação da janela \emph{subirem} antes da transição chegar. A receita
nasceu fora das séries de preço --- em lagos, climas e ecossistemas ---, e chegou aqui sem
nunca ter declarado o par que o capítulo do orçamento cobra de todo alarme: com que
frequência ela soa quando nada muda, e quanto demora quando algo muda.

Este módulo é a receita posta na régua do livro, e nada além disso. São três estatísticas
rolantes, uma por dia, cada uma olhando a janela que termina hoje:

1. a \textbf{variância} da janela --- o quadrado do tamanho típico do dia, medido na janela;
2. a \textbf{autocorrelação} da janela --- se o dia de ontem informa o de hoje, na mesma janela;
3. a \textbf{assimetria} da janela --- o terceiro momento padronizado, o objeto que o vigia
   da direção já vigia em blocos.

Cada uma vira alarme por um limiar, e o limiar é calibrado onde só existe barulho: nos mundos
que nunca mudam, no mesmo gasto medido do outro instrumento --- o posto do corte. A
calibração conta \emph{episódios}, e não dias: a janela rolante arrasta o mesmo dia por
dentro da estatística, de modo que dias consecutivos acima do limiar são um alarme só, e é o
episódio a unidade que se declara em alarmes por ano.

A receita merece esta régua pelo mesmo motivo que o vigia mereceu a dele: sem o par, um
indicador que sobe é uma opinião com gráfico --- e o número que falta é justamente o que ele
custa quando o mundo está parado.
"""
import numpy as np
import pandas as pd

JANELA_PADRAO = 252        # a janela do corte: a memória que a receita herda do livro
DIAS_UTEIS = 252
TOLERANCIA = 1e-12

__all__ = ["JANELA_PADRAO", "DIAS_UTEIS", "variancia", "autocorrelacao", "assimetria",
           "dispara", "orcamento", "limiar_do_orcamento"]


def variancia(retornos: pd.Series, janela: int = JANELA_PADRAO) -> pd.Series:
    r"""A variância da janela que termina hoje, dia a dia, sem olhar para a frente.

    É o indicador principal da receita: o mundo que vai piorar, diz a receita, mostra isso
    primeiro no tamanho típico do dia. O valor em \emph{t} usa \emph{t-janela+1} a \emph{t},
    e os primeiros \emph{janela-1} dias ficam sem estatística --- quem consome respeita o
    vazio em vez de tratá-lo como zero.
    """
    if janela < 2:
        raise ValueError("a janela precisa de pelo menos dois dias")
    return retornos.rolling(janela).var(ddof=1).rename("variancia")


def autocorrelacao(retornos: pd.Series, janela: int = JANELA_PADRAO) -> pd.Series:
    r"""A autocorrelação de primeira ordem dentro da janela: ontem informa hoje?

    A conta é a da correlação clássica, feita janela a janela com somas móveis exatas: a
    covariância entre o dia e o dia anterior, ambos centrados pela média da própria janela,
    dividida pelo produto dos dois desvios. É a segunda perna da receita --- a que daria
    o aviso \emph{antes} do tamanho crescer, se o mundo em questão desacelerar a sua
    recuperação ---, e é também a mais frágil: num mundo de dias independentes ela é zero, e
    tudo o que sobra é o barulho da estimativa.
    """
    if janela < 3:
        raise ValueError("a autocorrelação precisa de pelo menos três dias na janela")
    r = retornos.astype(float)
    r1 = r.shift(1)
    soma = r.rolling(janela).sum()
    soma1 = r1.rolling(janela).sum()
    soma_q = (r * r).rolling(janela).sum()
    soma_q1 = (r1 * r1).rolling(janela).sum()
    cruz = (r * r1).rolling(janela).sum()
    cov = cruz - soma * soma1 / janela
    var = soma_q - soma * soma / janela
    var1 = soma_q1 - soma1 * soma1 / janela
    return (cov / np.sqrt(var * var1)).where((var > 0.0) & (var1 > 0.0)).rename("autocorrelacao")


def assimetria(retornos: pd.Series, janela: int = JANELA_PADRAO) -> pd.Series:
    r"""O terceiro momento padronizado da janela: o quanto o lado de baixo pesa.

    É a terceira perna da receita, e a que o livro já conhece de outra casa: o vigia da
    direção mede o mesmo objeto em blocos que não se sobrepõem. Aqui ele entra como a
    receita o usa, janela a janela --- e a diferença de janela é a diferença que importa:
    o bloco conta episódios, a janela arrasta o mesmo dia duzentas e cinquenta e duas vezes.
    """
    if janela < 3:
        raise ValueError("a assimetria precisa de pelo menos três dias na janela")
    return retornos.rolling(janela).skew().rename("assimetria")


def dispara(estatistica: pd.Series, limiar: float) -> pd.Series:
    r"""O dia em que a estatística alcançou o limiar: verdadeiro/falso, onde ela existe.

    O limiar vem da calibração em mundo parado, e o silêncio dos dias sem estatística é
    declarado em vez de preenchido --- um alarme não pode julgar os dias em que a janela
    ainda não existia.
    """
    if limiar <= 0.0:
        raise ValueError("o limiar precisa ser positivo")
    existe = estatistica.notna().to_numpy()
    acima = np.asarray(estatistica, dtype=float) >= limiar
    return pd.Series(acima[existe], index=estatistica.index[existe], name="alerta")


def orcamento(estatisticas_nulas, limiar: float, dias_uteis: int = DIAS_UTEIS) -> dict:
    r"""O que o limiar custa em mundo parado: episódios por ano, medidos na matriz.

    Recebe um mundo por linha --- a estatística de cada mundo que nunca muda --- e conta
    \emph{episódios}: o primeiro dia de cada travessia do limiar, porque a janela rolante
    arrasta a estatística por cima do limiar por muitos dias seguidos e o alarme, para quem
    o ouve, é um só. É a mesma unidade do orçamento do vigia, e é ela que permite pôr a
    receita e o corte na mesma curva.
    """
    e = np.asarray(estatisticas_nulas, dtype=float)
    if e.ndim != 2:
        raise ValueError("o orçamento se mede sobre uma matriz de mundos × dias")
    mundos, dias = e.shape
    acima = e >= limiar
    comeca = acima & ~np.concatenate((np.zeros((mundos, 1), dtype=bool), acima[:, :-1]), axis=1)
    episodios = comeca.sum(axis=1)
    anos = dias / float(dias_uteis)
    media = float(episodios.mean())
    return {
        "mundos": int(mundos),
        "dias_por_mundo": float(dias),
        "episodios_por_mundo": media,
        "anos_por_alarme": float(anos / media) if media > 0 else float("inf"),
        "episodios_por_ano": float(media / anos) if anos > 0 else float("nan"),
    }


def limiar_do_orcamento(estatisticas_nulas, episodios_por_ano: float,
                        dias_uteis: int = DIAS_UTEIS) -> float:
    r"""O limiar cujo gasto, em episódios por ano, é o declarado --- medido, não prometido.

    A bisseção anda sobre o limiar e o \texttt{orcamento} responde: mais limiar, menos
    episódios, sempre. Calibrar pelo gasto medido --- e não por uma conta de quantil por dia
    --- é o que faz a comparação honesta: o posto do corte tem taxa exata de dias, mas os
    dias dele também se agrupam, e é o episódio que ambos gastam.
    """
    if episodios_por_ano <= 0.0:
        raise ValueError("o orçamento em episódios por ano precisa ser positivo")
    e = np.asarray(estatisticas_nulas, dtype=float)
    valores = e[~np.isnan(e)]
    if valores.size == 0:
        raise ValueError("não há estatística nula para calibrar")
    baixo, alto = float(valores.min()), float(valores.max())
    gasto = lambda lim: orcamento(e, lim, dias_uteis)["episodios_por_ano"]
    if gasto(alto) > episodios_por_ano:
        raise ValueError("nem o valor máximo gasta o orçamento pedido: %r" % gasto(alto))
    for _ in range(80):
        meio = 0.5 * (baixo + alto)
        if gasto(meio) > episodios_por_ano:
            baixo = meio
        else:
            alto = meio
        if alto - baixo <= TOLERANCIA * max(1.0, abs(meio)):
            break
    return float(0.5 * (baixo + alto))
