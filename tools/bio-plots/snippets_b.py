# -*- coding: utf-8 -*-
"""Standalone plotting snippets for gallery post 1 (ch6-ch8).
Key = unique last CSV line of that figure's data block in the post.
NEW_BLOCKS = figures without a data block; inserter adds a code-only toggle."""

SNIPPETS_B = {

"ANR,treated,3,23.0,18.1": r'''# 数据：将上方 CSV 保存为 23-qrt-pcr.csv（原始 Ct 值，Actin 为内参）
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

df = pd.read_csv("23-qrt-pcr.csv")
df["dCt"] = df.Ct_target - df.Ct_ref
ctl_mean = df[df.condition == "control"].groupby("gene").dCt.mean()
df["fold"] = 2 ** -(df.dCt - df.gene.map(ctl_mean))
genes = ["DWF4", "CHS", "ANS", "ANR"]
CAT = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]
x = np.arange(len(genes))
fig, ax = plt.subplots(figsize=(7.0, 5.2))
for k, cond in enumerate(["control", "treated"]):
    sub = df[df.condition == cond]
    m = sub.groupby("gene").fold.mean()[genes]
    e = sub.groupby("gene").fold.std(ddof=1)[genes]
    ax.bar(x + (k - 0.5) * 0.36, m, 0.32, yerr=e, capsize=4,
           color="0.72" if k == 0 else "#C44E52", label=cond)
for i, g in enumerate(genes):                     # 对 dCt 做 t 检验标星号
    a = df[(df.gene == g) & (df.condition == "control")].dCt
    b = df[(df.gene == g) & (df.condition == "treated")].dCt
    p = stats.ttest_ind(a, b).pvalue
    star = "***" if p < 0.001 else ("**" if p < 0.01 else ("*" if p < 0.05 else "ns"))
    ax.text(x[i], 5.3, star, ha="center", fontsize=11)
ax.set_xticks(x, genes)
ax.set_ylim(0, 5.9)
ax.set_ylabel("relative expression (2^-DDCt)")
ax.legend()
fig.savefig("23-qrt-pcr-bar.png", dpi=200, bbox_inches="tight")''',

"40,1.140,0.939,0.041": r'''# 数据：将上方 CSV 保存为 24-amp.csv（也可以像本例一样直接用逻辑函数生成）
import numpy as np
import matplotlib.pyplot as plt

cyc = np.arange(2, 41, 2)
sig = lambda c, ct, amp: 0.04 + amp / (1 + np.exp(-(c - ct) / 2.2))
fa, fb = sig(cyc, 18, 1.1), sig(cyc, 24, 0.9)
thr = 0.22
fig, ax = plt.subplots(figsize=(7.0, 5.0))
ax.plot(cyc, fa, "-o", ms=4, color="#4C72B0", label="sample A")
ax.plot(cyc, fb, "-o", ms=4, color="#DD8452", label="sample B")
ax.plot(cyc, np.full_like(cyc, 0.04), "-o", ms=4, color="0.6", label="NTC")
ax.axhline(thr, color="0.35", ls="--", lw=1.2)
for f, col in [(fa, "#4C72B0"), (fb, "#DD8452")]:
    ct = cyc[np.argmax(f > thr)]
    ax.axvline(ct, color=col, ls=":", lw=1.2)
    ax.text(ct + 0.3, 0.015, "Ct = %d" % ct, fontsize=9.5, color=col)
ax.set_xlabel("cycle number")
ax.set_ylabel("normalized fluorescence (Rn)")
ax.legend(loc="upper left")
fig.savefig("24-amp-curve.png", dpi=200, bbox_inches="tight")''',

"94,0.000,0.000": r'''# 数据：将上方 CSV 保存为 25-melt.csv（也可用 sigmoid 生成，见 Tm 列表）
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("25-melt.csv")
T = df.temperature.values
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.8), sharex=True)
ax1.plot(T, df.fluor_good, "-o", ms=4, color="#4C72B0", label="single amplicon")
ax1.plot(T, df.fluor_two_peak, "-o", ms=4, color="#DD8452", label="two amplicons")
ax1.set(xlabel="temperature (C)", ylabel="fluorescence (fraction)")
ax1.legend()
der_good = -np.gradient(df.fluor_good, T)      # 一阶负导数，注意用 T 作坐标
der_bad = -np.gradient(df.fluor_two_peak, T)
ax2.plot(T, der_good, "-o", ms=4, color="#4C72B0")
ax2.plot(T, der_bad, "-o", ms=4, color="#DD8452")
ax2.set(xlabel="temperature (C)", ylabel="-d(F) / dT")
pk = T[np.argmax(der_good)]
ax2.annotate("Tm = %d C" % pk, (pk, der_good.max()), (pk - 7, der_good.max() * 0.85),
             fontsize=9.5, color="#4C72B0",
             arrowprops=dict(arrowstyle="-", color="#4C72B0", lw=0.9))
fig.savefig("25-melt-curve.png", dpi=200, bbox_inches="tight")''',

"product,400,632": r'''# 数据：将上方 CSV 保存为 26-amplicon.csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow

df = pd.read_csv("26-amplicon.csv")
fig, ax = plt.subplots(figsize=(9.2, 3.6))
ax.plot([0, 900], [1, 1], color="0.75", lw=2)
for _, row in df.iterrows():
    f, s, e = row.feature, int(row.start), int(row.end)
    if f.startswith("exon"):
        ax.add_patch(Rectangle((s, 0.72), e - s, 0.56, facecolor="#4C72B0",
                               edgecolor="0.2"))
        ax.text((s + e) / 2, 0.35, f, ha="center", fontsize=8.5)
    elif f.endswith("primer"):
        col = "#DD8452" if f.startswith("forward") else "#55A868"
        ax.add_patch(FancyArrow(s, 1.9, e - s, 0, width=0.14, head_width=0.42,
                                head_length=26, length_includes_head=True,
                                facecolor=col, edgecolor="0.2"))
        dy = 0.42 if f.startswith("forward") else -0.62
        ax.text((s + e) / 2, 1.9 + dy, f.replace("_", " "), ha="center",
                fontsize=8.5, color=col)
ax.plot([400, 400, 632, 632], [2.5, 2.7, 2.7, 2.5], color="0.3", lw=1.2)
ax.text(516, 2.84, "product 233 bp", ha="center", fontsize=9.5)
ax.set_xticks(range(0, 901, 100))
ax.set_xlabel("position in CDS (bp)")
ax.set_yticks([])
ax.spines["left"].set_visible(False)
fig.savefig("26-amplicon-cds.png", dpi=200, bbox_inches="tight")''',

"negative_control,2,36": r'''# 示意图：无真实数据集，细胞群用随机椭圆模拟（固定种子可复现）
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

rng = np.random.default_rng(5)
pos = []
while len(pos) < 36:
    x, y = rng.uniform(0.6, 9.4), rng.uniform(0.6, 6.4)
    if all((x - a) ** 2 + (y - b) ** 2 > 1.1 for a, b in pos):
        pos.append((x, y))
fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.4))
for ax, title, npos in zip(axes, ["positive section", "negative control"], [22, 2]):
    idx = set(rng.permutation(36)[:npos])
    for i, (x, y) in enumerate(pos):
        ax.add_patch(Ellipse((x, y), 0.95, 0.78, facecolor="#8B5A2B" if i in idx
                             else "#C9B6D9", edgecolor="#5D4037", lw=0.8))
        ax.add_patch(Ellipse((x, y), 0.34, 0.3, facecolor="#3E2723", alpha=0.75))
    ax.add_patch(plt.Rectangle((8.0, 0.25), 1.6, 0.22, color="black"))
    ax.text(8.8, 0.62, "50 um", ha="center", fontsize=8)
    ax.set_title(title, fontsize=10.5)
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
fig.savefig("28-ihc.png", dpi=200, bbox_inches="tight")''',

"merged_colocalized,17": r'''# 示意图：三个通道面板（DAPI / 目标蛋白 / 合并），细胞位置固定种子复现
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

rng = np.random.default_rng(9)
pos = []
while len(pos) < 36:
    x, y = rng.uniform(0.6, 9.4), rng.uniform(0.6, 6.4)
    if all((x - a) ** 2 + (y - b) ** 2 > 1.1 for a, b in pos):
        pos.append((x, y))
green = set(rng.permutation(36)[:17])
fig, axes = plt.subplots(1, 3, figsize=(12.2, 4.0))
for ax, (title, mode) in zip(axes, [("DAPI (nuclei)", "blue"),
                                    ("anti-target (Alexa 488)", "green"),
                                    ("merged", "merge")]):
    for i, (x, y) in enumerate(pos):
        if mode in ("blue", "merge"):
            ax.add_patch(Ellipse((x, y), 0.9, 0.74, facecolor="#2962FF",
                                 edgecolor="none", alpha=0.55 if mode == "merge" else 0.75))
        if mode in ("green", "merge") and i in green:
            ax.add_patch(Ellipse((x, y), 1.35, 1.15, facecolor="#00C853",
                                 edgecolor="none", alpha=0.45))
    ax.set_title(title, fontsize=10)
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
fig.savefig("29-if.png", dpi=200, bbox_inches="tight")''',

"uv_treated,15,36": r'''# 示意图：TUNEL 双面板（对照 vs 处理），绿色核为凋亡阳性
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.4))
for ax, title, ngreen, seed in zip(axes, ["control", "UV-treated"], [3, 15],
                                   [12, 13]):
    rng = np.random.default_rng(seed)
    pos = []
    while len(pos) < 36:
        x, y = rng.uniform(0.6, 9.4), rng.uniform(0.6, 6.4)
        if all((x - a) ** 2 + (y - b) ** 2 > 1.1 for a, b in pos):
            pos.append((x, y))
    idx = set(rng.permutation(36)[:ngreen])
    for i, (x, y) in enumerate(pos):
        ax.add_patch(Ellipse((x, y), 0.85, 0.7,
                             facecolor="#00C853" if i in idx else "#2962FF",
                             edgecolor="none", alpha=0.8))
    ax.set_title("%s: %d/36 TUNEL+" % (title, ngreen), fontsize=10.5)
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
fig.savefig("30-tunel.png", dpi=200, bbox_inches="tight")''',

"275,18,18": r'''# 数据：将上方 CSV 保存为 31-cycle.csv（分箱计数表）
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("31-cycle.csv")
fig, ax = plt.subplots(figsize=(7.4, 5.0))
ax.bar(df.channel - 6, df.control_counts, width=11, color="#4C72B0",
       alpha=0.55, label="control")
ax.bar(df.channel + 6, df.treated_counts, width=11, color="#C44E52",
       alpha=0.55, label="drug-treated")
ax.set_xticks(df.channel)
ax.set_xlabel("DNA content (PI-A channel)")
ax.set_ylabel("cell count")
ax.legend()
fig.savefig("31-flow-cycle.png", dpi=200, bbox_inches="tight")''',

"0.34,0.45,double_negative": r'''# 数据：将上方 CSV 保存为 32-pheno.csv
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("32-pheno.csv")
CAT = {"double_positive": "#C44E52", "B_only": "#DD8452",
       "A_only": "#4C72B0", "double_negative": "0.6"}
fig, ax = plt.subplots(figsize=(6.4, 6.0))
for name, col in CAT.items():
    sub = df[df.population == name]
    ax.scatter(sub.marker_A, sub.marker_B, s=42, color=col,
               edgecolors="white", linewidths=0.6,
               label="%s (%d%%)" % (name.replace("_", " "),
                                    round(100 * len(sub) / len(df))))
ax.axvline(1.9, color="0.3", lw=1.2)
ax.axhline(1.9, color="0.3", lw=1.2)
ax.set_xlabel("marker A fluorescence (log)")
ax.set_ylabel("marker B fluorescence (log)")
ax.legend(loc="upper left", fontsize=8.5)
fig.savefig("32-flow-pheno.png", dpi=200, bbox_inches="tight")''',

"0.08,3.24,necrotic": r'''# 数据：将上方 CSV 保存为 33-apop.csv
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("33-apop.csv")
CAT = {"viable": "#55A868", "early_apoptotic": "#DD8452",
       "late_apoptotic": "#C44E52", "necrotic": "#8172B3"}
fig, ax = plt.subplots(figsize=(6.6, 6.0))
for name, col in CAT.items():
    sub = df[df.population == name]
    ax.scatter(sub.annexin_V, sub.PI, s=42, color=col, edgecolors="white")
    ax.text(sub.annexin_V.mean(), sub.PI.mean() + 0.75,
            "%s\n%d%%" % (name.replace("_", " "),
                          round(100 * len(sub) / len(df))),
            ha="center", fontsize=9.5, color=col, fontweight="bold")
ax.axvline(1.6, color="0.3", lw=1.2)
ax.axhline(1.6, color="0.3", lw=1.2)
ax.set_xlabel("Annexin V fluorescence (apoptosis)")
ax.set_ylabel("PI fluorescence (membrane integrity)")
fig.savefig("33-flow-apop.png", dpi=200, bbox_inches="tight")''',

"region,mapped,antisense,1.4": r'''# 数据：将上方 CSV 保存为 34-sankey.csv；飘带用三次贝塞尔带手绘
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

df = pd.read_csv("34-sankey.csv")
V = dict(zip(df.to, df.value_M))
S = 10.0 / 12.3
X0, X1, X2, W = 0.04, 0.46, 0.88, 0.07

def band(ax, x0, t0, t1, x1, u0, u1, color, alpha=0.35):
    ts = np.linspace(0, 1, 40)
    xm = (x0 + x1) / 2
    M = np.column_stack([(1 - ts) ** 3, 3 * (1 - ts) ** 2 * ts,
                         3 * (1 - ts) * ts ** 2, ts ** 3])
    top = M @ np.array([[x0, t0], [xm, t0], [xm, u0], [x1, u0]])
    bot = M @ np.array([[x0, t1], [xm, t1], [xm, u1], [x1, u1]])
    poly = np.vstack([top, bot[::-1]])
    ax.fill(poly[:, 0], poly[:, 1], color=color, alpha=alpha, lw=0)

fig, ax = plt.subplots(figsize=(9.0, 5.4))
ax.add_patch(Rectangle((X0, 0), W, 12.0 * S, facecolor="0.55"))
ax.add_patch(Rectangle((X1, 0), W, 10.8 * S, facecolor="#4C72B0"))
y_unm = 10.8 * S + 0.5
ax.add_patch(Rectangle((X1, y_unm), W, 1.2 * S, facecolor="0.75"))
band(ax, X0 + W, 0, 10.8 * S, X1, 0, 10.8 * S, "#4C72B0", alpha=0.3)
band(ax, X0 + W, 10.8 * S, 12.0 * S, X1, y_unm, y_unm + 1.2 * S, "0.7")
ycur, yfrom = 0.0, 0.0
for to, col in [("CDS", "#4C72B0"), ("intron_intergenic", "#DD8452"),
                ("antisense", "#55A868")]:
    v = V[to]
    ax.add_patch(Rectangle((X2, ycur), W, v * S, facecolor=col))
    ax.text(X2 + W + 0.03, ycur + v * S / 2, "%s  %.1f M" % (to, v),
            va="center", fontsize=10)
    band(ax, X1 + W, yfrom, yfrom + v * S, X2, ycur, ycur + v * S, col)
    ycur += v * S + 0.4
    yfrom += v * S
ax.set_xlim(-0.28, 1.35)
ax.set_ylim(-0.5, 10.8)
ax.axis("off")
fig.savefig("34-sankey.png", dpi=200, bbox_inches="tight")''',

"48,55": r'''# 数据：将上方 CSV 保存为 35-plddt.csv；背景色带按 AlphaFold 官方置信度分级
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("35-plddt.csv")
AF = [("#FF7D45", 0, 50), ("#FFDB13", 50, 70), ("#65CBF3", 70, 90), ("#0053D6", 90, 101)]
anchors = df[df.anchor != ""][["residue", "plddt"]]
fig, ax = plt.subplots(figsize=(8.0, 4.6))
for col, a, b in AF:
    ax.axhspan(a, b, color=col, alpha=0.12)
for col, a, b in AF:                       # 折线按数值分段上色
    seg = df[(df.plddt >= a) & (df.plddt < b)]
    ax.plot(seg.residue, seg.plddt, color=col, lw=1.8)
for _, row in anchors.iterrows():
    ax.axvline(row.residue, color="#C62828", ls="--", lw=1)
    ax.scatter([row.residue], [row.plddt], s=46, facecolor="white",
               edgecolor="#C62828", linewidth=1.5, zorder=5)
ax.set_ylim(20, 101)
ax.set_xlabel("residue number")
ax.set_ylabel("pLDDT")
fig.savefig("35-protein-anchor.png", dpi=200, bbox_inches="tight")''',

"ANR,1,1,0,1,0,0": r'''# 数据：将上方 CSV 保存为 36-evidence.csv（0/1 证据矩阵）
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("36-evidence.csv", index_col="gene")
fig, ax = plt.subplots(figsize=(8.6, 4.6))
for i, g in enumerate(df.index):
    for j, e in enumerate(df.columns):
        on = df.loc[g, e] == 1
        ax.scatter(j, i, s=640, facecolor="#4C72B0" if on else "white",
                   edgecolor="0.4", linewidth=1.1)
ax.set_xticks(range(df.shape[1]), [c.replace("_", " ") for c in df.columns],
              rotation=20, ha="right", fontsize=9.5)
ax.set_yticks(range(df.shape[0]), df.index)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_visible(False)
fig.savefig("36-evidence-matrix.png", dpi=200, bbox_inches="tight")''',

"Seed,28.4,88.3,42.1": r'''# 数据：将上方 CSV 保存为 37-tissue.csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("37-tissue.csv")
x = np.arange(len(df))
CAT = ["#4C72B0", "#DD8452", "#55A868"]
fig, ax = plt.subplots(figsize=(7.4, 5.0))
for i, g in enumerate(["DWF4", "CHS", "ANR"]):
    ax.bar(x + (i - 1) * 0.26, df[g], 0.24, label=g, color=CAT[i])
ax.set_xticks(x, df.tissue)
ax.set_ylabel("TPM")
ax.legend(title="gene")
fig.savefig("37-tissue-expression.png", dpi=200, bbox_inches="tight")''',

"skn-1_like,-1770,-1763,+": r'''# 数据：将上方 CSV 保存为 38-promoter.csv（+ 链在上、- 链在下）
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

df = pd.read_csv("38-promoter.csv")
CAT = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3", "#937860",
       "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]
fam = list(dict.fromkeys(df.element))
fcol = {f: CAT[i % 10] for i, f in enumerate(fam)}
fig, ax = plt.subplots(figsize=(9.6, 4.2))
for _, row in df.iterrows():
    y = 1.25 if row.strand == "+" else -1.25
    ax.add_patch(Rectangle((row.start, y - 0.22), row.end - row.start + 26,
                           0.44, facecolor=fcol[row.element], edgecolor="0.2"))
    ax.text(row.start + 13, y + (0.34 if row.strand == "+" else -0.42),
            row.element, ha="center", fontsize=8, rotation=30,
            color=fcol[row.element])
ax.plot([-2000, 120], [0, 0], color="black", lw=1.6)
ax.text(125, 0, "TSS", va="center", fontsize=9)
ax.set_xlim(-2050, 320)
ax.set_ylim(-2.5, 2.7)
ax.set_yticks([])
ax.set_xticks(range(-2000, 1, 250))
ax.set_xlabel("position relative to TSS (bp)")
ax.spines["left"].set_visible(False)
fig.savefig("38-promoter-cis.png", dpi=200, bbox_inches="tight")''',

"mature,1.4,0.9,1.8,1.1": r'''# 数据：将上方 CSV 保存为 39-brga.csv
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("39-brga.csv", index_col="stage")
CAT = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]
x = range(len(df))
fig, ax = plt.subplots(figsize=(7.2, 5.0))
for i, g in enumerate(df.columns):
    ax.plot(x, df[g], "-o", ms=6, color=CAT[i], label=g)
    pk = df[g].idxmax()
    ax.annotate("peak %.1f" % df[g].max(), (list(df.index).index(pk), df[g].max()),
                xytext=(8, 8), textcoords="offset points", fontsize=8.5, color=CAT[i])
ax.set_xticks(x, df.index)
ax.set_ylabel("TPM")
ax.legend()
fig.savefig("39-brga-dynamics.png", dpi=200, bbox_inches="tight")''',

"gene_08,-0.9,-1.0,-0.7,0.2,1.3": r'''# 数据：将上方 CSV 保存为 40-cascade.csv；行按峰值时间排序后斜带才会出现
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("40-cascade.csv", index_col="gene")
order = df.values.argmax(axis=1).argsort()       # 按峰值所在时间点排序
df = df.iloc[order]
fig, ax = plt.subplots(figsize=(6.6, 5.4))
im = ax.imshow(df.values, cmap="coolwarm", vmin=-2, vmax=2, aspect="auto")
ax.set_xticks(range(df.shape[1]), df.columns)
ax.set_yticks(range(df.shape[0]), df.index)
ax.grid(False)
for i in range(df.shape[0]):
    for j in range(df.shape[1]):
        ax.text(j, i, "%.1f" % df.values[i, j], ha="center", va="center",
                fontsize=7.5, color="white" if abs(df.values[i, j]) > 1.2 else "#222")
fig.colorbar(im, ax=ax, shrink=0.8, label="z-score")
fig.savefig("40-cascade-heatmap.png", dpi=200, bbox_inches="tight")''',

"c6,8.68": r'''# 数据：将上方 CSV 保存为 41-ridge.csv；山脊高度=核密度，纵向错开仅为排版
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

df = pd.read_csv("41-ridge.csv")
groups = list(df.groupby("cluster"))
xs = np.linspace(-1.5, 14, 300)
fig, ax = plt.subplots(figsize=(7.6, 5.6))
CAT = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3", "#937860"]
for i, (name, sub) in enumerate(reversed(groups)):
    d = gaussian_kde(sub.expression.values)(xs)
    base = (len(groups) - i) * 1.0
    ax.fill_between(xs, base, base + d, color=CAT[i % 6], alpha=0.55, lw=1.2,
                    edgecolor="white")
    ax.text(-1.7, base + 0.1, name, ha="right", fontsize=10)
ax.set_xlim(-3.2, 14)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.set_xlabel("expression (log2 TPM)")
fig.savefig("41-ridgeline.png", dpi=200, bbox_inches="tight")''',
}

# 没有数据折叠块的图：插入器会在其图注段后新增纯代码折叠块
NEW_BLOCKS = {
"> 图 7 四个组织表达分布的核密度估计。宽度编码样本密度，白点为中位数，粗线为四分位距；数据与图 6 相同。":
r'''{% hideToggle 展开查看：绘图代码（Python，独立可运行） %}

```python
# 数据：与 2.6 节的 06-boxplot.csv 完全相同
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("06-boxplot.csv")
groups = df.tissue.unique()
data = [df[df.tissue == g].tpm.values for g in groups]
CAT = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]
fig, ax = plt.subplots(figsize=(6.2, 4.8))
vp = ax.violinplot(data, showextrema=False)
for body, col in zip(vp["bodies"], CAT):
    body.set_facecolor(col)
    body.set_alpha(0.65)
for i, d in enumerate(data, 1):
    q1, med, q3 = np.percentile(d, [25, 50, 75])
    ax.vlines(i, q1, q3, color="black", lw=4)
    ax.scatter(i, med, s=28, color="white", edgecolors="black", zorder=3)
ax.set_xticks(range(1, 5), groups)
ax.set_ylabel("Expression (TPM)")
fig.savefig("07-violin.png", dpi=200, bbox_inches="tight")
```

{% endhideToggle %}''',

"> 图 17 KEGG 富集柱形图。条长为差异基因命中数，颜色为 -log10(padj)；按命中基因数降序排列。":
r'''{% hideToggle 展开查看：模拟数据与绘图代码 %}

```csv
pathway,enrich_factor,count,padj
Flavonoid biosynthesis,0.082,24,0.00012
Brassinosteroid biosynthesis,0.096,11,0.0031
Phenylpropanoid biosynthesis,0.064,31,0.00040
Plant hormone signal transduction,0.041,38,0.0021
Cutin suberine and wax biosynthesis,0.075,9,0.012
Starch and sucrose metabolism,0.037,22,0.0068
Circadian rhythm - plant,0.052,8,0.038
Amino sugar metabolism,0.028,15,0.041
```

```python
# 数据：将上方 CSV 保存为 17-kegg.csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("17-kegg.csv")
neglog = -np.log10(df.padj)
order = df["count"].sort_values(ascending=False).index
d = df.loc[order]
fig, ax = plt.subplots(figsize=(8.4, 5.2))
ax.barh(range(len(d)), d["count"], color=plt.cm.viridis(neglog[order] / neglog.max()),
        edgecolor="0.3", linewidth=0.5)
ax.set_yticks(range(len(d)), d.pathway, fontsize=9)
for i, v in enumerate(d["count"]):
    ax.text(v + 0.4, i, str(v), va="center", fontsize=8.5)
ax.set_xlabel("DEG count mapped to pathway")
sm = plt.cm.ScalarMappable(cmap="viridis",
                           norm=plt.Normalize(0, neglog.max()))
fig.colorbar(sm, ax=ax, shrink=0.8, label="-log10(padj)")
fig.savefig("17-kegg-bar.png", dpi=200, bbox_inches="tight")
```

{% endhideToggle %}''',

"> 图 14 候选基因层次聚类热图。行聚类采用平均连锁法与欧氏距离；颜色为行内 z-score，右侧为基因名。":
r'''{% hideToggle 展开查看：绘图代码（Python，独立可运行，数据复用 2.2 节） %}

```python
# 数据：与 2.2 节的 02-heatmap.csv 完全相同
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram

df = pd.read_csv("02-heatmap.csv", index_col="gene")
Z = linkage(df.values, method="average", metric="euclidean")
fig = plt.figure(figsize=(6.8, 7.0))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 2.6], hspace=0.04)
axd = fig.add_subplot(gs[0])
dd = dendrogram(Z, ax=axd, no_labels=True, color_threshold=0,
                link_color_func=lambda k: "0.4")
axd.set_yticks([])
axd.grid(False)
axh = fig.add_subplot(gs[1])
order = dd["leaves"]
im = axh.imshow(df.values[order], cmap="YlGnBu", vmin=-2, vmax=2, aspect="auto")
axh.set_xticks(range(df.shape[1]), df.columns, rotation=40, ha="right")
axh.set_yticks(range(len(order)), [df.index[i] for i in order], fontsize=8.5)
axh.grid(False)
fig.colorbar(im, ax=axh, shrink=0.7, label="row z-score of TPM")
fig.savefig("14-dendro-heatmap.png", dpi=200, bbox_inches="tight")
```

{% endhideToggle %}''',

"> 图 28 Co-IP 检测 DWF4 与 BZR1 的体内互作（示意）。Input 为总蛋白对照，IP: IgG 为阴性对照；以 anti-DWF4 沉淀后经 anti-BZR1 检测出现 58 kDa 条带，表明两者存在互作。":
r'''{% hideToggle 展开查看：绘图代码（Python，示意条带，非真实膜图） %}

```python
# 示意图：黑底白带模拟膜图排版，真实结果请扫描原图
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

fig, ax = plt.subplots(figsize=(7.6, 5.6))
ax.add_patch(Rectangle((0.7, 0.6), 8.6, 8.8, facecolor="#0B0B0B"))
lanes = {"Input": 2.6, "IP: IgG": 5.0, "IP: anti-DWF4": 7.6}
for name, x0 in lanes.items():
    ax.text(x0, 8.85, name, ha="center", fontsize=9.5, color="white")

def band(x0, y0, w, h, intensity):
    ax.add_patch(FancyBboxPatch((x0 - w / 2, y0 - h / 2), w, h,
                                boxstyle="round,pad=0.04", facecolor="white",
                                alpha=0.55 + 0.45 * intensity, edgecolor="none"))

ax.text(5.0, 7.7, "blot 1: probed with anti-DWF4", ha="center",
        fontsize=9, color="#9ADBFE")
band(2.6, 5.4, 1.5, 0.34, 0.8)            # Input 泳道
band(7.6, 5.4, 1.5, 0.34, 1.0)            # IP 泳道 43 kDa
ax.plot([0.9, 9.1], [4.55, 4.55], color="#333333", lw=1)
ax.text(5.0, 4.15, "blot 2: re-probed with anti-BZR1", ha="center",
        fontsize=9, color="#B9F6CA")
band(2.6, 2.9, 1.5, 0.34, 0.45)
band(7.6, 2.9, 1.5, 0.34, 0.75)           # 58 kDa 共沉淀条带 = 互作证据
for label, y0 in [("75", 7.3), ("50", 5.4), ("37", 3.9), ("25", 2.5)]:
    ax.text(1.15, y0, label, ha="center", fontsize=8.5, color="white")
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")
fig.savefig("27-wb-coip.png", dpi=200, bbox_inches="tight")
```

{% endhideToggle %}''',
}
