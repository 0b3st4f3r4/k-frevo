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

from . import (adaptativa, alerta, aposta, calendario, capacidade, cascata, centro, dados, dependencia, direcao, evidencia, esquecimento,
               estabilidade, graficos, intervencao, laco, lei, mudanca, multiplicidade, nivel, operador, partilha,
               pares, profundidade, proporcao, promessa, protecao, ramificacao, recorde, regimes, relogio,
                resumo, vigia, volatilidade)

# A versão tem uma fonte só, e ela é o pyproject.toml: duas cópias divergem, e a
# divergência é silenciosa. O fallback existe para o caso de o pacote ser lido da
# árvore de trabalho, sem instalação.
try:
    VERSAO = version("frevolab")
except PackageNotFoundError:
    VERSAO = "0.1.0"

__all__ = ["adaptativa", "alerta", "calendario", "capacidade", "cascata", "dados", "dependencia", "esquecimento", "estabilidade",
           "graficos", "intervencao", "laco", "lei", "mudanca", "nivel", "partilha", "pares", "profundidade",
           "proporcao", "protecao",
           "promessa", "ramificacao", "recorde", "regimes", "relogio", "resumo", "vigia", "volatilidade",
           "VERSAO", "auto_teste"]


def auto_teste() -> list:
    """Confere propriedades conhecidas de antemão. Devolve os problemas; vazio é limpo.

    Não é uma suíte de testes com arcabouço: são asserções de propriedade, do tipo que
    pega erro de sinal, de unidade e de eixo trocado — os três defeitos que uma figura
    bonita esconde.
    """
    import numpy as np
    import pandas as pd

    problemas = []

    # O criterio pelos autovalores e cego fora do caso simetrico: na familia de mesmo autovalor,
    # o caso diagonal tem as duas memorias iguais, e o acoplado tem pico maior que o prometido.
    serie_diagonal = operador.normas(0.0, 12)
    if abs(serie_diagonal[-1] - operador.RADIO_PADRAO ** 12) > 1e-12:
        problemas.append("operador: no caso diagonal a norma nao e raio^k")
    if operador.pico_da_norma(0.0, 12)[1] > 1.0 + 1e-12:
        problemas.append("operador: o caso diagonal nao tem pico")
    if not (operador.pico_da_norma(100.0, 40)[1] > operador.pico_da_norma(1.0, 40)[1] > 1.0):
        problemas.append("operador: o pico nao cresce com o acoplamento")
    if not (operador.memoria_da_norma(100.0) > operador.memoria_do_autovalor()):
        problemas.append("operador: o acoplado diz lembrar menos do que lembra")

    # A barra de uma comparacao nao e a barra da bateria: com quarenta, a chance de alguma
    # cruzar por acaso passa de 80%, e o quantil corrigido tem de ser maior que dois.
    if not (0.80 < multiplicidade.fwer_exata(40) < 0.90):
        problemas.append("multiplicidade: a conta da bateria de quarenta nao fecha")
    if not (multiplicidade.quantil_da_familia(40) > multiplicidade.INFLACAO_PADRAO > 1.9):
        problemas.append("multiplicidade: o quantil da familia nao e maior que a barra de uma")
    if multiplicidade.comparacoes() != multiplicidade.SINAIS_PADRAO * multiplicidade.FAIXAS_PADRAO:
        problemas.append("multiplicidade: a contagem de comparacoes nao bate")

    # A folga de uma explicacao e a distancia a fronteira da tolerancia, medida na unidade
    # dela: a que esta em 1 esta na borda, e a que esta em 0,5 tem metade do que se aceita.
    if not (0.0 <= evidencia.TOLERANCIA_PADRAO["taxa"] < 1.0):
        problemas.append("evidencia: a tolerancia da taxa nao esta na unidade declarada")
    if len(evidencia.CHAVES_PADRAO) != 4:
        problemas.append("evidencia: as quatro estatisticas do capitulo nao sao quatro")

    # Quem nunca esquece aprende cada vez mais devagar: a memoria da media acumulada e a idade
    # dela, e os dias para cruzar a tolerancia crescem com essa idade.
    if not (20.0 < esquecimento.dias_da_idade(21) < 30.0):
        problemas.append("esquecimento: a memoria da idade nao reproduz os vinte e um dias")
    if not (esquecimento.dias_da_idade(250) > esquecimento.dias_da_idade(50) > esquecimento.dias_da_idade(21)):
        problemas.append("esquecimento: os dias da idade nao crescem com ela")

    # A media acumulada nao esquece: no dia t o peso de cada dia e 1/t, e a estimativa demora a
    # reagir a uma mudanca que aconteceu ontem.
    degrau = np.concatenate([np.zeros(100), np.ones(100)])
    acumulada = esquecimento.media_acumulada(degrau)
    # Devagar quer dizer: dois dias depois do degrau ela ainda esta abaixo de um vigesimo do
    # caminho, e cem dias depois nao chegou a metade. A desigualdade anterior estava invertida.
    if not (acumulada[101] < 0.05 and acumulada[-1] < 0.6 < 1.0):
        problemas.append("esquecimento: a media acumulada nao reage devagar ao degrau")

    # A contagem de explicacoes que cabem e um MAXIMO sobre a familia: ela cresce com o numero
    # de pecas tentadas e cai com o numero de dias vistos.
    if len(evidencia.GRADE_P_PADRAO) * len(evidencia.GRADE_RAZAO_PADRAO) != 36:
        problemas.append("evidencia: a grade padrao deixou de ser seis por seis")

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

    # o piso do atraso é o limiar menos um: o dia da mudança conta zero
    if vigia.piso_de_atraso(13) != 12:
        problemas.append("o piso de atraso não é o limiar menos um (13 -> 12)")
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

    # --- a direção da queda conjunta (dependencia.py) ---

    # quem rompe primeiro: uma perna na frente, a outra atrás dentro da janela
    indices = pd.RangeIndex(200)
    forjado_a = pd.Series(np.zeros(200, dtype=bool), index=indices)
    forjado_b = pd.Series(np.zeros(200, dtype=bool), index=indices)
    forjado_a.iloc[50] = True
    forjado_b.iloc[52] = True
    dirigido = dependencia.episodios_dirigidos(forjado_a, forjado_b, 5)
    if (dirigido["lider_a"], dirigido["lider_b"]) != (1, 0):
        problemas.append("o episódio dirigido não achou a perna que rompeu primeiro")

    # rompimento no mesmo dia não é episódio de ninguém
    forjado_b.iloc[52] = False
    forjado_b.iloc[50] = True
    no_mesmo_dia = dependencia.episodios_dirigidos(forjado_a, forjado_b, 5)
    if (no_mesmo_dia["lider_a"], no_mesmo_dia["lider_b"], no_mesmo_dia["juntos"]) != (0, 0, 1):
        problemas.append("rompimento no mesmo dia virou episódio de um dos lados")

    # a outra perna fora da janela não fecha episódio nenhum: fica sozinho
    forjado_b.iloc[50] = False
    forjado_b.iloc[60] = True
    sozinho = dependencia.episodios_dirigidos(forjado_a, forjado_b, 5)
    if (sozinho["lider_a"], sozinho["sozinho_a"]) != (0, 1):
        problemas.append("a perna que rompeu fora da janela não ficou sozinha")

    # O relógio da espera reinicia quando um episódio COMEÇA, e não a cada rompimento. As três
    # séries abaixo separam as duas regras: com o rompimento do meio contando, o episódio de 58
    # não abriria, e o instrumento mediria um episódio onde mede dois. A regra já foi escrita
    # errada na docstring e no capítulo, e é esta asserção que impede a volta.
    forjado_b.iloc[60] = False
    forjado_a.iloc[50] = True
    forjado_a.iloc[54] = True
    forjado_a.iloc[58] = True
    seguidos = dependencia.episodios_dirigidos(forjado_a, forjado_b, 5)
    if seguidos["sozinho_a"] != 2:
        problemas.append("o relógio da espera reinicia a cada rompimento, e não a cada episódio: "
                         "com a regra escrita o instrumento mediria um episódio aqui, e não dois")

    # --- o recorde e o mundo que faltou (recorde.py) ---

    # a soma das duas chances é um: o maior valor do conjunto está de um lado ou do outro
    if abs(recorde.probabilidade(252, 252) - 0.5) > 1e-15:
        problemas.append("um ano de histórico contra um ano por vir deveria dar meio")
    if abs(recorde.probabilidade(100, 30) + recorde.probabilidade(30, 100) - 1.0) > 1e-15:
        problemas.append("as duas chances de recorde não somam um")
    if abs(recorde.do_proximo(100) - 1.0 / 101) > 1e-15:
        problemas.append("a chance do próximo dia superar o recorde não é 1/(n+1)")

    # o harmônico: um recorde no primeiro dia, e o logaritmo no limite
    if recorde.esperado(1) != 1.0:
        problemas.append("um dia deveria dar um recorde esperado")
    if abs(recorde.esperado(1000) - 7.4855) > 0.001:
        problemas.append("o número esperado de recordes em mil dias não é o harmônico")

    # os recordes fazem o que dizem: série crescente marca todos, série constante marca um
    if not recorde.recordes(np.arange(50.0)).all():
        problemas.append("série estritamente crescente deveria marcar todos os dias como recorde")
    if recorde.conta(np.full(500, 7.0)) != 1:
        problemas.append("série constante deveria ter um único recorde")

    # o que o futuro fez contra o passado: com o futuro todo acima, a fração é um
    cedo = np.linspace(0.0, 1.0, 100)
    tarde = np.linspace(2.0, 3.0, 100)
    faltou_teste = recorde.faltou(cedo, tarde)
    if abs(faltou_teste["fracao"] - 1.0) > 1e-15 or abs(faltou_teste["razao"] - 3.0) > 1e-15:
        problemas.append("o futuro todo acima do passado deveria dar fração um e razão três")

    # a conta conferida por sorteio, no tamanho em que ela é verificável à mão
    venceu = 0
    for i in range(2000):
        s_ = np.random.default_rng(9000 + i)
        if s_.normal(0.0, 1.0, 60).max() > s_.normal(0.0, 1.0, 60).max():
            venceu += 1
    if not 0.44 < venceu / 2000.0 < 0.56:
        problemas.append("a chance de recorde medida por sorteio saiu de meio (%.3f)"
                         % (venceu / 2000.0))

    # --- o passado apagado (esquecimento.py, mudanca.py) ---

    # o processo que lembra com decaimento tem a dispersão estacionária que declara
    ar_um = mudanca.ar1(20000, np.random.default_rng(31), 0.9, 1.0)
    esperado_ar = 1.0 / np.sqrt(1.0 - 0.9 ** 2)
    if abs(ar_um.std(ddof=1) - esperado_ar) / esperado_ar > 0.05:
        problemas.append("o processo AR(1) não tem a dispersão estacionária declarada (%.3f contra %.3f)"
                         % (ar_um.std(ddof=1), esperado_ar))

    # sem ruído, o mapa inverso recupera exatamente
    geometrica = 0.9 ** np.arange(200, dtype=float)
    if not np.allclose(esquecimento.reverter(geometrica, 0.9, 7), geometrica / 0.9 ** 7):
        problemas.append("o mapa inverso não desfez o decaimento geométrico")

    # as duas fórmulas de erro: uma explode, a outra para na dispersão do processo
    if abs(esquecimento.erro_do_inverso(0.5, 1, 1.0) - 2.0) > 1e-12:
        problemas.append("o erro do inverso em um passo não é 1/a")
    sigma_ar = 1.0 / np.sqrt(1.0 - 0.5 ** 2)
    if esquecimento.erro_do_otimo(0.5, 10 ** 6, 1.0) > sigma_ar:
        problemas.append("o erro ótimo passou da dispersão do processo")
    if not esquecimento.erro_do_otimo(0.5, 3, 1.0) > esquecimento.erro_do_otimo(0.5, 1, 1.0):
        problemas.append("o erro ótimo não cresce com os dias para trás")

    # o horizonte cresce com a tolerância e com a memória do processo
    if not esquecimento.horizonte(0.9, 0.9) > esquecimento.horizonte(0.9, 0.5):
        problemas.append("afrouxar a tolerância não esticou o horizonte de recuperação")
    if not esquecimento.horizonte(0.99, 0.5) > esquecimento.horizonte(0.5, 0.5):
        problemas.append("um processo com mais memória não recuperou por mais dias")

    # as duas fórmulas conferidas por sorteio, no caso em que a mão confere
    erros_inv, erros_otm = [], []
    for i in range(60):
        x_ = mudanca.ar1(4000, np.random.default_rng(500 + i), 0.8, 1.0)
        k_ = 5
        erros_inv.append(np.sqrt(np.mean((esquecimento.reverter(x_[k_:], 0.8, k_) - x_[:-k_]) ** 2)))
        erros_otm.append(np.sqrt(np.mean((0.8 ** k_ * x_[k_:] - x_[:-k_]) ** 2)))
    if abs(np.mean(erros_inv) - esquecimento.erro_do_inverso(0.8, 5, 1.0)) / esquecimento.erro_do_inverso(0.8, 5, 1.0) > 0.1:
        problemas.append("o erro do inverso medido não bate com a fórmula")
    if abs(np.mean(erros_otm) - esquecimento.erro_do_otimo(0.8, 5, 1.0)) / esquecimento.erro_do_otimo(0.8, 5, 1.0) > 0.1:
        problemas.append("o erro ótimo medido não bate com a fórmula")

    # --- o segundo momento contra a cauda (mudanca.py) ---

    # com p = 0 o par de cauda é o par gaussiano de sempre
    gauss_a, gauss_b = mudanca.par_de_cauda(40000, np.random.default_rng(77), 1.0, 0.5, 0.0)
    if abs(np.corrcoef(gauss_a, gauss_b)[0, 1] - 0.5) > 0.03:
        problemas.append("o par de cauda sem choque não tem a correlação declarada")

    # com choque comum a correlação continua a mesma e a cauda marginal engorda
    cauda_a, cauda_b = mudanca.par_de_cauda(40000, np.random.default_rng(78), 1.0, 0.5, 0.05, 3.0)
    if abs(np.corrcoef(cauda_a, cauda_b)[0, 1] - 0.5) > 0.03:
        problemas.append("o choque comum mexeu na correlação, que devia ficar declarada")
    curtose_gauss = float(((gauss_a / gauss_a.std(ddof=1)) ** 4).mean())
    curtose_cauda = float(((cauda_a / cauda_a.std(ddof=1)) ** 4).mean())
    if not curtose_cauda > 1.5 * curtose_gauss:
        problemas.append("o choque comum não engrossou a cauda marginal (%.2f contra %.2f)"
                         % (curtose_cauda, curtose_gauss))

    # --- o pedaço escolhido (estabilidade.py) ---

    # pedaços sem sobreposição cabem na série, e o último fecha dentro dela
    fatias = estabilidade.janelas(1000, 250)
    if len(fatias) != 4 or fatias[-1].stop > 1000:
        problemas.append("as janelas sem sobreposição não cobrem a série como deviam")
    if len(estabilidade.janelas(1000, 250, 100)) != 8:
        problemas.append("as janelas com passo não são as que o passo declara")

    # a mesma pergunta em cada pedaço: série constante dá respostas constantes
    constante_janela = pd.Series(np.full(1000, 3.0))
    respostas_constantes = estabilidade.por_janela(constante_janela, lambda p: float(p.mean()), 250)
    if not np.allclose(respostas_constantes, 3.0):
        problemas.append("a mesma pergunta em cada pedaço não devolveu o mesmo numa série constante")
    resumo_constante = estabilidade.resumo(respostas_constantes, 3.0, 0.01)
    if resumo_constante["dispersao"] != 0.0 or resumo_constante["fora_da_banda"] != 0.0:
        problemas.append("respostas constantes deveriam dar dispersão zero e nada fora da banda")

    # a banda independente cai com a raiz do número de dias
    if abs(estabilidade.banda_independente(0.05, 400) * 2
           - estabilidade.banda_independente(0.05, 100)) > 1e-15:
        problemas.append("a banda independente não segue a lei da raiz do número de dias")

    # --- o agora (promessa.py) ---

    # com atraso zero, o corte atrasado é o corte do primeiro capítulo
    serie_atraso = pd.Series(rng.normal(0.0, 0.01, 2000))
    if not (promessa.violacoes_atrasadas(serie_atraso, 252, 0.05, 0)
            .equals(promessa.violacoes(serie_atraso, 252, 0.05))):
        problemas.append("o corte com atraso zero não é o corte do primeiro capítulo")

    # num mundo que não muda, o atraso não mexe na taxa entregue
    taxas_atraso = [promessa.violacoes_atrasadas(serie_atraso, 252, 0.05, d).mean()
                    for d in (0, 1, 5, 21, 63)]
    if max(taxas_atraso) - min(taxas_atraso) > 0.01:
        problemas.append("num mundo parado o atraso mexeu na taxa entregue (%.4f a %.4f)"
                         % (min(taxas_atraso), max(taxas_atraso)))
    try:
        promessa.violacoes_atrasadas(serie_atraso, 252, 0.05, -1)
        problemas.append("o corte atrasado aceitou atraso negativo")
    except ValueError:
        pass

    # o salvamento grava os dois formatos
    import tempfile
    from pathlib import Path

    # --- centro: o instrumento de outra forma, e ele tem de ser cego à escala ---
    base = pd.Series(np.random.default_rng(11).normal(0.0, 0.01, 400))
    t_um = centro.media_padronizada(base, 60)
    t_dois = centro.media_padronizada(base * 2.0, 60)
    if not np.allclose(t_um.dropna().to_numpy(), t_dois.dropna().to_numpy()):
        problemas.append("o centro mudou quando a escala do mundo dobrou: ele não é cego à escala")
    if int(t_um.notna().to_numpy().argmax()) != 59:
        problemas.append("a janela do centro não vale para trás: ela não começa onde devia")
    if not np.isnan(centro.media_padronizada(pd.Series(np.full(120, 0.01)), 60).to_numpy()[-1]):
        problemas.append("janela sem barulho devolveu número: não há erro-padrão por onde medir o centro")
    nulo = np.abs(t_um.dropna().to_numpy())
    if centro.limiar_do_orcamento(nulo, 0.10) > centro.limiar_do_orcamento(nulo, 0.05):
        problemas.append("o limiar do centro não é monótono no orçamento")

    # --- regimes: a família do capítulo 8 ---
    real = {"taxa": 0.05, "pior": 20.0, "mediana": 3.0, "acima_do_dobro": 0.10}
    tol = {"taxa": 0.002, "pior": 2.0, "mediana": 1.0, "acima_do_dobro": 0.03}
    if len(regimes.cabem([{"estatisticas": dict(real)}], real, tol, ("pior",))) != 1:
        problemas.append("um membro idêntico ao dado não caberia na tolerância")
    if len(regimes.cabem([{"estatisticas": {**real, "pior": 22.0}}], real, tol, ("pior",))) != 1:
        problemas.append("a tolerância do pior bloco excluiu o próprio limite: ela é fechada")
    if regimes.cabem([{"estatisticas": {**real, "pior": 22.5}}], real, tol, ("pior",)):
        problemas.append("a tolerância aceitou um membro que está fora dela")
    sem = regimes.persistente(20000, np.random.default_rng(7), 0.01, 0.08, 3.0, permanencia=1.0)
    com = regimes.persistente(20000, np.random.default_rng(7), 0.01, 0.08, 3.0, permanencia=320.0)
    ac_um = float(np.corrcoef(np.abs(sem[:-1]), np.abs(sem[1:]))[0, 1])
    ac_muito = float(np.corrcoef(np.abs(com[:-1]), np.abs(com[1:]))[0, 1])
    if not ac_um < 0.05:
        problemas.append("com permanência de um dia o regime ainda encadeia (%.3f)" % ac_um)
    if not ac_muito > 0.15:
        problemas.append("com permanência longa o regime não encadeia (%.3f)" % ac_muito)

    # --- regimes: a projecao em divergencia escolhe o que a tolerancia nao escolhe ---
    membro_a = np.array([0.7, 0.2, 0.1, 0.0])
    membro_b = np.array([0.1, 0.3, 0.2, 0.4])
    mistura = 0.4 * membro_a + 0.6 * membro_b
    if abs(regimes.divergencia(mistura, mistura)) > 1e-15:
        problemas.append("divergencia: a divergencia de uma lei consigo nao e zero")
    if regimes.divergencia(np.array([1.0, 0.0]), np.array([0.0, 1.0])) != np.inf:
        problemas.append("divergencia: massa fora do suporte nao devolve infinito")
    achado = regimes.projecao(mistura, np.vstack([membro_a, membro_b]), passos=800)
    if abs(achado["divergencia"]) > 1e-6:
        problemas.append("projecao: uma lei da envoltoria nao projeta nela mesma (%.2e)"
                         % achado["divergencia"])
    vizinho = np.array([0.9, 0.05, 0.05, 0.0])
    outra = regimes.projecao(vizinho, np.vstack([membro_a, membro_b]), passos=800)
    pythagoras = (regimes.divergencia(vizinho, mistura)
                  - outra["divergencia"] - regimes.divergencia(outra["lei"], mistura))
    if pythagoras < -1e-6:
        problemas.append("projecao: a desigualdade de Pitagoras nao fecha (%.2e)" % pythagoras)
    # --- direcao: o instrumento da seta do tempo ---
    if abs(direcao.desvio_da_conta(252) - np.sqrt(15.0 / 252.0)) > 1e-12:
        problemas.append("o desvio da conta da direção não é raiz de 15 sobre a janela")
    passos = np.random.default_rng(11).normal(0.0, 0.01, 5000)
    ida = direcao.momento_amostral(passos)["momento"]
    volta = direcao.momento_amostral(direcao.invertida(passos))["momento"]
    if abs(ida + volta) > 1e-9:
        problemas.append("inverter o relógio não trocou o sinal da direção")
    if abs(ida - volta) < 1e-6:
        problemas.append("inverter o relógio trocou o tamanho da direção, e ele devia ficar")
    quantos = direcao.blocos(passos, 252).size
    if quantos != passos.size // 252 - 1:
        problemas.append("os blocos da direção não são sem sobreposição (%d para %d esperados)"
                         % (quantos, passos.size // 252 - 1))

    # --- intervencao: o desenho experimental do capítulo 11 ---
    from statistics import NormalDist as _NormalDist
    zeta = _NormalDist().inv_cdf(1.0 - (1.0 - intervencao.CONFIANCA) / 2.0)
    if abs(intervencao.replicatas_necessarias(0.20, 0.50) - (zeta * 0.50 / 0.20) ** 2) > 1e-9:
        problemas.append("a conta do tamanho da amostra não é (z s / d) ao quadrado")
    if abs(intervencao.custo(7.7, 80, 20) - 7.7 * 100.0) > 1e-9:
        problemas.append("o custo não é replicatas vezes (contenção mais espera)")
    sopro = intervencao.serie("memoria", 8000, np.random.default_rng(5), 0.01)
    variancia = float(sopro[intervencao.AQUECIMENTO:].var())
    if not 0.75 * 1e-4 < variancia < 1.25 * 1e-4:
        problemas.append("a variância de repouso do mundo de memória não é sigma ao quadrado (%.6f)" % variancia)

    # --- segunda passada: asserções de VALOR onde a primeira media propriedade fraca ---
    # Uma auditoria independente mutou cada função pública para uma versão plausivelmente errada e
    # achou 21 mutações que quebravam a matemática sem que o auto_teste acusasse. Cada linha abaixo
    # é uma delas, e cada uma foi conferida por mutação depois de escrita.

    # o posto do orçamento: o único ponto testado era 1/253, onde 'ceil' e 'floor' coincidem --- e o
    # piso promete MAIS do que o orçamento declarado, que é o oposto da promessa do módulo
    if vigia.posto_do_orcamento(252, 2.5 / 253.0) != 3:
        problemas.append("o posto do orçamento não arredonda para cima: ele entregaria mais do que o declarado")

    # a amplitude do calendário: só era medida com uma célula, onde toda implementação dá zero
    serie_amp = pd.Series(np.abs(np.random.default_rng(3).normal(0.0, 0.01, 3000)),
                          index=pd.date_range("2015-01-01", periods=3000, freq="D"))
    if not calendario.amplitude(serie_amp, calendario.semana) > calendario.amplitude(serie_amp, calendario.unica):
        problemas.append("a amplitude da semana não passa a de uma célula só: a partição não move nada")

    # padronizar olhando para a frente: a perturbação estava a cem dias da leitura e não podia ver.
    # As duas metades juntas são o teste --- uma sozinha não distingue a janela de trás da da frente.
    base_pad = np.abs(np.random.default_rng(4).normal(0.0, 0.01, 4000))
    dentro = base_pad.copy()
    dentro[490] *= 7.0
    depois = base_pad.copy()
    depois[521] *= 7.0
    referencia = partilha.padronizado(base_pad, 21)[500]
    if partilha.padronizado(dentro, 21)[500] == referencia:
        problemas.append("perturbar um dia dentro da janela não mudou a estatística: ela não olha os dias de trás")
    if partilha.padronizado(depois, 21)[500] != referencia:
        problemas.append("perturbar um dia depois da janela mudou a estatística: ela olha para a frente")

    # a proposição do esquecimento, que o próprio módulo declara conferida aqui e não era
    degrau = np.concatenate([np.zeros(60), np.ones(120)])
    taxa_esq = 1.0 / 21.0
    desvio_degrau = np.abs(esquecimento.exponencial(degrau, taxa_esq)[60:] - 1.0)
    # O expoente e t+1, e nao t: o estimador ja carrega o dia anterior no dia da mudanca.
    # A forma ingenua passou por aqui e foi reprovada pela propria assercao.
    if not np.allclose(desvio_degrau, (1.0 - taxa_esq) ** (np.arange(120) + 1), rtol=1e-9):
        problemas.append("o desvio da mistura exponencial não decai como (1 - taxa) elevado a t")
    if abs(esquecimento.dias_para_tolerancia(taxa_esq, 0.15) - np.log(0.15) / np.log(1.0 - taxa_esq)) > 1e-12:
        problemas.append("os dias até a tolerância não são log(eps) sobre log(1 - taxa)")
    # A tolerância do capítulo 13 tinha DUAS unidades com o mesmo 0,15: a do nível, que o erro
    # medido usa, e a do degrau, que a proposição usa. Num mundo que dobra, 0,15 do nível é 0,30 do
    # degrau — e enquanto isso não esteve separado, a prosa dizia uma unidade e o critério media na
    # outra. Estas três asserções fixam a ponte: a conversão, a conta dos dias em degraus, e o
    # caminho que a viabilidade percorre.
    if abs(esquecimento.TOLERANCIA_DEGRAU - 0.30) > 1e-12:
        problemas.append("0,15 do nível não virou 0,30 do degrau no mundo que dobra")
    if abs(esquecimento.dias_para_tolerancia(taxa_esq)
           - np.log(esquecimento.TOLERANCIA_DEGRAU) / np.log(1.0 - taxa_esq)) > 1e-12:
        problemas.append("o padrão dos dias até a tolerância não é a tolerância em degraus")
    aprendido = esquecimento.limiar([degrau], [0.2], degrau, 60, 120,
                                    tolerancia_nivel=esquecimento.TOLERANCIA)
    if abs(aprendido["tolerancia_degrau"] - esquecimento.TOLERANCIA_DEGRAU) > 1e-12:
        problemas.append("a viabilidade converte a tolerância do nível para o degrau errado")
    if abs(aprendido["dias_previstos"]
           - esquecimento.dias_para_tolerancia(0.2, esquecimento.TOLERANCIA_DEGRAU)) > 1e-12:
        problemas.append("os dias previstos da viabilidade não usam a tolerância em degraus")
    if abs(esquecimento.horizonte(0.99, 0.5) - np.log(1.0 - 0.25) / (2.0 * np.log(0.99))) > 1e-9:
        problemas.append("o horizonte de recuperação não é log(1 - t ao quadrado) sobre 2 log a")

    # a taxa da entrega nunca era lida, e é ela que separa a média da conta assinada
    entrega_curta = promessa.entrega(pd.Series(np.random.default_rng(6).normal(0.0, 0.01, 600)), 21, bloco=60)
    if abs(entrega_curta["taxa"] - entrega_curta["violacoes"] / entrega_curta["dias"]) > 1e-12:
        problemas.append("a taxa da entrega não é a razão entre violações e dias")

    # a dispersão entre pedaços: era conferida com valores idênticos, onde o ddof não existe
    if abs(estabilidade.resumo(np.array([1.0, 2.0, 3.0, 4.0]), 2.5, 1.0)["dispersao"]
           - np.std([1.0, 2.0, 3.0, 4.0], ddof=1)) > 1e-12:
        problemas.append("a dispersão entre pedaços não usa o desvio de amostra")

    # os ciclos da partilha: os três casos testados dividiam exatamente, onde truncar dá o mesmo
    if partilha.ciclos(3, 7, 500) != (167, 71):
        problemas.append("os ciclos da partilha não arredondam para o mais próximo")

    # --- nivel: as porcentagens não se somam, e o desvio do nível cresce com a raiz ---
    # O caso mínimo, escrito à mão: cem desce a noventa e cinco e volta a cem. As porcentagens
    # não somam zero (-5% e +5,26% dão +0,26%), e os logaritmos somam exatamente zero.
    desce_e_volta = np.array([-0.05, 0.05 / 0.95])
    if abs(nivel.soma_das_variacoes(desce_e_volta) - 0.002631578947368421) > 1e-12:
        problemas.append("a soma das porcentagens não dá o resíduo esperado na ida e volta")
    if abs(nivel.soma_dos_logs(np.log1p(desce_e_volta))) > 1e-15:
        problemas.append("o logaritmo não soma zero na ida e volta")
    if abs(nivel.produto_das_variacoes(desce_e_volta)) > 1e-15:
        problemas.append("o produto das variações não devolve o lugar")
    # as três contas do pedaço, juntas: a variação real e a soma dos logaritmos fecham em zero,
    # e a soma das porcentagens não fecha.
    contas = nivel.contas_do_pedaco([100.0, 95.0, 100.0])
    if abs(contas["variação real (%)"]) > 1e-12 or abs(contas["soma dos logaritmos (%)"]) > 1e-12:
        problemas.append("a ida e volta não fecha em zero na variação real e nos logaritmos")
    if abs(contas["soma das porcentagens (%)"] - 0.2631578947368421) > 1e-10:
        problemas.append("a soma das porcentagens não dá o resíduo esperado no pedaço de teste")
    # a previsão da raiz, no caso em que ela é exata, e contra a dispersão medida em mundos.
    if abs(nivel.desvio_do_nivel(0.01, 252) - 0.01 * np.sqrt(252)) > 1e-15:
        problemas.append("o desvio do nível não é o desvio de um dia vezes a raiz dos dias")
    sorteio_nivel = np.random.default_rng(20260924)
    medido_nivel = float(nivel.mundos_do_passeio(0.01213, 252, 4000, sorteio_nivel).std(ddof=1))
    previsto_nivel = nivel.desvio_do_nivel(0.01213, 252)
    if abs(medido_nivel - previsto_nivel) / previsto_nivel > 0.15:
        problemas.append("a dispersão do nível entre mundos sorteados não bate com a raiz "
                         "(medido %.5f, previsto %.5f)" % (medido_nivel, previsto_nivel))

    # --- nivel: a inclinação da banda em toda escala, o mesmo instrumento nos dois lados ---
    # No passeio gaussiano o expoente do caminho é meio (a banda cresce com a raiz) e a
    # dimensão, três meios, dentro da tolerância medida e declarada; na reta o expoente é
    # um, e na série plana, zero. No mundo antipersistente o expoente fica abaixo do
    # expoente baralhado da mesma série: é a ordem, e não a cauda, que a faixa curta mede.
    rng_e44 = np.random.default_rng(11)
    atrasos_e44 = (1, 2, 4, 8, 16, 32, 64, 128, 256)
    gamas_e44 = [nivel.expoente_do_caminho(np.exp(rng_e44.normal(0.0, 0.01, 20000).cumsum()),
                                           atrasos_e44, 30) for _ in range(4)]
    if not all(abs(g - 0.5) < 0.06 for g in gamas_e44):
        problemas.append("nivel: o expoente do passeio não dá meio (%s)"
                         % np.round(gamas_e44, 4))
    if abs(nivel.dimensao_do_caminho(np.exp(rng_e44.normal(0.0, 0.01, 20000).cumsum()),
                                     atrasos_e44, 30) - 1.5) > 0.06:
        problemas.append("nivel: a dimensão do passeio não dá três meios")
    if abs(nivel.expoente_do_caminho(np.exp(0.001 * np.arange(4000)), atrasos_e44, 30)
           - 1.0) > 1e-9:
        problemas.append("nivel: o expoente da reta não dá um")
    if nivel.expoente_do_caminho(np.full(4000, 100.0), atrasos_e44, 30) != 0.0:
        problemas.append("nivel: o expoente da série plana não dá zero")
    ruido_e44 = rng_e44.normal(0.0, 0.01, 20000)
    anti_e44 = ruido_e44[1:] - 0.5 * ruido_e44[:-1]
    if not (nivel.expoente_do_caminho(np.exp(np.concatenate([[0.0], anti_e44.cumsum()])),
                                      atrasos_e44, 30)
            < nivel.expoente_do_baralhado(anti_e44, atrasos_e44, 8,
                                          np.random.default_rng(31), 30)["media"]):
        problemas.append("nivel: o mundo antipersistente não fica abaixo do baralhado")

    # --- proporcao: a barra da média de muitos sorteios ---
    # A previsão da proposição, no caso em que ela é exata: a barra de uma moeda em cem
    # sorteios é 0,05, e não "aproximadamente 0,05".
    if abs(proporcao.barra(0.5, 100) - 0.05) > 1e-12:
        problemas.append("a barra da fração não é a raiz de p(1-p)/n")
    # e a barra tem de bater com a dispersão MEDIDA: é essa a propriedade que o capítulo usa,
    # e uma barra que só fecha na álgebra não serve para medir nada.
    sorteio = np.random.default_rng(20260924)
    medido = proporcao.mundos(0.5, 252, 4000, sorteio).std(ddof=1)
    previsto = proporcao.barra(0.5, 252)
    if abs(medido - previsto) / previsto > 0.15:
        problemas.append("a dispersão entre mundos sorteados não bate com a barra prevista "
                         "(medido %.5f, previsto %.5f)" % (medido, previsto))
    # a fração de uma série constante é um, e a de uma série que só cai é zero: sem isto, um
    # erro de sinal em indicadores passaria por média.
    if proporcao.fracao(np.array([1.0, 2.0, 3.0])) != 1.0 or proporcao.fracao(np.array([-1.0, -2.0])) != 0.0:
        problemas.append("o indicador do dia trocou de sinal")
    if abs(proporcao.janelas(np.arange(1.0, 11.0), 3).mean() - 1.0) > 1e-12:
        problemas.append("as janelas móveis não reproduzem a fração da série constante")

    # --- proporcao: a barra que a amostra ergue sozinha, sem lei e sem mundo novo ---
    rng_boot = np.random.default_rng(20260925)
    dias_boot = (rng_boot.random(252) < 0.3).astype(float)
    fracoes_boot = proporcao.reamostragens(dias_boot, 500, rng_boot)
    if abs(float(fracoes_boot.mean()) - float(dias_boot.mean())) > 0.01:
        problemas.append("reamostragens: a urna com reposicao nao centra na amostra")
    sem_boot = np.array([float(rng_boot.permutation(dias_boot).mean()) for _ in range(40)])
    if float(sem_boot.std()) > 1e-12:
        problemas.append("reamostragens: o controle sem reposicao nao colapsa")
    baixo_boot, alto_boot = proporcao.barra_reamostrada(dias_boot, 0.90, 2000, rng=rng_boot)
    if not baixo_boot < 0.3 < alto_boot:
        problemas.append("barra_reamostrada: a barra de 90 por cento nao contem a verdade iid "
                         "(%.4f, %.4f)" % (baixo_boot, alto_boot))
    blocos_boot = np.concatenate([np.full(60, float(rng_boot.random() < 0.3))
                                  for _ in range(10)])
    par_dia = proporcao.barra_reamostrada(blocos_boot, 0.90, 1000, rng=rng_boot)
    par_bloco = proporcao.barra_reamostrada(blocos_boot, 0.90, 1000, rng=rng_boot, bloco=60)
    largura_dia_boot = 100 * (par_dia[1] - par_dia[0])
    largura_bloco_boot = 100 * (par_bloco[1] - par_bloco[0])
    if not largura_bloco_boot > 1.5 * largura_dia_boot:
        problemas.append("barra_reamostrada: a barra de blocos nao e mais larga que a de dias "
                         "(%.3f contra %.3f pp)" % (largura_bloco_boot, largura_dia_boot))
    mundos_boot = np.vstack([(rng_boot.random(252) < 0.3).astype(float) for _ in range(60)])
    cobertura_boot = proporcao.cobertura(mundos_boot, 0.3, 0.90, 300, rng=rng_boot)
    if abs(cobertura_boot - 0.90) > 0.15:
        problemas.append("cobertura: a barra de 90 por cento cobre %.2f nos mundos iid"
                         % cobertura_boot)
    # --- o resumo e o teto dos bits (resumo.py) ---

    # O esboco compra o segundo momento: sem vies, com erro que cai com a raiz do numero de
    # contadores, e cego a ordem --- a energia de um fluxo embaralhado e a mesma.
    fluxo = np.array([0.01, -0.02, 0.03, 0.015, -0.005])
    exato = resumo.energia(fluxo)
    if abs(exato - float(np.dot(fluxo, fluxo))) > 1e-15:
        problemas.append("resumo: a energia nao e a soma dos quadrados")
    media = float(np.mean([resumo.esboco(fluxo, 400, np.random.default_rng(s))["estimativa"]
                           for s in range(200)]))
    if abs(media - exato) / exato > 0.05:
        problemas.append("resumo: o esboco tem vies (%.5f contra %.5f)" % (media, exato))
    if resumo.contadores_para(0.10) != 200 or resumo.contadores_para(0.01) != 20000:
        problemas.append("resumo: a conta do preco nao fecha")
    if abs(resumo.previsao(400) - 0.0707106781) > 1e-9:
        problemas.append("resumo: a previsao do erro nao e a raiz de 2/k")
    pequeno = resumo.varredura(fluxo, 100, 40, np.random.default_rng(11))["erro_medio"]
    grande = resumo.varredura(fluxo, 400, 40, np.random.default_rng(11))["erro_medio"]
    if not (pequeno > grande > 0.0):
        problemas.append("resumo: o erro nao cai com o numero de contadores")
    if abs(resumo.energia(fluxo[::-1]) - exato) > 1e-15:
        problemas.append("resumo: a energia mudou com a ordem, e ela nao deveria")

    # --- os pares de dias e o preco de conta-los (pares.py) ---

    # Num par perfeitamente ordenado a concordancia e um, no invertido e menos um, e a contagem de
    # pares dos dias do capitulo e um numero fechado.
    ordenado = pd.Series(np.arange(120.0))
    if abs(pares.concordancia(ordenado, ordenado * 2.0 + 1.0)["tau"] - 1.0) > 1e-12:
        problemas.append("pares: o par ordenado nao da concordancia um")
    if abs(pares.concordancia(ordenado, -ordenado)["tau"] + 1.0) > 1e-12:
        problemas.append("pares: o par invertido nao da concordancia menos um")
    if pares.pares(6204) != 19241706:
        problemas.append("pares: a contagem de pares dos dias do capitulo nao fecha")

    # E a lei da barra se confere medindo: com quatro vezes mais pares, o desvio cai pela metade.
    rng_pares = np.random.default_rng(97)
    eixo = pd.RangeIndex(300)
    um = pd.Series(rng_pares.normal(0.0, 0.01, 300), index=eixo)
    outro = pd.Series(0.6 * um.to_numpy() + rng_pares.normal(0.0, 0.01, 300), index=eixo)
    perto = float(np.std([pares.concordancia_amostrada(um, outro, 500, rng_pares)["tau"]
                          for _ in range(60)], ddof=1))
    longe = float(np.std([pares.concordancia_amostrada(um, outro, 2000, rng_pares)["tau"]
                          for _ in range(60)], ddof=1))
    if not (1.4 < perto / longe < 2.8):
        problemas.append("pares: o desvio medido nao cai com a raiz do numero de pares "
                         "(%.5f contra %.5f)" % (perto, longe))

    # --- a aposta e o orcamento que sobrevive a ser lido sempre (aposta.py) ---

    # Um bloco do mundo parado vale um em media: e essa a martingala que o capital usa.
    rng_aposta = np.random.default_rng(2026)
    bloco_unico = rng_aposta.binomial(60, 0.05, size=20000)
    media_razao = float(aposta.razao(bloco_unico, 60).mean())
    if abs(media_razao - 1.0) > 0.03:
        problemas.append("aposta: um bloco do mundo parado nao vale um em media (%.4f)" % media_razao)
    # E a desigualdade de Ville e respeitada: o mundo parado cruza um sobre alfa em no maximo alfa.
    caminhos_aposta = aposta.capital(rng_aposta.binomial(60, 0.05, size=(2000, 60)), 60, eixo=1)
    if float((caminhos_aposta.max(axis=1) >= aposta.orcamento_de_ville(0.05)).mean()) > 0.05:
        problemas.append("aposta: o mundo parado cruza o limiar de Ville demais")
    if abs(aposta.orcamento_de_ville(0.05) - 20.0) > 1e-12:
        problemas.append("aposta: o orcamento de Ville nao e um sobre alfa")
    # E o capital cresce no mundo que muda: com a taxa dobrada, a maioria dos mundos cruza.
    mudados_aposta = np.concatenate([rng_aposta.binomial(60, 0.05, size=(2000, 30)),
                                     rng_aposta.binomial(60, 0.10, size=(2000, 30))], axis=1)
    if float((aposta.capital(mudados_aposta, 60, eixo=1)[:, -1] >= 20).mean()) < 0.5:
        problemas.append("aposta: o capital nao cresce no mundo que muda")
    # Os blocos do capital nao se sobrepoem, e o resto da serie e descartado.
    if aposta.contagens_por_bloco(np.ones(125), 60).tolist() != [60.0, 60.0]:
        problemas.append("aposta: os blocos do capital se sobrepoem")

    # --- o alerta que todo mundo usa, com o par declarado (alerta.py) ---

    # Os tres indicadores da receita recuperam o que o mundo declarou: a variância recupera
    # sigma^2, a autocorrelação recupera o parametro de um AR(1), e a assimetria acusa o lado
    # que a construção pesou --- e fica em zero onde o mundo e simetrico.
    rng_alerta = np.random.default_rng(31)
    dias_alerta = pd.Series(rng_alerta.normal(0.0, 0.01, 40000))
    # As janelas medem-se sem sobrepor, e a tolerância cobre o erro do estimador na amostra.
    var_janelas = alerta.variancia(dias_alerta, 1000).dropna().iloc[::1000]
    if abs(float(var_janelas.mean()) - 1e-4) / 1e-4 > 0.02:
        problemas.append("alerta: a variância da janela não recupera sigma^2")
    if abs(float(alerta.autocorrelacao(dias_alerta, 1000).dropna().iloc[::1000].mean())) > 0.05:
        problemas.append("alerta: a autocorrelação de um mundo independente não é zero")
    ruído_ar1 = rng_alerta.normal(0.0, 1.0, 60000)
    ar1 = pd.Series(np.empty(60000))
    for t in range(1, 60000):
        ar1.iloc[t] = 0.5 * ar1.iloc[t - 1] + ruído_ar1[t]
    if abs(alerta.autocorrelacao(ar1, 20000).iloc[-1] - 0.5) > 0.02:
        problemas.append("alerta: a autocorrelação não recupera o parâmetro do AR(1)")
    # A assimetria da construção u = z + a(z^2-1) tem valor fechado, e é ele o que a janela
    # tem de recuperar: (6a + 8a^3) / (1 + 2a^2)^(3/2).
    assim = pd.Series(direcao.assimetrico(60000, rng_alerta, sigma=0.01, a=0.3))
    teorico_alerta = (6 * 0.3 + 8 * 0.3 ** 3) / (1 + 2 * 0.3 ** 2) ** 1.5
    if abs(alerta.assimetria(assim, 20000).iloc[-1] - teorico_alerta) > 0.05:
        problemas.append("alerta: a assimetria não recupera o valor fechado da construção")
    assim_calma = alerta.assimetria(dias_alerta, 1000).dropna().iloc[::1000]
    if abs(float(assim_calma.median())) > 0.05:
        problemas.append("alerta: a assimetria de um mundo simétrico não é zero")

    # O silêncio é declarado: quem não tem janela ainda não alerta, e o dia acima do limiar
    # é alarme onde a estatística existe --- episódio é conta do orçamento, não da leitura.
    pequena = pd.Series([np.nan, np.nan, 2.0, 2.0, 0.0, 3.0])
    toques = alerta.dispara(pequena, 1.0)
    if toques.tolist() != [True, True, False, True] or toques.index[0] != 2:
        problemas.append("alerta: a leitura não respeita o silêncio da janela")
    matriz_alerta = np.array([[0.0, 1.0, 1.0, 0.0, 1.0], [0.0, 0.0, 0.0, 0.0, 0.0]])
    if alerta.orcamento(matriz_alerta, 0.5, dias_uteis=1)["episodios_por_mundo"] != 1.0:
        problemas.append("alerta: o orçamento não conta episódios, conta dias ou mundos a mais")

    # A calibração entrega o que promete: o limiar devolvido gasta, em episódios por ano, o
    # orçamento pedido --- e subir o limiar nunca gasta mais.
    nulos_alerta = rng_alerta.normal(0.0, 0.01, size=(60, 2500))
    alvo_alerta = 1.0
    limiar_alerta = alerta.limiar_do_orcamento(nulos_alerta, alvo_alerta, dias_uteis=252)
    gasto_alerta = alerta.orcamento(nulos_alerta, limiar_alerta, dias_uteis=252)["episodios_por_ano"]
    if not 0.7 < gasto_alerta < 1.3:
        problemas.append("alerta: o limiar calibrado não gasta o orçamento pedido (%.3f)" % gasto_alerta)
    if alerta.orcamento(nulos_alerta, limiar_alerta * 1.01, dias_uteis=252)["episodios_por_ano"] > gasto_alerta:
        problemas.append("alerta: subir o limiar passou a gastar mais")

    # --- as duas famílias que podem ter gerado a cauda (ramificacao.py) ---
    rng_cauda = np.random.default_rng(41)
    ext_mao = ramificacao.extremos(np.array([0.01, -0.10, -0.05, 0.02]))
    if abs(ext_mao["razao"] - 2.0) > 1e-12 or abs(ext_mao["pior"] - 0.10) > 1e-12:
        problemas.append("ramificacao: extremos não devolve o pior e a razão de mão")
    try:
        ramificacao.extremos(np.array([0.01, 0.02, 0.03]))
        problemas.append("ramificacao: extremos aceitou série sem segundo pior em queda")
    except ValueError:
        pass
    # A família que sorteia: variância um, e a razão mediana do t dentro do intervalo declarado.
    sorteios_cauda = ramificacao.independente(200000, rng_cauda)
    if not 0.97 < float(sorteios_cauda.std()) < 1.03 or abs(float(sorteios_cauda.mean())) > 0.02:
        problemas.append("ramificacao: o t padronizado não tem variância um")
    razoes_t = [ramificacao.extremos(ramificacao.independente(2000, rng_cauda))["razao"]
                for _ in range(40)]
    if not 1.05 < float(np.median(razoes_t)) < 1.70:
        problemas.append("ramificacao: a razão mediana do t saiu do intervalo declarado")
    # A família que se reproduz: cacho (dias ruins correlacionados) e pico que o t não faz.
    mundo_repr = ramificacao.critica(60000, rng_cauda)
    lag1_repr = float(np.corrcoef(mundo_repr[:-1], mundo_repr[1:])[0, 1])
    if lag1_repr < 0.2:
        problemas.append("ramificacao: a família que se reproduz não agrupa os dias ruins (%.3f)" % lag1_repr)
    if float(-mundo_repr.min()) < 8.0:
        problemas.append("ramificacao: a ramificação crítica não faz o pico que a cauda pede")
    if float(np.unique(mundo_repr).size) < 50:
        problemas.append("ramificacao: a população não visita estados demais")

    # --- a lei que anda, com o orçamento da sua variação (lei.py) ---
    rng_lei = np.random.default_rng(53)
    # A curva recupera o coeficiente que gerou o mundo: AR(1) tem autocorrelação de defasagem um
    # igual ao próprio coeficiente, e mundo sem memória tem curva no zero.
    curva_ar = lei.coeficiente_rolante(mudanca.ar1(60000, rng_lei, a=0.5), 20000)
    if abs(float(curva_ar[-1]) - 0.5) > 0.02 or not np.isnan(curva_ar[0]):
        problemas.append("lei: a curva não recupera o coeficiente do AR(1)")
    curva_calma = lei.coeficiente_rolante(rng_lei.normal(0.0, 0.01, 60000), 20000)
    if abs(float(curva_calma[-1])) > 0.02:
        problemas.append("lei: a curva do mundo sem memória não está no zero")
    # O orçamento é conta de mão: curva parada gasta zero, reta gasta a inclinação inteira.
    if lei.orcamento_variacao(np.full(100, 0.3)) != 0.0:
        problemas.append("lei: o orçamento da curva parada não é zero")
    if abs(lei.orcamento_variacao(np.linspace(0.0, 1.0, 101)) - 1.0) > 1e-12:
        problemas.append("lei: o orçamento da reta não é a inclinação inteira")
    # A simulação honra a lei que recebe: coeficiente constante vira autocorrelação medida de novo,
    # e coeficiente acima do limite é cortado no limite declarado, sem explosão.
    mundo_lei = lei.simular(np.full(60000, 0.5), 0.01, rng_lei)
    lag1_lei = float(np.corrcoef(mundo_lei[:-1], mundo_lei[1:])[0, 1])
    if abs(lag1_lei - 0.5) > 0.02:
        problemas.append("lei: a simulação não devolve a lei que recebeu (%.3f)" % lag1_lei)
    if not 0.010 < float(mundo_lei.std()) < 0.012:
        problemas.append("lei: a escala do mundo simulado não é a declarada")
    mundo_cortado = lei.simular(np.full(5000, 2.0), 0.01, rng_lei)
    if not np.all(np.isfinite(mundo_cortado)) or float(np.max(np.abs(mundo_cortado))) > 1.0:
        problemas.append("lei: o corte do coeficiente não segurou o mundo")
    # A fração na tolerância é conta de mão: dois de quatro dias dentro.
    if abs(lei.fracao_na_tolerancia(np.ones(4), np.array([1.0, 1.1, 1.5, 2.0]), 0.2, horizonte=4) - 0.5) > 1e-12:
        problemas.append("lei: a fração na tolerância não é a conta de mão")

    # --- o relógio contra a causa (relogio) ---
    rng_r = np.random.default_rng(77)
    xa = pd.Series(rng_r.normal(0.0, 0.012, 900), index=pd.bdate_range("2010-01-01", periods=900))
    xb = pd.Series(rng_r.normal(0.0, 0.012, 900), index=xa.index)
    varrido = relogio.varredura(xa, xb, atrasos=(0, 1), nulos=12, sementes=99)
    for atraso, caixa in varrido.items():
        if abs(caixa["desvios"]) > 3.0:
            problemas.append("relogio: par sem adiantamento saiu do nulo no atraso %d" % atraso)
        if caixa["dias"] <= 0:
            problemas.append("relogio: varredura sem dias comuns no atraso %d" % atraso)
    rompimentos_x = dependencia.rompimentos(xa)
    rompimentos_y = dependencia.rompimentos(dependencia.pareado(xb, 1))
    direto = dependencia.episodios_dirigidos(
        rompimentos_x.reindex(xa.index).fillna(False).astype(bool),
        rompimentos_y.reindex(xa.index).fillna(False).astype(bool))["assimetria"]
    if abs(varrido[1]["assimetria"] - direto) > 1e-12:
        problemas.append("relogio: a varredura não casa com a conta isolada no atraso declarado")
    ta, tb = relogio.terceiro_comum(4000, np.random.default_rng(55), 0.9, 0.01, 0.02)
    if not (0.85 < float(np.corrcoef(ta, tb)[0, 1]) < 0.95):
        problemas.append("relogio: o terceiro comum não entrega a correlação declarada")
    if abs(float(np.std(ta)) - 0.01) > 0.002 or abs(float(np.std(tb)) - 0.02) > 0.004:
        problemas.append("relogio: o terceiro comum não guarda as margens declaradas")

    # --- a janela que se escolhe sozinha (adaptativa) ---
    plano = np.concatenate((np.full(30, 1.0), np.full(30, 2.0)))
    caixa = adaptativa.nivel(plano, limiar=0.05, minima=4, maxima=20)
    if not ((caixa["tamanhos"] <= 20).all() and (caixa["tamanhos"][3:] >= 4).all()):
        problemas.append("adaptativa: o tamanho escapou dos limites declarados")
    dia_corte = [d for d, _, _ in caixa["encolhimentos"]]
    if dia_corte and min(dia_corte) < 30:
        problemas.append("adaptativa: encolheu antes da mudança que não existe")
    if not dia_corte or max(dia_corte) > 55:
        problemas.append("adaptativa: não encolheu perto da mudança declarada")
    controle = adaptativa.nivel(plano, limiar=1e9, minima=4, maxima=20)
    direto = np.array([plano[max(0, t - 19):t + 1].mean() for t in range(plano.size)])
    if not np.allclose(controle["estimativa"], direto, atol=1e-12):
        problemas.append("adaptativa: o limiar infinito não devolve a janela fixa")

    # --- o laço que reage (laco) ---
    rng_laco = np.random.default_rng(41)
    mundo_laco = mudanca.estavel(600, rng_laco, sigma=0.01)
    serie = pd.Series(mundo_laco)
    linha_corte = promessa.corte_no_posto(serie, 63, 3)
    if not np.array_equal(laco.reage(mundo_laco, linha_corte.to_numpy(), fracao=0.0, atraso=1),
                          mundo_laco):
        problemas.append("laco: a reação nula não devolve o mundo intacto")
    fabricado = np.array([-0.10, -0.02, -0.03, 0.01])
    barra = np.array([-0.05, -0.05, -0.05, -0.05])
    saida_um = laco.reage(fabricado, barra, fracao=0.25, atraso=1)
    if abs(saida_um[1] - (-0.015)) > 1e-12 or abs(saida_um[0] + 0.10) > 1e-12:
        problemas.append("laco: o rompimento não amortece só o dia do atraso")
    dois = laco.reage(np.array([-0.10, -0.20, 0.0]), barra[:3], fracao=0.5, atraso=1)
    if abs(dois[1] - (-0.10)) > 1e-12 or abs(dois[0] + 0.10) > 1e-12:
        problemas.append("laco: cada rompimento amortece uma vez, no dia do próprio atraso")
    historico = laco.recalibra(mundo_laco, 63, 3, ciclos=3, fracao=0.0, atraso=1)
    if len(set(historico["cortes"])) != 1 or len(set(historico["entregas"])) != 1:
        problemas.append("laco: com reação nula, o laço não devolve a calibragem parada")

    # --- a rampa que nunca termina (mudanca.andando) ---
    rng_andando = np.random.default_rng(29)
    mundo_andando = mudanca.andando(4000, rng_andando, sigma=0.01, fator=2.0)
    if mundo_andando.size != 4000 or not np.all(np.isfinite(mundo_andando)):
        problemas.append("andando: o mundo não tem o tamanho ou a finitude declarados")
    if float(np.std(mundo_andando[3000:])) / float(np.std(mundo_andando[:1000])) < 1.5:
        problemas.append("andando: a escala não andou o declarado")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    with tempfile.TemporaryDirectory() as pasta:
        fig, _ = plt.subplots()
        caminhos = graficos.salvar(fig, "auto_teste", 1, destino=Path(pasta))
        plt.close(fig)
        if {c.suffix for c in caminhos} != {".pdf", ".png"}:
            problemas.append("a figura não saiu nos dois formatos: os caminhos foram %s"
                             % sorted(c.suffix for c in caminhos))
        for caminho in caminhos:
            if not caminho.exists() or caminho.stat().st_size == 0:
                problemas.append("figura não foi gravada: %s" % caminho.name)

    # --- a profundidade como eixo (profundidade.py) ---
    rng_prof = np.random.default_rng(51)
    caixas_ind = profundidade.razoes(pd.Series(rng_prof.normal(0.0, 0.01, 60000)),
                                    pd.Series(rng_prof.normal(0.0, 0.012, 60000)), janela=252)
    if abs(float(caixas_ind[0.05]["excesso"]) - 1.0) > 0.15 or abs(float(caixas_ind[0.02]["excesso"]) - 1.0) > 0.25:
        problemas.append("profundidade: pernas independentes não dão razão um no corte raso")
    if abs(profundidade.expoente(list(caixas_ind), caixas_ind) - 2.0) > 0.25:
        problemas.append("profundidade: o par independente não carrega o expoente dois da independência")
    ga, gb = profundidade.controle_gaussiano(60000, np.random.default_rng(52), 0.5)
    caixas_g = profundidade.razoes(pd.Series(0.01 * ga.to_numpy()), pd.Series(0.012 * gb.to_numpy()), janela=252)
    alfa_g = profundidade.expoente(list(caixas_g), caixas_g)
    ta, tb = profundidade.controle_t(60000, np.random.default_rng(53), 0.5, 4)
    caixas_t = profundidade.razoes(pd.Series(0.01 * ta.to_numpy()), pd.Series(0.012 * tb.to_numpy()), janela=252)
    alfa_t = profundidade.expoente(list(caixas_t), caixas_t)
    if not alfa_g - alfa_t > 0.15:
        problemas.append("profundidade: a gaussiana não ficou acima da t na mesma janela (%.3f contra %.3f)"
                         % (alfa_g, alfa_t))
    gc, gd = profundidade.controle_gaussiano(60000, np.random.default_rng(54), 0.7)
    caixas_g7 = profundidade.razoes(pd.Series(0.01 * gc.to_numpy()), pd.Series(0.012 * gd.to_numpy()), janela=252)
    if profundidade.expoente(list(caixas_g7), caixas_g7) >= alfa_g:
        problemas.append("profundidade: mais correlação não abaixou o expoente da gaussiana")

    # --- o preco da protecao que protege (protecao.py) ---
    rng_prot = np.random.default_rng(61)
    indep_a = pd.Series(0.012 * rng_prot.normal(0.0, 1.0, 30000))
    indep_b = pd.Series(0.017 * rng_prot.normal(0.0, 1.0, 30000))
    perdas_ind = protecao.perdas_conjuntas(indep_a, indep_b)
    chao_ind = protecao.capital_conjunto(perdas_ind) / protecao.capital_marginal(indep_a, indep_b)
    if not 1.2 < chao_ind < 2.2:
        problemas.append("protecao: o chao independente da conta conjunta saiu do declarado (%.3f)" % chao_ind)
    choq_a, choq_b = mudanca.par_de_cauda(30000, np.random.default_rng(62), 0.014, 0.5, 0.15, 3.0)
    perdas_choq = protecao.perdas_conjuntas(pd.Series(choq_a), pd.Series(choq_b))
    razao_choq = protecao.capital_conjunto(perdas_choq) / protecao.capital_marginal(pd.Series(choq_a), pd.Series(choq_b))
    if not razao_choq > chao_ind + 0.5:
        problemas.append("protecao: o choque comum nao encareceu a barreira correta (%.3f contra %.3f)" % (razao_choq, chao_ind))
    if not 0.0 <= protecao.descoberto(protecao.capital_conjunto(perdas_choq), perdas_choq) <= 0.08:
        problemas.append("protecao: o capital do quantil nao cobre o nivel prometido")
    # o canal com orcamento: fracao cheia devolve a conta cheia, fracao pequima aproxima o quadrado
    cheio = protecao.canal(pd.Series(rng_prot.normal(0.0, 0.01, 30000)),
                            pd.Series(0.012 * rng_prot.normal(0.0, 1.0, 30000)), 1.0,
                            semente=63)
    if not 0.85 < cheio["recall"] <= 1.0:
        problemas.append("protecao: o canal com fracao cheia nao devolve a observacao completa (%.3f)" % cheio["recall"])
    fino = protecao.canal(pd.Series(rng_prot.normal(0.0, 0.01, 30000)),
                          pd.Series(0.012 * rng_prot.normal(0.0, 1.0, 30000)), 0.1,
                          semente=64)
    if not 0.3 * fino["verdadeiros"] * 0.01 <= fino["detectados"] <= 2.5 * fino["verdadeiros"] * 0.01:
        problemas.append("protecao: o canal fino nao aproxima o quadrado da fracao (%d contra ~%.1f)" % (
            fino["detectados"], fino["verdadeiros"] * 0.01))


    # a capacidade de memoria: conservada no posto do estado, e o lugar onde mora separa
    rng_cap = np.random.default_rng(71)
    ruido = pd.Series(rng_cap.normal(0.0, 1.0, 4000))
    janela_cap = capacidade.capacidade_total(capacidade.capacidade_por_lag(
        capacidade.estados_janela(ruido, 40), ruido, 60))
    if abs(janela_cap - 40.0) > 0.5:
        problemas.append("capacidade: a janela devolve a capacidade exata (%.3f contra 40)" % janela_cap)
    exp_cap = capacidade.capacidade_total(capacidade.capacidade_por_lag(
        capacidade.estados_exponencial(ruido, 0.05), ruido, 200))
    if exp_cap > 1.5:
        problemas.append("capacidade: o estado escalar devolve mais de uma direcao (%.3f)" % exp_cap)
    res_cap = capacidade.capacidade_total(capacidade.capacidade_por_lag(
        capacidade.estados_reservatorio(ruido, 50, semente=65), ruido, 300))
    if not 25.0 <= res_cap <= 52.5:
        problemas.append("capacidade: o reservatorio fora da conservacao (%.2f contra n=50)" % res_cap)

    # a cascata calibrada: mesma contagem conjunta, e so a intervencao separa
    choque_t = cascata.mundo_choque(4000, 0.02, 0.04, 0.04, semente=81)
    alvo_t = cascata.pares_de_alinhamento(choque_t, 3).size
    q_t = cascata.calibra_transmissao(4000, 0.04, 0.02, (0, 1, 2), alvo_t, janela=3, semente=82)
    cascata_t = cascata.mundo_cascata(4000, 0.04, 0.02, (0, 1, 2), q_t, semente=82)
    obtido_t = cascata.pares_de_alinhamento(cascata_t, 3).size
    if abs(obtido_t - alvo_t) > max(3, 0.1 * alvo_t):
        problemas.append("cascata: a calibracao nao fecha a contagem conjunta (%d contra %d)" % (obtido_t, alvo_t))
    mortas_c = int(cascata_t['romp_b'].sum()) - int(cascata.bloqueia_a(cascata_t)['romp_b'].sum())
    mortas_h = int(choque_t['romp_b'].sum()) - int(cascata.bloqueia_a(choque_t)['romp_b'].sum())
    if not mortas_c > 0.3 * obtido_t:
        problemas.append("cascata: a intervencao mata pouco da cascata (%d de %d)" % (mortas_c, obtido_t))
    if mortas_h != 0:
        problemas.append("cascata: a intervencao mexeu no mundo do choque (%d mortas)" % mortas_h)

    # a fusao sob dependencia arbitraria: marginais validas, estrutura entre elas
    ps_t = aposta.ps_dependentes(2000, 107, 0.8, semente=91)
    if abs(float(ps_t.mean()) - 0.5) > 0.03:
        problemas.append("fusao: a marginal dos p-values dependentes nao e uniforme (%.3f)" % ps_t.mean())
    es_t = aposta.e_calibrado(np.random.default_rng(92).random(100000))
    if abs(float(es_t.mean()) - 1.0) > 0.1:
        problemas.append("fusao: o calibrador de e-value nao tem media um (%.3f)" % es_t.mean())
    forte_t = float(np.corrcoef(ps_t[:, 0], ps_t[:, 1])[0, 1])
    fraco_t = aposta.ps_dependentes(2000, 107, 0.0, semente=91)
    nulo_t = float(np.corrcoef(fraco_t[:, 0], fraco_t[:, 1])[0, 1])
    if not (forte_t > 0.3 > nulo_t):
        problemas.append("fusao: a copula nao gera a dependencia declarada (%.3f contra %.3f)" % (forte_t, nulo_t))

    return problemas
