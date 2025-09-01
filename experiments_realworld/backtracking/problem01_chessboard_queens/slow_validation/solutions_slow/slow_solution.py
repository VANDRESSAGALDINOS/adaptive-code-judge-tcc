import sys
from itertools import combinations

def main():
    board = [sys.stdin.readline().strip() for _ in range(8)]
    
    # Lista todas as casas livres ('.')
    free_cells = []
    for r in range(8):
        for c in range(8):
            if board[r][c] == '.':
                free_cells.append((r, c))
    
    if len(free_cells) < 8:
        print(0)
        return
    
    ans = 0
    
    # Gera todas as combinações de 8 casas livres (complexidade monstruosa)
    for positions in combinations(free_cells, 8):
        # Verifica se é uma configuração válida de rainhas
        valid = True
        for i in range(8):
            for j in range(i + 1, 8):
                r1, c1 = positions[i]
                r2, c2 = positions[j]
                # Mesma linha, coluna ou diagonal
                if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                    valid = False
                    break
            if not valid:
                break
        
        if valid:
            ans += 1
    
    print(ans)

if __name__ == "__main__":
    main()