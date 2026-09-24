"""Volatilidade: o algoritmo da primeira medição, testável fora de qualquer caderno."""
import numpy as np
import pandas as pd

DIAS_UTEIS = 252

__all__ = ["DIAS_UTEIS", "retornos_log", "volatilidade_anualizada", "volatilidade_rolante",
           "razao_recente_historica"]


def retornos_log(serie: pd.Series) -> pd.Series:
    """Retorno logarítmico entre pregões consecutivos, com o primeiro descartado."""
    return np.log(serie).diff().dropna()


def volatilidade_anualizada(retornos: pd.Series, dias_uteis: int = DIAS_UTEIS) -> float:
    r"""Desvio-padrão dos retornos escalado para o ano.

    A anualização multiplica por \sqrt{dias uteis}: variância cresce com o tempo, desvio
    cresce com a raiz dele. É por isso que a raiz aparece e não o número de dias.
    """
    return float(retornos.std(ddof=1) * np.sqrt(dias_uteis))


def volatilidade_rolante(retornos: pd.Series, janela: int,
                         dias_uteis: int = DIAS_UTEIS) -> pd.Series:
    r"""Volatilidade de cada janela de \emph{janela} retornos, sem olhar para a frente.

    A janela termina no instante corrente: o valor em \emph{t} usa \emph{t-janela+1} a
    \emph{t} e nada depois. Ler o futuro num gráfico de risco é o erro que transforma uma
    medição honesta numa promessa que não se paga.
    """
    if janela < 2:
        raise ValueError("a janela precisa de pelo menos dois retornos")
    return retornos.rolling(janela).std(ddof=1) * np.sqrt(dias_uteis)


def razao_recente_historica(retornos: pd.Series, janela: int) -> float:
    r"""Quanto a volatilidade recente difere da do histórico inteiro.

    Vale 1 quando nada mudou, e é o primeiro número que responde "o mundo ficou mais
    calmo ou mais agitado?" — sem responder \emph{quando} mudou, que é pergunta de outro
    instrumento.
    """
    historica = volatilidade_anualizada(retornos)
    if historica == 0:
        raise ValueError("histórico de volatilidade nula: a razão não existe")
    recente = volatilidade_anualizada(retornos.iloc[-janela:])
    return float(recente / historica)
