| Classe | Natureza (operação) | β (IC95%) |
|---|---|---|
| O(1) | aritmética básica (piso de overhead) | 4.3 [4.0-4.5] |
| O(log n) | busca binária (piso de overhead) | 4.1 [3.8-4.4] |
| O(n) | soma de array (varredura linear) | 3.9 [3.8-4.1] |
| O(n^2) | soma de matriz (laço duplo) | 4.5 [4.2-4.6] |
| O(n^3) | multiplicação de matrizes (laço numérico denso) | 77.2 [76.2-79.3] |
| O(2^n) | recursão exaustiva (subset-sum) | 33.8 [33.5-34.3] |

> **Nota (para lembrar): β é por NATUREZA da operação/problema, não pela ordem de complexidade.**
>
> β não mede a ordem de complexidade — mede a penalidade do Python para o TIPO de operação,
> no input escolhido:
>
> - O(n^3) aqui = multiplicação de matrizes: laço numérico denso (multiply-add). É o pior caso
>   pro Python (overhead de interpretador por operação, sem vetorização) vs C++ -O2
>   (SIMD/registrador) → gap enorme, β=77.
> - O(2^n) aqui = recursão (subset-sum): o Python sofre na chamada de função, mas o C++ também
>   paga overhead de chamada → gap menor, β=34.
> - Ou seja: laço numérico penaliza o Python MAIS que recursão. Bate com o real-world
>   (Floyd-Warshall compute-bound ~120 ≫ recursão). É QP3: β depende da NATUREZA do
>   problema/entrada, não da ordem.
>
> Cada classe usa input dimensionado por si (regra 10:1, S3.2); β é a razão Python/C++ DENTRO
> de cada classe — não comparável como tempo absoluto entre classes.
