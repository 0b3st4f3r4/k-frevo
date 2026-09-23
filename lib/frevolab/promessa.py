r"""Promessa e entrega: o corte, a conta que ele assina sozinho e o que ele paga.

O capítulo da raiz faz uma tentativa e a desmonta. A tentativa é a de todo dia: olhar o
último ano, pegar os piores dias, e anunciar "não passo daqui". O que este módulo mede é a
distância entre o que se anuncia e o que se entrega — e ele existe porque essa distância
tem duas partes de naturezas diferentes:

1. **a conta do corte** — a parte que não depende do mundo. Escolher a janela de \emph{n}
   dias e cortar no \emph{k}-ésimo pior assina, sozinho, uma taxa de k/(n+1). Quem pede
   5% e escolhe o 13º pior de 252 não pediu 5%: pediu 13/253 = 5,14%. Nenhum dado conserta
   essa aritmética, porque ela não veio do dado;
2. **o bloco** — a parte que é do mundo. A taxa média de violações não distingue uma série
   real de uma série que nunca mudou; a contagem em blocos móveis distingue na hora.

Por isso o resumo que este módulo devolve traz as duas leituras lado a lado. Ler só a
primeira é o defeito que o capítulo desmonta: a média é assinada pelo corte, então ela não
é evidência sobre o mundo — é evidência sobre a escolha.

**Um defeito que este módulo torna impossível.** Numa implementação ingênua, os primeiros
\emph{janela} dias, onde o corte ainda não existe, entram na conta como dias sem violação
(em \texttt{pandas}, comparar com \texttt{NaN} devolve \texttt{False}). São dias de graça,
e eles derrubam a taxa: com janela de 252 em 6718 dias, 3,75% de graça, o que transforma
5,14% em 4,95% — perto o bastante do prometido para parecer que a promessa foi cumprida.
`violacoes` devolve só os dias em que o corte existe, e o teste de propriedade confere
esse comprimento.
"""
import numpy as np
import pandas as pd

CAUDA_PADRAO = 0.05
BLOCO_PADRAO = 60

__all__ = ["CAUDA_PADRAO", "BLOCO_PADRAO", "posto", "corte", "corte_no_posto",
           "violacoes", "violacoes_no_posto", "entrega_do_corte", "conta_em_blocos",
           "episodios_acima", "entrega"]


def posto(janela: int, cauda: float = CAUDA_PADRAO) -> int:
    r"""Qual dos piores da janela é o corte: k = teto(cauda * janela).

    É este inteiro, e não a cauda, que decide a conta: 5% de 252 dá 12,6, e não existe o
    12,6-ésimo pior dia de um ano. Arredondar para cima é a escolha conservadora — corta no
    13º —, e é ela que faz a promessa anunciada de 5% valer, na aritmética do corte, 5,14%.
    """
    if janela < 2:
        raise ValueError("a janela precisa de pelo menos dois dias")
    if not 0.0 < cauda < 0.5:
        raise ValueError("a cauda precisa estar entre 0 e 0,5")
    return int(np.ceil(cauda * janela))


def corte_no_posto(retornos: pd.Series, janela: int, k: int) -> pd.Series:
    r"""O \emph{k}-ésimo pior dos \emph{janela} retornos que terminam ontem, dia a dia.

    O valor em \emph{t} usa \emph{t-janela} a \emph{t-1} e nada depois: a barra é erguida
    antes de o dia acontecer. Os primeiros \emph{janela} dias ficam sem corte, e é isso que
    o \texttt{NaN} declara — quem consome precisa respeitar esse vazio em vez de tratá-lo
    como zero.

    Esta é a forma crua, com o posto \emph{k} na mão. A cauda é uma maneira de escolher
    \emph{k}; o orçamento de erro (\texttt{orcamento.py}) é outra, e é por isso que o posto
    fica separado aqui da regra que o escolhe: \emph{k} é a decisão, \emph{n} é a memória.
    """
    if janela < 2:
        raise ValueError("a janela precisa de pelo menos dois dias")
    if not 1 <= k <= janela:
        raise ValueError("o posto precisa estar entre 1 e a janela (%d)" % janela)
    valores = np.asarray(retornos, dtype=float)
    saida = np.full(valores.size, np.nan)
    if valores.size > janela:
        janelas = np.lib.stride_tricks.sliding_window_view(valores, janela)
        de_cada_janela = np.partition(janelas, k - 1, axis=1)[:, k - 1]
        saida[janela:] = de_cada_janela[:-1]
    return pd.Series(saida, index=retornos.index, name="corte")


def violacoes_no_posto(retornos: pd.Series, janela: int, k: int) -> pd.Series:
    r"""Onde o dia ficou abaixo do \emph{k}-ésimo pior da janela, só onde o corte existe.

    A série devolvida tem exatamente \texttt{len(retornos) - janela} entradas: os dias de
    graça não entram, porque um dia em que não havia barra não é um dia em que a barra
    resistiu.
    """
    linha = corte_no_posto(retornos, janela, k).to_numpy()
    existe = ~np.isnan(linha)
    abaixo = np.asarray(retornos, dtype=float) < linha
    return pd.Series(abaixo[existe], index=retornos.index[existe], name="violacao")


def corte(retornos: pd.Series, janela: int, cauda: float = CAUDA_PADRAO) -> pd.Series:
    r"""O corte por cauda: o \emph{posto} que a cauda escolhe, na janela declarada."""
    return corte_no_posto(retornos, janela, posto(janela, cauda))


def violacoes(retornos: pd.Series, janela: int, cauda: float = CAUDA_PADRAO) -> pd.Series:
    r"""As violações por cauda: a taxa anunciada escolhendo o posto."""
    return violacoes_no_posto(retornos, janela, posto(janela, cauda))


def entrega_do_corte(janela: int, cauda: float = CAUDA_PADRAO) -> float:
    r"""A taxa que o corte assina sozinho: k/(janela + 1).

    Vale para qualquer lei contínua, e a prova é curta: se a janela tem \emph{n} dias
    independentes e o corte é o \emph{k}-ésimo pior deles, a posição de um dia novo entre
    os \emph{n+1} é uniforme, e a probabilidade de ele ficar abaixo do corte é k/(n+1) —
    sem o mundo aparecer na conta. É por isso que a média não é evidência sobre o mundo: ela
    já estava assinada antes de qualquer dado chegar.
    """
    return posto(janela, cauda) / (janela + 1)


def conta_em_blocos(violacoes_serie: pd.Series, bloco: int = BLOCO_PADRAO) -> pd.Series:
    r"""Quantas violações em cada bloco móvel de \emph{bloco} dias.

    O bloco é a leitura que o corte não assina: se o mundo não mudasse, o pior bloco de uma
    série longa ficaria perto da promessa; quando ele passa longe, alguma coisa no mundo
    mudou.
    """
    if bloco < 1:
        raise ValueError("o bloco precisa de pelo menos um dia")
    return violacoes_serie.astype(float).rolling(bloco).sum().dropna()


def episodios_acima(contagem: pd.Series, limite: float) -> list:
    r"""Os trechos em que o bloco passou do \emph{limite}, agrupados em episódios.

    Blocos móveis consecutivos acima do limite são o mesmo acontecimento: contar cada bloco
    como um evento multiplicaria por sessenta a mesma crise. O que se conta aqui é quantas
    vezes o mundo passou do teto — e o número que sai disso costuma ser maior do que a
    memória sugere, porque nem toda vez que o mundo muda tem nome de crise.
    """
    valores = contagem.to_numpy(dtype=float)
    acima = valores > limite
    if not acima.any():
        return []
    # um episódio começa onde o bloco entra acima do limite e termina onde ele sai: blocos
    # móveis consecutivos são o mesmo acontecimento, não vários.
    comeca = np.flatnonzero(acima & ~np.concatenate(([False], acima[:-1])))
    termina = np.flatnonzero(acima & ~np.concatenate((acima[1:], [False])))
    return [{"inicio": contagem.index[i], "fim": contagem.index[f],
             "pico": float(valores[i:f + 1].max())}
            for i, f in zip(comeca, termina)]


def entrega(retornos: pd.Series, janela: int, cauda: float = CAUDA_PADRAO,
            bloco: int = BLOCO_PADRAO) -> dict:
    r"""As duas leituras de uma vez: a taxa média e o pior bloco, com a data dele.

    A taxa média vem junto com \texttt{assinado}, que é a conta do corte, justamente para
    que ninguém leia a média sozinha: a diferença entre as duas é o pouco que sobra para o
    mundo dizer, e o bloco é onde ele diz.
    """
    v = violacoes(retornos, janela, cauda)
    contagem = conta_em_blocos(v, bloco)
    prometido = bloco * cauda
    # a data do pior bloco só existe quando o índice é de datas; série de teste tem
    # índice de posição, e ali o rótulo é a própria posição.
    pior = contagem.idxmax() if not contagem.empty else None
    rotulo = "—" if pior is None else (str(pior.date()) if hasattr(pior, "date") else str(pior))
    return {
        "dias": int(v.size),
        "violacoes": int(v.sum()),
        "taxa": float(v.mean()),
        "assinado": float(entrega_do_corte(janela, cauda)),
        "bloco_prometido": float(prometido),
        "bloco_mediana": float(contagem.median()) if not contagem.empty else float("nan"),
        "bloco_pior": int(contagem.max()) if not contagem.empty else 0,
        "bloco_pior_data": rotulo,
        "bloco_acima_do_dobro": float((contagem > 2 * prometido).mean()),
    }
