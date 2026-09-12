# -*- coding: utf-8 -*-
"""Standalone plotting snippets inserted into gallery post 1 (ch2-ch5).
Key = unique last CSV line of that figure's data block in the post."""

SNIPPETS_A = {

"ANR,-1.4,-0.8,0.3,-1.2,-0.5,0.1": r'''# 数据：将上方 CSV 保存为 02-heatmap.csv
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("02-heatmap.csv", index_col="gene")
fig, ax = plt.subplots(figsize=(6.4, 6.0))
im = ax.imshow(df.values, cmap="YlGnBu", vmin=-2, vmax=2, aspect="auto")
ax.set_xticks(range(df.shape[1]), df.columns, rotation=40, ha="right")
ax.set_yticks(range(df.shape[0]), df.index)
ax.grid(False)
for i in range(df.shape[0]):
    for j in range(df.shape[1]):
        ax.text(j, i, "%.1f" % df.values[i, j], ha="center", va="center", fontsize=7.5)
fig.colorbar(im, ax=ax, shrink=0.75, label="row z-score of TPM")
fig.savefig("02-heatmap.png", dpi=200, bbox_inches="tight")''',

"FLS,0.35,0.42,0.30,-0.46,-0.41,-0.38,-0.44,1.00": r'''# 数据：将上方 CSV 保存为 03-corr.csv
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("03-corr.csv", index_col="gene")
M = df.values
fig, ax = plt.subplots(figsize=(6.6, 5.6))
im = ax.imshow(M, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(df)), df.columns, rotation=40, ha="right")
ax.set_yticks(range(len(df)), df.index)
ax.grid(False)
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        ax.text(j, i, "%.2f" % M[i, j], ha="center", va="center", fontsize=7.5,
                color="white" if abs(M[i, j]) > 0.6 else "#222222")
fig.colorbar(im, ax=ax, shrink=0.8, label="Pearson r")
fig.savefig("03-corr-heatmap.png", dpi=200, bbox_inches="tight")''',

"S12,90,97": r'''# 数据：将上方 CSV 保存为 04-pearson.csv
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

df = pd.read_csv("04-pearson.csv")
x, y = df["DWF4_TPM"], df["BZR1_TPM"]
r, p = stats.pearsonr(x, y)
fig, ax = plt.subplots(figsize=(5.6, 5.0))
ax.scatter(x, y, s=55, color="#4C72B0", edgecolors="white", zorder=3)
k, b = np.polyfit(x, y, 1)
xs = np.array([x.min(), x.max()])
ax.plot(xs, k * xs + b, "--", color="#C44E52", lw=1.8, label="linear fit")
ax.text(0.05, 0.92, "Pearson r = %.2f\\np = %.1e" % (r, p), transform=ax.transAxes,
        va="top", bbox=dict(boxstyle="round,pad=0.35", fc="#F5F7FA", ec="0.7"))
ax.set_xlabel("DWF4 expression (TPM)")
ax.set_ylabel("BZR1 expression (TPM)")
ax.legend(loc="lower right")
fig.savefig("04-pearson.png", dpi=200, bbox_inches="tight")''',

"B,11.00,1.00": r'''# 数据：将上方 CSV 保存为 05-spearman.csv
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

df = pd.read_csv("05-spearman.csv")
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.6))
for ax, panel, title in [(axes[0], "A", "A. Monotone but nonlinear"),
                         (axes[1], "B", "B. One leverage outlier")]:
    sub = df[df.panel == panel]
    r, _ = stats.pearsonr(sub.x, sub.y)
    rho, _ = stats.spearmanr(sub.x, sub.y)
    ax.scatter(sub.x, sub.y, s=50, color="#4C72B0", edgecolors="white", zorder=3)
    ax.set_title(title)
    ax.text(0.05, 0.9, "Pearson r = %.2f\\nSpearman rho = %.2f" % (r, rho),
            transform=ax.transAxes, va="top", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.35", fc="#F5F7FA", ec="0.7"))
# B 组末行 (11.00, 1.00) 即红色杠杆离群点，会把虚线回归线拽到几乎躺平
fig.savefig("05-spearman.png", dpi=200, bbox_inches="tight")''',

"Seed,245": r'''# 数据：将上方 CSV 保存为 06-boxplot.csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("06-boxplot.csv")
groups = df.tissue.unique()
data = [df[df.tissue == g].tpm.values for g in groups]
CAT = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]
fig, ax = plt.subplots(figsize=(6.2, 4.8))
bp = ax.boxplot(data, tick_labels=groups, patch_artist=True, widths=0.55,
                medianprops=dict(color="black", lw=1.6))
for patch, col in zip(bp["boxes"], CAT):
    patch.set_facecolor(col)
    patch.set_alpha(0.65)
rng = np.random.default_rng(1)
for i, d in enumerate(data, 1):
    ax.scatter(rng.normal(i, 0.05, len(d)), d, s=10, color="0.25",
               alpha=0.6, zorder=3)
ax.set_ylabel("Expression (TPM)")
fig.savefig("06-boxplot.png", dpi=200, bbox_inches="tight")''',

"cold_total,45": r'''# 数据：区间数字取自上方 CSV，几何为三个半透明圆 + 区间文字
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

CAT = ["#4C72B0", "#DD8452", "#55A868"]
fig, ax = plt.subplots(figsize=(6.2, 5.6))
for (x0, y0), col in zip([(-0.1, 0), (0.95, 0), (0.42, 0.9)], CAT):
    ax.add_patch(Circle((x0, y0), 0.95, facecolor=col, alpha=0.35,
                        edgecolor=col, lw=1.6))
for t, x0, y0 in [("drought 26", -0.72, -0.35), ("salt 20", 1.58, -0.35),
                  ("cold 30", 0.42, 1.42), ("12", 0.43, -0.62),
                  ("9", -0.08, 0.45), ("11", 0.94, 0.45), ("5", 0.42, 0.12)]:
    ax.text(x0, y0, t, ha="center", va="center", fontsize=9.5)
ax.set_xlim(-1.5, 2.4)
ax.set_ylim(-1.6, 1.9)
ax.axis("off")
fig.savefig("08-venn-treatment.png", dpi=200, bbox_inches="tight")''',

"Arabidopsis_thaliana,27600,14200": r'''# 数据：两物种基因数与一对一同源数，两个圆即可
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

fig, ax = plt.subplots(figsize=(6.0, 4.6))
ax.add_patch(Circle((-0.55, 0), 1.15, facecolor="#4C72B0", alpha=0.35,
                    edgecolor="#4C72B0", lw=1.6))
ax.add_patch(Circle((0.55, 0), 1.15, facecolor="#55A868", alpha=0.35,
                    edgecolor="#55A868", lw=1.6))
ax.text(-1.35, 0, "19,200", ha="center", fontsize=12)
ax.text(0.0, 0, "14,200", ha="center", fontsize=12, fontweight="bold")
ax.text(1.35, 0, "13,400", ha="center", fontsize=12)
ax.text(-1.1, 1.35, "F. tataricum", ha="center", fontsize=10.5, color="#4C72B0")
ax.text(1.1, 1.35, "A. thaliana", ha="center", fontsize=10.5, color="#55A868")
ax.set_xlim(-2.1, 2.1)
ax.set_ylim(-1.5, 1.9)
ax.axis("off")
fig.savefig("09-venn-ortholog.png", dpi=200, bbox_inches="tight")''',

"1,1,1,1,9": r'''# 数据：将上方 CSV 保存为 10-upset.csv（0/1 成员矩阵 + 交集大小）
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("10-upset.csv").sort_values("size", ascending=False).reset_index(drop=True)
sets = ["DEG", "DEP", "PHOS", "DAM"]
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.6, 5.2), sharex=True,
                               gridspec_kw=dict(height_ratios=[3, 1.15], hspace=0.06))
ax1.bar(df.index, df["size"], color="#4C72B0", width=0.62)
for i, v in df["size"].items():
    ax1.text(i, v + 8, str(int(v)), ha="center", fontsize=9)
ax1.set_ylabel("Intersection size")
for i, row in df.iterrows():
    on = [s for s in sets if row[s] == 1]
    ax2.plot([i, i], [sets.index(on[0]), sets.index(on[-1])], color="black", lw=1)
    for s in sets:
        ax2.scatter(i, sets.index(s), s=52 if s in on else 14,
                    color="black" if s in on else "0.85")
ax2.set_yticks(range(4), sets)
ax2.invert_yaxis()
ax2.set_xticks([])
ax2.grid(False)
fig.savefig("10-upset.png", dpi=200, bbox_inches="tight")''',

"ANR,0.9,1.1,1.0,3.2,3.5,3.3": r'''# 数据：将上方 CSV 保存为 11-tpm.csv（行=基因，列=文库）
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("11-tpm.csv", index_col="gene")
fig, ax = plt.subplots(figsize=(6.6, 4.8))
bp = ax.boxplot([df[c] for c in df.columns], tick_labels=df.columns,
                patch_artist=True, widths=0.55)
colors = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3", "#937860"]
for patch, col in zip(bp["boxes"], colors):
    patch.set_facecolor(col)
    patch.set_alpha(0.6)
ax.set_yscale("log")
ax.set_ylabel("TPM (log scale)")
fig.savefig("11-tpm-dist.png", dpi=200, bbox_inches="tight")''',

"Z3_r4,Stage_III,3.3,0.2": r'''# 数据：将上方 CSV 保存为 12-pca.csv
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("12-pca.csv")
CAT = ["#4C72B0", "#DD8452", "#55A868"]
fig, ax = plt.subplots(figsize=(6.6, 5.6))
for i, g in enumerate(df.group.unique()):
    sub = df[df.group == g]
    ax.scatter(sub.PC1, sub.PC2, s=60, color=CAT[i], edgecolors="white", label=g)
for gene, lx, ly in [("DWF4", 0.85, 0.31), ("CHS", -0.72, 0.45),
                     ("FLS", 0.81, -0.38), ("ANS", -0.66, 0.52)]:
    ax.annotate("", xy=(lx * 3.4, ly * 3.4), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="#8172B3", lw=1.4))
    ax.text(lx * 3.75, ly * 3.75, gene, color="#8172B3", fontsize=9,
            ha="center", fontweight="bold")
ax.axhline(0, color="0.8", lw=0.8)
ax.axvline(0, color="0.8", lw=0.8)
ax.set_xlabel("PC1 (52.3% variance)")
ax.set_ylabel("PC2 (21.7% variance)")
ax.legend()
fig.savefig("12-pca.png", dpi=200, bbox_inches="tight")''',

"c36,C3,0.61,-5.89": r'''# 数据：将上方 CSV 保存为 13-umap.csv
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("13-umap.csv")
CAT = ["#4C72B0", "#DD8452", "#55A868"]
fig, ax = plt.subplots(figsize=(6.2, 5.4))
for i, c in enumerate(df.cluster.unique()):
    sub = df[df.cluster == c]
    ax.scatter(sub.UMAP1, sub.UMAP2, s=46, color=CAT[i], edgecolors="white", label=c)
ax.set_xlabel("UMAP 1 (arbitrary units)")
ax.set_ylabel("UMAP 2 (arbitrary units)")
ax.legend(title="cluster")
fig.savefig("13-umap.png", dpi=200, bbox_inches="tight")''',

"ANR,anthocyanin_biosynthesis": r'''# 数据：将上方 CSV 保存为 15-chord.csv（基因-功能关联表）
# 没有现成弦图包时用贝塞尔带手绘：左弧基因、右弧功能、带宽正比关联数
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("15-chord.csv")
genes = list(dict.fromkeys(df.gene))
terms = list(dict.fromkeys(df.go_term))
rel = list(zip(df.gene, df.go_term))
CAT = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3", "#937860",
       "#DA8BC3", "#8C8C8C"]
gcol = {g: CAT[i] for i, g in enumerate(genes)}

def slots(order, a0, a1, gap):
    deg = {n: sum(1 for g, t in rel if n in (g, t)) for n in order}
    avail = (a1 - a0) - gap * (len(order) - 1)
    out, cur = {}, a0
    for n in order:
        w = avail * deg[n] / sum(deg.values())
        out[n] = (cur, cur + w)
        cur += w + gap
    return out, deg

gs, gd = slots(genes, np.deg2rad(95), np.deg2rad(265), np.deg2rad(6))
ts, td = slots(terms, np.deg2rad(-85), np.deg2rad(85), np.deg2rad(6))
tsl = np.linspace(0, 1, 40)
fig, ax = plt.subplots(figsize=(8.6, 6.0))
ax.set_aspect("equal")
ax.axis("off")
gu = {g: 0.0 for g in genes}
tu = {t: 0.0 for t in terms}
for g, t in rel:
    gw = (gs[g][1] - gs[g][0]) / gd[g]
    tw = (ts[t][1] - ts[t][0]) / td[t]
    a0 = gs[g][0] + gu[g] * gw
    a1 = a0 + gw
    b0 = ts[t][0] + tu[t] * tw
    b1 = b0 + tw
    gu[g] += gw
    tu[t] += tw
    P = lambda a: np.array([np.cos(a), np.sin(a)])
    p0, p1, q0, q1 = P(a0), P(a1), P(b1), P(b0)
    top = ((1 - tsl) ** 3)[:, None] * p0 + (3 * (1 - tsl) ** 2 * tsl)[:, None] * p0 * 0.25 \\
        + (3 * (1 - tsl) * tsl ** 2)[:, None] * q0 * 0.25 + (tsl ** 3)[:, None] * q0
    bot = ((1 - tsl) ** 3)[:, None] * p1 + (3 * (1 - tsl) ** 2 * tsl)[:, None] * p1 * 0.25 \\
        + (3 * (1 - tsl) * tsl ** 2)[:, None] * q1 * 0.25 + (tsl ** 3)[:, None] * q1
    poly = np.vstack([top, bot[::-1]])
    ax.fill(poly[:, 0], poly[:, 1], color=gcol[g], alpha=0.35, lw=0)
for g in genes:
    arc = np.linspace(gs[g][0], gs[g][1], 30)
    ax.plot(np.cos(arc), np.sin(arc), color=gcol[g], lw=7, solid_capstyle="butt")
    am = gs[g][0] / 2 + gs[g][1] / 2
    ax.text(1.12 * np.cos(am), 1.12 * np.sin(am), g, ha="right", va="center",
            fontsize=10, color=gcol[g], fontweight="bold")
for t in terms:
    arc = np.linspace(ts[t][0], ts[t][1], 30)
    ax.plot(np.cos(arc), np.sin(arc), color="0.25", lw=7, solid_capstyle="butt")
    am = ts[t][0] / 2 + ts[t][1] / 2
    ax.text(1.12 * np.cos(am), 1.12 * np.sin(am), t.replace("_", " "),
            ha="left", va="center", fontsize=10)
fig.savefig("15-go-chord.png", dpi=200, bbox_inches="tight")''',

"WRKY1,-1.83,0": r'''# 数据：将上方 CSV 保存为 18-gsea.csv（score 降序，in_set=1 为成员）
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("18-gsea.csv")
s = df.score.values
hit = df.in_set.values.astype(bool)
w = np.abs(s) * hit / np.abs(s[hit]).sum()
run = np.cumsum(np.where(hit, w, -1.0 / (len(s) - hit.sum())))
peak = int(np.argmax(run))
ranks = np.arange(1, len(s) + 1)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.6, 5.4), sharex=True,
                               gridspec_kw=dict(height_ratios=[2.6, 1], hspace=0.08))
ax1.plot(ranks, run, color="#4C72B0", lw=2)
ax1.fill_between(ranks, run, 0, where=run > 0, color="#4C72B0", alpha=0.15)
ax1.axhline(0, color="0.6", lw=0.8)
ax1.axvline(peak, color="0.4", ls="--", lw=1)
ax1.annotate("peak ES = %.2f at rank %d" % (run[peak - 1], peak),
             (peak, run[peak - 1]), (peak - 7.5, run[peak - 1] - 0.02), fontsize=9)
ax1.set_ylabel("enrichment score (running sum)")
ax2.bar(ranks[hit], 1, color="black", width=0.7)
ax2.bar(ranks[~hit], 1, color="0.85", width=0.7)
ax2.set_xlabel("genes ranked by score")
fig.savefig("18-gsea.png", dpi=200, bbox_inches="tight")''',

"N10,0,0.05,0.26,0.74": r'''# 数据：将上方 CSV 保存为 19-roc.csv（label=1 阳性，列为各模型打分）
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("19-roc.csv")
label = df.label.values
fig, ax = plt.subplots(figsize=(5.8, 5.6))
for col in ["model_A", "model_B", "model_C"]:
    order = np.argsort(-df[col].values)
    lab = label[order]
    tpr = np.r_[0, np.cumsum(lab) / lab.sum()]
    fpr = np.r_[0, np.cumsum(1 - lab) / (1 - lab).sum()]
    auc = np.trapezoid(tpr, fpr)
    ax.plot(fpr, tpr, lw=2, label="%s  AUC = %.2f" % (col, auc))
ax.plot([0, 1], [0, 1], color="0.6", ls="--", lw=1.2, label="chance")
ax.set_xlabel("false positive rate")
ax.set_ylabel("true positive rate")
ax.legend(loc="lower right")
fig.savefig("19-roc.png", dpi=200, bbox_inches="tight")''',

"C10,control,18,0": r'''# 数据：将上方 CSV 保存为 20-km.csv（event=1 事件，0 删失）
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("20-km.csv")

def km(group):
    sub = df[df.group == group].sort_values("time_weeks")
    t, e = sub.time_weeks.values, sub.event.values
    s, times, surv, cx, cy = 1.0, [0.0], [1.0], [], []
    for i in range(len(t)):
        at_risk = int(np.sum(t >= t[i]))
        if e[i] == 1:
            s *= 1 - 1 / at_risk
            times += [t[i], t[i]]
            surv += [surv[-1], s]
        else:
            cx.append(t[i])
            cy.append(s)
    times.append(t.max() + 1)
    surv.append(s)
    return times, surv, cx, cy

fig, ax = plt.subplots(figsize=(6.6, 5.2))
for g, col in [("treated", "#55A868"), ("control", "#C44E52")]:
    times, surv, cx, cy = km(g)
    ax.step(times, surv, where="post", color=col, lw=2.2, label=g)
    ax.scatter(cx, cy, marker="+", s=64, color=col, linewidths=1.6, zorder=3)
ax.set_xlabel("time (weeks)")
ax.set_ylabel("survival probability")
ax.set_ylim(0, 1.05)
ax.legend(loc="lower left")
fig.savefig("20-km.png", dpi=200, bbox_inches="tight")''',

"0.9,0.038,-8.800,0.000": r'''# 数据：将上方 CSV 保存为 21-dca.csv
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("21-dca.csv")
fig, ax = plt.subplots(figsize=(6.8, 5.2))
ax.plot(df.threshold, df.model_net_benefit, "-o", ms=4, color="#4C72B0",
        label="prediction model")
ax.plot(df.threshold, df.treat_all, "--", color="#DD8452", label="treat all")
ax.axhline(0, color="0.55", lw=1.4, ls=":", label="treat none")
ax.set_xlabel("threshold probability")
ax.set_ylabel("net benefit")
ax.legend()
fig.savefig("21-dca.png", dpi=200, bbox_inches="tight")''',

"summary,1.45,1.26,1.67,100.0": r'''# 数据：将上方 CSV 保存为 22-forest.csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("22-forest.csv")
orr = df["or"].values
ys = np.arange(len(df))[::-1]
fig, ax = plt.subplots(figsize=(7.4, 5.4))
for i in range(len(df) - 1):
    ax.plot([df.low[i], df.high[i]], [ys[i]] * 2, color="0.35", lw=1.4)
    ax.scatter(orr[i], ys[i], s=df.weight_pct[i] * 26, color="#4C72B0",
               edgecolors="0.2", zorder=3)
si = len(df) - 1
ax.fill([df.low[si], orr[si], df.high[si], orr[si]],
        [ys[-1], ys[-1] + 0.28, ys[-1], ys[-1] - 0.28],
        color="#C44E52", edgecolor="0.2", zorder=3)
ax.axvline(1, color="0.5", ls="--", lw=1.2)
ax.set_yticks(ys, df.study)
ax.set_xscale("log")
ax.set_xlabel("odds ratio (log scale)")
fig.savefig("22-forest.png", dpi=200, bbox_inches="tight")''',
}
