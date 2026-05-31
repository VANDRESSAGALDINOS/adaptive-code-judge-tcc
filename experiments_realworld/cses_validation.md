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
