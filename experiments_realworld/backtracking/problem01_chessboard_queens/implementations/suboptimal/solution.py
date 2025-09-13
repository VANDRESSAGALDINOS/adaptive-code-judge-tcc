import sys
from itertools import combinations

def main():
    board = [sys.stdin.readline().strip() for _ in range(8)]
    
    free_cells = []
    for r in range(8):
        for c in range(8):
            if board[r][c] == '.':
                free_cells.append((r, c))
    
    if len(free_cells) < 8:
        print(0)
        return
    
    ans = 0
    
    for positions in combinations(free_cells, 8):
        valid = True
        for i in range(8):
            for j in range(i + 1, 8):
                r1, c1 = positions[i]
                r2, c2 = positions[j]
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