# -*- coding: utf-8 -*-
"""Gallery post 3 (part B): functional genomics, epigenome, single-cell and
spatial figures 92-103."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

from scipy.cluster.hierarchy import linkage, dendrogram

from common import save, dump, CAT, UP, DOWN

rng = np.random.default_rng(2092)


# ------------------------------------------------------------------ 92 GO DAG
def go_dag():
    nodes = {
        "BP":        (0.50, 3.00, "biological_process", 0.0),
        "stimulus":  (0.20, 2.05, "response to stimulus", 3.2e-4),
        "metabolic": (0.62, 2.05, "metabolic process", 0.21),
        "cellular":  (0.90, 2.05, "cellular process", 0.64),
        "BR":        (0.08, 1.00, "response to BR", 1.8e-5),
        "GA":        (0.30, 1.00, "response to GA", 1.1e-3),
        "defense":   (0.50, 1.00, "defense response", 0.08),
        "phenyl":    (0.71, 1.00, "phenylpropanoid", 4.2e-3),
        "flavonoid": (0.92, 1.00, "flavonoid synthesis", 0.031),
    }
    edges = [("BP", "stimulus"), ("BP", "metabolic"), ("BP", "cellular"),
             ("stimulus", "BR"), ("stimulus", "GA"), ("stimulus", "defense"),
             ("metabolic", "phenyl"), ("metabolic", "flavonoid")]
    rows = ["child,parent,padj"]
    rows += ["%s,%s,%s" % (c, p, nodes[c][3]) for c, p in edges]
    dump("92-go-dag", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(10.8, 5.6))

    def ncol(p):
        if p == 0.0:
            return "0.55"
        return CAT[3] if p < 0.001 else (CAT[1] if p < 0.05 else "0.75")

    for c, p in edges:
        (x0, y0, _, _), (x1, y1, _, _) = nodes[p], nodes[c]
        ax.annotate("", xy=(x1, y1 + 0.17), xytext=(x0, y0 - 0.17),
                    arrowprops=dict(arrowstyle="->", color="0.55", lw=1.2))
    for name, (x, y, term, p) in nodes.items():
        w = 0.085 + 0.0042 * len(term)
        ax.add_patch(FancyBboxPatch((x - w / 2, y - 0.15), w, 0.30,
                                    boxstyle="round,pad=0.012",
                                    facecolor=ncol(p), edgecolor="0.3",
                                    alpha=0.90))
        ax.text(x, y, term, ha="center", va="center", fontsize=7.6,
                color="white" if p < 0.05 else "#222")
        if p > 0:
            ax.text(x, y - 0.22, "padj %.3g" % p, ha="center", fontsize=6.5,
                    color="0.35")
    ax.text(0.02, 0.45, "red: padj < 0.001, orange: padj < 0.05,\ngray: not significant",
            fontsize=8.5, color="0.35")
    ax.set_xlim(0, 1)
    ax.set_ylim(0.3, 3.3)
    ax.axis("off")
    ax.set_title("GO directed acyclic graph, BR treatment (simulated)")
    save(fig, "92-go-dag")


# ------------------------------------------------------- 93 ChIP profile+heat
def chip_profile():
    d = np.arange(-3.0, 3.01, 0.1)
    ip = 1.05 + 3.4 * np.exp(-0.5 * (d / 0.38) ** 2) + rng.normal(0, 0.06, len(d))
    igg = 1.0 + 0.12 * np.exp(-0.5 * (d / 0.9) ** 2) + rng.normal(0, 0.03, len(d))
    rows = ["distance_kb,ip,igg"]
    rows += ["%.1f,%.2f,%.2f" % v for v in zip(d, ip, igg)]
    dump("93-chip-profile", "\n".join(rows))
    m = rng.normal(0, 1, (28, 61)) * 0.6
    bump = np.exp(-0.5 * (d / 0.55) ** 2) * 2.4
    strength = rng.uniform(0.5, 1.6, 28)
    m = m + strength[:, None] * bump[None, :]
    m += rng.normal(0.6, 0.25, (28, 1))
    order = np.argsort(-m[:, 41:50].mean(1))
    m = m[order]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.0, 6.4), sharex=True,
                                   gridspec_kw=dict(height_ratios=[1, 1.5],
                                                    hspace=0.08))
    ax1.plot(d, ip, color=CAT[3], lw=2, label="BZR1-IP")
    ax1.plot(d, igg, color="0.55", lw=1.6, label="IgG")
    ax1.axvline(0, color="0.5", ls=":", lw=1)
    ax1.set_ylabel("mean ChIP-seq signal")
    ax1.legend(fontsize=9)
    ax1.set_title("TSS profile + signal heatmap (matrix code-generated)")
    im = ax2.imshow(m, aspect="auto", cmap="magma",
                    extent=[-3.05, 3.05, 28, 0])
    ax2.axvline(0, color="white", ls=":", lw=1)
    ax2.set_xlabel("distance to TSS (kb)")
    ax2.set_ylabel("genes (sorted)")
    fig.colorbar(im, ax=ax2, shrink=0.85, label="signal")
    save(fig, "93-chip")


# ---------------------------------------------------------------- 94 footprint
def footprint():
    off = np.arange(-50, 51, 5)
    ctrl = 52 + rng.normal(0, 2.4, len(off))
    tre = 46 + rng.normal(0, 2.2, len(off))
    mot = np.abs(off) <= 10
    tre[mot] = 17 + rng.normal(0, 2.0, mot.sum())
    tre[np.abs(off) == 15] += 13
    tre[np.abs(off) == 20] += 8
    rows = ["offset_bp,control,treated"]
    rows += ["%d,%.1f,%.1f" % v for v in zip(off, ctrl, tre)]
    dump("94-footprint", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.axvspan(-10, 10, color=CAT[0], alpha=0.10)
    ax.text(0, 58, "motif (TGAAG)", ha="center", fontsize=9, color=CAT[0])
    ax.plot(off, ctrl, "-o", ms=4, color="0.55", label="control root")
    ax.plot(off, tre, "-o", ms=4, color=CAT[3], label="+BR treatment")
    ax.annotate("protected region:\nTF occupies motif", (0, 17), (22, 26),
                fontsize=9, arrowprops=dict(arrowstyle="->", lw=1))
    ax.set_xlabel("distance to motif centre (bp)")
    ax.set_ylabel("Tn5 cut sites (normalized)")
    ax.legend(loc="lower right")
    ax.set_title("ATAC-seq transcription factor footprint (simulated)")
    save(fig, "94-footprint")


# ------------------------------------------------------------- 95 WGCNA tree
def wgcna_tree():
    n = 28
    base = rng.normal(0, 1, (n, 12))
    mods = ["turquoise"] * 12 + ["brown"] * 9 + ["blue"] * 7
    for sl, add in [(slice(0, 12), 2.2), (slice(12, 21), -1.8),
                    (slice(21, 28), 0.9)]:
        base[sl] += add * rng.normal(0, 1, (1, 12))
    Z = linkage(base, "average")
    fig = plt.figure(figsize=(9.6, 6.2))
    gs = fig.add_gridspec(2, 2, width_ratios=[3.2, 1],
                          height_ratios=[4, 0.28], hspace=0.04, wspace=0.06)
    axd = fig.add_subplot(gs[0, 0])
    dn = dendrogram(Z, ax=axd, no_labels=True, no_plot=False,
                    color_threshold=0, above_threshold_color="0.4",
                    link_color_func=lambda k: "0.4")
    axd.axis("off")
    axd.set_title("Gene dendrogram and module colors (simulated)")
    axm = fig.add_subplot(gs[1, 0])
    mcol = {"turquoise": "#40BFC0", "brown": "#A6761D", "blue": "#1F77B4"}
    for li, gi in enumerate(dn["leaves"]):
        axm.bar(li * 10 + 5, 1, width=10, color=mcol[mods[gi]])
    axm.set_xlim(axd.get_xlim())
    axm.set_ylim(0, 1)
    axm.axis("off")
    axt = fig.add_subplot(gs[0:2, 1])
    R = np.array([[0.81, -0.42], [0.15, 0.88], [-0.35, 0.12]])
    axt.imshow(R, cmap="RdYlBu_r", vmin=-1, vmax=1, aspect="auto")
    axt.set_xticks(range(2), ["seed weight", "dwf score"], rotation=20,
                   ha="right", fontsize=8.5)
    axt.set_yticks(range(3), ["turquoise", "brown", "blue"], fontsize=8.5)
    for i in range(3):
        for j in range(2):
            axt.text(j, i, "%.2f" % R[i, j], ha="center", va="center",
                     fontsize=8.5,
                     color="white" if abs(R[i, j]) > 0.6 else "#222")
    axt.set_title("module-trait r", fontsize=9)
    rows = ["gene,module"]
    rows += ["g%d,%s" % (i + 1, m) for i, m in enumerate(mods)]
    dump("95-wgcna-modules", "\n".join(rows))
    save(fig, "95-wgcna-tree")


# -------------------------------------------------------------- 96 methylation
def methylation():
    contexts = ["CG", "CHG", "CHH"]
    tissues = ["leaf", "flower", "seed"]
    vals = {"CG": [85, 88, 82], "CHG": [55, 61, 48], "CHH": [12, 18, 8]}
    rows = ["context,tissue,meth_pct"]
    for c in contexts:
        for t, v in zip(tissues, vals[c]):
            rows.append("%s,%s,%d" % (c, t, v))
    dump("96-methylation", "\n".join(rows))
    x = np.arange(3)
    w = 0.25
    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    for k, (t, col) in enumerate(zip(tissues, [CAT[2], CAT[1], CAT[0]])):
        v = [vals[c][k] for c in contexts]
        err = rng.uniform(1.5, 3.0, 3)
        ax.bar(x + (k - 1) * w, v, width=w, color=col, alpha=0.88,
               label=t, yerr=err, capsize=3)
    ax.set_xticks(x, contexts)
    ax.set_ylabel("methylation level (%)")
    ax.set_ylim(0, 100)
    ax.legend(title="tissue")
    ax.set_title("DNA methylation across sequence contexts (simulated)")
    ax.text(2.05, 22, "CHH: lowest and\nmost tissue-responsive", fontsize=8.5,
            color="0.35")
    save(fig, "96-methylation")


# ------------------------------------------------------------------- 97 Hi-C
def hic_map():
    n = 60
    ii, jj = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    d = np.abs(ii - jj)
    M = np.exp(-d / 7.0) * rng.lognormal(0, 0.18, (n, n))
    tads = [(0, 9), (10, 23), (24, 39), (40, 51), (52, 59)]
    for a, b in tads:
        M[a:b + 1, a:b + 1] *= 1.65
    M[16:20, 30:34] += 0.28                              # loop
    M[30:34, 16:20] += 0.28
    M = np.clip(M + M.T, 0, None)
    rows = ["tad,start_bin,end_bin"]
    rows += ["TAD%d,%d,%d" % (i + 1, a, b) for i, (a, b) in enumerate(tads)]
    dump("97-hic-tads", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.4, 6.6))
    im = ax.imshow(M, cmap="YlOrRd", origin="upper",
                   extent=[0, n, n, 0], vmin=0, vmax=np.percentile(M, 99))
    for a, b in tads:
        ax.add_patch(plt.Rectangle((a, a), b - a + 1, b - a + 1, fill=False,
                                   edgecolor=CAT[0], lw=1.3))
    ax.plot([16.5, 32.5], [16.5, 32.5], color=CAT[0], ls=":", lw=1)
    ax.text(24, 20, "loop", fontsize=8.5, color=CAT[0])
    ax.set_xlabel("bin (40 kb)")
    ax.set_ylabel("bin (40 kb)")
    ax.set_title("Hi-C contact map with TADs (matrix code-generated)")
    fig.colorbar(im, ax=ax, shrink=0.82, label="contact count")
    save(fig, "97-hic")


# ------------------------------------------------------------ 98 velocity
def velocity():
    t = rng.uniform(0, 1, 90)
    u = 2.6 * np.sin(np.pi * t ** 0.85) * (1 - t) ** 0.35 + rng.normal(0, 0.14, 90)
    s = 3.3 * t ** 0.75 + rng.normal(0, 0.16, 90)
    u = np.clip(u + 0.3, 0, None)
    rows = ["cell,spliced,unspliced"]
    rows += ["c%d,%.2f,%.2f" % (i + 1, a, b)
             for i, (a, b) in enumerate(zip(s, u))]
    dump("98-velocity", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.0, 5.8))
    sc = ax.scatter(s, u, c=t, cmap="viridis", s=42, edgecolors="white",
                    linewidths=0.5)
    tt = np.linspace(0, 1, 60)
    ax.plot(3.3 * tt ** 0.75, np.clip(2.6 * np.sin(np.pi * tt ** 0.85)
            * (1 - tt) ** 0.35 + 0.3, 0, None), ls="--", color="0.45",
            lw=1.6, label="dynamics")
    ax.annotate("induction:\nunspliced leads", (0.5, 2.4), (1.6, 2.75),
                fontsize=9, arrowprops=dict(arrowstyle="->", lw=1))
    fig.colorbar(sc, ax=ax, label="latent time")
    ax.set_xlabel("spliced (exonic)")
    ax.set_ylabel("unspliced (inronic)")
    ax.legend(loc="lower right")
    ax.set_title("RNA velocity phase portrait, DWF4 (simulated)")
    save(fig, "98-velocity")


# ---------------------------------------------------------- 99 composition
def composition():
    ctypes = ["stem cell", "cortex", "endodermis", "pericycle", "xylem", "phloem"]
    conds = ["control", "drought", "heat", "recovery"]
    frac = np.array([
        [14, 26, 20, 12, 15, 13],
        [8, 33, 24, 10, 11, 14],
        [11, 22, 18, 14, 19, 16],
        [13, 27, 21, 12, 14, 13],
    ])
    rows = ["condition,cell_type,pct"]
    for c, row in zip(conds, frac):
        for t, v in zip(ctypes, row):
            rows.append("%s,%s,%d" % (c, t, v))
    dump("99-composition", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    bottom = np.zeros(4)
    for k, t in enumerate(ctypes):
        ax.bar(conds, frac[:, k], bottom=bottom, label=t,
               color=CAT[k % 6], width=0.6)
        bottom += frac[:, k]
    ax.set_ylabel("proportion of cells (%)")
    ax.set_ylim(0, 112)
    ax.legend(ncol=3, fontsize=8.5, loc="upper center",
              bbox_to_anchor=(0.5, 1.08))
    ax.set_title("Cell-type composition shift under stress (simulated)")
    save(fig, "99-composition")


# --------------------------------------------------------- 100 marker heatmap
def marker_heatmap():
    clusters = ["stem cell", "cortex", "endodermis", "pericycle", "xylem", "phloem"]
    genes = ["m%d" % (i + 1) for i in range(18)]
    Z = rng.normal(0, 0.55, (18, 6))
    for k in range(6):
        Z[k * 3:(k + 1) * 3, k] += rng.uniform(2.1, 2.9)
    Z += rng.normal(0.25, 0.2, (18, 6))
    fig, ax = plt.subplots(figsize=(7.2, 7.0))
    im = ax.imshow(Z, cmap="RdBu_r", vmin=-2.5, vmax=3)
    ax.set_xticks(range(6), clusters, rotation=30, ha="right", fontsize=9)
    ax.set_yticks(range(18), genes, fontsize=7.5)
    for k in range(1, 6):
        ax.axhline(k * 3 - 0.5, color="white", lw=1.6)
    ax.grid(False)
    ax.set_title("Cluster marker genes, row = marker set (code-generated)")
    fig.colorbar(im, ax=ax, shrink=0.75, label="mean expression (z)")
    save(fig, "100-markers")


# ------------------------------------------------------- 101 CellChat circle
def ccc_circle():
    groups = ["epidermis", "cortex", "endodermis", "pericycle", "xylem", "phloem"]
    ang = np.linspace(90, 90 - 360, len(groups), endpoint=False)
    pos = {g: (np.cos(np.deg2rad(a)), np.sin(np.deg2rad(a)))
           for g, a in zip(groups, ang)}
    edges = [("epidermis", "cortex", 0.42, "PSK"), ("epidermis", "xylem", 0.18, "EPF"),
             ("cortex", "endodermis", 0.31, "CLE"), ("cortex", "phloem", 0.14, "PSK"),
             ("endodermis", "pericycle", 0.27, "CLE"), ("pericycle", "xylem", 0.36, "TDIF"),
             ("xylem", "phloem", 0.22, "CLE"), ("phloem", "pericycle", 0.12, "PSK"),
             ("endodermis", "cortex", 0.16, "IDA"), ("pericycle", "cortex", 0.10, "IDA"),
             ("xylem", "endodermis", 0.15, "TDIF")]
    rows = ["source,target,prob,pathway"]
    rows += ["%s,%s,%.2f,%s" % e for e in edges]
    dump("101-ccc-edges", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.6, 7.0))
    ax.set_aspect("equal")
    ax.axis("off")
    for a, b, p, _ in edges:
        (x0, y0), (x1, y1) = pos[a], pos[b]
        rad = 0.22 if np.cross([x0, y0, 0], [x1, y1, 0])[2] > 0 else -0.22
        ax.add_patch(FancyArrowPatch((x0 * 0.86, y0 * 0.86), (x1 * 0.86, y1 * 0.86),
                                     connectionstyle="arc3,rad=%.2f" % rad,
                                     arrowstyle="simple,head_length=8,head_width=6",
                                     color=CAT[0], alpha=0.25 + 0.5 * p,
                                     lw=1 + 6 * p, zorder=1))
    for g, (x, y) in pos.items():
        ax.scatter([x], [y], s=900, color=CAT[groups.index(g)], zorder=3,
                   edgecolors="white", linewidths=1.5)
        ax.text(x * 1.28, y * 1.28, g, ha="center", va="center", fontsize=9.5)
    ax.set_xlim(-1.7, 1.7)
    ax.set_ylim(-1.6, 1.7)
    ax.set_title("Cell-cell communication network (simulated)")
    save(fig, "101-ccc-circle")


# ------------------------------------------------------------ 102 LR bubble
def lr_bubble():
    pairs = ["PSK-PSKR1", "CLE41-PXY", "IDA-HAE", "EPF2-TMM", "TDIF-PXY", "SPB-SCN"]
    clusters = ["stem cell", "cortex", "endodermis", "vasculature", "guard cell"]
    prob = rng.uniform(0.1, 0.9, (6, 5)) * np.array(
        [[0.9, 0.6, 0.3, 0.2, 0.1], [0.3, 0.8, 0.7, 0.5, 0.2],
         [0.5, 0.3, 0.4, 0.2, 0.6], [0.6, 0.2, 0.3, 0.1, 0.9],
         [0.2, 0.5, 0.6, 0.8, 0.1], [0.7, 0.4, 0.3, 0.2, 0.3]])
    nl = rng.uniform(1.5, 9.0, (6, 5)) * (prob > 0.35)
    rows = ["pair,cluster,prob,neglog10p"]
    for i, pr in enumerate(pairs):
        for j, cl in enumerate(clusters):
            if prob[i, j] > 0.2:
                rows.append("%s,%s,%.2f,%.1f" % (pr, cl, prob[i, j], nl[i, j]))
    dump("102-lr-bubble", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.8, 5.6))
    for i, pr in enumerate(pairs):
        for j, cl in enumerate(clusters):
            if prob[i, j] > 0.2 and nl[i, j] > 0.5:
                ax.scatter(j, i, s=prob[i, j] * 640, c=nl[i, j],
                           cmap="YlGnBu", vmin=0, vmax=9,
                           edgecolor="0.35", linewidth=0.6, zorder=3)
    ax.set_xticks(range(5), clusters, rotation=20, ha="right")
    ax.set_yticks(range(6), pairs)
    ax.invert_yaxis()
    sm = plt.cm.ScalarMappable(cmap="YlGnBu", norm=plt.Normalize(0, 9))
    fig.colorbar(sm, ax=ax, shrink=0.8, label="-log10(p)")
    ax.set_title("Ligand-receptor communication probability (simulated)")
    save(fig, "102-lr-bubble")


# ------------------------------------------------------------ 103 spatial
def spatial():
    pts = []
    for gx in range(16):
        for gy in range(11):
            x, y = gx * 1.0 + rng.uniform(-0.18, 0.18), gy * 1.0 + rng.uniform(-0.18, 0.18)
            cx, cy = 7.5, 5.0
            r = np.hypot(x - cx, (y - cy) * 1.35)
            if r < 4.9 and rng.uniform() > 0.06:
                expr = np.exp(-0.5 * ((r - 2.6) / 0.55) ** 2) * 3.1 \
                    + np.exp(-0.5 * ((r - 0.4) / 0.5) ** 2) * 1.2 \
                    + rng.normal(0, 0.18)
                pts.append((x, y, max(expr, 0.02)))
    fig, ax = plt.subplots(figsize=(7.6, 6.4))
    xs, ys, es = zip(*pts)
    sc = ax.scatter(xs, ys, s=310, c=es, cmap="viridis", marker="o",
                    edgecolors="0.55", linewidths=0.5)
    ax.annotate("cortex (outer)", xy=(3.6, 8.7), xytext=(0.1, 10.3),
                fontsize=9, color="0.3",
                arrowprops=dict(arrowstyle="->", lw=0.9, color="0.4"))
    ax.annotate("endodermis:\nDWF4 high", xy=(9.9, 2.6),
                xytext=(10.7, 1.15), fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=1))
    ax.set_aspect("equal")
    ax.set_xlim(-0.9, 12.9)
    ax.set_ylim(-0.9, 10.9)
    ax.axis("off")
    ax.set_title("Spatial feature plot, 2D section (code-generated)")
    fig.colorbar(sc, ax=ax, shrink=0.8, label="DWF4 expression")
    save(fig, "103-spatial")


if __name__ == "__main__":
    go_dag()
    chip_profile()
    footprint()
    wgcna_tree()
    methylation()
    hic_map()
    velocity()
    composition()
    marker_heatmap()
    ccc_circle()
    lr_bubble()
    spatial()
