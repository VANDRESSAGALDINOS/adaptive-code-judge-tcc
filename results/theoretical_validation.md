# Validacao do eixo TEORICO (classes de complexidade)

Registro de validacao do eixo teorico, par do `realworld_validation.md`. Cobre as 6 classes
de complexidade sinteticas (S3.4.1). Fonte de verdade dos numeros: `theoretical_summary.json`
(gerado por `experiments/aggregate_results.py` a partir dos
`experiments/complexity_analysis/<classe>/results/{calibration.json, selectivity.json}`).
Nada aqui e inventado; tudo vem desses JSONs.

## Escopo e diferenca para o eixo real-world
- Sao 6 problemas CONTROLADOS/sinteticos (nao CSES). A REGRA #0 (o CSES decide a injustica) NAO
  se aplica aqui - quem decide injustica e o eixo real-world. O eixo teorico valida:
  (a) que beta VARIA com a natureza/intensidade da operacao (QP1/QP3);
  (b) que a seletividade se preserva sob o limite adaptativo (QP2);
  (c) o PISO de overhead (O(1)/O(log n)) onde beta nao e calibravel.

## Metodologia (igual ao real-world)
- Motor unico `experiments/lib/benchmark_engine.py`: startup e compilacao FORA da medicao,
  timer ~microssegundo, repeticao adaptativa (blocos de 5, teto 35) + IQR, IC95 por bootstrap
  (10000 resamples, seed 42). Imagens Docker fixadas (gcc 16.1.0 / Python 3.11.15; ver
  `docker/ENVIRONMENT.md`), -O2, 512m, 1.0 CPU.
- beta = mediana(Python) / mediana(C++) no maior caso de teste.
- Limite adaptativo: limite_Python = beta x 1,0s; limite_C++ = 1,0s (C++ e a regua, beta_cpp=1).
- I/O simetrico (S3.1): os 6 C++ de referencia usam fast-IO (sync_with_stdio(false)+cin.tie(NULL)),
  igual ao real-world. Sem isso o beta das classes I/O-bound ficava deflacionado.

## Resultados (6 classes) - numeros de theoretical_summary.json
| Classe | beta | IC95 | C++ med | Python med | Status |
|--------|------|------|---------|------------|--------|
| O(n)   Array Sum        | 3,87  | [3,83; 4,05]  | 0,034s | 0,131s | escalavel, seletividade preservada |
| O(n^2) Matrix Sum       | 4,48  | [4,23; 4,56]  | 0,35s  | 1,59s  | escalavel, seletividade preservada |
| O(2^n) Subset Sum       | 33,84 | [33,5; 34,3]  | 0,012s | 0,42s  | escalavel, seletividade preservada |
| O(n^3) Matrix Multiply  | 77,22 | [76,2; 79,3]  | 0,021s | 1,69s  | escalavel, seletividade preservada |
| O(1)   Arithmetic       | 4,34  | [3,98; 4,46]  | 0,0018s| 0,0078s| PISO de overhead (nao calibravel) |
| O(log n) Binary Search  | 4,13  | [3,84; 4,44]  | 0,0020s| 0,0084s| PISO de overhead (nao calibravel) |
- Todas reliable. As 4 escalaveis: selectivity_preserved = true. As 2 floor: sem seletividade.

## Achados-chave
- QP1/QP3: beta NAO e constante por linguagem - cresce com a INTENSIDADE/TIPO de operacao, nao
  so com a ordem assintotica. Espectro: O(n) 3,87 < O(n^2) 4,48 < O(2^n) 33,84 < O(n^3) 77,22.
  O numerico-denso (n^3, laco aritmetico) supera ate o exponencial recursivo (2^n). Mesmo padrao
  do real-world (Floyd-Warshall compute-bound ~120 >> memory-bound ~3). Nenhum multiplicador fixo
  2-3x cobre de 3,9x a 77x.
- Prova do impacto do fast-IO (S3.1): no On2 o C++ caiu de 1,06s para 0,35s (3x) so com fast-IO,
  e o beta subiu de 1,51 (contaminado pelo cin lento) para 4,48 (real).
- PISO (S3.2, regra 10:1) - O(1) e O(log n): trabalho trivial demais; o tempo e ~100% overhead
  fixo de processo (O(1)) ou parse da entrada (O(log n) mede o parse, nao a busca). Ficam ABAIXO
  do limiar 10:1 -> beta NAO e calibravel; reportar como piso/controle, nunca como "beta de
  O(1)/O(log n)". Valor: (i) evidenciam a fronteira inferior que justifica a regra 10:1;
  (ii) anti-cherry-picking (mantemos classes onde o beta nao e grande). NOTA: o legado dava
  beta<1 ("Python superior") aqui por incluir a COMPILACAO do C++ no tempo; o motor novo exclui
  -> C++(1,8ms) << Python(7,8ms) -> ~4 (razao de OVERHEAD, nao algoritmica). Artefato morto.

## Seletividade (4 escalaveis)
- Para cada classe escalavel: a slow_solution roda sob o limite (C++ a 1,0s; Python a beta x 1,0s)
  e confirma-se TLE nas DUAS linguagens (hard-kill por timeout); a reference roda como CONTROLE e
  passa (AC). selectivity_preserved = slow rejeitada nas duas. n_trials=1 (TLE deterministico).
- Anti-otimizacao (S3.2.2): 3 casos em que o -O2 "consertava" a slow e ela passaria indevidamente
  -> strength reduction (On_linear, On2 -> volatile sink no laco); CSE (O2n -> efeito colateral
  volatile por chamada). On3 (O(n^4) loop-invariante de bloco) NAO foi reduzido (medido). Cada slow
  foi MEDIDA sob -O2, nao assumida. So no C++ (o Python interpretado nao otimiza).
- Floor (O(1)/O(log n)): a slow e pequena demais para estourar -> seletividade VACUA, nao reportada.

## Caveat (rastreabilidade)
- O C++ e tao rapido que os tempos absolutos das classes escalaveis sao pequenos (12-350ms); o
  beta (RAZAO) e reproduzivel e reliable, mas as entradas nao foram dimensionadas para o C++
  passar de 1s (tuning futuro, nao afeta a razao). On2 e o unico com Python ~1,6s e C++ ~0,35s.

## Fonte de verdade / reproducao
- Consolidado: `results/theoretical_summary.json`.
- Por classe (origem): `experiments/complexity_analysis/<classe>/results/{calibration.json, selectivity.json}`.
- Regenerar o consolidado: `cd experiments && python3 aggregate_results.py` (escreve em `results/theoretical_summary.json`).
