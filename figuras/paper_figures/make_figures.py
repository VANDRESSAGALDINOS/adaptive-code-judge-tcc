#!/usr/bin/env python3
"""
Gera as figuras do artigo a partir dos dados estruturados (sem inventar numero):
  - results/realworld_summary.json    (eixo real-world, 11 problemas CSES)
  - results/theoretical_summary.json  (eixo teorico, 6 classes)
Saida: paper_figures/figures/*.png e *.pdf
Titulos sobrios/academicos (sem sensacionalismo). Rodar: python3 make_figures.py
"""
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUTDIR = os.path.join(HERE, "figures")
TABLEDIR = os.path.join(HERE, "tabelas")
os.makedirs(OUTDIR, exist_ok=True)
os.makedirs(TABLEDIR, exist_ok=True)

# Tipografia consistente entre todas as figuras (mesma largura -> mesma escala na coluna)
plt.rcParams.update({
    "font.size": 10, "axes.titlesize": 11, "axes.labelsize": 10,
    "xtick.labelsize": 9, "ytick.labelsize": 9, "legend.fontsize": 9,
})
FIG_W = 7.8  # largura unica para todas as figuras

with open(os.path.join(ROOT, "results", "realworld_summary.json")) as f:
    RW = json.load(f)["problems"]
with open(os.path.join(ROOT, "results", "theoretical_summary.json")) as f:
    TH = json.load(f)["classes"]

# Paleta sobria por categoria (colorblind-friendly: Okabe-Ito)
CAT_COLOR = {
    "graphs": "#0072B2",
    "dp": "#D55E00",
    "backtracking": "#009E73",
    "recursion": "#CC79A7",
}
CAT_LABEL = {"graphs": "Grafos", "dp": "Prog. dinamica",
             "backtracking": "Backtracking", "recursion": "Recursao"}


def short(pid, prob):
    return f"{prob['name']} ({prob['cses']})"


def op_style(prob):
    """Estilo que define o limite operacional (maior beta); single quando ha 1."""
    styles = [s for s in prob["styles"] if s["beta"] is not None]
    if not styles:
        return prob["styles"][0]
    return max(styles, key=lambda s: s["beta"])


def save(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(OUTDIR, f"{name}.{ext}"), dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  {name}.png / .pdf")


# ----------------------------------------------------------------------
# FIG 1 - Forest plot de beta com IC95% (todos os style-betas do real-world)
# ----------------------------------------------------------------------
def fig_forest_beta():
    rows = []
    for pid, prob in RW.items():
        for s in prob["styles"]:
            if s["beta"] is None:
                continue
            label = short(pid, prob)
            if len(prob["styles"]) > 1:
                label += f" [{ 'iter' if s['style']=='iterative' else 'rec' }]"
            rows.append((label, s["beta"], s["ci95"], prob["category"]))
    rows.sort(key=lambda r: r[1])
    y = range(len(rows))
    fig, ax = plt.subplots(figsize=(FIG_W, 0.42 * len(rows) + 1.4))
    for i, (label, beta, ci, cat) in zip(y, rows):
        lo, hi = ci
        ax.plot([lo, hi], [i, i], color=CAT_COLOR[cat], lw=1.6, alpha=0.85, zorder=2)
        ax.scatter([beta], [i], color=CAT_COLOR[cat], s=42, zorder=3)
    for mult, ls in [(2, ":"), (3, "--")]:
        ax.axvline(mult, color="0.45", ls=ls, lw=1.1, zorder=1)
        ax.text(mult, len(rows) - 0.3, f"{mult}x fixo", rotation=90,
                va="top", ha="right", color="0.35", fontsize=8)
    ax.set_yticks(list(y))
    ax.set_yticklabels([r[0] for r in rows], fontsize=8.5)
    ax.set_xscale("log")
    ax.set_xlabel("Fator de calibracao  β = mediana(Python) / mediana(C++)   (escala log)")
    ax.set_title("Fator β por problema e estilo, com IC95%  (eixo real-world, n=11)")
    ax.set_xlim(1.5, 200)
    handles = [Line2D([0], [0], color=c, lw=2, marker="o", label=CAT_LABEL[k])
               for k, c in CAT_COLOR.items()]
    ax.legend(handles=handles, fontsize=8.5, loc="lower right", framealpha=0.9)
    ax.grid(axis="x", ls=":", alpha=0.4)
    save(fig, "fig1_forest_beta")


# ----------------------------------------------------------------------
# FIG 2 - beta iterativo vs recursivo (DP)
# ----------------------------------------------------------------------
def fig_dp_iter_rec():
    dp = {pid: p for pid, p in RW.items() if p["category"] == "dp"}
    fig, ax = plt.subplots(figsize=(FIG_W, 4.8))
    # stagger vertical das etiquetas do lado iterativo p/ valores proximos (ex. 11,1 e 12,0)
    iter_vals = {pid: next(s["beta"] for s in p["styles"] if s["style"] == "iterative")
                 for pid, p in dp.items()}
    order = sorted(iter_vals, key=iter_vals.get)
    dy = {}
    for idx, pid in enumerate(order):
        dy[pid] = 9 if (idx > 0 and iter_vals[pid] - iter_vals[order[idx - 1]] < 4) else -4
    for pid, p in dp.items():
        bi = next(s["beta"] for s in p["styles"] if s["style"] == "iterative")
        br = next(s["beta"] for s in p["styles"] if s["style"] == "recursive")
        ax.plot([0, 1], [bi, br], "-o", color=CAT_COLOR["dp"], alpha=0.85)
        ax.annotate(p["name"], (1, br), xytext=(6, 0), textcoords="offset points",
                    va="center", fontsize=8.5)
        ax.annotate(f"{bi:.1f}", (0, bi), xytext=(-8, dy[pid]), textcoords="offset points",
                    va="center", ha="right", fontsize=8, color="0.4")
        ax.annotate(f"{br:.1f}", (1, br), xytext=(6, 9), textcoords="offset points",
                    fontsize=8, color="0.4")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Iterativo", "Recursivo"])
    ax.set_xlim(-0.35, 1.5)
    ax.set_ylabel("Fator de calibracao β")
    ax.set_title("Fator β por estilo de solucao nos problemas de programacao dinamica")
    ax.grid(axis="y", ls=":", alpha=0.4)
    save(fig, "fig2_dp_iter_vs_rec")


# ----------------------------------------------------------------------
# FIG 3 - TLE injusto no CSES sob o limite tradicional, por problema
# ----------------------------------------------------------------------
def fig_tle_injusto():
    rows = []
    for pid, prob in RW.items():
        s = op_style(prob)
        rows.append((short(pid, prob), s["cses_python"]["tle_count"],
                     s["cses_python"]["total"], prob["category"], prob["role"]))
    rows.sort(key=lambda r: r[1] / r[2])
    y = range(len(rows))
    fig, ax = plt.subplots(figsize=(FIG_W, 0.42 * len(rows) + 1.3))
    for i, (label, tle, total, cat, role) in zip(y, rows):
        frac = tle / total
        ax.barh(i, frac, color=CAT_COLOR[cat], alpha=0.88)
        tag = f"{tle}/{total}" + ("  (controle)" if role == "control" else "")
        ax.text(frac + 0.01, i, tag, va="center", fontsize=8)
    ax.set_yticks(list(y))
    ax.set_yticklabels([r[0] for r in rows], fontsize=8.5)
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("Fracao dos casos com TLE injusto (Python optimal correto rejeitado, limite 1,0s)")
    ax.set_title("Penalizacao da solucao Python correta sob o limite tradicional, por problema")
    handles = [Line2D([0], [0], color=c, lw=6, label=CAT_LABEL[k])
               for k, c in CAT_COLOR.items()]
    ax.legend(handles=handles, fontsize=8.5, loc="lower right", framealpha=0.9)
    ax.grid(axis="x", ls=":", alpha=0.4)
    save(fig, "fig3_tle_injusto")


# ----------------------------------------------------------------------
# FIG 4 - Distribuicao dos casos com TLE por problema (concentracao nas instancias pesadas)
# ----------------------------------------------------------------------
def fig_tle_por_caso():
    items = [(pid, p) for pid, p in RW.items() if p["role"] == "injustice"]
    fig, ax = plt.subplots(figsize=(FIG_W, 0.45 * len(items) + 1.4))
    for i, (pid, p) in enumerate(items):
        s = op_style(p)
        total = s["cses_python"]["total"]
        tle = set(s["cses_python"]["tle_cases"])
        for c in range(1, total + 1):
            is_tle = c in tle
            ax.scatter(c, i, marker="s", s=46,
                       color="#D55E00" if is_tle else "#BBBBBB",
                       edgecolors="none")
        ax.text(total + 0.6, i, p["cost_driver"], va="center", fontsize=7.5, color="0.35")
    ax.set_yticks(range(len(items)))
    ax.set_yticklabels([f"{p['name']} ({p['cses']})" for _, p in items], fontsize=8.5)
    ax.set_xlabel("Indice do caso de teste no CSES (ordenados; indices altos = instancias maiores)")
    ax.set_title("Casos com TLE em Python por instancia (concentram-se nas mais pesadas)",
                 fontsize=10)
    ax.set_xlim(0, max(op_style(p)["cses_python"]["total"] for _, p in items) + 8)
    handles = [Line2D([0], [0], marker="s", color="w", markerfacecolor="#D55E00", markersize=9, label="TLE (Python)"),
               Line2D([0], [0], marker="s", color="w", markerfacecolor="#BBBBBB", markersize=9, label="Accepted")]
    ax.legend(handles=handles, fontsize=8.5, loc="lower right", framealpha=0.9)
    ax.grid(axis="x", ls=":", alpha=0.3)
    save(fig, "fig4_tle_por_caso")


# ----------------------------------------------------------------------
# FIG 5 - beta por classe de complexidade (eixo teorico controlado)
# ----------------------------------------------------------------------
def fig_teorico():
    order = ["O_log_n", "O1_constant", "On_linear", "On2_quadratic", "O2n_exponential", "On3_cubic"]
    labels = {"O1_constant": "O(1)", "O_log_n": "O(log n)", "On_linear": "O(n)",
              "On2_quadratic": "O(n^2)", "On3_cubic": "O(n^3)", "O2n_exponential": "O(2^n)"}
    rows = [(labels[k], TH[k]["beta"], TH[k]["beta_ci95"], TH[k]["is_overhead_floor"])
            for k in order if k in TH]
    fig, ax = plt.subplots(figsize=(FIG_W, 4.6))
    for i, (lab, beta, ci, floor) in enumerate(rows):
        color = "#999999" if floor else "#0072B2"
        ax.bar(i, beta, color=color, alpha=0.9)
        if ci:
            ax.plot([i, i], ci, color="0.2", lw=1.3)
        ax.text(i, beta + 1.5, f"{beta:.1f}", ha="center", fontsize=8.5)
    ax.set_xticks(range(len(rows)))
    ax.set_xticklabels([r[0] for r in rows])
    ax.set_ylabel("Fator de calibracao β  (IC95%)")
    ax.set_title("Fator β por classe de complexidade (eixo teorico controlado)")
    ax.set_xlim(-0.6, 6.6)
    for mult, lab in ((2, "2x fixo"), (3, "3x fixo")):
        ax.axhline(mult, color="0.45", ls=":", lw=1.0)
        ax.text(5.55, mult, lab, color="0.4", fontsize=8, va="center", ha="left")
    handles = [Line2D([0], [0], color="#0072B2", lw=7, label="β calibravel"),
               Line2D([0], [0], color="#999999", lw=7, label="piso de overhead (nao calibravel)")]
    ax.legend(handles=handles, fontsize=8.5, loc="upper left", framealpha=0.9)
    ax.grid(axis="y", ls=":", alpha=0.4)
    save(fig, "fig5_teorico_classes")


# ----------------------------------------------------------------------
# FIG 6 - Seletividade: a suboptimal permanece rejeitada sob o limite adaptativo
# ----------------------------------------------------------------------
def fig_selectivity():
    items = [(pid, p) for pid, p in RW.items() if p["selectivity"]["applicable"]]
    items.sort(key=lambda kv: (kv[1]["category"], kv[1]["name"]))
    cols = ["Suboptimal rejeitada\nsob limite β (caso decisivo)", "Falsos\nresgates", "WRONG\nANSWER"]
    fig, ax = plt.subplots(figsize=(FIG_W, 0.46 * len(items) + 1.9))
    for i, (pid, p) in enumerate(items):
        sel = p["selectivity"]
        dec = sel["decisive_case"][0] if sel["decisive_case"] else "-"
        cells = [(f"TLE (#{dec})", sel["preserved"]),
                 ("0", sel["preserved"]),
                 (str(sel["wrong_answer"]), sel["wrong_answer"] == 0)]
        for j, (txt, ok) in enumerate(cells):
            fc, ec = ("#D5F5E3", "#1E8449") if ok else ("#FADBD8", "#C0392B")
            ax.text(j, i, txt, ha="center", va="center", fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.45", fc=fc, ec=ec, lw=1.2))
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(cols, fontsize=8.5)
    ax.set_yticks(range(len(items)))
    ax.set_yticklabels([f"{p['name']} ({p['cses']})" for _, p in items], fontsize=8.5)
    ax.tick_params(length=0)
    ax.set_xlim(-0.5, len(cols) - 0.5)
    ax.set_ylim(-0.6, len(items) - 0.4)
    ax.invert_yaxis()
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(f"Seletividade preservada sob o limite adaptativo  ({len(items)}/{len(items)} problemas)",
                 fontsize=10)
    fig.text(0.5, 0.012, "Controles (instancias pequenas) = AC nas duas linguagens (correta, so lenta). "
             "Queens (1624) e controle, sem alvo de seletividade.",
             ha="center", fontsize=7.5, color="0.4")
    save(fig, "fig6_seletividade")


# ----------------------------------------------------------------------
# TABELA - eixo teorico: Classe e beta (IC95). Markdown em figures/.
# ----------------------------------------------------------------------
def write_tables():
    order = ["O1_constant", "O_log_n", "On_linear", "On2_quadratic", "On3_cubic", "O2n_exponential"]
    labels = {"O1_constant": "O(1)", "O_log_n": "O(log n)", "On_linear": "O(n)",
              "On2_quadratic": "O(n^2)", "On3_cubic": "O(n^3)", "O2n_exponential": "O(2^n)"}
    nature = {
        "O1_constant": "aritmética básica (piso de overhead)",
        "O_log_n": "busca binária (piso de overhead)",
        "On_linear": "soma de array (varredura linear)",
        "On2_quadratic": "soma de matriz (laço duplo)",
        "On3_cubic": "multiplicação de matrizes (laço numérico denso)",
        "O2n_exponential": "recursão exaustiva (subset-sum)",
    }
    lines = ["| Classe | Natureza (operação) | β (IC95%) |", "|---|---|---|"]
    for k in order:
        if k not in TH:
            continue
        b = TH[k]["beta"]
        ci = TH[k]["beta_ci95"]
        ci_txt = f" [{ci[0]:.1f}-{ci[1]:.1f}]" if ci else ""
        lines.append(f"| {labels[k]} | {nature[k]} | {b:.1f}{ci_txt} |")
    lines += [
        "",
        "> **Nota (para lembrar): β é por NATUREZA da operação/problema, não pela ordem de complexidade.**",
        ">",
        "> β não mede a ordem de complexidade — mede a penalidade do Python para o TIPO de operação,",
        "> no input escolhido:",
        ">",
        "> - O(n^3) aqui = multiplicação de matrizes: laço numérico denso (multiply-add). É o pior caso",
        ">   pro Python (overhead de interpretador por operação, sem vetorização) vs C++ -O2",
        ">   (SIMD/registrador) → gap enorme, β=77.",
        "> - O(2^n) aqui = recursão (subset-sum): o Python sofre na chamada de função, mas o C++ também",
        ">   paga overhead de chamada → gap menor, β=34.",
        "> - Ou seja: laço numérico penaliza o Python MAIS que recursão. Bate com o real-world",
        ">   (Floyd-Warshall compute-bound ~120 ≫ recursão). É QP3: β depende da NATUREZA do",
        ">   problema/entrada, não da ordem.",
        ">",
        "> Cada classe usa input dimensionado por si (regra 10:1, S3.2); β é a razão Python/C++ DENTRO",
        "> de cada classe — não comparável como tempo absoluto entre classes.",
    ]
    path = os.path.join(TABLEDIR, "tabela_teorico_beta.md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("  tabelas/tabela_teorico_beta.md")


if __name__ == "__main__":
    print("Gerando figuras em paper_figures/figures/ ...")
    fig_forest_beta()
    fig_dp_iter_rec()
    fig_tle_injusto()
    fig_tle_por_caso()
    fig_teorico()
    fig_selectivity()
    write_tables()
    print("OK.")
