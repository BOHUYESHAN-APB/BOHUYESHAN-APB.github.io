# -*- coding: utf-8 -*-
"""Gallery post 4 (part B): metabolomics, metagenomics, AI/multi-omics and
statistics figures 121-133."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from common import save, dump, CAT, UP, DOWN

rng = np.random.default_rng(2121)


# --------------------------------------------------------------- 121 mirror
def mirror_plot():
    peaks = [(74, 40, 38), (88, 100, 96), (120, 65, 70), (135, 0, 22),
             (163, 30, 28), (205, 55, 52), (250, 18, 15)]
    rows = ["mz,sample_intensity,library_intensity"]
    rows += ["%d,%d,%d" % v for v in peaks]
    dump("121-mirror", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    for mz, lib, sam in peaks:
        ax.vlines(mz, 0, -lib, color="0.55", lw=2.4)
        ax.vlines(mz, 0, sam, color=CAT[0], lw=2.4)
        ax.text(mz, -lib - 7, str(mz), ha="center", fontsize=7.5, color="0.4")
    ax.text(135, 23, "unmatched", fontsize=8, color=CAT[3], ha="center")
    ax.axhline(0, color="0.2", lw=1)
    ax.text(395, 60, "sample (query)", color=CAT[0], fontsize=9.5, ha="right")
    ax.text(395, -60, "library (reference)", color="0.45", fontsize=9.5,
            ha="right")
    ax.text(52, 78, "cosine similarity 0.93", fontsize=10, fontweight="bold")
    ax.set_xlim(40, 410)
    ax.set_ylim(-125, 125)
    ax.set_xlabel("m/z")
    ax.set_ylabel("relative intensity (%)")
    ax.set_title("Mirror plot of MS/MS identification (simulated)")
    save(fig, "121-mirror")


# ------------------------------------------------------------ 122 van Krevelen
def van_krevelen():
    regions = {"lipid": (1.7, 0.10), "protein": (1.6, 0.42),
               "carbohydrate": (1.65, 0.85), "lignin": (1.1, 0.35),
               "tannin": (0.95, 0.68)}
    rows = ["compound,HC,OC,class"]
    fig, ax = plt.subplots(figsize=(7.8, 6.2))
    for k, (c, (hc, oc)) in enumerate(regions.items()):
        for i in range(8):
            x = rng.normal(hc, 0.14)
            y = np.clip(rng.normal(oc, 0.10), 0.02, 1.08)
            ax.scatter([x], [y], s=26, color=CAT[k], alpha=0.65,
                       linewidths=0)
            rows.append("C%d,%.2f,%.2f,%s" % (k * 8 + i + 1, x, y, c))
    dump("122-vankrevelen", "\n".join(rows))
    boxes = [("lipid", 1.5, 2.0, 0.0, 0.2), ("protein", 1.4, 1.8, 0.3, 0.55),
             ("carbohydrate", 1.5, 1.8, 0.7, 1.0),
             ("lignin", 0.9, 1.3, 0.25, 0.5), ("tannin", 0.8, 1.2, 0.55, 0.8)]
    for name, x0, x1, y0, y1 in boxes:
        ax.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False,
                                   edgecolor="0.6", ls="--", lw=1.1))
        ax.text((x0 + x1) / 2, y1 + 0.02, name, ha="center", fontsize=9,
                color="0.35")
    ax.set_xlim(0.4, 2.4)
    ax.set_ylim(0, 1.15)
    ax.set_xlabel("H/C ratio")
    ax.set_ylabel("O/C ratio")
    ax.set_title("Van Krevelen diagram of DOM compounds (simulated)")
    save(fig, "122-vankrevelen")


# ------------------------------------------------------------------ 123 blob
def blob_plot():
    bins = [("bin1", "Bacteria", 51, 32, 18.4), ("bin2", "Bacteria", 44, 21, 9.2),
            ("bin3", "Bacteria", 58, 45, 3.1), ("bin4", "Bacteria", 47, 15, 2.4),
            ("bin5", "Archaea", 41, 27, 2.8), ("bin6", "Archaea", 45, 38, 1.9),
            ("bin7", "Eukarya", 39, 52, 31.6), ("bin8", "Eukarya", 43, 33, 8.8),
            ("bin9", "Eukarya", 55, 12, 1.5), ("bin10", "undefined", 62, 24, 0.9),
            ("bin11", "undefined", 35, 9, 0.6), ("bin12", "Bacteria", 60, 18, 1.2)]
    rows = ["bin,taxonomy,gc,coverage,length_mb"]
    rows += ["%s,%s,%d,%d,%.1f" % v for v in bins]
    dump("123-blob", "\n".join(rows))
    tcol = {"Bacteria": CAT[0], "Archaea": CAT[1], "Eukarya": CAT[2],
            "undefined": "0.7"}
    fig, ax = plt.subplots(figsize=(7.8, 5.8))
    for name, tax, gc, cov, mb in bins:
        ax.scatter([gc], [cov], s=30 * np.sqrt(mb) * 8, color=tcol[tax],
                   alpha=0.75, edgecolors="white", linewidths=1, zorder=3)
        ax.text(gc, cov, name, fontsize=7, ha="center", va="center", zorder=4)
    for tax, col in tcol.items():
        ax.scatter([], [], s=70, color=col, label=tax)
    ax.legend(fontsize=9, loc="upper right")
    ax.set_xlabel("GC content (%)")
    ax.set_ylabel("coverage depth (x)")
    ax.set_title("Blob plot: bin taxonomy by GC and coverage (simulated)")
    save(fig, "123-blob")


# -------------------------------------------------------------------- 124 MOFA
def mofa():
    gens = ["WT", "brz", "GA3"]
    mu = [(0, 0), (-2.6, 1.3), (2.4, -1.1)]
    data = []
    for g, (mx, my) in zip(gens, mu):
        for i in range(8):
            data.append(("%s%d" % (g, i + 1), g, rng.normal(mx, 0.5),
                         rng.normal(my, 0.45)))
    rows = ["sample,genotype,factor1,factor2"]
    rows += ["%s,%s,%.2f,%.2f" % v for v in data]
    dump("124-mofa-factors", "\n".join(rows))
    views = [("mRNA", [46, 21, 9]), ("proteome", [30, 12, 22]),
             ("metabolite", [14, 31, 6])]
    rows = ["view,factor1_r2,factor2_r2,factor3_r2"]
    rows += ["%s,%d,%d,%d" % (v[0], *v[1]) for v in views]
    dump("124-mofa-r2", "\n".join(rows))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.8),
                                   gridspec_kw=dict(width_ratios=[1.15, 1]))
    gcol = dict(zip(gens, [CAT[2], CAT[3], CAT[0]]))
    for g in gens:
        sub = [v for v in data if v[1] == g]
        ax1.scatter([v[2] for v in sub], [v[3] for v in sub], s=46,
                    color=gcol[g], edgecolors="white", label=g)
    ax1.set_xlabel("Factor 1 (18%)")
    ax1.set_ylabel("Factor 2 (11%)")
    ax1.legend(fontsize=9)
    ax1.set_title("Factors", fontsize=11)
    x = np.arange(3)
    w = 0.25
    for k, col in enumerate([CAT[0], CAT[1], CAT[2]]):
        v = [views[j][1][k] for j in range(3)]
        ax2.bar(x + (k - 1) * w, v, width=w, color=col,
                label=views[k][0], alpha=0.88)
    ax2.set_xticks(x, ["Factor 1", "Factor 2", "Factor 3"])
    ax2.set_ylabel("variance explained (%)")
    ax2.legend(fontsize=8.5)
    ax2.set_title("Per-view R2", fontsize=11)
    save(fig, "124-mofa")


# ---------------------------------------------------------------- 125 saliency
def saliency():
    n = 60
    bases = list(rng.choice(list("ACGT"), n))
    motif1, motif2 = "TGAAG", "GTTGAC"
    for i, b in enumerate(motif1):
        bases[18 + i] = b
    for i, b in enumerate(motif2):
        bases[42 + i] = b
    attrib = rng.uniform(0.02, 0.10, n)
    for i, b in enumerate(motif1):
        attrib[18 + i] = rng.uniform(0.55, 0.95)
    for i, b in enumerate(motif2):
        attrib[42 + i] = rng.uniform(0.40, 0.75)
    rows = ["pos,base,attribution"]
    rows += ["%d,%s,%.2f" % v for v in zip(range(1, n + 1), bases, attrib)]
    dump("125-saliency", "\n".join(rows))
    bcol = {"A": "#2E7D32", "C": "#1565C0", "G": "#E65100", "T": "#C62828"}
    fig, ax = plt.subplots(figsize=(10.0, 4.2))
    ax.bar(range(1, n + 1), attrib, width=0.8,
           color=[bcol[b] for b in bases])
    for a, b in [(18, 23), (42, 48)]:
        ax.axvspan(a - 0.4, b + 0.4, color=CAT[3], alpha=0.08)
    ax.text(20.5, 1.0, "TGAAG", ha="center", fontsize=9, color=CAT[3])
    ax.text(45, 0.82, "GTTGAC", ha="center", fontsize=9, color=CAT[3])
    ax.set_xlabel("position in promoter (bp)")
    ax.set_ylabel("attribution score")
    ax.set_ylim(0, 1.1)
    ax.set_title("Deep-learning per-base attribution of promoter model (simulated)")
    save(fig, "125-saliency")


# ------------------------------------------------------------- 126 protein LM
def protein_embed():
    fams = {"kinase": (2.2, 2.4), "bHLH": (-2.4, 1.8), "P450": (1.9, -2.3),
            "LRR": (-2.2, -2.0), "DUF": (0.2, 0.1)}
    rows = ["protein,family,umap1,umap2"]
    fig, ax = plt.subplots(figsize=(7.8, 6.2))
    for k, (f, (mx, my)) in enumerate(fams.items()):
        for i in range(10):
            x, y = rng.normal(mx, 0.42), rng.normal(my, 0.40)
            ax.scatter([x], [y], s=36, color=CAT[k], alpha=0.75,
                       edgecolors="white", linewidths=0.6)
            rows.append("%s_%d,%s,%.2f,%.2f" % (f, i + 1, f, x, y))
        ax.text(mx, my + 0.85, f, ha="center", fontsize=10, fontweight="bold",
                color=CAT[k])
    dump("126-protein-embed", "\n".join(rows))
    ax.set_xlabel("UMAP 1")
    ax.set_ylabel("UMAP 2")
    ax.set_title("Protein language-model embedding space (simulated)")
    save(fig, "126-protein-embed")


# ----------------------------------------------------------- 127 pangenome graph
def pangenome_graph():
    nodes = {"A": (0.6, 2.6, 1.2, "core"), "B": (2.4, 2.6, 0.8, "core"),
             "C": (4.2, 3.3, 1.0, "accessory"), "D": (4.2, 1.9, 0.7, "accessory"),
             "E": (6.0, 2.6, 1.5, "core"), "R": (7.9, 2.6, 0.7, "repeat"),
             "F": (9.4, 3.4, 0.9, "accessory"), "G": (9.4, 1.8, 1.1, "core")}
    edges = [("A", "B"), ("B", "C"), ("B", "D"), ("C", "E"), ("D", "E"),
             ("E", "R"), ("R", "F"), ("R", "G"), ("F", "G"), ("A", "G")]
    rows = ["node1,node2"]
    rows += ["%s,%s" % e for e in edges]
    dump("127-pangenome-edges", "\n".join(rows))
    rows = ["node,length_kb,class"]
    rows += ["%s,%d,%s" % (n, int(v[2] * 20), v[3]) for n, v in nodes.items()]
    dump("127-pangenome-nodes", "\n".join(rows))
    ncol = {"core": CAT[0], "accessory": CAT[1], "repeat": CAT[3]}
    fig, ax = plt.subplots(figsize=(10.4, 5.0))
    for a, b in edges:
        (x0, y0, _, _), (x1, y1, _, _) = nodes[a], nodes[b]
        ax.plot([x0 + 0.45, x1 - 0.45], [y0, y1], color="0.45", lw=1.6, zorder=1)
    for n, (x, y, w, cls) in nodes.items():
        ax.add_patch(FancyBboxPatch((x - w / 2, y - 0.30), w, 0.60,
                                    boxstyle="round,pad=0.02",
                                    facecolor=ncol[cls], edgecolor="0.25",
                                    alpha=0.92, zorder=3))
        ax.text(x, y, "%s (%d kb)" % (n, int(w * 20)), ha="center",
                va="center", fontsize=7.5, color="white", zorder=4)
    ax.plot([4.2, 4.2], [3.55, 3.72], color=CAT[3], lw=0)
    ax.text(4.2, 4.15, "variant bubble: C in sample 1, D in sample 2",
            ha="center", fontsize=9, color="0.35")
    ax.annotate("repeat node R:\nthree incident edges", (7.9, 2.15),
                (7.6, 0.95), fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=1))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0.5, 4.5)
    ax.axis("off")
    ax.set_title("Pangenome graph assembly view (schematic)")
    save(fig, "127-pangenome")


# -------------------------------------------------------- 128 multi-omics UMAP
def multiomics():
    gens = ["WT", "brz", "GA3"]
    mu = [(0.2, 0.4), (-2.4, 1.6), (2.2, -1.4)]
    rows = ["sample,genotype,umap1_mrna,umap2_mrna,umap1_prot,umap2_prot,"
            "umap1_met,umap2_met"]
    data = []
    for gi, (g, (mx, my)) in enumerate(zip(gens, mu)):
        for i in range(8):
            row = ["%s%d" % (g, i + 1), g]
            jitter = [(0, 0), (-0.35, 0.45), (0.5, -0.3)][gi]
            coords = []
            for j in range(3):
                x = rng.normal(mx + jitter[0] * (j - 1) * 0.2, 0.5)
                y = rng.normal(my + jitter[1] * (j - 1) * 0.2, 0.45)
                coords += [x, y]
            data.append((row[0], g, *coords))
            rows.append("%s,%s," % (row[0], g) +
                        ",".join("%.2f" % c for c in coords))
    dump("128-multiomics", "\n".join(rows))
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.2), sharey=True)
    gcol = dict(zip(gens, [CAT[2], CAT[3], CAT[0]]))
    for k, (ax, name) in enumerate(zip(axes, ["mRNA", "proteome", "metabolite"])):
        for g in gens:
            sub = [v for v in data if v[1] == g]
            ax.scatter([v[2 + k * 2] for v in sub], [v[3 + k * 2] for v in sub],
                       s=38, color=gcol[g], edgecolors="white", label=g
                       if k == 0 else None)
        ax.set_title(name, fontsize=11)
        ax.set_xlabel("UMAP 1")
    axes[0].set_ylabel("UMAP 2")
    axes[0].legend(fontsize=9)
    fig.suptitle("Cross-omics latent spaces of the same 24 samples (simulated)",
                 y=1.0)
    save(fig, "128-multiomics")


# -------------------------------------------------------------------- 129 funnel
def funnel():
    se = np.linspace(0.035, 0.165, 12)
    eff = 0.42 + 0.9 * se ** 0.5 * rng.choice([-1, 1], 12, p=[0.75, 0.25]) \
        * rng.uniform(0.4, 1.4, 12) + rng.normal(0, 0.02, 12)
    rows = ["study,effect,se"]
    rows += ["S%d,%.2f,%.3f" % v for v in zip(range(1, 13), eff, se)]
    dump("129-funnel", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.0, 5.6))
    sxs = np.linspace(0, 0.19, 40)
    ax.fill_between(sxs, 0.42 - 1.96 * sxs, 0.42 + 1.96 * sxs,
                    color="0.88", zorder=1)
    ax.axvline(0.42, color="0.3", lw=1.2)
    ax.scatter(se, eff, s=40, color=CAT[0], edgecolors="white", zorder=3)
    ax.set_xlabel("standard error")
    ax.set_ylabel("effect size (log response ratio)")
    ax.set_ylim(-0.1, 1.0)
    ax.text(0.005, 0.44, "pooled estimate 0.42", fontsize=9)
    ax.annotate("small-study effects\nshifted right:\npossible publication bias",
                (0.145, 0.72), (0.075, 0.86), fontsize=8.5,
                arrowprops=dict(arrowstyle="->", lw=1))
    ax.set_title("Funnel plot, 12 studies (simulated)")
    save(fig, "129-funnel")


# ----------------------------------------------------------------- 130 dumbbell
def dumbbell():
    paths = [("BR signaling", 1.8, 2.6), ("flavonoid biosynthesis", 1.2, 2.4),
             ("cell wall loosening", 0.9, 2.1), ("photosynthesis", -1.4, -2.2),
             ("starch degradation", -0.6, -1.7), ("ABA signaling", 0.4, 1.3),
             ("nitrate transport", -1.1, -0.4), ("protein synthesis", -1.9, -2.6)]
    rows = ["pathway,nes_12h,nes_48h"]
    rows += ["%s,%.1f,%.1f" % v for v in paths]
    dump("130-dumbbell", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(8.2, 5.4))
    order = sorted(paths, key=lambda v: v[2])
    for k, (name, a, b) in enumerate(order):
        ax.plot([a, b], [k, k], color="0.8", lw=2.4, zorder=1)
        ax.scatter([a], [k], s=64, color=CAT[1], zorder=3, label="12 h"
                   if k == 0 else None)
        ax.scatter([b], [k], s=64, color=CAT[3], zorder=3, label="48 h"
                   if k == 0 else None)
        ax.text(max(a, b) + 0.14, k, "%.1f" % b, va="center", fontsize=8.5,
                color="0.4")
    ax.set_yticks(range(len(order)), [v[0] for v in order], fontsize=9.5)
    ax.axvline(0, color="0.5", lw=0.9)
    ax.set_xlabel("GSEA normalized enrichment score")
    ax.legend(loc="lower right")
    ax.set_title("Pathway NES at two time points (simulated)")
    save(fig, "130-dumbbell")


# ---------------------------------------------------------------- 131 waterfall
def waterfall():
    n = 20
    dy = np.sort(rng.uniform(-19, 27, n))[::-1]
    rows = ["genotype,dy_pct"]
    rows += ["G%d,%.1f" % (i + 1, v) for i, v in enumerate(dy)]
    dump("131-waterfall", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(9.0, 4.8))
    cols = [CAT[2] if v >= 0 else CAT[3] for v in dy]
    ax.bar(range(1, n + 1), dy, color=cols, alpha=0.9, width=0.7)
    ax.axhline(0, color="0.25", lw=1)
    ax.axhline(np.median(dy), color="0.5", ls=":", lw=1.1)
    ax.text(19.8, np.median(dy) + 0.8, "median %.1f%%" % np.median(dy),
            fontsize=8.5, color="0.4", ha="right")
    ax.set_xlabel("genotypes ranked by drought response")
    ax.set_ylabel("yield change vs control (%)")
    ax.set_title("Waterfall plot of drought response, 20 genotypes (simulated)")
    save(fig, "131-waterfall")


# -------------------------------------------------------------------- 132 pareto
def pareto():
    cats = ["index hopping", "adapter dimer", "low Q30", "duplication",
            "GC bias", "chimera", "N-heavy reads", "short insert",
            "poly-G tail", "other"]
    counts = [42, 31, 18, 12, 9, 7, 5, 4, 3, 2]
    rows = ["category,count"]
    rows += ["%s,%d" % v for v in zip(cats, counts)]
    dump("132-pareto", "\n".join(rows))
    cum = np.cumsum(counts) / sum(counts) * 100
    fig, ax = plt.subplots(figsize=(9.0, 4.9))
    ax.bar(cats, counts, color=CAT[0], alpha=0.85, width=0.62)
    ax2 = ax.twinx()
    ax2.plot(range(10), cum, "-o", color=CAT[3], lw=1.8, ms=4.5)
    ax2.axhline(80, color="0.5", ls="--", lw=1)
    ax2.text(9.4, 82, "80%", fontsize=8.5, color="0.4", ha="right")
    ax2.set_ylim(0, 105)
    ax2.set_ylabel("cumulative share (%)", color=CAT[3])
    for i, v in enumerate(counts):
        ax.text(i, v + 1, str(v), ha="center", fontsize=8.5)
    ax.set_ylabel("run failures")
    ax.set_xticks(range(10), cats, rotation=30, ha="right", fontsize=8.5)
    ax.set_title("Pareto chart of sequencing QC failures (simulated)")
    save(fig, "132-pareto")


# --------------------------------------------------------------------- 133 3D PCA
def pca3d():
    gens = ["WT", "brz", "GA3"]
    mu = [(2.4, 0.4, -0.6), (-2.2, 1.4, 0.8), (0.3, -2.2, -1.2)]
    rows = ["sample,genotype,pc1,pc2,pc3"]
    fig = plt.figure(figsize=(8.2, 6.6))
    ax = fig.add_subplot(projection="3d")
    for gi, (g, m) in enumerate(zip(gens, mu)):
        for i in range(10):
            x, y, z = rng.normal(m[0], 0.6), rng.normal(m[1], 0.55), \
                rng.normal(m[2], 0.5)
            ax.scatter(x, y, z, s=36, color=CAT[gi], edgecolors="white",
                       linewidths=0.5, label=g if i == 0 else None)
            rows.append("%s%d,%s,%.2f,%.2f,%.2f" % (g, i + 1, g, x, y, z))
    dump("133-pca3d", "\n".join(rows))
    ax.set_xlabel("PC1 (41%)")
    ax.set_ylabel("PC2 (24%)")
    ax.set_zlabel("PC3 (12%)")
    ax.view_init(elev=22, azim=118)
    ax.legend(loc="upper left", fontsize=9)
    ax.set_title("3D PCA of metabolome (simulated)")
    save(fig, "133-pca3d")


if __name__ == "__main__":
    mirror_plot()
    van_krevelen()
    blob_plot()
    mofa()
    saliency()
    protein_embed()
    pangenome_graph()
    multiomics()
    funnel()
    dumbbell()
    waterfall()
    pareto()
    pca3d()
