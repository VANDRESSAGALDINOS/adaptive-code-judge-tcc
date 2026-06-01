#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figura 1 (forest plot do fator beta) em PLOTNINE (gramatica de graficos, ggplot2).
NAO altera nenhum valor de beta nem o metodo do IC - so apresentacao.

Fonte de dados (canonica, NAO alterada): paper_figures/realworld_summary.json
  -> beta/IC95 LIDOS do JSON (nada hardcoded).

Estilo: forest plot limpo. IC = linha + caps FINOS atras do ponto. Categoria =
cor + forma (P&B/daltonismo). beta operacional (limite aplicado) = ponto OPACO;
estilo nao-operacional (DP) = ponto ESMAECIDO (alpha menor) - le como secundario,
nao como "caixa vazia".

Saidas: fig1_forest_beta.png (300 dpi) e fig1_forest_beta.pdf (vetorial).
Rodar: python3 make_fig1_plotnine.py
"""
import json
import os
import warnings
import pandas as pd
from plotnine import (
    ggplot, aes, geom_segment, geom_point, geom_vline, annotate,
    scale_x_log10, scale_color_manual, scale_alpha_manual,
    scale_y_discrete, labs, theme_bw, theme,
    element_text, element_blank, element_line, guides, guide_legend,
)

warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
JSON_PATH = os.path.join(ROOT, "paper_figures", "realworld_summary.json")

# Paleta Okabe-Ito (colorblind-friendly) - MANTIDA do original
CAT_COLOR = {"graphs": "#0072B2", "dp": "#D55E00",
             "backtracking": "#009E73", "recursion": "#CC79A7"}
CAT_LABEL = {"graphs": "Grafos", "dp": "Prog. dinâmica",
             "backtracking": "Backtracking", "recursion": "Recursão"}
# formas fillable distintas por categoria
CAT_SHAPE = {"graphs": "o", "dp": "s", "backtracking": "^", "recursion": "D"}
CAT_ORDER = ["graphs", "dp", "backtracking", "recursion"]

with open(JSON_PATH, encoding="utf-8") as f:
    RW = json.load(f)["problems"]

# ---------------------------------------------------------------- monta dados
recs = []
for pid, prob in RW.items():
    styles = [s for s in prob["styles"] if s["beta"] is not None]
    max_beta = max((s["beta"] for s in styles), default=None)
    for s in prob["styles"]:
        if s["beta"] is None:        # controle (Queens): sem beta -> omitido
            continue
        label = f"{prob['name']} ({prob['cses']})"
        if len(styles) > 1:
            label += f" [{'iter' if s['style'] == 'iterative' else 'rec'}]"
        recs.append({
            "label": label,
            "beta": s["beta"], "lo": s["ci95"][0], "hi": s["ci95"][1],
            "cat": prob["category"],
            "cat_label": CAT_LABEL[prob["category"]],
            "operational": (len(styles) == 1) or (s["beta"] == max_beta),
        })

df = pd.DataFrame(recs).sort_values("beta").reset_index(drop=True)
n_est = len(df)
n_prob = df["label"].str.replace(r" \[.*\]$", "", regex=True).nunique()

# ordem do eixo y = beta crescente (menor embaixo)
df["label"] = pd.Categorical(df["label"], categories=list(df["label"]), ordered=True)
df["cat_label"] = pd.Categorical(df["cat_label"],
                                 categories=[CAT_LABEL[c] for c in CAT_ORDER],
                                 ordered=True)
df["op_label"] = df["operational"].map(
    {True: "β operacional (aplicado)", False: "estilo não-operacional (DP)"})
df["op_label"] = pd.Categorical(
    df["op_label"],
    categories=["β operacional (aplicado)", "estilo não-operacional (DP)"],
    ordered=True)

colors = [CAT_COLOR[c] for c in CAT_ORDER]

# ------------------------------------------------------------------- plot
p = (
    ggplot(df, aes(y="label", x="beta"))
    # linhas de referencia 2x / 3x com o MESMO estilo (tracejado), rotuladas na linha
    + geom_vline(xintercept=2, linetype="dashed", color="#737373", size=0.5)
    + geom_vline(xintercept=3, linetype="dashed", color="#737373", size=0.5)
    # rotulos JUNTO das linhas, na vertical. 2x: esquerda da linha de x=2.
    # 3x: esquerda da linha de x=3 (entre as linhas), um pouco acima do 2x.
    + annotate("text", x=1.84, y=n_est - 6.5, label="2× fixo", angle=90,
               ha="center", va="center", size=7.5, color="#595959")
    + annotate("text", x=2.75, y=n_est - 5.5, label="3× fixo", angle=90,
               ha="center", va="center", size=7.5, color="#595959")
    # IC: linha fina horizontal SEM caps, atras do ponto (forest plot limpo).
    # show_legend=False -> nao polui a chave de Categoria com um risco no ponto.
    + geom_segment(aes(x="lo", xend="hi", y="label", yend="label",
                       color="cat_label"), size=0.7, alpha=0.9, show_legend=False)
    # ponto: bolinha pequena, solida, cor = categoria (sem distincao operacional;
    # o beta operacional do DP e o maior dos estilos -> explicado no caption/texto)
    + geom_point(aes(color="cat_label"), shape="o", size=2.2, stroke=0.5)
    + scale_color_manual(values=colors, name="Categoria")
    + scale_x_log10(breaks=[2, 3, 10, 100], labels=["2", "3", "10", "100"],
                    minor_breaks=[4, 5, 6, 7, 8, 9, 20, 30, 40, 50, 60, 70, 80, 90],
                    limits=(1.6, 200))
    + scale_y_discrete(expand=(0, 0.6, 0, 0.6))
    + labs(
        x="Fator de calibração  β = mediana(Python) / mediana(C++)   (escala log)",
        y="",
        title=f"Fator β: {n_est} estimativas em {n_prob} problemas — IC95%, escala log",
    )
    + guides(color=guide_legend(order=1))
    + theme_bw(base_size=9)
    + theme(
        figure_size=(6.0, 5.6),
        plot_title=element_text(size=10, ha="center"),
        axis_text_y=element_text(size=8.5),
        axis_text_x=element_text(size=9),
        axis_title_x=element_text(size=9),
        legend_title=element_text(size=8.5),
        legend_text=element_text(size=8),
        legend_key=element_blank(),
        panel_grid_major_y=element_blank(),
        panel_grid_minor_y=element_blank(),
        panel_grid_major_x=element_line(color="#D9D9D9", size=0.4),
        panel_grid_minor_x=element_line(color="#EDEDED", size=0.3),
    )
)

png = os.path.join(HERE, "fig1_forest_beta.png")
pdf = os.path.join(HERE, "fig1_forest_beta.pdf")
p.save(png, dpi=300, verbose=False)
p.save(pdf, verbose=False)
print("fig1_forest_beta.png / .pdf gerados em paper_figures_regeneradas/ (plotnine)")
print(f"contagem plotada: {n_est} estimativas em {n_prob} problemas")
