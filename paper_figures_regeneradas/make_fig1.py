#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regera a Figura 1 do artigo (forest plot do fator beta) com as correcoes de
apresentacao, SEM alterar nenhum valor de beta nem o metodo de calculo do IC.

Fonte de dados (canonica, NAO alterada): paper_figures/realworld_summary.json
  -> os beta/IC95 sao LIDOS do JSON (nao hardcoded).
Adaptado de paper_figures/make_figures.py :: fig_forest_beta().

Saidas: paper_figures_regeneradas/fig1_forest_beta.png (>=300 dpi) e .pdf (vetorial).
Rodar: python3 make_fig1.py
"""
import json
import os
from matplotlib import use as mpl_use
mpl_use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, FixedFormatter, LogLocator, NullFormatter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
JSON_PATH = os.path.join(ROOT, "paper_figures", "realworld_summary.json")
OUTDIR = HERE

# --- Tipografia para insercao 1:1 em coluna SBC (~6 in). Fontes ~9-10 pt. ---
plt.rcParams.update({
    "font.size": 9.5,
    "axes.titlesize": 10,
    "axes.labelsize": 9.5,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 8.5,
})
FIG_W = 6.0  # largura final da coluna (~15 cm) para insercao sem reescala

# Paleta sobria por categoria (Okabe-Ito, colorblind-friendly) - MANTIDA do original
CAT_COLOR = {
    "graphs": "#0072B2",
    "dp": "#D55E00",
    "backtracking": "#009E73",
    "recursion": "#CC79A7",
}
CAT_LABEL = {"graphs": "Grafos", "dp": "Prog. dinâmica",
             "backtracking": "Backtracking", "recursion": "Recursão"}
# Forma de marcador distinta por categoria (legibilidade P&B / daltonismo)
CAT_MARKER = {"graphs": "o", "dp": "s", "backtracking": "^", "recursion": "D"}

with open(JSON_PATH, encoding="utf-8") as f:
    RW = json.load(f)["problems"]


def short(prob):
    return f"{prob['name']} ({prob['cses']})"


def fig_forest_beta():
    # ----- monta as linhas (uma por estimativa de beta) a partir do JSON -----
    rows = []
    for pid, prob in RW.items():
        styles = [s for s in prob["styles"] if s["beta"] is not None]
        max_beta = max((s["beta"] for s in styles), default=None)
        for s in prob["styles"]:
            if s["beta"] is None:  # controle (Queens) nao tem beta -> omitido
                continue
            label = short(prob)
            if len(styles) > 1:
                label += f" [{'iter' if s['style'] == 'iterative' else 'rec'}]"
            # operacional = maior beta entre os estilos (limite efetivamente aplicado)
            operational = (len(styles) == 1) or (s["beta"] == max_beta)
            rows.append((label, s["beta"], s["ci95"], prob["category"], operational))
    rows.sort(key=lambda r: r[1])
    n_est = len(rows)
    n_prob_plot = len({r[0].split(" [")[0] for r in rows})

    y = list(range(n_est))
    fig, ax = plt.subplots(figsize=(FIG_W, 0.46 * n_est + 1.7),
                           constrained_layout=True)

    for i, (label, beta, ci, cat, operational) in zip(y, rows):
        lo, hi = ci
        color = CAT_COLOR[cat]
        # IC desenhado ANTES do marcador (zorder menor) + caps espessos p/ IC estreito
        ax.errorbar(beta, i, xerr=[[beta - lo], [hi - beta]], fmt="none",
                    ecolor=color, elinewidth=1.9, capsize=3.2, capthick=1.5,
                    alpha=0.95, zorder=2)
        # marcador: forma=categoria; preenchido=operacional, vazado=nao-operacional
        ax.scatter(beta, i, marker=CAT_MARKER[cat], s=40,
                   facecolors=(color if operational else "white"),
                   edgecolors=color, linewidths=1.5, zorder=3)

    # ----- linhas de referencia 2x / 3x (rotulos horizontais, fora das barras) -----
    for mult, ls in [(2, ":"), (3, "--")]:
        ax.axvline(mult, color="0.45", ls=ls, lw=1.1, zorder=1)
    top = n_est - 1
    ax.text(2, top + 0.7, "2× fixo", ha="right", va="bottom",
            color="0.35", fontsize=8)
    ax.text(3, top + 0.7, "3× fixo", ha="left", va="bottom",
            color="0.35", fontsize=8)

    # ----- eixo y -----
    ax.set_yticks(y)
    ax.set_yticklabels([r[0] for r in rows])
    ax.set_ylim(-0.7, top + 1.5)

    # ----- eixo x log: ticks menores + rotulos so em 2,3,10,100 -----
    ax.set_xscale("log")
    ax.set_xlim(1.6, 200)
    major = [2, 3, 10, 100]
    ax.xaxis.set_major_locator(FixedLocator(major))
    ax.xaxis.set_major_formatter(FixedFormatter([str(m) for m in major]))
    ax.xaxis.set_minor_locator(
        LogLocator(base=10, subs=[2, 3, 4, 5, 6, 7, 8, 9], numticks=100))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis="x", which="minor", length=3)
    ax.tick_params(axis="x", which="major", length=5)

    ax.set_xlabel("Fator de calibração  β = mediana(Python) / mediana(C++)   "
                  "(escala log)")
    # titulo centrado na FIGURA (nao no eixo, que e estreitado pelos rotulos y)
    fig.suptitle(f"Fator β: {n_est} estimativas em {n_prob_plot} problemas "
                 "— IC95%, escala log", fontsize=10)
    ax.grid(axis="x", which="major", ls=":", alpha=0.4)

    # ----- legenda unica no canto inferior direito (zona vazia: betas baixos
    #       ficam a esquerda nas linhas de baixo) - nao cobre barras de IC -----
    cat_handles = [Line2D([0], [0], marker=CAT_MARKER[k], color=c, lw=0,
                          markerfacecolor=c, markeredgecolor=c, markersize=7,
                          label=CAT_LABEL[k])
                   for k, c in CAT_COLOR.items()]
    state_handles = [
        Line2D([0], [0], marker="o", color="0.35", lw=0, markerfacecolor="0.35",
               markeredgecolor="0.35", markersize=7,
               label="preenchido = β operacional (aplicado)"),
        Line2D([0], [0], marker="o", color="0.35", lw=0, markerfacecolor="white",
               markeredgecolor="0.35", markersize=7, markeredgewidth=1.5,
               label="vazado = estilo não-operacional (DP)"),
    ]
    ax.legend(handles=cat_handles + state_handles, loc="lower right",
              framealpha=0.95, borderpad=0.7, labelspacing=0.5)

    fig.savefig(os.path.join(OUTDIR, "fig1_forest_beta.png"), dpi=300)
    fig.savefig(os.path.join(OUTDIR, "fig1_forest_beta.pdf"))
    plt.close(fig)
    return n_est, n_prob_plot


if __name__ == "__main__":
    n_est, n_prob = fig_forest_beta()
    print("fig1_forest_beta.png / .pdf gerados em paper_figures_regeneradas/")
    print(f"contagem plotada: {n_est} estimativas em {n_prob} problemas")
