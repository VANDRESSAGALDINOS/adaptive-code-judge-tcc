s = ""
vis = [[False] * 7 for _ in range(7)]
count_paths = 0

def check(i, j):
    if vis[i][j]:
        return False
    
    neighbors = 0
    if i-1 >= 0 and not vis[i-1][j]:
        neighbors += 1
    if i+1 < 7 and not vis[i+1][j]:
        neighbors += 1
    if j-1 >= 0 and not vis[i][j-1]:
        neighbors += 1
    if j+1 < 7 and not vis[i][j+1]:
        neighbors += 1
    
    if i == 6 and j == 0 and neighbors > 0:
        return False
    
    if neighbors < 2:
        return True
    
    return False

def trap(i, j):
    x = 0
    y = 0
    
    if i-1 >= 0 and not vis[i-1][j]:
        y += 1
    if i+1 < 7 and not vis[i+1][j]:
        y += 1
    if j-1 >= 0 and not vis[i][j-1]:
        x += 1
    if j+1 < 7 and not vis[i][j+1]:
        x += 1
    
    if (x == 0 and y == 2) or (x == 2 and y == 0):
        return True
    
    return False

def backtrack(move, i, j):
    global count_paths
    
    if vis[i][j]:
        return
    
    vis[i][j] = True
    
    pruning_flags = 0
    
    if i == 6 and j == 0:
        if move == 48:
            count_paths += 1
        else:
            vis[i][j] = False
            pruning_flags += 1
    
    if i-1 >= 0 and j-1 >= 0:
        pruning_flags += check(i-1, j-1)
    if i-1 >= 0 and j+1 < 7:
        pruning_flags += check(i-1, j+1)
    if i+1 < 7 and j+1 < 7:
        pruning_flags += check(i+1, j+1)
    if i+1 < 7 and j-1 >= 0:
        pruning_flags += check(i+1, j-1)
    
    pruning_flags += trap(i, j)
    
    if pruning_flags != 0:
        vis[i][j] = False
        return
    
    if move < 48:
        if s[move] == '?':
            if i-1 >= 0:
                backtrack(move+1, i-1, j)
            if i+1 < 7:
                backtrack(move+1, i+1, j)
            if j-1 >= 0:
                backtrack(move+1, i, j-1)
            if j+1 < 7:
                backtrack(move+1, i, j+1)
        else:
            if s[move] == 'L' and j-1 >= 0:
                backtrack(move+1, i, j-1)
            elif s[move] == 'R' and j+1 < 7:
                backtrack(move+1, i, j+1)
            elif s[move] == 'U' and i-1 >= 0:
                backtrack(move+1, i-1, j)
            elif s[move] == 'D' and i+1 < 7:
                backtrack(move+1, i+1, j)
    
    vis[i][j] = False

def main():
    global s
    s = input().strip()
    backtrack(0, 0, 0)
    print(count_paths)

if __name__ == "__main__":
    main()
