# -*- coding: utf-8 -*-
"""Gallery post 2 - part B: microbiome, single-cell, network, wet-lab (56-66)."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

from common import save, dump, CAT

rng = np.random.default_rng(77)


# ------------------------------------------------------------------- 56 pcoa
def pcoa():
    groups = {"rhizosphere": (2.4, 1.8), "bulk_soil": (-2.2, 1.2),
              "root_endo": (0.1, -2.6)}
    rows = ["site,group,PCo1,PCo2"]
    pts = []
    for g, (cx, cy) in groups.items():
        for i in range(8):
            a, b = cx + rng.normal(0, 0.55), cy + rng.normal(0, 0.45)
            pts.append((a, b, g))
            rows.append("S%d,%s,%.2f,%.2f" % (len(pts), g, a, b))
    dump("56-pcoa", "\n".join(rows))

    fig, ax = plt.subplots(figsize=(6.6, 5.6))
    for i, (g, col) in enumerate(zip(groups, CAT)):
        m = np.array([p[2] for p in pts]) == g
        xa = np.array([p[0] for p in pts])[m]
        xb = np.array([p[1] for p in pts])[m]
        ax.scatter(xa, xb, s=52, color=CAT[i], edgecolors="white", label=g)
        cov = np.cov(xa, xb)
        vals, vecs = np.linalg.eigh(cov)
        order = vals.argsort()[::-1]
        ang = np.degrees(np.arctan2(*vecs[:, order[0]][::-1]))
        w, h = 2 * np.sqrt(vals[order[0]] * 5.99), 2 * np.sqrt(vals[order[1]] * 5.99)
        ax.add_patch(Ellipse((xa.mean(), xb.mean()), w, h, angle=ang,
                             fill=False, edgecolor=CAT[i], lw=1.4, ls="--"))
    ax.set_xlabel("PCo1 (41.6%)")
    ax.set_ylabel("PCo2 (23.8%)")
    ax.set_title("PCoA of Bray-Curtis distances, dashed = 95% envelope")
    ax.legend()
    save(fig, "56-pcoa")


# ----------------------------------------------------------------- 57 alpha
def alpha():
    rows = ["treatment,shannon"]
    meds = {"control": 3.1, "low_N": 3.9, "high_N": 2.6}
    data = {}
    for g, m in meds.items():
        v = np.round(m + rng.normal(0, 0.28, 10), 2)
        data[g] = v
        rows += ["%s,%.2f" % (g, x) for x in v]
    dump("57-alpha", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(6.4, 5.0))
    bp = ax.boxplot([data[g] for g in meds], tick_labels=meds, patch_artist=True,
                    widths=0.5, medianprops=dict(color="black", lw=1.6))
    for patch, col in zip(bp["boxes"], CAT[:3]):
        patch.set_facecolor(col)
        patch.set_alpha(0.6)
    letters = ["b", "a", "c"]
    for i, (g, letter) in enumerate(zip(meds, letters), 1):
        ax.text(i, data[g].max() + 0.18, letter, ha="center", fontsize=12,
                fontweight="bold")
    ax.set_ylabel("Shannon index")
    ax.set_title("Alpha diversity: boxes sharing no letter differ (p < 0.05)")
    save(fig, "57-alpha")


# -------------------------------------------------------------- 58 abundance
def abundance():
    phyla = ["Proteobacteria", "Actinobacteriota", "Acidobacteriota",
             "Chloroflexi", "Bacteroidota", "Other"]
    samples = ["S1", "S2", "S3", "S4", "S5", "S6"]
    mat = np.array([
        [38, 22, 14, 9, 8, 9],
        [41, 19, 13, 10, 9, 8],
        [36, 24, 15, 8, 9, 8],
        [26, 31, 12, 12, 9, 10],
        [24, 33, 13, 11, 10, 9],
        [27, 29, 14, 11, 10, 9],
    ])
    rows = ["sample," + ",".join(phyla)]
    rows += [",".join([s] + [str(int(v)) for v in row])
             for s, row in zip(samples, mat)]
    dump("58-abundance", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    bottom = np.zeros(len(samples))
    for j, p in enumerate(phyla):
        ax.bar(samples, mat[:, j], bottom=bottom, label=p, color=CAT[j % 10],
               width=0.62)
        bottom += mat[:, j]
    ax.set_ylabel("relative abundance (%)")
    ax.set_ylim(0, 118)
    ax.legend(ncol=2, fontsize=8.5, loc="upper center", bbox_to_anchor=(0.5, 1.02))
    ax.set_title("Top-5 phyla composition per sample (percentages sum to 100)")
    save(fig, "58-abundance")


# -------------------------------------------------------------- 59 trajectory
def trajectory():
    t = np.linspace(0, 1, 40)
    px = 40 * t - 18
    py = 0.06 * (px + 18) ** 2 * 0.09 - 3 + 1.2 * np.sin(px * 0.18)
    cx = px + rng.normal(0, 1.1, 40)
    cy = py + rng.normal(0, 1.0, 40)
    rows = ["cell,x,y,pseudotime"]
    rows += ["c%d,%.2f,%.2f,%.2f" % (i + 1, a, b, tt)
             for i, (a, b, tt) in enumerate(zip(cx, cy, t))]
    dump("59-trajectory", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.4, 5.6))
    sc = ax.scatter(cx, cy, c=t, cmap="viridis", s=58, edgecolors="white",
                    linewidths=0.6)
    order = np.argsort(px)
    ax.plot(px[order], py[order], color="0.55", lw=2, ls="--", label="principal curve")
    k = np.argsort(t)[3]
    ax.annotate("progenitors", (cx[k], cy[k]), (cx[k] - 9, cy[k] - 6.5), fontsize=9.5,
                arrowprops=dict(arrowstyle="->", lw=1))
    k2 = np.argsort(t)[-4]
    ax.annotate("mature cells", (cx[k2], cy[k2]), (cx[k2] + 3, cy[k2] + 7),
                fontsize=9.5, arrowprops=dict(arrowstyle="->", lw=1))
    fig.colorbar(sc, ax=ax, label="pseudotime")
    ax.set_xlabel("component 1")
    ax.set_ylabel("component 2")
    ax.legend(loc="lower right")
    save(fig, "59-trajectory")


# ------------------------------------------------------------- 60 scdotplot
def sc_dotplot():
    genes = ["DWF4", "BZR1", "CHS", "ANS", "FLS", "ANR", "PAL", "SAUR19"]
    clusters = ["epidermis", "cortex", "vasculature"]
    pct = np.clip(rng.uniform(15, 100, (8, 3)), 10, 100)
    avg = rng.uniform(0.2, 2.6, (8, 3))
    pct[0, 2], avg[0, 2] = 94, 2.4
    pct[2, 0], avg[2, 0] = 91, 2.1
    rows = ["gene,cluster,pct_expr,avg_expr"]
    for i, g in enumerate(genes):
        for j, c in enumerate(clusters):
            rows.append("%s,%s,%.0f,%.2f" % (g, c, pct[i, j], avg[i, j]))
    dump("60-scdotplot", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    for i, g in enumerate(genes):
        for j, c in enumerate(clusters):
            ax.scatter(j, i, s=pct[i, j] * 3.4, c=avg[i, j], cmap="YlGnBu",
                       vmin=0, vmax=2.6, edgecolor="0.4", linewidth=0.6)
    ax.set_xticks(range(3), clusters, rotation=20, ha="right")
    ax.set_yticks(range(8), genes)
    ax.grid(True, alpha=0.3)
    ax.invert_yaxis()
    sc = plt.cm.ScalarMappable(cmap="YlGnBu", norm=plt.Normalize(0, 2.6))
    fig.colorbar(sc, ax=ax, shrink=0.7, label="mean expression (z)")
    ax.set_xlim(-0.5, 2.5)
    ax.set_title("Single-cell dot plot: size = percent expressing,\ncolor = mean expression")
    save(fig, "60-scdotplot")


# ------------------------------------------------------------------- 61 ppi
def ppi():
    nodes = ["DWF4", "BZR1", "BRI1", "BIN2", "SAUR19", "PRE1", "CHS",
             "ANS", "FLS", "MYB12", "bHLH3", "WRKY1", "PAL"]
    edges = [("DWF4", "BZR1"), ("BZR1", "BRI1"), ("BRI1", "BIN2"),
             ("BZR1", "BIN2"), ("BZR1", "PRE1"), ("BZR1", "SAUR19"),
             ("BZR1", "MYB12"), ("MYB12", "CHS"), ("MYB12", "FLS"),
             ("CHS", "ANS"), ("ANS", "FLS"), ("bHLH3", "CHS"),
             ("bHLH3", "ANS"), ("WRKY1", "PAL"), ("PRE1", "SAUR19")]
    rows = ["node1,node2,edge_type"]
    rows += ["%s,%s,protein_interaction" % e for e in edges]
    dump("61-ppi", "\n".join(rows))
    deg = {n: 0 for n in nodes}
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    n = len(nodes)
    ang = np.linspace(90, 90 - 360, n, endpoint=False) + 15
    pos = {node: (np.cos(np.deg2rad(a)), np.sin(np.deg2rad(a)))
           for node, a in zip(nodes, ang)}
    fig, ax = plt.subplots(figsize=(7.6, 7.2))
    ax.set_aspect("equal")
    ax.axis("off")
    for a, b in edges:
        x0, y0 = pos[a]
        x1, y1 = pos[b]
        ax.plot([x0, x1], [y0, y1], color="0.72", lw=1.1, zorder=1)
    for node in nodes:
        x, y = pos[node]
        ax.scatter([x], [y], s=430 + deg[node] * 260, color=CAT[2] if deg[node] >= 3
                   else CAT[0], edgecolors="white", linewidths=1.4, zorder=3)
        dx, dy = x * 1.24, y * 1.24
        ax.text(dx, dy, node, ha="center", va="center", fontsize=9,
                fontweight="bold" if deg[node] >= 3 else "normal")
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.45, 1.45)
    ax.set_title("Protein-interaction network, node size = degree (simulated)")
    save(fig, "61-ppi")


# --------------------------------------------------------- 62 module-trait
def module_trait():
    mods = ["brown", "turquoise", "blue", "green", "red", "yellow"]
    traits = ["seed_weight", "dwf_score", "flavonoid", "flowering_day"]
    M = np.array([
        [0.86, 0.72, 0.15, -0.31],
        [0.12, 0.18, 0.88, 0.05],
        [-0.42, -0.66, 0.21, 0.48],
        [0.33, 0.24, -0.58, -0.12],
        [-0.15, -0.09, 0.62, 0.71],
        [0.08, -0.21, -0.35, -0.79],
    ])
    rows = ["module," + ",".join(traits)]
    rows += [",".join([m] + ["%.2f" % v for v in r]) for m, r in zip(mods, M)]
    dump("62-moduletrait", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(6.8, 5.2))
    im = ax.imshow(M, cmap="RdYlBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(4), traits, rotation=20, ha="right")
    ax.set_yticks(range(6), mods)
    ax.grid(False)
    for i in range(6):
        for j in range(4):
            v = M[i, j]
            ax.text(j, i, "%.2f\n%s" % (v, "*" if abs(v) >= 0.6 else "ns"),
                    ha="center", va="center", fontsize=8,
                    color="white" if abs(v) > 0.55 else "#222")
    fig.colorbar(im, ax=ax, shrink=0.8, label="Pearson r")
    ax.set_title("WGCNA module-trait correlations (* = |r| >= 0.6)")
    save(fig, "62-moduletrait")


# -------------------------------------------------------------- 63 dose IC50
def dose():
    dose = np.array([0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30])

    def fourpl(x, bottom, top, ic50, slope):
        return bottom + (top - bottom) / (1 + (x / ic50) ** slope)

    ra = fourpl(dose, 8, 100, 0.32, -1.1)
    rb = fourpl(dose, 10, 100, 3.4, -1.3)
    rows = ["dose_uM,response_A,response_B"]
    rows += ["%.3f,%.1f,%.1f" % (d, a, b) for d, a, b in zip(dose, ra, rb)]
    dump("63-dose", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    ax.semilogx(dose, ra, "-o", ms=5, color=CAT[0], label="compound A")
    ax.semilogx(dose, rb, "-o", ms=5, color=CAT[1], label="compound B")
    ax.axhline(54, color="0.6", ls=":", lw=1.2)
    ax.text(0.0012, 57, "50% response", fontsize=8.5, color="0.4")
    for r, col, ic in [(ra, CAT[0], 0.32), (rb, CAT[1], 3.4)]:
        ax.axvline(ic, color=col, ls="--", lw=1)
        ax.text(ic * 1.15, 20, "IC50 = %.2f uM" % ic, fontsize=9, color=col,
                rotation=90, va="bottom")
    ax.set_xlabel("dose (uM, log scale)")
    ax.set_ylabel("response (% of control)")
    ax.legend(loc="lower left")
    save(fig, "63-dose")


# -------------------------------------------------------------- 64 michaelis
def michaelis():
    S = np.array([0.1, 0.2, 0.5, 1, 2, 5, 10, 20])
    v1 = 62 * S / (0.8 + S)
    v2 = 95 * S / (4.5 + S)
    rows = ["substrate_mM,v_iso1,v_iso2"]
    rows += ["%.1f,%.1f,%.1f" % (a, b, c) for a, b, c in zip(S, v1, v2)]
    dump("64-michaelis", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    for v, km, vmax, col, lab in [(v1, 0.8, 62, CAT[0], "isozyme 1"),
                                  (v2, 4.5, 95, CAT[1], "isozyme 2")]:
        xs = np.linspace(0, 20, 200)
        ax.plot(xs, vmax * xs / (km + xs), color=col, lw=1.8)
        ax.scatter(S, v, s=40, color=col, edgecolors="white", zorder=3, label=lab)
        ax.axhline(vmax, color=col, ls=":", lw=1)
        ax.axvline(km, color=col, ls="--", lw=1)
        ax.annotate("Km = %.1f mM" % km, (km, 4), (km + 0.5, 2), fontsize=8.5,
                    color=col)
    ax.text(19.6, 96.5, "Vmax", fontsize=8.5, color="0.4", ha="right")
    ax.set_xlabel("substrate concentration (mM)")
    ax.set_ylabel("velocity (umol/min/mg)")
    ax.set_ylim(0, 108)
    ax.legend(loc="lower right")
    save(fig, "64-michaelis")


# -------------------------------------------------------------------- 65 gel
def gel():
    fig, ax = plt.subplots(figsize=(7.8, 5.8))
    ax.grid(False)
    ax.add_patch(plt.Rectangle((0.5, 0.5), 9.0, 8.8, facecolor="#0E0E0E"))
    lanes = {"M": 1.7, "undig": 3.6, "digest": 5.3, "wrong": 6.9, "PCR+": 8.4}
    for name, x0 in lanes.items():
        ax.text(x0, 9.0, name, ha="center", fontsize=9, color="white")
        ax.add_patch(plt.Rectangle((x0 - 0.75, 8.35), 1.5, 0.18,
                                   facecolor="#2A2A2A"))

    def band(x0, y0, w, h, it=1.0):
        ax.add_patch(plt.Rectangle((x0 - w / 2, y0 - h / 2), w, h,
                    facecolor="white", alpha=0.5 + 0.5 * it, edgecolor="none"))

    ladder = [("10 kb", 8.0), ("8000", 7.35), ("5 kb", 6.3), ("3000", 5.2),
              ("2000", 4.4), ("1 kb", 3.2), ("500", 2.2)]
    for label, y0 in ladder:
        band(1.7, y0, 1.3, 0.16, 0.85)
        ax.text(0.85, y0, label if label.endswith("kb") else "",
                ha="right", fontsize=7.5, color="white")
    band(3.6, 3.8, 1.4, 0.34, 0.9)     # undigested plasmid: single supercoiled band
    band(5.3, 5.6, 1.4, 0.22, 0.9)     # digest: backbone 5.4 kb
    band(5.3, 3.4, 1.4, 0.22, 0.75)    # digest: insert 2.1 kb
    band(6.9, 6.2, 1.4, 0.22, 0.8)     # wrong clone: single 6.2 kb
    band(8.4, 3.6, 1.4, 0.2, 0.85)     # PCR positive control 1.9 kb
    ax.text(5.0, 0.15, "digest lane shows backbone + insert at expected sizes",
            ha="center", fontsize=8.5, color="#BBBBBB")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 9.6)
    ax.axis("off")
    ax.set_title("Agarose gel schematic: colony PCR / restriction check", pad=10)
    save(fig, "65-gel")


# ----------------------------------------------------------------- 66 growth
def growth():
    t = np.array([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22])
    od_a = 0.02 + 1.15 / (1 + np.exp(-(t - 10.5) / 2.1))
    od_b = 0.02 + 0.72 / (1 + np.exp(-(t - 13.2) / 2.6))
    rows = ["time_h,WT,mutant"]
    rows += ["%d,%.3f,%.3f" % (a, b, c) for a, b, c in zip(t, od_a, od_b)]
    dump("66-growth", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    ax.plot(t, od_a, "-o", ms=5, color=CAT[0], label="WT")
    ax.plot(t, od_b, "-o", ms=5, color=CAT[3], label="mutant")
    ax.axvspan(2, 6, color=CAT[1], alpha=0.10)
    ax.text(4, 1.24, "lag", ha="center", fontsize=9, color=CAT[1])
    ax.axvspan(6, 14, color=CAT[2], alpha=0.10)
    ax.text(10, 1.24, "exponential", ha="center", fontsize=9, color="#3D6B35")
    ax.axvspan(14, 22, color="0.5", alpha=0.10)
    ax.text(18, 1.24, "stationary", ha="center", fontsize=9, color="0.4")
    ax.set_xlabel("time (h)")
    ax.set_ylabel("OD600")
    ax.set_ylim(0, 1.35)
    ax.legend(loc="upper left")
    save(fig, "66-growth")


if __name__ == "__main__":
    pcoa()
    alpha()
    abundance()
    trajectory()
    sc_dotplot()
    ppi()
    module_trait()
    dose()
    michaelis()
    gel()
    growth()
