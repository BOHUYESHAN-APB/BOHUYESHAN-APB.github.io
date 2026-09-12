# -*- coding: utf-8 -*-
"""Chapter 3 (dimension reduction & clustering) + chapter 4 (enrichment)."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path as MPath
import matplotlib.patches as mpatches
from scipy.cluster.hierarchy import linkage, dendrogram

from common import save, dump, csv_cols, num, CAT, UP, DOWN
from ch2_diff_expr import HEAT_CSV

rng = np.random.default_rng(7)


# --------------------------------------------------------------------- 12 PCA
def pca():
    csv = """sample,group,PC1,PC2
Z1_r1,Stage_I,-3.2,-0.8
Z1_r2,Stage_I,-2.8,0.4
Z1_r3,Stage_I,-3.5,0.1
Z1_r4,Stage_I,-2.4,-0.3
Z2_r1,Stage_II,0.1,1.8
Z2_r2,Stage_II,0.6,2.3
Z2_r3,Stage_II,-0.4,1.2
Z2_r4,Stage_II,0.3,2.8
Z3_r1,Stage_III,3.1,-0.5
Z3_r2,Stage_III,3.6,0.6
Z3_r3,Stage_III,2.7,-1.1
Z3_r4,Stage_III,3.3,0.2"""
    dump("12-pca", csv)
    _, c = csv_cols(csv)
    x, y = num(c, "PC1"), num(c, "PC2")
    groups = sorted(set(c["group"]))

    fig, ax = plt.subplots(figsize=(6.6, 5.6))
    for i, g in enumerate(groups):
        m = np.array(c["group"]) == g
        ax.scatter(x[m], y[m], s=60, color=CAT[i], edgecolors="white",
                   linewidths=0.8, zorder=3, label=g)
    load = [("DWF4", 0.85, 0.31), ("CHS", -0.72, 0.45),
            ("FLS", 0.81, -0.38), ("ANS", -0.66, 0.52)]
    for g, lx, ly in load:
        ax.annotate("", xy=(lx * 3.4, ly * 3.4), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color=CAT[4], lw=1.4))
        ax.text(lx * 3.75, ly * 3.75, g, color=CAT[4], fontsize=9, ha="center",
                fontweight="bold")
    ax.axhline(0, color="0.8", lw=0.8, zorder=1)
    ax.axvline(0, color="0.8", lw=0.8, zorder=1)
    ax.set_xlabel("PC1 (52.3% variance)")
    ax.set_ylabel("PC2 (21.7% variance)")
    ax.set_title("PCA score plot with gene loadings")
    ax.legend(loc="upper left")
    ax.set_xlim(-4.6, 4.6)
    ax.set_ylim(-3.2, 3.6)
    save(fig, "12-pca")


# -------------------------------------------------------------------- 13 UMAP
def umap():
    centers = {"C1": (-4.0, 2.0), "C2": (3.0, 3.0), "C3": (0.0, -4.0)}
    rows = ["cell,cluster,UMAP1,UMAP2"]
    pts = []
    for name, (cx, cy) in centers.items():
        for k in range(12):
            a, b = cx + rng.normal(0, 0.95), cy + rng.normal(0, 0.95)
            pts.append((a, b, name))
            rows.append("c%d,%s,%.2f,%.2f" % (len(pts), name, a, b))
    csv = "\n".join(rows)
    dump("13-umap", csv)
    _, c = csv_cols(csv)
    x, y = num(c, "UMAP1"), num(c, "UMAP2")
    cl = np.array(c["cluster"])

    fig, ax = plt.subplots(figsize=(6.2, 5.4))
    for i, name in enumerate(centers):
        m = cl == name
        ax.scatter(x[m], y[m], s=46, color=CAT[i], edgecolors="white",
                   linewidths=0.7, label=name)
    ax.set_xlabel("UMAP 1 (arbitrary units)")
    ax.set_ylabel("UMAP 2 (arbitrary units)")
    ax.set_title("UMAP embedding, 3 clusters x 12 cells")
    ax.legend(title="cluster")
    ax.text(0.02, 0.02, "axes have no physical unit:\nonly neighbor structure matters",
            transform=ax.transAxes, fontsize=8.5, color="0.35")
    save(fig, "13-umap")


# ------------------------------------------------------- 14 dendro + heatmap
def dendro_heatmap():
    _, c = csv_cols(HEAT_CSV)
    genes = c["gene"]
    samples = [k for k in c if k != "gene"]
    M = np.vstack([num(c, s) for s in samples]).T

    Z = linkage(M, method="average", metric="euclidean")
    fig = plt.figure(figsize=(6.8, 7.0))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 2.6], hspace=0.04)
    axd = fig.add_subplot(gs[0])
    axh = fig.add_subplot(gs[1])
    dendro = dendrogram(Z, ax=axd, no_labels=True, color_threshold=0,
                        above_threshold_color="0.4", link_color_func=lambda k: "0.4")
    axd.set_xticks([])
    axd.set_yticks([])
    axd.grid(False)
    axd.set_title("Hierarchical clustering of genes (average linkage)")
    order = dendro["leaves"]
    im = axh.imshow(M[order], cmap="YlGnBu", vmin=-2, vmax=2, aspect="auto")
    axh.set_xticks(range(len(samples)), samples, rotation=40, ha="right")
    axh.set_yticks(range(len(order)), [genes[i] for i in order], fontsize=8.5)
    axh.grid(False)
    cb = fig.colorbar(im, ax=axh, shrink=0.7)
    cb.set_label("row z-score of TPM")
    save(fig, "14-dendro-heatmap")


# --------------------------------------------------------------- 15 GO chord
CHORD_CSV = """gene,go_term
DWF4,BR_biosynthesis
BZR1,BR_signaling
BZR1,cell_elongation
SAUR19,cell_elongation
CHS,flavonoid_biosynthesis
F3H,flavonoid_biosynthesis
FLS,flavonoid_biosynthesis
ANS,flavonoid_biosynthesis
ANS,anthocyanin_biosynthesis
ANR,anthocyanin_biosynthesis"""


def chord():
    dump("15-go-chord", CHORD_CSV)
    _, c = csv_cols(CHORD_CSV)
    genes = list(dict.fromkeys(c["gene"]))
    terms = list(dict.fromkeys(c["go_term"]))
    rel = list(zip(c["gene"], c["go_term"]))
    gcol = {g: CAT[i % len(CAT)] for i, g in enumerate(genes)}

    fig, ax = plt.subplots(figsize=(8.6, 6.0))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.grid(False)
    R = 1.0

    def slots(order, a_start, a_end, gap_deg):
        deg = {n: sum(1 for g, t in rel if n in (g, t)) for n in order}
        avail = (a_end - a_start) - gap_deg * (len(order) - 1)
        out, cur = {}, a_start
        for n in order:
            w = avail * deg[n] / sum(deg.values())
            out[n] = (cur, cur + w)
            cur += w + gap_deg
        return out, deg

    gslot, gdeg = slots(genes, np.deg2rad(95), np.deg2rad(265), np.deg2rad(6))
    tslot, tdeg = slots(terms, np.deg2rad(-85), np.deg2rad(85), np.deg2rad(6))

    # ribbons first (under the arcs)
    gused = {g: 0.0 for g in genes}
    tused = {t: 0.0 for t in terms}
    for g, t in rel:
        gw = (gslot[g][1] - gslot[g][0]) / gdeg[g]
        tw = (tslot[t][1] - tslot[t][0]) / tdeg[t]
        a0 = gslot[g][0] + gused[g] * gw
        a1 = a0 + gw
        b0 = tslot[t][0] + tused[t] * tw
        b1 = b0 + tw
        gused[g] += gw
        tused[t] += tw
        ts = np.linspace(0, 1, 40)
        p0 = np.array([R * np.cos(a0), R * np.sin(a0)])
        p1 = np.array([R * np.cos(a1), R * np.sin(a1)])
        q0 = np.array([R * np.cos(b1), R * np.sin(b1)])
        q1 = np.array([R * np.cos(b0), R * np.sin(b0)])
        c1, c2 = p0 * 0.25, q0 * 0.25
        top = ((1 - ts) ** 3)[:, None] * p0 + 3 * ((1 - ts) ** 2 * ts)[:, None] * c1 \
            + 3 * ((1 - ts) * ts ** 2)[:, None] * c2 + (ts ** 3)[:, None] * q0
        c1b, c2b = p1 * 0.25, q1 * 0.25
        bot = ((1 - ts) ** 3)[:, None] * p1 + 3 * ((1 - ts) ** 2 * ts)[:, None] * c1b \
            + 3 * ((1 - ts) * ts ** 2)[:, None] * c2b + (ts ** 3)[:, None] * q1
        poly = np.vstack([top, bot[::-1]])
        ax.fill(poly[:, 0], poly[:, 1], color=gcol[g], alpha=0.35, lw=0)

    # node arcs + labels
    for g in genes:
        a0, a1 = gslot[g]
        ax.plot(R * np.cos(np.linspace(a0, a1, 30)), R * np.sin(np.linspace(a0, a1, 30)),
                color=gcol[g], lw=7, solid_capstyle="butt")
        am = (a0 + a1) / 2
        ax.text(1.12 * np.cos(am), 1.12 * np.sin(am), g, ha="right", va="center",
                fontsize=10, color=gcol[g], fontweight="bold")
    for t in terms:
        a0, a1 = tslot[t]
        ax.plot(R * np.cos(np.linspace(a0, a1, 30)), R * np.sin(np.linspace(a0, a1, 30)),
                color="0.25", lw=7, solid_capstyle="butt")
        am = (a0 + a1) / 2
        ax.text(1.12 * np.cos(am), 1.12 * np.sin(am), t.replace("_", " "), ha="left",
                va="center", fontsize=10, color="0.15")
    ax.set_xlim(-1.75, 2.15)
    ax.set_ylim(-1.35, 1.35)
    ax.set_title("GO chord diagram: genes (left) to terms (right)")
    save(fig, "15-go-chord")


# ------------------------------------------------------- 16/17 KEGG bubble/bar
KEGG_CSV = """pathway,enrich_factor,count,padj
Flavonoid biosynthesis,0.082,24,0.00012
Brassinosteroid biosynthesis,0.096,11,0.0031
Phenylpropanoid biosynthesis,0.064,31,0.00040
Plant hormone signal transduction,0.041,38,0.0021
Cutin suberine and wax biosynthesis,0.075,9,0.012
Starch and sucrose metabolism,0.037,22,0.0068
Circadian rhythm - plant,0.052,8,0.038
Amino sugar metabolism,0.028,15,0.041"""


def kegg_bubble():
    dump("16-kegg-bubble", KEGG_CSV)
    _, c = csv_cols(KEGG_CSV)
    ef = num(c, "enrich_factor")
    cnt = num(c, "count")
    y = -np.log10(num(c, "padj"))

    fig, ax = plt.subplots(figsize=(8.8, 5.8))
    sc = ax.scatter(ef, y, s=cnt * 28, c=y, cmap="viridis", alpha=0.8,
                    edgecolors="0.3", linewidths=0.7)
    for i, name in enumerate(c["pathway"]):
        short = name if len(name) <= 26 else name[:24] + ".."
        dx, dy = 0.004, 0.14
        if name == "Amino sugar metabolism":
            dx, dy = 0.004, -0.24
        elif name == "Circadian rhythm - plant":
            dx, dy = 0.004, 0.10
        ax.annotate(short, (ef[i], y[i]), (ef[i] + dx, y[i] + dy), fontsize=8.2)
    ax.set_ylim(1.05, 4.35)
    ax.set_xlabel("enrichment factor (DEG ratio / background ratio)")
    ax.set_ylabel("-log10 (padj)")
    ax.set_title("KEGG enrichment bubble plot")
    cb = fig.colorbar(sc, ax=ax, shrink=0.85)
    cb.set_label("-log10(padj)")
    handles = [plt.Line2D([], [], ls="", marker="o", color="0.6",
                          markersize=np.sqrt(n * 28) / 2, label=str(n)) for n in (10, 20, 30)]
    ax.legend(handles=handles, title="gene count", loc="lower right")
    ax.set_xlim(0.02, 0.125)
    save(fig, "16-kegg-bubble")


def kegg_bar():
    dump("17-kegg-bar", KEGG_CSV)
    _, c = csv_cols(KEGG_CSV)
    cnt = num(c, "count")
    neglog = -np.log10(num(c, "padj"))
    order = np.argsort(cnt)

    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    names = [c["pathway"][i] for i in order]
    ax.barh(range(len(order)), cnt[order], color=plt.cm.viridis(neglog[order] / neglog.max()),
            edgecolor="0.3", linewidth=0.5)
    ax.set_yticks(range(len(order)), names, fontsize=9)
    for i, v in enumerate(cnt[order]):
        ax.text(v + 0.4, i, str(int(v)), va="center", fontsize=8.5)
    ax.set_xlabel("DEG count mapped to pathway")
    ax.set_title("KEGG enrichment bar plot (color = -log10 padj)")
    sm = plt.cm.ScalarMappable(cmap="viridis", norm=plt.Normalize(0, neglog.max()))
    cb = fig.colorbar(sm, ax=ax, shrink=0.8)
    cb.set_label("-log10(padj)")
    save(fig, "17-kegg-bar")


# -------------------------------------------------------------------- 18 GSEA
GSEA_CSV = """gene,score,in_set
CHS,3.42,1
F3H,3.10,1
CHI,2.87,1
ANS,2.55,1
FLS,2.31,1
ANR,1.98,1
PAL,1.76,1
4CL,1.52,1
ACT7,1.31,0
EF1a,1.10,0
TUB6,0.92,0
RBCS,0.74,0
LHCB,0.55,0
SOD,-0.32,0
APX1,-0.51,0
CAT2,-0.77,0
NCED3,-0.98,0
PYL4,-1.24,0
ABF2,-1.47,0
WRKY1,-1.83,0"""


def gsea():
    dump("18-gsea", GSEA_CSV)
    _, c = csv_cols(GSEA_CSV)
    genes = c["gene"]
    s = num(c, "score")
    hit = np.array([int(v) for v in c["in_set"]], dtype=bool)
    nh = hit.sum()
    w = np.abs(s) * hit / np.abs(s[hit]).sum()
    miss = 1.0 / (len(s) - nh)
    run = np.cumsum(np.where(hit, w, -miss))
    peak = int(np.argmax(run))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.6, 5.4), sharex=True,
                                   gridspec_kw=dict(height_ratios=[2.6, 1], hspace=0.08))
    ranks = np.arange(1, len(s) + 1)
    ax1.plot(ranks, run, color=CAT[0], lw=2)
    ax1.fill_between(ranks, run, 0, where=run > 0, color=CAT[0], alpha=0.15)
    ax1.axhline(0, color="0.6", lw=0.8)
    ax1.axvline(peak, color="0.4", ls="--", lw=1)
    ax1.annotate("peak ES = %.2f at rank %d" % (run[peak - 1], peak),
                 (peak, run[peak - 1]), (peak - 7.5, run[peak - 1] - 0.02), fontsize=9.5)
    ax1.text(0.985, 0.955, "gene set: flavonoid biosynthesis (8 genes)\nNES = 2.31, FDR = 0.021",
             transform=ax1.transAxes, ha="right", va="top", fontsize=9.5,
             bbox=dict(boxstyle="round,pad=0.35", fc="#F5F7FA", ec="0.7"))
    ax1.set_ylabel("enrichment score (running sum)")
    ax1.set_title("GSEA: one set, one running sum")
    ax2.bar(ranks[hit], 1, color="black", width=0.7)
    ax2.bar(ranks[~hit], 1, color="0.85", width=0.7)
    ax2.set_yticks([])
    ax2.set_xlabel("genes ranked by score (down-regulated to the right)")
    for i in (0, peak - 1):
        ax2.text(ranks[i], 1.15, genes[i], ha="center", fontsize=8, rotation=45)
    ax2.set_ylim(0, 1.9)
    save(fig, "18-gsea")


if __name__ == "__main__":
    pca()
    umap()
    dendro_heatmap()
    chord()
    kegg_bubble()
    kegg_bar()
    gsea()
