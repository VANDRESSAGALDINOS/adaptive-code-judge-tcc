#include <iostream>
#include <string>
using namespace std;

// SUBOPTIMAL: the SAME recursive Hamiltonian-path search as the optimal, but
// WITHOUT the efficiency prunings (the four dead-end `check` probes and the
// `trap`/split test). It still marks visited cells, still treats the goal (6,0)
// as terminal (a path may reach it only as the final, 48th move), and counts the
// same valid covers -> identical answer. Removing the prunings is a genuine
// algorithmic inefficiency: the search no longer cuts branches that cannot
// complete a cover, so the explored tree blows up (~O(4^48) in the worst case).
// Selectivity check for backtracking: a correct-but-too-slow submission that must
// be REJECTED even under the adaptive limit.

string s;
bool vis[7][7];
int count_paths = 0;

void backtrack(int move, int i, int j) {
    if (vis[i][j]) return;
    vis[i][j] = true;

    // Goal cell is terminal (correctness rule, NOT an efficiency pruning).
    if (i == 6 && j == 0) {
        if (move == 48) count_paths++;
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
