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

from . import (calendario, centro, dados, dependencia, direcao, esquecimento, estabilidade,
               graficos, intervencao, mudanca, partilha, promessa, recorde, regimes, vigia,
               volatilidade)

# A versão tem uma fonte só, e ela é o pyproject.toml: duas cópias divergem, e a
# divergência é silenciosa. O fallback existe para o caso de o pacote ser lido da
# árvore de trabalho, sem instalação.
try:
    VERSAO = version("frevolab")
except PackageNotFoundError:
    VERSAO = "0.1.0"

__all__ = ["calendario", "dados", "dependencia", "esquecimento", "estabilidade", "graficos",
           "intervencao", "mudanca", "partilha", "promessa", "recorde", "regimes", "vigia",
           "volatilidade", "VERSAO", "auto_teste"]


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

    # --- regimes: a família do capítulo 6 ---
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

    # --- intervencao: o desenho experimental do capítulo 9 ---
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
    # A tolerância do capítulo 11 tinha DUAS unidades com o mesmo 0,15: a do nível, que o erro
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

    return problemas
