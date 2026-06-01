# paper_figures_regeneradas

Figuras regeradas para o artigo: **Figura 1** (forest plot do fator beta) e
**Figura 2** (slope chart iterativo vs. recursivo nos problemas de DP).
Ambas em plotnine, lendo do JSON canonico, largura 6 in (insercao 1:1), sem nada inventado.

## Arquivos
- `make_fig1_plotnine.py` — gerador da Figura 1 em **plotnine** (ggplot2). Le os
  beta/IC do JSON canonico `../../results/realworld_summary.json`
  (nenhum valor hardcoded; nada alterado nos dados).
- `make_fig1.py` — versao alternativa em matplotlib (mantida como fallback; nao e a usada).
- `make_fig2_plotnine.py` — gerador da Figura 2 (slope chart DP) em plotnine. Mesma fonte.
- `make_fig3_plotnine.py` — gerador da Figura 3 (barras de TLE injusto, CSES) em plotnine.
- `fig1_forest_beta.{png,pdf}` — Figura 1. PDF vetorial 6,0 x 5,6 in.
- `fig2_dp_iter_vs_rec.{png,pdf}` — Figura 2. PDF vetorial 6,0 x 4,6 in.
- `fig3_tle_injusto.{png,pdf}` — Figura 3. PDF vetorial 6,0 x 5,0 in.
  PNG ~600 dpi; PDF para insercao 1:1 em coluna SBC (`width=\linewidth`, sem reescalar).

Regenerar: `python3 make_fig1_plotnine.py`, `make_fig2_plotnine.py`, `make_fig3_plotnine.py`
(precisa de plotnine + pandas no venv).

## O que e o beta (fator de calibracao)
Mede **quantas vezes o Python e mais lento que o C++** no mesmo problema, rodando o
**mesmo algoritmo** nas duas linguagens, no mesmo ambiente:

    beta = mediana(tempo Python) / mediana(tempo C++)

- Calculado no **maior caso de teste** (onde o TLE se decide).
- Mediana (robusta a ruido); incerteza = **IC95% por bootstrap** (10000 reamostragens, seed 42).
- Compilacao e startup ficam **fora** da medicao.

Uso (juiz adaptativo): `limite_Python = beta x limite_base`; `limite_C++ = limite_base`
(o C++ e a regua, beta_cpp = 1). O modelo iguala "para cima": da folga ao Python igual a
desvantagem real medida, nunca aperta o C++.

Achado central (QP1/QP3): beta **nao e constante por linguagem** — varia com a NATUREZA do
problema (de ~3 em memory-bound a ~120 em laco numerico denso). Por isso os multiplicadores
fixos 2x-3x sao inadequados.

## Como ler a Figura 1 (mapeamento visual)
- **Posicao horizontal (eixo X, log)** = valor do beta. Mais a direita = beta maior.
- **Distancia ate as linhas tracejadas (2x / 3x)** = o quanto o beta real supera o
  multiplicador fixo (evidencia visual da QP1).
- **Ordem vertical** = estimativas ordenadas por beta (menor embaixo).
- **Cor** = categoria (grafos / DP / backtracking / recursao). NAO depende do beta.
- **Linha fina horizontal** = IC95% (incerteza do beta). Onde o IC e muito estreito
  (<~6% de beta) a barra fica menor que a bolinha e some sob ela (nao e dado faltante).

Decisao de design (banca-proof): o forest plot e padrao e bem estabelecido. Optou-se por
NAO codificar visualmente "beta operacional vs nao-operacional" (escuro/claro) para manter a
figura limpa; essa informacao vai no caption/texto (abaixo).

## Contagem (reconciliar no texto)
**11 problemas no estudo / 10 plotados / 13 estimativas.** Chessboard and Queens (1624) e
controle (entrada fixa, sem beta calibravel) -> omitido. Os 3 problemas de DP entram com
2 estilos (iterativo e recursivo), cada um com seu beta -> 13 estimativas em 10 problemas.

## Caption sugerido (PT)
> Figura 1. Fator de calibracao beta = mediana(Python)/mediana(C++) por estimativa, com
> IC95% (bootstrap), em escala logaritmica. Sao 13 estimativas em 10 problemas: dos 11 do
> estudo, Chessboard and Queens (controle, entrada fixa) nao tem beta calibravel e foi
> omitido; os 3 problemas de programacao dinamica aparecem com dois estilos corretos
> (iterativo e recursivo), cada um com seu beta. Nos problemas de DP, o limite efetivamente
> aplicado usa o MAIOR beta entre os estilos, para resgatar ate o estilo correto mais lento.
> As linhas tracejadas marcam os multiplicadores fixos 2x e 3x. Em estimativas com IC95%
> muito estreito (<~6% de beta, p. ex. Grid Paths/1638 iter, Shortest Routes II e Grid
> Paths/1625), a barra e menor que o marcador e fica oculta sob ele - ausencia de barra
> indica intervalo apertado, nao dado faltante.

---

# Figura 2 - slope chart: beta iterativo vs. recursivo (DP)

## O que mostra
Para cada um dos 3 problemas de DP, o beta do estilo ITERATIVO (esquerda) ligado ao beta do
estilo RECURSIVO (direita). Cada problema = uma serie distinta por cor + marcador (linhas
todas solidas, por preferencia da usuaria; distincao P&B via marcador): Coin Combinations I
(azul, circulo); Grid Paths/1638 (verde, quadrado); Two Sets II (laranja, triangulo).
Barras = IC95% bootstrap.
Eixo Y LINEAR (faixa 11-68 justifica; mantem a queda do Two Sets II visivel).

betas (iter -> rec): Coin 11,1 -> 34,8 | Grid 12,0 -> 23,5 | Two Sets II 68,3 -> 43,3.

## Leitura (achado)
O estilo de implementacao altera beta de forma PROBLEMA-DEPENDENTE: em Coin e Grid o recursivo
sobe o beta; no Two Sets II ele DESCE (inversao). No Two Sets II os IC95% de iter e rec NAO se
sobrepoem (rec ate 47,9; iter a partir de 64,9) -> a inversao e real, nao ruido. Reforca que
beta deve ser calibrado por problema E por estilo. Sao 3 problemas com 3 comportamentos, NAO
uma tendencia geral (n=3).

## Por que so 3 problemas
So o DP tem dois estilos corretos comparaveis (iterativo e recursivo). Grafos, backtracking e
recursao tem um unico estilo de solucao -> nao ha par iter/rec a comparar.

## Caption sugerido (PT)
> Figura 2. Fator de calibracao beta por estilo de solucao (iterativo vs. recursivo) nos tres
> problemas de programacao dinamica; barras indicam IC95% (bootstrap). Apenas o DP aparece
> porque grafos, backtracking e recursao tem estilo unico, sem par iter/rec a comparar. Os
> tres problemas exibem tres comportamentos distintos - em Coin Combinations I e Grid Paths o
> estilo recursivo aumenta beta, enquanto em Two Sets II o reduz (inversao; os IC95% de
> iterativo e recursivo nao se sobrepoem) -, e nao uma tendencia geral, dado n=3. O estilo de
> implementacao altera beta de forma problema-dependente, podendo ate inverter o sentido, o
> que reforca a necessidade de calibrar beta por problema e por estilo.

---

# Figura 3 - TLE injusto da solucao Python correta, por problema (CSES)

## O que mostra
Barras horizontais: fracao de casos de teste em que a solucao Python optimal (correta) recebeu
TLE no JUIZ OFICIAL CSES, sob o limite tradicional de 1,0s, por problema. Cor = categoria.
Ordenado por fracao (maior em cima). Rotulo = numerador/denominador (casos TLE / total de casos
oficiais do problema no CSES). A fracao mede a PERVASIVIDADE do TLE (em quantos casos aparece);
o veredito de submissao e binario (1 caso TLE ja reprova).

## Definicoes (declaradas)
- **Fonte do veredito = CSES** (juiz oficial), NAO o pipeline local (que e hardware-dependente).
- **TLE injusto** = o C++ optimal foi ACEITO e o Python optimal EQUIVALENTE recebeu TLE no CSES
  sob 1,0s (mesma solucao, so muda a linguagem).
- **Denominador** = total de casos de teste oficiais do problema no CSES.
- **DP (2 estilos)**: a barra usa o estilo do **beta operacional** (o de maior beta, o que define
  o limite aplicado), anotado no rotulo ([rec] ou [iter]). Criterio aplicado a todos os DP.
- **Eixo X**: 0 a 0,66 (maior barra ~0,56; reduz o vazio a direita). Grid vertical mantido.

## Controle (anti-cherry-picking)
Chessboard and Queens (1624) = 0/10, marcado "(controle)": entrada fixa 8x8 (nao escala), C++ e
Python ambos aceitos. Confirma que a injustica depende da NATUREZA do problema, nao e artefato do
metodo (nem todo problema penaliza o Python).

## Caption sugerido (PT)
> Figura 3. Fracao de casos de teste em que a solucao Python correta recebeu TLE injusto no juiz
> oficial CSES, sob o limite tradicional de 1,0s, por problema (TLE injusto = C++ optimal aceito e
> Python optimal equivalente rejeitado; denominador = total de casos oficiais do problema no CSES).
> Nos tres problemas de programacao dinamica a barra corresponde ao estilo de maior beta (o
> operacional, que define o limite aplicado), indicado por [iter]/[rec]. Chessboard and Queens
> (controle, entrada fixa 8x8) tem 0/10 e confirma que a penalizacao depende da natureza do
> problema, nao do metodo. As fracoes provem do veredito do CSES; o pipeline local, por ser
> hardware-dependente, nao e a fonte desta figura.
