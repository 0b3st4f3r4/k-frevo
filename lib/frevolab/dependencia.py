r"""Dependência: quando as coisas ruins vêm juntas.

Família C. Os capítulos anteriores mediram uma série por vez: o corte, o vigia, a célula do
calendário. Todos leem **uma** margem, e é por isso que nenhum deles pode ver o que este
módulo mede.

**O fracasso que o abre.** Proteger cada mercado no seu próprio corte de 5% e supor que a
proteção conjunta é a soma das duas. Num par de mercados reais, os dois rompem juntos 7,3 vezes
mais do que a independência prevê — e o número não aparece em nenhuma das duas séries.

**A medida.** Junte as duas séries, conte os dias em que **as duas** rompem o próprio corte, e
compare com o que a independência prevê: o produto das duas taxas. A razão entre os dois é o
instrumento, e ele tem a vantagem de não supor nada sobre a forma da dependência — não é
correlação, não é cópula, é contagem.

**O defeito que este módulo torna impossível.** Ler a dependência na margem. O \emph{pareamento}
— qual dia de uma série anda com qual dia da outra — não muda nenhum dos dois números de cada
série, e muda tudo o que se pode perder junto. Por isso \texttt{pareado} existe: desloca uma das
séries e deixa a outra exatamente onde estava, de modo que a experiência possa mostrar que a
margem não se mexeu e a conta conjunta desabou.

**A continuação que a identificação pede.** A contagem da junta assina quatro cantos e
nenhum ponto a mais: a \emph{subcópula} mede esses cantos, a \emph{família de extensões}
constrói um subconjunto explícito das medidas duplamente estocásticas que os casam, e o
\emph{conjunto identificado} devolve o intervalo que esse subconjunto assina em cada nível de
corte. O defeito que elas tornam impossível: casar a família na margem nominal em vez da
medida --- cada membro carrega o resíduo contra a massa-alvo, e resíduo grande é erro de
construção, não largura de família.
"""
import math

import numpy as np
import pandas as pd
from scipy.integrate import quad
from scipy.special import ndtr as _ndtr, ndtri as _ndtri
from scipy.stats import chi2 as _chi2
from scipy.stats import t as _t

from . import promessa

JANELA_EPISODIO = 5

__all__ = ["JANELA_EPISODIO", "rompimentos", "pareado", "juntos", "episodios_dirigidos",
           "bloco_conjunto", "carteira", "perda_media", "subcopula", "familia_compativel",
           "conjunto_identificado"]


def rompimentos(serie: pd.Series, janela: int = 252, cauda: float = promessa.CAUDA_PADRAO) -> pd.Series:
    r"""Os dias em que a série rompeu o próprio corte, pelos dias de graça do capítulo 3."""
    return promessa.violacoes(serie, janela, cauda)


def pareado(serie: pd.Series, atraso: int) -> pd.Series:
    r"""A mesma série, pareada de outro jeito: cada valor anda com o dia \emph{atraso} depois.

    Não é uma série nova, e é isso que importa. Os valores são os mesmos, na mesma ordem, com os
    mesmos rompimentos; o que o deslocamento troca é o \emph{par} — qual dia de uma série encontra
    qual dia da outra. Com atraso zero o par é o que o mundo fez; com qualquer outro, é um par
    que o mundo não fez, e a diferença entre os dois é a dependência.
    """
    if atraso == 0:
        return serie
    valores = np.roll(np.asarray(serie, dtype=float), atraso)
    return pd.Series(valores, index=serie.index)


def juntos(rompe_a: pd.Series, rompe_b: pd.Series) -> dict:
    r"""Quantos dias os dois romperam, contra o que a independência previria.

    Devolve as duas taxas marginais, a taxa conjunta, o produto delas e a razão entre o medido e
    o previsto. A razão vale 1 quando não há nada além de coincidência, e cresce com a
    dependência; ela não exige supor normalidade nem forma nenhuma de cópula, porque é contagem
    sobre as datas em que as duas séries existem.
    """
    comuns = rompe_a.index.intersection(rompe_b.index)
    if comuns.empty:
        raise ValueError("as duas series nao tem datas em comum")
    a = rompe_a.loc[comuns].astype(bool)
    b = rompe_b.loc[comuns].astype(bool)
    taxa_a, taxa_b = float(a.mean()), float(b.mean())
    taxa_juntos = float((a & b).mean())
    esperado = taxa_a * taxa_b
    return {
        "dias": int(a.size),
        "rompe_a": int(a.sum()),
        "rompe_b": int(b.sum()),
        "taxa_a": taxa_a,
        "taxa_b": taxa_b,
        "juntos": int((a & b).sum()),
        "taxa_juntos": taxa_juntos,
        "esperado": esperado,
        "esperado_dias": float(esperado * a.size),
        "excesso": float(taxa_juntos / esperado) if esperado > 0 else float("nan"),
        "acompanhados": float((a & b).sum() / a.sum()) if a.sum() else float("nan"),
    }


def episodios_dirigidos(rompe_a: pd.Series, rompe_b: pd.Series,
                        janela: int = JANELA_EPISODIO) -> dict:
    r"""Quem rompeu primeiro, e se o outro veio atrás dentro da janela.

    Um episódio começa no dia em que **uma** das pernas rompe, desde que nenhum episódio tenha
    começado nos \emph{janela} dias anteriores: rompimentos dentro desses dias não abrem episódio
    novo. Se a outra perna romper dentro dos \emph{mesmos} \emph{janela} dias seguintes, o episódio
    é **dirigido**, e a primeira perna é a que liderou. O que se conta é a diferença entre os
    episódios liderados por uma e os liderados pela outra, dividida pelo total.

    A distinção é fina e já custou um defeito: o relógio da espera reinicia quando um episódio
    **começa**, e não a cada rompimento. Quem escreve "nenhum rompimento nos dias anteriores"
    descreve uma regra que este código não executa --- e mede vinte e seis episódios onde ele mede
    trinta e cinco. A asserção do \emph{auto\_teste} fixa a regra, e a prosa do capítulo diz a
    mesma coisa.

    A regra tem um viés próprio, e ele precisa ser declarado: a espera olha para trás e a
    detecção olha para a frente, de modo que **num par sem adiantamento nenhum** os dois lados já
    não saem iguais. Por isso o número do par real só vale contra o número dos pares sorteados, e
    nunca contra zero --- é a mesma regra dos capítulos do orçamento e da direção.

    Pelo mesmo motivo a inversão do relógio não serve de conferência aqui: virar o mundo ao
    contrário não vira a regra. Quem confere este instrumento é o nulo, que carrega a mesma regra.
    """
    if janela < 1:
        raise ValueError("a janela do episodio precisa de pelo menos um dia")
    comuns = rompe_a.index.intersection(rompe_b.index)
    if comuns.empty:
        raise ValueError("as duas series nao tem datas em comum")
    a = rompe_a.loc[comuns].astype(bool).to_numpy()
    b = rompe_b.loc[comuns].astype(bool).to_numpy()
    lider_a = lider_b = sozinho_a = sozinho_b = juntos_ = 0
    ultimo = -10 ** 9
    for t in range(a.size):
        if not (a[t] or b[t]):
            continue
        if t - ultimo <= janela:
            continue
        ultimo = t
        if a[t] and b[t]:
            # romperam no mesmo dia: não há primeiro, e contar isso como episódio de um dos lados
            # inventaria uma direção que o dado não tem.
            juntos_ += 1
            continue
        futuro = slice(t + 1, min(a.size, t + 1 + janela))
        outra = b[futuro] if a[t] else a[futuro]
        if not outra.any():
            if a[t]:
                sozinho_a += 1
            else:
                sozinho_b += 1
        elif a[t]:
            lider_a += 1
        else:
            lider_b += 1
    dirigidos = lider_a + lider_b
    return {"dias": int(a.size), "lider_a": lider_a, "lider_b": lider_b,
            "sozinho_a": sozinho_a, "sozinho_b": sozinho_b, "juntos": juntos_,
            "dirigidos": dirigidos,
            "assimetria": (lider_a - lider_b) / dirigidos if dirigidos else float("nan")}


def bloco_conjunto(retornos_a: pd.Series, retornos_b: pd.Series, janela: int = 252,
                   cauda: float = promessa.CAUDA_PADRAO, bloco: int = 60) -> pd.Series:
    r"""Quantos dias os dois romperam o proprio corte, contados em blocos moveis.

    E o instrumento da dependencia: a margem de cada perna nao se mexe quando o par muda, mas a
    contagem conjunta se mexe. O bloco existe pelo mesmo motivo do capitulo 2 --- o que o mundo
    faz aparece na forma com que os dias ruins chegam, e nao na media.
    """
    a = rompimentos(retornos_a, janela, cauda)
    b = rompimentos(retornos_b, janela, cauda)
    comuns = a.index.intersection(b.index)
    juntos = a.loc[comuns].astype(float) * b.loc[comuns].astype(float)
    return promessa.conta_em_blocos(juntos, bloco)


def carteira(retornos_a: pd.Series, retornos_b: pd.Series, peso: float = 0.5) -> pd.Series:
    r"""A carteira de peso fixo nas duas pernas, pelos dias em que as duas existem."""
    comuns = retornos_a.index.intersection(retornos_b.index)
    if comuns.empty:
        raise ValueError("as duas series nao tem datas em comum")
    return peso * retornos_a.loc[comuns] + (1.0 - peso) * retornos_b.loc[comuns]


def perda_media(carteira: pd.Series, mascara: pd.Series) -> float:
    r"""A perda média da carteira nos dias marcados pela máscara.

    É a peça que o capítulo precisa para dizer o que a proteção individual não cobre: a perda
    média no dia em que as duas pernas rompem, contra a perda média no dia em que só uma rompe.
    """
    comuns = carteira.index.intersection(mascara.index)
    if comuns.empty:
        raise ValueError("a mascara e a carteira nao tem datas em comum")
    selecionados = carteira.loc[comuns][mascara.loc[comuns].astype(bool)]
    if selecionados.empty:
        raise ValueError("a mascara nao seleciona dia nenhum")
    return float(selecionados.mean())


# --- a cópula que a contagem não escolhe: subcópula, família e conjunto identificado ---

def subcopula(rompe_a: pd.Series, rompe_b: pd.Series) -> dict:
    r"""O que a contagem assina na grade das margens: os quatro cantos da subcópula.

    A margem deste capítulo é binária --- o dia rompe o corte ou não rompe ---, e a
    probabilidade integral de uma margem binária só visita três pontos: zero, o ponto em
    que ela salta e um. Lida nessa grade, a junta inteira se decide em quatro cantos: os
    dois que cada margem assina sozinha, o canto do um, e o canto de \emph{dia nenhum},
    único que a contagem conjunta assina. É pouco, e é tudo: a subcópula carrega esse
    pouco sem inventar o resto --- e sem escolher membro nenhum da família que o estende.

    Devolve as taxas marginais medidas, a massa do retângulo em que as duas rompem, os
    quatro cantos na grade das margens e a contagem que assina cada um. A margem casada é
    sempre a \emph{medida} --- a taxa que o dado entregou ---, e nunca a nominal: casar na
    nominal é o defeito que o resíduo da família pega, porque nenhum membro devolveria a
    massa-alvo.
    """
    comuns = rompe_a.index.intersection(rompe_b.index)
    if comuns.empty:
        raise ValueError("as duas series nao tem datas em comum")
    a = rompe_a.loc[comuns].astype(bool).to_numpy()
    b = rompe_b.loc[comuns].astype(bool).to_numpy()
    taxa_a, taxa_b = float(a.mean()), float(b.mean())
    if not 0.0 < taxa_a < 1.0 or not 0.0 < taxa_b < 1.0:
        raise ValueError("a grade exige margem com rompimento e com dia comum "
                         "(taxa estritamente entre zero e um em cada perna)")
    nenhum = int((~a & ~b).sum())
    somente_a = int((a & ~b).sum())
    somente_b = int((~a & b).sum())
    juntos_ = int((a & b).sum())
    massa = juntos_ / a.size
    return {
        "dias": int(a.size),
        "taxa_a": taxa_a,
        "taxa_b": taxa_b,
        "u_a": 1.0 - taxa_a,
        "u_b": 1.0 - taxa_b,
        "massa_retangulo": float(massa),
        "canto_nenhum": 1.0 - taxa_a - taxa_b + massa,
        "canto_margem_a": 1.0 - taxa_a,
        "canto_margem_b": 1.0 - taxa_b,
        "canto_tudo": 1.0,
        "contagem": {"nenhum": nenhum, "somente_a": somente_a,
                     "somente_b": somente_b, "juntos": juntos_},
    }


def _normal_binaria(rho: float, x: float, y: float) -> float:
    r"""A acumulada normal bivariada de correlação \emph{rho} em (\emph{x}, \emph{y}).

    Pela fórmula de Plackett: a acumulada é o produto das marginais mais a integral da
    densidade bivariada, integrada de correlação zero até \emph{rho}. É quadratura
    determinística de função suave --- sem sorteio nenhum, porque a família inteira não
    sorteia: a correlação de cada membro é resolvida, não estimada.
    """
    if rho <= -1.0 + 1e-12:
        return max(_ndtr(x) + _ndtr(y) - 1.0, 0.0)
    if rho >= 1.0 - 1e-12:
        return min(_ndtr(x), _ndtr(y))

    def densidade(t):
        um_menos = 1.0 - t * t
        expoente = -(x * x - 2.0 * t * x * y + y * y) / (2.0 * um_menos)
        return math.exp(expoente) / (2.0 * math.pi * math.sqrt(um_menos))

    integral, _ = quad(densidade, 0.0, rho, epsabs=1e-13, epsrel=1e-13, limit=200)
    return _ndtr(x) * _ndtr(y) + integral


def _cdf_gaussiana(rho: float, u: float, v: float) -> float:
    r"""A cópula gaussiana de correlação \emph{rho}, lida em (\emph{u}, \emph{v})."""
    if u <= 0.0 or v <= 0.0:
        return 0.0
    if u >= 1.0:
        return v
    if v >= 1.0:
        return u
    if rho <= -1.0 + 1e-12:
        return max(u + v - 1.0, 0.0)
    if rho >= 1.0 - 1e-12:
        return min(u, v)
    return _normal_binaria(rho, _ndtri(u), _ndtri(v))


def _cdf_t(nu: float, rho: float, u: float, v: float) -> float:
    r"""A cópula t de \emph{nu} graus de liberdade e correlação \emph{rho}, em (\emph{u}, \emph{v}).

    A t bivariada é uma mistura de escala da normal: o denominador comum vem de uma
    qui-quadrado, e a acumulada é a esperada da acumulada normal sobre ela. A esperada sai
    por quadratura no quantil da qui-quadrado --- determinística ---, com a escala
    limitada, para o extremo da quadratura não produzir infinito vezes zero.
    """
    if u <= 0.0 or v <= 0.0:
        return 0.0
    if u >= 1.0:
        return v
    if v >= 1.0:
        return u
    if rho <= -1.0 + 1e-12:
        return max(u + v - 1.0, 0.0)
    if rho >= 1.0 - 1e-12:
        return min(u, v)
    x, y = _t.ppf(u, nu), _t.ppf(v, nu)

    def esperada(quantil):
        escala = min(math.sqrt(_chi2.ppf(quantil, nu) / nu), 1e12)
        return _normal_binaria(rho, x * escala, y * escala)

    integral, _ = quad(esperada, 0.0, 1.0, epsabs=1e-13, epsrel=1e-13, limit=200)
    return integral


def _rho_do_canto(cdf, u: float, v: float, alvo: float) -> float:
    r"""A correlação que faz a cópula valer \emph{alvo} em (\emph{u}, \emph{v}), por bisseção.

    A acumulada cresce com a correlação --- a derivada é a densidade, que não é negativa
    ---, e o alvo está dentro das bordas de Fréchet: a bisseção converge sem sorteio e sem
    inicialização. No alvo que encosta numa borda devolve a borda, porque toda cópula
    coincide com as duas.
    """
    piso, teto = max(u + v - 1.0, 0.0), min(u, v)
    if alvo <= piso + 1e-14:
        return -1.0
    if alvo >= teto - 1e-14:
        return 1.0
    baixo, alto = -1.0, 1.0
    for _ in range(200):
        meio = 0.5 * (baixo + alto)
        valor = cdf(meio, u, v)
        if abs(valor - alvo) < 1e-13:
            return meio
        if valor < alvo:
            baixo = meio
        else:
            alto = meio
        if alto - baixo < 1e-14:
            break
    return 0.5 * (baixo + alto)


def familia_compativel(u_a: float, u_b: float, massa: float,
                       nus: tuple = (2.0, 4.0, 8.0)) -> list:
    r"""Um subconjunto explícito e declarado das extensões duplamente estocásticas da subcópula.

    O teorema garante que toda medida duplamente estocástica que casa os quatro cantos é
    uma cópula legítima das margens da contagem --- e são infinitas. Esta função constrói
    um subconjunto finito e declarado delas: a gaussiana, uma t para cada elemento de
    \emph{nus} e a mistura das duas bordas (comonótone e anti), com o peso resolvido pela
    linearidade da massa no canto. A correlação de cada membro sai por bisseção no canto
    que a contagem assina, e cada membro carrega o resíduo contra a massa-alvo: resíduo
    grande é erro de construção, não largura de família. O subconjunto não é a família do
    teorema --- é o que se escreve para ler a banda sem escolher membro.
    """
    if not 0.0 < u_a < 1.0 or not 0.0 < u_b < 1.0:
        raise ValueError("os pontos da grade precisam ser interiores ao intervalo aberto")
    if not nus:
        raise ValueError("a familia declarada precisa de pelo menos um grau de liberdade")
    if any(nu <= 0.0 for nu in nus):
        raise ValueError("os graus de liberdade precisam ser positivos")
    piso = max((1.0 - u_a) + (1.0 - u_b) - 1.0, 0.0)
    teto = min(1.0 - u_a, 1.0 - u_b)
    if not piso - 1e-12 <= massa <= teto + 1e-12:
        raise ValueError("massa %g fora das bordas de Frechet [%g, %g] para essas margens"
                         % (massa, piso, teto))
    massa = min(max(massa, piso), teto)
    alvo = u_a + u_b - 1.0 + massa
    membros = []
    rho = _rho_do_canto(lambda r, u, v: _cdf_gaussiana(r, u, v), u_a, u_b, alvo)
    membros.append({"nome": "gaussiana", "familia": "gaussiana", "correlacao": rho,
                    "cdf": lambda u, v, r=rho: _cdf_gaussiana(r, u, v)})
    for nu in nus:
        rho = _rho_do_canto(lambda r, u, v, n=nu: _cdf_t(n, r, u, v), u_a, u_b, alvo)
        membros.append({"nome": "t_%s" % ("%g" % nu), "familia": "t",
                        "nu": float(nu), "correlacao": rho,
                        "cdf": lambda u, v, r=rho, n=float(nu): _cdf_t(n, r, u, v)})
    borda_baixa, borda_alta = max(u_a + u_b - 1.0, 0.0), min(u_a, u_b)
    peso = (alvo - borda_baixa) / (borda_alta - borda_baixa)
    membros.append({"nome": "mistura", "familia": "mistura", "peso": peso,
                    "cdf": lambda u, v, w=peso: w * min(u, v)
                    + (1.0 - w) * max(u + v - 1.0, 0.0)})
    for membro in membros:
        membro["canto"] = float(membro["cdf"](u_a, u_b))
        membro["residuo"] = abs(membro["canto"] - alvo)
    return membros


def conjunto_identificado(membros: list, niveis) -> dict:
    r"""O intervalo que a família inteira assina na diagonal, em cada nível de corte.

    No corte de nível \emph{q}, a taxa conjunta que um membro prevê é a leitura da
    diagonal do canto de cima: a acumulada no ponto \emph{um menos q} de cada margem, mais
    duas vezes o nível, menos um. A identidade vive aqui --- e não no caderno --- porque é
    o lugar onde um sinal trocado passa sem ninguém ver. O dicionário devolvido tem, para
    cada nível, a taxa de cada membro, o mínimo, o máximo e a razão entre os dois.
    """
    if not membros:
        raise ValueError("a familia nao pode ser vazia")
    niveis = tuple(niveis)
    if not niveis:
        raise ValueError("a varredura precisa de pelo menos um nivel")
    saida = {}
    for nivel in niveis:
        if not 0.0 < nivel < 0.5:
            raise ValueError("o nivel %g precisa estar entre zero e meio" % nivel)
        taxas = {}
        for membro in membros:
            canto = float(membro["cdf"](1.0 - nivel, 1.0 - nivel))
            taxa = canto + 2.0 * nivel - 1.0
            if taxa < -1e-9 or taxa > nivel + 1e-9:
                raise ValueError("membro %s fora das bordas do par no nivel %g (taxa %g): "
                                 "erro de leitura da diagonal" % (membro.get("nome", "?"), nivel, taxa))
            taxas[membro["nome"]] = max(taxa, 0.0)
        minimo, maximo = min(taxas.values()), max(taxas.values())
        saida[float(nivel)] = {"taxas": taxas, "minimo": minimo, "maximo": maximo,
                               "razao": (maximo / minimo) if minimo > 0.0 else float("inf")}
    return saida
