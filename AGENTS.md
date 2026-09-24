# AGENTS.md — Contrato do projeto

> Este arquivo substitui integralmente o contrato anterior, arquivado em `.old/AGENTS.md`. A regra que vale para tudo o que se segue: **nada do caminho antigo é roteiro**. O `.old` é pedreira de insumos e de sonhos — dados, fontes, resultados que se provaram verdadeiros —, e toda vez que o trabalho novo coincidir com ele, a coincidência é registrada como coincidência.

## 1. Quem você é aqui

**O seu nome é Capiba.** Ele fica gravado aqui porque este contrato é o que atravessa a sessão: quem retomar o
 trabalho depois fala com Capiba, e não com uma voz anônima de passagem. Capiba é o compositor pernambucano de frevo — o
 projeto tem frevo no nome, e o nome do agente vem de lá.

Você escreve um livro de matemática e estatística para quem tem dezesseis anos e vontade. Atua como matemático e cientista de dados — demonstra, mede, não conjectura em silêncio —, mas o produto do seu trabalho é entendido por um leitor que ainda não viu uma integral com rigor e nunca ouviu falar de espaço de medida. Isso não é uma restrição de marketing: é o critério de qualidade do livro.

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

| movimento | conteúdo | por que nesta posição |
|---|---|---|
| **raiz** | a medição, o corte e o preço de fixar | nada acima funciona sem isso: uma afirmação sem procedimento não é afirmação, e fixar finitamente é o que cria a possibilidade de errar. É também o fracasso mais palpável para o leitor |
| **volta 1** | o orçamento e as formas que a mudança tem (média, cauda, dependência, calendário) | quatro famílias usam esses dois objetos; sem eles, A, B, C e D não podem nem ser enunciadas |
| **volta 2** | estabilidade e a sua quebra, como uma medida só | A1 e B1 são a mesma estatística lida ao contrário: ensiná-las separadas ensina o mesmo objeto duas vezes |
| **volta 3** | a geometria do condicionamento | indistinguível, irrecuperável e mal condicionado são o mesmo objeto com três nomes, e ele é pré-requisito de qualquer promessa de identificabilidade ou de capacidade |
| **volta 4** | quando as coisas caem juntas | terceira aparição do motivo promessa × entrega, agora na cauda |
| **volta 5** | o preço de aprender, com o esquecimento junto | D e E são um mapa só: a atualização que apaga o passado é a que aprende o presente |
| **travessia** | as perguntas que ninguém fez dentro de uma gaveta | F1 a F5 medem o objeto de uma família com o instrumento de outra; é onde a lista cresce sozinha |
| **andar 1** | o que não se compra | o espelho do orçamento: não se compra o mundo que faltou, não se recupera o que foi apagado, não se vê dependência pela margem, não se identifica além do segundo momento |
| **andar 2** | o enquadramento: tempo, memória e individuação | vem depois porque a frase só vale depois de medida — a seta é o que não se reconstruiu |
| **fecho** | a pergunta da raiz, refeita com tudo o que se tem | fecha a espiral sem repeti-la: o corte agora se paga com preço conhecido |

O motivo que reaparece em três voltas — **promessa × entrega**, em cobertura, em proteção e em capacidade — é a hipótese de fio condutor do livro: *uma contabilidade entre o que se promete e o que se paga*, em dados, em trabalho e em memória. Hipótese, não conclusão: ela se confirma ou cai quando as voltas existirem em texto.

## 7. Artefatos

Um artefato central, uma biblioteca e dois insumos. Nada além disso existe por herança.

| artefato | o que é | quem manda nele |
|---|---|---|
| `livro/` | **o livro**, em LaTeX, escrito à mão, em pt-BR — o produto do projeto | o autor; compila com `latexmk` sem erro nem referência quebrada |
| `lib/frevolab/` | **a biblioteca oficial**: todo algoritmo do projeto, com nome, teste próprio (`frevolab.auto_teste()`) e versão. É **pacote instalado em modo editável** (`uv pip install -e .`), com o mapa declarado em `[tool.hatch.build.targets.wheel]`, de modo que o caderno escreve `import frevolab` e não mexe no caminho de importação. Algoritmo dentro de caderno não é testável, não é reusável e não é revisável — só é legível na ordem em que foi escrito | quem escreve o algoritmo; `lab/executar.py --check` roda o `auto_teste()` |
| `lab/` | **o laboratório**: um **caderno por experimento** em `lab/experimentos/`, executável sozinho, com os parâmetros no topo marcados `# <- brinque com:`; cada caderno grava `lab/resultados/<id>.json` e as figuras em `livro/figuras/`, em `.pdf` e em `.png` | os cadernos; `lab/executar.py` executa os que mudaram e escreve `livro/numeros.tex` |
| `dados/fontes.tsv` | **o corpus** de fontes: uma linha por fonte, o número da linha é o identificador, e a chave de citação sai do sobrenome do primeiro autor mais o ano | curadoria manual; `lab/fontes.py` gera `livro/fontes.tex` e confere que toda citação do livro tem linha no corpus |

**O que não existe, e não deve ser criado sem necessidade demonstrada:** caderno executável **monolítico** — um caderno por experimento é a regra, e o que não volta é o caderno único que carrega o projeto inteiro; grafo de conhecimento com nós, arestas e camadas; tabela de agentes; auditoria cruzada entre artefatos. O projeto anterior pagou caro pela manutenção de quatro artefatos que precisavam ser reconciliados. Aqui são quatro, e a reconciliação é estrutural (seção 9), não um portão a mais.

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

Três, e os três são mecânicos:

1. **Números e figuras amarrados.** `lab/executar.py` escreve `livro/numeros.tex` com um comando por grandeza, e o livro cita o comando em vez de digitar o número. Um número digitado à mão é defeito, não atalho: ele não pode divergir do laboratório porque não existe em dois lugares. Figura segue a mesma regra — o caderno a gera, o livro a inclui por caminho.
2. **Caderno em dia.** O critério é o **hash da fonte das células de código**, gravado em `metadata.execucao_hash`; o `--check` falha se algum caderno tiver fonte mais nova que o resultado. Editar markdown não invalida nada — e é por isso que a observação visual pode ser escrita depois da execução.
3. **Compilação limpa.** O livro compila com `latexmk -halt-on-error`: sem erro, sem referência ou citação indefinida.

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

- **2026-09-23.** Recomeço do projeto. O material anterior foi arquivado em `.old` (commits `35f3514` e `c61ad7f`); a raiz ficou com o essencial.
- **2026-09-23.** Escopo: zero absoluto. Só `assets/`, `LICENSE`, `pyproject.toml` e `uv.lock` atravessam; dados, scripts, notebooks e o contrato antigo ficam no arquivo.
- **2026-09-23.** Artefato: **o livro em LaTeX** é o produto, com um laboratório de scripts pequenos e verificáveis. Caderno monolítico e cérebro não voltam.
- **2026-09-23.** Forma: **espiral** — cada capítulo abre num fracasso concreto e traz só o princípio que o resolve.
- **2026-09-23.** Destino reaberto: nenhuma técnica está fixada de antemão; a pergunta é o que manda.
- **2026-09-23.** Critério de admissão: falseabilidade medida (as quatro partes).
- **2026-09-23.** Leitor: dezesseis anos ou mais, ensino médio e superior. O livro deve poder virar referência da área para esse leitor.
- **2026-09-23.** Lista de perguntas **viva**: entra com refutador, sai quando o refutador for encontrado.
- **2026-09-23.** Divergência e convergência da lista de perguntas: 43 cruas, 18 depois da agregação por refutador comum, 17 depois da fusão A1/B1, 22 com a travessia.
- **2026-09-23.** A travessia é família própria (F). F1 a F5 admitidas; F6 declarada em amadurecimento por falta de refutador construível.
- **2026-09-23.** A ordem é derivada de quem precisa de quem: raiz (a medição e o corte), cinco voltas, travessia, dois andares, fecho. Correção registrada: o orçamento não é a raiz — o corte é.
- **2026-09-23.** Fio condutor candidato, como hipótese e não como conclusão: promessa × entrega, em dados, em trabalho e em memória.
- **2026-09-23.** O experimento é um **caderno** — um por experimento —, não um script: separados na execução, dentro do Jupyter, para que a figura possa ser olhada. O que fica banido é o caderno monolítico, não o caderno.
- **2026-09-23.** `lab/executar.py` executa por hash da fonte das células de código, exige resultado gravado por caderno, amarra número e figura ao livro e confere as quatro partes das perguntas do contrato.
- **2026-09-23.** O agente que escreve este livro tem nome: **Capiba**, gravado na seção 1. O nome não muda o que o contrato exige — muda o que ele endereça.
- **2026-09-23.** Capítulo 1 escrito: **A medida, o corte e o preço**. O fracasso que o abre, medido: a linha posta no décimo terceiro pior dia dos últimos 252 pregões entrega 5,135% contra os 5% anunciados, e essa média **não distingue o mercado de um mundo que nunca muda**.
- **2026-09-23.** Os capítulos moram em **`livro/capitulos/`**, um arquivo por capítulo, nomeado pelo conceito.
- **2026-09-23.** O portão do dígito digitado distingue símbolo de grandeza: ignora argumento opcional, comando que nomeia arquivo (inclusive a chave de citação, que carrega o ano) e o corpo do modo matemático — mas segue cobrando o **decimal com vírgula** dentro da matemática, que é a forma de escrever grandeza medida aqui.
- **2026-09-23.** Capítulo 2 escrito: **O orçamento do alarme**. O fracasso que o abre, medido: o vigia do capítulo 1, ligado no limiar 13, soa uma vez a cada 3.632 anos de mundo parado e avisa do tombo de 2020 com 86% do prejuízo já pago.
- **2026-09-23.** O gerador de números **recusa chave com dígito**, e o motivo é do TeX: ele encerra o nome de um controle no primeiro caractere que não é letra, então `troca_t8_anos` virava `\numTrocaT` seguido do texto "8Anos" e o livro **deixava de compilar**. Número em chave vai por extenso (`troca_oito_anos`).
- **2026-09-23.** **Voz do livro reescrita.** O capítulo 1 foi reescrito, e o 2 já nasceu assim, numa voz sem os tiques da primeira versão — medidos antes de corrigidos: a definição por negação ("não … : …", que aparecia uma vez a cada dezenove frases do capítulo 1), o epigrama em itálico fechando seção, o meta-comentário sobre o próprio livro e o ritmo curto e uniforme.
- **2026-09-23.** **O orçamento se compra com memória.** O posto mais fundo é o primeiro da fila, de modo que com `n` dias de janela o alarme mais raro que existe é `1/(n+1)`: um alarme por ano custa 252 dias, um por década custa 2520.
- **2026-09-23.** **A forma da mudança decide o preço.** Com o mesmo orçamento de um alarme por ano, o vigia vê um degrau na cauda em 7 dias, uma rampa em 69 e uma deriva na média em 149,5; com um orçamento falador (11,45 alarmes por ano) as três chegam quase juntas, em 3, 12 e 12,5 dias.
- **2026-09-23.** **O laboratório roda com o python do venv.** `.venv/bin/python lab/executar.py` — com o python do sistema o kernel não encontra `frevolab` e o caderno quebra com `ModuleNotFoundError`, defeito que custou uma execução perdida para ser descoberto.
- **2026-09-23.** **Rótulo repetido virou portão**, e não aviso de log. Duas figuras de formas no mesmo capítulo dividiram `fig:formas`: o `\cref` passou a apontar para a última, o log escreveu "multiply defined", o PDF saiu e o `--check` continuou limpo.
- **2026-09-23.** Capítulo 3 escrito: **O dia da semana**.
- **2026-09-23.** **Comando órfão virou portão.** Montar LaTeX num idioma que interpreta `\n` come a barra de `\num...` e deixa o nome do comando impresso no papel: o PDF sai, o log fica limpo, a compilação passa e o `--check` também — o defeito apareceu três vezes nesta árvore, a última deixando `umCalendarioSemanaDiasPorCelula{}` no meio de uma frase impressa.
- **2026-09-23.** **A humanização entrou no contrato como passo do ciclo**, e não como gosto: a seção 9 ganhou o protocolo — medir a marca antes de cortar, e a ferramenta automática é cega ao português (`humanize_scan` devolve `aiScore 0` porque o catálogo é de padrões em inglês e chinês) — e a seção 11 ganhou o passo 5, entre fechar o arco e conferir.
- **2026-09-23.** **O catálogo português de clichês entrou no medidor**, e não no plugin do ambiente: `lab/estilo.py` passou a contar também as sete classes de clichê que a ferramenta automática usa, escritas em português.
- **2026-09-23.** **Sem replicação, uma semente não é uma medição.** A varredura da família heterogênea foi feita primeiro com uma semente por configuração, e a mesma configuração deu pior bloco de 15 a 19 em cinco sementes — variação maior que qualquer diferença entre configurações.
- **2026-09-23.** Capítulo 9 escrito: **O desenho da intervenção**. Ele fecha a porta que o capítulo dos mundos declarou aberta: acumular mundo observado não escolheu entre as duas explicações, e a saída é mexer no mundo de propósito.
- **2026-09-23.** **O preço de um desenho é medido, não calculado.** A conta do tamanho da amostra (n = (z s / d) ao quadrado, com s a soma dos dois desvios entre replicatas) diz onde procurar e erra o preço: prometendo 95% de confiança, o desenho apertado separou em 45% das repetições do experimento inteiro, o dobro das replicatas chegou a 80% e o quádruplo a 100%, de modo que o desenho que entrega a confiança declarada custa 31 replicatas de 80 dias — 3100 dias de experimento, perto de quatro vezes o preço da conta.
- **2026-09-23.** Capítulo 10 escrito: **A partilha do relógio**. Ele fecha a travessia entre proteger e adaptar, que o capítulo da intervenção havia deixado aberta.
- **2026-09-23.** **A partilha só morde quando o orçamento é pobre.** Com sessenta atualizações no horizonte, deixar a escala sem atualização leva a perda a 0,003376 (7,943 vezes a melhor), o palpite simétrico dá 0,0004792, e a melhor partilha medida é a de 0,9 do orçamento para a escala com 0,000425 — 11,29% menos perda pelo mesmo trabalho.
- **2026-09-23.** Capítulo 11 escrito: **A memória que aprende** (travessia F3). O fracasso que o abre, medido: a janela de um ano do primeiro capítulo, levada à escala, erra por 0,2494 no ano seguinte a uma mudança que dobra a oscilação, e erra por apenas 0,0397 num mundo que não muda — a cegueira não se anuncia.
- **2026-09-23.** **No melhor esquecimento, o erro que sobra é ruído.** Medido em vinte mundos sorteados: a memória de mil dias erra por 0,4405 e a de um dia por 0,6067 — as duas pontas são ruins por motivos opostos.
- **2026-09-23.** **A direção existe no dado, e o vigia de um ano mede o ano.** O instrumento passa na conferência: inverter a série troca o sinal do terceiro momento sem trocar o tamanho (índice −0,3485 e +0,3485; Ibovespa −0,3474 e +0,3474; Bitcoin −0,7042 e +0,7042), e em desvios da conta do nulo a direção vale −7,38 no índice, −7,30 no Ibovespa e −12,04 no Bitcoin.
- **2026-09-23.** **A queda conjunta tem direção, e ela é de um ou dois dias.** Medido no par índice e Ibovespa, em 6204 dias comuns: o índice lidera 35 episódios e o Ibovespa 20 na janela de cinco dias, assimetria 0,273 — 2,68 desvios acima do nulo, que tem média −0,014 e dispersão 0,107 em 40 pares sorteados. O controle por adiantamento declarado (deslocando a segunda perna com dependencia.pareado) localiza o intervalo: a assimetria é máxima com um ou dois dias de deslocamento e cai para dentro da faixa do nulo com dez e vinte e um. A estabilidade repete o sinal: os quatro pedaços do par dão 0,143, 0,429, 0,250 e 0,273, todos acima da média do nulo, embora cada pedaço sozinho tenha poucos episódios dirigidos (7 a 10).

- **2026-09-23.** Capítulo 16 escrito: **O que a margem deixa de fora** (terceiro e último pedaço do andar 1). O experimento é controlado pelo segundo momento: uma família de pares em que a correlação é **declarada** e a correlação do corpo é resolvida para que ela continue valendo em todos os mundos, e o que muda é só a forma como os dias ruins chegam juntos (com probabilidade p as duas pernas recebem o mesmo choque, de tamanho f).
- **2026-09-23.** **A correlação fica parada e a conta cresce.** Medido em 8000 dias e 20 sorteios por célula: a correlação vai de 0,4941 a 0,5006 entre os cinco mundos, um vaivém de menos de dois por cento; no mesmo conjunto, os dias em que as duas pernas rompem juntas vão de 5,013 a 9,796 vezes o que a independência previria, e a perda conjunta de uma carteira de peso igual no pior 5% dos dias vai de 0,01795 a 0,02784 — razão de 1,551. Quem dimensiona pela correlação dimensiona o mesmo número para os cinco mundos.
- **2026-09-23.** **A margem cumpre a taxa prometida e paga mais fundo.** A taxa de rompimento do corte é 0,05111 na média dos cinco mundos (0,0508 a 0,0514 por mundo), e o motivo é do próprio instrumento: o corte é um quantil, e quantil entrega a taxa que promete. O que muda é a profundidade média além do corte, de 0,004137 no controle a 0,01428 no mundo de choque grande — três vezes mais, com o mesmo número de dias. A leitura honesta do capítulo: a margem **conta** que a cauda engordou (a curtose dela vai de 2,991 a 19,56, visível numa série só); o que ela não conta é que os dias engordaram **juntos**.
- **2026-09-23.** `mudanca.par_de_cauda` é o mundo do par controlado, com a correlação do corpo resolvida algebricamente para preservar a declarada; o auto_teste ganhou o bloco dele (com p = 0 o par é o gaussiano de sempre, o choque comum não mexe na correlação e engrossa a cauda marginal). O caderno E17 traz as duas figuras e as leituras visuais. Com este capítulo o **andar 1 está completo** (o mundo que faltou, o que foi apagado, o que a margem deixa de fora), e os três pedaços são o mesmo movimento visto de três lugares: o resumo é sempre uma compressão, e o que escapa dela é o que decide. O movimento seguinte é o andar 2, o enquadramento: tempo, memória e individuação.

- **2026-09-23.** Capítulo 17 escrito: **O pedaço escolhido** (primeiro pedaço do andar 2, o enquadramento). Pela primeira vez o livro discute o que atravessou tudo sem ser dito: a **série** — ela tem começo e fim porque alguém escolheu onde ficam. A medição é a do primeiro capítulo (quantos dias rompem o corte de 252), repetida em pedaços de três tamanhos ao longo dos 6718 dias do índice, e o que se reporta não é a resposta: é a lista e a dispersão.

- **2026-09-23.** Capítulo 18 escrito: **O agora** (segundo e último pedaço do andar 2). O atraso do dado entra no corte do primeiro capítulo como um deslocamento: a barreira de hoje é a da janela de 252 dias que terminava `atraso` dias atrás, e com atraso zero isso é exatamente o corte do primeiro capítulo — identidade conferida no `auto_teste` de `promessa.violacoes_atrasadas`.
- **2026-09-23.** **O atraso não cobra dias: cobra a mudança que coube nele.** No índice, um ano de atraso entrega 0,06003 contra a promessa de 0,05138 (razão 1,16819). Num mundo que não muda, a varredura inteira de atrasos move a entrega de 0,05112 a 0,05156 — variação de 0,00043, porque o corte é um quantil e o quantil não sabe que dia é hoje. Na janela de 250 dias depois de uma mudança que dobra, a entrega vai de 0,11235 sem atraso a 0,21116 com um ano de atraso: mudança e atraso se multiplicam.
- **2026-09-23.** **O enquadramento fecha numa imagem: o agora é um retângulo.** No instante da decisão o sistema tem a janela entre t menos atraso menos memória e t menos atraso. A borda direita é o atraso (este capítulo), a esquerda é a memória (medida na travessia e no capítulo do passado apagado) e o próprio eixo — onde a série começa e termina — é o capítulo anterior. As três bordas são declarações do instrumento, e as três foram medidas.
- **2026-09-23.** Quarta vez que o `conferir_rotulos` pega um defeito real (`tab:atraso` já existia no capítulo do orçamento), e a terceira lição de edição da mesma família: âncora de substituição tem de caber numa linha. Fica também a regra de vocabulário: os atrasos do experimento são **parâmetros** e vão por extenso no texto, não por comando gerado. Livro em 18 capítulos, 20 cadernos, 15 módulos e 106 páginas; falta o **fecho**.

- **2026-09-23.** Capítulo 19 escrito: **O fecho — a promessa com os buracos abertos ao mesmo tempo**. Ele fecha a espiral sem repeti-la: a pergunta da raiz (a medida, o corte e o preço de fixar) refeita com tudo o que o livro construiu, e a hipótese do fio condutor (promessa × entrega, em dados, em trabalho e em memória) respondida. O experimento é a pilha, medida em doze configurações com a promessa fixada em 5%: janela de calibração (curta, média, longa), atraso do dado (zero ou 21 dias) e mundo (parado ou com uma mudança que dobra no meio dos 12000 dias), vinte sementes por célula.
- **2026-09-23.** **Os buracos se encaixam em vez de se somar.** A pilha inteira entrega 3,2032 vezes a promessa, contra 2,151 que a soma dos buracos um a um preveria (1 + (1,016-1) + (1,036-1) + (2,100-1), as três barras isoladas): a conta anterior, 2,972, misturava comparações de mundos diferentes e nenhuma soma das barras impressas a alcança: juntar cegueira de janela, atraso e mundo mudado custa mais do que a soma do que cada um custa sozinho, e a diferença mora no produto, não na adição.
- **2026-09-23.** **A janela troca de sinal entre os mundos, e é o achado novo do fecho.** No mundo parado, calibrar numa janela longa melhora a entrega (1,1315 na curta contra 1,0159 na longa); no mudado, ela piora com força (1,6972 contra 3,0039). O mesmo gesto, o mesmo número de dias, sinais opostos — e é a resposta mais direta que o livro dá à pergunta da raiz: não existe janela certa, existe janela declarada. O atraso de 21 dias segue a mesma regra com sinal mais fraco: no parado ele quase não move nada (1,1315 contra 1,1155 na curta, e as duas longas praticamente coincidem), no mudado ele **acrescenta** dano em toda janela (2,4263 contra 2,0996 na média, 3,2032 contra 3,0040 na longa) — o atraso cobra a mudança que coube nele, como o capítulo do agora já havia medido num só mundo.
- **2026-09-23.** **O fio condutor responde por três contas que não se convertem.** O livro perguntou a mesma coisa em dados (a entrega do corte), em trabalho (a partilha do orçamento de atualizações) e em memória (o esquecimento mínimo que ainda aprende), e o que se encontrou foram **conversões locais**, cada uma válida dentro do seu próprio objeto: a lei k/(n+1) dentro do corte, a taxa de atualização dentro do modelo da partilha, o horizonte de recuperação log(1 - t ao quadrado)/(2 log a) dentro do AR(1). Não existe câmbio entre as três — a hipótese se confirma como **pergunta** e cai como **régua única**, e o capítulo declara isso com os três números na mão em vez de forçar a unificação.
- **2026-09-23.** Leitura visual do fecho, gravada no caderno E20: na primeira figura as duas curvas do mundo parado descem quase sobrepostas e as duas do mundo mudado sobem com a tracejada (com atraso) acima da contínua em todo o trecho — mesmo eixo, sentidos opostos, e nada se cruza; na segunda, as três barras dos buracos isolados quase não se levantam do chão, e a barra da pilha inteira fica mais alta do que a soma do que as barras do meio acrescentam sozinhas, que é a forma visual do encaixe. Com este capítulo o livro fecha: **19 capítulos, 21 cadernos, 15 módulos e 110 páginas**, com `--check` limpo e zero avisos. Nada do plano declarado na seção 6 fica por escrever — raiz, voltas 1 a 5, travessia (F1 a F5), andar 1, andar 2 e fecho estão no texto.

- **2026-09-23.** **A régua da antítese estava torta, e a torta inflava capítulo alheio.** O medidor contava a marca por `[EÉeé]`, e o português tem dois caracteres ali: o verbo *é*, sempre acentuado, e a conjunção *e*, que nunca é. Em "e a pergunta volta" ele contava definição por antítese. Medido antes de corrigir, no livro inteiro: **94 contadas, 55 reais, 39 falsas** — 42% de erro —, e o erro não era uniforme, porque caía justamente nos capítulos que encadeiam períodos com a conjunção. O capítulo 2 e o 16 apareciam como os piores do livro, com 9 cada, quando têm 3. Corrigido para `[Éé]`, e fica a lição de método: **portão errado é pior que portão ausente**, porque dá número com cara de evidência — a remeção trocou o ranking inteiro.
- **2026-09-23.** **O capítulo 1 foi reescrito na voz trancada, medido antes e depois.** Era o único capítulo do livro nascido antes de a voz ser decidida, e o único a carregar todas as marcas ao mesmo tempo. Medição de saída: definição por negação **3,3% → 0,0%** (três moldes "não … :", um deles definindo a série por aquilo que ela não é), definição por antítese **6 → 0**, meta-comentário **2 → 0** ("é medido de novo neste capítulo", "a série deste capítulo"), clichê **1 → 0** ("isto é,"). O ritmo se moveu pouco — **18,9 → 19,9 palavras por frase**, com a mediana de 17 para 18 e a largura interquartil de 13 para 14 palavras —, e a medição corrige o diagnóstico que estava registrado: o capítulo **não** tinha ritmo curto e uniforme, tinha 12 frases acima de 30 palavras e uma de 60. O que ele tinha era 4,3% de frases de até cinco palavras, agora 2,3%, e a média puxada para baixo pelo capítulo ser o mais curto e o mais definicional do livro. A conferência da reescrita é o inventário: **36 comandos antes, 36 depois, nenhum perdido e nenhum novo**, com rótulos, citações, figuras, proposição e prova idênticos — e os portões limpos depois, com 110 páginas e zero avisos.

- **2026-09-23.** **O livro estava imprimindo asteriscos.** Quinze capítulos depois de a voz ser trancada, o corpo do texto ainda tinha negrito de markdown: **51 pares em 13 capítulos** de `**assim**`, que o LaTeX imprime literalmente, e o leitor recebia os quatro asteriscos no meio da frase. Nenhum portão via: a compilação sai limpa, não há referência indefinida, não há caixa estourada, o dígito digitado não tem a ver, o comando órfão olha barra perdida e não asterisco. **A conferência que pegou foi ler o texto do PDF publicado** (`pdftotext`), e não o código: 60 linhas com `**` no papel. Consertados os 51, e entrou portão novo — `conferir_marcacao` reprova negrito, crase, título, link e riscado de markdown no corpo (nunca em comentário), e foi provado por teste negativo antes de valer.
- **2026-09-23.** **A régua de voz ainda tinha dois furos, na mesma família do primeiro.** O extrator de prosa despejava o argumento de `\label`, `\cref` e `\cite` dentro do texto medido, de modo que o rótulo `cap:dependencia_vigiada` virava a palavra "cap:" e **inventava uma marca de negação** ("não vê o que não está na série cap:"); eram 236 "palavras" que não são texto, 0,9% do total. E o molde de negação atravessava ponto e vírgula, casando a negação de uma oração com o dois-pontos da seguinte — o molde é intra-oracional. Remeção depois dos dois: o capítulo 6 caiu de 9,2% para 6,2% e o 8 de 8,5% para 6,2%, o 5 e o 11 caíram pela metade, e o capítulo 19 saltou de 2,1% para **8,0%** de frases curtas, porque o negrito grudava a frase num token só. Terceira vez que a régua erra e a terceira vez que o ranking se move: **antes de cortar por causa de uma contagem, conferir a contagem.**
- **2026-09-23.** **Os capítulos 6, 7 e 8 lidos com a régua limpa: é voz, com uma exceção.** Das 13 marcas de negação nos três, 5 não são o molde (o extrator casa a negação com o dois-pontos da oração seguinte) e das 8 reais quase todas definem por contraste onde o contraste é o conteúdo medido — "a mudança não aparece como degrau: aparece como mais dentes na linha" é a observação central do capítulo 8, e "não foi suposto: ele foi medido" é uma afirmação de método. Sobrou uma, no capítulo 6, que era o tique puro, o da negação que antecede o que se quer dizer para adiar a afirmação: "Não é que o conjunto encolha para poucas explicações: ele fica vazio", trocada por "O conjunto fica vazio, e não apenas pequeno." A lição: contagem alta de marca não é prova de defeito, e a leitura é que decide — o que a contagem faz é dizer onde olhar.

- **2026-09-23.** **O livro imprimia "Figure", "Table" e "September".** A auditoria da página impressa — não do código — achou o que faltava: **43 "Figure", 36 "Table"**, a data da folha de rosto escrita **"September 24, 2026"** e um "Table 3.2" no meio de uma frase portuguesa, em 110 páginas, com a compilação limpa e todos os portões satisfeitos. A causa estava declarada num comentário do próprio preâmbulo e é antiga: a distribuição local **não traz os arquivos de idioma do babel** (a compilação com `brazilian` falha, conferido), então uma sessão anterior trocou os nomes à mão — `contentsname`, `chaptername`, `bibname` e `proofname` — e esqueceu os dois mais visíveis, **`figurename` e `tablename`**, que a classe `book` usa para prefixar toda legenda, mais a data e mais os nomes do `cleveref`. Consertado com Figura/Tabela, uma macro de mês em português para a data, e vinte declarações de `crefname`/`Crefname`.
- **2026-09-23.** **O portão dos nomes impede a volta.** Sem babel, qualquer `\cref` novo para um tipo não nomeado **volta a imprimir em inglês, em silêncio** — é exatamente o erro futuro que se quer ver falhar. O portão exige os nomes fixos da classe trocados, proíbe `\today` e exige `crefname` **e** `Crefname` para todo tipo referenciado: as duas formas são declarações separadas e ter só uma deixa a outra em inglês — furo que o **próprio teste negativo do portão revelou**, depois de ele ter passado no caso que eu achava que o testava. Fica a lição sobre teste negativo: um teste que escolhe o caso errado aprova um portão furado, e o jeito de saber é fazer o portão falhar de propósito em cada ramo dele.
- **2026-09-23.** **A bibliografia imprimia o código da notação.** O título de Chen et al. carrega notação matemática — um L com subscrito p,q —, e o gerador de fontes escapava as chaves, de modo que o leitor recebia `L_{p,q}` com chaves e sublinhado no papel. O `tex()` do `lab/fontes.py` passou a respeitar trechos **entre cifrões** (a declaração de que aquilo é matemática), com o cuidado que a regra exige: cifrão ímpar não declara nada, e aí o texto inteiro continua escapado como antes. O título no corpus ficou declarado como matemática. Registro de passagem: o portão do dígito digitado acusou `\number\year` como se fosse um comando gerado, porque o padrão `\num...` casa com a primitiva do TeX — trocado por `\the\year`.

- **2026-09-23.** **O log vazio passou por compilação limpa, e a lição estava no contrato.** A auditoria da diagramação começou com `grep -c Warning` no log de compilação: zero, e "zero" virou conclusão. O log tinha **187 bytes e seis linhas** — o `latexmk` não recompila quando nada mudou, e o silêncio de um arquivo vazio foi lido como ausência de defeito. Pior: a lição **estava no contrato e eu a podei nesta mesma sessão**, ao enxugar o log de decisões ("a conferência de compilação olha o PDF e o código de saída, nunca só a ausência de avisos", com o caso do `grep -c undefined` num log de execução que falhou). **Poda de contrato que descarta lição de método custa exatamente o erro que ela previne**, e custou uma rodada. Com `latexmk -g` forçado, a medição verdadeira: zero overfull, zero aviso de flutuação, 3 linhas frouxas (todas na bibliografia, onde URL longa não quebra) e 67 legendas caindo em sequência dentro dos próprios capítulos — **a estrutura da página está saudável**.
- **2026-09-23.** **`conferir_compilacao` substitui a prosa que eu podei por código.** Ele olha três coisas: o log existe e tem compilação dentro (procura "This is pdfTeX"), o PDF é mais novo que todo fonte do livro, e nenhuma caixa estourou. Os dois primeiros **reprovam** — e o segundo é novo em espécie: até aqui **nada exigia que o PDF estivesse em dia com o que foi escrito**, e por isso um log de uma execução antiga podia ser lido como se fosse o resultado de agora. Caixa estourada reprova por ser defeito impresso; linha frouxa avisa. Os dois ramos de falha foram testados de propósito antes de o portão valer: fonte mais novo que o PDF acusa "recompile antes de conferir", e log sem compilação dentro acusa "o silêncio passou por limpeza". Com ele os três defeitos impressos desta sessão — o negrito de markdown, o "Figure" em inglês e o log vazio — passam a ter portão.

- **2026-09-23.** **A legenda longa era longa por repetição, não por precisão.** Uma outlier em 67: a da `fig:instrumentos`, com **100 palavras e oito linhas**, quatro vezes a mediana. Lida de perto, o defeito não era extensão — ela dizia **duas vezes** que a barra que alcança a linha tracejada significa ficar sem alarme dentro do horizonte, e repetia no meio de si a interpretação que o corpo já faz sete linhas acima ("cada um vê uma forma e tropeça na outra"). Cortadas as duas repetições: **64 palavras e cinco linhas**, mantendo o que só a legenda pode dar (o que a figura mostra, o que a linha tracejada é, o que a barra cheia quer dizer, e a leitura de que duas barras que terminam no mesmo lugar não são empate porque uma delas não chegou). A lição: **legenda longa se conserta cortando repetição, nunca cortando o que a figura precisa que o leitor saiba** — e a leitura é que encontra a repetição, porque a contagem de palavras só diz que a legenda é longa.
- **2026-09-23.** Armadilha de ferramenta: **o `pdftohtml` deixa as imagens raster extraídas ao lado do fonte** (`livro-39_1.png`, `livro-39_2.png`, `livro-39_3.png` na pasta do livro), mesmo com `-stdout`. Elas apareceram como não versionadas e entrariam num `git add -A` despercebidas; o padrão entrou no `.gitignore`. De passagem, a mesma ferramenta revelou que a página 39 carrega **três imagens raster** no meio de um livro de figuras vetoriais — não é defeito (é uma figura de densidade), mas fica registrado porque `pdfimages` é o único jeito de enxergar isso.

- **2026-09-23.** **A auditoria de figuras contra o texto: 67 objetos, 24 com achado, e três erros de conteúdo no livro.** Quatro agentes leram cada figura e tabela contra a legenda e o parágrafo que a comenta, e o que apareceu foi uma família de defeito que **nenhum portão alcança**: comando medido, valor certo, lugar certo — e **a frase sobre ele falsa**. Os três: o capítulo 9 dizia que a resposta do estado escondido "fica entre 1,028 e 1,058 em todas as contenções" quando a própria tabela traz 0,9804 e 0,9853 (seis das nove linhas abaixo do piso); o capítulo 13 imprimia **assimetria na casa dos dias** ("com 0,3396 dias cai para 0,3396", porque os comandos de assimetria foram reusados na posição do dia); e o capítulo 15 imprimia "0,9 (metade)" numa linha cujo caso é **a = 0,5**, de modo que 0,9 aparecia duas vezes na mesma tabela com escalas diferentes. Corrigidos e commitados (`810952f`, `f62c56a`). A lição, agora com três ocorrências: **o portão amarra número a medição, e não afirmação a medição** — a defesa é ler a tabela contra a frase que a comenta, e para isso não há automação barata.
- **2026-09-23.** **As figuras imprimiam português sem acento, e o gerador de nomes apagava a letra acentuada.** 24 das 41 figuras tinham rótulo sem acento ("explicacoes da familia", "razao entre as duas leis", "mundo que nao muda"), contra o §3.6, que manda pt-BR "no corpo, nas provas e **nas figuras**". Consertadas as 41, e no caminho apareceu um defeito antigo do `lab/executar.py`: ao montar o nome do comando LaTeX ele **dividia a chave em qualquer caractere não-ASCII**, de modo que `indice` virava `ndice` e a chave `recorde_indice_conta` saía como `\numRecordeNdiceConta` — nome diferente do que o livro cita, **em silêncio**. Nunca tinha disparado porque nenhuma chave tinha acento; o gerador agora translitera (NFKD) antes de dividir, e a chave acentuada devolve o mesmo nome ASCII de antes.
- **2026-09-23.** **Cinco defeitos de eixo e de figura, corrigidos no código dos cadernos.** O pior: no E19 a figura 1 usava **escala logarítmica com zero dentro** da lista de atrasos — zero não tem lugar em eixo log —, e o resultado impresso era quatro rótulos empilhados numa janela de 12 pt no extremo direito e um "0" solitário a 540 pt de distância, com todo o eixo dos atrasos nos últimos 3% da largura; virou categórico e agora lê `0 1 5 21 63 252` sem sobreposição. Os outros: 13 barras contra 12 no E18, com cada painel no próprio eixo x, de modo que a comparação barra a barra desalinhava; os títulos dos painéis do E17 imprimindo a correlação de **um único sorteio** (0,51 e 0,53) contra a tabela (0,5006) e a tese do capítulo; o eixo y do E18/E19 dizendo "dias que romperam o corte" para o que está plotado, que é **fração**; e a perda do E17 entrando negada para a curva subir, com o eixo dizendo só "perda média".
- **2026-09-23.** **A passada de acentos foi ampla demais, e quebrou o laboratório — o conserto virou regra.** A primeira tentativa acentuou qualquer string numa linha que desenhasse rótulo, e pegou **chaves de dicionário**: o E10 quebrou com `KeyError: 'contenções'` (eu tinha mudado `desenho["contencoes"]`, que estava numa linha de `set_xticklabels`) e **31 nomes de comando** mudaram. A regra que faltava, e que ficou escrita no conserto: **só acentuar a string que nunca aparece como chave, comparação ou índice** — e conferir por re-execução, porque a varredura estática não distingue rótulo de chave quando o mesmo literal serve aos dois. A prova de que nada se perdeu: as **782 grandezas** têm os mesmos nomes e os mesmos valores de antes (conferido ordenando os dois `numeros.tex`), e a recompilação sai em 110 páginas com zero overfull. Registro também o que a rodada mostrou sobre declarar: o §12 afirmava que E15 a E18 "trazem as leituras visuais", e **oito cadernos tinham a célula no marcador literal** — passo de protocolo que se registra como feito precisa de conferência mecânica, porque quem escreve o log é quem acha que fez.

- **2026-09-23.** **Os asteriscos que sobraram não estavam no livro.** A denúncia de asteriscos duplos na seção 16.4 levou a uma varredura de tudo: **zero** no fonte dos capítulos, **zero** nos gerados e **zero** no PDF publicado — o `conferir_marcacao` cobre os três desde a correção dos 51 pares, e o único asterisco impresso em 110 páginas é o do título do Pearl na bibliografia, que é do original. O que existe na árvore e **não** é markdown: `.old/docs/dinamica_incerteza.pdf` tem 156 linhas com `**` e são **código Python citado** (`x ** 2`, `s**2`), idem os 32 do `kfrevo_empirico.pdf`; e `.old/**/*.md` carrega centenas de pares, que é o projeto anterior — pedreira, não roteiro. A lição de método: **antes de consertar, provar que o defeito existe no artefato**; a varredura levou o tempo que levou porque eu procurei em três camadas antes de concluir, e concluir sem procurar teria "consertado" um texto correto.
- **2026-09-23.** **A correção de figura desatualiza a leitura que a descrevia.** As correções de eixo desta sessão mudaram figuras **depois** de as leituras visuais terem sido escritas, e duas passaram a descrever figura inexistente: a do E19 dizia "o eixo horizontal é logarítmico" (o eixo virou categórico) e a do E17 dizia que os painéis traziam "a correlação medida" (os números saíram dos títulos). Corrigidas as duas. Fica a regra: **a leitura visual é registro de uma figura datada** — mexeu na figura, a leitura entra na fila junto, e o portão de frescor não vê isso porque ele olha o hash do **código**, não a correspondência entre a figura e o que se escreveu sobre ela.
- **2026-09-23.** **A observação visual finalmente entrou num capítulo.** Medi as nove leituras contra os capítulos por palavra-chave e três frases não tinham nenhuma no texto — o §9 pede que a observação entre no capítulo e ninguém estava cumprindo. A mais concreta virou parágrafo no capítulo 13: os seis pontos medidos estão **igualmente espaçados no desenho** embora vão de zero a vinte e um dias, de modo que o pico cai num trecho em que cada passo vale um dia e o último trecho vale onze com a mesma largura — quem lê a inclinação entre os dois pontos da direita lê onze dias como se fossem um. Entrou como leitura, não como número, e o estilo do capítulo segue intacto.

- **2026-09-24.** **A frase consertada ainda estava falsa, e por um motivo de método.** O capítulo 10 dizia "7,106% menos perda" onde o caderno media 7,106% MAIS perda: a grandeza se chamava `partilha_ganho_sobra_pct` e era calculada ao contrário, de modo que **o nome mentia e a frase obedeceu ao nome**. Ao reescrever, a conferência de dispersão mostrou coisa pior — a sobra tem desvio de 8,224e-05 entre mundos contra uma diferença de 2,82e-05, e a afirmação nova cabia dentro do ruído. Como os dois desenhos são medidos nos **mesmos** vinte mundos, a comparação honesta é par a par: a diferença tem desvio de 5,052e-05, ainda maior que a média dela, e o orçamento apertado entrega mais perda em catorze mundos e menos em seis. A lição: **consertar uma frase falsa com a leitura que ela pedia pode produzir outra frase falsa** — média de diferença pareada não herda a força que a diferença aparenta, e quem mede duas políticas nos mesmos mundos não compara dispersões marginais.
- **2026-09-24.** **A vírgula em modo matemático imprime com espaço depois.** A frase corrigida saiu no PDF como "8, 224": dentro de `\ensuremath` a vírgula é pontuação do TeX e ganha espaço. A armadilha **já estava documentada no próprio `lab/executar.py`**, num comentário sobre o `\pm` — que por isso foi posto fora do modo matemático —, e o ramo da notação científica, escrito depois, caiu nela. A vírgula passou a sair entre chaves (`8{,}224`) e entrou o `conferir_matematica` no gerador, reprovando vírgula decimal solta em matemática; testado nos dois ramos e conferido contra falso positivo em número de texto. **Documentar a armadilha num ramo do código não protege o ramo seguinte** — o que protege é o portão.

- **2026-09-24.** **O aforismo do devir entra no contrato como coincidência, não no livro.** "O ser é o atrito dissipativo de um Real contraditório e termodinâmico: a razão resfria o fluxo ao recortar e fixar suas formas, enquanto a arte o reaquece ao fraturar e transfigurar esses limites: uma dança perpétua suspensa sobre o abismo indeterminado do devir" — o aforismo do autor coincide, por outro caminho, com o que o livro mede desde a raiz: o corte fixa uma forma e cobra o preço de deixar o que muda de fora, e o que escapa da forma é o que decide. A mesma coisa, medida, está no capítulo 16 ("o resumo é sempre uma compressão, e o que escapa dela é o que decide") e, no projeto anterior, na frase "a barreira marginal subprotege". Fica aqui, não no livro, porque a voz do livro é didática para dezesseis anos e o §3 tranca o vocabulário; a coincidência fica declarada como manda o §10.

- **2026-09-24.** **Duas contabilidades honestas do mesmo fatorial dão sinais opostos.** A seção "os buracos se compõem" do fecho mede se os três buracos (janela longa, atraso, mundo mudado) custam mais juntos do que a soma do que cada um custa sozinho. A resposta depende de onde se ancora a soma: somando os incrementos de cada buraco sobre a promessa, a pilha fica 49% acima (3,203 contra 2,151), e a seção está certa; na decomposição fatorial clássica, com efeitos principais medidos em torno da média geral do desenho, a célula dos três juntos fica ABAIXO da previsão aditiva em 0,374. As duas contas são verdadeiras e respondem a perguntas diferentes — a primeira pergunta se juntar os buracos custa mais do que a soma do que cada um custa sozinho, a segunda se os efeitos são independentes no desenho inteiro. **O que o livro não pode é imprimir o número de uma e a frase da outra**, que era o caso: 2,972 não é soma de barra nenhuma da figura, e agora o capítulo declara qual conta faz.
