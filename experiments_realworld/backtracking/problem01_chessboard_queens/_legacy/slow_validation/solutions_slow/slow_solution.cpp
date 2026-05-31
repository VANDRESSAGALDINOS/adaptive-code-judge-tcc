#include <bits/stdc++.h>
using namespace std;

static inline pair<int,int> rc(int idx) {
    return {idx / 8, idx % 8};
}

bool is_valid(const array<int,8>& pos) {
    for (int i = 0; i < 8; ++i) {
        auto [ri, ci] = rc(pos[i]);
        for (int j = i + 1; j < 8; ++j) {
            auto [rj, cj] = rc(pos[j]);
            if (ri == rj) return false;
            if (ci == cj) return false;
            if (abs(ri - rj) == abs(ci - cj)) return false;
        }
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<string> g(8);
    for (int i = 0; i < 8; ++i) cin >> g[i];

    vector<int> free_cells;
    free_cells.reserve(64);
    for (int r = 0; r < 8; ++r)
        for (int c = 0; c < 8; ++c)
            if (g[r][c] == '.') free_cells.push_back(r * 8 + c);

    if ((int)free_cells.size() < 8) {
        cout << 0 << "\n";
        return 0;
    }

    unsigned long long ans = 0ULL;
    array<int,8> pick{};
    const int n = (int)free_cells.size();

    function<void(int,int)> gen = [&](int idx, int taken) {
        if (taken == 8) {
            if (is_valid(pick)) ++ans;
            return;
        }
        if (idx == n) return;

        pick[taken] = free_cells[idx];
        gen(idx + 1, taken + 1);

        gen(idx + 1, taken);
    };

    gen(0, 0);
    cout << ans << "\n";
    return 0;
}