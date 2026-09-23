r"""O desenho da intervenção: o que separa duas explicações que a observação não separa.

Os capítulos anteriores deixaram uma pergunta de pé. Duas famílias explicam o mesmo dado --- uma
diz que a memória mora na própria série, outra que existe um estado escondido que troca de lei ---
e acumular mundo observado não escolheu entre elas. Este módulo trata a única saída que sobra:
**mexer no mundo de propósito** e ver o que ele faz.

O desenho mínimo é um ato só: **segurar o mundo parado** por \emph{k} dias e olhar como ele volta.
O ato é idêntico nos dois mundos; o que muda é o que ele significa. Num mundo em que a memória
mora na série, segurar apaga a memória acumulada, e quanto mais tempo se segura, mais fundo o
buraco --- ele volta ferido, e a ferida cresce com \emph{k} até saturar. Num mundo de estado
escondido, o estado continua correndo enquanto a série está parada, e a soltura devolve o mundo
no mesmo nível de antes: a resposta não depende de \emph{k}. É essa diferença de \emph{forma} ---
uma curva que sobe contra uma reta --- que a observação não via.

**O defeito que este módulo torna impossível.** Dizer "precisamos de mais dados" sem dizer quantos,
e desenhar um experimento caro que não separa nada. O que a medição entrega é o preço: a
\texttt{resposta} dá a diferença, a dispersão entre replicatas dá o ruído, e a conta
\texttt{replicatas\_necessarias} dá quantas vezes o experimento precisa se repetir para os dois
intervalos não se cruzarem. O custo em dias é o produto --- e ele tem mínimo interior, porque
segurar mais fundo separa mais e custa mais.

Toda função que sorteia recebe o \texttt{rng} por parâmetro e não toca a semente global.
"""
from statistics import NormalDist

import numpy as np

from . import regimes

ALFA = 0.02
BETA = 0.97
P_AGITADO = 0.08
RAZAO = 3.0
PERMANENCIA = 320.0
AQUECIMENTO = 1500
ESPERA_PADRAO = 20
CONFIANCA = 0.95
MUNDOS = ("memoria", "escondido")
LEITURAS = ("taxa", "pior", "mediana", "acima_do_dobro")

__all__ = ["ALFA", "BETA", "P_AGITADO", "RAZAO", "PERMANENCIA", "AQUECIMENTO", "ESPERA_PADRAO",
           "CONFIANCA", "MUNDOS", "LEITURAS", "serie", "resposta", "replicatas", "leituras",
           "replicatas_necessarias", "custo", "desenho", "separa"]


def serie(mundo: str, n: int, rng: np.random.Generator, sigma: float, segurar=None,
          **parametros) -> np.ndarray:
    r"""A série de um dos dois mundos, com a contenção opcional.

    \texttt{mundo} é \texttt{"memoria"} (a volatilidade de hoje é função do que a série fez
    ontem, e o estado é a própria série) ou \texttt{"escondido"} (a série é ruído cuja escala
    obedece a um estado que a série não mostra). \texttt{segurar=(início, dias)} fixa a série em
    zero nessa janela --- é o ato, e fora dela nada muda.

    A escala dos dois mundos é a mesma, \emph{sigma}: comparar membros compare o mecanismo, e não
    o tamanho --- é a mesma regra do capítulo das explicações equivalentes.
    """
    if mundo not in MUNDOS:
        raise ValueError("mundo desconhecido: %r; os mundos são %s" % (mundo, list(MUNDOS)))
    if n <= 1:
        raise ValueError("a serie precisa de pelo menos dois dias")
    if segurar is not None:
        inicio, dias = segurar
        if inicio < 0 or dias < 1 or inicio + dias >= n:
            raise ValueError("a contencao precisa caber na serie, com um dia depois dela")
    if mundo == "memoria":
        alfa = float(parametros.get("alfa", ALFA))
        beta = float(parametros.get("beta", BETA))
        if alfa <= 0.0 or beta <= 0.0 or alfa + beta >= 1.0:
            raise ValueError("a volatilidade da serie precisa de alfa > 0, beta > 0 e alfa+beta < 1")
        return _memoria(n, rng, sigma, alfa, beta, segurar)
    return _escondido(n, rng, sigma, float(parametros.get("p", P_AGITADO)),
                      float(parametros.get("razao", RAZAO)),
                      float(parametros.get("permanencia", PERMANENCIA)), segurar)


def _memoria(n: int, rng: np.random.Generator, sigma: float, alfa: float, beta: float,
             segurar) -> np.ndarray:
    r"""A oscilação de amanhã depende do que a série fez hoje: a série carrega o próprio estado.

    \emph{v(t) = omega + alfa x(t-1)^2 + beta v(t-1)}, com \emph{omega} escolhido para que a
    variância de repouso seja \emph{sigma^2}. Durante a contenção a série é zero por decreto, e a
    oscilação decai para o seu piso --- é por isso que ela volta ferida, e mais ferida quanto mais
    tempo ficou parada.
    """
    omega = sigma ** 2 * (1.0 - alfa - beta)
    inicio, dias = segurar if segurar is not None else (n, 0)
    v = np.empty(n)
    x = np.empty(n)
    v[0] = sigma ** 2
    x[0] = rng.normal(0.0, sigma)
    for i in range(1, n):
        v[i] = omega + alfa * x[i - 1] ** 2 + beta * v[i - 1]
        x[i] = 0.0 if inicio <= i < inicio + dias else rng.normal(0.0, np.sqrt(v[i]))
    return x


def _escondido(n: int, rng: np.random.Generator, sigma: float, p: float, razao: float,
               permanencia: float, segurar) -> np.ndarray:
    r"""O estado troca de lei sem aparecer na série: parar a série não para o estado.

    É a família persistente do capítulo das explicações equivalentes, de modo que o empate entre
    os dois mundos é medido com o instrumento que já existe, e não com um novo. O estado é
    sorteado antes da contenção e continua a correr durante ela.
    """
    x = regimes.persistente(n, rng, sigma, p, razao, permanencia)
    if segurar is not None:
        inicio, dias = segurar
        x = x.copy()
        x[inicio:inicio + dias] = 0.0
    return x


def resposta(x: np.ndarray, inicio: int, contencao: int, espera: int) -> float:
    r"""Quanto do próprio nível o mundo perdeu, medido depois de soltar.

    A referência é o próprio mundo, na janela de \emph{espera} dias que antecede a contenção: a
    resposta vale um quando o mundo volta ao que era, e menos que um quando volta ferido. Medir
    contra a escala de fora esconderia justamente o que se quer ver.
    """
    x = np.asarray(x, dtype=float)
    if inicio < espera or inicio + contencao + espera > x.size:
        raise ValueError("a janela de referencia ou de espera nao cabe na serie")
    antes = float(np.mean(np.abs(x[inicio - espera:inicio])))
    if antes <= 0.0:
        raise ValueError("o mundo estava parado antes da contencao: nao ha referencia")
    depois = float(np.mean(np.abs(x[inicio + contencao:inicio + contencao + espera])))
    return depois / antes


def replicatas(mundo: str, rng: np.random.Generator, sigma: float, contencao: int, espera: int,
               repeticoes: int, aquecimento: int = AQUECIMENTO, **parametros) -> np.ndarray:
    r"""O mesmo experimento repetido: uma resposta por replicata, cada uma num mundo novo.

    Cada replicata é um mundo sorteado inteiro, e não um pedaço do mesmo mundo: é o que o
    experimento de fato faz quando não se pode repetir o mesmo dia.
    """
    if repeticoes < 2:
        raise ValueError("a dispersao precisa de pelo menos duas replicatas")
    n = aquecimento + contencao + espera
    saida = np.empty(repeticoes)
    for i in range(repeticoes):
        saida[i] = resposta(serie(mundo, n, rng, sigma, (aquecimento, contencao), **parametros),
                            aquecimento, contencao, espera)
    return saida


def leituras(mundo: str, sigma: float, dias: int, sementes: int, semente: int = 7000,
             **parametros) -> dict:
    r"""As quatro leituras de um mundo, tomadas na mediana de várias sementes.

    Uma leitura só não é uma leitura: o pior bloco de uma série sorteada varia de semente para
    semente mais do que varia entre mecanismos vizinhos, e é isso que obriga a mediana. As chaves
    são as do capítulo das explicações equivalentes, de modo que o empate entre dois mundos é
    medido com o instrumento que já existe.
    """
    if sementes < 1:
        raise ValueError("a mediana precisa de pelo menos uma semente")
    medidas = [regimes.estatisticas(serie(mundo, dias, np.random.default_rng(semente + i), sigma,
                                           **parametros)) for i in range(sementes)]
    return {c: float(np.median([m[c] for m in medidas])) for c in LEITURAS}


def replicatas_necessarias(diferenca: float, desvio: float, confianca: float = CONFIANCA) -> float:
    r"""Quantas replicatas para os dois intervalos não se cruzarem.

    Cada lado carrega o seu raio, e a soma dos dois tem de caber dentro da diferença que se quer
    ver: o intervalo do primeiro mundo e o do segundo não podem se cruzar. O raio cai com a raiz do
    número de replicatas, de modo que \emph{n = (z s / d)^2}, com \emph{s} a **soma** dos dois
    desvios medidos, \emph{z} o quantil da confiança declarada e \emph{d} a diferença que se
    **insiste** em ver. Quem não declara essa diferença está comprando um experimento sem preço.

    A conta supõe que a resposta se comporta como uma média de muitos sorteios. Quando a cauda é
    gorda --- e ela é, porque o estado escondido às vezes atravessa o experimento inteiro ---, a
    conta **subestima** o preço, e o número que vale é o medido por \texttt{separa}.
    """
    if diferenca <= 0.0 or desvio <= 0.0:
        raise ValueError("a diferenca e o desvio precisam ser positivos")
    if not 0.0 < confianca < 1.0:
        raise ValueError("a confianca precisa estar entre 0 e 1")
    z = NormalDist().inv_cdf(1.0 - (1.0 - confianca) / 2.0)
    return float((z * desvio / diferenca) ** 2)


def custo(repeticoes: float, contencao: int, espera: int) -> float:
    r"""Os dias de experimento: cada replicata segura o mundo e depois o observa."""
    return float(repeticoes) * (contencao + espera)


def desenho(rng: np.random.Generator, sigma: float, contensoes, espera: int, repeticoes: int,
            diferencas, aquecimento: int = AQUECIMENTO, confianca: float = CONFIANCA,
            **parametros) -> dict:
    r"""O preço de separar, varrendo quanto tempo se segura o mundo e o que se quer ver.

    Devolve, para cada contenção, a resposta medida nos dois mundos, a dispersão entre replicatas
    e --- para cada diferença declarada --- o número de replicatas e os dias de experimento. O
    melhor desenho é o mais barato que entrega a diferença declarada, e ele existe porque as duas
    pontas puxam para lados opostos: segurar mais fundo separa mais e custa mais por replicata,
    enquanto a dispersão cresce com o tempo de contenção no mundo de estado escondido.

    **Um desenho só vale onde a diferença existe.** Comprar replicatas para enxergar uma diferença
    que a contenção não produz é comprar um erro de leitura: o experimento sairia dizendo "não
    há diferença" com toda a confiança do mundo. Por isso cada diferença declarada vem com o
    veredito de viabilidade --- emph{d = 0,2} só é desenhável onde a resposta medida entrega ao
    menos isso ---, e o melhor desenho é o mais barato entre os viáveis. Ao lado dele vai o
    desenho emph{apertado}, que declara exatamente o que cada contenção entrega, e é o único que
    não depende de adivinhar a diferença antes de medir.
    """
    contensoes = [int(k) for k in contensoes]
    diferencas = [float(d) for d in diferencas]
    if not contensoes or not diferencas:
        raise ValueError("a varredura precisa de pelo menos uma contencao e uma diferenca")
    saida = {"contencoes": contensoes, "memoria_media": [], "memoria_desvio": [],
             "escondido_media": [], "escondido_desvio": [], "diferenca_medida": [],
             "desvio_somado": [], "diferencas": diferencas,
             "replicatas": {d: [] for d in diferencas},
             "dias": {d: [] for d in diferencas},
             "viavel": {d: [] for d in diferencas},
             "aperta_replicatas": [], "aperta_dias": [],
             "melhor": {}, "apertado": None, "inviavel": []}
    for k in contensoes:
        m = replicatas("memoria", rng, sigma, k, espera, repeticoes, aquecimento, **parametros)
        e = replicatas("escondido", rng, sigma, k, espera, repeticoes, aquecimento, **parametros)
        dm, de = float(m.mean()), float(e.mean())
        s = float(m.std(ddof=1) + e.std(ddof=1))
        saida["memoria_media"].append(dm)
        saida["memoria_desvio"].append(float(m.std(ddof=1)))
        saida["escondido_media"].append(de)
        saida["escondido_desvio"].append(float(e.std(ddof=1)))
        saida["diferenca_medida"].append(dm - de)
        saida["desvio_somado"].append(s)
        for d in diferencas:
            n = replicatas_necessarias(d, s, confianca)
            saida["replicatas"][d].append(n)
            saida["dias"][d].append(custo(n, k, espera))
            saida["viavel"][d].append(abs(saida["diferenca_medida"][-1]) >= d)
        justo = replicatas_necessarias(abs(saida["diferenca_medida"][-1]), s, confianca)
        saida["aperta_replicatas"].append(justo)
        saida["aperta_dias"].append(custo(justo, k, espera))
    for d in diferencas:
        viáveis = [i for i, ok in enumerate(saida["viavel"][d]) if ok]
        if not viáveis:
            saida["inviavel"].append(d)
            continue
        i = min(viáveis, key=lambda j: saida["dias"][d][j])
        saida["melhor"][d] = {"contencao": contensoes[i], "replicatas": saida["replicatas"][d][i],
                              "dias": saida["dias"][d][i]}
    i = int(np.argmin(saida["aperta_dias"]))
    saida["apertado"] = {"contencao": contensoes[i], "diferenca": abs(saida["diferenca_medida"][i]),
                         "replicatas": saida["aperta_replicatas"][i],
                         "dias": saida["aperta_dias"][i]}
    return saida


def separa(rng: np.random.Generator, sigma: float, contencao: int, espera: int, repeticoes: float,
           aquecimento: int = AQUECIMENTO, meta: int = 60, confianca: float = CONFIANCA,
           **parametros) -> dict:
    r"""A promessa do desenho, medida: com esse número de replicatas, quantas vezes separa.

    É a conferência que falta em todo desenho de experimento --- a conta diz que \emph{n}
    replicatas bastam, e esta função repete o experimento inteiro \emph{meta} vezes para ver com
    que frequência os dois intervalos de fato deixam de se cruzar. Um desenho que promete
    noventa e cinco por cento e entrega cinquenta não separa nada, e só a repetição mostra isso.
    """
    n = int(np.ceil(repeticoes))
    z = NormalDist().inv_cdf(1.0 - (1.0 - confianca) / 2.0)
    separou = 0
    for _ in range(meta):
        m = replicatas("memoria", rng, sigma, contencao, espera, n, aquecimento, **parametros)
        e = replicatas("escondido", rng, sigma, contencao, espera, n, aquecimento, **parametros)
        raio = z * (m.std(ddof=1) + e.std(ddof=1)) / np.sqrt(n)
        if abs(m.mean() - e.mean()) > raio:
            separou += 1
    return {"meta": meta, "repeticoes": n, "separacoes": separou,
            "fracao": separou / float(meta), "confianca": confianca}
