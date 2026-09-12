# -*- coding: utf-8 -*-
"""Gallery post 3 (part A): sequencing QC, variants, fine-mapping, breeding
figures 75-91."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch

from common import save, dump, CAT, UP, DOWN

rng = np.random.default_rng(2075)


# ------------------------------------------------------- 75 per-cycle quality
def fastq_qc():
    cycles = list(range(1, 146, 5)) + [150]
    base = 36.0 - 0.062 * (np.array(cycles) - 60) ** 2 / 60.0
    base = np.clip(base, 25.5, None)
    base[:2] -= 3.2                                     # 开头染料残留低质量
    med, q1, q3 = [], [], []
    for m in base:
        s = rng.normal(m, 1.6, 240)
        med.append(np.median(s))
        q1.append(np.percentile(s, 25))
        q3.append(np.percentile(s, 75))
    rows = ["cycle,median_q,q25,q75"]
    rows += ["%d,%.1f,%.1f,%.1f" % v for v in zip(cycles, med, q1, q3)]
    dump("75-fastq-qc", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.axhspan(20, 28, color="#FFD54F", alpha=0.30, lw=0)
    for c, m, a, b in zip(cycles, med, q1, q3):
        ax.plot([c, c], [a, b], color="#1565C0", lw=3.2,
                solid_capstyle="round", alpha=0.85)
        ax.scatter([c], [m], s=9, color="#0D47A1", zorder=3)
    ax.axhline(20, color="#C62828", ls="--", lw=1.1)
    ax.axhline(28, color="#C62828", ls="--", lw=1.1)
    ax.text(151, 20, "Q20", fontsize=8.5, color="#C62828", va="center")
    ax.text(151, 28, "Q28", fontsize=8.5, color="#C62828", va="center")
    ax.set_xlabel("cycle in read")
    ax.set_ylabel("Phred quality score")
    ax.set_title("Per-cycle base quality, 1 x 150 bp run (simulated)")
    save(fig, "75-fastq-qc")


# ------------------------------------------------------------------ 76 gc bias
def gc_bias():
    gc = rng.uniform(28, 72, 90)
    cov = rng.normal(-0.0042 * (gc - 48) ** 2, 0.24)
    bins = np.arange(27.5, 75, 5)
    centers, means = [], []
    for b0, b1 in zip(bins[:-1], bins[1:]):
        sel = (gc >= b0) & (gc < b1)
        if sel.sum() >= 3:
            centers.append((b0 + b1) / 2)
            means.append(cov[sel].mean())
    rows = ["gc_bin_center,mean_log2fc"]
    rows += ["%.1f,%.3f" % v for v in zip(centers, means)]
    dump("76-gc-bias", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.scatter(gc, cov, s=22, color=CAT[0], alpha=0.55, linewidths=0)
    ax.plot(centers, means, "-o", color=CAT[3], lw=2, ms=5, label="binned mean")
    ax.axhline(0, color="0.6", ls=":", lw=1)
    ax.axvline(48, color="0.6", ls=":", lw=1)
    ax.text(48.6, 0.85, "expected GC = 48%", fontsize=9, color="0.4")
    ax.set_xlabel("GC content of window (%)")
    ax.set_ylabel("log2 (observed / expected coverage)")
    ax.set_ylim(-1.8, 1.2)
    ax.legend(loc="lower left")
    ax.set_title("GC bias in sequencing coverage (simulated)")
    save(fig, "76-gc-bias")


# --------------------------------------------------------------- 77 sanger
def sanger():
    seq = "ATGGCGTACCTGAAGTTCGATCCAGGCATTACGGTA"
    qual = rng.integers(30, 42, len(seq)).astype(float)
    het = 22                                            # C/T 双峰
    seq = seq[:het] + "Y" + seq[het + 1:]
    rows = ["pos,base,quality"]
    for i, (b, q) in enumerate(zip(seq, qual)):
        rows.append("%d,%s,%.0f" % (i + 1, b, q))
    dump("77-sanger", "\n".join(rows))
    bcol = {"A": "#2E7D32", "C": "#1565C0", "G": "#33691E", "T": "#C62828"}
    bcol["Y"] = "#6A1B9A"
    x = np.linspace(0, len(seq) - 1, len(seq) * 14)
    fig, ax = plt.subplots(figsize=(9.6, 4.4))
    order = ["A", "C", "G", "T"]
    for i, b in enumerate(seq):
        c = b if b in order else ("C" if i == het else "T")
        for j, base in enumerate(order):
            h = 1.05 + rng.uniform(-0.06, 0.06) if base == c else \
                rng.uniform(0.03, 0.11)
            if i == het and base in ("C", "T"):
                h = 0.62 + rng.uniform(-0.04, 0.04)
            ax.plot(x, 0.9 * j - 0.45 + h * np.exp(-0.5 * ((x - i) / 0.34) ** 2),
                    color=bcol[base], lw=1.4)
    for i, b in enumerate(seq):
        ax.text(i, 3.30, b, ha="center", fontsize=8.5,
                color="#6A1B9A" if i == het else bcol[b], fontweight="bold")
    ax.plot(range(len(seq)), qual / 12.0 + 2.62, color="0.35", lw=1)
    ax.annotate("heterozygous double peak (C/T)", (het, 3.0),
                (het + 2.2, 3.9), fontsize=9, color="#6A1B9A",
                arrowprops=dict(arrowstyle="->", color="#6A1B9A"))
    ax.text(35.8, qual[-1] / 12.0 + 2.62 + 0.18, "quality", fontsize=8,
            color="0.35", ha="right")
    ax.set_yticks([0.9 * j - 0.45 for j in range(4)], order, fontsize=9)
    ax.set_xlabel("base position")
    ax.set_title("Sanger chromatogram, 36 bp window (simulated)")
    ax.set_ylim(-0.6, 5.9)
    save(fig, "77-sanger")


# --------------------------------------------------------------- 78 sashimi
def sashimi():
    exons = [(10, 180), (320, 520), (760, 940)]
    junctions = [(180, 320, 182), (520, 760, 64), (180, 760, 12)]
    rows = ["element,start,end,note"]
    for i, (a, b) in enumerate(exons):
        rows.append("exon,%d,%d,transcript X1" % (a, b))
    for a, b, n in junctions:
        rows.append("junction,%d,%d,%d reads" % (a, b, n))
    dump("78-sashimi", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    x = np.linspace(0, 1000, 2000)
    cov = np.zeros_like(x)
    for a, b in exons:
        sel = (x >= a) & (x <= b)
        cov[sel] = 40 + 14 * np.sin(x[sel] / 9) + rng.normal(0, 1.6, sel.sum())
        cov[sel] *= np.exp(-0.5 * ((x[sel] - (a + b) / 2) / (b - a)) ** 2 * 0.4)
    ax.fill_between(x, 0, cov, color=CAT[0], alpha=0.35)
    ax.plot(x, cov, color=CAT[0], lw=1)
    for a, b, n in junctions:
        h = 90 + 130 * (n / 182.0)
        t = np.linspace(0, np.pi, 80)
        ax.plot(a + (b - a) * (1 - np.cos(t)) / 2, h * np.sin(t) + 62,
                color=CAT[3], lw=1.2 + 4.2 * n / 182.0)
        ax.text((a + b) / 2, h + 66, str(n), ha="center", fontsize=9,
                color=CAT[3], fontweight="bold")
    for k, (a, b) in enumerate(exons):
        ax.add_patch(plt.Rectangle((a, 18), b - a, 26,
                                   facecolor="#8FA6D9", edgecolor="0.25"))
        ax.text((a + b) / 2, 31, "exon %d" % (k + 1), ha="center",
                va="center", fontsize=9)
    ax.set_ylim(0, 330)
    ax.set_xlim(0, 1000)
    ax.set_xlabel("position on transcript (bp)")
    ax.set_ylabel("read coverage")
    ax.set_title("RNA-seq coverage with sashimi junction arcs (simulated)")
    save(fig, "78-sashimi")


# --------------------------------------------------------------- 79 pileup
def pileup():
    reads = []
    for i in range(14):
        hap = 0 if i < 7 else 1
        reads.append((i, hap, rng.integers(0, 25), rng.integers(135, 165)))
    snp = 82
    rows = ["read,haplotype,start,end,base_at_82"]
    for i, hap, a, b in reads:
        b82 = "T" if hap == 0 else "C"
        rows.append("r%d,%d,%d,%d,%s" % (i + 1, hap, a, b, b82))
    dump("79-pileup", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    hcol = ["#4C72B0", "#DD8452"]
    for i, hap, a, b in reads:
        ax.add_patch(plt.Rectangle((a, i + 0.2), b - a, 0.6,
                                   facecolor=hcol[hap], alpha=0.35,
                                   edgecolor=hcol[hap], lw=0.8))
        ax.text(b + 1.5, i + 0.5, "T" if hap == 0 else "C", fontsize=7.5,
                va="center", color=hcol[hap])
        if i % 5 == 2:
            e = rng.integers(a + 8, b - 8)
            if abs(e - snp) > 6:
                ax.scatter([e], [i + 0.5], s=16, color="0.25", zorder=4)
    ax.axvline(snp, color="#C44E52", lw=1.4)
    ax.text(snp + 1.5, 14.35, "SNP T/C (pos 82)", fontsize=9, color="#C44E52")
    ax.set_ylim(-0.3, 15)
    ax.set_xlim(-2, 175)
    ax.set_xlabel("position in region (bp)")
    ax.set_ylabel("reads")
    ax.set_title("Read pileup around a heterozygous SNP (simulated)")
    save(fig, "79-pileup")


# ---------------------------------------------------------- 80 mut spectrum
def mut_spectrum():
    classes = ["C>A", "C>G", "C>T", "T>A", "T>C", "T>G"]
    counts = [68, 41, 132, 37, 52, 45]
    rows = ["mutation_class,count"]
    rows += ["%s,%d" % v for v in zip(classes, counts)]
    dump("80-mut-spectrum", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    cols = ["#4C72B0", "#937860", "#C44E52", "#55A868", "#DD8452", "#8172B3"]
    ax.bar(classes, counts, color=cols, alpha=0.9, width=0.62)
    for i, v in enumerate(counts):
        ax.text(i, v + 3, "%d (%.0f%%)" % (v, v / 375 * 100), ha="center",
                fontsize=9)
    ax.annotate("C>T dominance:\ncytosine deamination", (2, 132), (3.15, 122),
                fontsize=9, arrowprops=dict(arrowstyle="->", lw=1))
    ax.set_xlabel("mutation class (pyrimidine reference)")
    ax.set_ylabel("number of SNVs")
    ax.set_ylim(0, 155)
    ax.set_title("SNV mutation spectrum, n = 375 (simulated)")
    save(fig, "80-mut-spectrum")


# ------------------------------------------------------------------- 81 SFS
def sfs():
    n = 10
    counts = [286, 104, 61, 33, 21, 14, 9, 6, 4, 2]
    rows = ["derived_allele_count,variants"]
    rows += ["%d,%d" % v for v in zip(range(1, n + 1), counts)]
    dump("81-sfs", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.bar(range(1, n + 1), counts, color=CAT[0], alpha=0.85, width=0.62)
    ax.set_yscale("log")
    ax.set_ylim(1, 900)
    for i, v in enumerate(counts):
        ax.text(i + 1, v * 1.15, str(v), ha="center", fontsize=8.5)
    ax.annotate("rare-variant excess:\nrecent growth or purifying selection",
                (1, 286), (3.4, 420), fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=1))
    ax.set_xlabel("derived allele count (of 20 chromosomes)")
    ax.set_ylabel("number of variants (log)")
    ax.set_title("Unfolded site frequency spectrum (simulated)")
    save(fig, "81-sfs")


# ---------------------------------------------------------------- 82 tajima
def tajima():
    win = np.arange(5, 500, 10)
    td = rng.normal(0.05, 0.28, len(win))
    sel = (win >= 215) & (win <= 285)
    td[sel] = rng.normal(-2.05, 0.22, sel.sum())
    rows = ["window_kb,tajima_d"]
    rows += ["%d,%.3f" % v for v in zip(win, td)]
    dump("82-tajima", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.plot(win, td, "-o", ms=3.5, color=CAT[0], alpha=0.8)
    ax.axhline(0, color="0.7", lw=0.8)
    ax.axhline(-1.5, color=CAT[3], ls="--", lw=1.2)
    ax.text(487, -1.42, "threshold -1.5", fontsize=8.5, color=CAT[3],
            ha="right")
    ax.axvspan(215, 285, color=CAT[3], alpha=0.08)
    ax.text(250, 0.85, "selective sweep", ha="center", fontsize=9.5,
            color=CAT[3])
    ax.set_xlabel("position on Chr4 (kb)")
    ax.set_ylabel("Tajima's D")
    ax.set_title("Sliding-window Tajima's D (simulated)")
    save(fig, "82-tajima")


# ------------------------------------------------------- 83 haplotype network
def hap_network():
    nodes = [("H1", 0, 0, 46), ("H2", 2.2, 0.7, 18), ("H3", 1.1, -1.4, 11),
             ("H4", -2.0, 0.9, 9), ("H5", -1.2, -1.7, 6), ("H6", 3.6, -0.5, 4),
             ("H7", -3.3, 0.1, 3), ("H8", 2.7, 1.9, 2)]
    edges = [("H1", "H2", 1), ("H1", "H3", 2), ("H1", "H4", 1),
             ("H1", "H5", 3), ("H2", "H6", 2), ("H4", "H7", 2),
             ("H2", "H8", 3), ("H3", "H5", 1)]
    rows_n = ["haplotype,x,y,samples"]
    rows_n += ["%s,%.1f,%.1f,%d" % v for v in nodes]
    rows_e = ["hap1,hap2,mutations"]
    rows_e += ["%s,%s,%d" % v for v in edges]
    dump("83-hap-nodes", "\n".join(rows_n))
    dump("83-hap-edges", "\n".join(rows_e))
    pos = {v[0]: (v[1], v[2]) for v in nodes}
    fig, ax = plt.subplots(figsize=(7.8, 6.2))
    for a, b, m in edges:
        (x0, y0), (x1, y1) = pos[a], pos[b]
        ax.plot([x0, x1], [y0, y1], color="0.6", lw=1.1, zorder=1)
        ax.text((x0 + x1) / 2 + 0.06, (y0 + y1) / 2 + 0.10, str(m),
                fontsize=8.5, color="0.35")
    for name, x, y, c in nodes:
        ax.scatter([x], [y], s=110 * c, color=CAT[0], alpha=0.55,
                   edgecolors=CAT[0], linewidths=1.6, zorder=3)
        ax.text(x, y, "%s\n%d" % (name, c), ha="center", va="center",
                fontsize=8.5, zorder=4)
    ax.text(-3.9, -2.3, "circle area = haplotype frequency\nedge label = mutated sites",
            fontsize=8.5, color="0.4")
    ax.set_xlim(-4.3, 4.6)
    ax.set_ylim(-2.6, 2.6)
    ax.axis("off")
    ax.set_title("Median-joining haplotype network (simulated)")
    save(fig, "83-hap-network")


# ------------------------------------------------------------------- 84 GRM
def grm():
    n = 12
    K = rng.normal(0.02, 0.03, (n, n))
    fam = [(0, 3), (4, 7), (8, 11)]
    for a, b in fam:
        K[a:b + 1, a:b + 1] += rng.uniform(0.38, 0.55)
    K = (K + K.T) / 2
    np.fill_diagonal(K, 1.0)
    rows = ["id," + ",".join("s%d" % (i + 1) for i in range(n))]
    for i in range(n):
        rows.append("s%d," % (i + 1) + ",".join("%.3f" % v for v in K[i]))
    dump("84-grm", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.0, 5.8))
    im = ax.imshow(K, cmap="Blues", vmin=0, vmax=1)
    for b, c in zip([0, 4, 8], ["Fam A", "Fam B", "Fam C"]):
        ax.add_patch(plt.Rectangle((b - 0.5, b - 0.5), 4, 4, fill=False,
                                   edgecolor=CAT[3], ls="--", lw=1.4))
        ax.text(b + 1.5, -0.75, c, ha="center", fontsize=9.5, color=CAT[3])
    ax.set_xticks(range(n), ["s%d" % (i + 1) for i in range(n)], fontsize=8,
                  rotation=45)
    ax.set_yticks(range(n), ["s%d" % (i + 1) for i in range(n)], fontsize=8)
    ax.grid(False)
    fig.colorbar(im, ax=ax, shrink=0.82, label="kinship")
    ax.set_title("Genomic relationship matrix, 3 families (simulated)")
    save(fig, "84-grm")


# ------------------------------------------------------------ 85 sweep trio
def sweep_trio():
    win = np.arange(100, 6000, 200)
    pi_a = rng.normal(0.0016, 0.00008, len(win))
    pi_b = rng.normal(0.0015, 0.00008, len(win))
    fst = rng.normal(0.08, 0.012, len(win))
    xp = rng.normal(0.2, 0.25, len(win))
    sel = (win >= 2700) & (win <= 3300)
    pi_a[sel] = rng.normal(0.00042, 0.00004, sel.sum())
    fst[sel] = rng.normal(0.44, 0.03, sel.sum())
    xp[sel] = rng.normal(3.9, 0.45, sel.sum())
    xp[np.argmax(xp[sel]) + np.where(sel)[0][0]] = 4.72
    rows = ["window_kb,pi_A,pi_B,fst,xp_clr"]
    rows += ["%d,%.5f,%.5f,%.3f,%.2f" % v
             for v in zip(win, pi_a, pi_b, fst, xp)]
    dump("85-sweep-trio", "\n".join(rows))
    fig, axes = plt.subplots(3, 1, figsize=(9.0, 6.6), sharex=True,
                             gridspec_kw=dict(hspace=0.12,
                                              height_ratios=[1.2, 1, 1.2]))
    for ax in axes:
        ax.axvspan(2700, 3300, color=CAT[3], alpha=0.08)
    axes[0].plot(win, pi_a * 1000, color=CAT[0], lw=1.7, label="population A")
    axes[0].plot(win, pi_b * 1000, color=CAT[2], lw=1.7, label="population B")
    axes[0].set_ylabel("pi (x1e-3)")
    axes[0].legend(loc="lower left", fontsize=8.5)
    axes[1].plot(win, fst, color="0.3", lw=1.7)
    axes[1].axhline(0.25, color=CAT[3], ls="--", lw=1)
    axes[1].set_ylabel("Fst")
    axes[2].plot(win, xp, color=CAT[1], lw=1.7)
    axes[2].set_ylabel("XP-CLR score")
    axes[2].set_xlabel("position on Chr6 (kb)")
    axes[2].annotate("peak 4.72", (win[np.argmax(xp)], 4.72),
                     (win[np.argmax(xp)] - 1050, 4.35), fontsize=9,
                     arrowprops=dict(arrowstyle="->", lw=1))
    axes[0].set_title("Three-statistic selective sweep scan (simulated)")
    save(fig, "85-sweep-trio")


# ------------------------------------------------------- 86 structure duo
def structure_duo():
    pops = ["west", "east", "south"]
    cols = {"west": 0, "east": 1, "south": 2}
    mus = [(-3.2, 1.4), (1.6, 2.6), (1.1, -2.7)]
    data = []
    for p in pops:
        for i in range(10):
            pc1, pc2 = rng.normal(mus[cols[p]], (0.75, 0.6))
            if p == "west":
                q = rng.dirichlet([1.2, 8.5, 7.5])
            elif p == "east":
                q = rng.dirichlet([7.5, 1.3, 8.2])
            else:
                q = rng.dirichlet([8.0, 7.6, 1.2])
            data.append(("%s%d" % (p[0].upper(), i + 1), p, pc1, pc2, *q))
    rows = ["ind,pop,pc1,pc2,q1,q2,q3"]
    rows += ["%s,%s,%.2f,%.2f,%.3f,%.3f,%.3f" % v for v in data]
    dump("86-structure", "\n".join(rows))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.8),
                                   gridspec_kw=dict(width_ratios=[1, 1.35]))
    pcol = dict(zip(pops, [CAT[0], CAT[1], CAT[2]]))
    for p in pops:
        sub = [v for v in data if v[1] == p]
        ax1.scatter([v[2] for v in sub], [v[3] for v in sub], s=38,
                    color=pcol[p], edgecolors="white", label=p)
    ax1.set_xlabel("PC1 (34%)")
    ax1.set_ylabel("PC2 (21%)")
    ax1.legend(fontsize=9)
    left = np.zeros(len(data))
    for k in range(3):
        ax2.barh(range(len(data)), [v[4 + k] for v in data], left=left,
                 color=CAT[k], height=0.86)
        left += np.array([v[4 + k] for v in data])
    ax2.set_yticks(range(len(data)), [v[0] for v in data], fontsize=6.5)
    ax2.invert_yaxis()
    ax2.set_xlabel("ancestry proportion (K = 3)")
    for y, p in [(4.5, "west"), (14.5, "east"), (24.5, "south")]:
        ax2.text(-0.02, y, p, transform=ax2.get_yaxis_transform(),
                 ha="right", fontsize=9)
    ax2.set_xlim(0, 1)
    ax1.set_title("PCA", fontsize=11)
    ax2.set_title("ADMIXTURE, K = 3", fontsize=11)
    save(fig, "86-structure")


# ------------------------------------------------------------- 87 locuszoom
def locuszoom():
    lead_kb, lead_p = 91.0, 2.1e-9
    pos = np.sort(np.r_[rng.uniform(20, 180, 86), [lead_kb]])
    d = np.abs(pos - lead_kb)
    r2 = np.clip(np.exp(-d / 26) * rng.uniform(0.82, 1.08, len(pos)), 0.01, 1)
    r2[np.argmin(d)] = 1.0
    lp = np.where(pos == lead_kb, -np.log10(lead_p), np.nan)
    bg = -np.log10(rng.uniform(1e-4, 0.4, len(pos)))
    lp = np.where(np.isnan(lp), r2 * 8.68 + rng.normal(0, 0.30, len(pos)), lp)
    lp = np.maximum(lp, bg)
    bins = [(0.8, 1.01, "#D62728"), (0.6, 0.8, "#FF7F0E"), (0.4, 0.6, "#2CA02C"),
            (0.2, 0.4, "#9EDAE5"), (0.0, 0.2, "#1F77B4")]
    genes = [(30, 52, "FaDWF4", 1), (70, 96, "FaBRI1", -1), (128, 168, "FaCHS", 1)]
    rows = ["pos_kb,pvalue,r2_to_lead"]
    for p, v, r in zip(pos, 10 ** (-lp), r2):
        rows.append("%.1f,%.2e,%.2f" % (p, v, r))
    dump("87-locuszoom", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(9.6, 5.4))
    for lo, hi, c in bins:
        sel = (r2 >= lo) & (r2 < hi)
        ax.scatter(pos[sel], lp[sel], s=18, color=c, alpha=0.9,
                   label="%.1f-%.1f" % (lo, min(hi, 1.0)), linewidths=0)
    ax.scatter([lead_kb], [lp[np.argmin(d)]], s=120, marker="D",
               color="#D62728", edgecolors="white", zorder=5)
    ax.text(lead_kb + 2, lp.max(), "FaDWF4 lead", fontsize=9, fontweight="bold")
    ax.axhline(-np.log10(5e-8), color="0.4", ls="--", lw=1)
    ax.text(20, -np.log10(5e-8) + 0.18, "5e-8", fontsize=8.5, color="0.3")
    ax2 = ax.twinx()
    ax2.plot(np.sort(rng.uniform(20, 180, 25)),
             rng.uniform(0.2, 3.4, 25), color="0.6", lw=1, alpha=0.7)
    ax2.set_ylabel("recombination (cM/Mb)", color="0.45")
    ax2.set_ylim(0, 6)
    for g0, g1, name, side in genes:
        y = -1.15 if side < 0 else -0.55
        ax.annotate("", xy=(g1, y), xytext=(g0, y),
                    arrowprops=dict(arrowstyle="->", color=CAT[0], lw=3.5))
        ax.text((g0 + g1) / 2, y - 0.42, name, ha="center", fontsize=8.5,
                color=CAT[0])
    ax.set_xlim(20, 180)
    ax.set_ylim(-1.8, 9.6)
    ax.set_xlabel("position on Chr3 (kb)")
    ax.set_ylabel("-log10(p)")
    ax.set_title("Regional association with LD coloring (simulated)")
    ax.legend(title="r2 to lead", loc="upper right", fontsize=8, title_fontsize=8)
    save(fig, "87-locuszoom")


# -------------------------------------------------------------------- 88 PIP
def pip():
    pos = np.sort(rng.uniform(40, 160, 22))
    top = [0.74, 0.11, 0.055, 0.028, 0.02]
    vals = np.r_[top, rng.uniform(0.002, 0.05, 17)]
    order = rng.permutation(len(pos))
    v = vals[order]
    inset = np.isin(v, top)
    rows = ["variant,pos_kb,pip,in_95set"]
    for i, (p, vv, s) in enumerate(zip(pos, v, inset)):
        rows.append("rs%d,%.1f,%.3f,%s" % (i + 1, p, vv, str(bool(s)).lower()))
    dump("88-pip", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    for p, vv, s in zip(pos, v, inset):
        ax.bar([p], [vv], width=2.2, color=CAT[3] if s else "0.72")
    ax.annotate("PIP = 0.74", (pos[v == 0.74][0], 0.74),
                (pos[v == 0.74][0] + 12, 0.70), fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=1))
    ax.set_xlabel("position on Chr5 (kb)")
    ax.set_ylabel("posterior inclusion probability")
    ax.set_ylim(0, 0.82)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=CAT[3], label="in 95% credible set (5 variants)"),
                       Patch(color="0.72", label="outside")],
              loc="upper right", fontsize=9)
    ax.set_title("SuSiE fine-mapping PIP (simulated)")
    save(fig, "88-pip")


# ------------------------------------------------------------------ 89 QTL
def qtl_lod():
    cm = np.arange(0, 131, 5)
    lod = 0.32 + 3.55 * np.exp(-0.5 * ((cm - 52) / 7.2) ** 2) \
        + rng.normal(0, 0.06, len(cm))
    rows = ["cM,lod"]
    rows += ["%d,%.2f" % v for v in zip(cm, lod)]
    dump("89-qtl-lod", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(cm, lod, "-o", ms=3.5, color=CAT[0])
    ax.axhline(2.9, color=CAT[3], ls="--", lw=1.2)
    ax.text(128, 2.98, "permutation threshold 2.9", fontsize=8.5,
            color=CAT[3], ha="right")
    ax.axvspan(44, 61, color=CAT[1], alpha=0.12)
    ax.text(52.5, 0.75, "95% CI\n44-61 cM", ha="center", fontsize=9,
            color=CAT[1])
    ax.annotate("peak LOD 3.72", (50, 3.72), (66, 3.42), fontsize=9.5,
                arrowprops=dict(arrowstyle="->", lw=1))
    ax.set_xlabel("position on LG4 (cM)")
    ax.set_ylabel("LOD score")
    ax.set_title("QTL mapping for seed weight, LG4 (simulated)")
    save(fig, "89-qtl-lod")


# ------------------------------------------------------------ 90 linkage map
def linkage_map():
    groups = {
        1: [("M1", 0), ("M2", 11), ("M3", 24), ("M4", 38), ("M5", 55), ("M6", 72)],
        2: [("M7", 0), ("M8", 9), ("M9", 21), ("M10", 33), ("M11", 47)],
        3: [("M12", 0), ("FaDWF4", 14), ("M13", 29), ("M14", 44), ("M15", 58), ("M16", 69)],
        4: [("M17", 0), ("M18", 13), ("M19", 26), ("M20", 41)],
        5: [("M21", 0), ("M22", 16), ("M23", 31), ("M24", 45), ("M25", 59)],
        6: [("M26", 0), ("M27", 12), ("M28", 27)],
        7: [("M29", 0), ("M30", 14), ("M31", 30), ("M32", 43), ("M33", 57)],
    }
    rows = ["group,marker,cM"]
    for g, ms in groups.items():
        for m, c in ms:
            rows.append("%d,%s,%d" % (g, m, c))
    dump("90-linkage-map", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.6, 6.8))
    gw = 1.6
    for gi, (g, ms) in enumerate(groups.items()):
        x = gi * gw
        top = max(c for _, c in ms)
        ax.plot([x, x], [0, top], color="#B9CAF2", lw=7, solid_capstyle="round")
        ax.text(x, top + 5, "LG%d" % g, ha="center", fontsize=10,
                fontweight="bold")
        for mi, (m, c) in enumerate(ms):
            side = 1 if mi % 2 == 0 else -1
            ax.plot([x + side * 0.16, x + side * 0.62], [c, c],
                    color="0.4", lw=0.9)
            ax.scatter([x + side * 0.62], [c], s=14, color=CAT[3], zorder=3)
            ax.text(x + side * 0.70, c, m, fontsize=7.2, va="center",
                    ha="left" if side == 1 else "right")
        if g == 3:
            ax.add_patch(plt.Rectangle((x - 0.20, 44), 0.40, 15,
                                       facecolor=CAT[1], alpha=0.30))
            ax.text(x, 40.5, "QTL", ha="center", fontsize=8, color=CAT[1])
    ax.set_xlim(-1.6, 7 * gw + 0.4)
    ax.set_ylim(-3, 82)
    ax.axis("off")
    ax.set_title("Genetic linkage map, 33 markers / 7 LGs (simulated)")
    save(fig, "90-linkage-map")


# ------------------------------------------------------------------ 91 AMMI
def ammi():
    envs = ["E1", "E2", "E3", "E4", "E5"]
    Y = np.array([
        [4.2, 4.9, 3.1, 4.6, 3.4],
        [4.8, 5.1, 2.9, 5.0, 3.6],
        [3.4, 3.9, 3.8, 3.5, 4.3],
        [5.0, 4.7, 2.6, 5.3, 3.1],
        [3.8, 4.3, 3.4, 4.1, 3.9],
        [4.5, 5.4, 2.8, 5.5, 3.3],
    ])
    Y = Y.T                                          # 行=环境，列=基因型
    rows = ["env," + ",".join("G%d" % (i + 1) for i in range(6))]
    for e, r in zip(envs, Y):
        rows.append("%s,%s" % (e, ",".join("%.1f" % v for v in r)))
    dump("91-ammi-yield", "\n".join(rows))
    R = Y - Y.mean(0) - Y.mean(1)[:, None] + Y.mean()
    U, S, Vt = np.linalg.svd(R, full_matrices=False)
    g = Vt.T[:, 0] * S[0]
    e = U[:, 0] * S[0]
    fig, ax = plt.subplots(figsize=(7.4, 6.0))
    ax.scatter(g, np.zeros(6), s=70, color=CAT[0], zorder=3)
    for i in range(6):
        ax.text(g[i] * 1.14, 0.14 if i % 2 else -0.20, "G%d" % (i + 1),
                fontsize=10, color=CAT[0], fontweight="bold", ha="center")
    for j in range(5):
        ax.annotate("", xy=(e[j], U[j, 1] * S[1] * 6), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color=CAT[3], lw=1.4))
        ax.text(e[j] * 1.16, U[j, 1] * S[1] * 6 * 1.16, envs[j], fontsize=9,
                color=CAT[3])
    ax.axhline(0, color="0.8", lw=0.8)
    ax.axvline(0, color="0.8", lw=0.8)
    ax.set_xlim(-2.8, 2.8)
    ax.set_ylim(-3.4, 3.4)
    ax.set_xlabel("IPCA1 (%.0f%% of GxE)" % (S[0] ** 2 / (S ** 2).sum() * 100))
    ax.set_ylabel("IPCA2 (%.0f%%)" % (S[1] ** 2 / (S ** 2).sum() * 100))
    ax.set_title("AMMI1 biplot: G mean x IPCA (simulated)")
    save(fig, "91-ammi")


if __name__ == "__main__":
    fastq_qc()
    gc_bias()
    sanger()
    sashimi()
    pileup()
    mut_spectrum()
    sfs()
    tajima()
    hap_network()
    grm()
    sweep_trio()
    structure_duo()
    locuszoom()
    pip()
    qtl_lod()
    linkage_map()
    ammi()
