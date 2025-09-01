#include <bits/stdc++.h>
using namespace std;

// Converte índice linear [0..63] para (linha, coluna)
static inline pair<int,int> rc(int idx) {
    return {idx / 8, idx % 8};
}

// Verifica se as 8 posições formam uma configuração válida de rainhas
bool is_valid(const array<int,8>& pos) {
    // checagem O(8^2) bem ingênua (sem podas/flags)
    for (int i = 0; i < 8; ++i) {
        auto [ri, ci] = rc(pos[i]);
        for (int j = i + 1; j < 8; ++j) {
            auto [rj, cj] = rc(pos[j]);
            if (ri == rj) return false;                  // mesma linha
            if (ci == cj) return false;                  // mesma coluna
            if (abs(ri - rj) == abs(ci - cj)) return false; // mesma diagonal
        }
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<string> g(8);
    for (int i = 0; i < 8; ++i) cin >> g[i];

    // Lista **todas** as casas livres ('.'). Não fazemos nenhuma poda por linha/coluna.
    vector<int> free_cells;
    free_cells.reserve(64);
    for (int r = 0; r < 8; ++r)
        for (int c = 0; c < 8; ++c)
            if (g[r][c] == '.') free_cells.push_back(r * 8 + c);

    if ((int)free_cells.size() < 8) {
        cout << 0 << "\n";
        return 0;
    }

    // Gera combinações de tamanho 8 dentre free_cells (complexidade monstruosa).
    // Implementação propositalmente "crua": sem pruning e com cópias.
    unsigned long long ans = 0ULL;
    array<int,8> pick{};
    const int n = (int)free_cells.size();

    function<void(int,int)> gen = [&](int idx, int taken) {
        if (taken == 8) {
            if (is_valid(pick)) ++ans;
            return;
        }
        if (idx == n) return;

        // Escolher a célula atual
        pick[taken] = free_cells[idx];
        gen(idx + 1, taken + 1);

        // Não escolher a célula atual
        gen(idx + 1, taken);
    };

    gen(0, 0);
    cout << ans << "\n";
    return 0;
}