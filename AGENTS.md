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
- **2026-09-23.** Passo visual declarado como protocolo: figura em `.pdf` para o livro e `.png` para inspeção; a leitura visual entra no caderno como observação, nunca como número. Sessão sem entrada de imagem declara a falta em vez de inventar a leitura — é o caso desta sessão, cujo modelo não aceita imagem.
- **2026-09-23.** `lab/executar.py` executa por hash da fonte das células de código, exige resultado gravado por caderno, amarra número e figura ao livro e confere as quatro partes das perguntas do contrato.
- **2026-09-23.** **A biblioteca é artefato**: `lib/frevolab/` guarda todo algoritmo, com teste de propriedade (`auto_teste()`) e versão. O caderno deixa de implementar conta — ele chama a biblioteca e cuida do gráfico. A justificativa é testabilidade e reuso: algoritmo dentro de caderno não tem nem uma nem outra.
- **2026-09-23.** O portão `lab/executar.py --check` passou a rodar o `auto_teste()` da biblioteca antes de tudo: se o algoritmo quebra, nada abaixo dele merece confiança.
- **2026-09-23.** **Empacotamento**: `lib/frevolab` virou pacote instalado em modo editável (`uv pip install -e .`), com o mapa em `[tool.hatch.build.targets.wheel]` e `[build-system]` hatchling. Verificado aqui: o wheel constrói, instala, importa de fora do repositório e desinstalar devolve o venv ao estado anterior. Mantém-se o diretório `lib/` em vez do layout `src/` convencional.
- **2026-09-23.** **Quatro regras da biblioteca**, vindas da pesquisa de modularização: versão com fonte única (o pyproject), `rng` por parâmetro (SPEC 7 do ecossistema científico), `__all__` explícito por módulo, e módulo batizado por família de pergunta — nunca por tipo de código.
- **2026-09-23.** O agente que escreve este livro tem nome: **Capiba**, gravado na seção 1. O nome não muda o que o contrato exige — muda o que ele endereça.
- **2026-09-23.** Capítulo 1 escrito: **A medida, o corte e o preço**. O fracasso que o abre, medido: a linha posta no décimo terceiro pior dia dos últimos 252 pregões entrega 5,135% contra os 5% anunciados, e essa média **não distingue o mercado de um mundo que nunca muda**. O que o capítulo fixa como instrumento: declarar o corte, ler em bloco, varrer o corte.
- **2026-09-23.** Os capítulos moram em **`livro/capitulos/`**, um arquivo por capítulo, nomeado pelo conceito. Consequência obrigatória: `lab/executar.py` e `lab/fontes.py` passaram a varrer `livro/` **recursivamente** — com número, figura e citação um nível abaixo, o glob de primeiro nível pararia de conferir sem avisar.
- **2026-09-23.** O portão do dígito digitado distingue símbolo de grandeza: ignora argumento opcional, comando que nomeia arquivo (inclusive a chave de citação, que carrega o ano) e o corpo do modo matemático — mas segue cobrando o **decimal com vírgula** dentro da matemática, que é a forma de escrever grandeza medida aqui. Exceção legítima se declara na própria linha, com `numeros-ok`.
- **2026-09-23.** `frevolab.promessa` é o módulo da família promessa × entrega: posto, corte, violações, entrega do corte, blocos e episódios. O defeito que ele torna impossível: os **dias de graça** — os primeiros `janela` dias, em que o corte não existe e a comparação com `NaN` devolve `False`, afundando a taxa sem avisar.
- **2026-09-23.** Grandeza com erro sai do gerador em modo texto, com o `\pm` em matemática própria: dentro de um `$...$` maior o valor vira "5, 139 ± 0, 1091" no papel, que não é como se escreve número em português.
- **2026-09-23.** Capítulo 2 escrito: **O orçamento do alarme**. O fracasso que o abre, medido: o vigia do capítulo 1, ligado no limiar 13, soa uma vez a cada 3.632 anos de mundo parado e avisa do tombo de 2020 com 86% do prejuízo já pago. A troca é medida (baixar o limiar para 8 antecipa para 36% e paga com um falso alarme a cada 4 anos) e o atraso tem piso provado (um alarme que exige L violações não soa antes de L pregões). O que o capítulo fixa: **todo alarme é o par declarado** (frequência em mundo parado, atraso em mundo que muda).
- **2026-09-23.** `frevolab.vigia` é o módulo da família do orçamento: alarmes, piso de atraso, teto independente, orçamento e prejuízo pago. O teto da `prop:teto` é provado e declarado frouxo (`5,879%` de teto contra `0,6%` medido); para limiares baixos a união passa de cem por cento e deixa de dizer qualquer coisa.
- **2026-09-23.** O gerador de números **recusa chave com dígito**, e o motivo é do TeX: ele encerra o nome de um controle no primeiro caractere que não é letra, então `troca_t8_anos` virava `\numTrocaT` seguido do texto "8Anos" e o livro **deixava de compilar**. Número em chave vai por extenso (`troca_oito_anos`). O defeito custou um PDF inexistente para ser descoberto.
- **2026-09-23.** A conferência de compilação olha o **PDF e o código de saída**, nunca só a ausência de avisos: `grep -c undefined` num log de uma execução que falhou devolve zero, e zero ali não é prova de nada.
- **2026-09-23.** O portão do dígito digitado aprendeu mais duas faxinas: rótulo e referência (`\label`, `\cref`) nomeiam objeto, e a chave de citação carrega o ano — nenhum dos dois é número digitado.
- **2026-09-23.** **Voz do livro reescrita.** O capítulo 1 foi reescrito, e o 2 já nasceu assim, numa voz sem os tiques
  da primeira versão — medidos antes de corrigidos: a definição por negação ("não … : …", que aparecia uma vez a cada
  dezenove frases do capítulo 1), o epigrama em itálico fechando seção, o meta-comentário sobre o próprio livro e o
  ritmo curto e uniforme. No lugar entram ritmo alternado, caso concreto e data. É decisão de estilo, não de conteúdo:
  nenhum número, prova, rótulo ou fonte mudou, e a reescrita saiu com os mesmos comandos de `numeros.tex` e as
  mesmas figuras.
- **2026-09-23.** **O capítulo 2 é uma fusão.** Duas sessões escreveram o capítulo ao mesmo tempo nesta árvore, com
  desenhos diferentes, e o que ficou é um capítulo só, com as duas leituras do mesmo corte: **contar** as violações em
  blocos e alarmar no limiar (orçamento sem forma fechada, medido com erro de contagem e limitado por cima pela
  `prop:teto`) e **aprofundar** o corte e alarmar quando o próprio dia fica abaixo do posto (orçamento exato,
  `k/(n+1)`). Medido: a segunda leitura entrega o que declara (25,66 alarmes contra 25,56 declarados nos mundos
  parados) e, no mesmo silêncio, paga quase o mesmo que a primeira (35,46% contra 36,02% do prejuízo já pago no tombo
  recente, com um alarme a cada cinco anos de um lado e a cada 4,145 anos do outro).
- **2026-09-23.** **O orçamento se compra com memória.** O posto mais fundo é o primeiro da fila, de modo que com
  `n` dias de janela o alarme mais raro que existe é `1/(n+1)`: um alarme por ano custa 252 dias, um por década custa
  2520. Pedir um orçamento mais fino do que a memória compra levanta erro declarado, em vez de entregar um alarme mais
  frequente do que o prometido.
- **2026-09-23.** **A forma da mudança decide o preço.** Com o mesmo orçamento de um alarme por ano, o vigia vê um
  degrau na cauda em 7 dias, uma rampa em 69 e uma deriva na média em 149,5; com um orçamento falador (11,45 alarmes
  por ano) as três chegam quase juntas, em 3, 12 e 12,5 dias. A curva da troca do capítulo 2 foi desenhada com tombos,
  que são degraus: para uma deriva, ela estaria deslocada para a direita.
- **2026-09-23.** `frevolab.mudanca` é o banco de provas das formas da mudança — estável, degrau, rampa e deriva —,
  cada uma com o `rng` por parâmetro e conferida pelo `auto_teste()` contra a escala que declara. O módulo
  `orcamento.py` chegou a existir por minutos e foi absorvido por `vigia.py`: dois donos do mesmo conceito divergem em
  silêncio.
- **2026-09-23.** **O laboratório roda com o python do venv.** `.venv/bin/python lab/executar.py` — com o python do
  sistema o kernel não encontra `frevolab` e o caderno quebra com `ModuleNotFoundError`, defeito que custou uma
  execução perdida para ser descoberto.

- **2026-09-23.** **Rótulo repetido virou portão**, e não aviso de log. Duas figuras de formas no mesmo capítulo
  dividiram `fig:formas`: o `\cref` passou a apontar para a última, o log escreveu "multiply defined", o PDF saiu
  e o `--check` continuou limpo. `conferir_rotulos` varre o livro e falha; foi conferido contra o defeito, forjando o
  rótulo repetido de propósito e restaurando depois.

- **2026-09-23.** Capítulo 3 escrito: **O dia da semana**. O fracasso que o abre, medido: levado à carga elétrica
  diária da Dinamarca no mesmo orçamento de um alarme por ano, o vigia do capítulo 2 dispara 21 vezes — 4,2 por ano
  contra o 1 declarado — e **todos** os alarmes caem em fim de semana (oito sábados, treze domingos, nenhuma sexta).
  O princípio: o calendário é uma partição declarada dos dias em células, e o corte se ergue dentro da célula; com uma
  célula só a leitura É o vigia do capítulo anterior, alarme por alarme. O preço é aritmético: $C$ células dividem a
  memória por $C$ e o orçamento mais fino passa de $1/(n+1)$ para $C/(n+C)$ — medido, de 4,2 alarmes por ano para 13,6
  (semana), 42,0 (semana × estação) e 80,4 (semana × mês). O controle: no índice americano, onde o perfil semanal vale
  0,04216 desvios contra 1,472 da carga, a mesma partição só custa (de 1,24 para 5,10 alarmes por ano).
- **2026-09-23.** `frevolab.calendario` é o módulo da forma que o relógio desenha: as partições (dia da semana, dia ×
  estação, dia × mês), o perfil, a amplitude em desvios-padrão, o orçamento por célula e o vigia por célula. O teste
  de propriedade que o ancora é uma identidade: com `calendario.unica` o vigia por célula devolve exatamente o vigia do
  capítulo 2, alarme por alarme. O defeito que o módulo torna impossível é comparar um domingo com sábados e segundas.
- **2026-09-23.** O dado da carga diária (`opsd_carga_diaria.csv`, cinco praças europeias, 2015–2019) entrou no
  laboratório como sistema: era dado que estava no repositório desde o recomeço e nunca havia sido medido.
- **2026-09-23.** Piso declarado e medição divergem nos dois sentidos, e o capítulo 3 declara isso em vez de esconder:
  a medição fica **acima** do piso quando a célula ainda tem estrutura dentro (domingos de janeiro contra domingos de
  julho, 42,0 contra 36,5) e **abaixo** quando os dias da célula se parecem demais entre si (o inverno puxa o inverno,
  os alarmes se agrupam, e a janela de mil dias fica em zero contra o piso de 2,54).
- **2026-09-23.** **O laboratório exporta o que o livro cita.** Os cadernos `E03_formas` e `E04_calendario` passaram
  a filtrar o dicionário de resultados por uma lista explícita de chaves citadas: medida que o livro não usa é medida
  morta, e os 22 avisos de 'medido e não citado' viraram zero (154 grandezas exportadas contra 172). Parâmetro de
  experimento — número de casos, limiar, país, duração — não é medição e não sai do caderno.
- **2026-09-23.** **Comando órfão virou portão.** Montar LaTeX num idioma que interpreta `\n` come a barra de
  `\num...` e deixa o nome do comando impresso no papel: o PDF sai, o log fica limpo, a compilação passa e o `--check`
  também — o defeito apareceu três vezes nesta árvore, a última deixando `umCalendarioSemanaDiasPorCelula{}` no meio de
  uma frase impressa. `conferir_comandos_orfaos` procura nome com maiúscula no meio, seguido de chaves e sem barra
  antes, e falha; conferido contra o defeito forjado de propósito.
- **2026-09-23.** **A humanização entrou no contrato como passo do ciclo**, e não como gosto: a seção 9 ganhou o
  protocolo — medir a marca antes de cortar, e a ferramenta automática é cega ao português (`humanize_scan` devolve
  `aiScore 0` porque o catálogo é de padrões em inglês e chinês) — e a seção 11 ganhou o passo 5, entre fechar o arco e
  conferir. A decisão de voz já estava registrada; o que faltava era o lugar no ciclo e o que medir antes de cortar.
  Corrigido de passagem: a seção 9 dizia "dois" portões e listava três.
- **2026-09-23.** **O catálogo português de clichês entrou no medidor**, e não no plugin do ambiente: `lab/estilo.py`
  passou a contar também as sete classes de clichê que a ferramenta automática usa, escritas em português. O lugar é o
  repositório por dois motivos — o plugin vive fora dele e morreria no próximo `pnpm install`, e o contrato diz que os
  artefatos são quatro. A primeira rodada sobre os quatro capítulos deu **uma** ocorrência ("isto é," definindo a
  promessa, no capítulo 1) e dois falsos positivos, os dois cortados no ajuste: *alavanca* é a física que o capítulo 2
  usa no sentido próprio, não o jargão *alavancar*, e *vale dizer* é português legítimo quando é ganho, ao contrário
  do molde *vale notar*. Clichê e marca são coisas diferentes: um texto pode não ter clichê nenhum e ainda assim soar
  de máquina — foi o caso do capítulo 1, cujo problema era estrutura, não palavra gasta.
- **2026-09-23.** **A volta 4 medida por eliminação (A4).** Três mercados — S&P 500, Ibovespa e Bitcoin — submetidos à mesma
  família de explicações do capítulo 6 (duas leis, com persistência e com duração de episódio heterogênea), exigindo as quatro
  estatísticas. O resultado separa o que concorda do que discorda: as **marginais concordam** (taxa 0,0513, 0,0509 e 0,0520;
  mediana dos blocos 2, 2 e 3) e o **agrupamento discorda**. A interseção das explicações que sobrevivem é vazia nas duas
  grades (0 de 125 e 0 de 280), com a lei compartilhada e a escala de cada mercado própria; o gargalo é o pior bloco,
  satisfeito pelos três simultaneamente em 3 triplos de 280; Ibovespa e Bitcoin concordam em torno de permanência de 25 dias
  (45% e 30% de acerto, replicados em quarenta sementes por célula) e o S&P fica em 8% — e enriquecer a duração dos
  episódios **piora** em vez de melhorar (0 a 5%). Resposta provisória: ver mundos **não** basta para identificar mecanismo
  comum. Porta declarada aberta, e é o único caminho que mantém o refutador de A4 vivo: uma família mais rica — memória
  longa além de troca de regimes, parâmetros que variam no tempo — ainda não foi testada.
- **2026-09-23.** **Sem replicação, uma semente não é uma medição.** A varredura da família heterogênea foi feita primeiro
  com uma semente por configuração, e a mesma configuração deu pior bloco de 15 a 19 em cinco sementes — variação maior que
  qualquer diferença entre configurações. O veredito de hoje só existe porque a conta foi refeita com quarenta sementes por
  célula, reportando mediana e dispersão. É o mesmo tratamento que os mundos que nunca mudam receberam nos capítulos 1 e 2, e
  a regra vale para tudo o que vier: **toda medição sobre mundos sorteados reporta dispersão, ou não reporta nada**.
- **2026-09-23.** **A recusa de chave com dígito passou a olhar o nome gerado, e não o primeiro caractere de cada pedaço.** As chaves do `E09`
  começavam com `f1_`, e a guarda aprovava porque cada pedaço começa com letra — mas o nome gerado era `\numF1Dias`, e o TeX lê isso como
  `\numF` seguido do texto `1Dias`. O livro deixou de compilar, e o defeito só apareceu porque o commit foi feito **antes** da conferência: a
  ordem certa é compilar e só depois commitar, e esta é a segunda vez que a inversão custou um commit quebrado. A guarda agora monta o nome e
  exige que ele seja só letras.
- **2026-09-23.** O teste de **propriedade** (hypothesis) fica adiado até existir a primeira função que sorteia: dependência nova se justifica com uso, não com antecipação. O `auto_teste()` continua como porteiro barato dentro do `--check`.
- **2026-09-23.** Capítulo 9 escrito: **O desenho da intervenção**. Ele fecha a porta que o capítulo dos mundos
  declarou aberta: acumular mundo observado não escolheu entre as duas explicações, e a saída é mexer no mundo de
  propósito. O fracasso que o abre, medido: segurar o mundo por muito tempo e olhar duas vezes separa as explicações
  em 32,5% das repetições — decisão no sorteio —, e o empate que obriga a esse experimento é apertado exatamente onde
  sempre foi, no pior bloco (−2 contra a tolerância de 2). O princípio mínimo é um ato só, a **contenção**, com a
  resposta medida contra o próprio mundo e uma proposição que dá a forma da curva: sob contenção a variância cai
  geometricamente para o piso ω/(1−β), de modo que **segurar mais fundo tem limite** e cada dia a mais compra menos
  ferida. Medido: a resposta do mundo em que a memória mora na série desce de 0,9803 a 0,6157, a do mundo de estado
  escondido fica entre 1,028 e 1,058, e a diferença medida cresce até 0,4126.
- **2026-09-23.** **O preço de um desenho é medido, não calculado.** A conta do tamanho da amostra
  (n = (z s / d) ao quadrado, com s a soma dos dois desvios entre replicatas) diz onde procurar e erra o preço:
  prometendo 95% de confiança, o desenho apertado separou em 45% das repetições do experimento inteiro, o dobro das
  replicatas chegou a 80% e o quádruplo a 100%, de modo que o desenho que entrega a confiança declarada custa 31
  replicatas de 80 dias — 3100 dias de experimento, perto de quatro vezes o preço da conta. A causa é a cauda gorda
  da resposta: o estado escondido às vezes atravessa a janela inteira, e a média de poucas replicatas não se comporta
  como a média de muitos sorteios pequenos. O controle fecha o capítulo: o mesmo orçamento gasto na contenção de dois
  dias separa em 0% das repetições, porque aos dois dias a diferença medida é 0,04394 — **comprar replicatas para
  enxergar o que a contenção não produz é comprar um erro de leitura**. Fica também o limite duro: uma intervenção
  dessas existe para um sistema que se pode segurar, e para um índice de mercado ela não existe.
- **2026-09-23.** `frevolab.intervencao` é o módulo da travessia do desenho: os dois mundos (a memória na própria
  série, por GARCH; o estado escondido, pela família persistente do capítulo das explicações equivalentes), a
  contenção, a resposta, a replicata, a conta de replicatas com o veredito de viabilidade, o custo em dias, a
  varredura de contenções e a função que mede a promessa do desenho repetindo o experimento inteiro. O defeito que
  ela torna impossível: dizer que precisamos de mais dados sem dizer quantos, e desenhar um experimento caro que não
  separa nada. O caderno E10 traz as duas figuras e as leituras visuais. Corrigido de passagem: as duas tabelas que
  estouravam a margem (a do capítulo 8 e a do capítulo 9) entraram em corpo menor, e o livro compila agora sem
  nenhuma caixa estourada.
