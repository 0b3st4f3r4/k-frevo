r"""Regimes: quantas explicações cabem nos mesmos dados.

Volta 3, a geometria do condicionamento. O capítulo 7 deixou a pergunta em termos de informação
--- quanta cabe num pedaço finito de passado ---, e este módulo a torna contável: dada uma
família de explicações e um conjunto de estatísticas medidas no dado, **quantos membros da
família reproduzem todas elas** dentro da tolerância?

A conta é grosseira de propósito. Não é estimação, não é verossimilhança, não é otimização: é
uma grade, um punhado de estatísticas e uma contagem. O que ela mede é a **forma** do conjunto
factível, e é isso que decide duas coisas diferentes que costumam ser confundidas:

1. uma estatística que deixa **região** --- muitas explicações cabem, e o dado não escolhe entre
   elas;
2. uma estatística que corta **a zero** --- nenhuma explicação da família cabe, e o dado refuta
   a família inteira.

**O defeito que este módulo torna impossível.** Dizer "o modelo explica os dados" sem dizer
*qual* dos dois casos é. Uma taxa média é reproduzida por quase toda a família; o agrupamento
dos dias ruins, não. Quem só olha a primeira conclui que encontrou o mecanismo.

Toda função que sorteia recebe o \texttt{rng} por parâmetro e não toca a semente global. A
família tem duas leis --- calma e agitada --- e, na versão persistente, um terceiro parâmetro: a
duração média do regime agitado. Sem ele, o estado é sorteado de novo a cada dia, e é por isso
que a família sem persistência não alcança o agrupamento do dado.

**A extensão da travessia da divergência (capítulo 11, a escolha).** As quatro estatísticas são
funcionais de UMA lei --- a lei empírica das contagens de rompimentos por bloco ---, e a pergunta
que o capítulo deixa em pé é a escolha: quando a região não escolhe, quem escolhe? A resposta da
geometria é a projeção em divergência sobre a envoltória convexa da família. **O defeito que esta
extensão torna impossível:** apresentar um membro escolhido pela tolerância --- ou pela mão ---
como "a explicação que o dado escolheu". A projeção é canônica, a convexidade garante que ela
existe e é única, e a distância entre ela e a escolha da tolerância é medida nas duas moedas,
não opinada.
"""
import numpy as np
import pandas as pd

TAXA_PADRAO = 0.05
JANELA_PADRAO = 252
POSTO_PADRAO = 13
BLOCO_PADRAO = 60

__all__ = ["TAXA_PADRAO", "JANELA_PADRAO", "POSTO_PADRAO", "BLOCO_PADRAO", "estatisticas",
           "lei_dos_blocos", "mistura", "persistente", "persistente_heterogeneo",
           "serve_a_todos", "cabem", "divergencia", "projecao"]


def estatisticas(valores, janela: int = JANELA_PADRAO, posto: int = POSTO_PADRAO,
                 bloco: int = BLOCO_PADRAO, taxa: float = TAXA_PADRAO) -> dict:
    r"""As quatro leituras do dado: a taxa, o pior bloco, a mediana e o excesso de blocos cheios.

    A taxa é a leitura que a promessa do capítulo 3 entrega; as outras três são a forma com que
    os rompimentos chegam, e é aí que as famílias se separam.
    """
    v = np.asarray(valores, dtype=float)
    if v.size <= janela + bloco:
        raise ValueError("serie curta demais para a janela e o bloco")
    janelas = np.lib.stride_tricks.sliding_window_view(v, janela)
    corte = np.partition(janelas, posto - 1, axis=1)[:, posto - 1][:-1]
    rompe = (v[janela:] < corte).astype(float)
    blocos = pd.Series(rompe).rolling(bloco).sum().dropna().to_numpy()
    return {
        "taxa": float(rompe.mean()),
        "pior": int(blocos.max()),
        "mediana": float(np.median(blocos)),
        "acima_do_dobro": float((blocos > 2 * bloco * taxa).mean()),
    }


def lei_dos_blocos(valores, janela: int = JANELA_PADRAO, posto: int = POSTO_PADRAO,
                   bloco: int = BLOCO_PADRAO, alfabeto: int = 25) -> np.ndarray:
    r"""A lei empírica das contagens de rompimentos por bloco --- a lei inteira, não quatro resumos.

    As quatro estatísticas do capítulo são funcionais desta lei: o pior bloco é a casa mais alta
    com massa, a mediana e o excesso de blocos cheios saem dela, e a taxa é a média da contagem
    dividida pelo bloco. Perguntar às quatro estatísticas é perguntar a quatro funcionais;
    perguntar à lei é perguntar a ela inteira.

    As janelas são desencontradas e dependentes, e isso é declarado em vez de escondido: cada
    bloco começa um dia depois do anterior, de modo que dois blocos vizinhos partilham quase
    todo o seu material --- a lei não conta episódios independentes, conta janelas do mesmo
    passado. O alfabeto é o das contagens: a casa emph{k} recebe os blocos com emph{k}
    rompimentos, e a última casa engloba a cauda --- nela entra tudo o que alcança ou passa do
    fim do alfabeto, para que a lei nunca perca massa.
    """
    v = np.asarray(valores, dtype=float)
    if alfabeto < 2:
        raise ValueError("o alfabeto precisa de pelo menos duas casas")
    if v.size <= janela + bloco:
        raise ValueError("serie curta demais para a janela e o bloco")
    janelas = np.lib.stride_tricks.sliding_window_view(v, janela)
    corte = np.partition(janelas, posto - 1, axis=1)[:, posto - 1][:-1]
    rompe = (v[janela:] < corte).astype(float)
    blocos = pd.Series(rompe).rolling(bloco).sum().dropna().to_numpy()
    casas = np.minimum(blocos, alfabeto - 1).astype(int)
    lei = np.bincount(casas, minlength=alfabeto)[:alfabeto].astype(float)
    return lei / lei.sum()


def mistura(n: int, rng: np.random.Generator, sigma: float, p: float, razao: float) -> np.ndarray:
    r"""Duas leis, sorteadas todo dia: o estado de hoje não diz nada sobre o de amanhã.

    A oscilação global é preservada qualquer que seja \emph{p}: a lei calma encolhe para que a
    média das variâncias continue sendo \emph{sigma}, de modo que comparar membros da família
    compare o mecanismo e não o tamanho.
    """
    if not 0.0 < p < 1.0:
        raise ValueError("a probabilidade do regime agitado precisa estar entre 0 e 1")
    if razao <= 1.0:
        raise ValueError("a razao entre as duas leis precisa ser maior que um")
    calma = sigma / np.sqrt(1.0 + p * (razao ** 2 - 1.0))
    agitada = calma * razao
    return rng.normal(0.0, np.where(rng.random(n) < p, agitada, calma))


def persistente(n: int, rng: np.random.Generator, sigma: float, p: float, razao: float,
                permanencia: float) -> np.ndarray:
    r"""As mesmas duas leis, com o estado durando: a permanência é a duração média do regime.

    A cadeia tem dois estados e trocas assimétricas, porque a simétrica não serve: com a mesma
    probabilidade de trocar nos dois sentidos a proporção estacionária fica presa em metade, e
    não em \emph{p}. Dada a duração média do regime agitado, a do regime calmo sai da conta
    \emph{p = d/(d + c)}, que é o que mantém a oscilação global comparável entre os membros da
    família.
    """
    if permanencia < 1.0:
        raise ValueError("a permanencia media precisa ser de pelo menos um dia")
    if not 0.0 < p < 1.0:
        raise ValueError("a probabilidade do regime agitado precisa estar entre 0 e 1")
    calma = sigma / np.sqrt(1.0 + p * (razao ** 2 - 1.0))
    agitada = calma * razao
    dura_calma = permanencia * (1.0 - p) / p
    sai_do_agitado = 1.0 / permanencia
    sai_do_calmo = 1.0 / dura_calma
    estado = np.empty(n, dtype=bool)
    estado[0] = rng.random() < p
    for i in range(1, n):
        troca = sai_do_agitado if estado[i - 1] else sai_do_calmo
        estado[i] = (not estado[i - 1]) if rng.random() < troca else estado[i - 1]
    return rng.normal(0.0, np.where(estado, agitada, calma))


def persistente_heterogeneo(n: int, rng: np.random.Generator, sigma: float, p: float,
                            razao: float, curta: float, longa: float,
                            fracao_curta: float) -> np.ndarray:
    r"""Como \texttt{persistente}, mas a duração do episódio agitado não é uma só.

    Cada episódio sorteia a sua duração média entre uma curta e uma longa. A marginal não muda
    --- a fração agitada é a mesma ---, e o que muda é a forma do agrupamento: episódios de
    tamanhos diferentes convivem, e é isso que permite o pior bloco **e** o excesso de blocos
    cheios serem altos ao mesmo tempo. Na família de duração única os dois são substitutos.
    """
    if curta < 1.0 or longa < curta:
        raise ValueError("as duracoes precisam ser >= 1 e a longa >= a curta")
    if not 0.0 <= fracao_curta <= 1.0:
        raise ValueError("a fracao de episodios curtos precisa estar entre 0 e 1")
    calma = sigma / np.sqrt(1.0 + p * (razao ** 2 - 1.0))
    agitada = calma * razao
    dura_calma = (fracao_curta * curta + (1.0 - fracao_curta) * longa) * (1.0 - p) / p
    estado = np.empty(n, dtype=bool)
    duracao = float(longa)
    estado[0] = rng.random() < p
    if estado[0]:
        duracao = curta if rng.random() < fracao_curta else longa
    for i in range(1, n):
        if estado[i - 1]:
            troca = 1.0 / duracao
        else:
            troca = 1.0 / dura_calma
        if rng.random() < troca:
            estado[i] = not estado[i - 1]
            if estado[i]:
                duracao = curta if rng.random() < fracao_curta else longa
        else:
            estado[i] = estado[i - 1]
    return rng.normal(0.0, np.where(estado, agitada, calma))


def serve_a_todos(mercados: dict, grade_p, grade_razao, grade_permanencia, tolerancia: dict,
                  chaves, semente: int = 211) -> list:
    r"""Os triplos que servem a \emph{todos} os mercados ao mesmo tempo.

    A lei é compartilhada e a escala é de cada mercado — cada série é gerada com o seu próprio
    desvio, e o mecanismo é o mesmo. É o teste da pergunta A4: se observar mais mundos basta para
    identificar um mecanismo comum, é aqui que o conjunto de triplos sobreviventes aparece; se
    ele fica vazio, os mundos discordam do mecanismo e não só do tamanho.
    """
    servem = []
    for p_ in grade_p:
        for razao in grade_razao:
            for permanencia in grade_permanencia:
                ok = True
                for m in mercados.values():
                    sorteio = np.random.default_rng(semente)
                    e = estatisticas(persistente(len(m["x"]), sorteio, m["sigma"], p_, razao,
                                                 permanencia))
                    if not all(abs(e[k] - m["real"][k]) <= tolerancia[k] for k in chaves):
                        ok = False
                        break
                if ok:
                    servem.append((p_, razao, permanencia))
    return servem


def cabem(candidatos: list, real: dict, tolerancia: dict, chaves) -> list:
    r"""Os candidatos que reproduzem todas as estatísticas pedidas dentro da tolerância."""
    return [c for c in candidatos
            if all(abs(c["estatisticas"][k] - real[k]) <= tolerancia[k] for k in chaves)]


def divergencia(p, q) -> float:
    r"""A divergência de emph{p} a emph{q}: o custo médio, em nats, de apostar em emph{q}
    quando o mundo segue emph{p}.

    Casa a casa do alfabeto, a massa de emph{p} paga o logaritmo da razão entre o que o mundo
    dá e o que a aposta diz. A casa onde o mundo põe massa e a aposta não põe nada custa
    infinito --- esta é a forma que a refutação assume na moeda da divergência: uma explicação
    que dá probabilidade zero ao que aconteceu não está longe, está fora. A casa onde o mundo
    não põe massa não custa nada, seja lá o que diga a aposta. Zero vezes o logaritmo de zero
    é zero, por decreto da conta.
    """
    a, b = np.asarray(p, dtype=float), np.asarray(q, dtype=float)
    if a.shape != b.shape:
        raise ValueError("as duas leis precisam viver no mesmo alfabeto")
    if (a < 0).any() or (b < 0).any():
        raise ValueError("lei com massa negativa não é lei")
    if not np.isclose(a.sum(), 1.0) or not np.isclose(b.sum(), 1.0):
        raise ValueError("lei que não soma um não é lei")
    if ((a > 0) & (b <= 0)).any():
        return float("inf")
    casas = a > 0
    return float(np.sum(a[casas] * np.log(a[casas] / b[casas])))


def projecao(lei, leis, inicio=None, passos: int = 800) -> dict:
    r"""A projeção em divergência da lei sobre a envoltória convexa das leis da família.

    A envoltória convexa é o conjunto das misturas --- cada membro da família com o seu peso,
    pesos não negativos que somam um ---, e é convexa por construção. Por isso a projeção em
    divergência existe e é única, e toda candidata da envoltória está pelo menos tão longe do
    dado quanto a soma das duas pernas pela projeção: a desigualdade de Pitágoras da
    divergência, que separa o que falta à projeção do que falta à candidata.

    A conta é a atualização multiplicativa de Csiszár: cada vértice ganha ou perde peso na
    razão entre o que ele diz e o que a mistura corrente diz, somada casa a casa com a massa
    que o dado põe. Determinística, sem sorteio: dados a lei e os vértices, o resultado é um
    só. O peso inicial é uniforme quando não se declara outro, e a parada é o número de passos
    ou o peso que para de se mover.
    """
    alvo = np.asarray(lei, dtype=float)
    vertices = np.asarray(leis, dtype=float)
    if vertices.ndim != 2 or vertices.shape[1] != alvo.size:
        raise ValueError("os vértices precisam viver no alfabeto da lei")
    if (vertices < 0).any() or (alvo < 0).any():
        raise ValueError("lei com massa negativa não é lei")
    if not np.allclose(vertices.sum(axis=1), 1.0) or not np.isclose(alvo.sum(), 1.0):
        raise ValueError("lei que não soma um não é lei")
    casas = alvo > 0
    if (vertices[:, casas].sum(axis=0) <= 0).any():
        raise ValueError("o dado tem massa numa casa onde nenhum vértice tem: "
                         "a projeção em divergência é infinita")
    n = vertices.shape[0]
    if inicio is None:
        pesos = np.full(n, 1.0 / n)
    else:
        pesos = np.asarray(inicio, dtype=float)
        if pesos.size != n or (pesos < 0).any() or pesos.sum() <= 0:
            raise ValueError("o peso inicial precisa ter o tamanho da família, "
                             "ser não negativo e somar mais que zero")
        pesos = pesos / pesos.sum()
    for _ in range(int(passos)):
        mistura = pesos @ vertices
        fator = vertices[:, casas] @ (alvo[casas] / mistura[casas])
        novos = pesos * fator
        novos = novos / novos.sum()
        parou = float(np.abs(novos - pesos).max()) < 1e-13
        pesos = novos
        if parou:
            break
    lei_projetada = pesos @ vertices
    dominante = int(np.argmax(pesos))
    return {"pesos": pesos, "lei": lei_projetada,
            "divergencia": divergencia(alvo, lei_projetada),
            "vertice_dominante": dominante,
            "peso_dominante": float(pesos[dominante])}
