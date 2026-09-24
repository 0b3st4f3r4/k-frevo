r"""O vigia e o seu orçamento: quanto ele grita quando nada muda, quanto demora quando muda.

O capítulo anterior deixou um instrumento que sabe dizer que o mundo mudou. Este módulo
cuida da pergunta seguinte, a que transforma um instrumento em vigia: **com que frequência
ele soa sozinho, e quanto tempo ele leva quando a mudança é real**.

A ideia que o módulo carrega é que essas duas coisas são **um par**, e não dois ajustes
independentes. Baixar o limiar antecipa o alarme e multiplica o falso alarme; subir o
limiar faz o contrário. Não existe limiar que seja ao mesmo tempo raro e rápido, e o
motivo é aritmético: um alarme que exige \emph{T} violações dentro de uma janela móvel não
pode soar antes de \emph{T} dias com violação, e é disso que trata \`piso_de_atraso\`.

Por isso \emph{orçamento} aqui não é verba nem erro padrão: é o par declarado
(frequência em mundo parado, atraso em mundo que muda) que faz de um alarme uma afirmação.

**Duas leituras do mesmo corte.** O corte do capítulo anterior — o \emph{k}-ésimo pior da
janela — admite dois vigias, e os dois moram aqui, porque são o mesmo instrumento e é isso
que os põe na mesma curva:

1. **contar** as violações em blocos móveis e alarmar quando o bloco atinge o limiar
   (\texttt{alarmes}). É a leitura do capítulo anterior, e o orçamento dela \emph{não tem
   forma fechada}: sessenta blocos móveis se sobrepõem, de modo que a frequência só se sabe
   medindo (\texttt{orcamento}) e o único limite provado é frouxo
   (\texttt{teto\_independente});
2. **aprofundar** o corte e alarmar quando o próprio dia fica abaixo do \emph{k}-ésimo pior
   (\texttt{dispara}). Aqui o orçamento é \textbf{exato}, porque é a proposição da conta do
   corte lida ao contrário: \texttt{k/(n+1)}. E dele sai um limite que nenhuma calibração
   contorna — com \emph{n} dias de memória o alarme mais raro possível é \texttt{1/(n+1)}
   (\texttt{orcamento\_minimo}), de modo que \emph{o orçamento se compra com memória}: um
   alarme por ano custa um ano de memória, e um alarme por década custa dez anos que ninguém
   tem.

As duas leituras têm preço na mesma moeda — \texttt{prejuizo\_pago} — e é por isso que
podem ser postas lado a lado em vez de discutidas em separado.
"""
import numpy as np
import pandas as pd
from scipy import stats

from . import promessa

DIAS_UTEIS = 252
BLOCO_PADRAO = 60
TOLERANCIA = 1e-9

__all__ = ["DIAS_UTEIS", "BLOCO_PADRAO", "TOLERANCIA", "alarmes", "piso_de_atraso",
           "teto_independente", "orcamento", "prejuizo_pago", "orcamento_minimo",
           "memoria_para", "posto_do_orcamento", "dispara", "taxa_de_alarme",
           "alarmes_por_ano", "falsos_antes", "latencia"]


def alarmes(contagem: pd.Series, limiar: float) -> list:
    r"""Os episódios em que o bloco \emph{atingiu} o limiar: limiar ou mais violações.

    É o alarme do capítulo: o bloco chega ao limiar e o vigia soa. O limiar é contagem de
    violações, então atingi-lo é contar \emph{limiar} ou mais — e não \emph{limiar} estrito,
    que é o que \`presença\` responde quando a pergunta é "passou do teto".
    """
    return promessa.episodios_acima(contagem, limiar - 1)


def piso_de_atraso(limiar: int) -> int:
    r"""O atraso mínimo, em pregões, de um alarme que exige \emph{limiar} violações.

    A mudança começa no dia em que o nível novo vale, e esse dia já pode violar o corte, de
    modo que contar \emph{limiar} violações leva \emph{limiar} dias --- mas o atraso, que é a
    distância entre a mudança e o alarme, é de \emph{limiar}-1 pregões: o primeiro dia conta
    zero. O piso é aritmético e não se compra com calibração; a única alavanca é o próprio
    limiar, que é o orçamento.
    """
    if limiar < 1:
        raise ValueError("o limiar precisa de pelo menos uma violação")
    return int(limiar) - 1


def teto_independente(n_blocos: int, bloco: int, probabilidade: float, limiar: int) -> float:
    r"""Teto da probabilidade de algum bloco atingir o limiar, se os dias fossem independentes.

    A conta é a união sobre os blocos: a chance de \emph{algum} bloco passar do limiar não
    pode exceder a soma das chances de cada um. Com \emph{limiar} violações exigidas entre
    \emph{bloco} dias de probabilidade \emph{probabilidade} cada, cada parcela é a cauda da
    binomial e a soma é o teto.

    O teto é honesto e frouxo: ele ignora que violações vizinhas se parecem. Serve como
    limite superior provado, e a medição do mundo parado diz quanto ele sobra.
    """
    if not 0.0 <= probabilidade <= 1.0:
        raise ValueError("probabilidade fora de [0, 1]")
    return float(n_blocos * stats.binom.sf(limiar - 1, bloco, probabilidade))


def orcamento(blocos_nulos, limiar: float, dias_uteis: int = DIAS_UTEIS) -> dict:
    r"""O que o limiar custa em mundo parado: com que frequência ele soa sozinho.

    Recebe a matriz de blocos dos mundos que nunca mudam (um mundo por linha) e devolve a
    frequência com que o vigia soa sem que houvesse nada para ver. É esta a metade do par
    que ninguém mede quando calibra um alarme no olho.
    """
    b = np.asarray(blocos_nulos, dtype=float)
    if b.ndim != 2:
        raise ValueError("o orçamento se mede sobre uma matriz de mundos × blocos")
    mundos, n_blocos = b.shape
    acima = b >= limiar
    comeca = acima & ~np.concatenate((np.zeros((mundos, 1), dtype=bool), acima[:, :-1]), axis=1)
    episodios = comeca.sum(axis=1)
    anos = n_blocos / float(dias_uteis)
    media = float(episodios.mean())
    return {
        "mundos": int(mundos),
        "anos_por_mundo": float(anos),
        "dias_por_mundo": float(acima.sum(axis=1).mean()),
        "episodios_por_mundo": media,
        "fracao_com_alarme": float((episodios > 0).mean()),
        "anos_por_alarme": float(anos / media) if media > 0 else float("inf"),
    }


def prejuizo_pago(preco: pd.Series, alarme, janela: int = DIAS_UTEIS) -> dict:
    r"""O que já estava pago quando o alarme soou: topo, atraso e a fração do tombo.

    O topo é o maior preço da janela anterior ao alarme — havendo empate, o mais antigo,
    que é o que a série faz quando bate no mesmo preço duas vezes. O fundo é o menor preço
    da janela seguinte. A \emph{fração paga} é quanto do tombo total já tinha acontecido no
    dia do alarme — o número que decide se o vigia serviu para alguma coisa.
    """
    i = preco.index.get_loc(alarme)
    antes = preco.iloc[max(0, i - janela):i + 1]
    topo_data, topo = antes.idxmax(), float(antes.max())
    fundo = float(preco.iloc[i:i + janela + 1].min())
    queda_total = 1.0 - fundo / topo
    queda_ate = 1.0 - float(preco.loc[alarme]) / topo
    return {
        "topo": topo_data,
        "atraso_dias": int((alarme - topo_data).days),
        "queda_ate_alarme": queda_ate,
        "queda_total": queda_total,
        "fracao_paga": float(queda_ate / queda_total) if queda_total > 0 else float("nan"),
    }

def orcamento_minimo(janela: int) -> float:
    r"""O alarme mais raro que \emph{janela} dias de memória conseguem declarar: 1/(janela+1).

    Não é escolha de quem vigia, é limite: o posto mais fundo é o primeiro da fila, e a
    proposição da conta do corte dá a taxa dele. Com um ano de pregões, o mais raro que se
    pode prometer é um alarme por ano.
    """
    if janela < 2:
        raise ValueError("a janela precisa de pelo menos dois dias")
    return 1.0 / (janela + 1)


def memoria_para(orcamento: float) -> int:
    r"""Quantos dias de memória são precisos para declarar este orçamento.

    É o inverso do orçamento mínimo, e a resposta prática de "quero um alarme por década":
    dois mil e quinhentos e tantos pregões, dez anos. Quem não tem esses dias não tem esse
    alarme, e nenhuma calibração compra o que a memória não tem.
    """
    if not 0.0 < orcamento < 1.0:
        raise ValueError("o orcamento precisa estar entre 0 e 1 por dia")
    return int(np.ceil(1.0 / orcamento - TOLERANCIA)) - 1


def posto_do_orcamento(janela: int, orcamento: float) -> int:
    r"""O posto \emph{k} que entrega o orçamento declarado: $k = \lceil \alpha (n+1) \rceil$.

    Devolve o primeiro posto cuja taxa não passa do orçamento — o lado conservador, que
    promete no máximo o que se declarou. Como o posto é inteiro, a taxa entregue raramente
    coincide com a declarada: um alarme a cada quatrocentos dias não existe, e o vigia
    entrega o mais próximo que existe.

    A tolerância existe porque o caso interessante é a fronteira: "um alarme por ano" com uma
    janela de um ano é exatamente \texttt{1/(n+1)}, e a aritmética de ponto flutuante erra por
    um bit em \texttt{1/253 * 253}. Sem ela, um orçamento legítimo seria recusado por erro de
    representação, não por falta de memória.
    """
    if not 0.0 < orcamento < 1.0:
        raise ValueError("o orcamento precisa estar entre 0 e 1 por dia")
    minimo = orcamento_minimo(janela)
    if orcamento < minimo * (1.0 - TOLERANCIA):
        raise ValueError(
            "memoria insuficiente: %d dias declaram no maximo %.6f por dia (%.2f alarmes por "
            "ano); pedido %.6f por dia, que exige %d dias"
            % (janela, minimo, DIAS_UTEIS * minimo, orcamento, memoria_para(orcamento)))
    return max(1, int(np.ceil(orcamento * (janela + 1) - TOLERANCIA)))


def dispara(retornos: pd.Series, janela: int, orcamento: float) -> pd.Series:
    r"""A segunda leitura: o dia ficou abaixo do posto que o orçamento escolheu.

    Devolve verdadeiro/falso pelos mesmos dias de graça do corte — \texttt{len(retornos) -
    janela} entradas —, porque um alarme não pode ser julgado nos dias em que a linha ainda
    não existia.

    O nome não é enfeite: o que sai daqui é o que um operador recebe de manhã, e a lista
    costuma ser lida como se cada linha fosse evidência sobre o mundo. Não é. Sob o orçamento
    declarado, a maior parte dela é o próprio orçamento sendo gasto.
    """
    return promessa.violacoes_no_posto(retornos, janela, posto_do_orcamento(janela, orcamento))


def taxa_de_alarme(alarmes: pd.Series) -> float:
    """A fração de dias que soaram, entre os dias em que o alarme podia soar."""
    if alarmes.empty:
        raise ValueError("serie de alarmes vazia: nao ha taxa a medir")
    return float(alarmes.astype(float).mean())


def alarmes_por_ano(alarmes: pd.Series, dias_uteis: int = DIAS_UTEIS) -> float:
    """A mesma taxa, dita em alarmes por ano — a unidade em que o orçamento se declara."""
    return dias_uteis * taxa_de_alarme(alarmes)


def falsos_antes(alarmes: pd.Series, mudanca) -> int:
    r"""Quantos alarmes soaram antes da data da mudança: o orçamento, gasto à toa.

    É a metade da medição que a latência sozinha esconde. Um vigia que dispara no dia
    seguinte a qualquer mudança e mais quatrocentas vezes no ano é o pior dos dois mundos, e
    só as duas contas juntas o denunciam.
    """
    passado = np.asarray(alarmes.index) < mudanca
    return int(np.sum(np.asarray(alarmes)[passado]))


def latencia(alarmes: pd.Series, mudanca) -> float:
    r"""Dias entre a mudança e o primeiro alarme; \texttt{nan} se não veio alarme nenhum.

    A conta é em passos da série, que numa série diária é o mesmo que dias. O alarme que cai
    no próprio dia da mudança tem latência zero — não é caso degenerado, é o vigia que não
    dorme, e a convenção está escrita em \texttt{mudanca.py}: o dia da mudança já é um dia
    mudado.

    Devolver \texttt{nan} em vez de um número grande é deliberado: "não alarmou em oitocentos
    dias" e "alarmou no dia oitocentos" são resultados diferentes, e uma média que os
    confunde pinta um vigia que não existe.
    """
    if not alarmes.index.is_monotonic_increasing:
        raise ValueError("a serie de alarmes precisa estar em ordem de data")
    inicio = int(alarmes.index.searchsorted(mudanca))
    depois = np.flatnonzero(np.asarray(alarmes)[inicio:])
    if depois.size == 0:
        return float("nan")
    return float(depois[0])
