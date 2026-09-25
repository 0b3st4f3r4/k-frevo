r"""O relógio e a causa: a ordem que sobrevive (ou não) ao alinhamento declarado.

O capítulo da queda conjunta deixou de pé uma assimetria medida e repetida --- o número que o leitor
escreve como causa na linha seguinte. Este módulo é o instrumento da pergunta seguinte: a ordem
sobrevive ao alinhamento do relógio? Cada atraso declarado reencontra os dias --- a sessão de ontem
de um mercado contra a sessão de hoje do outro --- e mede a mesma assimetria dos episódios dirigidos
contra o nulo de pares sorteados que carrega \emph{o mesmo deslocamento}: sem essa carga, a régua é
de outro desenho, e o pico da varredura pode ser do instrumento, não do mundo.

**O que a varredura não promete.** Ela separa relógio de ordem, e não ordem de causa: um par sem
canal nenhum que repete a assinatura, e um par movido por um terceiro comum sem seta nenhuma, são os
controles que faltam --- e vivem no caderno, montados com o resto da casa.
"""
import numpy as np
import pandas as pd

from . import dependencia, mudanca

JANELA_PADRAO = 252
CAUDA_PADRAO = 0.05
EPISODIO_PADRAO = 5
NULOS_PADRAO = 40
SEMENTES_PADRAO = 300
SIGMA_NULO = 0.012
RHO_NULO = 0.5

__all__ = ["varredura", "terceiro_comum"]


def terceiro_comum(n: int, rng: np.random.Generator, rho: float,
                   sigma_a: float, sigma_b: float) -> tuple:
    r"""Duas pernas independentes movidas por um terceiro comum, com as margens declaradas.

    O grafo é o declarado: um choque padrão partilhado e dois ruídos próprios, um em cada perna ---
    nenhuma seta de uma perna para a outra. O 	exttt{rho} é a fração da variância de cada perna que
    vem do terceiro. As margens carregam os 	exttt{sigma} pedidos: a perna menos ruidosa cruza o
    próprio corte antes, e é isso que faz a ordem aparecer sem causa nenhuma --- o par de calos que
    este gerador existe para calçar.
    """
    if n < 2:
        raise ValueError("a série precisa de pelo menos dois dias")
    if not 0.0 <= rho <= 1.0:
        raise ValueError("o rho do terceiro precisa estar entre zero e um")
    if sigma_a <= 0.0 or sigma_b <= 0.0:
        raise ValueError("os sigmas das pernas precisam ser positivos")
    t = rng.normal(0.0, 1.0, n)
    ea = rng.normal(0.0, 1.0, n)
    eb = rng.normal(0.0, 1.0, n)
    c = np.sqrt(rho)
    s = np.sqrt(1.0 - rho)
    return sigma_a * (c * t + s * ea), sigma_b * (c * t + s * eb)


def varredura(retornos_a: pd.Series, retornos_b: pd.Series, atrasos=(0, 1, 2, 5, 10, 21),
              janela: int = JANELA_PADRAO, cauda: float = CAUDA_PADRAO,
              episodio: int = EPISODIO_PADRAO, nulos: int = NULOS_PADRAO,
              sementes: int = SEMENTES_PADRAO) -> dict:
    r"""A assimetria dos episódios dirigidos em cada atraso, contra o nulo deslocado igual.

    Para cada atraso: a perna B anda com o \texttt{pareado} da casa (os mesmos valores, o par
    reencontrado), os rompimentos são os do corte próprio de cada série, e o nulo sorteia pares
    correlacionados do mesmo comprimento --- com a perna sorteada passando pelo MESMO
    deslocamento antes da medida. Devolve, por atraso, a assimetria do par real, a média e a
    dispersão do nulo, a distância em desvios e os dias comuns do par.
    """
    comuns = retornos_a.index.intersection(retornos_b.index)
    if comuns.empty:
        raise ValueError("as duas séries não têm datas em comum")
    rompe_a = dependencia.rompimentos(retornos_a, janela, cauda)
    rompe_b = dependencia.rompimentos(retornos_b, janela, cauda)
    saida = {}
    for atraso in atrasos:
        b_desloc = dependencia.pareado(retornos_b, atraso)
        index = comuns.intersection(b_desloc.index)
        pa = rompe_a.reindex(index).fillna(False).astype(bool)
        pb = dependencia.rompimentos(b_desloc, janela, cauda).reindex(index).fillna(False).astype(bool)
        real = dependencia.episodios_dirigidos(pa, pb, episodio)["assimetria"]
        nulos_medidas = []
        for i in range(nulos):
            x, y = mudanca.dependencia(comuns.size, np.random.default_rng(sementes + i),
                                       SIGMA_NULO, RHO_NULO, RHO_NULO, comuns.size // 2)
            y_serie = dependencia.pareado(pd.Series(y, index=comuns), atraso)
            idx = comuns.intersection(y_serie.index)
            px = dependencia.rompimentos(pd.Series(x, index=comuns), janela, cauda).reindex(idx).fillna(False).astype(bool)
            py = dependencia.rompimentos(y_serie, janela, cauda).reindex(idx).fillna(False).astype(bool)
            nulos_medidas.append(dependencia.episodios_dirigidos(px, py, episodio)["assimetria"])
        nulos_medidas = np.asarray(nulos_medidas, dtype=float)
        media = float(nulos_medidas.mean())
        dispersao = float(nulos_medidas.std(ddof=1)) if nulos > 1 else 0.0
        saida[atraso] = {"assimetria": float(real), "nulo_media": media, "nulo_dispersao": dispersao,
                         "desvios": float((real - media) / dispersao) if dispersao > 0 else 0.0,
                         "dias": int(index.size)}
    return saida
