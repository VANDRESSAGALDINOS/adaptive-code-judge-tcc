#include <iostream>
#include <string>
using namespace std;

const int EXTRA_WORK = 2000;

string s;
bool vis[7][7];
int count_paths = 0;

bool check(int i, int j) {
    int neighbors = 0;
    if (vis[i][j]) return false;
    if (i-1 >= 0 && !vis[i-1][j]) neighbors++;
    if (i+1 < 7 && !vis[i+1][j]) neighbors++;
    if (j-1 >= 0 && !vis[i][j-1]) neighbors++;
    if (j+1 < 7 && !vis[i][j+1]) neighbors++;
    if (i == 6 && j == 0 && neighbors > 0) return false;
    if (neighbors < 2) return true;
    return false;
}

bool trap(int i, int j) {
    int x = 0, y = 0;
    if (i-1 >= 0 && !vis[i-1][j]) y++;
    if (i+1 < 7 && !vis[i+1][j]) y++;
    if (j-1 >= 0 && !vis[i][j-1]) x++;
    if (j+1 < 7 && !vis[i][j+1]) x++;
    if ((x == 0 && y == 2) || (x == 2 && y == 0)) return true;
    return false;
}

void extra_computational_work() {
    volatile int dummy = 0;
    for (int i = 0; i < EXTRA_WORK; i++) {
        dummy += i * i;
    }
}

void backtrack(int move, int i, int j) {
    extra_computational_work();
    
    if (vis[i][j]) return;
    vis[i][j] = true;
    
    int pruning_flags = 0;
    if (i == 6 && j == 0) {
        if (move == 48) count_paths++;
        else {
            vis[i][j] = false;
            pruning_flags++;
        }
    }
    
    if (i-1 >= 0 && j-1 >= 0) pruning_flags += check(i-1, j-1);
    if (i-1 >= 0 && j+1 < 7) pruning_flags += check(i-1, j+1);
    if (i+1 < 7 && j+1 < 7) pruning_flags += check(i+1, j+1);
    if (i+1 < 7 && j-1 >= 0) pruning_flags += check(i+1, j-1);
    pruning_flags += trap(i, j);
    
    if (pruning_flags != 0) {
        vis[i][j] = false;
        return;
    }
    
    if (move < 48) {
        if (s[move] == '?') {
            if (i-1 >= 0) backtrack(move+1, i-1, j);
            if (i+1 < 7) backtrack(move+1, i+1, j);
            if (j-1 >= 0) backtrack(move+1, i, j-1);
            if (j+1 < 7) backtrack(move+1, i, j+1);
        } else {
            if (s[move] == 'L' && j-1 >= 0) backtrack(move+1, i, j-1);
            else if (s[move] == 'R' && j+1 < 7) backtrack(move+1, i, j+1);
            else if (s[move] == 'U' && i-1 >= 0) backtrack(move+1, i-1, j);
            else if (s[move] == 'D' && i+1 < 7) backtrack(move+1, i+1, j);
        }
    }
    vis[i][j] = false;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    cin >> s;
    backtrack(0, 0, 0);
    cout << count_paths << "\n";
    
    return 0;
}
