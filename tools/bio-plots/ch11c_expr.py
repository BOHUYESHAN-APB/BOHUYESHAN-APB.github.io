# -*- coding: utf-8 -*-
"""Gallery post 5 part C: SIMULATED expression-validation figures.

156 qPCR standard curve, 157 semi-quantitative RT-PCR gel + densitometry,
158 multi-gene tissue heatmap, 159 wild-vs-cultivar genotype x gene heatmap,
160 mutant-vs-WT expression boxes, 161 genotype x environment interaction,
162 semi-quant gray vs qPCR correlation, 163 expression-phenotype scatter.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from common import save, dump, csv_cols, num


# --------------------------------------------------- 156 qPCR std curve
def stdcurve():
    txt = """copies,Cq
1e6,19.42
1e5,22.87
1e4,26.31
1e3,29.79
1e2,33.24"""
    h, c = csv_cols(txt)
    x = np.log10(num(c, "copies"))
    y = num(c, "Cq")
    k, b = np.polyfit(x, y, 1)
    pred = k * x + b
    r2 = 1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    eff = (10 ** (-1 / k) - 1) * 100
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    xx = np.linspace(1.7, 6.3, 50)
    ax.plot(xx, k * xx + b, color="#4C72B0", lw=1.4)
    ax.scatter(x, y, s=52, color="#C44E52", zorder=3)
    ax.set_xlabel("log10(template copies)")
    ax.set_ylabel("Cq")
    ax.text(0.04, 0.10,
            "slope = %.2f\nintercept = %.1f\nR$^2$ = %.4f\nE = %.1f%%"
            % (k, b, r2, eff),
            transform=ax.transAxes, fontsize=9.5, va="bottom",
            bbox=dict(fc="white", ec="0.8", alpha=0.9))
    ax.set_title("qPCR standard curve: 10-fold dilution series, "
                 "efficiency near 100% (simulated)")
    save(fig, "156-qpcr-stdcurve")
    dump("156-qpcr-std", txt)
    print("156 fit: slope=%.3f R2=%.4f E=%.1f" % (k, r2, eff))


# ------------------------------------------------------- 157 gel
def gel():
    rng = np.random.default_rng(5157)
    lanes = ["M", "WT", "mut-1", "mut-2", "comp-1", "comp-2"]
    # actin-normalized target intensity per non-M lane (WT = 1.0)
    target_gray = np.array([1.00, 0.21, 0.33, 0.88, 0.74])
    actin_gray = np.array([0.97, 1.02, 0.95, 0.98, 1.01])
    fig = plt.figure(figsize=(8.6, 5.6))
    gs = fig.add_gridspec(2, 1, height_ratios=[2.6, 1.0], hspace=0.42)
    axg = fig.add_subplot(gs[0])
    W, H = 5.4, 2.0
    axg.add_patch(Rectangle((0.25, 0), W, H, fc="0.04", ec="0.3", lw=0.8))
    ladder = [1.86, 1.50, 1.16, 0.86, 0.58]
    for yy in ladder:
        axg.add_patch(Rectangle((0.42, yy - 0.045), 0.26, 0.09,
                                fc="0.85", ec="none"))
    axg.text(0.55, 1.93, "500", fontsize=6.5, color="0.8", ha="center")
    axg.text(0.55, 1.57, "250", fontsize=6.5, color="0.8", ha="center")
    for i, (ln, g) in enumerate(zip(lanes[1:], target_gray)):
        cx = 1.35 + i * 0.85
        inten = 0.28 + 0.62 * g * actin_gray[i] + rng.normal(0, 0.03)
        axg.add_patch(Rectangle((cx - 0.16, 1.30 - 0.09), 0.32, 0.18,
                                fc=str(min(0.92, inten)), ec="none"))
        yy = 0.98 - 0.09
        axg.add_patch(Rectangle((cx - 0.16, yy), 0.32, 0.18,
                                fc=str(min(0.92, 0.30 + 0.62 * actin_gray[i])),
                                ec="none"))
    axg.text(0.68, 1.31, "target 312 bp", fontsize=7.5, color="0.75",
             va="center")
    axg.text(0.68, 0.99, "actin 245 bp", fontsize=7.5, color="0.75",
             va="center")
    axg.set_xticks([0.55] + [1.35 + i * 0.85 for i in range(5)], lanes)
    axg.set_yticks([])
    axg.set_xlim(0.15, 5.75)
    axg.set_ylim(-0.06, 2.06)
    axg.set_title("Semi-quantitative RT-PCR gel, 28 cycles "
                  "(simulated image)")
    axb = fig.add_subplot(gs[1])
    rel = target_gray  # already actin-normalized, WT = 1.0
    axb.bar(range(5), rel, color=["#4C72B0", "#C44E52", "#C44E52",
                                  "#55A868", "#55A868"], width=0.6)
    axb.axhline(1.0, ls="--", color="0.4", lw=0.9)
    axb.set_xticks(range(5), lanes[1:], fontsize=9)
    axb.set_ylabel("target / actin (rel. WT)")
    axb.set_title("Densitometry of the gel above")
    for i, v in enumerate(rel):
        axb.text(i, v + 0.03, "%.2f" % v, ha="center", fontsize=8.5)
    save(fig, "157-rt-pcr-gel")
    rows = ["lane,target_gray,actin_gray,ratio_rel_WT"]
    for ln, tg, ag, rv in zip(lanes[1:], target_gray, actin_gray, rel):
        rows.append("%s,%.2f,%.2f,%.2f" % (ln, tg, ag, rv))
    dump("157-gel", "\n".join(rows))


# --------------------------------------------- 158 tissue heatmap
def geneheat():
    rng = np.random.default_rng(5158)
    genes = ["DWF4", "CPD", "DWF1", "DET2", "BR6OX1", "BR6OX2",
             "BZR1", "BAK1"]
    tis = ["seedling", "root", "leaf", "stem", "flower", "silique",
           "callus"]
    base = np.array([1.0, 0.4, 0.8, 1.2, 2.2, 0.7, 1.0, 1.4])
    prof = np.array([[1.0, 0.9, 1.1, 0.8, 1.0, 0.9, 1.0],   # DWF4-ish
                     [0.6, 0.5, 0.7, 1.6, 1.8, 0.8, 0.6],
                     [1.2, 1.0, 0.9, 0.8, 1.1, 1.0, 1.6],
                     [0.9, 0.8, 1.0, 1.0, 1.3, 0.9, 0.8],
                     [1.6, 0.8, 1.3, 2.4, 2.8, 1.2, 1.5],
                     [0.7, 0.6, 0.8, 1.2, 1.5, 0.9, 0.7],
                     [1.0, 1.1, 1.0, 1.1, 1.2, 1.1, 1.3],
                     [1.1, 1.3, 1.0, 1.0, 1.1, 0.9, 1.2]])
    M = np.log2(base[:, None] * prof *
                np.exp2(rng.normal(0, 0.18, (8, 7))))
    fig, ax = plt.subplots(figsize=(7.6, 5.2))
    im = ax.imshow(M, cmap="RdBu_r", vmin=-2.5, vmax=2.5)
    ax.set_xticks(range(len(tis)), tis, rotation=30, ha="right")
    ax.set_yticks(range(len(genes)), genes)
    for i in range(len(genes)):
        for j in range(len(tis)):
            ax.text(j, i, "%+.1f" % M[i, j], ha="center", va="center",
                    fontsize=7.6,
                    color="white" if abs(M[i, j]) > 1.4 else "0.15")
    ax.set_title("Tissue-expression map of 8 brassinosteroid genes\n"
                 "log2 TPM relative to row mean (simulated)")
    fig.colorbar(im, ax=ax, shrink=0.8, label="log2 ratio")
    save(fig, "158-gene-tissue-heatmap")
    rows = ["gene," + ",".join(tis)]
    for g, row in zip(genes, M):
        rows.append(g + "," + ",".join("%+.1f" % v for v in row))
    dump("158-gene-tissue", "\n".join(rows))


# ------------------------------------- 159 wild vs cultivar heatmap
def wildcultivar():
    rng = np.random.default_rng(5159)
    acc = ["wild-A", "wild-B", "wild-C", "wild-D",
           "cv-A", "cv-B", "cv-C", "cv-D"]
    genes = ["DWF4", "CPD", "DET2", "BR6OX1", "BZR1", "DWF1"]
    wild = np.array([[0.0, 0.3, -0.2, 1.1, 0.2, -0.3],
                     [0.2, 0.1, 0.4, 1.4, 0.4, 0.0],
                     [-0.3, 0.4, 0.0, 0.9, 0.1, -0.5],
                     [0.1, 0.0, 0.2, 1.2, 0.3, -0.1]])
    cult = wild * np.array([0.15, 0.25, 0.35, -0.4, 0.6, 0.2]) + \
        np.array([0.9, -0.7, -0.4, -1.3, 0.5, 0.8])
    M = np.vstack([wild, cult]) + rng.normal(0, 0.16, (8, 6))
    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    im = ax.imshow(M, cmap="PiYG", vmin=-2.0, vmax=2.0)
    ax.set_xticks(range(len(genes)), genes)
    ax.set_yticks(range(len(acc)), acc)
    for i in range(len(acc)):
        for j in range(len(genes)):
            ax.text(j, i, "%+.1f" % M[i, j], ha="center", va="center",
                    fontsize=8,
                    color="white" if abs(M[i, j]) > 1.3 else "0.15")
    ax.axhline(3.5, color="0.2", lw=1.6)
    ax.text(-0.62, 1.5, "wild", rotation=90, va="center", ha="right",
            fontsize=9, color="#2d6a4f")
    ax.text(-0.62, 5.5, "cultivar", rotation=90, va="center", ha="right",
            fontsize=9, color="#7a4a94")
    ax.set_title("Wild accessions vs cultivars, log2 expression "
                 "difference\nvs reference sample (simulated)")
    fig.colorbar(im, ax=ax, shrink=0.8, label="log2 difference")
    save(fig, "159-wild-cultivar")
    rows = ["accession," + ",".join(genes)]
    for a, row in zip(acc, M):
        rows.append(a + "," + ",".join("%+.1f" % v for v in row))
    dump("159-wild-cultivar", "\n".join(rows))


# --------------------------------------------------- 160 mutant boxes
def mutbox():
    rng = np.random.default_rng(5160)
    groups = ["WT", "dwf4-1", "dwf4-2", "complement"]
    mu = [1.00, 0.18, 0.27, 0.86]
    data = [np.clip(rng.normal(m, 0.06 * max(m, 0.3) + 0.03, 6), 0.02, None)
            for m in mu]
    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    bp = ax.boxplot(data, patch_artist=True, widths=0.55,
                    medianprops=dict(color="0.25"))
    for patch, col in zip(bp["boxes"],
                          ["#4C72B0", "#C44E52", "#C44E52", "#55A868"]):
        patch.set_facecolor(col)
        patch.set_alpha(0.55)
    for i, d in enumerate(data):
        ax.scatter(rng.normal(i + 1, 0.055, len(d)), d, s=16,
                   color="0.3", zorder=3)
        ax.text(i + 1, d.mean(), "%.2f" % d.mean(), ha="center",
                va="bottom", fontsize=9,
                bbox=dict(fc="white", ec="none", alpha=0.75, pad=0.8))
    ax.set_xticks(range(1, 5), groups)
    ax.set_ylabel("relative expression (2^-ddCt)")
    ax.text(0.985, 0.965,
            "one-way ANOVA p < 0.001;\nTukey groups a / b / b / a",
            transform=ax.transAxes, ha="right", va="top", fontsize=9,
            bbox=dict(fc="white", ec="0.8", alpha=0.9))
    ax.set_title("Target-gene expression in mutants vs WT vs "
                 "complemented line\n3 biological x 2 technical replicates "
                 "(simulated)")
    save(fig, "160-mutant-box")
    rows = ["genotype,mean,sd,n"]
    for g, d in zip(groups, data):
        rows.append("%s,%.2f,%.3f,6" % (g, d.mean(), d.std()))
    dump("160-mutant-box", "\n".join(rows))


# ------------------------------------------- 161 genotype x environment
def gxe():
    rng = np.random.default_rng(5161)
    envs = ["control", "drought", "low temp", "high light"]
    geno = {"wild": np.array([1.00, 2.10, 1.70, 1.40]),
            "cultivar": np.array([1.05, 1.15, 1.10, 1.20]),
            "mutant": np.array([0.20, 0.42, 0.35, 0.30])}
    cols = {"wild": "#55A868", "cultivar": "#4C72B0", "mutant": "#C44E52"}
    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    for g, v in geno.items():
        se = 0.08 * v + 0.02
        ax.errorbar(range(4), v, yerr=se, marker="o", ms=6, lw=1.6,
                    color=cols[g], label=g, capsize=3)
        v2 = v + rng.normal(0, 0.03, 4)
        ax.plot(range(4), v2, "o", ms=3.5, color=cols[g], alpha=0.6)
    ax.set_xticks(range(4), envs)
    ax.set_ylabel("relative expression")
    ax.legend(title="genotype", fontsize=9)
    ax.set_title("Genotype x environment induction of a stress-responsive "
                 "gene\nwild shows strong induction, cultivar stays flat, "
                 "mutant stays low (simulated)")
    save(fig, "161-gxe-lines")
    rows = ["genotype," + ",".join(envs)]
    for g, v in geno.items():
        rows.append(g + "," + ",".join("%.2f" % x for x in v))
    dump("161-gxe", "\n".join(rows))


# ------------------------------------------- 162 gray vs qPCR corr
def grayqpcr():
    rng = np.random.default_rng(5162)
    gray = np.array([1.00, 0.78, 0.55, 0.42, 0.30, 0.18,
                     1.10, 0.90, 0.62, 0.35, 0.24, 0.12])
    qpcr = np.clip(gray * 0.92 + rng.normal(0, 0.035, 12), 0.02, None)
    k, b = np.polyfit(gray, qpcr, 1)
    r = np.corrcoef(gray, qpcr)[0, 1]
    xx = np.linspace(0.05, 1.15, 50)
    fig, ax = plt.subplots(figsize=(6.6, 5.2))
    ax.plot(xx, k * xx + b, color="#4C72B0", lw=1.4)
    ax.scatter(gray, qpcr, s=52, color="#C44E52", zorder=3)
    ax.set_xlabel("semi-quantitative gel gray ratio")
    ax.set_ylabel("qPCR 2^-ddCt")
    ax.text(0.05, 0.93, "Pearson r = %.3f\ny = %.2f x + %.2f" % (r, k, b),
            transform=ax.transAxes, fontsize=9.5, va="top",
            bbox=dict(fc="white", ec="0.8", alpha=0.9))
    ax.set_title("Semi-quantitative gel vs qPCR quantification of the "
                 "same 12\nsamples (simulated)")
    save(fig, "162-gray-vs-qpcr")
    rows = ["sample,gel_gray,qpcr"]
    for i, (g, q) in enumerate(zip(gray, qpcr)):
        rows.append("S%02d,%.2f,%.3f" % (i + 1, g, q))
    dump("162-gray-qpcr", "\n".join(rows))
    print("162 fit: r=%.4f slope=%.3f" % (r, k))


# --------------------------------------- 163 expression vs phenotype
def exprpheno():
    rng = np.random.default_rng(5163)
    expr = np.round(np.linspace(0.15, 1.45, 12), 2)
    leaf = np.clip(38 + 34 * expr + rng.normal(0, 5.2, 12), 0, None)
    k, b = np.polyfit(expr, leaf, 1)
    r = np.corrcoef(expr, leaf)[0, 1]
    xx = np.linspace(0.1, 1.5, 50)
    fig, ax = plt.subplots(figsize=(7.0, 5.2))
    ax.plot(xx, k * xx + b, color="#4C72B0", lw=1.4)
    ax.scatter(expr, leaf, s=56, color="#55A868", zorder=3)
    ax.annotate("low-BR dwarf line", (expr[0], leaf[0]),
                textcoords="offset points", xytext=(12, -4), fontsize=9)
    ax.annotate("over-expression line", (expr[-1], leaf[-1]),
                textcoords="offset points", xytext=(-88, -14), fontsize=9)
    ax.set_xlabel("DWF4 relative expression")
    ax.set_ylabel("leaf blade angle (deg)")
    ax.text(0.05, 0.93, "r = %.2f,  p = 3e-07" % r,
            transform=ax.transAxes, fontsize=10, va="top",
            bbox=dict(fc="white", ec="0.8", alpha=0.9))
    ax.set_title("Expression level vs organ phenotype across 12 "
                 "transgenic lines (simulated)")
    save(fig, "163-expr-pheno")
    rows = ["line,expression,leaf_angle_deg"]
    for i, (e, l) in enumerate(zip(expr, leaf)):
        rows.append("L%02d,%.2f,%.1f" % (i + 1, e, l))
    dump("163-expr-pheno", "\n".join(rows))
    print("163 fit: r=%.4f slope=%.2f" % (r, k))


if __name__ == "__main__":
    stdcurve()
    gel()
    geneheat()
    wildcultivar()
    mutbox()
    gxe()
    grayqpcr()
    exprpheno()
