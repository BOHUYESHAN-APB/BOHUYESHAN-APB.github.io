# -*- coding: utf-8 -*-
"""Gallery post 2 - part A: population genetics, GWAS, comparative genomics,
gene family figures (42-55)."""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.cluster.hierarchy import linkage, dendrogram

from common import save, dump, CAT, UP, DOWN

rng = np.random.default_rng(2026)


# ------------------------------------------------------------- 42 manhattan
def manhattan():
    chr_len = {c: 400 + c * 30 for c in range(1, 9)}
    rows = ["chr,pos_kb,pvalue,gene"]
    sig = [(3, 1210, 2.2e-7, "FaDWF4"), (5, 1875, 8.9e-7, "FaCHS"),
           (3, 1195, 6.1e-6, "FaBRI1"), (7, 2430, 1.8e-5, "FaANS")]
    pts = []
    for c in range(1, 9):
        n = 120
        pos = np.sort(rng.uniform(0, chr_len[c], n)).astype(int)
        p = rng.uniform(1e-4, 1, n)
        pts += [(c, int(x), float(y), "") for x, y in zip(pos, p)]
    rows = ["chr,pos_kb,pvalue,gene"]
    for c, pos, p, g in sig:
        rows.append("%d,%d,%.2e,%s" % (c, pos, p, g))
    pts = [r for r in pts if (r[0], r[1]) not in [(s[0], s[1]) for s in sig]]
    for c, pos, p, g in pts:
        rows.append("%d,%d,%.2e," % (c, pos, p))
    dump("42-manhattan", "\n".join(rows))

    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    xoff, xt, xl = 0, [], []
    for c in range(1, 9):
        sub = np.array([[p, -np.log10(q)] for cc, p, q, _ in
                        [(a, b, d, e) for a, b, d, e in pts] if cc == c]
                       + [[s[1], -np.log10(s[2])] for s in sig if s[0] == c])
        ax.scatter(sub[:, 0] + xoff, sub[:, 1], s=9,
                   color=CAT[0] if c % 2 else CAT[1], alpha=0.8, linewidths=0)
        ss = np.array([[s[1], -np.log10(s[2])] for s in sig if s[0] == c])
        if len(ss):
            ax.scatter(ss[:, 0] + xoff, ss[:, 1], s=42, color=CAT[3],
                       edgecolors="white", linewidths=0.7, zorder=4)
        xt.append(xoff + chr_len[c] / 2)
        xl.append("Chr%d" % c)
        xoff += chr_len[c] + 60
    ax.axhline(-np.log10(1e-4), color="0.5", ls="--", lw=1)
    ax.text(60, -np.log10(1e-4) + 0.12, "suggestive 1e-4", fontsize=8.5, color="0.4")
    ax.axhline(-np.log10(4.2e-6), color=CAT[3], lw=1.2)
    ax.text(60, -np.log10(4.2e-6) + 0.12, "genome-wide 4.2e-6", fontsize=8.5,
            color=CAT[3])
    for g, c, pos, p in [("FaDWF4", 3, 1210, 2.2e-7), ("FaCHS", 5, 1875, 8.9e-7)]:
        x = sum(chr_len[i] + 60 for i in range(1, c)) + pos
        ax.annotate(g, (x, -np.log10(p)), (x + 40, -np.log10(p) + 0.35),
                    fontsize=9, fontweight="bold", color=CAT[3])
    ax.set_xticks(xt, xl)
    ax.set_ylim(0, 7.8)
    ax.set_ylabel("-log10(p)")
    ax.set_xlabel("chromosome")
    ax.set_title("Manhattan plot: 960 SNPs, dwarfism trait (simulated)")
    save(fig, "42-manhattan")


# -------------------------------------------------------------------- 43 qq
def qq():
    n = 800
    p = rng.uniform(1e-6, 1, n)
    chi2_obs = stats.chi2.isf(p, 1)
    lam = np.median(chi2_obs) / 0.4549
    chi2_exp = stats.chi2.ppf((np.arange(n) + 0.5) / n, 1)
    ox = -np.log10(1 - stats.chi2.cdf(chi2_exp, 1))
    oy = -np.log10(1 - stats.chi2.cdf(np.sort(chi2_obs), 1))
    lo = -np.log10(1 - stats.chi2.cdf(stats.chi2.ppf(0.025, 1), 1))
    fig, ax = plt.subplots(figsize=(5.8, 5.8))
    ax.scatter(ox, oy, s=10, color=CAT[0], alpha=0.7, linewidths=0)
    lim = max(ox.max(), oy.max()) * 1.05
    ax.plot([0, lim], [0, lim], color="0.4", lw=1.2, label="expected (lambda = 1)")
    ax.plot(ox, ox * lam, color=CAT[3], ls="--", lw=1.2,
            label="lambda = %.2f" % lam)
    ax.set_xlabel("expected -log10(p)")
    ax.set_ylabel("observed -log10(p)")
    ax.set_title("QQ plot, same GWAS as Fig. 42")
    ax.legend(loc="upper left")
    save(fig, "43-qq")


# ---------------------------------------------------------------- 44 lddecay
def lddecay():
    d = rng.uniform(0.5, 200, 240)
    r2 = np.clip(np.exp(-d / 55) * rng.uniform(0.55, 1.35, len(d)), 0.01, 1)
    bins = np.arange(0, 201, 10)
    centers, means = [], []
    for b0, b1 in zip(bins[:-1], bins[1:]):
        m = (d >= b0) & (d < b1)
        if m.sum() > 2:
            centers.append((b0 + b1) / 2)
            means.append(r2[m].mean())
    rows = ["distance_kb,mean_r2"]
    rows += ["%.0f,%.3f" % (a, b) for a, b in zip(centers, means)]
    dump("44-lddecay", "\n".join(rows))
    half = 55 * np.log(2)
    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    ax.scatter(d, r2, s=8, color=CAT[0], alpha=0.35, linewidths=0)
    ax.plot(centers, means, color=CAT[3], lw=2.2, label="binned mean")
    ax.axvline(half, color="0.5", ls=":", lw=1.2)
    ax.text(half + 3, 0.55, "r2 = 0.5 at ~38 kb", fontsize=9, color="0.4")
    ax.set_xlabel("physical distance (kb)")
    ax.set_ylabel("LD (r2)")
    ax.set_ylim(0, 1.02)
    ax.legend()
    save(fig, "44-lddecay")


# -------------------------------------------------------------- 45 admixture
def admixture():
    rows = ["individual,pop,K1,K2,K3"]
    data = []
    for i in range(1, 7):
        k = [0.05 + rng.uniform(0, 0.08), rng.uniform(0.08, 0.18), 0]
        k[2] = 1 - sum(k)
        data.append(("W%d" % i, "west", *np.round(k, 3)))
    for i in range(1, 7):
        k = [rng.uniform(0.06, 0.16), 0.05 + rng.uniform(0, 0.06), 0]
        k[2] = 1 - sum(k)
        data.append(("E%d" % i, "east", *np.round(k, 3)))
    for ind, pop, a, b, c in data:
        rows.append("%s,%s,%.3f,%.3f,%.3f" % (ind, pop, a, b, c))
    dump("45-admixture", "\n".join(rows))

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    y = 0
    yticks, ylabels = [], []
    for ind, pop, a, b, c in data:
        ax.barh(y, a, color=CAT[0], left=0)
        ax.barh(y, b, color=CAT[1], left=a)
        ax.barh(y, c, color=CAT[2], left=a + b)
        yticks.append(y)
        ylabels.append(ind)
        y += 1
    ax.set_yticks(yticks, ylabels, fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlabel("ancestry proportion")
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in CAT[:3]]
    ax.legend(handles, ["K1", "K2", "K3"], ncol=3, loc="lower right",
              bbox_to_anchor=(1.0, -0.28))
    save(fig, "45-admixture")


# ------------------------------------------------------------------ 46 phylo
def phylo():
    names = ["F. tataricum", "F. esculentum", "F. cymosum", "Rheum rhabarbarum",
             "A. thaliana", "S. lycopersicum", "O. sativa", "Z. mays"]
    proto = {"F. tataricum": (1.00, 0.00, 0.08),
             "F. esculentum": (1.06, 0.08, 0.02),
             "F. cymosum": (0.95, 0.04, 0.14),
             "Rheum rhabarbarum": (1.18, 0.22, 0.06),
             "A. thaliana": (0.04, 1.00, 0.04),
             "S. lycopersicum": (0.12, 1.12, 0.10),
             "O. sativa": (0.06, 0.10, 1.00),
             "Z. mays": (0.10, 0.02, 1.14)}
    M = np.array([proto[n] + rng.normal(0, 0.04, 3) for n in names])
    Z = linkage(M, "average")
    dump("46-phylo-matrix", "\n".join(
        ",".join("%.2f" % v for v in row) for row in M))
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    dendrogram(Z, orientation="left", labels=names, ax=ax,
               color_threshold=0, link_color_func=lambda k: "0.35")
    ax.set_xlabel("genetic distance (average linkage)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("UPGMA tree of eight species (simulated distances)")
    save(fig, "46-phylo")


# ------------------------------------------------------------- 47 pi-fst
def pi_fst():
    rows = ["window_kb,pi_A,pi_B,fst"]
    n = 30
    for i in range(n):
        pos = (i + 0.5) * 200
        sweep = 2.6e3 < pos < 3.6e3
        pa = 1.6e-3 if not sweep else 0.4e-3
        pb = 1.5e-3
        f = 0.08 if not sweep else 0.42 + rng.uniform(-0.05, 0.05)
        rows.append("%.0f,%.4f,%.4f,%.3f" % (pos, pa * rng.uniform(0.9, 1.1),
                                             pb * rng.uniform(0.9, 1.1), f))
    dump("47-pi-fst", "\n".join(rows))

    dfc = [ln.split(",") for ln in rows[1:]]
    x = [float(r[0]) for r in dfc]
    pa = [float(r[1]) for r in dfc]
    pb = [float(r[2]) for r in dfc]
    f = [float(r[3]) for r in dfc]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9.0, 5.2), sharex=True,
                                   gridspec_kw=dict(height_ratios=[2, 1.3],
                                                    hspace=0.08))
    ax1.plot(x, pa, color=CAT[0], lw=1.8, label="population A (dwarf)")
    ax1.plot(x, pb, color=CAT[2], lw=1.8, label="population B (tall)")
    ax1.set_ylabel("nucleotide diversity pi")
    ax1.legend()
    ax1.set_title("Sliding-window pi (top) and Fst (bottom)")
    ax1.axvspan(2600, 3600, color=CAT[3], alpha=0.10)
    ax2.plot(x, f, color="0.3", lw=1.6)
    ax2.axhline(0.25, color=CAT[3], ls="--", lw=1.1)
    ax2.text(3050, 0.27, "selective sweep", fontsize=9, color=CAT[3], ha="center")
    ax2.set_ylabel("Fst")
    ax2.set_xlabel("position on Chr3 (kb)")
    ax2.axvspan(2600, 3600, color=CAT[3], alpha=0.10)
    save(fig, "47-pi-fst")


# ---------------------------------------------------------------- 48 dotplot
def dotplot():
    pts = []
    for i in range(220):                                  # 共线性主带
        q = 2 + i * 0.13 + rng.uniform(0, 0.06)
        t = 1.5 + i * 0.125 + rng.uniform(0, 0.06)
        pts.append((q, t))
    for i in range(60):                                   # 倒位区块
        q = 12 + i * 0.1
        t = 20 - i * 0.1
        pts.append((q, t))
    fig, ax = plt.subplots(figsize=(6.4, 6.4))
    ax.scatter([p[0] for p in pts[:220]], [p[1] for p in pts[:220]], s=6,
               color=CAT[0], alpha=0.7, linewidths=0, label="collinear")
    ax.scatter([p[0] for p in pts[220:]], [p[1] for p in pts[220:]], s=6,
               color=CAT[3], alpha=0.8, linewidths=0, label="inverted block")
    ax.add_patch(plt.Rectangle((11.6, 14.2), 6.8, 6.4, fill=False,
                               edgecolor=CAT[3], ls="--", lw=1.2))
    ax.annotate("inversion (~6 Mb)", (15, 17.4), (16.5, 22.5), fontsize=9.5,
                color=CAT[3])
    ax.plot([0, 30], [0, 30], color="0.8", lw=0.8, ls=":")
    ax.set_xlabel("F. esculentum chr5 (Mb)")
    ax.set_ylabel("F. tataricum chr5 (Mb)")
    ax.legend(loc="upper left")
    save(fig, "48-dotplot")


# ------------------------------------------------------------------- 49 kaks
def kaks():
    v = rng.lognormal(-1.4, 1.0, 320)
    v = v[v < 3]
    counts, edges = np.histogram(v, bins=np.arange(0, 3.01, 0.25))
    rows = ["bin_left,bin_right,count"]
    rows += ["%.2f,%.2f,%d" % (a, b, c) for a, b, c in zip(edges[:-1], edges[1:], counts)]
    dump("49-kaks", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.bar(edges[:-1], counts, width=0.24, align="edge", color=CAT[0],
           alpha=0.8, edgecolor="white")
    ax.axvline(1.0, color=CAT[3], lw=1.6)
    ax.text(1.03, counts.max() * 0.95, "Ka/Ks = 1\n(neutral)", fontsize=9,
            color=CAT[3])
    ax.axvline(0.5, color="0.5", ls="--", lw=1.2)
    ax.text(0.52, counts.max() * 0.95, "0.5\n(duplication)", fontsize=9, color="0.4")
    frac = (v < 0.5).mean() * 100
    ax.text(0.35, counts.max() * 0.72, "%.0f%% of pairs < 0.5\n(strong purifying)"
            % frac, fontsize=9, ha="center")
    ax.set_xlabel("Ka/Ks per ortholog pair")
    ax.set_ylabel("number of gene pairs")
    ax.set_title("Ka/Ks distribution, n = %d pairs (simulated)" % len(v))
    save(fig, "49-kaks")


# ------------------------------------------------------------------ 50 chrloc
def chrloc():
    genes = [("FaDWF4", 1, 61.2), ("FaBRI1", 1, 143.7), ("FaCHS", 2, 38.4),
             ("FaCHI", 2, 96.1), ("FaF3H", 3, 27.8), ("FaFLS", 3, 122.5),
             ("FaANS", 4, 55.0), ("FaANR", 4, 148.2), ("FaPAL", 5, 72.9),
             ("Fa4CL", 6, 44.3), ("FaGA20ox", 7, 88.6), ("FaGA2ox", 7, 165.1),
             ("FaDET2", 8, 33.7), ("FaBZR1", 8, 118.9)]
    rows = ["gene,chr,pos_mb"]
    rows += ["%s,%d,%.1f" % g for g in genes]
    dump("50-chrloc", "\n".join(rows))
    lens = {1: 212.0, 2: 198.5, 3: 185.2, 4: 172.8, 5: 160.4, 6: 148.9,
            7: 135.6, 8: 120.3}
    fig, ax = plt.subplots(figsize=(5.6, 7.2))
    for i, (c, L) in enumerate(lens.items()):
        x = i * 1.4
        ax.add_patch(plt.Rectangle((x - 0.22, 0), 0.44, L, facecolor=CAT[i % 2],
                                   alpha=0.35, edgecolor="0.3"))
        ax.text(x, L + 6, "Chr%d" % c, ha="center", fontsize=9.5)
        for g, gc, pos in genes:
            if gc == c:
                side = 1 if pos < L / 2 else -1
                ax.plot([x + side * 0.22, x + side * 0.95], [pos, pos],
                        color="0.4", lw=1)
                ax.scatter([x + side * 0.95], [pos], s=34, color=CAT[3], zorder=3)
                ax.text(x + side * 1.02, pos, g, fontsize=7.6, va="center",
                        ha="left" if side == 1 else "right")
    ax.set_xlim(-1.6, 11.2)
    ax.set_ylim(-8, 235)
    ax.axis("off")
    ax.set_title("Chromosomal distribution of 14 candidate genes")
    save(fig, "50-chrloc")


# ----------------------------------------------------------------- 51 circos
def circos():
    lens = {"Fa1": 212.0, "Fa2": 198.5, "Fa3": 185.2, "Fa4": 172.8, "Fa5": 160.4}
    total = sum(lens.values())
    start = {}
    a = 90
    for c, L in lens.items():                      # 顺时针从顶部开始
        start[c] = a
        a -= L / total * 360
    blocks = [("Fa1", 20, 68, "Fa3", 12, 55), ("Fa1", 120, 168, "Fa2", 30, 82),
              ("Fa2", 140, 190, "Fa5", 20, 66), ("Fa3", 100, 150, "Fa4", 40, 88)]
    rows = ["chr1,start_mb,end_mb,chr2,start_mb,end_mb"]
    rows += ["%s,%.0f,%.0f,%s,%.0f,%.0f" % b for b in blocks]
    dump("51-circos-blocks", "\n".join(rows))

    fig, ax = plt.subplots(figsize=(7.4, 7.4))
    ax.set_aspect("equal")
    ax.axis("off")
    R = 1.0

    def ang(c, mb):
        deg = start[c] - (mb / lens[c]) * (lens[c] / total * 360)
        return np.deg2rad(deg)

    for c, L in lens.items():
        a0 = np.deg2rad(start[c])
        a1 = np.deg2rad(start[c] - L / total * 360)
        arc = np.linspace(a1, a0, 60)
        ax.plot(R * np.cos(arc), R * np.sin(arc), color=CAT[list(lens).index(c)],
                lw=11, solid_capstyle="butt")
        am = (a0 + a1) / 2
        ax.text(1.14 * np.cos(am), 1.14 * np.sin(am), c, ha="center", va="center",
                fontsize=10.5, fontweight="bold")
    tsl = np.linspace(0, 1, 40)

    def bez(p0, c1, c2, p1):
        return ((1 - tsl) ** 3)[:, None] * p0 + (3 * (1 - tsl) ** 2 * tsl)[:, None] * c1 \
            + (3 * (1 - tsl) * tsl ** 2)[:, None] * c2 + (tsl ** 3)[:, None] * p1

    for k, (c1, s1, e1, c2, s2, e2) in enumerate(blocks):
        a1a, a1b = ang(c1, s1), ang(c1, e1)
        a2a, a2b = ang(c2, s2), ang(c2, e2)
        P = lambda a: np.array([R * np.cos(a), R * np.sin(a)])
        p0, p1, q0, q1 = P(a1a), P(a1b), P(a2b), P(a2a)
        top = bez(p0, 0.58 * P(a1a), 0.58 * P(a2b), q0)
        bot = bez(p1, 0.58 * P(a1b), 0.58 * P(a2a), q1)
        poly = np.vstack([top, bot[::-1]])
        ax.fill(poly[:, 0], poly[:, 1], color=CAT[(k + 2) % 10], alpha=0.4, lw=0)
    ax.set_title("Circos-style synteny between five chromosomes (simulated)", pad=18)
    save(fig, "51-circos")


# ------------------------------------------------------------ 52 genedensity
def genedensity():
    rows = ["window_mb,count"]
    n = 20
    for i in range(n):
        c = 14 + 26 * np.exp(-((i - 6) ** 2) / 30) + 18 * np.exp(-((i - 15) ** 2) / 20)
        rows.append("%.1f,%d" % ((i + 0.5) * 5, int(c + rng.integers(-2, 3))))
    dump("52-genedensity", "\n".join(rows))
    dfc = [ln.split(",") for ln in rows[1:]]
    x = [float(r[0]) for r in dfc]
    y = [int(r[1]) for r in dfc]
    fig, ax = plt.subplots(figsize=(8.4, 4.2))
    ax.fill_between(x, y, color=CAT[0], alpha=0.4, lw=0)
    ax.plot(x, y, color=CAT[0], lw=1.8)
    ax.set_xlabel("position on Chr1 (Mb)")
    ax.set_ylabel("genes per 5 Mb window")
    ax.set_title("Gene density along Chr1 (100 genes in 100 Mb, simulated)")
    save(fig, "52-genedensity")


# -------------------------------------------------------------- 53 motiflogo
def motiflogo():
    core = "TGAAG"
    pwm = {b: [] for b in "ACGT"}
    bases = "ACGT"
    bias = [0.30, 0.25, 0.25, 0.20]
    for i in range(15):
        probs = []
        for k, b in enumerate(bases):
            if i < 5 and b == core[i]:
                p = 0.55                       # 核心位置强偏好
            else:
                p = bias[(k + i) % 4] * 0.6    # 其余位置弱偏好，随位置轮换
            probs.append(p)
        tot = sum(probs)
        for k, b in enumerate(bases):
            pwm[b].append(round(probs[k] / tot, 3))
    rows = ["pos,A,C,G,T"]
    rows += ["%d,%.3f,%.3f,%.3f,%.3f" % (i, pwm["A"][i], pwm["C"][i],
                                         pwm["G"][i], pwm["T"][i])
             for i in range(15)]
    dump("53-motif-pwm", "\n".join(rows))

    bcol = {"A": "#2E7D32", "C": "#1565C0", "G": "#E65100", "T": "#C62828"}
    fig, ax = plt.subplots(figsize=(8.6, 3.2))
    for i in range(15):
        stack = 0.0
        for b in sorted(bases, key=lambda x: pwm[x][i]):
            h = pwm[b][i]
            ax.text(i + 0.5, stack + h / 2, b, fontsize=h * 30, color=bcol[b],
                    ha="center", va="center", fontweight="bold")
            stack += h
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 1.02)
    ax.set_xticks(range(1, 16))
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("position in motif")
    ax.set_title("Motif logo: 15 bp promoter element (PWM, schematic glyph sizes)")
    save(fig, "53-motiflogo")


# --------------------------------------------------------- 54 genestructure
def genestructure():
    feats = [
        ("FaDWF4", "utr5", 1, 180), ("FaDWF4", "exon", 181, 520),
        ("FaDWF4", "intron", 521, 940), ("FaDWF4", "exon", 941, 1310),
        ("FaDWF4", "utr3", 1311, 1490),
        ("FaBZR1", "utr5", 1, 120), ("FaBZR1", "exon", 121, 380),
        ("FaBZR1", "intron", 381, 720), ("FaBZR1", "exon", 721, 1040),
        ("FaBZR1", "intron", 1041, 1380), ("FaBZR1", "exon", 1381, 1700),
        ("FaBZR1", "utr3", 1701, 1855),
        ("FaCHS", "utr5", 1, 95), ("FaCHS", "exon", 96, 430),
        ("FaCHS", "exon", 431, 760), ("FaCHS", "utr3", 761, 900),
        ("FaANS", "utr5", 1, 140), ("FaANS", "exon", 141, 490),
        ("FaANS", "intron", 491, 830), ("FaANS", "exon", 831, 1170),
        ("FaANS", "utr3", 1171, 1320),
    ]
    rows = ["gene,part,start,end"]
    rows += ["%s,%s,%d,%d" % f for f in feats]
    dump("54-genestructure", "\n".join(rows))
    gl = list(dict.fromkeys(f[0] for f in feats))
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    for y, g in enumerate(gl):
        sub = [f for f in feats if f[0] == g]
        L = max(f[3] for f in sub)
        ax.plot([0, L], [y, y], color="0.75", lw=1.6, zorder=1)
        for _, part, s, e in sub:
            if part == "intron":
                continue
            w = 0.52 if part == "exon" else 0.30
            col = CAT[0] if part == "exon" else CAT[1]
            yy = y + (0.52 - w) / 2
            ax.add_patch(plt.Rectangle((s, yy), e - s, w, facecolor=col,
                                       edgecolor="0.25", lw=0.6))
        ax.text(-40, y, g, ha="right", va="center", fontsize=9.5)
    ax.set_yticks([])
    ax.set_xlabel("position (bp)")
    ax.invert_yaxis()
    ax.spines["left"].set_visible(False)
    handles = [plt.Rectangle((0, 0), 1, 1, color=CAT[0], label="CDS exon"),
               plt.Rectangle((0, 0), 1, 1, color=CAT[1], label="UTR")]
    ax.legend(handles=handles, loc="lower right", ncol=2)
    ax.set_title("Exon-intron structures, five genes (GSDS style, simulated)")
    save(fig, "54-genestructure")


# --------------------------------------------------------------- 55 msa
def msa():
    cons = "MAGKKKVLATGGAGL"
    rows = ["pos,identity,consensus"]
    for i, ch in enumerate(cons):
        ident = 1.0 if i < 3 else max(0.35, 1 - rng.uniform(0, 0.6))
        rows.append("%d,%.2f,%s" % (i + 1, round(ident, 2), ch))
    dump("55-msa", "\n".join(rows))
    dfc = [ln.split(",") for ln in rows[1:]]
    x = np.arange(1, len(dfc) + 1)
    y = [float(r[1]) for r in dfc]
    fig, ax = plt.subplots(figsize=(8.6, 4.0))
    ax.bar(x, y, color=[CAT[0] if v >= 0.8 else (CAT[1] if v >= 0.5 else "0.75")
                        for v in y], width=0.7)
    for xi, r in zip(x, dfc):
        if float(r[1]) >= 0.5:
            ax.text(xi, float(r[1]) + 0.02, r[2], ha="center", fontsize=9)
    ax.set_ylim(0, 1.15)
    ax.set_xlabel("alignment position")
    ax.set_ylabel("fraction identity (12 sequences)")
    ax.set_title("MSA conservation across the N-terminal 15 residues")
    save(fig, "55-msa")


if __name__ == "__main__":
    manhattan()
    qq()
    lddecay()
    admixture()
    phylo()
    pi_fst()
    dotplot()
    kaks()
    chrloc()
    circos()
    genedensity()
    motiflogo()
    genestructure()
    msa()
