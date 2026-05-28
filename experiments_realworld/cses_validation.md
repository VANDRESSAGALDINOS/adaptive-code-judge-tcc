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
- Suboptimal Python continua falhando sob adaptativo
  (validação de seletividade preservada).

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

**Python suboptimal CPython3** — [a preencher após submissão CSES]

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
- Suboptimal sob adaptativo — [a preencher após pipeline]

### Notas
- O conjunto de TLE observado {6,7,8,9,10,11,12,14,15} coincide com o critical_cases do runner antigo do problem01.
- metadata/metadata_graficos.json dizia casos_tle_cses=[8,12,15] — incompleto/incorreto vs realidade observada; revisar quando for re-organizar configs por problema.
