import sys

# Grid Paths - CSES 1625
# Python equivalent to the C++ solution that passed

s = ""
vis = [[False] * 7 for _ in range(7)]
c = 0

def check(i, j):
    if vis[i][j]:
        return False
    
    count = 0
    if i-1 >= 0 and not vis[i-1][j]:
        count += 1
    if i+1 < 7 and not vis[i+1][j]:
        count += 1
    if j-1 >= 0 and not vis[i][j-1]:
        count += 1
    if j+1 < 7 and not vis[i][j+1]:
        count += 1
    
    if i == 6 and j == 0 and count > 0:
        return False
    
    if count < 2:
        return True
    
    return False

def trap(i, j):
    x = 0  # horizontal
    y = 0  # vertical
    
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

def rec(mv, i, j):
    global c
    
    if vis[i][j]:
        return
    
    vis[i][j] = True
    
    # diagonals
    f = 0
    
    if i == 6 and j == 0:
        if mv == 48:
            c += 1
        else:
            vis[i][j] = False
            f += 1
    
    if i-1 >= 0 and j-1 >= 0:
        f += check(i-1, j-1)
    if i-1 >= 0 and j+1 < 7:
        f += check(i-1, j+1)
    if i+1 < 7 and j+1 < 7:
        f += check(i+1, j+1)
    if i+1 < 7 and j-1 >= 0:
        f += check(i+1, j-1)
    
    f += trap(i, j)
    
    if f != 0:
        vis[i][j] = False
        return
    
    if mv < 48:
        if s[mv] == '?':
            if i-1 >= 0:
                rec(mv+1, i-1, j)  # up
            if i+1 < 7:
                rec(mv+1, i+1, j)  # down
            if j-1 >= 0:
                rec(mv+1, i, j-1)  # left
            if j+1 < 7:
                rec(mv+1, i, j+1)  # right
        else:
            if s[mv] == 'L' and j-1 >= 0:
                rec(mv+1, i, j-1)
            elif s[mv] == 'R' and j+1 < 7:
                rec(mv+1, i, j+1)
            elif s[mv] == 'U' and i-1 >= 0:
                rec(mv+1, i-1, j)
            elif s[mv] == 'D' and i+1 < 7:
                rec(mv+1, i+1, j)
    
    vis[i][j] = False

def solve():
    global s
    s = input().strip()
    rec(0, 0, 0)
    print(c)

if __name__ == "__main__":
    solve()