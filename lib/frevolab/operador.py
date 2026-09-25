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



def matriz_aberta(acoplamento: float, abertura: float,
                  radio: float = RADIO_PADRAO) -> np.ndarray:
    r"""A família com o canto de baixo aberto: \emph{[[raio, c], [delta, raio]]}.

    Com abertura nula ela é a matriz de cima --- o autovalor duplo com um bloco de Jordan, onde
    a norma cresce em $k$. Com abertura positiva os dois autovalores se separam, e a separação
    é o que decide o sinal do transitório: é a mesma família do capítulo, com uma porta a mais.
    """
    if not 0.0 < float(radio) < 1.0:
        raise ValueError("o raio precisa estar entre zero e um")
    if acoplamento < 0.0 or abertura < 0.0:
        raise ValueError("o acoplamento e a abertura nao podem ser negativos")
    return np.array([[float(radio), float(acoplamento)],
                     [float(abertura), float(radio)]])


def kreiss(a, raios=None, pontos: int = 512) -> float:
    r"""A constante de Kreiss: o sup de \emph{delta} vezes a norma do resolvente em |z| = 1+delta.

    É o preço declarado do transitório: ela limita a amplificação de qualquer potência, e é
    calculada aqui pelo resolvente em um círculo de cada vez, numa grade log de raios. O sup em
    grade SUBESTIMA a constante, e é por isso que a asserção do \texttt{auto\_teste} cobra a
    grade mais fina quando o teto ameaça cair abaixo do pico medido.
    """
    m = np.asarray(a, dtype=float)
    if m.ndim != 2 or m.shape[0] != m.shape[1]:
        raise ValueError("a constante de Kreiss quer uma matriz quadrada")
    if int(pontos) < 8:
        raise ValueError("o circulo precisa de pelo menos oito pontos")
    if raios is None:
        raios = np.logspace(-6.0, 1.0, 60)
    ident = np.eye(m.shape[0])
    angulos = np.linspace(0.0, 2.0 * np.pi, int(pontos), endpoint=False)
    melhor = 0.0
    for delta in np.asarray(raios, dtype=float):
        if delta <= 0.0:
            raise ValueError("a grade de raios precisa ser positiva")
        raio = 1.0 + delta
        maior = 0.0
        for theta in angulos:
            z = raio * complex(np.cos(theta), np.sin(theta))
            resolvente = np.linalg.solve(z * ident - m, ident)
            maior = max(maior, float(np.linalg.norm(resolvente, 2)))
        melhor = max(melhor, delta * maior)
    return float(melhor)


def teto(acoplamento: float, passos: int = PASSOS_PADRAO, radio: float = RADIO_PADRAO,
         pontos: int = 512) -> dict:
    r"""O teto demonstrável da norma da potência, e a folga que ele carrega.

    A cota é \emph{e (k+1) K}, com \emph{k} o dia do pico medido e \emph{K} a constante de
    Kreiss: ela não é uma previsão, é um limite --- e o que se publica dela é a folga, isto é,
    quanto o limite fica acima do que a medição mostrou.
    """
    serie = normas(acoplamento, passos, radio)
    dia = int(np.argmax(serie))
    constante = kreiss(matriz(acoplamento, radio), pontos=pontos)
    limite = float(np.e * (dia + 1) * constante)
    pico = float(serie[dia])
    return {"kreiss": constante, "dia": dia, "teto": limite, "pico": pico,
            "folga": (limite / pico) if pico > 0.0 else float("inf")}


def desdobramento(acoplamento: float, aberturas, radio: float = RADIO_PADRAO) -> list:
    r"""Uma linha por abertura: os dois autovalores, a separação entre eles e o raio espectral.

    É a medição do ponto excepcional: perto da abertura em que os autovetores coalescem, a
    separação cresce na raiz da abertura, e a sensibilidade do autovalor diverge.
    """
    saida = []
    for abertura in aberturas:
        m = matriz_aberta(acoplamento, abertura, radio)
        autovalores = np.linalg.eigvals(m)
        ordenados = sorted(autovalores, key=lambda z: (z.real, z.imag))
        separacao = float(abs(ordenados[0] - ordenados[1]))
        raio = float(np.max(np.abs(autovalores)))
        saida.append({"abertura": float(abertura), "separacao": separacao,
                      "raio": raio,
                      "complexos": bool(abs(ordenados[0].imag) > 1e-12)})
    return saida


def sensibilidade(acoplamento: float, abertura: float, radio: float = RADIO_PADRAO,
                  passo: float = 1e-6) -> float:
    r"""A sensibilidade do autovalor à abertura, por diferença central.

    No ponto excepcional ela diverge: é a conta que o critério escalar não faz e que a seção
    mede, para mostrar que ali o autovalor deixa de ter número estável.
    """
    if passo <= 0.0:
        raise ValueError("o passo da diferenca precisa ser positivo")
    if abertura - passo <= 0.0:
        raise ValueError("a diferenca central precisa de abertura maior que o passo")
    def maior_autovalor(ab):
        return complex(np.linalg.eigvals(matriz_aberta(acoplamento, ab, radio))[0])
    derivada = (maior_autovalor(abertura + passo) - maior_autovalor(abertura - passo))
    return float(abs(derivada) / (2.0 * passo))


def fronteira(acoplamento: float, radio: float = RADIO_PADRAO) -> float:
    r"""A abertura em que o raio espectral toca o círculo: \emph{(1-raio)^2 / c}.

    Ela sai da conta exata do autovalor da família aberta, $\lambda = raio \pm \sqrt{c\,delta}$,
    e é a abertura em que o passado de memória longa deixa de desbotar.
    """
    if acoplamento <= 0.0:
        raise ValueError("a fronteira pede acoplamento positivo")
    return float((1.0 - float(radio)) ** 2 / float(acoplamento))


def nuvem(acoplamento: float, abertura: float, sortes: int, semente: int,
          radio: float = RADIO_PADRAO) -> np.ndarray:
    r"""O raio espectral sob perturbações aleatórias de norma fixa: a nuvem que o critério devolve.

    A perturbação é um sorteio normal de norma de Frobenius igual à abertura declarada --- a
    mesma norma em todos os mundos, para que a comparação seja entre direções e não entre
    tamanhos.
    """
    if int(sortes) < 1:
        raise ValueError("a nuvem precisa de pelo menos uma sorte")
    rng = np.random.default_rng(int(semente))
    base = matriz_aberta(acoplamento, abertura, radio)
    raios = np.empty(int(sortes))
    for i in range(int(sortes)):
        direcao = rng.standard_normal(base.shape)
        norma = float(np.linalg.norm(direcao))
        if norma == 0.0:
            raios[i] = float(np.max(np.abs(np.linalg.eigvals(base))))
            continue
        perturbada = base + direcao * (float(abertura) / norma)
        raios[i] = float(np.max(np.abs(np.linalg.eigvals(perturbada))))
    return raios


__all__ = ["matriz", "normas", "memoria_do_autovalor", "dias_do_autovalor",
           "memoria_da_norma", "pico_da_norma",
           "familia", "matriz_aberta", "kreiss", "teto", "desdobramento",
           "sensibilidade", "fronteira", "nuvem",
           "RADIO_PADRAO", "ACOPLAMENTOS_PADRAO", "PASSOS_PADRAO", "TOLERANCIA_PADRAO"]


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
