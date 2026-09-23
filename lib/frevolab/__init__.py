"""frevolab — a biblioteca oficial do projeto.

A divisão é uma só, e vale para tudo o que vier: **o que é algoritmo mora aqui; o que é
experimento mora em `lab/experimentos/`**. O caderno importa, chama, constrói o gráfico e
grava o resultado — ele não implementa conta.

Por que a separação vale o incômodo: algoritmo dentro de caderno não é testável, não é
reusável e não é revisável — só é legível na ordem em que foi escrito. Aqui ele vira
código com nome, com teste próprio (`auto_teste()`) e com versão.

Os dados minerados do arquivo do projeto anterior vivem em `.old/dados/` e são declarados
em `frevolab.dados.ARQUIVO`: o empréstimo é explícito, e o número que sai dele é remedido
(AGENTS.md §10).
"""
from importlib.metadata import PackageNotFoundError, version

from . import dados, graficos, volatilidade

# A versão tem uma fonte só, e ela é o pyproject.toml: duas cópias divergem, e a
# divergência é silenciosa. O fallback existe para o caso de o pacote ser lido da
# árvore de trabalho, sem instalação.
try:
    VERSAO = version("frevolab")
except PackageNotFoundError:
    VERSAO = "0.1.0"

__all__ = ["dados", "graficos", "volatilidade", "VERSAO", "auto_teste"]


def auto_teste() -> list:
    """Confere propriedades conhecidas de antemão. Devolve os problemas; vazio é limpo.

    Não é uma suíte de testes com arcabouço: são asserções de propriedade, do tipo que
    pega erro de sinal, de unidade e de eixo trocado — os três defeitos que uma figura
    bonita esconde.
    """
    import numpy as np
    import pandas as pd

    problemas = []

    # uma série constante não tem volatilidade
    constante = pd.Series(np.full(600, 100.0))
    if abs(volatilidade.volatilidade_anualizada(volatilidade.retornos_log(constante))) > 1e-12:
        problemas.append("série constante deveria ter volatilidade zero")

    # volatilidade conhecida: desvio diário fixo, anualização pela raiz de 252
    rng = np.random.default_rng(7)
    diario = pd.Series(rng.normal(0.0, 0.01, 4000))
    esperado = 0.01 * np.sqrt(252)
    medido = volatilidade.volatilidade_anualizada(diario)
    if abs(medido - esperado) / esperado > 0.05:
        problemas.append("volatilidade anualizada fora de 5%% do esperado (%.4f contra %.4f)"
                         % (medido, esperado))

    # a razão recente/histórica dobra quando o desvio recente dobra
    calmo = rng.normal(0.0, 0.01, 2000)
    agitado = rng.normal(0.0, 0.02, 300)
    serie = pd.Series(np.concatenate([calmo, agitado]))
    retornos = volatilidade.retornos_log(np.exp(serie.cumsum()))
    razao = volatilidade.razao_recente_historica(retornos, 300)
    if not 1.6 < razao < 2.4:
        problemas.append("razão de volatilidade fora do esperado (%.3f)" % razao)

    # a janela rolante tem o comprimento certo e não olha para a frente
    rolante = volatilidade.volatilidade_rolante(retornos, 300)
    if int(rolante.notna().sum()) != len(retornos) - 299:
        problemas.append("janela rolante com comprimento errado")
    if abs(rolante.iloc[-1] - retornos.iloc[-300:].std() * np.sqrt(252)) > 1e-9:
        problemas.append("janela rolante não fecha na última janela completa")

    # o salvamento grava os dois formatos
    import tempfile
    from pathlib import Path

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    with tempfile.TemporaryDirectory() as pasta:
        fig, _ = plt.subplots()
        caminhos = graficos.salvar(fig, "auto_teste", 1, destino=Path(pasta))
        plt.close(fig)
        for caminho in caminhos:
            if not caminho.exists() or caminho.stat().st_size == 0:
                problemas.append("figura não foi gravada: %s" % caminho.name)

    return problemas
