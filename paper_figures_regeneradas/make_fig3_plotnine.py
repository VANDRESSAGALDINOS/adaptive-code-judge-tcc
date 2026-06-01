#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figura 3 (barras horizontais: fracao de TLE injusto da solucao Python correta, por
problema, sob o limite tradicional de 1,0s no JUIZ OFICIAL CSES) em PLOTNINE.
NAO altera as fracoes nem o criterio de TLE injusto - so apresentacao.

Fonte de dados (canonica, NAO alterada): paper_figures/realworld_summary.json
  -> contagens cses_python LIDAS do JSON (nada hardcoded).

Decisoes (declaradas no caption/README):
 - Fonte do veredito = CSES (juiz oficial). TLE injusto = C++ optimal ACEITO e Python
   optimal equivalente recebe TLE no CSES sob 1,0s. O pipeline local nao e a fonte.
 - DP (2 estilos): a barra usa o estilo do beta OPERACIONAL (maior beta), anotado [rec]/[iter].
 - Eixo X = 0..0,65 (maior barra ~0,56; reduz vazio a direita). Grid vertical mantido.
 - Denominador = total de casos de teste oficiais do problema no CSES (rotulo = tle/total).

Saidas: fig3_tle_injusto.png (300 dpi) e fig3_tle_injusto.pdf (vetorial).
Rodar: python3 make_fig3_plotnine.py
"""
import json
import os
import warnings
import pandas as pd
from plotnine import (
    ggplot, aes, geom_col, geom_text, coord_flip, scale_y_continuous,
    scale_fill_manual, labs, theme_bw, theme, element_text, element_blank,
    element_line, guides, guide_legend,
)

warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
JSON_PATH = os.path.join(ROOT, "paper_figures", "realworld_summary.json")

CAT_COLOR = {"graphs": "#0072B2", "dp": "#D55E00",
             "backtracking": "#009E73", "recursion": "#CC79A7"}
CAT_LABEL = {"graphs": "Grafos", "dp": "Prog. dinâmica",
             "backtracking": "Backtracking", "recursion": "Recursão"}
CAT_ORDER = ["graphs", "dp", "backtracking", "recursion"]

with open(JSON_PATH, encoding="utf-8") as f:
    RW = json.load(f)["problems"]

# ------------------------------------------------- monta dados (barra por problema)
recs = []
for pid, prob in RW.items():
    styles = [s for s in prob["styles"] if s["beta"] is not None]
    op = max(styles, key=lambda s: s["beta"]) if styles else prob["styles"][0]
    label = f"{prob['name']} ({prob['cses']})"
    if len(styles) > 1:                       # DP: anota o estilo operacional
        label += " [iter]" if op["style"] == "iterative" else " [rec]"
    tle = op["cses_python"]["tle_count"]
    total = op["cses_python"]["total"]
    tag = f"{tle}/{total}" + ("  (controle)" if prob["role"] == "control" else "")
    recs.append({"label": label, "frac": tle / total, "tag": tag,
                 "cat_label": CAT_LABEL[prob["category"]]})

df = pd.DataFrame(recs).sort_values("frac").reset_index(drop=True)
df["label"] = pd.Categorical(df["label"], categories=list(df["label"]), ordered=True)
df["cat_label"] = pd.Categorical(df["cat_label"],
                                 categories=[CAT_LABEL[c] for c in CAT_ORDER],
                                 ordered=True)

# -------------------------------------------------------------------- plot
p = (
    ggplot(df, aes(x="label", y="frac", fill="cat_label"))
    + geom_col(alpha=0.9, width=0.72)
    + geom_text(aes(label="tag"), ha="left", nudge_y=0.008, size=8, color="#333333")
    + scale_fill_manual(values=[CAT_COLOR[c] for c in CAT_ORDER], name="Categoria")
    + scale_y_continuous(limits=(0, 0.66),
                         breaks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                         expand=(0, 0, 0, 0))
    + coord_flip()
    + labs(
        x="",
        y="Fração dos casos de teste com TLE injusto\n"
          "(C++ optimal aceito, Python optimal equivalente rejeitado), limite 1,0s",
        title="TLE injusto da solução Python correta, por problema "
              "(veredito do juiz oficial CSES)",
    )
    + guides(fill=guide_legend(order=1))
    + theme_bw(base_size=9)
    + theme(
        figure_size=(6.0, 5.2),
        plot_title=element_text(size=9.5, ha="center"),
        axis_text_y=element_text(size=8.5),
        axis_text_x=element_text(size=9),
        axis_title_x=element_text(size=8.5, lineheight=1.45,
                                  margin={"t": 12, "units": "pt"}),
        legend_title=element_text(size=8.5),
        legend_text=element_text(size=8),
        legend_key=element_blank(),
        panel_grid_major_x=element_blank(),
        panel_grid_minor_x=element_blank(),
        panel_grid_minor_y=element_blank(),
        panel_grid_major_y=element_line(color="#D9D9D9", size=0.4),
    )
)

png = os.path.join(HERE, "fig3_tle_injusto.png")
pdf = os.path.join(HERE, "fig3_tle_injusto.pdf")
p.save(png, dpi=300, verbose=False)
p.save(pdf, verbose=False)
print("fig3_tle_injusto.png / .pdf gerados em paper_figures_regeneradas/ (plotnine)")
print("fonte do veredito: CSES | criterio DP: estilo do beta operacional (maior) | eixo X: 0..0,65")
print("fracoes (ordenadas):")
for _, r in df[::-1].iterrows():
    print(f"  {r['label']:34s} {r['tag']:18s} = {r['frac']:.3f}")
