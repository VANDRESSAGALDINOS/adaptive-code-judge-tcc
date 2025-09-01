import sys

MOD = 1000000007
EXTRA_WORK = 200  # Overhead intencional para garantir TLE

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    
    n = int(next(it))
    x = int(next(it))
    
    coins = []
    for _ in range(n):
        coins.append(int(next(it)))
    
    # DP iterativo bottom-up com overhead intencional
    dp = [0] * (x + 1)
    dp[0] = 1  # Caso base: uma maneira de formar soma 0
    
    # Para cada soma possível de 1 até x
    for sum_val in range(1, x + 1):
        # Tentar usar cada moeda
        for coin in coins:
            if sum_val >= coin:
                dp[sum_val] = (dp[sum_val] + dp[sum_val - coin]) % MOD
                
                # OVERHEAD INTENCIONAL - trabalho desnecessário
                waste = 0
                for k in range(EXTRA_WORK):
                    waste += k * k
    
    print(dp[x])

if __name__ == "__main__":
    main()




