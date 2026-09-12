# -*- coding: utf-8 -*-
"""Chapter 2 - differential expression & data panorama (11 figures)."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from scipy import stats

from common import save, dump, csv_cols, num, CAT, UP, DOWN, NS

rng = np.random.default_rng(42)


# ---------------------------------------------------------------- 01 volcano
def volcano():
    csv = """gene,log2FC,padj
DWF4,2.85,3.2e-06
BZR1,1.92,4.1e-05
CHS,3.41,8.8e-08
F3H,2.34,1.2e-05
ANS,2.66,5.5e-06
PAL,1.63,2.3e-04
SAUR32,1.28,3.5e-03
GA20ox,1.75,9.9e-04
EXP8,1.42,4.7e-03
CHI,2.11,6.8e-05
FLS,1.55,1.8e-04
PER12,1.19,2.1e-02
DET2,-1.87,1.1e-04
GA2ox,-1.44,2.9e-03
ANR,-2.22,8.3e-05
F3H5H,-1.62,7.4e-03
LAC4,-1.28,1.6e-02
SUS1,-1.09,3.9e-02
BRI1,-1.71,5.2e-04
XTH22,-1.35,2.6e-03
ACT7,0.21,0.61
EF1a,-0.12,0.77
TUB6,0.34,0.44
UBQ10,-0.05,0.91
RBCS,0.58,0.18
LHCB,-0.42,0.29
NCED3,0.87,0.061
PYL4,-0.66,0.23
ABF2,0.44,0.37
SOD,-0.28,0.52
APX1,0.73,0.12
CAT2,-0.51,0.31
HSP70,0.39,0.41
WRKY1,0.95,0.049
MYB12,1.05,0.058"""
    dump("01-volcano", csv)
    _, c = csv_cols(csv)
    x = num(c, "log2FC")
    y = -np.log10(num(c, "padj"))

    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    col = np.where((x >= 1) & (y > -np.log10(0.05)), UP,
          np.where((x <= -1) & (y > -np.log10(0.05)), DOWN, NS))
    ax.scatter(x, y, c=col, s=42, alpha=0.85, edgecolors="white", linewidths=0.6)
    ax.axvline(1, color="grey", ls="--", lw=1)
    ax.axvline(-1, color="grey", ls="--", lw=1)
    ax.axhline(-np.log10(0.05), color="grey", ls="--", lw=1)
    ax.text(3.35, -np.log10(0.05) + 0.08, "padj = 0.05", fontsize=8.5, color="grey", ha="right")
    ax.text(1.05, 6.4, "|log2FC| = 1", fontsize=8.5, color="grey", rotation=90, va="top")
    for g, lx, ly, dx in [("CHS", 3.41, 7.06, 0.0), ("DWF4", 2.85, 5.49, 0.0),
                          ("ANR", -2.22, 4.08, 0.0), ("BRI1", -1.71, 3.28, 0.0)]:
        ax.annotate(g, (lx, ly), (lx + dx, ly + 0.45), ha="center",
                    fontsize=9, fontweight="bold",
                    arrowprops=dict(arrowstyle="-", lw=0.8, color="0.35"))
    # edge cases for teaching: significant but small FC, or big FC but not significant
    ax.annotate("WRKY1\npadj<0.05 but\n|log2FC|<1", (0.95, 1.31), (0.15, 2.6),
                fontsize=8, color="0.35", ha="center",
                arrowprops=dict(arrowstyle="-", lw=0.8, color="0.6"))
    ax.annotate("MYB12\n|log2FC|>1 but\npadj>0.05", (1.05, 1.24), (2.0, 1.9),
                fontsize=8, color="0.35", ha="center",
                arrowprops=dict(arrowstyle="-", lw=0.8, color="0.6"))
    ax.set_xlabel("log2 (fold change, treated / control)")
    ax.set_ylabel("-log10 (adjusted p-value)")
    ax.set_title("Volcano plot of DE genes")
    ax.legend(handles=[plt.Line2D([], [], ls="", marker="o", color=UP, label="Up"),
                       plt.Line2D([], [], ls="", marker="o", color=DOWN, label="Down"),
                       plt.Line2D([], [], ls="", marker="o", color=NS, label="Not significant")],
              loc="upper left")
    save(fig, "01-volcano")


# ------------------------------------------------------- 02 heatmap (12 x 6)
HEAT_CSV = """gene,A_Z1,A_Z2,A_Z3,B_Z1,B_Z2,B_Z3
DWF4,-1.2,-0.1,1.6,-0.9,0.2,1.4
DET2,-0.8,-0.3,0.9,-0.6,-0.1,1.1
BRI1,0.9,1.2,0.4,-0.7,-0.2,-0.5
BZR1,-1.1,0.3,1.8,-1.0,0.1,1.2
PRE1,0.4,1.0,1.4,-0.3,0.6,0.9
SAUR19,-0.6,0.2,1.1,-0.8,-0.4,0.7
CHS,1.5,1.8,0.6,0.9,1.2,-0.3
CHI,1.1,1.4,0.3,0.6,0.9,-0.5
F3H,0.8,1.2,0.1,0.4,0.8,-0.6
FLS,-0.9,-0.4,0.7,-1.1,-0.6,0.4
ANS,1.3,1.6,0.2,0.7,1.0,-0.4
ANR,-1.4,-0.8,0.3,-1.2,-0.5,0.1"""


def heatmap():
    dump("02-heatmap", HEAT_CSV)
    _, c = csv_cols(HEAT_CSV)
    genes = c["gene"]
    samples = [k for k in c if k != "gene"]
    M = np.vstack([num(c, s) for s in samples]).T

    fig, ax = plt.subplots(figsize=(6.4, 6.0))
    im = ax.imshow(M, cmap="YlGnBu", vmin=-2, vmax=2, aspect="auto")
    ax.set_xticks(range(len(samples)), samples, rotation=40, ha="right")
    ax.set_yticks(range(len(genes)), genes)
    ax.grid(False)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, "%.1f" % M[i, j], ha="center", va="center",
                    fontsize=7.5, color="#333333")
    ax.set_title("Expression heatmap (row z-score)")
    cb = fig.colorbar(im, ax=ax, shrink=0.75)
    cb.set_label("row z-score of TPM")
    save(fig, "02-heatmap")


# ------------------------------------------------------- 03 correlation heat
CORR_CSV = """gene,DWF4,BZR1,SAUR19,CHS,CHI,F3H,ANS,FLS
DWF4,1.00,0.86,0.82,-0.21,-0.18,-0.15,-0.24,0.35
BZR1,0.86,1.00,0.78,-0.12,-0.16,-0.09,-0.19,0.42
SAUR19,0.82,0.78,1.00,-0.18,-0.22,-0.11,-0.27,0.30
CHS,-0.21,-0.12,-0.18,1.00,0.93,0.88,0.91,-0.46
CHI,-0.18,-0.16,-0.22,0.93,1.00,0.85,0.89,-0.41
F3H,-0.15,-0.09,-0.11,0.88,0.85,1.00,0.86,-0.38
ANS,-0.24,-0.19,-0.27,0.91,0.89,0.86,1.00,-0.44
FLS,0.35,0.42,0.30,-0.46,-0.41,-0.38,-0.44,1.00"""


def corr_heatmap():
    dump("03-corr-heatmap", CORR_CSV)
    _, c = csv_cols(CORR_CSV)
    genes = c["gene"]
    M = np.vstack([num(c, g) for g in genes])

    fig, ax = plt.subplots(figsize=(6.6, 5.6))
    im = ax.imshow(M, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(genes)), genes, rotation=40, ha="right")
    ax.set_yticks(range(len(genes)), genes)
    ax.grid(False)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M[i, j]
            ax.text(j, i, "%.2f" % v, ha="center", va="center", fontsize=7.5,
                    color="white" if abs(v) > 0.6 else "#222222")
    ax.set_title("Pearson correlation between genes")
    cb = fig.colorbar(im, ax=ax, shrink=0.8)
    cb.set_label("Pearson r")
    save(fig, "03-corr-heatmap")


# ---------------------------------------------------------------- 04 pearson
def pearson():
    csv = """sample,DWF4_TPM,BZR1_TPM
S1,12,15
S2,24,31
S3,31,38
S4,38,44
S5,45,41
S6,52,63
S7,58,57
S8,64,74
S9,71,70
S10,77,85
S11,84,80
S12,90,97"""
    dump("04-pearson", csv)
    _, c = csv_cols(csv)
    x, y = num(c, "DWF4_TPM"), num(c, "BZR1_TPM")
    r, p = stats.pearsonr(x, y)

    fig, ax = plt.subplots(figsize=(5.6, 5.0))
    ax.scatter(x, y, s=55, color=CAT[0], edgecolors="white", linewidths=0.8, zorder=3)
    k, b = np.polyfit(x, y, 1)
    xs = np.linspace(x.min(), x.max(), 50)
    ax.plot(xs, k * xs + b, color=CAT[3], lw=1.8, ls="--",
            label="linear fit (least squares)")
    ax.text(0.05, 0.92, "Pearson r = %.2f\np = %.1e" % (r, p), transform=ax.transAxes,
            fontsize=10.5, va="top",
            bbox=dict(boxstyle="round,pad=0.35", fc="#F5F7FA", ec="0.7"))
    ax.set_xlabel("DWF4 expression (TPM)")
    ax.set_ylabel("BZR1 expression (TPM)")
    ax.set_title("Pearson correlation, 12 samples")
    ax.legend(loc="lower right")
    save(fig, "04-pearson")


# --------------------------------------------------------------- 05 spearman
def spearman():
    x = np.arange(1, 13)
    y = 2.0 ** x
    r_p, _ = stats.pearsonr(x, y)
    rho_s, _ = stats.spearmanr(x, y)

    n = 14
    xl = rng.uniform(1, 10, n)
    yl = 2.0 * xl + rng.normal(0, 1.2, n)
    xl = np.append(xl, 11.0)           # leverage outlier: largest x, lowest y
    yl = np.append(yl, 1.0)
    r_p2, _ = stats.pearsonr(xl, yl)
    rho_s2, _ = stats.spearmanr(xl, yl)
    xs = np.sort(xl)

    dump("05-spearman",
         "panel,x,y\n" + "\n".join("A,%d,%d" % (a, b) for a, b in zip(x, y)) + "\n" +
         "\n".join("B,%.2f,%.2f" % (a, b) for a, b in zip(xl, yl)))

    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.6))
    axes[0].scatter(x, y, s=50, color=CAT[0], edgecolors="white", zorder=3)
    axes[0].set_title("A. Monotone but nonlinear")
    axes[0].text(0.05, 0.9, "Pearson r = %.2f\nSpearman rho = %.2f" % (r_p, rho_s),
                 transform=axes[0].transAxes, va="top", fontsize=10,
                 bbox=dict(boxstyle="round,pad=0.35", fc="#F5F7FA", ec="0.7"))
    axes[0].set_xlabel("x"); axes[0].set_ylabel("y = 2^x")
    axes[1].scatter(xl[:-1], yl[:-1], s=50, color=CAT[0], edgecolors="white", zorder=3)
    axes[1].scatter(xl[-1], yl[-1], s=70, color=CAT[3], edgecolors="white", zorder=4)
    axes[1].annotate("leverage outlier\n(largest x, lowest y)", (xl[-1], yl[-1]),
                     (xl[-1] - 1.8, yl[-1] + 3.4), fontsize=9, ha="center")
    k, b = np.polyfit(xs, yl, 1)
    axes[1].plot(xs, k * xs + b, ls="--", color=CAT[3], lw=1.6)
    axes[1].set_title("B. Linear cloud plus one leverage outlier")
    axes[1].text(0.05, 0.9, "Pearson r = %.2f\nSpearman rho = %.2f" % (r_p2, rho_s2),
                 transform=axes[1].transAxes, va="top", fontsize=10,
                 bbox=dict(boxstyle="round,pad=0.35", fc="#F5F7FA", ec="0.7"))
    axes[1].set_xlabel("x"); axes[1].set_ylabel("y = 2x + noise")
    fig.suptitle("Pearson vs Spearman: when each one lies to you", y=1.02)
    save(fig, "05-spearman")


# ------------------------------------------------- 06/07 boxplot + violin
BOX_CSV = """tissue,tpm
Root,2
Root,4
Root,5
Root,7
Root,9
Root,11
Root,13
Root,16
Root,19
Root,23
Root,28
Root,34
Stem,8
Stem,12
Stem,15
Stem,18
Stem,21
Stem,24
Stem,27
Stem,30
Stem,34
Stem,39
Stem,45
Stem,52
Leaf,15
Leaf,22
Leaf,28
Leaf,34
Leaf,40
Leaf,47
Leaf,55
Leaf,63
Leaf,72
Leaf,84
Leaf,97
Leaf,110
Seed,40
Seed,55
Seed,68
Seed,80
Seed,95
Seed,110
Seed,128
Seed,145
Seed,168
Seed,190
Seed,215
Seed,245"""


def box_violin():
    dump("06-boxplot", BOX_CSV)
    _, c = csv_cols(BOX_CSV)
    tissues = ["Root", "Stem", "Leaf", "Seed"]
    data = [[float(v) for t0, v in zip(c["tissue"], c["tpm"]) if t0 == t]
            for t in tissues]

    fig, ax = plt.subplots(figsize=(6.2, 4.8))
    bp = ax.boxplot(data, tick_labels=tissues, patch_artist=True, widths=0.55,
                    medianprops=dict(color="black", lw=1.6),
                    meanprops=dict(marker="D", markerfacecolor="white",
                                   markeredgecolor="black", markersize=5))
    for patch, col in zip(bp["boxes"], CAT):
        patch.set_facecolor(col)
        patch.set_alpha(0.65)
    for i, d in enumerate(data, 1):
        ax.scatter(rng.normal(i, 0.05, len(d)), d, s=10, color="0.25",
                   alpha=0.6, zorder=3)
    ax.set_ylabel("Expression (TPM)")
    ax.set_title("Boxplot: boxes are IQR, whiskers 1.5x IQR, diamond = mean")
    save(fig, "06-boxplot")

    fig, ax = plt.subplots(figsize=(6.2, 4.8))
    vp = ax.violinplot(data, showextrema=False)
    for body, col in zip(vp["bodies"], CAT):
        body.set_facecolor(col)
        body.set_alpha(0.65)
    for i, d in enumerate(data, 1):
        q1, med, q3 = np.percentile(d, [25, 50, 75])
        ax.vlines(i, q1, q3, color="black", lw=4)
        ax.scatter(i, med, s=28, color="white", edgecolors="black", zorder=3)
    ax.set_xticks(range(1, 5), tissues)
    ax.set_ylabel("Expression (TPM)")
    ax.set_title("Violin plot: width encodes density, white dot = median")
    save(fig, "07-violin")


# ------------------------------------------------------------- 08/09 venn
def venn_treatment():
    csv = """set,size
drought_only,26
salt_only,20
cold_only,30
drought_and_salt,12
drought_and_cold,9
salt_and_cold,11
all_three,5
drought_total,42
salt_total,38
cold_total,45"""
    dump("08-venn-treatment", csv)

    fig, ax = plt.subplots(figsize=(6.2, 5.6))
    ax.set_aspect("equal")
    ax.grid(False)
    circles = [(0.00, 0.00, CAT[0]), (1.05, 0.00, CAT[1]), (0.52, 0.90, CAT[2])]
    for x0, y0, col in circles:
        ax.add_patch(Circle((x0, y0), 0.95, facecolor=col, alpha=0.35, edgecolor=col, lw=1.6))
    labels = [("drought\n26", -0.62, -0.35), ("salt\n20", 1.68, -0.35),
              ("cold\n30", 0.52, 1.42), ("12", 0.53, -0.62),
              ("9", 0.02, 0.45), ("11", 1.04, 0.45), ("5", 0.52, 0.12)]
    for t, x0, y0 in labels:
        ax.text(x0, y0, t, ha="center", va="center", fontsize=10.5)
    ax.text(-0.62, 0.85, "Drought DEG (42)", fontsize=10, color=CAT[0], fontweight="bold")
    ax.text(1.35, 0.85, "Salt DEG (38)", fontsize=10, color=CAT[1], fontweight="bold")
    ax.text(0.05, -1.25, "Cold DEG (45)", fontsize=10, color=CAT[2], fontweight="bold")
    ax.set_xlim(-1.4, 2.4)
    ax.set_ylim(-1.6, 1.9)
    ax.set_title("Venn diagram of DE genes under three stresses")
    ax.axis("off")
    save(fig, "08-venn-treatment")


def venn_ortholog():
    csv = """species,total_genes,one2one_orthologs
Fagopyrum_tataricum,33400,14200
Arabidopsis_thaliana,27600,14200"""
    dump("09-venn-ortholog", csv)

    fig, ax = plt.subplots(figsize=(6.0, 4.6))
    ax.set_aspect("equal")
    ax.grid(False)
    ax.add_patch(Circle((-0.55, 0), 1.15, facecolor=CAT[0], alpha=0.35, edgecolor=CAT[0], lw=1.6))
    ax.add_patch(Circle((0.55, 0), 1.15, facecolor=CAT[2], alpha=0.35, edgecolor=CAT[2], lw=1.6))
    ax.text(-1.35, 0.05, "19,200", ha="center", fontsize=12)
    ax.text(0.0, 0.05, "14,200", ha="center", fontsize=12, fontweight="bold")
    ax.text(1.35, 0.05, "13,400", ha="center", fontsize=12)
    ax.text(-1.1, 1.35, "F. tataricum\n(33,400 genes)", ha="center", fontsize=10.5, color=CAT[0])
    ax.text(1.1, 1.35, "A. thaliana\n(27,600 genes)", ha="center", fontsize=10.5, color=CAT[2])
    ax.set_xlim(-2.1, 2.1)
    ax.set_ylim(-1.5, 1.9)
    ax.set_title("Ortholog Venn between two species")
    ax.axis("off")
    save(fig, "09-venn-ortholog")


# ------------------------------------------------------------------ 10 upset
def upset():
    csv = """DEG,DEP,PHOS,DAM,size
1,0,0,0,402
0,1,0,0,121
0,0,0,1,108
1,1,0,0,96
0,0,1,0,74
1,0,0,1,58
1,0,1,0,41
0,1,0,1,27
0,1,1,0,33
1,1,1,0,18
1,1,1,1,9"""
    dump("10-upset", csv)
    _, c = csv_cols(csv)
    sets = ["DEG", "DEP", "PHOS", "DAM"]
    mask = np.vstack([[int(v) for v in c[s]] for s in sets]).T
    size = num(c, "size")
    order = np.argsort(-size)
    mask, size = mask[order], size[order]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.6, 5.2), sharex=True,
                                   gridspec_kw=dict(height_ratios=[3, 1.15], hspace=0.06))
    ax1.bar(range(len(size)), size, color=CAT[0], width=0.62)
    for i, v in enumerate(size):
        ax1.text(i, v + 8, str(int(v)), ha="center", fontsize=9)
    ax1.set_ylabel("Intersection size")
    ax1.set_title("UpSet plot: four omics layers, one membership matrix")
    for i, m in enumerate(mask):
        members = np.where(m == 1)[0]
        ax2.plot([i, i], [members.min(), members.max()], color="black", lw=1, zorder=2)
        for s in range(len(sets)):
            filled = m[s] == 1
            ax2.scatter(i, s, s=52 if filled else 14,
                        color="black" if filled else "0.85", zorder=3)
    ax2.set_yticks(range(len(sets)), sets)
    ax2.invert_yaxis()
    ax2.set_xticks([])
    ax2.grid(False)
    ax1.set_xlim(-0.7, len(size) - 0.3)
    save(fig, "10-upset")


# ---------------------------------------------------------------- 11 tpm dist
TPM_CSV = """gene,L1,L2,L3,L4,L5,L6
DWF4,3.1,3.4,3.0,12.5,13.1,12.8
CHS,88.4,95.1,91.7,54.2,57.8,55.6
CHI,12.2,13.0,12.6,9.8,10.4,10.1
F3H,25.6,27.8,26.3,19.4,20.9,20.1
ANS,1.8,2.1,1.9,6.7,7.0,6.9
PAL,41.0,44.6,42.8,30.5,32.2,31.4
BZR1,8.5,9.1,8.8,11.2,10.8,11.5
DET2,5.2,5.0,5.4,8.9,9.4,9.1
FLS,15.9,17.2,16.4,12.1,12.9,12.5
ANR,0.9,1.1,1.0,3.2,3.5,3.3"""


def tpm_dist():
    dump("11-tpm-dist", TPM_CSV)
    _, c = csv_cols(TPM_CSV)
    libs = [k for k in c if k != "gene"]
    data = [num(c, s) for s in libs]

    fig, ax = plt.subplots(figsize=(6.6, 4.8))
    bp = ax.boxplot(data, tick_labels=libs, patch_artist=True, widths=0.55)
    for patch, col in zip(bp["boxes"], CAT):
        patch.set_facecolor(col)
        patch.set_alpha(0.6)
    ax.set_yscale("log")
    ax.set_ylabel("TPM (log scale)")
    ax.set_title("TPM distribution per library (10 genes)")
    ax.text(0.02, 0.04, "same total-per-sample scale:\nL1-L3 vs L4-L6 shift is a real signal,\nnot a normalization artifact",
            transform=ax.transAxes, fontsize=8.5, color="0.35")
    save(fig, "11-tpm-dist")


if __name__ == "__main__":
    volcano()
    heatmap()
    corr_heatmap()
    pearson()
    spearman()
    box_violin()
    venn_treatment()
    venn_ortholog()
    upset()
    tpm_dist()
