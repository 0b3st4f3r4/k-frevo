"""Leitura das séries do arquivo. O empréstimo é declarado aqui, num lugar só."""
from pathlib import Path

import pandas as pd

# O projeto anterior deixou os dados em .old/dados/. Minerar é permitido e declarado
# (AGENTS.md §10): o dado atravessa, o resultado não.
ARQUIVO = Path(".old/dados")


def carregar_serie(nome: str, coluna: str = "close") -> pd.Series:
    """Lê uma série do arquivo e devolve uma Series indexada por data.

    `nome` é o arquivo dentro de `frevolab.dados.ARQUIVO` — por exemplo
    `carregar_serie("sp500.csv")`. A coluna padrão é `close`; as séries do arquivo têm a
    data na primeira coluna e o valor na coluna pedida.
    """
    caminho = ARQUIVO / nome
    if not caminho.exists():
        raise FileNotFoundError("série ausente no arquivo: %s" % caminho)
    tabela = pd.read_csv(caminho, index_col=0, parse_dates=True)
    if coluna not in tabela.columns:
        raise KeyError("a série %s não tem a coluna %r; tem %s"
                       % (nome, coluna, list(tabela.columns)))
    serie = tabela[coluna].astype(float).sort_index()
    serie = serie[~serie.index.duplicated(keep="last")].dropna()
    serie.index.name = "data"
    return serie
