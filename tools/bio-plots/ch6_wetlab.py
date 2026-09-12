# -*- coding: utf-8 -*-
"""Chapter 6 - wet-lab validation figures (qPCR, gel, microscopy, flow)."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrow, Rectangle, FancyBboxPatch
from scipy import stats

from common import save, dump, csv_cols, num, CAT

rng = np.random.default_rng(23)


def circled(ax, x, y, n, r=0.35, color="black"):
    """A small numbered marker used for figure-caption callouts."""
    ax.scatter([x], [y], s=r * 260, facecolor="white", edgecolor=color,
               linewidth=1.1, zorder=6)
    ax.text(x, y, str(n), ha="center", va="center", fontsize=8.5,
            color=color, zorder=7, fontweight="bold")


# ------------------------------------------------------------------ 23 qPCR
def qpcr_bar():
    ct = {
        ("DWF4", "control"): [(24.1, 18.2), (24.3, 18.1), (24.2, 18.3)],
        ("DWF4", "treated"): [(22.4, 18.2), (22.6, 18.0), (22.5, 18.1)],
        ("CHS", "control"): [(21.0, 18.2), (21.2, 18.1), (21.1, 18.3)],
        ("CHS", "treated"): [(18.9, 18.2), (19.1, 18.0), (19.0, 18.1)],
        ("ANS", "control"): [(23.2, 18.2), (23.4, 18.1), (23.3, 18.3)],
        ("ANS", "treated"): [(21.4, 18.2), (21.6, 18.0), (21.5, 18.1)],
        ("ANR", "control"): [(22.8, 18.2), (23.0, 18.1), (22.9, 18.3)],
        ("ANR", "treated"): [(22.9, 18.2), (23.1, 18.0), (23.0, 18.1)],
    }
    rows = ["gene,condition,rep,Ct_target,Ct_ref"]
    for (g, cond), reps in ct.items():
        for i, (a, b) in enumerate(reps, 1):
            rows.append("%s,%s,%d,%.1f,%.1f" % (g, cond, i, a, b))
    dump("23-qrt-pcr", "\n".join(rows))

    genes = ["DWF4", "CHS", "ANS", "ANR"]
    d = {(g, cond): [a - b for a, b in v] for (g, cond), v in ct.items()}
    means, errs, pvals = [], [], []
    for g in genes:
        dc_ctl = np.array(d[(g, "control")])
        dc_trt = np.array(d[(g, "treated")])
        fold_ctl = 2 ** (-(dc_ctl - dc_ctl.mean()))
        fold_trt = 2 ** (-(dc_trt - dc_ctl.mean()))
        means.append([fold_ctl.mean(), fold_trt.mean()])
        errs.append([fold_ctl.std(ddof=1), fold_trt.std(ddof=1)])
        pvals.append(stats.ttest_ind(dc_ctl, dc_trt).pvalue)

    x = np.arange(len(genes))
    fig, ax = plt.subplots(figsize=(7.0, 5.2))
    ax.bar(x - 0.18, [m[0] for m in means], 0.32, yerr=[e[0] for e in errs],
           capsize=4, color="0.72", label="control (set to 1)")
    ax.bar(x + 0.18, [m[1] for m in means], 0.32, yerr=[e[1] for e in errs],
           capsize=4, color=CAT[0], label="treated")
    for i, p in enumerate(pvals):
        star = "***" if p < 0.001 else ("**" if p < 0.01 else ("*" if p < 0.05 else "ns"))
        top = max(means[i][0] + errs[i][0], means[i][1] + errs[i][1])
        ax.text(x[i], top + 0.22, star, ha="center", fontsize=11)
    ax.set_xticks(x, genes)
    ax.set_ylim(0, 5.9)
    ax.set_ylabel("relative expression (2^-DDCt)")
    ax.set_title("qRT-PCR validation, 3 biological reps, error bar = SD")
    ax.legend()
    save(fig, "23-qrt-pcr-bar")


# ------------------------------------------------------------ 24 amplification
def amp_curve():
    cyc = np.arange(2, 41, 2)

    def sig(c, ct, amp):
        return 0.04 + amp / (1 + np.exp(-(c - ct) / 2.2))

    fa = sig(cyc, 18, 1.1)
    fb = sig(cyc, 24, 0.9)
    fntc = 0.04 + rng.normal(0, 0.002, len(cyc)).clip(-0.001, 0.001)
    rows = ["cycle,sample_A,sample_B,NTC"]
    rows += ["%d,%.3f,%.3f,%.3f" % (a, b, cc, dd)
             for a, b, cc, dd in zip(cyc, fa, fb, fntc)]
    dump("24-amp-curve", "\n".join(rows))
    thr = 0.22

    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    ax.plot(cyc, fa, "-o", ms=4, color=CAT[0], label="target, sample A")
    ax.plot(cyc, fb, "-o", ms=4, color=CAT[1], label="target, sample B")
    ax.plot(cyc, fntc, "-o", ms=4, color="0.6", label="NTC (no template)")
    ax.axhline(thr, color="0.35", ls="--", lw=1.2)
    ax.text(39.5, thr + 0.015, "threshold", ha="right", fontsize=9, color="0.35")
    for f, col in [(fa, CAT[0]), (fb, CAT[1])]:
        ct = cyc[np.argmax(f > thr)]
        ax.axvline(ct, color=col, ls=":", lw=1.2)
        ax.text(ct + 0.25, 0.012, "Ct = %d" % ct, fontsize=9.5, color=col)
    ax.set_xlabel("cycle number")
    ax.set_ylabel("normalized fluorescence (Rn)")
    ax.set_title("qPCR amplification curves")
    ax.legend(loc="upper left")
    save(fig, "24-amp-curve")


# ----------------------------------------------------------------- 25 melting
def melt_curve():
    T = np.arange(72, 95, 2)

    def flu(Tm_list, amp_list, w=1.2):
        return sum(a / (1 + np.exp((T - t) / w)) for t, a in zip(Tm_list, amp_list))

    f_good = flu([82], [1.0])
    f_bad = flu([76, 82], [0.35, 0.65])
    dT = np.gradient(T)
    der_good = -np.gradient(f_good, T)
    der_bad = -np.gradient(f_bad, T)

    rows = ["temperature,fluor_good,fluor_two_peak"]
    rows += ["%d,%.3f,%.3f" % (t, a, b) for t, a, b in zip(T, f_good, f_bad)]
    dump("25-melt-curve", "\n".join(rows))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.8), sharex=True)
    ax1.plot(T, f_good, "-o", ms=4, color=CAT[0], label="single amplicon")
    ax1.plot(T, f_bad, "-o", ms=4, color=CAT[1], label="two amplicons")
    ax1.set_xlabel("temperature (C)")
    ax1.set_ylabel("fluorescence (fraction of initial)")
    ax1.set_title("A. Melting curves")
    ax1.legend()
    ax2.plot(T, der_good, "-o", ms=4, color=CAT[0])
    ax2.plot(T, der_bad, "-o", ms=4, color=CAT[1])
    ax2.set_xlabel("temperature (C)")
    ax2.set_ylabel("-d(F) / dT")
    ax2.set_title("B. Derivative peaks (= Tm)")
    pk_g = T[np.argmax(der_good)]
    ax2.annotate("Tm = %.0f C" % pk_g, (pk_g, der_good.max()),
                 (72.0, 0.150), fontsize=9.5, color=CAT[0],
                 arrowprops=dict(arrowstyle="-", color=CAT[0], lw=0.9))
    i82 = int(np.where(T == 82)[0][0])
    i76 = int(np.where(T == 76)[0][0])
    circled(ax2, 82.4, der_bad[i82] + 0.003, 1)
    ax2.text(83.2, der_bad[i82] + 0.004, "main peak (target)", fontsize=8.5, va="center")
    circled(ax2, 74.9, der_bad[i76] + 0.003, 2)
    ax2.text(68.3, 0.098, "extra peak =\nprimer-dimer /\nnon-specific",
             fontsize=8.5, ha="left", va="center")
    circled(ax2, 81.6, der_good[i82] - 0.004, 3)
    ax2.text(0.98, 0.04, "one sharp peak = one amplicon = specific assay",
             transform=ax2.transAxes, fontsize=9, color="0.3", va="bottom", ha="right")
    save(fig, "25-melt-curve")


# ------------------------------------------------------------- 26 amplicon map
def amplicon_cds():
    csv = """feature,start,end
exon1,1,281
intron1,282,381
exon2,382,655
intron2,656,755
exon3,756,861
forward_primer,400,422
reverse_primer,610,632
product,400,632"""
    dump("26-amplicon-cds", csv)
    _, c = csv_cols(csv)

    fig, ax = plt.subplots(figsize=(9.2, 3.6))
    ax.grid(False)
    y_exon, y_primer, y_prod = 1.0, 1.9, 2.7
    # backbone
    ax.plot([0, 900], [y_exon, y_exon], color="0.75", lw=2, zorder=1)
    for i, (f, s, e) in enumerate(zip(c["feature"], num(c, "start"), num(c, "end"))):
        if f.startswith("exon"):
            ax.add_patch(Rectangle((s, y_exon - 0.28), e - s, 0.56,
                                   facecolor=CAT[0], edgecolor="0.2", zorder=2))
            ax.text((s + e) / 2, y_exon - 0.65, f, ha="center", fontsize=8.5)
        elif f.startswith("intron"):
            ax.plot([s, e], [y_exon, y_exon], color="0.75", lw=2, zorder=1)
        elif f.endswith("primer"):
            col = CAT[1] if f.startswith("forward") else CAT[2]
            dy = 0.42 if f.startswith("forward") else -0.62
            ax.add_patch(FancyArrow(s, y_primer, e - s, 0, width=0.14, head_width=0.42,
                                    head_length=26, length_includes_head=True,
                                    facecolor=col, edgecolor="0.2", zorder=3))
            ax.text((s + e) / 2, y_primer + dy, f.replace("_", " "), ha="center",
                    fontsize=8.5, color=col)
    p0, p1 = 400, 632
    ax.plot([p0, p0, p1, p1], [y_primer + 0.6, y_prod, y_prod, y_primer + 0.6],
            color="0.3", lw=1.2)
    ax.text((p0 + p1) / 2, y_prod + 0.14, "product 233 bp (exon2 only, no intron)",
            ha="center", fontsize=9.5)
    ax.plot([1, 1], [y_exon - 0.75, y_exon + 0.75], color="0.2", lw=1.2)
    ax.text(1, y_exon + 0.95, "ATG", ha="left", fontsize=8.5, fontweight="bold")
    ax.plot([861, 861], [y_exon - 0.75, y_exon + 0.75], color="0.2", lw=1.2)
    ax.text(861, y_exon + 0.95, "stop", ha="right", fontsize=8.5, fontweight="bold")
    ax.set_xticks(range(0, 901, 100))
    ax.set_xlabel("position in CDS (bp)")
    ax.set_ylim(0.2, 3.6)
    ax.set_yticks([])
    ax.set_title("qPCR primers anchored on the CDS")
    ax.spines["left"].set_visible(False)
    save(fig, "26-amplicon-cds")


# --------------------------------------------------------------- 27 WB / Co-IP
def wb_coip():
    fig, ax = plt.subplots(figsize=(7.6, 5.6))
    ax.grid(False)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.add_patch(Rectangle((0.7, 0.6), 8.6, 8.8, facecolor="#0B0B0B"))
    lanes = {"Input": 2.6, "IP: IgG": 5.0, "IP: anti-DWF4": 7.6}
    for name, x0 in lanes.items():
        ax.text(x0, 8.85, name, ha="center", fontsize=9.5, color="white")

    def band(x0, y0, w, h, intensity):
        for k, a in [(3, 0.10), (2, 0.22), (1, 0.5)]:
            ax.add_patch(FancyBboxPatch((x0 - w / 2 - k * 0.045, y0 - h / 2 - k * 0.028),
                                        w + 2 * k * 0.045, h + 2 * k * 0.028,
                                        boxstyle="round,pad=0.02",
                                        facecolor="white", alpha=a * intensity,
                                        edgecolor="none"))
        ax.add_patch(FancyBboxPatch((x0 - w / 2, y0 - h / 2), w, h,
                                    boxstyle="round,pad=0.02", facecolor="white",
                                    alpha=min(1, 0.55 + 0.45 * intensity), edgecolor="none"))

    mw = [("75", 7.3), ("50", 5.4), ("37", 3.9), ("25", 2.5)]
    for label, y0 in mw:
        ax.text(1.15, y0, label, ha="center", fontsize=8.5, color="white")
    ax.text(1.15, 8.0, "kDa", ha="center", fontsize=8.5, color="white")

    ax.text(5.0, 7.7, "blot 1: probed with anti-DWF4", ha="center", fontsize=9,
            color="#9ADBFE")
    band(2.6, 5.4, 1.5, 0.34, 0.8)
    band(7.6, 5.4, 1.5, 0.34, 1.0)
    ax.text(9.55, 5.4, "43 kDa", va="center", fontsize=8.5, color="white")

    ax.plot([0.9, 9.1], [4.55, 4.55], color="#333333", lw=1)
    ax.text(5.0, 4.15, "blot 2: same membrane, re-probed with anti-BZR1", ha="center",
            fontsize=9, color="#B9F6CA")
    band(2.6, 2.9, 1.5, 0.34, 0.45)
    band(7.6, 2.9, 1.5, 0.34, 0.75)
    ax.text(9.55, 2.9, "58 kDa", va="center", fontsize=8.5, color="white")

    ax.text(5.0, 0.25, "BZR1 is pulled down only with anti-DWF4 -> the two proteins interact",
            ha="center", fontsize=9.5, color="white")
    ax.set_title("Co-IP schematic (simulated bands, not a real blot)", pad=10)
    save(fig, "27-wb-coip")


# ------------------------------------------------------- microscopy scaffolding
def _cells(n, seed):
    r = np.random.default_rng(seed)
    pos = []
    for _ in range(n):
        x, y = r.uniform(0.6, 9.4), r.uniform(0.6, 6.4)
        if all((x - a) ** 2 + (y - b) ** 2 > 1.1 for a, b in pos):
            pos.append((x, y))
    return pos, r


def _scalebar(ax):
    ax.add_patch(Rectangle((8.0, 0.25), 1.6, 0.22, facecolor="black"))
    ax.text(8.8, 0.62, "50 um", ha="center", fontsize=8)


def ihc():
    csv = """panel,dab_positive_cells,total_cells
positive_section,22,36
negative_control,2,36"""
    dump("28-ihc", csv)
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.4))
    for ax, (title, npos) in zip(axes, [("positive tissue section", 22),
                                        ("negative control (no primary Ab)", 2)]):
        ax.grid(False)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 7)
        ax.axis("off")
        ax.set_title(title, fontsize=10.5)
        pos, r = _cells(36, seed=5)
        order = r.permutation(len(pos))
        for i, (x, y) in enumerate(pos):
            brown = i in set(order[:npos])
            face = "#8B5A2B" if brown else "#C9B6D9"
            ax.add_patch(Ellipse((x, y), 0.95, 0.78, facecolor=face,
                                 edgecolor="#5D4037", lw=0.8, alpha=0.9))
            ax.add_patch(Ellipse((x, y), 0.34, 0.30, facecolor="#3E2723", alpha=0.75))
        _scalebar(ax)
    fig.suptitle("IHC schematic: DAB brown signal marks in-situ protein presence", y=1.02)
    save(fig, "28-ihc")


def immunofluorescence():
    csv = """panel,signal
DAPI_nuclei,36
anti_target_positive_cells,17
merged_colocalized,17"""
    dump("29-if", csv)
    fig, axes = plt.subplots(1, 3, figsize=(12.2, 4.0))
    pos, r = _cells(36, seed=9)
    green_idx = set(r.permutation(len(pos))[:17])
    panels = [("DAPI (nuclei)", "blue", None), ("anti-target (Alexa 488)", "green", green_idx),
              ("merged", "merge", green_idx)]
    for ax, (title, mode, gidx) in zip(axes, panels):
        ax.grid(False)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 7)
        ax.axis("off")
        ax.set_title(title, fontsize=10)
        for i, (x, y) in enumerate(pos):
            if mode in ("blue", "merge"):
                ax.add_patch(Ellipse((x, y), 0.9, 0.74, facecolor="#2962FF",
                                     edgecolor="none", alpha=0.55 if mode == "merge" else 0.75))
            if mode in ("green", "merge") and i in gidx:
                ax.add_patch(Ellipse((x, y), 1.35, 1.15, facecolor="#00C853",
                                     edgecolor="none", alpha=0.45))
                ax.add_patch(Ellipse((x, y), 0.8, 0.68, facecolor="#00E676",
                                     edgecolor="none", alpha=0.45))
        _scalebar(ax)
    fig.suptitle("Immunofluorescence schematic: channel split + merge (colocalization = cyan)",
                 y=1.04)
    save(fig, "29-if")


def tunel():
    csv = """panel,green_apoptotic_nuclei,total_nuclei
control,3,36
uv_treated,15,36"""
    dump("30-tunel", csv)
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.4))
    for ax, (title, ngreen, seed) in zip(
            axes, [("control", 3, 12), ("UV-treated", 15, 13)]):
        ax.grid(False)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 7)
        ax.axis("off")
        ax.set_title("%s: %d/36 TUNEL+" % (title, ngreen), fontsize=10.5)
        pos, r = _cells(36, seed=seed)
        idx = set(r.permutation(len(pos))[:ngreen])
        for i, (x, y) in enumerate(pos):
            face = "#00C853" if i in idx else "#2962FF"
            ax.add_patch(Ellipse((x, y), 0.85, 0.7, facecolor=face,
                                 edgecolor="none", alpha=0.8))
        _scalebar(ax)
    fig.suptitle("TUNEL schematic: green = DNA fragments (apoptotic nuclei)", y=1.02)
    save(fig, "30-tunel")


# ------------------------------------------------------------- 31 flow: cycle
def flow_cycle():
    chan = np.arange(50, 276, 25)

    def counts(f_g1, f_s, f_g2):
        g1 = f_g1 * np.exp(-((chan - 100) ** 2) / (2 * 13 ** 2))
        g2 = f_g2 * np.exp(-((chan - 200) ** 2) / (2 * 16 ** 2))
        s = f_s * np.exp(-((chan - 150) ** 2) / (2 * 42 ** 2)) * 0.55
        tot = 18000 / (g1 + g2 + s).sum()
        return np.round((g1 + g2 + s) * tot).astype(int)

    ctl = counts(0.62, 0.30, 0.28)
    trt = counts(0.34, 0.30, 0.55)
    rows = ["channel,control_counts,treated_counts"]
    rows += ["%d,%d,%d" % (a, b, cc) for a, b, cc in zip(chan, ctl, trt)]
    dump("31-flow-cycle", "\n".join(rows))

    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    ax.bar(chan - 6, ctl, width=11, color=CAT[0], alpha=0.55, label="control")
    ax.bar(chan + 6, trt, width=11, color=CAT[3], alpha=0.55, label="drug-treated")
    ax.annotate("G0/G1 peak (2N)", (100, ctl.max()), (58, ctl.max() * 1.12), fontsize=9.5,
                arrowprops=dict(arrowstyle="->", lw=1))
    ax.annotate("S phase (synthesis)", (150, 1400), (150, 2600), ha="center", fontsize=9.5,
                arrowprops=dict(arrowstyle="->", lw=1))
    ax.annotate("G2/M peak (4N)", (200, trt.max()), (232, trt.max() * 1.12), fontsize=9.5,
                arrowprops=dict(arrowstyle="->", lw=1))
    ax.set_xticks(chan)
    ax.set_ylim(0, 7800)
    ax.set_xlabel("DNA content (PI-A channel)")
    ax.set_ylabel("cell count")
    ax.set_title("Flow cytometry: cell-cycle histogram")
    ax.legend()
    save(fig, "31-flow-cycle")


# ------------------------------------------------------------- 32 flow: pheno
def flow_pheno():
    blobs = {"double_positive": ((3.4, 3.6), 14), "B_only": ((0.6, 3.9), 6),
             "A_only": ((3.7, 0.7), 4), "double_negative": ((0.5, 0.5), 6)}
    rows = ["marker_A,marker_B,population"]
    pts = []
    for name, ((cx, cy), n) in blobs.items():
        for _ in range(n):
            a, b = cx + rng.normal(0, 0.38), cy + rng.normal(0, 0.38)
            pts.append((a, b, name))
            rows.append("%.2f,%.2f,%s" % (a, b, name))
    dump("32-flow-pheno", "\n".join(rows))

    fig, ax = plt.subplots(figsize=(6.4, 6.0))
    cols = {"double_positive": CAT[3], "B_only": CAT[1], "A_only": CAT[0],
            "double_negative": "0.6"}
    total = len(pts)
    for name, col in cols.items():
        m = np.array([p[2] for p in pts]) == name
        xa = np.array([p[0] for p in pts])[m]
        xb = np.array([p[1] for p in pts])[m]
        ax.scatter(xa, xb, s=42, color=col, edgecolors="white", linewidths=0.6,
                   label="%s (%d%%)" % (name.replace("_", " "), round(100 * m.sum() / total)))
    ax.axvline(1.9, color="0.3", lw=1.2)
    ax.axhline(1.9, color="0.3", lw=1.2)
    ax.set_xlim(-0.6, 5.2)
    ax.set_ylim(-0.6, 5.6)
    ax.set_xlabel("marker A fluorescence (log)")
    ax.set_ylabel("marker B fluorescence (log)")
    ax.set_title("Flow cytometry: 2D dot plot with quadrant gates")
    ax.legend(loc="upper left", fontsize=8.5)
    save(fig, "32-flow-pheno")


# -------------------------------------------------------------- 33 flow: apop
def flow_apop():
    blobs = {"viable": ((0.45, 0.45), 24), "early_apoptotic": ((2.9, 0.45), 5),
             "late_apoptotic": ((3.0, 3.0), 7), "necrotic": ((0.5, 3.1), 2)}
    rows = ["annexin_V,PI,population"]
    pts = []
    for name, ((cx, cy), n) in blobs.items():
        for _ in range(n):
            a, b = cx + rng.normal(0, 0.22), cy + rng.normal(0, 0.22)
            pts.append((a, b, name))
            rows.append("%.2f,%.2f,%s" % (a, b, name))
    dump("33-flow-apop", "\n".join(rows))

    fig, ax = plt.subplots(figsize=(6.6, 6.0))
    cols = {"viable": CAT[2], "early_apoptotic": CAT[1], "late_apoptotic": CAT[3],
            "necrotic": CAT[4]}
    total = len(pts)
    for name, col in cols.items():
        m = np.array([p[2] for p in pts]) == name
        xa = np.array([p[0] for p in pts])[m]
        xb = np.array([p[1] for p in pts])[m]
        ax.scatter(xa, xb, s=42, color=col, edgecolors="white", linewidths=0.6)
        cx, cy = blobs[name][0]
        label = name.replace("_", " ")
        ax.text(cx, cy + 0.75, "%s\n%d%%" % (label, round(100 * m.sum() / total)),
                ha="center", fontsize=9.5, color=col, fontweight="bold")
    ax.axvline(1.6, color="0.3", lw=1.2)
    ax.axhline(1.6, color="0.3", lw=1.2)
    ax.set_xlim(-0.5, 4.2)
    ax.set_ylim(-0.5, 4.4)
    ax.set_xlabel("Annexin V fluorescence (apoptosis)")
    ax.set_ylabel("PI fluorescence (membrane integrity)")
    ax.set_title("Flow cytometry: Annexin V / PI apoptosis assay")
    save(fig, "33-flow-apop")


if __name__ == "__main__":
    qpcr_bar()
    amp_curve()
    melt_curve()
    amplicon_cds()
    wb_coip()
    ihc()
    immunofluorescence()
    tunel()
    flow_cycle()
    flow_pheno()
    flow_apop()
