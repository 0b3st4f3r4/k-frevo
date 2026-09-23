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

from . import dados, graficos, promessa, volatilidade

# A versão tem uma fonte só, e ela é o pyproject.toml: duas cópias divergem, e a
# divergência é silenciosa. O fallback existe para o caso de o pacote ser lido da
# árvore de trabalho, sem instalação.
try:
    VERSAO = version("frevolab")
except PackageNotFoundError:
    VERSAO = "0.1.0"

__all__ = ["dados", "graficos", "promessa", "volatilidade", "VERSAO", "auto_teste"]


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

    # --- a promessa e a entrega (promessa.py) ---

    # o posto é inteiro: 5% de 252 não existe, e o corte é o 13º pior
    if [promessa.posto(j) for j in (21, 252, 1260)] != [2, 13, 63]:
        problemas.append("posto errado: %s" % [promessa.posto(j) for j in (21, 252, 1260)])
    if abs(promessa.entrega_do_corte(252) - 13 / 253) > 1e-15:
        problemas.append("a conta do corte não é k/(n+1)")

    # o corte não olha para a frente: o de `t` é o k-ésimo pior da janela que termina em t-1
    curta = pd.Series(rng.normal(0.0, 0.01, 1000))
    linha = promessa.corte(curta, 21)
    for t in (21, 500, 999):
        esperado = float(np.sort(curta.to_numpy()[t - 21:t])[1])
        if abs(float(linha.iloc[t]) - esperado) > 1e-15:
            problemas.append("corte em t=%d não é o 2º pior da janela que termina ontem" % t)

    # dias de graça não existem: a série de violações tem exatamente len - janela entradas
    if len(promessa.violacoes(curta, 21)) != len(curta) - 21:
        problemas.append("violações com dias de graça: %d entradas para %d dias"
                         % (len(promessa.violacoes(curta, 21)), len(curta)))

    # a proposição, num mundo que nunca muda: a entrega média é a conta do corte
    uniforme = pd.Series(rng.uniform(0.0, 1.0, 50000))
    medida = promessa.entrega(uniforme, 21)["taxa"]
    if abs(medida - promessa.entrega_do_corte(21)) > 0.02:
        problemas.append("mundo uniforme: entrega %.4f longe da conta do corte %.4f"
                         % (medida, promessa.entrega_do_corte(21)))

    # as duas leituras são da mesma conta: a taxa é a média das violações
    d = promessa.entrega(curta, 21, bloco=60)
    if d["violacoes"] != int(promessa.violacoes(curta, 21).sum()):
        problemas.append("o resumo da entrega não fecha com as violações")

    # episódios: blocos consecutivos acima do limite são um episódio, não vários
    contagem_teste = pd.Series([0.0, 0.0, 5.0, 5.0, 0.0, 0.0, 6.0, 0.0])
    if len(promessa.episodios_acima(contagem_teste, 3)) != 2:
        problemas.append("episódios acima do limite não agrupam blocos consecutivos")
    if len(promessa.episodios_acima(contagem_teste, 9)) != 0:
        problemas.append("episódios acima do limite contam o que não passou do limite")
    if promessa.episodios_acima(contagem_teste, 3)[1]["pico"] != 6.0:
        problemas.append("o pico do episódio não é o maior bloco dele")

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
