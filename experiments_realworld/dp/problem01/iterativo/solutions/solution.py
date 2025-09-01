import sys

MOD = 1000000007

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    
    n = int(next(it))
    x = int(next(it))
    
    coins = []
    for _ in range(n):
        coins.append(int(next(it)))
    
    # DP iterativo bottom-up
    dp = [0] * (x + 1)
    dp[0] = 1  # Caso base: uma maneira de formar soma 0
    
    # Para cada soma possível de 1 até x
    for sum_val in range(1, x + 1):
        # Tentar usar cada moeda
        for coin in coins:
            if sum_val >= coin:
                dp[sum_val] = (dp[sum_val] + dp[sum_val - coin]) % MOD
    
    print(dp[x])

if __name__ == "__main__":
    main()




