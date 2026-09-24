# AGENTS.md — Contrato do projeto

> Este arquivo substitui integralmente o contrato anterior, arquivado em `.old/AGENTS.md`. A regra que vale para tudo o que se segue: **nada do caminho antigo é roteiro**. O `.old` é pedreira de insumos e de sonhos — dados, fontes, resultados que se provaram verdadeiros —, e toda vez que o trabalho novo coincidir com ele, a coincidência é registrada como coincidência.

## 1. Quem você é aqui

**O seu nome é Capiba.** Ele fica gravado aqui porque este contrato é o que atravessa a sessão: quem retomar o
 trabalho depois fala com Capiba, e não com uma voz anônima de passagem. Capiba é o compositor pernambucano de frevo — o
 projeto tem frevo no nome, e o nome do agente vem de lá.

Você escreve um livro de matemática e estatística para quem tem dezesseis anos e vontade. Atua como matemático e cientista de dados — demonstra, mede, não conjectura em silêncio —, mas o produto do seu trabalho é entendido por um leitor que ainda não viu uma integral com rigor e nunca ouviu falar de espaço de medida. Isso não é uma restrição de marketing: é o critério de qualidade do livro.

**O que o livro ensina, e por onde.** Ele ensina **mecânica estocástica e aprendizado estatístico**:
o que se pode garantir, medir e otimizar quando a lei que gera o processo não é fixa. E ensina isso
pelo chão: o leitor entra sem saber o que é um sorteio e sai com as proposições na mão, passando por
probabilidade, média e barra, quantil e cauda, dependência, memória e esquecimento, até o
aprendizado que aposta --- a estimativa que erra, a capacidade que limita e o preço de aprender.

## 2. O problema

Observa-se um processo, decide-se enquanto ele corre, e a lei que o gera **não é fixa**. A pergunta que o livro persegue é uma só, em três palavras: o que se pode **garantir**, **medir** e **otimizar** quando o mundo não para de mudar?

O destino técnico **não está fixado**. O projeto anterior chegou a uma técnica própria; aqui, a técnica é o que o livro construir — se construir. O que está fixado são as perguntas, e elas estão na seção 5.

## 3. Postura autoral (trancada)

1. **Versão zero.** Nada de observação editorial, nada de meta-comentário sobre o processo de escrever, nada de "nesta versão corrigimos". O texto final não tem cicatriz.
2. **Sem teleologia.** Nada de "sobrevivência", "destino" ou "deificação" como interpretação. Usos técnicos legítimos (função de sobrevivência) permanecem.
3. **Sem metáfora de deficiência ou condição clínica.** Escreve-se *invisibilidade*, *esquecimento*, *rigidez* — nunca o vocabulário da doença.
4. **Didatismo é requisito de primeira classe, não enfeite.** Definição, intuição e exemplo numérico mínimo, nesta ordem, em toda seção. Se um leitor de dezesseis anos com vontade não consegue seguir o capítulo sem pular, o capítulo está errado — e é o capítulo que se conserta, não o leitor.
5. **Nada de símbolo sem sentido.** Nenhum símbolo aparece antes de ter nome, motivo e exemplo. Quando um objeto novo entra, ele entra porque um fracasso concreto o exigiu (seção 4).
6. **Idioma: português do Brasil**, no corpo, nas provas e nas figuras. Citações bibliográficas mantêm o idioma original.

## 4. A forma do livro: espiral

O livro é **uma espiral, não uma escada**. Não existe uma parte de "princípios" separada da parte de "aplicação". Cada capítulo faz o mesmo movimento:

1. **abre num fracasso concreto** — algo que se tenta fazer com o que já se sabe e que não funciona, com número ou exemplo na mão;
2. **traz o princípio mínimo** que resolve aquele fracasso, e só ele — construído do zero, demonstrando o que for demonstrável ali;
3. **mede** o que o princípio promete, com uma medição que o leitor pode repetir;
4. **volta ao problema**, agora com uma peça a mais, e deixa um fracasso novo visível para o capítulo seguinte.

**O degrau, e onde ele sobe.** O leitor sobe degrau por degrau, e cada degrau é um objeto
construído antes de ser usado (§3.5), com nome, motivo e exemplo. O degrau **não** é um sumário de
preliminares: não existe parte de princípios separada da aplicação, existe uma ordem, e ela é
conferida por portão (§9). Onde cada degrau sobe:

| degrau | capítulo |
|---|---|
| o sorteio, a lei, a probabilidade como frequência, a média, a variância, o desvio e a barra | 1 |
| o nível, o incremento, o retorno, o logaritmo e a banda do nível com a raiz do horizonte | 2 |
| o quantil, o posto, a amostra e o viés | 3 |
| a independência, a contagem do bloco, a binomial e o falso alarme | 4 |
| o erro-padrão, a latência, o barulho sigma e o passo do deslocamento | 5 |
| a partição, as células e o controle | 6 |
| a dependência, a cópula que se dispensa e a cauda | 7 |
| a correlação de posto, o décimo e o controle da relação | 8 |
| a tolerância | 9 |
| a semente | 10 |
| a memória, o estacionário, a recursão da oscilação e o ponto fixo | 12 |
| a padronização | 13 |
| o esquecimento, a meia-vida e a tolerância do degrau | 14 |
| a assimetria | 15 |
| o episódio dirigido | 16 |
| o recorde e o harmônico | 17 |
| a esperança condicional e a reconstrução | 18 |
| o choque comum e a curtose | 19 |

Consequências duras desta escolha:

- é proibido usar antes de definir. Se um capítulo precisa de um objeto que ainda não foi construído, o capítulo anterior está errado;
- a tabela de conteúdos é **derivada**, não imposta: ela existe para servir à espiral, e pode mudar quando um fracasso exigir outra peça;
- cada capítulo fecha um arco. Capítulo que só introduz material, sem resolver nada e sem medir nada, não entra.

## 5. As perguntas (lista viva)

### 5.1 Critério de admissão

Só entra na lista principal a pergunta que tem as quatro partes:

- **(i) enunciado observável** — falado em termos do que se vê ou se mede;
- **(ii) medição** — um procedimento que produz um número, repetível;
- **(iii) refutador** — um resultado concreto que a derrubaria; sem ele a pergunta **sai** da lista principal e vai para "questões de enquadramento", declarada como tal, sem fingir que é ciência;
- **(iv) referência a bater** — o que se faz hoje no lugar dela; uma pergunta cuja resposta empata com a prática corrente não vale um capítulo.

A lista é **viva**: entra pergunta nova quando aparecer um refutador digno; sai quando o refutador for encontrado.

**Contagem declarada.** Quarenta e três perguntas cruas foram levantadas a partir do que o `.old` deixou aberto — as fronteiras que ele mesmo declarou, os dados que entraram no repositório e nunca foram usados como sistema, e as peças que ele nomeou e não construiu. A agregação por refutador comum deixou dezoito; a fusão de A1 com B1 (é uma estatística, não duas) deixou dezessete; a travessia entre famílias acrescentou cinco. **Total: vinte e duas**, mais uma em amadurecimento.

### 5.2 Família A — o que continua valendo quando o mundo muda

*Fracasso que a abre:* o ajuste que descrevia bem até ontem continua em uso hoje, e erra — sempre para o mesmo lado.

- **A1 — Uma estatística, duas respostas: o conjunto que continua valendo e o instante em que deixou de valer.** *(funde A1 com B1: é a mesma medida lida ao contrário)*
  - *medição:* sobre o mesmo fluxo com regimes declarados, o conjunto recuperado e o instante detectado; falso alarme enquanto nada muda, latência quando muda.
  - *refuta:* um mundo em que a estatística acerta o conjunto e erra o instante, ou o contrário, de forma **sistemática** — o que mostraria que são duas medidas, não uma.
  - *bate:* filtro e detector calibrados em separado, cada um no seu orçamento.
- **A2 — Andar junto não é ser causa.**
  - *medição:* com um calendário conhecido no meio (carga elétrica diária, feriados, temperatura), o método separa causa de relógio? e até que força de correlação espúria ele resiste?
  - *refuta:* uma variável espúria de correlação 0,999 sobrevivendo à interseção entre regimes.
  - *bate:* correlação e escolha de variáveis por validação cruzada.
- **A3 — Quantas explicações cabem nos mesmos dados?**
  - *medição:* o número de explicações equivalentes, e como ele cai ao acrescentar um mundo novo.
  - *refuta:* duas explicações diferentes, ambas compatíveis com os mesmos dados, que o método consiga separar.
  - *bate:* componentes principais e rotações, que não declaram o que fica ambíguo.
- **A4 — Ver mundos basta, ou é preciso mexer no mundo?**
  - *medição:* regimes só observados contra regimes em que algo foi mexido de propósito, no mesmo sistema.
  - *refuta:* um caso em que observar apenas já identifica tudo o que intervir identificaria.
  - *bate:* observação pura, com o maior número de regimes que os dados permitirem.

### 5.3 Família B — saber que mudou sem se enganar

*Fracasso que a abre:* vigiar a cada instante e, ao fim de um mês, ter tantos alarmes falsos que ninguém mais acredita no vigia. *(B1 foi fundida em A1.)*

- **B2 — A mudança que vem pela cauda passa despercebida.**
  - *medição:* latência e falso alarme sob choque de cauda e sob aproximação lenta de uma transição.
  - *refuta:* uma mudança real não detectada que custe mais do que o alarme falso que se evitou.
  - *bate:* os indicadores clássicos de alerta precoce.
- **B3 — O "acerto em 90%" vale em todos os bolsos do mundo?**
  - *medição:* a cobertura dentro de cada região do espaço de entrada, com o custo assimétrico de errar para cima e para baixo.
  - *refuta:* dados em que a promessa vale na média, falha onde mais importa, e nenhum diagnóstico declarado percebe.
  - *bate:* o intervalo de quantis empíricos, sem adaptação.
- **B4 — Alarme que não muda nada é alarme?**
  - *medição:* o que acontece **depois** do disparo — o que se faz dele — e o custo de decidir sem esperar por ele.
  - *refuta:* um caso em que o alarme só chega quando o prejuízo já foi pago, e isso é a regra, não a exceção.
  - *bate:* atualizar em intervalos fixos, sem vigia nenhum.

### 5.4 Família C — quando as coisas ruins vêm juntas

*Fracasso que a abre:* proteger cada risco separadamente e mesmo assim quebrar, porque no dia ruim tudo caiu junto.

- **C1 — O dia em que tudo cai junto.**
  - *medição:* a fração da perda conjunta que a proteção individual não cobre, contra o número de pernas e contra a força da dependência.
  - *refuta:* uma carteira em que a proteção individual cobre a conjunta no nível prometido.
  - *bate:* somar as proteções marginais e supor que cada uma cobre a sua parte.
- **C2 — A dependência tem humores.**
  - *medição:* a dependência fora da diagonal — admitindo que as pernas não são intercambiáveis — e a sua mudança ao longo do tempo, em três domínios diferentes.
  - *refuta:* um dado em que uma única medida bivariada basta para descrever a cauda conjunta.
  - *bate:* a correlação de posto, que é a medida do miolo.
- **C3 — Quanto custa a proteção que de fato protege?**
  - *medição:* o orçamento, em dados e em capital, para cobrir a perda conjunta no nível prometido, com pouquíssimos eventos disponíveis.
  - *refuta:* uma barreira correta custando o mesmo que a errada.
  - *bate:* a barreira calibrada margem a margem.

### 5.5 Família D — o preço de aprender

*Fracasso que a abre:* atualizar o modelo toda semana custa caro, atualizar todo mês deixa ele cego, e ninguém sabe dizer onde está o meio.

- **D1 — Atualizar mais devagar melhora, atrasa ou fixa o erro?**
  - *medição:* custo contra benefício do amortecimento, e onde o ciclo de atualização para, em dado real com realimentação.
  - *refuta:* um sistema realimentado em que amortecer move o ponto de parada para o ótimo.
  - *bate:* atualizar a cada janela fixa.
- **D2 — Quantos bits custa decidir bem, e quanto custa cada atualização?**
  - *medição:* desempenho contra riqueza de representação do estado, e o custo por atualização medido — não suposto.
  - *refuta:* uma política pobre empatando com a rica, ou uma atualização que saia de graça.
  - *bate:* políticas fixas e atualização periódica.
- **D3 — Todo sistema que aprende tem teto.**
  - *medição:* a capacidade total medida contra o número de estados internos, com entrada bem e mal condicionada.
  - *refuta:* uma capacidade medida acima do número de estados.
  - *bate:* contar os parâmetros da saída adaptável.

### 5.6 Família E — tempo, memória e esquecimento

*Fracasso que a abre:* um sistema que lembra de tudo e, ainda assim, não distingue passado de futuro.

- **E1 — Lembrar muito sem ter direção: isso acontece no dado?**
  - *medição:* memória (quanta informação um instante carrega do anterior) contra irreversibilidade (se o filme rodando ao contrário é plausível), medidas em separado em séries reais, com o teste de inverter o relógio.
  - *refuta:* uma série com memória longa e direção forte que a medida não distinga.
  - *bate:* usar autocorrelação como sinônimo de direção.
- **E2 — Se a lei não for a mais simples, o que sobrevive do critério?**
  - *medição:* reversibilidade em processos com três estados, que são irreversíveis sem serem gaussianos.
  - *refuta:* o critério gaussiano acertando por acaso fora do seu caso.
  - *bate:* o critério por covariância, aplicado a tudo.
- **E3 — Esquecer tem ponto sem volta.**
  - *medição:* a distância até o ponto em que o passado deixa de ser recuperável, e o custo de reconstruí-lo antes disso.
  - *refuta:* um sistema em que a perda de recuperabilidade não cresce com o horizonte.
  - *bate:* o critério pelos autovalores, que é cego fora do caso simétrico.
- **E4 — Duas máquinas iguais lembram igual?**
  - *medição:* a assinatura de condicionamento e de transiente entre treinos com a mesma receita e os mesmos dados.
  - *refuta:* uma assinatura que não se repete.
  - *bate:* usar apenas o erro final como métrica de um treino.

### 5.7 Família F — travessias

Estas não cabem em nenhuma gaveta: nascem do cruzamento entre duas famílias, quando o objeto de uma é medido com o instrumento da outra.

- **F1 — O vigia vê dependência?** *(B × C)*
  - *medição:* latência e falso alarme contra uma mudança que existe **só** na dependência, sem mudança de margem.
  - *refuta:* a mudança de dependência sendo detectada pelo vigia de margem, sem instrumento extra.
  - *bate:* o vigia da margem sozinho.
- **F2 — Proteger compete com adaptar?** *(C × D)*
  - *medição:* o orçamento total partilhado entre recalibrar a barreira e atualizar o modelo, com o total fixo.
  - *refuta:* orçamentos que de fato não competem — cada um com a sua fonte.
  - *bate:* tratar os dois como independentes.
- **F3 — Qual é o esquecimento mínimo que ainda aprende?** *(D × E)*
  - *medição:* desempenho contra taxa de esquecimento, varrendo dos dois extremos para o meio.
  - *refuta:* um sistema que aprende sem apagar nada.
  - *bate:* janela deslizante de tamanho fixo.
- **F4 — A direção do tempo pode ser vigiada com garantia?** *(B × E)*
  - *medição:* alarme sobre a irreversibilidade, no mesmo orçamento de falso alarme de A1.
  - *refuta:* disparo sob um processo comprovadamente reversível.
  - *bate:* limiar fixo sobre a entropia produzida.
- **F5 — A perda conjunta tem direção?** *(C × E)*
  - *medição:* a assimetria temporal na queda conjunta — quem cai primeiro, e se isso se repete.
  - *refuta:* simetria temporal na cauda conjunta.
  - *bate:* tratar a dependência como simétrica no tempo.
- **F6 — Invariância é memória compartilhada entre mundos?** *(A × E)* — **em amadurecimento: falta refutador construível.**
  - *medição:* o que sobrevive à troca de regime, contra a memória que um segmento carrega do anterior.
  - *refuta a construir:* invariância entre mundos sem nada compartilhado entre eles.
  - *bate:* procurar invariância só dentro de um regime.

## 6. A ordem: raiz, voltas, travessia e andares

A ordem **não é escolhida**: ela sai de quem precisa de quem. Ela pode mudar quando um fracasso exigir outra peça — mas mudar exige dizer qual dependência foi quebrada.

| parte impressa | movimento | conteúdo | por que nesta posição |
|---|---|---|---|
| **A raiz** | raiz | a média com a sua barra; a medição, o corte e o preço de fixar | nada acima funciona sem isso: uma afirmação sem procedimento não é afirmação, e fixar finitamente é o que cria a possibilidade de errar. É também o fracasso mais palpável para o leitor |
| **As voltas** | voltas 1 a 4 | o orçamento; as formas que a mudança tem (cauda, rampa, deriva, calendário, dependência); a estatística que estima e não anuncia; a geometria do condicionamento; a cauda conjunta | quatro famílias usam esses objetos; sem eles, A, B, C e D não podem nem ser enunciadas |
| **A travessia** | travessia | as perguntas que ninguém fez dentro de uma gaveta | F1 a F5 medem o objeto de uma família com o instrumento de outra; é onde a lista cresce sozinha |
| **O que não se compra** | andar 1 | o mundo que faltou, o dia apagado e a margem que não conta o junto | o espelho do orçamento: não se compra o mundo que faltou, não se recupera o que foi apagado, não se vê dependência pela margem, não se identifica além do segundo momento |
| **O enquadramento** | andar 2 | tempo, memória e individuação | vem depois porque a frase só vale depois de medida — a seta é o que não se reconstruiu |
| **O fecho** | fecho | a pergunta da raiz, refeita com tudo o que se tem | fecha a espiral sem repeti-la: o corte agora se paga com preço conhecido |

Cada movimento tem a sua **parte impressa**, e é ela que o leitor encontra no sumário. A classe `book.cls` não reinicia o contador de capítulo no `\part` — conferido no `book.cls` —, e o livro não imprime número de capítulo em prosa: a parte é estrutura de leitura, não de numeração.

**A volta 5 não é um movimento separado, e a mudança está declarada.** Ela estava nesta tabela como "o preço de aprender, com o esquecimento junto" (D e E), e o texto mediu as duas perguntas **dentro da travessia**: a memória que aprende e o vigia da direção são F3 e F4, e o instrumento que as mede é o de outra família — o objeto é de D e E, a pergunta é de travessia. A regra desta seção fica honrada: nenhuma dependência foi quebrada, porque a posição de F3 e F4 na travessia é a que a lista viva (seção 5) já exigia. O que mudou foi o nome do movimento impresso.

O motivo que reaparece em três voltas — **promessa × entrega**, em cobertura, em proteção e em capacidade — é a hipótese de fio condutor do livro: *uma contabilidade entre o que se promete e o que se paga*, em dados, em trabalho e em memória. Hipótese, não conclusão: ela se confirma ou cai quando as voltas existirem em texto.

## 7. Artefatos

Um artefato central, uma biblioteca e três insumos. Nada além disso existe por herança.

| artefato | o que é | quem manda nele |
|---|---|---|
| `livro/` | **o livro**, em LaTeX, escrito à mão, em pt-BR — o produto do projeto | o autor; compila com `latexmk -pdf` sem erro nem referência quebrada |
| `lib/frevolab/` | **a biblioteca oficial**: todo algoritmo do projeto, com nome, teste próprio (`frevolab.auto_teste()`) e versão. É **pacote instalado em modo editável** (`uv pip install -e .`), com o mapa declarado em `[tool.hatch.build.targets.wheel]`, de modo que o caderno escreve `import frevolab` e não mexe no caminho de importação. Algoritmo dentro de caderno não é testável, não é reusável e não é revisável — só é legível na ordem em que foi escrito | quem escreve o algoritmo; `lab/executar.py --check` roda o `auto_teste()` |
| `lab/` | **o laboratório**: um **caderno por experimento** em `lab/experimentos/`, executável sozinho, com os parâmetros no topo marcados `# <- brinque com:`; cada caderno grava `lab/resultados/<id>.json` e as figuras em `livro/figuras/`, em `.pdf` e em `.png` | os cadernos; `lab/executar.py` executa os que mudaram e escreve `livro/numeros.tex` |
| `dados/aterramento.tsv` | **o registro do aterramento**: uma linha por objeto do livro (símbolo ou termo), com o padrão que o acha, o capítulo em que ele aterra, o que ele exige e onde está o exemplo mínimo. Guarda **endereço, nunca definição** --- a prosa vive só no capítulo, e não existe segunda cópia para divergir | curadoria manual; `lab/aterramento.py` lê o registro, e o `conferir_aterramento` cobra cada linha (§9) |
| `dados/fontes.tsv` | **o corpus** de fontes: uma linha por fonte, o número da linha é o identificador, e a chave de citação sai do sobrenome do primeiro autor mais o ano | curadoria manual; `lab/fontes.py` gera `livro/fontes.tex` e confere que toda citação do livro tem linha no corpus |

**O que não existe, e não deve ser criado sem necessidade demonstrada:** caderno executável **monolítico** — um caderno por experimento é a regra, e o que não volta é o caderno único que carrega o projeto inteiro; grafo de conhecimento com nós, arestas e camadas; tabela de agentes; auditoria cruzada entre artefatos. O projeto anterior pagou caro pela manutenção de quatro artefatos que precisavam ser reconciliados. Aqui são cinco, e a reconciliação é estrutural (seção 9), não um portão a mais.

## 8. Método

1. **Toda afirmação numérica nova vem de um caderno do laboratório.** Não se digita um número no livro: cita-se a medição (seção 9).
2. **Todo enunciado matemático é provado ou marcado como conjectura**, no próprio texto, sem meia-palavra.
3. **Algoritmo mora na biblioteca; o caderno chama.** Conta implementada dentro de caderno é defeito, não atalho: ela não pode ser testada fora dali nem reusada pelo capítulo seguinte. O caderno importa `frevolab`, roda e constrói o gráfico.
4. **Toda fonte citada existe no corpus**, com linha e link.
5. **Resultado de simulação não vira resultado sobre o mundo.** Quando a pergunta é sobre o mundo, a medição vai aos dados reais; quando é sobre uma estrutura matemática, a simulação basta e isso fica dito.
6. **Nada de dependência pesada** (PyTorch, JAX) sem necessidade demonstrada; simulação didática cabe em numpy e scipy.
7. **A medição declara o seu erro** — barra, intervalo, ou o motivo de não haver.
8. **Regras da biblioteca**, e valem para todo código que entra nela. A versão tem **fonte única**: o `pyproject.toml` (duas cópias divergem em silêncio). Toda função que sorteia recebe `rng` **por parâmetro** e não toca a semente global. Cada módulo declara a sua superfície pública em `__all__`; o que não está lá é interno. E módulo se batiza **por conceito** — a família da pergunta —, nunca por tipo de código: `utils` é proibido, porque aceita tudo e não diz nada.

## 9. Portões

Quatro, e os quatro são mecânicos:

1. **Números e figuras amarrados.** `lab/executar.py` escreve `livro/numeros.tex` com um comando por grandeza, e o livro cita o comando em vez de digitar o número. Um número digitado à mão é defeito, não atalho: ele não pode divergir do laboratório porque não existe em dois lugares. Figura segue a mesma regra — o caderno a gera, o livro a inclui por caminho.
2. **Caderno em dia.** O critério é o **hash da fonte das células de código**, gravado em `metadata.execucao_hash`; o `--check` falha se algum caderno tiver fonte mais nova que o resultado. Editar markdown não invalida nada — e é por isso que a observação visual pode ser escrita depois da execução.
3. **Compilação limpa.** O livro compila com `latexmk -pdf -halt-on-error`: sem erro, sem referência ou citação indefinida. O `-pdf` é declarado porque sem ele o latexmk escolhe outro motor nesta máquina --- o LuaHBTeX, que não imprime o apóstrofo tipográfico da bibliografia e deixa o defeito só no log.

4. **Aterramento declarado.** `dados/aterramento.tsv` declara cada objeto do livro (símbolo ou termo) com o padrão que o acha, o capítulo em que ele aterra --- a âncora `% aterramento: <id>` --- e o que ele exige. `conferir_aterramento` reprova símbolo fora do registro, entrada morta, âncora declarada e ausente, uso antes da âncora, pré-requisito fora de ordem e número no nome
do arquivo diferente da posição do capítulo: é o §3.4 e o §3.5, que até aqui não tinham portão. O objeto que ainda não aterrou entra na fila (`aterrou` = `-`), e a fila não reprova --- ela é **aviso em toda execução**, porque a fila é o trabalho declarado.
`lab/executar.py --check` confere ainda duas coisas baratas e visíveis: toda citação do livro tem linha no corpus, e toda pergunta da lista tem as quatro partes declaradas.

**Passo visual, protocolo e não portão.** Toda figura sai também em `.png` justamente para ser **olhada**: um agente com entrada de imagem abre o PNG e escreve o que vê — forma das curvas, onde está a mudança, o que o eixo engana — numa célula de markdown do próprio caderno. O que ele escreve vira observação no capítulo, nunca número. **Uma sessão cujo modelo não tem entrada de imagem declara a falta e não inventa a leitura.**

**Passo de humanização, protocolo e não portão.** O texto é reescrito depois de medido e antes
do portão final, e a reescrita é **de voz**: nenhum número, prova, rótulo ou fonte muda, e a
conferência de que ela não estragou nada é que os portões mecânicos continuem limpos --- a
reescrita cita os mesmos comandos de `numeros.tex` e as mesmas figuras. O julgamento é de
leitura, e por isso o que se mede **antes** de cortar é a marca, e não a impressão: a frequência
da definição por negação ("não … : …"), a presença do epigrama em itálico fechando seção, a
metáfora única conduzida pelo capítulo inteiro, o ritmo (palavras por frase e a fração de frases
com cinco palavras ou menos) e o meta-comentário sobre o próprio livro. **A ferramenta automática
não serve para o português:** o `humanize_scan` devolve `aiScore 0` porque o catálogo dele é de
padrões em inglês e chinês; quem lê é o autor, e as contagens são a evidência em que ele se
apoia. A contagem tem ferramenta no laboratório: `lab/estilo.py` mede as cinco marcas capítulo
por capítulo — palavras por frase, fração de frases de até cinco palavras, a definição por
negação, a antítese, o epigrama de fecho, a palavra condutora e o meta-comentário — e **nada
nela reprova nada**: o que reprova é a leitura, e o que a leitura precisa é de número para saber
onde olhar. O **catálogo português de clichês mora no próprio medidor**, e não no plugin do
ambiente: as sete classes que a ferramenta usa --- abertura vazia, clichê, hesitação, transição de
molde, fecho de resumo, paralelismo mecânico e explicação em excesso --- escritas em português e
versionadas junto com o livro. O que a humanização **não** é: licença para inventar número, encurtar prova ou trocar
fonte.

## 10. O arquivo: `.old` é pedreira, não roteiro

Em `.old/` está tudo o que o projeto anterior produziu: o livro em 25 seções e 92 páginas, dois cadernos, um cérebro de consulta, o corpus de 234 fontes, os dados, os scripts e o notebook aposentado. Regras de uso:

- **pode ser minerado** por dados, fontes, resultados verificados e, principalmente, pela lista do que se provou verdadeiro — é o que os números de lá valem;
- **não é roteiro**: a ordem, a estrutura, os nomes e as conclusões do caminho antigo não têm autoridade aqui;
- **todo empréstimo é declarado** no capítulo onde entra, como coincidência (chegamos à mesma coisa por outro caminho) ou como herança explícita (usamos o resultado antigo, com esta procedência);
- **nada do `.old` entra no livro sem medição nova** quando a afirmação é numérica. Se o número antigo for reaproveitado, ele é remedido no laboratório novo, e é o número novo que entra.

## 11. Ciclo de trabalho

1. **Escolher o fracasso, não o capítulo.** Antes de escrever, diga em uma frase que tentativa concreta falha e com que número.
2. **Construir o mínimo.** Só o princípio que aquele fracasso exige. O que não for usado neste capítulo não entra nele.
3. **Medir.** O algoritmo entra na biblioteca (com o seu teste de propriedade); o caderno em `lab/experimentos/` chama a biblioteca, constrói o gráfico e grava o resultado. O número entra no texto pelo comando gerado e a figura por `\includegraphics`. Se houver como olhar a figura, o que se viu vai para o caderno.
4. **Fechar o arco** e deixar o fracasso seguinte visível.
5. **Humanizar.** Depois de medido e antes de conferir: reescrever a voz sem tocar em número,
   prova, rótulo ou fonte, medindo as marcas antes de cortar (§9). A humanização não é portão; o
   que ela não pode é derrubar os portões — se um comando sumir na reescrita, o `--check` acusa.
6. **Conferir:** `lab/executar.py --check`, compilação limpa, e a pergunta final — um leitor de
   dezesseis anos com vontade segue este capítulo sem pular?

## 12. Decisões registradas

> **As decisões dos ciclos anteriores moram em [`AGENTS-archive.md`](AGENTS-archive.md).**
> Ao fim de um ciclo elas descem para lá **na íntegra**, e ficam aqui só o índice de uma
> linha cada — a lição continua achável por busca, e o contrato continua legível. O arquivo
> é **registro, não contrato**: onde ele divergir deste documento, **este documento manda**.
>
> Ciclos arquivados: **2026-09-23** (47 entradas, abaixo).

### 12.1 Índice das decisões arquivadas

- 2026-09-23 — Recomeço do projeto. O material anterior foi arquivado em `.old` (commits `35f3514` e...
- 2026-09-23 — Escopo: zero absoluto. Só `assets/`, `LICENSE`, `pyproject.toml` e `uv.lock` atravessam; dados,...
- 2026-09-23 — Artefato: **o livro em LaTeX** é o produto, com um laboratório de scripts pequenos e...
- 2026-09-23 — Forma: **espiral** — cada capítulo abre num fracasso concreto e traz só o princípio que o...
- 2026-09-23 — Destino reaberto: nenhuma técnica está fixada de antemão; a pergunta é o que manda.
- 2026-09-23 — Critério de admissão: falseabilidade medida (as quatro partes).
- 2026-09-23 — Leitor: dezesseis anos ou mais, ensino médio e superior. O livro deve poder virar referência da...
- 2026-09-23 — Lista de perguntas **viva**: entra com refutador, sai quando o refutador for encontrado.
- 2026-09-23 — Divergência e convergência da lista de perguntas: 43 cruas, 18 depois da agregação por...
- 2026-09-23 — A travessia é família própria (F). F1 a F5 admitidas; F6 declarada em amadurecimento por falta...
- 2026-09-23 — A ordem é derivada de quem precisa de quem: raiz (a medição e o corte), cinco voltas,...
- 2026-09-23 — Fio condutor candidato, como hipótese e não como conclusão: promessa × entrega, em dados, em...
- 2026-09-23 — O experimento é um **caderno** — um por experimento —, não um script: separados na execução,...
- 2026-09-23 — `lab/executar.py` executa por hash da fonte das células de código, exige resultado gravado por...
- 2026-09-23 — O agente que escreve este livro tem nome: **Capiba**, gravado na seção 1. O nome não muda o que...
- 2026-09-23 — Os capítulos moram em **`livro/capitulos/`**, um arquivo por capítulo, nomeado pelo conceito.
- 2026-09-23 — O portão do dígito digitado distingue símbolo de grandeza: ignora argumento opcional, comando...
- 2026-09-23 — O gerador de números **recusa chave com dígito**, e o motivo é do TeX: ele encerra o nome de um...
- 2026-09-23 — Voz do livro reescrita.
- 2026-09-23 — O orçamento se compra com memória.
- 2026-09-23 — A forma da mudança decide o preço.
- 2026-09-23 — Comando órfão virou portão.
- 2026-09-23 — A humanização entrou no contrato como passo do ciclo
- 2026-09-23 — O catálogo português de clichês entrou no medidor
- 2026-09-23 — Sem replicação, uma semente não é uma medição.
- 2026-09-23 — O preço de um desenho é medido, não calculado.
- 2026-09-23 — A partilha só morde quando o orçamento é pobre.
- 2026-09-23 — No melhor esquecimento, o erro que sobra é ruído.
- 2026-09-23 — A margem cumpre a taxa prometida e paga mais fundo.
- 2026-09-23 — `mudanca.par_de_cauda` é o mundo do par controlado, com a correlação do corpo resolvida...
- 2026-09-23 — O atraso não cobra dias: cobra a mudança que coube nele.
- 2026-09-23 — O enquadramento fecha numa imagem: o agora é um retângulo.
- 2026-09-23 — Quarta vez que o `conferir_rotulos` pega um defeito real (`tab:atraso` já existia no capítulo...
- 2026-09-23 — A janela troca de sinal entre os mundos, e é o achado novo do fecho.
- 2026-09-23 — O fio condutor responde por três contas que não se convertem.
- 2026-09-23 — A régua da antítese estava torta, e a torta inflava capítulo alheio.
- 2026-09-23 — O capítulo 1 foi reescrito na voz trancada, medido antes e depois.
- 2026-09-23 — A régua de voz ainda tinha dois furos, na mesma família do primeiro.
- 2026-09-23 — Os capítulos 6, 7 e 8 lidos com a régua limpa: é voz, com uma exceção.
- 2026-09-23 — O portão dos nomes impede a volta.
- 2026-09-23 — A bibliografia imprimia o código da notação.
- 2026-09-23 — O log vazio passou por compilação limpa, e a lição estava no contrato.
- 2026-09-23 — A legenda longa era longa por repetição, não por precisão.
- 2026-09-23 — A auditoria de figuras contra o texto: 67 objetos, 24 com achado, e três erros de conteúdo no...
- 2026-09-23 — As figuras imprimiam português sem acento, e o gerador de nomes apagava a letra acentuada.
- 2026-09-23 — Cinco defeitos de eixo e de figura, corrigidos no código dos cadernos.
- 2026-09-23 — Os asteriscos que sobraram não estavam no livro.

- **2026-09-24.** **O aforismo do devir entra no contrato como intuição pré-técnica do autor, não no livro.** "O ser é o atrito dissipativo de um Real contraditório e termodinâmico: a razão resfria o fluxo ao recortar e fixar suas formas, enquanto a arte o reaquece ao fraturar e transfigurar esses limites: uma dança perpétua suspensa sobre o abismo indeterminado do devir" — o aforismo é a intuição pré-técnica do autor daquilo que o livro depois mediu: o corte fixa uma forma e cobra o preço de deixar o que muda de fora, e o que escapa da forma é o que decide. A mesma coisa, medida, está no capítulo 16 ("o resumo é sempre uma compressão, e o que escapa dela é o que decide") e, no projeto anterior, na frase "a barreira marginal subprotege". Fica aqui, não no livro, porque a voz do livro é didática para dezesseis anos e o §3 tranca o vocabulário. Não é coincidência (§10): semente e fruto são o mesmo caminho, não dois — o aforismo é a origem do caminho que o livro percorreu, não um segundo caminho independente, e o §10 só certifica dois caminhos.

- **2026-09-24.** **Duas contabilidades honestas do mesmo fatorial dão sinais opostos.** A seção "os buracos se compõem" do fecho mede se os três buracos (janela longa, atraso, mundo mudado) custam mais juntos do que a soma do que cada um custa sozinho. A resposta depende de onde se ancora a soma: somando os incrementos de cada buraco sobre a promessa, a pilha fica 49% acima (3,203 contra 2,151), e a seção está certa; na decomposição fatorial clássica, com efeitos principais medidos em torno da média geral do desenho, a célula dos três juntos fica ABAIXO da previsão aditiva em 0,374. As duas contas são verdadeiras e respondem a perguntas diferentes — a primeira pergunta se juntar os buracos custa mais do que a soma do que cada um custa sozinho, a segunda se os efeitos são independentes no desenho inteiro. **O que o livro não pode é imprimir o número de uma e a frase da outra**, que era o caso: 2,972 não é soma de barra nenhuma da figura, e agora o capítulo declara qual conta faz.

- **2026-09-24.** **O lote que morre na primeira âncora deixa as outras sem aplicar, e o rastro sai onde eu não olhava.** Um lote de dez substituições parava numa asserção; a primeira âncora tinha uma quebra de linha no meio e não casou, então **as nove restantes nunca foram aplicadas** — e eu segui adiante porque li a saída padrão (compilação limpa, portão limpo) como se o lote tivesse passado, enquanto o traceback tinha saído depois dela. O estrago ficou no livro: o capítulo 19 imprimia o número **novo** da soma do fecho com a frase **velha** que o descrevia mal, que é exatamente o defeito que esta sessão registrou como lição. Duas regras: **lote de edição aplica e RELATA cada item, nunca asserta e morre**; e **depois de aplicar, conferir o artefato por busca no arquivo** — o relato do script e o silêncio dele não são evidência. **A irmã dessa falha é mais silenciosa, e apareceu nesta rodada: a correção que aplica, mas só em UMA das camadas que repetem a mesma regra.** O capítulo 13 passou a dizer a regra do episódio que o código executa, e a docstring de `dependencia.py` e a leitura do caderno E14 continuaram dizendo a outra — a que mede vinte e seis episódios onde o instrumento mede trinta e cinco. Onde a mesma regra vive em três lugares, o lote só está aplicado quando os três concordam; conferir a camada que foi corrigida não diz nada sobre as outras.


- **2026-09-24.** **A mesma tolerância tinha duas unidades, e a prosa dizia uma enquanto o critério media na outra.** O capítulo declara 0,15, e ele vivia com dois significados --- fração do degrau, na proposição da meia-vida, e fração do nível novo, no critério de viabilidade ---, e num mundo que dobra 15% do nível é 30% do degrau. A decisão é do autor, e ele a tomou: a tolerância é do **nível novo**, que é a unidade do erro medido. O conserto separa as duas em todo o caminho: `esquecimento.TOLERANCIA`, `FATOR_PADRAO` e `TOLERANCIA_DEGRAU` são três constantes, o `limiar` converte explicitamente, e três asserções novas no `auto_teste` fixam a ponte. A lição: **um número só com dois significados é a porta pela qual o defeito entra**.


- **2026-09-24.** **O cleveref imprime o nome do CONTADOR, e o livro imprimia "a teorema 15.1".** A leitura da página compilada do capítulo 11 — a tabela que esta rodada reescreveu — mostrou "os dias que a **teorema** 11.2 prevê", com artigo feminino. No PDF inteiro: **7 referências, todas a proposições, todas impressas "teorema X.Y"**, nenhuma "proposição X.Y", e **nenhum ambiente `teorema` existe no livro**. O nome que o cleveref cunha é o do **contador**, não o do ambiente, e os sete ambientes de teorema do livro compartilham o contador `teorema`. Os `\crefname` estavam declarados um por um — que é exatamente o que o `conferir_nomes` exigia —, e por isso o portão passava com a página errada: **o portão conferia o nome, e o defeito estava no contador**. Seis das sete frases foram escritas com artigo feminino ("na teorema 1.1", "da teorema 15.1"), o que mostra que o texto esperava "proposição" e ninguém leu o que saía. Conserto: o contador de base virou `proposicao`, o tipo que o livro de fato referencia, e os outros ambientes continuam compartilhando ele — **a numeração não mudou em lugar nenhum**; só o nome impresso. Uma frase trocou de artigo (o capítulo 12, a única escrita no masculino). E o `conferir_nomes` ganhou o ramo que faltava: lê os `
ewtheorem` do preâmbulo e **reprova** o `\cref` cujo ambiente não seja dono do contador, dizendo o que sairia na página; testado nos dois ramos, limpo no estado real e acusando com um `\cref{def:...}` de teste.

- **2026-09-24.** **O livro ganhou as seis partes que a espiral já tinha.** A estrutura vivia só no comentário do fonte e nesta seção, e o sumário era uma lista plana de dezenove capítulos: agora há **A raiz** (cap. 1), **As voltas** (2 a 8), **A travessia** (9 a 14), **O que não se compra** (15 a 17), **O enquadramento** (18 e 19) e **O fecho** (20), cada uma com uma nota de abertura de duas a quatro frases — prosa simples, sem itálico de epigrama e sem meta-comentário, como o §3 tranca. Sem babel a folha de parte imprimiria "Part I": `\renewcommand{\partname}{Parte}` entrou, o `conferir_nomes` **exige** a troca e o mapa de prefixos ganhou `par: part`. Os dois ramos foram provados por teste negativo: sem o `\partname` o portão acusa "Part I", e sem `\crefname{part}`, com um `\cref{par:...}` de teste, acusa o nome em inglês.

- **2026-09-24.** **O capítulo 2 era dois capítulos colados.** Ele tinha 400 linhas contra uma mediana de 160 e carregava três objetos: o vigia do bloco, a segunda leitura do mesmo corte e — em "A forma decide o preço" — um **segundo instrumento**, a média da janela em erros-padrão dela mesma, medida em outro caderno (E03). Virou **2 O orçamento do alarme** (E02) e **3 A forma decide o preço** (E03), cada um com o seu "O que fica", e os capítulos 3 a 19 andaram uma casa: arquivos renomeados com `git mv`, `\input`, comentários-cabeçalho e a referência interna do antigo capítulo 4. **O log acima não é reescrito — esta entrada é o mapa.** O que autoriza a renumeração, conferido antes: o livro não imprime número de capítulo em prosa (só em comentário), os rótulos são simbólicos e as proposições acompanham sozinhas.

- **2026-09-24.** **A leitura do texto achou três frases que nenhum portão via.** No capítulo 9 a oração "e por isso a mudança é posta de propósito" aparecia **duas vezes** na mesma frase; no capítulo 8 faltava a fronteira entre dois períodos ("...a mesma forma nos três**, Se** o mecanismo..."); e no capítulo 19 o texto dizia "com atraso **de nenhum atraso a** `\numAgoraAtrasoMaior{}` dias", com a palavra repetida no lugar de "nenhum dia". Junto: a única aspa francesa do livro (cap. 12), um clichê de explicação em excesso (cap. 7) e o exemplo mínimo que faltava em duas seções de definição (o ato e a resposta, no cap. 10, e o esquecimento com taxa, no cap. 12) — mais o "O que fica" do capítulo 1, que era o único dos vinte sem o ritual de fecho. A lição é a que já custou três rodadas: **o portão amarra número a medição, não afirmação a medição** — quem acha frase partida é a leitura da página.

- **2026-09-24.** **A leitura integral do texto e das legendas, e a lição de onde o defeito morava.** Os vinte capítulos foram lidos de ponta a ponta (cinco leitores independentes nos capítulos 9 a 20) e as legendas de todas as figuras conferidas contra o código que as desenha, com cada comando cruzado contra o caderno. Vinte e uma correções, e quase todas no mesmo lugar: **a frase que comenta o número, não o número**. Duas armadilhas de língua atravessaram dez rodadas de portão: **"previria"** (do verbo previr) onde o livro quer **"preveria"** (de prever), e **"1,168 vez"** onde numeral não unitário pede plural. A rodada seguinte virou a mesma leitura para as figuras: quatro auditores leram cada figura e cada tabela contra o desenho (o PNG pela ponte de visão, e a geometria medida no pixel) e acharam treze legendas contando mundos ou barras que o desenho não tem, um painel com o alvo trocado e dois eixos dizendo a unidade errada. A lição: **o portão amarra número a medição, não afirmação a medição --- e a legenda é a frase que ninguém relê.**

- **2026-09-24.** **O §3.5 virou portão: todo objeto do livro tem de estar aterrado, ou declarado na fila.** A varredura em ordem de leitura (a ordem dos `\input`, e não a do nome do arquivo) achou 30 símbolos de matemática e mostrou o estado real: "variável aleatória", "densidade", "covariância", "lei dos grandes números", "derivada", "integral", "simulação" e "semente" **não aparecem em página nenhuma**; a "esperança" entra no cap. 16 dentro do GARCH, a "variância" no 10 e a "curtose" no 17 em cabeçalho de tabela. Entraram `dados/aterramento.tsv` (66 objetos: endereço, nunca definição) e `lab/aterramento.py`, com o portão `conferir_aterramento` cobrando símbolo registrado, entrada viva, âncora existente, uso depois dela e pré-requisito em ordem --- os seis ramos provados por teste negativo, um a um, com o livro real passando limpo. O objeto na fila vira **aviso**, e os 66 avisos são o trabalho declarado que falta.

- **2026-09-24.** **O motor do livro passou a ser declarado, e o portão passou a nomeá-lo.** O mesmo `latexmk` de sempre escolheu nesta árvore o LuaHBTeX em vez do pdfTeX, e o log dele traz `Missing character` para o apóstrofo tipográfico dos títulos: o livro compilava, o PDF safa e faltava uma letra no papel. O portão da compilação acusava «log sem compilação` com 46 KB de log dentro. O `-pdf` entrou no §9.3 e a mensagem passou a imprimir a máquina que escreveu o log.


- **2026-09-24.** **A raiz ganhou o capítulo que faltava: o número e a barra.** O livro media com máquinas que nunca construía --- sorteava mundos inteiros e tirava média de muitos sorteios sem que "sorteio", "média" e "variância" fossem construídos em lugar nenhum. O capítulo abre nos dois números do índice (a fração de altas nos últimos vinte e um pregões e nos últimos duzentos e cinquenta e dois), constrói sorteio, lei, probabilidade como frequência, variável aleatória, média, variância e desvio, prova a barra da fração contando os pares de dias e mede em quatro mil mundos por janela. No dado, as janelas de vinte e um dias têm dispersão de 10,40 contra a barra de 10,86 (razão 0,957), e a leitura é que **o que muda no mundo não é a média**. Dois registros de método: o plano previa **dois** capítulos novos na raiz e o segundo (a taxa, o decaimento, o ponto fixo) **não entrou**, porque esse material já tem onde nascer --- o logaritmo vive no capítulo 2, a recursão no 12 e no 14 --- e capítulo de preparação sem fracasso próprio não é capítulo (§4); e a ordem que o portão cobra passou a ser a de **capítulo**, não a de linha, porque o §4 manda cada capítulo abrir num fracasso que nomeia o objeto antes de o construir.

- **2026-09-24.** **O livro ganhou um capítulo 1 e todos os outros andaram uma casa --- este é o mapa.** O capítulo novo (o número e a barra) entrou antes da raiz antiga, e com ele as partes ficaram assim: **A raiz (1 e 2), As voltas (3 a 9), A travessia (10 a 15), O que não se compra (16 a 18), O enquadramento (19 e 20), O fecho (21)** --- vinte e um capítulos, seis partes. Os cadernos E01 a E21 seguem com os mesmos ids: o id do experimento é estável e **não** segue o número do capítulo. A renumeração foi um deslocamento de mais um em tudo: os vinte arquivos renomeados com `git mv`, os `\input` e os comentários do `livro.tex`, os cabeçalhos «% CAPÍTULO n`, e as referências numéricas em `lib/`, `lab/` e nos cadernos. **O log acima não é reescrito --- esta entrada é o mapa.** Dois defeitos que a varredura sozinha deixou passar e a conferência por busca no arquivo pegou: a faixa «capítulos 2 e 4` virou «3 e 4`, porque o segundo número não estava colado na palavra, e uma referência sem acento («capitulo 11`) escapou do padrão acentuado. Entrou o ramo da renumeração no portão --- o número no nome do arquivo tem de ser a posição do capítulo na ordem de leitura ---, provado por teste negativo.

- **2026-09-24.** **O segundo capítulo novo entrou, e o livro está em vinte e dois --- este é o mapa.** «O que a soma guarda` abre na conta que soma as porcentagens diárias para saber o que o índice andou: num mês as duas contas quase coincidem, e em vinte e seis anos a soma entrega metade do que aconteceu, sem que nada na conta avise. Ele constrói o **nível** e o **incremento** como dois objetos, o **logaritmo** como a operação que troca multiplicação por soma, o **retorno**, e a **banda do nível**, que cresce com a raiz do horizonte --- proposição própria, medida em quatro mil mundos e depois na série, onde ela exagera porque o desvio de um dia é carregado por poucos dias. Caderno E22 e o módulo `nivel` na biblioteca. As partes ficaram: **A raiz (1 a 3), As voltas (4 a 10), A travessia (11 a 16), O que não se compra (17 a 19), O enquadramento (21 a 23), O fecho (24)**. A renumeração foi o deslocamento de mais um nos vinte arquivos, nos `\input`, nos cabeçalhos, nas referências de `lib/` e `lab/` e nas âncoras do registro; o logaritmo e o índice `t` passaram a ser aterrados no capítulo 2, e o capítulo 3 perdeu o parágrafo que os construía, porque agora ele cita. **O log acima não é reescrito --- esta entrada é o mapa.** O portão ganhou uma regra: o que está dentro de um `\text{}` é prosa, e não símbolo --- sem ela, o artigo «a` de «a soma das duas` era lido como o coeficiente de memória e acusava uso antes de aterrar.

- **2026-09-24.** **O segundo sumário saiu vazio, e o conserto é gerar de fora.** O livro ganhou um «Sumário completo» no fim, e a primeira tentativa foi um segundo `\tableofcontents`: a página saiu com o título e mais nada. A causa é do LaTeX, e não do texto --- o `.toc` é aberto para escrita no começo da compilação e lido de novo quando o `\tableofcontents` aparece, de modo que no fim do documento o arquivo ainda está pela metade. O conserto é o `lab/sumario.py`: ele copia o `.toc` da compilação anterior para `livro/sumario.tex` (154 entradas: 6 partes, 26 capítulos, 122 seções), o livro inclui o arquivo, e a lista de gerados do portão passou de dois para três nomes. E a bibliografia deixou de ficar fora do mapa: o `\bibname` virou **Referências** e a entrada no sumário sai do próprio gerador de fontes, para cair na página em que a lista começa. E as três listas do fim --- figuras, tabelas e os enunciados numerados --- entraram: as duas primeiras pelo mecanismo da classe, que funciona ali porque é a primeira vez que aparecem na compilação, e a terceira gerada do `.aux`. A leitura da página nova achou o defeito que faltava: **a página de capítulo sem número herda o cabeçalho corrente do anterior** --- o sumário completo saiu com REFERÊNCIAS em cima ---, e o `conferir_nomes` passou a exigir um `\markboth` para cada `\chapter*`.
- **2026-09-24.** **O paratexto tinha quatro frases cortadas no meio da palavra, e nenhum portão olhava para lá.** O lote do commit `42970e5` (as seis notas de parte expandidas) inseriu **cada nota expandida na parte anterior à sua**: em `livro.tex` ficaram `...antes de ` (:197), `...outra perna d` (:218), `...o que se perdeu` sem ponto (:255) e `...ficou da` (:263), e o bloco das Partes IV, V e VI imprimiu **dentro do fecho do capítulo 7** (pp. 56–57), entregando a resposta que o capítulo 22 vende como sua setenta e seis páginas antes. Zero de seis notas imprimia inteira na sua parte. Cada parte fica com a **versão expandida**; a curta sai. Nasce o `conferir_paratexto` --- `\chapter*` sem `\addcontentsline` (o "Sumário completo" era invisível para as três listas) e parágrafo de prosa sem pontuação final ---, falsificado nos dois sentidos antes de entrar.


- **2026-09-24.** **O capítulo 22: o teto do posto, e a diferença entre a dispersão e o erro-padrão.** A cláusula "com o posto acompanhando a janela para que a taxa anunciada não mude" era **falsa**: `k = teto(0,05 n)` avaliado em `k/(n+1)` assina **5,512%** na janela curta, **5,138%** na média e **5,149%** na longa --- a própria docstring de `promessa.posto` já dizia 5,14%. O denominador do capítulo continua sendo **a promessa declarada** (5%), porque o livro distingue "a promessa" da "conta do corte" do capítulo 21, que é a taxa assinada; e o capítulo passa a imprimir as três taxas assinadas. E uma lição de estatística que o próprio medidor confundiu: a **dispersão entre os mundos** (0,2499) e o **erro-padrão da média** (0,05589) são objetos diferentes --- dividir pela primeira dá 0,46 desvio, pela segunda, 2,07, e é o segundo que responde "a janela longa entrega mesmo menos?". Os dois ficam impressos.

- **2026-09-24.** **A causa do √h exagerar é a ORDEM dos dias, e não a cauda --- a entrada acima fica corrigida.** A entrada do capítulo 2 diz que a banda exagera "porque o desvio de um dia é carregado por poucos dias"; a causa medida é a **autocorrelação de um dia**, `numSomaRhoUm` = −0,09896. Baralhando os retornos (os mesmos dias enormes, todos, em outra ordem) a razão no mês vai de 0,866 a **0,9973** em 200 baralhamentos, e em cinco anos a 0,8407 --- o que resta ali é do próprio estimador, que mede janelas sobrepostas. O E22 passa a gravar `rho_um` e o controle baralhado, e a monotonia do parágrafo cai (0,866 / 0,8153 / 0,8821 / 0,7104 não é escada).

- **2026-09-24.** **A oscilação do capítulo 8 tem sessenta dias, e o controle do ano entra no texto.** A prosa chamava de "a oscilação do ano" o denominador que o caderno mede em **60 dias** (`BLOCO = 60`, o bloco do capítulo do alarme). O E06 passa a rodar o mesmo posto com o denominador de 252 dias como **controle declarado**: o sinal cai de `numEstabilidadeRelativoPosto` = 0,2627 para `numEstabilidadeRelativoAnoPosto` = 0,05187 --- o que o nível do corte carrega além da oscilação é do bloco de sessenta dias, e não do ano. Duas frases menores do mesmo lote de defeitos: o capítulo 4 dizia que 13 era "um número que o mundo parado nunca alcançou" (ele alcança, e 0,6% dos mundos parados soam), e o capítulo 18 definia θ em fração da **escala** e a chamava de fração do **degrau** na linha seguinte.


- **2026-09-24.** **A contagem de sobreviventes deixa de ser um sorteio publicado como medida.** Os capítulos 9 e 10 faziam a MESMA pergunta com duas grades (180 e 125 membros) e duas sementes (131 e 211), e o livro imprimia as duas respostas --- dois membros e zero explicações ---, com o capítulo 12 construído sobre "as duas". A grade passa a ser uma só (a do capítulo 9) e a contagem ganha replicação de dez: no capítulo 9 ela vai de 0 a 5, mediana 2,5; no 10, de 0 a 7, mediana 3. O zero da legenda sai, o fecho do 10 deixa de emprestar "as duas" do primeiro mercado e o 12 passa a falar de duas **famílias** de explicação. Fica a lição de portão: a lista \`CITADAS_NO_LIVRO\` de cada caderno filtra o JSON, e medida nova que o livro cita precisa entrar nela --- senão o número existe no caderno e não chega ao papel.

- **2026-09-24.** **O nulo carrega o mesmo deslocamento, e o pico deixa de ser do par.** O capítulo 16 media o adiantamento do par contra um nulo **sem** o deslocamento que o próprio controle aplica: com o mesmo atraso declarado, o nulo vai de −0,0138 a **+0,344** (±0,1022) no atraso de um dia --- um par sem adiantamento nenhum pica no mesmo lugar. O E14 passa a varrer o atraso também nos pares sorteados e a medir o nulo no comprimento de um pedaço (borda de dois desvios em 0,6093, que nenhum dos quatro pedaços alcança sozinho). O capítulo passa a dizer que a varredura delimita um intervalo curto e **não** separa um dia de dois.

- **2026-09-24.** **A fronteira do esquecimento é do sorteio tanto quanto do dado.** A memória mínima de vinte e um dias saía de 0,150561 contra a tolerância de 0,15 --- margem de 0,0006 contra um erro-padrão de 0,0039 ---, e o capítulo imprimia a dispersão só da candidata **vencedora**. O E12 passa a gravar a da que perde e a repetir a medida em cinco bases independentes: a memória de dez dias fica dentro da tolerância em **duas** delas, com o erro indo de 0,1410 a 0,1513. O que a medição sustenta é a ordem de grandeza.

- **2026-09-24.** **No capítulo 19 o que fica parado é a correlação, e a escala entra na conta.** A família do choque comum conserva a correlação e **não** os segundos momentos --- a docstring de \`mudanca.par_de_cauda\` já declarava que a margem não é preservada, e a prosa dizia o contrário. O E17 passa a medir a variância da margem de cada mundo, a perda com cada perna padronizada pela própria escala (razão 1,144 contra 1,551) e uma gaussiana de mesma covariância (1,472 dos 1,551): a maior parte do crescimento da perda conjunta é a margem que o choque engrossou.


- **2026-09-24.** **O livro ganhou formato de livro: página brasileira de 16 x 23 cm, com o aparato da ABNT.** A página deixou de ser A4. O corte passou a ser o do livro brasileiro de texto técnico, 16 x 23 cm, com as margens da NBR 14724 (3 cm na esquerda e no topo, 2 cm na direita e no pé), fonte Times em 12 pt --- uma das duas que a norma nomeia, porque a distribuição local não traz o newtx ---, entrelinha de um e meio, paginação no canto superior direito (inclusive na abertura de capítulo) e título corrente à esquerda. O livro passou de 171 para **275 páginas**. **Quinze tabelas** estouraram a mancha nova (a linha caiu de 15,2 cm para 11 cm) e foram ajustadas com resizebox em largura de linha, e uma equação do capítulo 2 foi partida em duas linhas --- sem o ambiente gathered, que o portão do aterramento acusou, com razão, como símbolo fora do registro. **O aparato em ABNT:** as referências passam a sair em NBR 6023 (sobrenome em caixa alta, título em negrito) pelo lab/fontes.py; o ano duplicado de 52 entradas morreu, porque o periódico já o carregava no campo veiculo; e a chamada da citação subiu para sobrescrito (NBR 10520, sistema numérico). Fica declarado o que a ABNT ainda pediria e este formato não faz: a lista impressa é o corpus inteiro (240 fontes) e não as 18 citadas na ordem de citação, e a folha de rosto não traz autor, local nem ano --- as duas são decisão de conteúdo, não de formato.
- **2026-09-24.** **O contrato emagreceu por arquivamento, e não por poda --- a poda não pagava a conta.** O `AGENTS.md` estava em 70.870 bytes contra o teto de ~67 KB declarado. A regra de poda do §12 tira a entrada cujo conteúdo já vive no cabeçalho do capítulo, no portão, no caderno ou no `.gitignore` que a criou; aplicada por medição --- frases de 45 caracteres ou mais com shingles de seis palavras já presentes nos 349 KB de `lab/` e `lib/frevolab/` ---, ela encontrou **uma** entrada em 71: a do ordinal nu, 659 bytes, cuja lição está inteira na docstring do `conferir_ordinais`, que passou a ser o registro dela. As outras 70 não têm duplicata em lugar nenhum --- são lição de método, que a mesma regra manda preservar. A saída foi então **outra operação, e não uma poda**: as 47 decisões do ciclo de 2026-09-23 desceram **na íntegra** para `AGENTS-archive.md` (sha256 conferido antes e depois), e ficaram no §12 as 24 do ciclo corrente mais o índice de uma linha por entrada arquivada. O contrato foi a 56.009 bytes, a lição continua achável por busca, e a regra passa a valer para todo ciclo que se fechar.
