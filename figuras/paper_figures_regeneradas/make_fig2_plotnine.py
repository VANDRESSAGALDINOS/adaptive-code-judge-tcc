#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figura 2 (slope chart: fator beta por estilo iterativo vs. recursivo nos
problemas de DP) em PLOTNINE. NAO altera nenhum valor de beta nem o metodo do IC.

Fonte de dados (canonica, NAO alterada): results/realworld_summary.json
  -> beta/IC95 LIDOS do JSON (nada hardcoded).

Decisoes (confirmadas pela usuaria): plotnine (coerencia c/ Fig.1); eixo Y LINEAR;
barras de IC95% em cada ponto; series identificadas por LEGENDA lateral
(cor + traco + marcador, P&B/daltonismo), nao por rotulo nos dois lados; rotulos de
beta junto dos pontos com a colisao 11,1/12,0 resolvida.

Saidas: fig2_dp_iter_vs_rec.png (300 dpi) e fig2_dp_iter_vs_rec.pdf (vetorial).
Rodar: python3 make_fig2_plotnine.py
"""
import json
import os
import warnings
import pandas as pd
from plotnine import (
    ggplot, aes, geom_line, geom_point, geom_errorbar, geom_text,
    scale_x_continuous, scale_color_manual, scale_linetype_manual,
    scale_shape_manual, labs, theme_bw, theme, element_text, element_blank,
    element_line, guides, guide_legend,
)

warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
JSON_PATH = os.path.join(ROOT, "results", "realworld_summary.json")

with open(JSON_PATH, encoding="utf-8") as f:
    RW = json.load(f)["problems"]

# ------------------------------------------------- monta dados (3 DP x 2 estilos)
recs = []
for pid, prob in RW.items():
    if prob["category"] != "dp":
        continue
    label = f"{prob['name']} ({prob['cses']})"
    for s in prob["styles"]:
        recs.append({
            "prob": label,
            "style": "Iterativo" if s["style"] == "iterative" else "Recursivo",
            "x": 0 if s["style"] == "iterative" else 1,
            "beta": s["beta"], "lo": s["ci95"][0], "hi": s["ci95"][1],
        })
df = pd.DataFrame(recs)

# ordem fixa das series (legenda) e estilos distintos P&B-safe
PROB_ORDER = ["Coin Combinations I (1635)", "Grid Paths (1638)", "Two Sets II (1093)"]
COL = {PROB_ORDER[0]: "#0072B2", PROB_ORDER[1]: "#009E73", PROB_ORDER[2]: "#D55E00"}
LT = {PROB_ORDER[0]: "solid", PROB_ORDER[1]: "solid", PROB_ORDER[2]: "solid"}
SH = {PROB_ORDER[0]: "o", PROB_ORDER[1]: "s", PROB_ORDER[2]: "^"}
df["prob"] = pd.Categorical(df["prob"], categories=PROB_ORDER, ordered=True)


def declutter(pairs, min_gap):
    """Empurra para cima rotulos cujo y fica a menos de min_gap do anterior."""
    out, last = {}, -1e9
    for key, y in sorted(pairs, key=lambda t: t[1]):
        ly = max(y, last + min_gap)
        out[key] = ly
        last = ly
    return out


def fmt(b):
    return f"{b:.1f}".replace(".", ",")


# rotulos de beta: iterativo a ESQUERDA dos pontos, recursivo a DIREITA.
# colisao do lado iterativo (Coin 11,1 e Grid 12,0) resolvida com declutter.
lab_rows = []
for side, x0, xt, ha in [("Iterativo", 0, -0.04, "right"),
                         ("Recursivo", 1, 1.04, "left")]:
    sub = df[df["x"] == x0]
    yt = declutter(list(zip(sub["prob"], sub["beta"])), min_gap=3.0)
    for _, r in sub.iterrows():
        lab_rows.append({"xt": xt, "yt": yt[r["prob"]], "lab": fmt(r["beta"]),
                         "ha": ha})
lab_iter = pd.DataFrame([r for r in lab_rows if r["ha"] == "right"])
lab_rec = pd.DataFrame([r for r in lab_rows if r["ha"] == "left"])

# -------------------------------------------------------------------- plot
p = (
    ggplot(df, aes(x="x", y="beta", group="prob"))
    + geom_line(aes(color="prob", linetype="prob"), size=0.8)
    + geom_errorbar(aes(ymin="lo", ymax="hi", color="prob"),
                    width=0.05, size=0.6, show_legend=False)
    + geom_point(aes(color="prob", shape="prob"), size=2.8)
    + geom_text(lab_iter, aes(x="xt", y="yt", label="lab"), ha="right",
                size=8, color="#595959")
    + geom_text(lab_rec, aes(x="xt", y="yt", label="lab"), ha="left",
                size=8, color="#595959")
    + scale_color_manual(values=[COL[p_] for p_ in PROB_ORDER], name="Problema")
    + scale_linetype_manual(values=[LT[p_] for p_ in PROB_ORDER], name="Problema")
    + scale_shape_manual(values=[SH[p_] for p_ in PROB_ORDER], name="Problema")
    + scale_x_continuous(breaks=[0, 1], labels=["Iterativo", "Recursivo"],
                         limits=(-0.45, 1.55), expand=(0, 0))
    + labs(
        x="",
        y="Fator de calibração β",
        title="Fator β por estilo de solução (iterativo vs. recursivo)\n"
              "nos problemas de programação dinâmica",
    )
    + guides(color=guide_legend(order=1), linetype=guide_legend(order=1),
             shape=guide_legend(order=1))
    + theme_bw(base_size=9)
    + theme(
        figure_size=(6.0, 4.6),
        plot_title=element_text(size=10, ha="center"),
        axis_text_x=element_text(size=9.5),
        axis_text_y=element_text(size=9),
        axis_title_y=element_text(size=9.5),
        legend_title=element_text(size=8.5),
        legend_text=element_text(size=8),
        legend_key=element_blank(),
        panel_grid_major_x=element_blank(),
        panel_grid_minor_x=element_blank(),
        panel_grid_minor_y=element_blank(),
        panel_grid_major_y=element_line(color="#D9D9D9", size=0.4),
    )
)

png = os.path.join(HERE, "fig2_dp_iter_vs_rec.png")
pdf = os.path.join(HERE, "fig2_dp_iter_vs_rec.pdf")
p.save(png, dpi=300, verbose=False)
p.save(pdf, verbose=False)
print("fig2_dp_iter_vs_rec.png / .pdf gerados em paper_figures_regeneradas/ (plotnine)")
print("betas usados (iter -> rec):")
for pr in PROB_ORDER:
    bi = df[(df.prob == pr) & (df.x == 0)].iloc[0]
    br = df[(df.prob == pr) & (df.x == 1)].iloc[0]
    print(f"  {pr:28s} {bi.beta:5.2f} [{bi.lo:.2f},{bi.hi:.2f}] -> "
          f"{br.beta:5.2f} [{br.lo:.2f},{br.hi:.2f}]")
