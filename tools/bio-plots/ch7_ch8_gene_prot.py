# -*- coding: utf-8 -*-
"""Chapter 7 (Sankey) + chapter 8 (gene/protein专题) figures."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.stats import gaussian_kde

from common import save, dump, csv_cols, num, CAT

rng = np.random.default_rng(31)


def _hband(ax, x0, t0, t1, x1, u0, u1, color, alpha=0.45):
    """Vertical ribbon between (x0, t0..t1) and (x1, u0..u1)."""
    ts = np.linspace(0, 1, 40)
    xm = (x0 + x1) / 2
    top_t = np.column_stack([(1 - ts) ** 3, 3 * (1 - ts) ** 2 * ts,
                             3 * (1 - ts) * ts ** 2, ts ** 3])
    p0, c1 = np.array([x0, t0]), np.array([xm, t0])
    c2, p1 = np.array([xm, u0]), np.array([x1, u0])
    top = top_t @ np.vstack([p0, c1, c2, p1])
    q0, d1 = np.array([x0, t1]), np.array([xm, t1])
    d2, q1 = np.array([xm, u1]), np.array([x1, u1])
    bot = top_t @ np.vstack([q0, d1, d2, q1])
    poly = np.vstack([top, bot[::-1]])
    ax.fill(poly[:, 0], poly[:, 1], color=color, alpha=alpha, lw=0)


# ----------------------------------------------------------------- 34 sankey
def sankey():
    csv = """flow,from,to,value_M
mapping,total,mapped,10.8
mapping,total,unmapped,1.2
region,mapped,CDS,6.3
region,mapped,intron_intergenic,3.1
region,mapped,antisense,1.4"""
    dump("34-sankey", csv)

    fig, ax = plt.subplots(figsize=(9.0, 5.4))
    ax.grid(False)
    X0, X1, X2 = 0.04, 0.46, 0.88
    W = 0.07
    SCALE = 1 / 12.3 * 10.0
    # column 0: total
    ax.add_patch(Rectangle((X0, 0), W, 12.0 * SCALE, facecolor="0.55"))
    ax.text(X0 - 0.03, 6.0 * SCALE, "raw reads\n12.0 M", ha="right", va="center",
            fontsize=10.5)
    # column 1
    y_map = 0.0
    ax.add_patch(Rectangle((X1, y_map), W, 10.8 * SCALE, facecolor=CAT[0]))
    y_unm = 10.8 * SCALE + 0.5
    ax.add_patch(Rectangle((X1, y_unm), W, 1.2 * SCALE, facecolor="0.75"))
    ax.text(X1 + W / 2, y_map + 5.4 * SCALE, "mapped\n10.8 M", ha="center", va="center",
            fontsize=9.5, color="white")
    ax.text(X1 + W / 2, y_unm + 0.6 * SCALE, "unmapped\n1.2 M", ha="center", va="center",
            fontsize=9.5, color="0.2")
    # column 2
    parts = [("CDS  6.3 M", 6.3, CAT[0]), ("intron + intergenic  3.1 M", 3.1, CAT[1]),
             ("antisense  1.4 M", 1.4, CAT[2])]
    ycur = 0.0
    edges = []
    for label, v, col in parts:
        ax.add_patch(Rectangle((X2, ycur), W, v * SCALE, facecolor=col))
        ax.text(X2 + W + 0.03, ycur + v * SCALE / 2, label, va="center", fontsize=10)
        edges.append((ycur, ycur + v * SCALE, col))
        ycur += v * SCALE + 0.4
    # ribbons
    _hband(ax, X0 + W, 0.0, 10.8 * SCALE, X1, 0.0, 10.8 * SCALE, CAT[0], alpha=0.30)
    _hband(ax, X0 + W, 10.8 * SCALE, 12.0 * SCALE, X1, y_unm, y_unm + 1.2 * SCALE,
           "0.7", alpha=0.35)
    y_from = 0.0
    for (ya, yb, col) in edges:
        v = (yb - ya) / SCALE
        _hband(ax, X1 + W, y_from, y_from + v * SCALE, X2, ya, yb, col, alpha=0.35)
        y_from += v * SCALE
    ax.set_xlim(-0.28, 1.18)
    ax.set_ylim(-0.5, 10.8)
    ax.axis("off")
    ax.set_title("Sankey diagram: where do 12 M reads land (hisat2 featureCounts style)")
    save(fig, "34-sankey")


# -------------------------------------------------- 35 protein anchors + pLDDT
PLDDT_CSV = """residue,plddt,anchor
1,48,
2,52,
3,57,
4,62,
5,68,
6,72,
7,75,
8,78,
9,81,
10,85,
11,89,
12,91,S12 catalytic
13,92,
14,94,
15,95,
16,94,
17,93,
18,91,
19,92,
20,90,
21,88,
22,86,
23,84,
24,82,
25,78,
26,75,
27,76,
28,77,
29,79,
30,88,D30 strand
31,90,
32,91,
33,89,
34,87,
35,81,
36,84,
37,87,
38,89,
39,91,
40,92,
41,93,K41 catalytic
42,92,
43,90,
44,88,
45,85,
46,82,
47,70,
48,55"""


def protein_anchor():
    dump("35-protein-plddt", PLDDT_CSV)
    _, c = csv_cols(PLDDT_CSV)
    res = num(c, "residue")
    pl = num(c, "plddt")
    anchors = [(12, "S12"), (30, "D30"), (41, "K41")]

    AF = [("#FF7D45", 0, 50), ("#FFDB13", 50, 70), ("#65CBF3", 70, 90), ("#0053D6", 90, 101)]

    def col_of(v):
        for col, a, b in AF:
            if a <= v < b:
                return col

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.4, 4.9),
                                   gridspec_kw=dict(width_ratios=[1, 1.35]))
    # ---- left: cartoon
    ax1.grid(False)
    ax1.axis("off")
    ax1.set_xlim(0, 12)
    ax1.set_ylim(0, 7)
    ax1.set_title("cartoon (colored by pLDDT)")
    t = np.linspace(0, 1, 200)
    coil = np.column_stack([2.0 + 2.6 * t, 3.6 + 0.5 * np.sin(t * 6 * np.pi)])
    ax1.plot(coil[:, 0], coil[:, 1], color="#65CBF3", lw=6, solid_capstyle="round")
    ax1.plot([4.6, 6.2], [4.15, 4.9], color="#0053D6", lw=9, solid_capstyle="round")
    ax1.annotate("", xy=(8.6, 4.4), xytext=(6.9, 4.6),
                 arrowprops=dict(arrowstyle="-|>", color="#0053D6", lw=7))
    ax1.plot([8.7, 10.4], [4.15, 3.4], color="#0053D6", lw=9, solid_capstyle="round")
    ax1.plot([1.4, 2.0], [3.5, 3.7], color="#FFDB13", lw=6, solid_capstyle="round")
    ax1.plot([10.4, 11.2], [3.4, 3.0], color="#FF7D45", lw=6, solid_capstyle="round")
    ax1.text(1.15, 4.6, "N", fontsize=11, fontweight="bold")
    ax1.text(11.35, 2.5, "C", fontsize=11, fontweight="bold")
    apos = {12: (4.85, 5.35), 30: (8.35, 4.95), 41: (9.9, 4.15)}
    for rr, name in anchors:
        x, y = apos[rr]
        ax1.scatter([x], [y], s=90, facecolor="white", edgecolor="#C62828",
                    linewidth=1.6, zorder=6)
        ax1.text(x, y, name[0], ha="center", va="center", fontsize=7.5,
                 color="#C62828", zorder=7, fontweight="bold")
        ax1.annotate(name, (x, y), (x + 0.28, y + 0.62), fontsize=8.5,
                     color="#C62828", fontweight="bold")
    ax1.text(6, 0.6, "circles 1-3: conserved anchor residues\n(motif-anchored, see MSA)",
             ha="center", fontsize=9, color="0.3")
    # ---- right: pLDDT per residue
    for col, a, b in AF:
        ax2.axhspan(a, b, color=col, alpha=0.12)
    for i in range(len(res) - 1):
        ax2.plot(res[i:i + 2], pl[i:i + 2], color=col_of((pl[i] + pl[i + 1]) / 2), lw=1.8)
    for rr, name in anchors:
        ax2.axvline(rr, color="#C62828", ls="--", lw=1)
        ax2.scatter([rr], [pl[rr - 1]], s=46, facecolor="white", edgecolor="#C62828",
                    linewidth=1.5, zorder=5)
    ax2.text(0.35, 96.5, "very high > 90", fontsize=8.5, color="#0053D6")
    ax2.text(0.35, 84.5, "confident 70-90", fontsize=8.5, color="#0288D1")
    ax2.text(0.35, 60.5, "low 50-70", fontsize=8.5, color="#B8860B")
    ax2.text(0.35, 44.5, "very low < 50", fontsize=8.5, color="#E65100")
    ax2.set_ylim(20, 101)
    ax2.set_xlim(0, 49)
    ax2.set_xlabel("residue number")
    ax2.set_ylabel("pLDDT")
    ax2.set_title("per-residue confidence with anchors marked")
    save(fig, "35-protein-anchor")


# ------------------------------------------------------- 36 evidence matrix
def evidence_matrix():
    csv = """gene,DEG,WGCNA_hub,enriched_pathway,promoter_element,conserved_residue,qPCR
DWF4,1,1,1,1,1,1
BZR1,1,1,1,0,1,1
CHS,1,1,1,1,1,1
ANS,1,0,1,1,1,1
FLS,1,0,1,0,1,0
ANR,1,1,0,1,0,0"""
    dump("36-evidence-matrix", csv)
    _, c = csv_cols(csv)
    genes = c["gene"]
    evs = [k for k in c if k != "gene"]

    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.grid(False)
    for i, g in enumerate(genes):
        for j, e in enumerate(evs):
            on = c[e][i] == "1"
            ax.scatter(j, i, s=640, marker="o",
                       facecolor=CAT[0] if on else "white",
                       edgecolor="0.4", linewidth=1.1)
    ax.set_xticks(range(len(evs)), [e.replace("_", " ") for e in evs],
                  rotation=20, ha="right", fontsize=9.5)
    ax.set_yticks(range(len(genes)), genes)
    ax.set_xlim(-0.6, len(evs) - 0.4)
    ax.set_ylim(len(genes) - 0.4, -0.6)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_title("Evidence matrix: every claim a gene makes needs a filled circle")
    save(fig, "36-evidence-matrix")


# ------------------------------------------------------- 37 tissue expression
def tissue_expression():
    csv = """tissue,DWF4,CHS,ANR
Root,4.2,8.1,2.2
Stem,6.8,5.4,1.8
Leaf,3.1,21.7,0.9
Flower,12.5,45.2,15.6
Seed,28.4,88.3,42.1"""
    dump("37-tissue-expression", csv)
    _, c = csv_cols(csv)
    tissues = c["tissue"]
    x = np.arange(len(tissues))
    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    for i, g in enumerate(["DWF4", "CHS", "ANR"]):
        ax.bar(x + (i - 1) * 0.26, num(c, g), 0.24, label=g, color=CAT[i])
    ax.set_xticks(x, tissues)
    ax.set_ylabel("TPM")
    ax.set_title("Where is it expressed? grouped bar by tissue")
    ax.legend(title="gene")
    for i, g in enumerate(["DWF4", "CHS", "ANR"]):
        for j, v in enumerate(num(c, g)):
            ax.text(x[j] + (i - 1) * 0.26, v + 1.2, "%.0f" % v, ha="center", fontsize=7.5)
    save(fig, "37-tissue-expression")


# ------------------------------------------------------ 38 promoter elements
def promoter_cis():
    csv = """element,start,end,strand
TATA-box,-29,-24,+
CAAT-box,-152,-145,+
ABRE,-412,-405,+
G-box,-588,-583,+
ARE,-615,-610,-
E-box,-921,-916,+
ABRE,-1035,-1028,+
MYB1AT,-1210,-1204,+
W-box,-1330,-1323,-
TGA1,-1520,-1514,+
skn-1_like,-1770,-1763,+"""
    dump("38-promoter-cis", csv)
    _, c = csv_cols(csv)

    fam_color = {"TATA-box": "0.3", "CAAT-box": "0.55", "ABRE": CAT[3],
                 "G-box": CAT[0], "E-box": CAT[0], "MYB1AT": CAT[2],
                 "W-box": CAT[4], "TGA1": CAT[1], "ARE": CAT[5],
                 "skn-1_like": CAT[6]}
    fig, ax = plt.subplots(figsize=(9.6, 4.2))
    ax.grid(False)
    for name, s, e, strand in zip(c["element"], num(c, "start"), num(c, "end"),
                                  c["strand"]):
        up = strand == "+"
        y = 1.25 if up else -1.25
        ax.add_patch(Rectangle((s, y - 0.22), e - s + 26, 0.44,
                               facecolor=fam_color[name], edgecolor="0.2"))
        ax.text(s + (e - s) / 2 + 13, y + (0.34 if up else -0.42), name,
                ha="center", fontsize=8, rotation=30, color=fam_color[name])
    ax.plot([-2000, 120], [0, 0], color="black", lw=1.6)
    ax.annotate("", xy=(120, 0), xytext=(40, 0),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.6))
    ax.text(125, 0, "TSS /\nATG", va="center", fontsize=9)
    ax.set_xlim(-2050, 320)
    ax.set_ylim(-2.5, 2.7)
    ax.set_yticks([])
    ax.set_xticks(range(-2000, 1, 250))
    ax.set_xlabel("position relative to transcription start site (bp)")
    ax.set_title("Promoter (2 kb upstream) cis-element map, above = + strand")
    ax.spines["left"].set_visible(False)
    save(fig, "38-promoter-cis")


# ------------------------------------------------------ 39 BRGA pathway dyn
def brga_dynamics():
    csv = """stage,BRGA,DWF4,BZR1,CPD
globular,1.2,0.8,1.5,0.6
heart,2.8,2.2,2.4,1.8
torpedo,5.1,4.4,3.2,3.9
cotyledon,3.6,2.9,2.7,3.1
mature,1.4,0.9,1.8,1.1"""
    dump("39-brga-dynamics", csv)
    _, c = csv_cols(csv)
    stages = c["stage"]
    x = np.arange(len(stages))
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    for i, g in enumerate(["BRGA", "DWF4", "BZR1", "CPD"]):
        v = num(c, g)
        ax.plot(x, v, "-o", ms=6, color=CAT[i], label=g)
        pk = int(np.argmax(v))
        ax.annotate("peak %.1f" % v[pk], (x[pk], v[pk]), (x[pk] + 0.06, v[pk] + 0.18),
                    fontsize=8.5, color=CAT[i])
    ax.set_xticks(x, stages)
    ax.set_ylabel("TPM")
    ax.set_title("BR pathway genes peak at torpedo stage")
    ax.legend()
    save(fig, "39-brga-dynamics")


# ------------------------------------------------------- 40 cascade heatmap
def cascade_heatmap():
    csv = """gene,0h,2h,4h,8h,12h
gene_01,1.8,0.6,-0.5,-0.9,-1.0
gene_02,1.2,1.0,-0.2,-0.8,-0.9
gene_03,-0.3,1.5,0.9,-0.4,-0.8
gene_04,-0.7,0.9,1.4,0.2,-0.5
gene_05,-0.8,-0.2,1.2,1.5,0.1
gene_06,-0.9,-0.6,0.3,1.6,0.8
gene_07,-1.0,-0.8,-0.4,0.9,1.5
gene_08,-0.9,-1.0,-0.7,0.2,1.3"""
    dump("40-cascade-heatmap", csv)
    _, c = csv_cols(csv)
    genes = c["gene"]
    cols = [k for k in c if k != "gene"]
    M = np.vstack([num(c, s) for s in cols])
    fig, ax = plt.subplots(figsize=(6.6, 5.4))
    im = ax.imshow(M, cmap="coolwarm", vmin=-2, vmax=2, aspect="auto")
    ax.set_xticks(range(len(cols)), cols)
    ax.set_yticks(range(len(genes)), genes)
    ax.grid(False)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, "%.1f" % M[i, j], ha="center", va="center", fontsize=7.5,
                    color="white" if abs(M[i, j]) > 1.2 else "#222222")
    ax.set_title("Cascade: the expression wave travels down the rows")
    cb = fig.colorbar(im, ax=ax, shrink=0.8)
    cb.set_label("z-score")
    save(fig, "40-cascade-heatmap")


# -------------------------------------------------------------- 41 ridgeline
def ridgeline():
    means = [2.0, 3.5, 5.0, 6.5, 8.0, 9.5]
    groups = {}
    rows = ["cluster,expression"]
    for i, m in enumerate(means, 1):
        vals = np.round(m + rng.normal(0, 1.0, 10), 2)
        groups["c%d" % i] = vals
        rows += ["c%d,%.2f" % (i, v) for v in vals]
    dump("41-ridgeline", "\n".join(rows))

    fig, ax = plt.subplots(figsize=(7.6, 5.6))
    ax.grid(False)
    xs = np.linspace(-1.5, 14, 300)
    for i, (name, vals) in enumerate(reversed(list(groups.items()))):
        kde = gaussian_kde(vals)
        d = kde(xs)
        base = (len(groups) - i) * 1.0
        ax.fill_between(xs, base, base + d, color=CAT[i % len(CAT)], alpha=0.55, lw=1.2,
                        edgecolor="white")
        ax.text(-1.7, base + 0.1, name, ha="right", fontsize=10)
    ax.set_xlim(-3.2, 14)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("expression (log2 TPM)")
    ax.set_title("Ridgeline: expression distributions per cluster")
    save(fig, "41-ridgeline")


if __name__ == "__main__":
    sankey()
    protein_anchor()
    evidence_matrix()
    tissue_expression()
    promoter_cis()
    brga_dynamics()
    cascade_heatmap()
    ridgeline()
