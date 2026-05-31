# Validacao CSES (auditoria externa por problema)

## problem02 — Cycle Finding (CSES 1197)
- Time limit oficial: 1,00s
- Memory limit oficial: 512 MB
- Link do problema: https://cses.fi/problemset/task/1197

### Submissões CSES (auditoria externa)

**C++ optimal** (28/05/2026)
- Resultado: ACCEPTED 27/27
- Tempo máximo: 0,09s (casos #6–#10)
- Tempo nos casos onde Python TLE: #6=0,09s, #7=0,09s, #8=0,08s, #9=0,09s, #10=0,08s, #27=0,02s

**Python optimal CPython3** (28/05/2026)
- Resultado: TIME LIMIT EXCEEDED
- Casos TLE: #6, #7, #8, #9, #10, #27 (6 de 27)
- Casos ACCEPTED com tempo alto: #13=0,71s, #21=0,38s, #19=0,19s, #24=0,17s
- Razão Python/C++ observada no CSES (casos AC com tempo significativo):
  #13: 0,71 / 0,02 = 35,5x
  #21: 0,38 / 0,01 = 38x
  #19: 0,19 / 0,01 = 19x

**Python suboptimal CPython3** (28/05/2026) — validação de seletividade
- Resultado: TLE em #6,7,8,9,10,13,15,19,21,27 (mais casos que a optimal,
  como esperado — adaptativo NÃO deve resgatar)

### Calibração local (pipeline rigoroso)
- Caso escolhido pelo seletor: 8.in (96.596 bytes)
- β = 35,58 [29,37 — 36,94] IC95% bootstrap (10.000 resamples, seed 42)
- C++ mediana: 0,0240s (5 reps, IQR/mediana 14,4%)
- Python mediana: 0,8542s (5 reps, IQR/mediana 3,8%)
- Ambos convergiram (is_reliable = True)

### Cross-check pipeline vs CSES
- β do pipeline local (8.in): 35,58
- β observado no CSES no caso #13 (mesma ordem de tamanho): 35,5
- Convergência forte entre métrica controlada local e juiz oficial.

### Injustiça e correção adaptativa
- CSES rejeita 6/27 casos da Python optimal por TLE.
- Limite adaptativo = β × time_limit = 35,58 × 1,0s = 35,58s.
- Sob limite adaptativo, todos os 6 casos seriam aceitos (tempos no
  CSES estavam na casa de poucos segundos).
- Suboptimal sob adaptativo (pipeline local, 30/05/2026 — veredito de submissão + caso decisivo): seletividade PRESERVADA.
  - Caso decisivo {8} (maior n×m = 2500×5000 = 12,5M; pior caso desta suboptimal — Bellman-Ford SEM early-stop + EXTRA_PASSES=150 varreduras/iteração, custo ∝ n×m, ~151× o trabalho de um Bellman-Ford completo; também já TLE no CSES). MEDIDO sob limite adaptativo 35,58s: suboptimal Python = TLE → NÃO resgatado. C++ suboptimal = TLE já a 1,0s (também tem EXTRA_PASSES=150; não recebe bônus adaptativo). Controles {1,25,26} = AC nas duas linguagens → suboptimal é correta, só lenta (0 WRONG_ANSWER).
  - Margem (justifica 1 rep determinístico): ~n×151×m ≈ 1,9×10⁹ operações de aresta em Python puro ≫ 35,58s por ordens de grandeza.
  - Aggregate (verdict_suboptimal.json): candidato TLE tradicional = {8}; resgatados = 0; selectivity_preserved = true.
  - Veredito de submissão: TLE sob o adaptativo (o caso decisivo basta) → suboptimal não resgatada; casos mais pesados seguem por monotonicidade.
  - PROVA vs EVIDÊNCIA: o CSES (TLE a 1,0s) mostra que o caso é pesado; a PROVA da seletividade é esta medição local sob o limite adaptativo (35,58s).

### Notas
- O conjunto de TLE atual {6,7,8,9,10,27} difere do antigo
  critical_cases=[6,7,8,9,10,19,21,27] registrado no código. Casos 19 e 21
  agora são ACCEPTED no CSES (com tempo alto, mas dentro do limite).
  Atualizar critical_cases quando for re-organizar configs por problema.
- Rótulos antigos no runner mencionavam CSES 1671/1672 — incorretos.
  O problema correto é CSES 1197 Cycle Finding.

## problem01 — Shortest Routes II (CSES 1672)
- Time limit oficial: 1,00s
- Memory limit oficial: 512 MB
- Link do problema: https://cses.fi/problemset/task/1672/

### Submissões CSES (auditoria externa)

**C++ optimal** (28/05/2026)
- Resultado: ACCEPTED 16/16
- Tempo máximo: 0,27s (#14)
- Tempos: #1–5,#13,#16 ≈ 0,00–0,02s; #6=0,09s, #7=0,09s, #8=0,09s, #9=0,09s, #10=0,06s, #11=0,16s, #12=0,17s, #14=0,27s, #15=0,15s

**Python optimal CPython3** (28/05/2026)
- Resultado: TIME LIMIT EXCEEDED
- Casos TLE: #6, #7, #8, #9, #10, #11, #12, #14, #15 (9 de 16, 56%)
- Casos ACCEPTED: #1–5, #13, #16 (todos ~0,02s)

**Python suboptimal CPython3** (30/05/2026) — validação de seletividade
- Resultado: TIME LIMIT EXCEEDED
- Casos TLE: #6, #7, #8, #9, #10, #11, #12, #14, #15 (9 de 16) — mesmo conjunto da Python optimal
- Casos ACCEPTED: #1–5 (~0,03s), #13 (0,02s), #16 (0,02s)
- Observação: no limite tradicional de 1,0s o veredito da suboptimal é IDÊNTICO ao da optimal. A seletividade do adaptativo (não resgatar a suboptimal) só se demonstra sob o limite β=120,12s no pipeline local — ver "Suboptimal sob adaptativo".
- Link da submissão: dressa, 2026-05-30 18:39:12

**C++ suboptimal C++11** (30/05/2026) — documentação (não entra em β nem no argumento de injustiça)
- Resultado: TIME LIMIT EXCEEDED
- Casos TLE: #6, #7, #8, #9, #10, #11, #12, #14, #15 (9 de 16) — mesmos casos
- Casos ACCEPTED: #1–5, #13, #16 (todos 0,00s)
- Nota: SLOW_FACTOR=100 também no C++; logo NÃO é o "optimal C++" da calibração. Warning benigno do compilador: zero-length printf format string.
- Link da submissão: dressa, 2026-05-30 18:41:28

### Calibração local (pipeline rigoroso)
- Caso escolhido pelo seletor: 14.in (5.121.212 bytes; n=500, m=250.000, q=100.000)
- β = 120,12 [118,01 — 124,26] IC95% bootstrap (10.000 resamples, seed 42)
- C++ mediana: 0,1477s (5 reps, IQR/mediana 2,1%)
- Python mediana: 17,7412s (5 reps, IQR/mediana 3,4%)
- Ambos convergiram (is_reliable = True). Wall total da calibração: 118s.

### Cross-check pipeline vs CSES
- β do pipeline local (14.in): 120,12
- No CSES o caso #14 deu C++ 0,27s e Python TLE (>1s, tempo exato indisponível); sem AC do Python no caso, não dá para calcular um β CSES direto neste caso.
- Cross-check de hardware no C++ (mesmo caso #14): CSES 0,27s vs local 0,1477s → CSES ~1,83x mais lento. Coerente: na ordem do que vimos no problem02.
- Magnitude do β (~120x) é coerente com Floyd-Warshall puro em laço Python (overhead do interpretador domina o triplo-laço n³).

### Injustiça e correção adaptativa
- CSES rejeita 9/16 casos (56%) da Python optimal por TLE — proporcionalmente mais severa que problem02 (6/27 = 22%).
- Limite adaptativo = β × time_limit = 120,12 × 1,0s = 120,12s.
- Veredito local (pipeline, 3 reps/caso, wall total 347s):
  - TLE injusto no tradicional (C++ AC + Python TLE a 1,0s): **9/16** casos = {6,7,8,9,10,11,12,14,15}.
  - Resgatados pelo adaptativo (Python AC a 120,12s): **9/9 = 100%**.
  - Conjunto TLE local bate EXATAMENTE com o CSES — diferente do problem02, aqui o local reproduz a injustiça integralmente (Floyd-Warshall em Python é lento o bastante para TLE a 1,0s mesmo nesta máquina; máquina mais rápida não "esconde" a injustiça como no problem02).
  - Nenhum WRONG_ANSWER.
- Suboptimal sob adaptativo (pipeline local, re-rodado 30/05/2026 — abordagem veredito-de-submissão): seletividade PRESERVADA.
  - Princípio: o veredito do juiz é da SUBMISSÃO, definido pelo pior caso — basta 1 caso dar TLE sob o adaptativo para a submissão suboptimal ser rejeitada. Não é preciso medir todos os casos; mede-se o caso decisivo (o de MAIOR tempo medido, onde a suboptimal mais estoura o limite).
  - MEDIDO (verdict_suboptimal.json, 1 rep — TLE no limite é determinístico): caso decisivo {14} (maior tempo, optimal Python 17,1s → suboptimal ≈ 100× ≫ 120,12s) = TLE @120,12s sob o adaptativo → NÃO resgatado. Controles {1,13,16} = ACCEPTED sob os dois limites → a suboptimal é CORRETA, só lenta (não WRONG_ANSWER). Aggregate: candidatos TLE tradicional = {14}; resgatados = 0; selectivity_preserved = true; 0 WRONG_ANSWER.
  - Veredito de submissão: TLE sob o adaptativo (o caso decisivo basta) → suboptimal não resgatada.
  - Monotonicidade (só para cima): como o caso decisivo é o mais lento, qualquer entrada maior também daria TLE. Casos menores podem ser AC, e isso é irrelevante para o veredito da submissão. Logo a afirmação correta é "submissão rejeitada (TLE no caso decisivo)", NÃO "todos os casos dão TLE".
  - C++ no caso decisivo {14}: também TLE (o C++ suboptimal tem SLOW_FACTOR=100; TLE já a 1,0s, tradicional e adaptativo, pois o C++ não recebe o bônus adaptativo). Documenta que a solução ineficiente é rejeitada nas duas linguagens; coerente com o CSES.
  - Nota de método: substitui a rodada anterior (controles + borderline {10} + maior {14} + argumento analítico para 7 casos). A nova abordagem dispensa o argumento analítico — o caso decisivo medido fecha a submissão.

### Notas
- O conjunto de TLE observado {6,7,8,9,10,11,12,14,15} coincide com o critical_cases do runner antigo do problem01.
- metadata/metadata_graficos.json dizia casos_tle_cses=[8,12,15] — incompleto/incorreto vs realidade observada; revisar quando for re-organizar configs por problema.

## problem03 — Planets Queries I (CSES 1750)
- Time limit oficial: 1,00s
- Memory limit oficial: 512 MB
- Link do problema: https://cses.fi/problemset/task/1750
- Código submetido idêntico ao implementations/optimal/ do repo (conferido).

### Submissões CSES (auditoria externa)

**C++ optimal** (C++11, 2026-05-30 22:53:17, dressa)
- Resultado: ACCEPTED 14/14
- Tempo máximo: 0,99s (#12 — quase no limite de 1,0s)
- Tempos: #12=0,99s, #8=0,60s, #9=0,37s, #10=0,34s, #6=0,23s, #7=0,22s, #14=0,02s; demais (#1–5,#11,#13) ≈ 0,00s

**Python optimal CPython3** (2026-05-30 22:52:27, dressa)
- Resultado: TIME LIMIT EXCEEDED
- Casos TLE: #6, #7, #8, #9, #10, #12 (6 de 14, 43%)
- Casos ACCEPTED: #1–5 (0,02s), #11 (0,02s), #13 (0,02s), #14 (0,20s)
- Injustiça confirmada: nos casos {6,7,8,9,10,12} o C++ é ACCEPTED e o Python equivalente recebe TLE.

**Python suboptimal CPython3** (2026-05-30 23:58:58, dressa) — validação de seletividade
- Resultado: TIME LIMIT EXCEEDED
- Casos TLE: #6,7,8,9,10,12,14 (7 de 14); ACCEPTED: #1–5,#11,#13 (0,02s)
- Suboptimal = simulação ingênua O(q·k) (versão limpa, sem padding artificial). TLE em MAIS casos que a optimal (+#14, que a optimal passou em 0,20s) — a ingênua é mais lenta. AC nos casos pequenos (k pequeno) confirma que é correta, só lenta.

**C++ suboptimal C++11** (2026-05-30 23:59:35, dressa) — documentação
- Resultado: TIME LIMIT EXCEEDED
- Casos TLE: #6,7,8,9,10,12,14 (7); ACCEPTED: #1–5,#11,#13 (~0,00s) — mesmo conjunto da Python suboptimal.
- A solução ineficiente é rejeitada nas duas linguagens (não recebe bônus adaptativo no C++).

### Calibração local (pipeline rigoroso)
- Caso escolhido pelo seletor: 12.in (4.577.707 bytes — maior por bytes; coincide com o caso #12, o boundary do C++ no CSES)
- β = 3,07 [2,85 — 3,60] IC95% bootstrap (10.000 resamples, seed 42)
- C++ mediana: 0,8442s (5 reps, IQR/mediana 7,3%)
- Python mediana: 2,5914s (5 reps, IQR/mediana 12,8%)
- Ambos convergiram (is_reliable = True).
- β baixo (~3) vs problem01 (120) e problem02 (36): binary lifting é memory-bound (saltos aleatórios na tabela `up` ~24 MB → cache misses), então o C++ não tem a vantagem usual; ambos ~1–3s. Contraste útil pro artigo: β depende de compute-bound (alto) vs memory-bound (baixo). Aqui o β novo (3,07) ficou perto do legado (3,19), pois com tempos ~1–3s o startup quase não contamina.

### Cross-check pipeline vs CSES
- C++ no caso 12: local 0,844s vs CSES 0,99s → CSES ~1,17x mais lento (coerente com problem01/02).
- β direto do CSES no caso grande NÃO disponível: nos casos grandes o Python deu TLE no CSES (sem tempo registrado). O único caso com ambos medidos é #14 (pequeno): C++ 0,02s, Python 0,20s → ~10x, mas dominado por overhead de caso pequeno, não comparável ao β do caso grande. Logo o cross-check aqui é mais fraco que no problem02; β=3,07 é a medição controlada local.

### Injustiça e correção adaptativa
- CSES rejeita 6/14 casos (43%) da Python optimal por TLE.
- Limite adaptativo = β × time_limit = 3,07 × 1,0s = 3,07s.
- Veredito local (pipeline, 3 reps/caso):
  - TLE injusto no tradicional (C++ AC + Python TLE a 1,0s): 4/14 {8,9,10,12}.
  - Resgatados pelo adaptativo (Python AC a 3,07s): 4/4 = 100%. Nenhum WRONG_ANSWER.
  - Cases 6 e 7: CSES = TLE, local = AC (máquina local mais rápida; Python rodou <1,0s neles). Logo o local reproduz 4 dos 6 casos TLE do CSES (perde os 2 borderline). Coerente com a REGRA #0 (CSES decide; local é hardware-dependente).
  - RESSALVA (margem apertada): o resgate do caso 12 é no limiar — Python ~2,59s (reps até 3,04s) vs limite adaptativo 3,07s. Com o β pontual resgata; se o limite usasse o IC inferior (2,85), o caso 12 poderia estourar em algumas reps. β pequeno → pouca folga (diferente do problem01).
- Suboptimal sob adaptativo (pipeline local, 30/05/2026 — veredito de submissão + caso decisivo): seletividade PRESERVADA.
  - Suboptimal = simulação ingênua O(q·k) (versão limpa, sem padding artificial). Caso decisivo {12} (maior soma de k ≈ 1,07×10¹⁴ → ~10¹⁴ passos ≫ qualquer limite; também já TLE no CSES). MEDIDO sob limite adaptativo 3,07s: suboptimal Python = TLE → NÃO resgatada. C++ suboptimal = TLE já a 1,0s (não recebe bônus). Controles {1,13} = AC nas duas linguagens → correta, só lenta (0 WRONG_ANSWER).
  - Margem (1 rep determinístico): ~10¹⁴ passos estouram o limite por ordens de grandeza.
  - Aggregate (verdict_suboptimal.json): candidato TLE tradicional = {12}; resgatados = 0; selectivity_preserved = true.
  - Veredito de submissão: TLE sob o adaptativo → suboptimal não resgatada; casos mais pesados seguem por monotonicidade.
  - PROVA vs EVIDÊNCIA: o CSES (TLE a 1,0s) mostra que é pesada; a prova da seletividade é esta medição local sob o limite adaptativo (3,07s).

### Notas
- Caso #12 no C++ deu 0,99s (no fio do limite de 1,0s) — boundary case mesmo para C++.
- Equivalência comportamental (CSES): nos 8 casos onde ambos terminam (#1–5,#11,#13,#14), as duas linguagens produzem a saída aceita (correta).

## dp/problem01 — Coin Combinations I (CSES 1635)
- Time limit oficial: 1,00s
- Memory limit oficial: 512 MB
- Link do problema: https://cses.fi/problemset/task/1635
- Design DP (diferente dos grafos): dois optimals — ITERATIVO (bottom-up) vs RECURSIVO (top-down memoizado); ambos O(x·n). 4 submissões CSES (iter cpp/py, rec cpp/py). Suboptimal (recursão sem memo, exponencial) virá na fase seguinte. 13 casos de teste.

### Submissões CSES (auditoria externa)

**C++ optimal ITERATIVO** (C++11, 2026-05-31 00:40:03, dressa)
- Resultado: ACCEPTED 13/13
- Tempo máximo: 0,57s (#4, #8, #11); demais ≤ 0,30s

**Python optimal ITERATIVO** (CPython3, 2026-05-31 00:36:34, dressa)
- Resultado: TIME LIMIT EXCEEDED
- Casos TLE: #4, #5, #8, #11, #12 (5 de 13)
- Casos ACCEPTED: #1,#3,#6,#7,#9,#10,#13 (≤0,07s); #2 = 0,21s
- Injustiça (iterativo): nos casos {4,5,8,11,12} o C++ iterativo é ACCEPTED (≤0,57s) e o Python iterativo equivalente recebe TLE.

**C++ optimal RECURSIVO** (C++11, 2026-05-31 00:42:55, dressa)
- Resultado: ACCEPTED 13/13
- Tempo máximo: 0,55s (#4), 0,54s (#8, #11); demais ≤ 0,19s
- NÃO deu RTE / stack overflow — a preocupação de profundidade de recursão não se materializou nestes casos. β_recursivo é viável.

**Python optimal RECURSIVO** (CPython3, 2026-05-31 00:42:22, dressa)
- Resultado: TIME LIMIT EXCEEDED
- Casos TLE: #4, #5, #8, #11 (4 de 13)
- Casos ACCEPTED: #1,#3,#6,#7,#9,#10,#12,#13 (≤0,11s); #2 = 0,79s (perto do limite)
- Injustiça (recursivo): nos casos {4,5,8,11} o C++ recursivo é ACCEPTED (≤0,55s) e o Python recursivo equivalente recebe TLE.

**Suboptimal ITERATIVA** (optimal iterativo deliberadamente desacelerado, SLOW_FACTOR=100) — seletividade
- C++ (2026-05-31 02:18:58): TIME LIMIT EXCEEDED. TLE em {4,5,8,11,12} (5); AC em {1,2,3,6,7,9,10,13} (#2=0,63s)
- Python (2026-05-31 02:20:17): TIME LIMIT EXCEEDED. TLE em {2,4,5,7,8,11,12,13} (8); AC em {1,3,6,9,10}

**Suboptimal RECURSIVA** (recursão sem memo, exponencial) — seletividade
- Python (2026-05-31 02:21:05): TIME LIMIT EXCEEDED. TLE em {4,5,7,8,11,13} (6); AC em {1,2,3,6,9,10,12}
- C++ (2026-05-31 02:21:59): TIME LIMIT EXCEEDED. TLE em {4,5,7,8,11,13} (6); AC em {1,2,3,6,9,10,12} — mesmo conjunto da Python recursiva
- Nota: as DUAS suboptimals são REJEITADAS (TLE geral) no CSES, nas duas linguagens. Conjuntos TLE diferem (iterativa: custo ∝ x·n×100, TLE em tabela grande incl. #12; recursiva: custo ∝ nº de combinações, AC no #12 de resposta pequena). Ambas rejeitadas → seletividade confirmada externamente; falta confirmar local sob o β operacional 34,80s.

### Calibração local (pipeline rigoroso) — dois β
- Caso escolhido (override --case 11): 11.in (denso, x=10⁶, n=100, x·n=10⁸; ambos estilos estressados). NÃO o #12 (maior bytes) porque #12 é esparso e o recursivo escapa (memo só visita estados alcançáveis) — subestimaria β_rec. Cost driver do DP é x·n, não bytes.
- **β_iterativo = 11,12** [10,93 — 12,04] IC95%. C++ iter 0,566s (IQR 0,8%, 5 reps) · Python iter 6,29s (IQR 5,6%, 5 reps). is_reliable.
- **β_recursivo = 34,80** [30,69 — 35,45] IC95%. C++ rec 0,324s (IQR 8,6%, 5 reps) · Python rec 11,28s (IQR 1,3%, 5 reps). is_reliable.
- ACHADO (QP3): o estilo RECURSIVO ~triplica o β (11 → 35). Dois efeitos: (a) Python recursivo mais lento que iterativo (overhead de chamada: 11,28s vs 6,29s); (b) C++ recursivo mais RÁPIDO que iterativo (memo visita menos estados: 0,324s vs 0,566s). A recursão amplifica a penalidade do Python no MESMO problema.
- Cross-check de hardware: C++ iterativo local 0,566s ≈ CSES #11 0,57s.

### Injustiça e correção adaptativa
- β OPERACIONAL = β_rec = 34,80 (o maior; resgata o estilo correto mais lento — ver HANDOVER "MULTIPLOS ESTILOS"). Limite adaptativo Python = 34,80s. Os dois β (11,12 e 34,80) ficam como resultado de QP3.
- Veredito local ITERATIVO (3 reps, sob 34,80s): TLE injusto {4,5,8,11} (4/13, C++ AC + Python TLE); resgatados 4/4 = 100%; 0 WA. (#12 local = Python AC, ≠ CSES TLE — máquina mais rápida; local reproduz 4 dos 5 casos do CSES iterativo.)
- Veredito local RECURSIVO (3 reps, sob 34,80s): TLE injusto {4,5,8,11} (4/13); resgatados 4/4 = 100%.
  - SETUP DE PILHA (ajuste de fidelidade ao CSES, NÃO uma anomalia): o caso #2 (x=10⁶, moeda única=1 → profundidade de recursão 10⁶) estourava a pilha default do container (~8MB) no C++ recursivo, enquanto o CSES aceita (usa pilha maior). Era inconsistência nossa — dávamos sys.setrecursionlimit(1.1M) ao Python mas o C++ usava a pilha default. CORRIGIDO: ulimit -s = 256MB no engine (benchmark_engine.py). VERIFICADO no pipeline: com o fix, o C++ recursivo #2 passa local (ACCEPTED, 0,027s — batendo com o CSES 0,06s); os outros 12 casos ficam idênticos (o ulimit só afeta runs que estouravam). Conjunto injusto {4,5,8,11} e resgate 4/4 inalterados.
- Suboptimal sob adaptativo (pipeline local, 31/05/2026 — veredito de submissão + caso decisivo): seletividade PRESERVADA nos DOIS estilos.
  - β operacional 34,80s. Caso decisivo {11} (TLE no CSES nas duas suboptimals; é o caso de calibração). Controles {1,9} = AC (corretas, só lentas).
  - suboptimal_iterative (optimal iterativo ×100, slowdown deliberado): caso 11 = TLE em Python E C++ sob 34,80s → NÃO resgatada. selectivity_preserved=true, 0 WA.
  - suboptimal_recursive (sem memo, exponencial): caso 11 = TLE em Python E C++ sob 34,80s → NÃO resgatada. selectivity_preserved=true, 0 WA.
  - Veredito de submissão: as duas rejeitadas sob o adaptativo. O β generoso (34,80 — do estilo correto mais lento) resgata os optimals mas NÃO resgata as suboptimals → seletividade mantida mesmo com o β grande (gap optimal↔suboptimal claro). Coerente com o CSES (as duas TLE lá).

### Notas
- RESULTADO HONESTO (contraria a hipótese simples "recursivo pior, iterativo passa"): AMBOS os estilos Python deram TLE. O iterativo TLE em 5 casos {4,5,8,11,12}; o recursivo em 4 {4,5,8,11} — o iterativo TLE em MAIS casos, não menos.
- Nuance (achado real): onde ambos rodam, o RECURSIVO é mais LENTO por caso (overhead de chamada; #2 = 0,79s rec vs 0,21s iter). MAS o recursivo memoiza só os estados ALCANÇÁVEIS, enquanto o iterativo preenche a tabela inteira O(x·n); no #12 isso fez o recursivo passar (0,06s) e o iterativo dar TLE. Logo "recursivo sempre pior" não se sustenta — depende da esparsidade dos estados.
- C++ AC nos dois estilos → a injustiça é Python vs C++ em ambos. β a medir por estilo (β_rec ≷ β_iter conforme o caso/esparsidade). NÃO houve RTE no C++ recursivo (profundidade não estourou a pilha nestes casos).

## dp/problem02 — Grid Paths (CSES 1638)
- Time limit oficial: 1,00s
- Memory limit oficial: 512 MB
- Link do problema: https://cses.fi/problemset/task/1638
- Design DP: dois optimals — ITERATIVO (forward, dp[i][j]=dp[i-1][j]+dp[i][j-1]) vs RECURSIVO (backward, solve(i,j)=solve(i,j+1)+solve(i+1,j), memo); ambos O(n²). Recursão RASA (prof ≤ 2(n-1) ~2000, sem RTE). 15 casos.

### Submissões CSES (auditoria externa)

**C++ optimal ITERATIVO** (C++11, 2026-05-31 02:54:27, dressa)
- Resultado: ACCEPTED 15/15. Tempo máximo: 0,02s (#10).

**Python optimal ITERATIVO** (CPython3, 2026-05-31 02:53:12, dressa)
- Resultado: ACCEPTED 15/15. Tempos: #6=0,38s, #7=0,36s, #8=0,34s, #9=0,31s, #10=0,21s; demais ~0,02s.

**C++ optimal RECURSIVO** (C++11, 2026-05-31 02:56:20, dressa)
- Resultado: ACCEPTED 15/15. Tempo máximo: 0,03s. SEM RTE (recursão rasa ≤~2000 níveis — confirma a análise estática).

**Python optimal RECURSIVO** (CPython3, 2026-05-31 02:55:10, dressa)
- Resultado: TIME LIMIT EXCEEDED. Casos TLE: #6, #7 (2 de 15); ACCEPTED nos demais (#8=0,88s no fio, #9=0,53s).
- INJUSTIÇA (recursão-específica): C++ recursivo AC (≤0,03s) mas Python recursivo equivalente TLE em {6,7}. O Python ITERATIVO passa (AC 15/15) — só o estilo recursivo sofre.

### Calibração local (pipeline rigoroso) — dois β
- Caso = default (maior bytes = #6, n=1000, n²=10⁶, denso). O seletor por bytes serve aqui (input ~n² = custo), não precisou override como no dp01.
- **β_iterativo = 12,03** [11,65 — 12,15] IC95%. C++ iter 0,0114s (IQR 3,3%, 5 reps) · Python iter 0,1375s (IQR 1,2%, 5 reps). is_reliable.
- **β_recursivo = 23,47** [21,50 — 26,92] IC95%. C++ rec 0,0172s (IQR 12,0%, 5 reps) · Python rec 0,4042s (IQR 5,4%, 5 reps). is_reliable.
- ACHADO (QP3): recursão ~DOBRA o β (12 → 23,5). Diferente do dp01: aqui o C++ recursivo é mais LENTO que o iterativo (0,017 vs 0,011 — Grid Paths é DENSO, o memo visita todos os n² estados, sem escape); o Python recursivo é ~3x o iterativo (0,40 vs 0,14, overhead de chamada).

### Cross-check / dependência de hardware
- SEM cross-check de β confiável aqui: os tempos de C++ no CSES estão no piso de resolução (~0,01-0,03s) e o Python recursivo deu TLE (sem tempo registrado) — não dá pra computar uma razão Python/C++ confiável no CSES. β é a medição local controlada (como no problem03). (NÃO usar 0,38/0,01 ≈ "38x" — o 0,01s é piso de resolução, razão instável.)
- Hardware-dependência (ancorada no RECURSIVO, que é onde houve TLE): o Python recursivo deu TLE no CSES em {6,7} (>1s) mas roda ~0,40s < 1,0s LOCALMENTE → AC. A máquina local é mais rápida que a do CSES.
- O Python ITERATIVO passou nos dois ambientes (CSES AC 15/15 e local AC) — então NÃO há injustiça no estilo iterativo; a injustiça é só no recursivo.
- IMPLICAÇÃO (confirmada no veredito): o veredito local NÃO reproduz o TLE do CSES — a injustiça do dp02 é CSES-only (REGRA #0: CSES decide; veredito local é hardware-dependente). Mesmo padrão do problem02 grafos.

### Injustiça e correção adaptativa
- β operacional = β_rec = 23,47 (o maior — ver HANDOVER "MULTIPLOS ESTILOS"). Limite adaptativo Python = 23,47s. Os dois β (12,03 e 23,47) = resultado de QP3.
- Veredito local (pipeline, 3 reps, os 2 estilos, sob β operacional 23,47s): TLE injusto local = 0/15 nos DOIS estilos (todos os 15 casos AC sob 1,0s, Python E C++). 0 WA.
- A injustiça do dp02 é CSES-ONLY: no CSES o Python recursivo deu TLE em {6,7}, mas localmente roda ~0,40s < 1,0s → AC (máquina local mais rápida; REGRA #0). O mecanismo adaptativo (β_rec=23,47 → 23,47s) resgataria o Python recursivo ONDE a injustiça aparece (CSES / máquina mais lenta); localmente não há o que resgatar (tudo < 1,0s).

### Notas
- CASO LIMPO da injustiça de recursão (valida a S2.2 do artigo): Python iterativo (bottom-up) AC nas duas linguagens; Python recursivo memoizado TLE. Mesmo problema, mesma complexidade O(n²), mesma resposta — só o estilo muda. A penalidade da recursão (overhead de chamada no interpretador) foi DECISIVA (empurrou o recursivo por cima do limite; o iterativo ficou abaixo).
- Contraste com dp01 (Coin Combinations): lá AMBOS os Python TLE (recursão não foi decisiva). Aqui é decisiva → a penalidade da recursão é sempre real (recursivo sempre mais lento; β_rec > β_iter), mas sua DECISIVIDADE (separar AC de TLE) é PROBLEMA-DEPENDENTE.
- O fix do ulimit não foi exigido aqui (recursão rasa, sem RTE); está no engine por consistência.

### Seletividade (fase suboptimal — CSES decide a rejeição)
- 2 suboptimals (paralelo aos optimals): `suboptimal_recursive` (recursão SEM memo → exponencial no nº de caminhos) e `suboptimal_iterative` (optimal iterativo × SLOW_FACTOR, slowdown deliberado honesto).
- CSES `suboptimal_recursive`: C++ TLE {6,7,8,9}, Python TLE {6,7,8,9} (ambas AC no resto, inclusive #10 — o nº de caminhos varia por grid; #10 tem poucos o bastante). → REJEITADA nas duas linguagens. ✓
- CSES `suboptimal_iterative` ×100: Python TLE {6,7,8,9,10} → REJEITADA; **C++ ACCEPTED 15/15** (máx #10 = 0,96s, no fio) → PASSOU. Ou seja: ×100 BASTOU pro Python, mas NÃO pro C++.
  - ACHADO (magnitude da injustiça): um C++ iterativo sabotado 100× ainda passa, enquanto a optimal recursiva Python (correta) não — ver anotacoes_para_artigo.md.
  - AJUSTE: SLOW_FACTOR elevado 100 → 300. CSES iterativa ×300: C++ TLE {6,7,8,9,10}, Python TLE {6,7,8,9,10} → REJEITADA nas DUAS (seletividade limpa). ✓ confirmado.
- RESUMO CSES suboptimal: as 2 suboptimals (recursiva sem memo + iterativa ×300) ficam REJEITADAS nas duas linguagens no CSES.
- SELETIVIDADE LOCAL (bench, sob β_op 23,47s, reps=1, hard-kill): decisivo #6 (CSES-TLE) + controles {1-5}. As DUAS suboptimals: controles {1-5} AC (corretas, só lentas); decisivo #6 trad[cpp=TLE, py=TLE] adapt[py=TLE] → 0 resgatadas pelo adaptativo, selectivity_preserved=True, 0 WA. Mesmo com o bônus de 23,47s o juiz adaptativo NÃO deixa passar as suboptimals (continuam rejeitadas). ✓ dp/problem02 FECHADO (optimal + suboptimal, 2 estilos).

---

## dp/problem03 — Two Sets II (CSES 1093)
- Time limit oficial: 1,00s
- Memory limit oficial: 512 MB
- Link do problema: https://cses.fi/problemset/task/1093
- Design DP: contar subconjuntos de {1..n} com soma S/2 (S=n(n+1)/2; se S ímpar → 0; ÷2 via inverso modular de 2 / Fermat). Dois optimals — ITERATIVO (rolling 2-row, O(n²) espaço) vs RECURSIVO (top-down + memo 2D cheio, O(n³) espaço); ambos O(n³) tempo. n≤500. 24 casos.
- FIX (análise estática, pré-CSES): o C++ iterativo usava matriz 2D cheia (~250MB) e o Python rolling 2-row — não batiam (distorceria β). C++ iterativo reescrito p/ rolling 2-row (= Python); re-validado no CSES (AC).

### Submissões CSES (auditoria externa)

**C++ optimal ITERATIVO** (C++11, rolling pós-fix, 2026-05-31, dressa)
- Resultado: ACCEPTED 24/24. Tempo máximo: 0,07s (#21, #24). Confirma o fix.

**C++ optimal RECURSIVO** (C++11, memo 2D, 2026-05-31, dressa)
- Resultado: ACCEPTED 24/24. Tempo máximo: 0,57s (#21, #24). ~8× mais lento que o iterativo (memo 250MB + memset + recursão), mas AC.

**Python optimal ITERATIVO** (CPython3, 2026-05-31, dressa)
- Resultado: TIME LIMIT EXCEEDED. Casos TLE: {17,19,20,21,23,24} (n=328,431,451,500,480,499 — even-sum grandes). Máx AC 0,16s (#15, n=147).

**Python optimal RECURSIVO** (CPython3, 2026-05-31, dressa)
- Resultado: TIME LIMIT EXCEEDED. Casos TLE: {17,19,20,21,23,24} (os MESMOS do iterativo). Máx AC 0,44s (#15). Sem MLE (memo coube em 512 MB, só estourou tempo).
- INJUSTIÇA confirmada: os 2 Python TLE, os 2 C++ AC. Recursão NÃO foi decisiva (os 2 estilos Python falham nos mesmos casos — como dp01, ≠ dp02).

### Calibração local (pipeline rigoroso) — dois β
- Caso = #21 (n=500, --case 21 override; o seletor por bytes não distingue — inputs ~3 bytes, driver de custo é n³).
- **β_iterativo = 68,27** [64,91–74,22] IC95. C++ 0,0312s (IQR 8,7%, 5 reps), Python 2,13s (IQR 0,3%, 5 reps). is_reliable=True.
- **β_recursivo = 43,27** [40,24–47,86] IC95. C++ 0,191s (IQR 0,8%, 5 reps), Python 8,26s (IQR 16,1%, 10 reps). is_reliable=True.
  - NOTA de confiabilidade (is_reliable validada na prática): uma rodada ANTERIOR do recursivo saiu is_reliable=**False** (β=39,01; C++ IQR=37%, bateu no teto de 35 reps) e ENVIESADA — outliers de contenção esporádica do host (macOS/Docker, sem cpuset/governador, S3.6) inflaram a mediana C++ (0,2035s vs ~0,191s limpos) e DEFLACIONARAM o β. As re-rodadas reliable concordam (42,73 e 43,27; IC95 sobrepostos). Experimento isolado de 35 runs do C++ deu IQR de só 3,4% → o ruído é do HOST, não do algoritmo/memset; a repetição adaptativa + a flag is_reliable filtram (descartar/re-rodar quando false, em vez de aceitar β contaminado). Em rodadas diferentes o pico de contenção cai num lado diferente (ora C++, ora Python).
- ACHADO (QP3): **β_rec < β_iter** (43 < 68) — INVERTE dp01 (β_rec≫β_iter) e dp02 (β_rec~2×). Os IC95 não se sobrepõem → robusto. Causa ESTRUTURAL (validada por medição isolada dos 4 lados, caso #21): a recursão deixa o C++ ~6,3× mais lento (0,031s→0,191s, memo 2D cheio de 250MB + memset) mas o Python só ~3,6× (2,15s→7,78s) → como β=T_py/T_cpp e o denominador (C++) cresce mais, o β encolhe.
- **β OPERACIONAL = max(β_iter, β_rec) = β_iterativo = 68,27** (reliable). PRIMEIRO DP em que o operacional vem do ITERATIVO (dp01/dp02 vinha do recursivo). Limite adaptativo Python = 68,27s; resgata os 2 estilos (Python iter 2,13s, rec 8,26s, ambos < 68,27s). NOTA: aqui a intuição "estilo mais lento = maior β" quebra (o mais lento é o rec, mas tem o menor β); mesmo assim max(β) resgata tudo, pois todo C++ < 1,0s → β_estilo×1,0 ≥ tempo_Python_estilo.

### Cross-check pipeline vs CSES
- SEM cross-check de β confiável (igual dp02 e problem03 grafos): nos casos grandes o Python deu TLE no CSES (sem tempo registrado) e o C++ iterativo está no piso de resolução (~0,03–0,07s) — razão Python/C++ instável. O β é a medição controlada local. (NÃO fabricar razão a partir do piso de resolução.)

### Injustiça e correção adaptativa
- Veredito local sob β operacional **68,27s** (24 casos, 3 reps), os dois estilos, 0 WRONG_ANSWER (equivalência comportamental confirmada):
  - **ITERATIVO**: 5 TLE injusto (trad. 1,0s) {19,20,21,23,24}; resgatados pelo adaptativo 5/5 (100%). Reproduz 5 dos 6 TLE do CSES — perde o borderline #17 (o Python iterativo local é rápido o bastante, #17 fica < 1,0s).
  - **RECURSIVO**: 6 TLE injusto {17,19,20,21,23,24}; resgatados 6/6 (100%). Reproduz EXATO os 6 do CSES (o Python recursivo é mais lento — 8,3s vs 2,1s em n=500 — então mesmo o #17 estoura 1,0s local).
  - Limite adaptativo 68,27s resgata 100% nos dois estilos; nenhum WA.
  - Nuance (valida S2.2 do artigo): mesmo problema, mesma complexidade O(n³), mesma resposta — só o ESTILO muda, e o RECURSIVO é mais propenso a TLE (reproduz +1 caso de injustiça que o iterativo). A penalidade da recursão em Python é real e mensurável.

### Notas
- test_data: BAIXADO do CSES (não gerado — gerar o output seria circular com a nossa solução). Download inicial veio com 23 casos (faltava o n=1) e numeração +1 deslocada; reconstruído dos detalhes oficiais (Test #1..#24) → 24/24, numeração IDÊNTICA ao CSES (#N = caso N). Stress n=500 = #21.
- Casos com S ímpar (n=222,357,69,114,126…) curto-circuitam em 0 instantâneo; só even-sum grandes (n=107,112,147,431,451,480,499,500) são pesados.
- O legado problem_specification.md tinha erro (dizia n=4 → soma ímpar → 0; na verdade soma 10 é par, resposta 1, confirmado pelo CSES #4). Já em _legacy/; usamos o output do CSES.

### Seletividade (fase suboptimal — CSES decide a rejeição)
- 2 suboptimals (paralelo aos optimals): `suboptimal_recursive` (recursão SEM memo → exponencial ~2ⁿ; ineficiência algorítmica genuína; profundidade O(n) rasa, sem array memo → TLE por TEMPO, não RTE) e `suboptimal_iterative` (optimal iterativo rolling 2-row × SLOW_FACTOR=100, slowdown deliberado honesto com volatile sink no C++).

**Suboptimal RECURSIVA** (sem memo, exponencial) — 2026-05-31, dressa
- Python CPython3: TLE → REJEITADA. Casos TLE {11,12,15,17,19,20,21,23,24} (9); AC nos demais 15 (corretos, só lentos).
- C++ C++11: TLE → REJEITADA. Casos TLE {11,12,15,17,19,20,21,23,24} (9; MESMO conjunto da Python). → rejeitada nas duas linguagens. ✓

**Suboptimal ITERATIVA** (optimal iterativo ×100) — 2026-05-31, dressa
- Python CPython3: TLE → REJEITADA. Casos TLE {11,12,15,17,19,20,21,23,24} (9).
- C++ C++11: TLE → REJEITADA. Casos TLE {17,19,20,21,23,24} (6); AC nos demais 18 (máx #11=0,07s, #12=0,08s, #15=0,17s).
- CONTRASTE com dp02: aqui ×100 BASTOU para rejeitar o C++ também (n=500 maior, custo n³×100 estoura), enquanto no dp02 (n menor) o C++ ×100 passava e foi preciso subir a ×300. SLOW_FACTOR=100 mantido. O C++ iterativo ×100 dá TLE no MESMO conjunto que a optimal Python ({17,19,20,21,23,24}).

- RESUMO CSES suboptimal: as 2 suboptimals (recursiva sem memo + iterativa ×100) ficam REJEITADAS nas duas linguagens no CSES.
- SELETIVIDADE LOCAL (bench, sob β operacional 68,27s, reps=1, hard-kill): decisivo #21 (n=500, TLE no CSES nas duas) + controles {3,4,7,8} (even-sum pequenos, exercitam o algoritmo). As DUAS suboptimals: controles {3,4,7,8} AC nas duas linguagens (corretas, só lentas); decisivo #21 trad[cpp=TLE, py=TLE] adapt[py=TLE] → 0 resgatadas pelo adaptativo; selectivity_preserved=True, 0 WA. verdict_suboptimal_{iterative,recursive}.json gravados (β=68,27). Mesmo com o bônus de 68,27s o juiz adaptativo NÃO resgata as suboptimals (gap optimal↔suboptimal claro: optimal Python iter 2,13s / rec 8,26s em n=500 ≪ 68,27s; as suboptimals estouram). ✓ dp/problem03 FECHADO (optimal 2 estilos + suboptimal 2 estilos).

---

## backtracking/problem01 — Chessboard and Queens (CSES 1624)
- Time limit oficial: 1,00s | Memory limit: 512 MB
- Link: https://cses.fi/problemset/task/1624
- Design backtracking: UM optimal recursivo (DFS row-by-row + poda de coluna e 2 diagonais), 1 beta (backtracking não tem contraparte iterativa idiomática). 10 casos. Profundidade fixa = 8 (sem stack issue).
- PAPEL deste problema: CASO DE CONTROLE (caso justo), NÃO um caso de injustiça. O input é FIXO 8x8 (não-escalável) → o optimal é trivial nas 2 linguagens (ver CSES abaixo). Decisão (usuária, 31/05): manter como controle + seletividade; NÃO reportar beta.

### Submissões CSES (auditoria externa) — 2026-05-31, dressa (código = repo)
**C++ optimal RECURSIVO** (C++11)
- Resultado: ACCEPTED 10/10. Tempo: 0,00s em todos (piso de resolução).
**Python optimal RECURSIVO** (CPython3)
- Resultado: ACCEPTED 10/10. Tempo: 0,02s em todos.
- Caso de controle: as duas linguagens AC, sem TLE (Python 0,02s, abaixo do limite de 1,0s). Como o input é fixo (8x8, não escalável), não há disparidade observável no optimal. Dado relevante para QP3: a ocorrência de injustiça depende da natureza do problema, não é uma constante por linguagem.

### Calibração / beta — NÃO APLICÁVEL (declarado, não fabricado)
- beta INVIÁVEL aqui: input fixo 8x8, C++ no piso (0,00s) → impossível satisfazer a dominância de escala 10:1 da S3.2 (custo algorítmico ≫ overhead). Calibrar beta violaria a própria metodologia. NÃO se reporta beta para o queens. (Mesma família do "sem cross-check confiável no piso de resolução" dos outros, mas aqui atinge o próprio beta.)
- Implicação: sem TLE injusto no optimal → este problema NÃO entra na métrica de redução de TLE injusto; entra na dimensão de SELETIVIDADE.

### Suboptimal — injustiça diferencial pura (NÃO é teste de seletividade)
- Suboptimal = MESMA recursão SEM as podas (coluna/diagonais). Mesmo algoritmo, mesma complexidade, mesma resposta — só a poda removida.
- IMPORTANTE: aqui NÃO há teste de seletividade. O input é fixo 8x8 → "sem poda" muda só a CONSTANTE, não é assintoticamente pior → o C++ suboptimal PASSA. Seletividade pressupõe código a ser REJEITADO; não há alvo. O que a suboptimal mostra é INJUSTIÇA DIFERENCIAL: mesmo código, vereditos diferentes por linguagem.

**CSES suboptimal** — 2026-05-31, dressa (código = repo)
- C++ C++11: ACCEPTED 10/10 (tempos 0,21/0,19/0,13/0,04/0,04/0,03/0,01/0,02/0,01/0,01s; C++ NÃO no piso nos casos grandes).
- Python CPython3: TIME LIMIT EXCEEDED. TLE em {1,2,3,4,5,6} (6/10); AC em {7=0,45s, 8=0,95s, 9=0,20s, 10=0,09s}. Mesmo código do C++, veredito diferente → injustiça diferencial.
- Padrão monótono com o tamanho da árvore de busca (produto de casas livres por linha): Python só estoura nas árvores grandes (≥~1,4×10⁶); ponto de virada ~10⁶ nós (#8=9,4×10⁵ passou no fio).

### Veredito local (tradicional, sem beta)
- Rodado sob limite tradicional 1,0s nas 2 linguagens (beta=1.0; queens não tem beta), reps=1, casos {1,2,3,7,8,10}: C++ AC em todos; Python TLE em {1,2,3} (as 3 maiores árvores), AC em {7,8,10}. Reproduz 3 dos 6 TLE do CSES (máquina local mais rápida; mesmo padrão dos demais). 0 WRONG_ANSWER → equivalência comportamental local confirmada.
- verdict_suboptimal.json: gravado com beta=1.0 só para registrar o veredito tradicional. O campo selectivity_preserved=True ali é VÁCUO (não há beta) — NÃO citar como seletividade.

### Correção adaptativa (conceitual)
- O juiz adaptativo afrouxa só o Python (limite_py = limite_base × beta); o C++ mantém o base. Sob o adaptativo, a mesma suboptimal passaria nas 2 linguagens (justo: mesmo código → mesmo veredito). Não é "deixar passar código ruim" — o C++ de mesma ineficiência também passa; o critério é igual para as duas. Como o queens não tem beta, isto é argumento conceitual, não medição.

=> backtracking/problem01 FECHADO: optimal = controle justo; suboptimal = injustiça diferencial pura (local + CSES). Sem beta (input fixo) e sem eixo de seletividade — por design, justificado.

---

## backtracking/problem02 — Grid Paths (CSES 1625)
- Time limit oficial: 1,00s | Memory limit: 512 MB
- Link: https://cses.fi/problemset/task/1625
- Design backtracking: UM optimal recursivo (DFS de caminho hamiltoniano 7x7, 48 movimentos; 3 podas: dead-end/check, split/trap, parada antecipada no destino), 1 beta. 20 casos. Profundidade fixa = 48 (sem stack issue).
- Input = 1 linha de 48 chars {D,U,L,R,?}; driver de custo = nro de '?' (mais '?' = arvore maior). Caso mais pesado = #11 (48 '?', saida 88418) -> calibracao --case 11.
- NOTA: este problema TEM injustica no OPTIMAL (≠ queens, que e controle). Backtracking com input que escala (via nro de '?') gera disparidade real.
- RETROFIT (31/05): o test_data ANTERIOR estava ERRADO (era copia dos tabuleiros 8x8 do Queens/1624); substituido pelos 20 casos corretos do CSES 1625 (baixados pela usuaria). O errado foi p/ _legacy/test_data_queens_wrong. Suboptimal antiga (EXTRA_WORK=2000 + solution_clean.cpp) -> _legacy/ (estilo abandonado). README+formal_proof+runner reescritos.

### Submissões CSES (auditoria externa) — 2026-05-31, dressa (código = repo)
**C++ optimal RECURSIVO** (C++11)
- Resultado: ACCEPTED 20/20. Tempos: max 0,19s (#11,12,13,14,20). Folgado.
**Python optimal RECURSIVO** (CPython3)
- Resultado: TIME LIMIT EXCEEDED. TLE em {4,6,7,10,11,12,13,14,15,16,20} = 11/20 (55%). AC em {1=0,85s, 2=0,03s, 3=0,56s, 5=0,48s, 8=0,83s, 9=0,11s, 17=0,37s, 18=0,22s, 19=0,03s}.
- INJUSTICA confirmada (no optimal): mesma solucao equivalente, C++ AC 20/20, Python barrado em 11/20. Padrao monotono com o nro de '?' (arvore): os TLE concentram nos casos de muitos '?' (#11=48, #10/12/13/14/15/16/20=47); os AC do Python tem mais letras fixas (arvore menor: #2=39?, #19=40?, #9=42?).
- Os AC do Python ja chegam perto do limite (1=0,85s, 8=0,83s, 3=0,56s) -> borderline; o C++ no pior caso e 0,19s. Gap claro.

### Calibração local (pipeline rigoroso)
- Caso = #11 (48 '?', a árvore mais pesada; --case 11; o seletor por bytes não distingue — todos 49 B).
- **β = 59,46** [56,79 — 60,67] IC95% bootstrap. C++ mediana 0,089s (IQR 5,0%, 15 reps), Python mediana 5,30s (IQR 1,9%, 5 reps). is_reliable=True.
- β alto (~59) coerente com QP3: backtracking recursivo profundo (48 níveis) amplifica a penalidade do Python (overhead de chamada de função no interpretador). Faixa dos β grandes (dp01 rec ~35, Floyd-Warshall ~120).

### Cross-check pipeline vs CSES
- SEM cross-check de β confiável: o C++ no CSES (0,19s no #11) e o local (0,089s) são máquinas diferentes; o Python no CSES deu TLE (sem tempo). Não fabricar razão. β é a medição local controlada.

### Injustiça e correção adaptativa
- Veredito local sob β operacional **59,46s** (20 casos, 3 reps), 0 WRONG_ANSWER:
  - TLE injusto tradicional local (C++ AC + Python TLE @1,0s): **7/20** {7,10,11,12,13,14,20}.
  - Resgatados pelo adaptativo (59,46s): **7/7 = 100%**.
  - Relação com o CSES: o CSES tem 11 TLE {4,6,7,10,11,12,13,14,15,16,20}; o local reproduz 7 deles e perde os 4 borderline {4,6,15,16} (a máquina local é mais rápida — esses ficam < 1,0s aqui). Mesmo padrão dos demais problemas: o veredito local é hardware-dependente e reproduz PARTE do CSES (REGRA #0: o CSES decide a injustiça; o local é ilustrativo). NÃO é match exato.
- Caso COMPLETO de injustiça + correção (≠ queens, que é controle): mesma solução equivalente, C++ AC 20/20; Python TLE em 11/20 no CSES e 7/20 local; o limite adaptativo resgata 100% dos casos locais sem WA.

### Seletividade (fase suboptimal)
- Suboptimal = MESMA recursão SEM as 3 podas de eficiência (check x4 + trap); mantém vis[][] e o goal (6,0) terminal (regra de correção, não poda). Ineficiência algorítmica genuína: sem poda a árvore não corta ramos inviáveis e explode (~O(4^48)).
- CSES suboptimal (2026-05-31, dressa, código = repo): Python TLE → REJEITADA (AC só em {2,19}=0,81s); C++ TLE → REJEITADA (AC só em {2,3,9,19}). Rejeitada nas DUAS linguagens. Contraste com o optimal (C++ AC 20/20): remover as podas quebra o C++ também → é ineficiência algorítmica, não diferença de linguagem.
- SELETIVIDADE LOCAL (sob β operacional 59,46s, reps=1, hard-kill): decisivo #11 (48 '?', já TLE no CSES) = TLE sob 59,46s → submissão NÃO resgatada. Controles {2,19} (os que dão AC no CSES) = AC nas duas linguagens (corretas, só lentas). selectivity_preserved=True, 0 WA. verdict_suboptimal.json gravado.
- Veredito de submissão: TLE no caso decisivo basta → suboptimal rejeitada mesmo sob o limite adaptativo generoso (59,46s). Seletividade preservada.

=> backtracking/problem02 FECHADO nas 4 frentes (CSES optimal + β + veredito optimal + seletividade suboptimal). Caso COMPLETO de injustiça+correção (≠ queens controle).

---

## recursion/problem01 — Tree Distances II (CSES 1133)
- Time limit oficial: 1,00s | Memory limit: 512 MB
- Link: https://cses.fi/problemset/task/1133
- Design recursão profunda: UM optimal recursivo (DFS rerooting, 2 passadas: dfs1 pós-ordem tamanhos+soma de profundidades; dfs2 pré-ordem reroot res[v]=res[u]+(n-cnt[v])-cnt[v]). O(n) tempo, profundidade até n=2×10⁵ (cadeia). 1 beta. 15 casos.
- ESCOLHA do problema (varredura empírica de problemas recursivos de árvore, 31/05): Subordinates (1674, 1 DFS) → Python AC 0,59s (recursão leve demais); Tree Diameter (1131, 2 DFS) → Python AC no fio 0,94s; Tree Distances II (1133, rerooting) → Python TLE. Nem todo recursivo dá TLE; a decisividade depende do trabalho-por-nó + tamanho (QP3). Ver anotacoes_para_artigo.md (seção "Recursão profunda").
- INPUT ESCALA (n até 2×10⁵) → beta CALIBRÁVEL (≠ backtracking de tabuleiro fixo).
- FENÔMENO DE PILHA (recursão profunda, S3.1): os casos #6/#14 (n=200000) fazem o C++ recursivo estourar a pilha default do container (~8MB, segfault) — o CSES usa pilha grande (por isso C++ AC lá). O engine aplica ulimit -s 256MB para reproduzir o CSES (mesmo do dp01). FIX de engine (31/05): o warm-up da calibração não aplicava o ulimit que os trials já usavam → corrigido (benchmark_engine.py:223; untimed, não afeta medição).

### Submissões CSES (auditoria externa) — 2026-05-31, dressa (código = repo)
**C++ optimal RECURSIVO** (C++11)
- Resultado: ACCEPTED 15/15. Tempos: max 0,22s (#6,#7,#8,#14).
**Python optimal RECURSIVO** (CPython3)
- Resultado: TIME LIMIT EXCEEDED. TLE em {6,7,8,14} (4/15, n=200000); AC nos outros 11 (borderline #9,#10=0,72s, #15=0,69s). setrecursionlimit(300000).
- INJUSTIÇA confirmada: mesma solução, C++ AC 15/15, Python TLE 4/15. Recursão profunda em árvore — overhead de chamada no interpretador.

### Calibração local (pipeline rigoroso)
- Caso = #6 (n=200000, Python-TLE no CSES; --case 6). O seletor por bytes não distingue (vários casos n=200000 com bytes quase iguais; o #9 de maior byte é AC, não TLE).
- **β = 5,97** [5,08 — 6,35] IC95% bootstrap. C++ mediana 0,089s (IQR 13,8%, 5 reps), Python mediana 0,531s (IQR 5,9%, 5 reps). is_reliable=True.
- β BAIXO (~6): o DFS é O(n) linear (pouco trabalho por nó) → gap Python/C++ modesto. Contrasta com os β grandes da DP recursiva (memo, mais trabalho por estado) e do backtracking profundo (grid_paths ~59). QP3: a magnitude depende da intensidade do trabalho, não só de "ser recursivo".

### Cross-check pipeline vs CSES
- SEM cross-check de β confiável: o C++ no CSES (0,22s) e o local (0,089s) são máquinas diferentes; o Python no CSES deu TLE (sem tempo). Não fabricar razão. β é a medição local controlada.

### Injustiça e correção adaptativa
- Veredito local sob β operacional **5,97s** (15 casos, 3 reps), 0 WRONG_ANSWER (equivalência comportamental confirmada — os 15 outputs corretos nas duas linguagens):
  - TLE injusto local: **0/15** (todos AC sob 1,0s, Python E C++).
  - A injustiça é CSES-ONLY: o Python local roda 0,53s < 1,0s no #6 (máquina local mais rápida que a do CSES), então o local não reproduz os 4 TLE do CSES. Mesmo padrão do problem02 grafos / dp02 / dp03 (REGRA #0: o CSES decide a injustiça; o veredito local é hardware-dependente e ilustrativo).
  - O mecanismo adaptativo (β=5,97 → 5,97s) resgataria o Python ONDE a injustiça aparece (CSES / máquina mais lenta); localmente não há o que resgatar (tudo < 1,0s).

### Seletividade (fase suboptimal)
- Suboptimal = variante O(n²): para CADA nó, um DFS recursivo separado somando as distâncias daquele nó a todos os outros (sem o rerooting). Mesma forma recursiva e mesma resposta da optimal, mas O(n²) em vez de O(n) — ineficiência algorítmica GENUÍNA (complexidade pior, não slowdown artificial).
- CSES suboptimal (2026-05-31, dressa, código = repo): Python TLE em {6,7,8,9,10,13,14,15} (8/15); C++ TLE no MESMO conjunto {6,7,8,9,10,13,14,15} (8/15). Rejeitada nas DUAS linguagens (O(n²) com n=2×10⁵ ≈ 4×10¹⁰ ops explode em ambas). AC só nos casos pequenos.
- SELETIVIDADE LOCAL (sob β operacional 5,97s, reps=1, hard-kill): decisivo #6 (n=200000, já TLE no CSES) = TLE sob 5,97s → submissão NÃO resgatada. Controles {1,2,3} = AC nas duas linguagens (corretas, só lentas). selectivity_preserved=True, 0 WA. verdict_suboptimal.json gravado.
- Veredito de submissão: TLE no caso decisivo basta → suboptimal rejeitada mesmo sob o limite adaptativo. Seletividade preservada (o gap O(n²) vs O(n) é grande; o β pequeno de 5,97 não chega perto de resgatar).

=> recursion/problem01 FECHADO nas 4 frentes (CSES optimal + β + veredito optimal + seletividade suboptimal). Injustiça CSES-only (β baixo, DFS O(n) linear); seletividade limpa (suboptimal O(n²) rejeitada nas duas linguagens).

---

## recursion/problem02 — Distinct Colors (CSES 1139)
- Time limit oficial: 1,00s | Memory limit: 512 MB
- Link: https://cses.fi/problemset/task/1139
- Design recursão profunda (perfil DIFERENTE do problem01): UM optimal recursivo = DFS + small-to-large merging de conjuntos de cores por subárvore. O(n log n). Recursão + ESTRUTURA DE DADOS (sets), não rerooting puro. 16 casos. n até 2×10⁵; cores até 1e9.
- ESCOLHA: segundo problema de recursão, escolhido por ser mais complexo que os simples (que davam AC) e por agregar perfil distinto ao problem01. Caso BORDERLINE (ver abaixo) — aceito como ponto legítimo no espectro da injustiça.

### Submissões CSES (auditoria externa) — 2026-05-31, dressa (código = repo)
**C++ optimal RECURSIVO** (C++11)
- Resultado: ACCEPTED 16/16. Tempos: max 0,41s (#10).
**Python optimal RECURSIVO** (CPython3)
- Resultado: TIME LIMIT EXCEEDED. TLE em {6,7,8} (3/16); AC nos outros mas BORDERLINE: #15=1,00s (no limite exato), #9=0,94s, #14=0,85s, #13=0,83s. setrecursionlimit(300000).
- INJUSTIÇA confirmada (C++ AC, Python TLE) porém FRÁGIL/borderline — honesto registrar: menos limpa que o problem01, mas o "borderline" é ele mesmo um dado (faixa onde a injustiça começa a se manifestar). Perfil diferente (recursão + sets).

### Calibração local (pipeline rigoroso)
- Caso = #6 (n=200000; --case 6; também o maior por bytes, 4,5 MB).
- **β = 3,55** [3,09 — 4,02] IC95% bootstrap. C++ mediana 0,160s (IQR 12,2%, 5 reps), Python mediana 0,568s (IQR 9,0%, 5 reps). is_reliable=True.
- β BAIXO (~3,5, ainda menor que o problem01 ~6): o gargalo é parte recursão, parte operações de set; o std::set do C++ (árvore balanceada) também é lento → o C++ não é tão mais rápido → razão menor. Coerente com o borderline do CSES. QP3: β depende da natureza do trabalho, não só de "ser recursivo".

### Cross-check pipeline vs CSES
- SEM cross-check de β confiável (máquinas diferentes; Python TLE no CSES sem tempo). β é a medição local controlada.

### Injustiça e correção adaptativa
- Veredito local sob β operacional **3,55s** (16 casos, 3 reps), 0 WRONG_ANSWER (equivalência comportamental confirmada):
  - TLE injusto local: **0/16** (todos AC sob 1,0s, Python E C++).
  - Injustiça CSES-ONLY: Python local 0,57s < 1,0s no #6 (máquina local mais rápida); o local não reproduz os TLE do CSES. Mesmo padrão do problem01 / grafos / dp (REGRA #0: o CSES decide).

### Seletividade (fase suboptimal)
- Suboptimal = MESMO DFS, mas merge INGÊNUO (sem small-to-large; sempre filho→pai). Mesma resposta da optimal, mas o trabalho de merge não é mais limitado → O(n²) no pior caso (cadeia), vs O(n log n) da optimal. Ineficiência algorítmica genuína (complexidade pior, não slowdown).
- CSES suboptimal (2026-05-31, dressa, código = repo): Python TLE em {6,7,8,9,11,13,14,15} (8/16); C++ TLE no MESMO conjunto {6,7,8,9,11,13,14,15} (8/16). Rejeitada nas DUAS linguagens (O(n²) explode em ambas). AC só nos casos pequenos (#10 borderline: C++ 0,89s / Python 0,98s).
- SELETIVIDADE LOCAL (sob β operacional 3,55s, reps=1, hard-kill): decisivo #6 (n=200000, já TLE no CSES) = TLE sob 3,55s → submissão NÃO resgatada. Controles {1,2} = AC nas duas linguagens (corretas, só lentas). selectivity_preserved=True, 0 WA. verdict_suboptimal.json gravado.
- Veredito de submissão: TLE no caso decisivo basta → suboptimal rejeitada mesmo sob o limite adaptativo. Seletividade preservada (gap O(n²) vs O(n log n); β=3,55 não chega perto de resgatar).

=> recursion/problem02 FECHADO nas 4 frentes (CSES optimal + β + veredito optimal + seletividade suboptimal). Injustiça CSES-only borderline (β=3,55, recursão + sets); seletividade limpa (suboptimal O(n²) rejeitada nas duas linguagens).

### Notas
- Estrutura retrofitada ao canônico (31/05): legado → _legacy/ (README/algorithmic_analysis/experimental_results/CSES_VALIDATION_RESULTS/problem_description/problem_specification antigos; benchmarking antigo; 6 JSONs results; slow_validation; suboptimal antigo estilo `itertools.combinations`). README+formal_proof+runner reescritos no padrão. Optimal e test_data intactos.
- Números do _legacy (Python/C++ ≈12,5x, p<0,001, 90%/100% TLE) = metodologia antiga, NÃO confiar.
