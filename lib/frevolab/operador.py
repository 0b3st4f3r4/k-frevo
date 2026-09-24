r"""O operador: onde o critério pelos autovalores fica cego.

O capítulo da memória mede um sistema de um número só --- a estimativa de hoje é uma mistura da
de ontem com o dia de hoje, e a memória é \emph{1/(1-a)} dias. Ali o critério pelo autovalor é
exato. O §5 do contrato declara, para a pergunta E3, a referência a bater: **o critério pelos
autovalores, que é cego fora do caso simétrico**. Este módulo torna o cego visível.

Um sistema linear \emph{x(t+1) = A x(t)} tem o MESMO autovalor em toda a família

    A(c) = [[0,9, c], [0, 0,9]],

de modo que a conta escalar devolve a mesma memória --- dez dias --- para qualquer \emph{c}. Mas
a influência do estado inicial não é o autovalor: é a norma da potência, \emph{||A^k||}, e ela
**cresce antes de cair** quando a matriz não é simétrica. Em \emph{c = 100} a norma chega a
centenas no nono dia, onde o autovalor prevê 0,387.

**O defeito que este módulo torna impossível.** Dizer "a memória é 1/(1-λ)" para um sistema que
não é simétrico. A conta certa é a norma da potência contra a tolerância, e a distância entre as
duas é o que a seção mede.

As propriedades que sustentam a conta estão no \texttt{auto\_teste}: no caso diagonal a norma é
exatamente \emph{raio^k} e as duas memórias coincidem; fora dele o pico cresce com o acoplamento,
monotonamente.
"""
import numpy as np

RADIO_PADRAO = 0.9
ACOPLAMENTOS_PADRAO = (0.0, 1.0, 10.0, 100.0)
PASSOS_PADRAO = 200
TOLERANCIA_PADRAO = 0.15

__all__ = ["matriz", "normas", "memoria_do_autovalor", "dias_do_autovalor",
           "memoria_da_norma", "pico_da_norma",
           "familia", "RADIO_PADRAO", "ACOPLAMENTOS_PADRAO", "PASSOS_PADRAO", "TOLERANCIA_PADRAO"]


def matriz(acoplamento: float, radio: float = RADIO_PADRAO) -> np.ndarray:
    """A família: mesmo autovalor, acoplamento diferente.

    O autovalor é raio, duplo, para todo acoplamento --- é o que faz da família um experimento
    controlado do critério do autovalor contra a norma.
    """
    return np.array([[radio, float(acoplamento)], [0.0, radio]])


def normas(acoplamento: float, passos: int = PASSOS_PADRAO,
           radio: float = RADIO_PADRAO) -> np.ndarray:
    """||A^k|| para k = 0, 1, ..., passos --- a influência do estado inicial, dia a dia."""
    a = matriz(acoplamento, radio)
    p = np.eye(2)
    # Norma ESPECTRAL, e nao de Frobenius: ela e a medida de quanto o estado inicial ainda pesa
    # (a norma de operador induzida pela euclidiana). Com a de Frobenius a propria identidade vale
    # 1,41 e o caso diagonal nasce com um "pico" que nao existe.
    saida = [float(np.linalg.norm(p, 2))]
    for _ in range(int(passos)):
        p = p @ a
        saida.append(float(np.linalg.norm(p, 2)))
    return np.array(saida)


def memoria_do_autovalor(radio: float = RADIO_PADRAO) -> float:
    """A memória que o critério escalar anuncia: 1/(1-raio) dias, igual para toda a família."""
    return 1.0 / (1.0 - float(radio))


def dias_do_autovalor(tolerancia: float = TOLERANCIA_PADRAO,
                      radio: float = RADIO_PADRAO) -> int:
    """A travessia que o criterio escalar preve: log(tol)/log(raio) dias.

    E a conta exata do caso diagonal, e a conta que o capitulo faz quando o sistema tem um
    numero so. Na familia ela devolve o MESMO numero para toda coluna --- e e isso que a
    secao usa como promessa.
    """
    return int(np.ceil(np.log(float(tolerancia)) / np.log(float(radio))))


def memoria_da_norma(acoplamento: float, tolerancia: float = TOLERANCIA_PADRAO,
                     passos: int = PASSOS_PADRAO, radio: float = RADIO_PADRAO) -> int:
    """O primeiro dia em que a influência cai abaixo da tolerância --- e que já caiu de fato.

    O "e que já caiu de fato" é o ponto: a norma precisa ter passado pelo pico. Se ela ainda
    está subindo, a memória não acabou, por mais que o autovalor diga o contrário.
    """
    serie = normas(acoplamento, passos, radio)
    pico = int(np.argmax(serie))
    for k in range(pico, len(serie)):
        if serie[k] <= float(tolerancia):
            return int(k)
    return -1


def pico_da_norma(acoplamento: float, passos: int = PASSOS_PADRAO,
                  radio: float = RADIO_PADRAO) -> tuple:
    """O par (dia, valor) em que a influência do estado inicial é máxima."""
    serie = normas(acoplamento, passos, radio)
    k = int(np.argmax(serie))
    return k, float(serie[k])


def familia(acoplamentos=ACOPLAMENTOS_PADRAO, passos: int = PASSOS_PADRAO,
            tolerancia: float = TOLERANCIA_PADRAO, radio: float = RADIO_PADRAO) -> list:
    """Uma linha por acoplamento: o que o autovalor promete e o que a norma entrega."""
    linhas = []
    for c in acoplamentos:
        k, valor = pico_da_norma(c, passos, radio)
        linhas.append({"acoplamento": float(c),
                       "autovalor": float(np.max(np.abs(np.linalg.eigvals(matriz(c, radio))))),
                       "memoria_autovalor": memoria_do_autovalor(radio),
                       "pico_dia": int(k), "pico": float(valor),
                       "dias_autovalor": dias_do_autovalor(tolerancia, radio),
                       "memoria_norma": memoria_da_norma(c, tolerancia, passos, radio)})
    return linhas
