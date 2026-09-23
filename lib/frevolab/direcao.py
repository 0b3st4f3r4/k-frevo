r"""O vigia da direção: a assimetria do incremento, com orçamento de alarme.

A pergunta desta travessia é se a direção do tempo pode ser vigiada **com garantia**. O instrumento
é o mesmo do resto do livro --- um limiar e um orçamento declarado --- aplicado a um objeto novo: a
assimetria do incremento.

A conta mínima é esta. Se os incrementos fossem simétricos, o cubo deles teria média zero e a sua
média sobre \emph{n} dias teria desvio \emph{raiz de 15/n} --- o número sai de \emph{E[z^3] = 0} e
\emph{E[z^6] = 15} para um normal padrão, e é a proposição que o \texttt{auto\_teste} confere. Com
esse desvio, um limiar em unidades de desvio é um orçamento: \emph{z = 3} promete
\emph{2,7 por mil} blocos alarmados num mundo simétrico.

**O defeito que este módulo torna impossível.** Declarar o orçamento pela conta gaussiana e acreditar
nela. Num mundo com agrupamento de oscilação --- que é o mundo dos dados deste livro --- a dispersão
medida da estatística é maior do que a conta diz, e o vigia gasta mais alarmes do que prometeu. É a
mesma lição do orçamento do alarme e do preço do desenho, agora na direção do tempo: **o orçamento se
lê da medição, e não da álgebra**.

A estatística de cada bloco padroniza pela escala da **janela anterior**, nunca pela do próprio
bloco: quem se padroniza com os dias que está medindo já sabe a resposta antes de responder.
"""
import numpy as np

JANELA_PADRAO = 252
Z_PADRAO = 3.0

__all__ = ["JANELA_PADRAO", "Z_PADRAO", "assimetrico", "passos", "blocos", "resumo",
           "desvio_da_conta", "limiar", "momento_amostral", "invertida"]


def assimetrico(n: int, rng: np.random.Generator, sigma: float = 0.01, a: float = 0.0) -> np.ndarray:
    r"""Incrementos com assimetria declarada, e nada mais.

    A construção é \emph{u = z + a(z^2 - 1)}, com \emph{z} normal padrão, reescalada para que a
    variância continue sendo \emph{sigma} ao quadrado. O terceiro momento padronizado dessa
    família é \emph{(6a + 8a^3) / (1 + 2a^2) elevado a três meios}, de modo que \emph{a} é o botão
    da direção: em \emph{a = 0} o mundo é simétrico, e o vigia não deve achar nada nele.
    """
    if n < 2:
        raise ValueError("o mundo precisa de pelo menos dois incrementos")
    if sigma <= 0.0:
        raise ValueError("a escala precisa ser positiva")
    z = rng.normal(0.0, 1.0, n)
    return sigma * (z + a * (z ** 2 - 1.0)) / np.sqrt(1.0 + 2.0 * a ** 2)


def passos(serie: np.ndarray) -> np.ndarray:
    r"""Os incrementos de uma série: é neles que a direção mora."""
    s = np.asarray(serie, dtype=float)
    if s.size < 2:
        raise ValueError("a serie precisa de pelo menos dois pontos")
    return np.diff(s)


def invertida(serie: np.ndarray) -> np.ndarray:
    r"""A mesma série com o relógio ao contrário.

    É o controle do instrumento: se a medida da direção não troca de sinal quando o filme roda ao
    contrário, ela não está medindo direção nenhuma.
    """
    return np.asarray(serie, dtype=float)[::-1].copy()


def desvio_da_conta(janela: int = JANELA_PADRAO) -> float:
    r"""O desvio do nulo pela conta: raiz de 15 sobre a janela.

    Vale para incrementos simétricos de escala constante. Onde a escala muda, ele é o piso, e não a
    resposta --- e é a diferença entre os dois que o caderno mede.
    """
    if janela < 2:
        raise ValueError("a janela precisa de pelo menos dois dias")
    return float(np.sqrt(15.0 / janela))


def limiar(z: float = Z_PADRAO, janela: int = JANELA_PADRAO) -> float:
    r"""O limiar em unidades da estatística, para \emph{z} desvios declarados."""
    return float(z) * desvio_da_conta(janela)


def blocos(incrementos: np.ndarray, janela: int = JANELA_PADRAO) -> np.ndarray:
    r"""A estatística bloco a bloco, sem sobreposição.

    Blocos que não se sobrepõem mantêm os alarmes contáveis: com janelas deslizantes, o mesmo dia
    entra em duzentos e cinquenta e dois blocos seguidos, e o orçamento deixa de ter unidade.
    """
    d = np.asarray(incrementos, dtype=float)
    if janela < 2:
        raise ValueError("a janela precisa de pelo menos dois dias")
    if d.size < 2 * janela:
        raise ValueError("a serie precisa de pelo menos duas janelas")
    quantos = d.size // janela
    saida = []
    for b in range(quantos):
        fim = b * janela
        if fim < janela:
            continue
        anterior = d[fim - janela:fim]
        bloco = d[fim:fim + janela]
        escala = anterior.std(ddof=1)
        if escala <= 0.0:
            raise ValueError("a janela anterior estava parada: nao ha escala para padronizar")
        z = (bloco - anterior.mean()) / escala
        saida.append(float((z ** 3).mean()))
    return np.array(saida)


def resumo(valores: np.ndarray, limite: float) -> dict:
    r"""Média, dispersão e taxa de alarme de uma coleção de blocos."""
    v = np.asarray(valores, dtype=float)
    if v.size == 0:
        raise ValueError("nao ha blocos para resumir")
    padronizados = np.abs(v) > abs(limite)
    return {"media": float(v.mean()),
            "dispersao": float(v.std(ddof=1)) if v.size > 1 else 0.0,
            "taxa": float(padronizados.mean()),
            "blocos": int(v.size)}


def momento_amostral(serie: np.ndarray) -> dict:
    r"""O terceiro momento padronizado dos incrementos de uma série inteira.

    É a leitura do dado real: o número com a sua conta de nulo, e a razão entre os dois, que é o
    tamanho da direção em desvios. A conta do nulo supõe escala constante, e num dado com
    agrupamento ela é otimista --- a razão sai maior do que a evidência sustenta, e o caderno diz
    quanto.
    """
    d = passos(serie)
    escala = d.std(ddof=1)
    if escala <= 0.0:
        raise ValueError("a serie nao tem oscilacao: nao ha direcao a medir")
    z = (d - d.mean()) / escala
    momento = float((z ** 3).mean())
    conta = float(np.sqrt(15.0 / d.size))
    return {"momento": momento, "conta": conta, "razao": momento / conta, "dias": int(d.size)}
