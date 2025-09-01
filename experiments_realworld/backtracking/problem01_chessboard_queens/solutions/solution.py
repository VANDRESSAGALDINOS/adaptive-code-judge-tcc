import sys

def main():
    board = [sys.stdin.readline().strip() for _ in range(8)]

    ans = 0
    # usaremos máscaras de bits:
    # cols: 8 bits para colunas ocupadas
    # d1: 15 bits para diagonais (r+c)
    # d2: 15 bits para anti-diagonais (r-c+7)
    def dfs(r: int, cols: int, d1: int, d2: int):
        nonlocal ans
        if r == 8:
            ans += 1
            return
        for c in range(8):
            if board[r][c] == '*':
                continue
            bc = 1 << c
            b1 = 1 << (r + c)
            b2 = 1 << (r - c + 7)
            if (cols & bc) or (d1 & b1) or (d2 & b2):
                continue
            dfs(r + 1, cols | bc, d1 | b1, d2 | b2)

    dfs(0, 0, 0, 0)
    print(ans)

if __name__ == "__main__":
    main()