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

from . import (calendario, dados, dependencia, estabilidade, graficos, intervencao, mudanca,
               partilha, promessa, regimes, vigia, volatilidade)

# A versão tem uma fonte só, e ela é o pyproject.toml: duas cópias divergem, e a
# divergência é silenciosa. O fallback existe para o caso de o pacote ser lido da
# árvore de trabalho, sem instalação.
try:
    VERSAO = version("frevolab")
except PackageNotFoundError:
    VERSAO = "0.1.0"

__all__ = ["calendario", "dados", "dependencia", "estabilidade", "graficos", "intervencao",
           "mudanca", "partilha", "promessa", "regimes", "vigia", "volatilidade", "VERSAO",
           "auto_teste"]


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

    # --- o vigia e o seu orçamento (vigia.py) ---

    # o piso do atraso é o próprio limiar
    if vigia.piso_de_atraso(13) != 13:
        problemas.append("o piso de atraso não é o limiar")
    try:
        vigia.piso_de_atraso(0)
        problemas.append("piso de atraso aceitou limiar zero")
    except ValueError:
        pass

    # o alarme soa onde o bloco atinge o limiar, e blocos vizinhos são um episódio só
    contagem = pd.Series([0.0, 2.0, 3.0, 3.0, 0.0, 5.0, 5.0, 0.0])
    if len(vigia.alarmes(contagem, 3)) != 2:
        problemas.append("alarmes não agrupam blocos vizinhos acima do limiar")
    if len(vigia.alarmes(contagem, 6)) != 0:
        problemas.append("alarmes dispararam sem o bloco atingir o limiar")
    if vigia.alarmes(contagem, 5)[0]["pico"] != 5.0:
        problemas.append("o pico do alarme não é o maior bloco dele")

    # o teto independente: com limiar 1, cada bloco conta se algum dia violar
    teto = vigia.teto_independente(8, 60, 0.05, 1)
    esperado = 8 * (1 - 0.95 ** 60)
    if abs(teto - esperado) > 1e-12:
        problemas.append("teto independente errado no limiar 1 (%.6f contra %.6f)"
                         % (teto, esperado))
    if vigia.teto_independente(8, 60, 0.05, 5) >= vigia.teto_independente(8, 60, 0.05, 4):
        problemas.append("o teto não cai quando o limiar sobe")

    # o orçamento de uma matriz de mundos: dias, episódios e anos por alarme
    blocos = np.array([[0.0, 2.0, 3.0, 3.0, 0.0, 5.0, 5.0, 0.0],
                       [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]])
    orcado = vigia.orcamento(blocos, 3, dias_uteis=252)
    if abs(orcado["dias_por_mundo"] - 2.0) > 1e-12:
        problemas.append("orçamento com dias por mundo errado")
    if abs(orcado["episodios_por_mundo"] - 1.0) > 1e-12:
        problemas.append("orçamento com episódios por mundo errado")
    if abs(orcado["anos_por_alarme"] - (8 / 252)) > 1e-12:
        problemas.append("orçamento com anos por alarme errado")

    # o prejuízo já pago: topo, fundo e a fração que já tinha acontecido
    datas = pd.date_range("2020-01-01", periods=700, freq="D")
    valores = np.concatenate([np.linspace(90.0, 100.0, 300), np.linspace(100.0, 80.0, 100),
                              np.full(300, 80.0)])
    valores[350] = 90.0
    pago = vigia.prejuizo_pago(pd.Series(valores, index=datas), datas[350], janela=252)
    if abs(pago["fracao_paga"] - 0.5) > 1e-9:
        problemas.append("fração paga errada (%.4f contra 0,5)" % pago["fracao_paga"])
    if pago["atraso_dias"] != (datas[350] - datas[299]).days:
        problemas.append("atraso até o topo errado")

    # --- o orçamento declarado e as formas da mudança (vigia.py, mudanca.py) ---

    # o corte por posto é o mesmo corte: a cauda é só uma maneira de escolher o posto
    por_posto = promessa.corte_no_posto(curta, 21, promessa.posto(21, 0.05))
    if not np.allclose(promessa.corte(curta, 21).to_numpy(), por_posto.to_numpy(), equal_nan=True):
        problemas.append("o corte por posto não coincide com o corte por cauda")

    # o orçamento mínimo é 1/(n+1), e o posto que ele compra é o primeiro
    if abs(vigia.orcamento_minimo(252) - 1 / 253) > 1e-15:
        problemas.append("o orçamento mínimo não é 1/(n+1)")
    if vigia.posto_do_orcamento(252, 1 / 253) != 1:
        problemas.append("um alarme por ano com um ano de memória não é o primeiro posto")
    if vigia.memoria_para(1 / 253) != 252:
        problemas.append("a memória de um alarme por ano não é um ano (%d)"
                         % vigia.memoria_para(1 / 253))
    if vigia.memoria_para(1 / 2521) != 2520:
        problemas.append("a memória de um alarme por década não é uma década")

    # pedir mais fino do que a memória compra é erro declarado, e não silêncio
    try:
        vigia.posto_do_orcamento(21, 1 / 253)
        problemas.append("memória de um mês aceitou um orçamento que ela não pode honrar")
    except ValueError:
        pass

    # o vigia do dia entrega o orçamento que declara, num mundo que nunca muda
    rng_declarado = np.random.default_rng(31)
    mundo_parado = pd.Series(mudanca.estavel(20000, rng_declarado))
    alarmado = vigia.dispara(mundo_parado, 252, vigia.orcamento_minimo(252))
    esperado_alarmes = alarmado.size / 253
    if not 0.5 * esperado_alarmes < alarmado.sum() < 1.8 * esperado_alarmes:
        problemas.append("o vigia do dia não entregou o orçamento declarado (%d alarmes para %.1f)"
                         % (alarmado.sum(), esperado_alarmes))

    # a latência é zero no próprio dia da mudança, e nan quando não veio alarme nenhum
    posicoes = pd.RangeIndex(10)
    if not np.isnan(vigia.latencia(pd.Series([False] * 10, index=posicoes), 5)):
        problemas.append("latência sem alarme deveria ser nan, e não um número")
    no_dia = pd.Series([False, False, False, False, False, True, False, False, False, False],
                       index=posicoes)
    if vigia.latencia(no_dia, 5) != 0.0:
        problemas.append("o alarme no próprio dia da mudança não tem latência zero")
    if vigia.falsos_antes(no_dia, 5) != 0:
        problemas.append("falsos antes contou um alarme que veio depois da mudança")
    if vigia.falsos_antes(pd.Series([True, False, False, True, False], index=posicoes[:5]), 3) != 1:
        problemas.append("falsos antes não contou o alarme que veio antes da mudança")

    # as formas da mudança fazem exatamente o que dizem: mesmo sorteio, escala declarada
    base = mudanca.estavel(3000, np.random.default_rng(41))
    escalado = np.ones(3000)
    escalado[1000:] = 2.0
    if not np.allclose(mudanca.degrau(3000, np.random.default_rng(41), fator=2.0, quando=1000),
                       base * escalado):
        problemas.append("o degrau não multiplica a oscilação pelo fator declarado")
    em_rampa = np.ones(3000)
    em_rampa[1000:1100] = np.linspace(1.0, 3.0, 100)
    em_rampa[1100:] = 3.0
    if not np.allclose(mudanca.rampa(3000, np.random.default_rng(41), fator=3.0, quando=1000,
                                     dias=100), base * em_rampa):
        problemas.append("a rampa não cresce até o fator declarado no número de dias declarado")
    deslocado = base.copy()
    deslocado[1000:] += -0.001
    if not np.allclose(mudanca.deriva(3000, np.random.default_rng(41), passo=-0.001, quando=1000),
                       deslocado):
        problemas.append("a deriva não desloca a média no passo declarado")

    # --- o calendário (calendario.py) ---

    # com uma célula só, o vigia por célula É o vigia do capítulo anterior, alarme por alarme
    serie_cal = pd.Series(rng.normal(0.0, 0.01, 1500),
                          index=pd.date_range("2015-01-01", periods=1500, freq="D"))
    por_celula = calendario.vigia_por_celula(serie_cal, 252, calendario.unica)
    do_capitulo = vigia.dispara(serie_cal, 252, vigia.orcamento_minimo(252))
    if not (por_celula.index.equals(do_capitulo.index)
            and bool((por_celula.to_numpy() == do_capitulo.to_numpy()).all())):
        problemas.append("o vigia por célula não coincide com o vigia do capítulo anterior")

    # uma célula só não desenha calendário nenhum
    if calendario.amplitude(serie_cal, calendario.unica) != 0.0:
        problemas.append("amplitude com célula única deveria ser zero")

    # o orçamento por célula é o orçamento mínimo do capítulo anterior, com a memória dividida
    if abs(calendario.orcamento_por_celula(252, 1) - vigia.orcamento_minimo(252)) > 1e-15:
        problemas.append("orçamento por célula com uma célula não é o orçamento mínimo")
    if abs(calendario.orcamento_por_celula(252, 7) - 7 / 259) > 1e-15:
        problemas.append("orçamento por célula errado com sete células")

    # o que o calendário faz, medido num mundo de sete níveis: o vigia cru gasta os alarmes
    # no dia mais baixo da semana, e o vigia que lê o calendário não
    niveis = np.tile(np.arange(7, dtype=float) * 100.0, 300) + rng.normal(0.0, 1.0, 2100)
    com_calendario = pd.Series(niveis, index=pd.date_range("2015-01-05", periods=2100, freq="D"))
    cru = calendario.vigia_por_celula(com_calendario, 252, calendario.unica)
    semanal = calendario.vigia_por_celula(com_calendario, 252, calendario.semana)
    if cru.sum() == 0:
        problemas.append("o vigia cru não alarmou num mundo com sete níveis semanais")
    elif bool((cru.index[cru.to_numpy()].dayofweek != 0).any()):
        problemas.append("o vigia cru alarmou fora do dia mais baixo do calendário")
    if semanal.sum() == 0:
        problemas.append("o vigia que lê o calendário não alarmou no mundo de sete níveis")
    elif float((semanal.index[semanal.to_numpy()].dayofweek == 0).mean()) > 0.6:
        problemas.append("o vigia que lê o calendário continua preso a um dia da semana")

    # --- a partilha do relógio (partilha.py) ---

    # padronizar não olha para a frente: a escala de hoje sai só dos dias anteriores a hoje
    base_partilha = np.abs(rng.normal(0.0, 0.01, 800)) + 0.002
    mexida = base_partilha.copy()
    mexida[600] *= 7.0
    if partilha.padronizado(base_partilha, 21)[500] != partilha.padronizado(mexida, 21)[500]:
        problemas.append("padronizar olhou para a frente: mudar um dia futuro mudou o padrão de hoje")

    # uma série constante padroniza em um, e uma barreira em cima dela não deixa passar nada
    constante_partilha = np.full(900, 0.01)
    if not np.allclose(partilha.padronizado(constante_partilha, 21)[21:], 1.0):
        problemas.append("série constante deveria padronizar em um")
    if partilha.absorvido(constante_partilha, 1, 1, inicio=300, horizonte=100) != 0.0:
        problemas.append("barreira em cima de série constante deixou passar perda")

    # o ciclo é o horizonte dividido pelas atualizações, e zero atualizações é o horizonte inteiro
    if partilha.ciclos(25, 25, 500) != (20, 20):
        problemas.append("o ciclo não é o horizonte dividido pelas atualizações: %s"
                         % (partilha.ciclos(25, 25, 500),))
    if partilha.ciclos(0, 5, 500)[0] != 500:
        problemas.append("sem atualização, o ciclo da escala deveria ser o horizonte inteiro")
    if partilha.ciclos(500, 500, 500) != (1, 1):
        problemas.append("atualizar todo dia deveria dar ciclo um")

    # a partilha cobre todos os pares pedidos, e com uma série só a dispersão é zero
    uma = [np.abs(mudanca.degrau(4000, np.random.default_rng(91), fator=2.0, quando=1500))]
    medida = partilha.partilha(uma, (10,), (0.5, 1.0), inicio=1500, horizonte=200)
    if set(medida["media"]) != {(10, 0.5), (10, 1.0)}:
        problemas.append("a partilha não devolveu todos os pares pedidos")
    if any(v != 0.0 for v in medida["dispersao"].values()):
        problemas.append("com uma série só, a dispersão da partilha deveria ser zero")

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
