r"""A partilha do relógio: proteger e acompanhar disputam o mesmo orçamento.

A pergunta da travessia é se recalibrar a barreira compete com atualizar o modelo. A resposta
começa por separar o que a barreira tem dentro, porque são duas coisas com pressas diferentes:

1. **a escala** --- o nível da oscilação, que muda depressa e é o que uma mudança de verdade mexe;
2. **a forma** --- o corte padronizado, que diz quantos desvios acima da escala fica a barreira, e
   que muda devagar, porque padronizar já tirou dele o que a escala carregava.

Uma barreira é o produto dos dois. Depois de uma mudança que dobra a oscilação, o nível está
errado por um fator dois e a forma continua valendo; é essa assimetria que decide quem consome o
orçamento de atualizações.

**O defeito que este módulo torna impossível.** Tratar proteger e acompanhar como dois
consumidores simétricos do mesmo relógio, e repartir o orçamento meio a meio. O que a medição
mostra é que as duas pressas não têm a mesma ordem: a escala pede atualização quase cinco vezes mais
atualizar a forma todo dia custam o mesmo em trabalho, e o segundo gasto não compra quase nada. Em
compensação, o módulo também mostra o outro lado: enquanto o orçamento for folgado, a partilha não
morde, e a competição que a pergunta supõe só aparece quando o orçamento fica pobre.

A perda usada aqui é a que a barreira **não** segurou: a soma do que passou por cima dela, dia a
dia. É a moeda natural de quem protege, e é a mesma nos dois ingredientes, de modo que a
comparação não depende de declarar um câmbio entre coisas diferentes.
"""
import numpy as np

JANELA_NIVEL = 21
JANELA_CORTE = 252
POSTO = 13
HORIZONTE = 500

__all__ = ["JANELA_NIVEL", "JANELA_CORTE", "POSTO", "HORIZONTE", "padronizado", "absorvido",
           "ciclos", "perdas", "partilha"]


def padronizado(serie: np.ndarray, janela_nivel: int = JANELA_NIVEL) -> np.ndarray:
    r"""A série dividida pela escala que se conhecia **antes** dela.

    O nível de cada dia é a média dos \emph{janela\_nivel} dias anteriores, e o próprio dia não
    entra na conta. Sem essa separação a padronização olharia para a frente, e o corte extraído
    dela saberia o que ia acontecer --- que é o defeito que o primeiro capítulo tornou impossível.
    """
    s = np.asarray(serie, dtype=float)
    if janela_nivel < 2:
        raise ValueError("a janela do nivel precisa de pelo menos dois dias")
    if s.size <= janela_nivel:
        raise ValueError("a serie precisa ser maior que a janela do nivel")
    acumulado = np.concatenate([[0.0], np.cumsum(s)])
    nivel = np.full(s.size, np.nan)
    nivel[janela_nivel:] = (acumulado[janela_nivel:-1] - acumulado[:-(janela_nivel + 1)]) / janela_nivel
    if np.any(nivel[janela_nivel:] <= 0.0):
        raise ValueError("o nivel precisa ser positivo: a serie tem que ser de oscilacao, nao de resto")
    return s / nivel


def absorvido(serie: np.ndarray, ciclo_nivel: int, ciclo_corte: int,
              janela_nivel: int = JANELA_NIVEL, janela_corte: int = JANELA_CORTE,
              posto: int = POSTO, inicio: int = 0, horizonte: int = HORIZONTE) -> float:
    r"""A perda média por dia que a barreira deixou passar.

    Cada ingrediente é recalculado no seu ciclo --- de quantos em quantos dias alguém paga o
    trabalho de refazê-lo ---, e entre uma atualização e a seguinte vale o valor antigo. A
    barreira do dia é o produto da escala pela forma; o que passa por cima dela é a perda.
    """
    s = np.asarray(serie, dtype=float)
    if ciclo_nivel < 1 or ciclo_corte < 1:
        raise ValueError("os ciclos sao contados em dias e precisam ser pelo menos um")
    if inicio < max(janela_nivel, janela_corte + janela_nivel):
        raise ValueError("a avaliacao precisa comecar depois das janelas")
    if inicio + horizonte > s.size:
        raise ValueError("a avaliacao nao cabe na serie")
    forma = padronizado(s, janela_nivel)
    escala = s[inicio - janela_nivel:inicio].mean()
    corte = np.sort(forma[inicio - janela_corte:inicio])[-posto]
    total = 0.0
    for t in range(inicio, inicio + horizonte):
        if (t - inicio) % ciclo_nivel == 0:
            escala = s[t - janela_nivel:t].mean()
        if (t - inicio) % ciclo_corte == 0:
            corte = np.sort(forma[t - janela_corte:t])[-posto]
        total += max(0.0, s[t] - escala * corte)
    return total / horizonte


def ciclos(repeticoes_nivel: float, repeticoes_corte: float,
           horizonte: int = HORIZONTE) -> tuple:
    r"""Quantos dias separam duas atualizações de cada ingrediente.

    O orçamento é contado em **atualizações ao longo do horizonte**, que é o trabalho que alguém
    paga; o ciclo é o horizonte dividido por elas. Um orçamento de zero atualizações vira um ciclo
    do tamanho do horizonte: o ingrediente entra na avaliação com o valor que já tinha.
    """
    if repeticoes_nivel < 0.0 or repeticoes_corte < 0.0:
        raise ValueError("nao existe orcamento negativo")
    ciclo_nivel = max(1, int(round(horizonte / repeticoes_nivel))) if repeticoes_nivel > 0 else horizonte
    ciclo_corte = max(1, int(round(horizonte / repeticoes_corte))) if repeticoes_corte > 0 else horizonte
    return ciclo_nivel, ciclo_corte


def perdas(series, ciclo_nivel: int, ciclo_corte: int, janela_nivel: int = JANELA_NIVEL,
           janela_corte: int = JANELA_CORTE, posto: int = POSTO, inicio: int = 0,
           horizonte: int = HORIZONTE) -> tuple:
    r"""A perda média entre as séries sorteadas, e a dispersão entre elas.

    Uma perda medida num mundo só não é uma medida: a perda absorvida varia de sorteio para
    sorteio mais do que varia entre políticas vizinhas, e é a mesma regra que os capítulos
    anteriores já seguem --- sem dispersão, não se reporta.
    """
    series = [np.asarray(s, dtype=float) for s in series]
    if not series:
        raise ValueError("a medicao precisa de pelo menos uma serie")
    valores = np.array([absorvido(s, ciclo_nivel, ciclo_corte, janela_nivel, janela_corte, posto,
                                  inicio, horizonte) for s in series])
    if valores.size == 1:
        return float(valores[0]), 0.0
    return float(valores.mean()), float(valores.std(ddof=1))


def partilha(series, orcamentos, fracoes, janela_nivel: int = JANELA_NIVEL,
             janela_corte: int = JANELA_CORTE, posto: int = POSTO, inicio: int = 0,
             horizonte: int = HORIZONTE) -> dict:
    r"""A perda contra o orçamento, e contra a fração que vai para a escala.

    Devolve, para cada orçamento e cada fração, a perda média entre as séries sorteadas e a
    dispersão entre elas. A fração é a parte do orçamento que vai para a escala; o resto vai para
    a forma. Repartir meio a meio é o palpite simétrico, e é o que a medição põe à prova.
    """
    series = [np.asarray(s, dtype=float) for s in series]
    if not series:
        raise ValueError("a partilha precisa de pelo menos uma serie")
    saida = {"orcamentos": list(orcamentos), "fracoes": list(fracoes), "media": {}, "dispersao": {}}
    for orcamento in orcamentos:
        for fracao in fracoes:
            ciclo_nivel, ciclo_corte = ciclos(fracao * orcamento, (1.0 - fracao) * orcamento,
                                             horizonte)
            perdas = [absorvido(s, ciclo_nivel, ciclo_corte, janela_nivel, janela_corte, posto,
                                inicio, horizonte) for s in series]
            saida["media"][(orcamento, fracao)] = float(np.mean(perdas))
            saida["dispersao"][(orcamento, fracao)] = float(np.std(perdas, ddof=1)) if len(perdas) > 1 else 0.0
    return saida
