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
"""
import numpy as np
import pandas as pd

from . import promessa

JANELA_EPISODIO = 5

__all__ = ["JANELA_EPISODIO", "rompimentos", "pareado", "juntos", "episodios_dirigidos",
           "bloco_conjunto", "carteira", "perda_media"]


def rompimentos(serie: pd.Series, janela: int = 252, cauda: float = promessa.CAUDA_PADRAO) -> pd.Series:
    r"""Os dias em que a série rompeu o próprio corte, pelos dias de graça do capítulo 2."""
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
