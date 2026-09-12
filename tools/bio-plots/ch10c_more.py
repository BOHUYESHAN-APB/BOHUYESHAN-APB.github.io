# -*- coding: utf-8 -*-
"""Gallery post 4 (part A): protein, biochemistry, microbiome figures
104-120."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Ellipse

from scipy.optimize import curve_fit

from common import save, dump, CAT, UP, DOWN

rng = np.random.default_rng(2104)


# ------------------------------------------------------------ 104 domains
def domains():
    prots = [
        ("FaBZR1", 345, [("N-terminal activation", 1, 120, CAT[0]),
                         ("NLS", 132, 148, CAT[5]),
                         ("bHLH DNA-binding", 168, 232, CAT[3])]),
        ("FaDWF4", 563, [("P450 domain", 38, 96, CAT[2]),
                         ("substrate-binding", 210, 292, CAT[1]),
                         ("heme-binding", 452, 486, CAT[3])]),
        ("FaCHS", 389, [("chalcone synthase N", 60, 178, CAT[4]),
                        ("thiolase fold", 190, 352, CAT[0])]),
    ]
    rows = ["protein,domain,start,end"]
    for name, _, doms in prots:
        for d, a, b, _ in doms:
            rows.append("%s,%s,%d,%d" % (name, d, a, b))
    dump("104-domains", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(9.4, 4.6))
    for k, (name, L, doms) in enumerate(prots):
        y = len(prots) - 1 - k
        ax.plot([0, L], [y, y], color="0.75", lw=5, solid_capstyle="round")
        for d, a, b, c in doms:
            ax.add_patch(plt.Rectangle((a, y - 0.19), b - a, 0.38,
                                       facecolor=c, edgecolor="0.25", alpha=0.9))
            ax.text((a + b) / 2, y, d, ha="center", va="center", fontsize=7.6,
                    color="white" if c != CAT[1] else "#222")
        ax.text(-12, y + 0.28, "NLS", ha="center", fontsize=6.5,
                color=CAT[5]) if name == "FaBZR1" else None
        ax.text(-12, y, name, ha="right", va="center", fontsize=9.5,
                fontweight="bold")
        ax.text(L + 12, y, "%d aa" % L, va="center", fontsize=8.5, color="0.45")
    ax.set_xlim(-105, 660)
    ax.set_ylim(-0.7, 2.7)
    ax.set_xlabel("amino acid position")
    ax.spines["left"].set_visible(False)
    ax.set_title("Protein domain architecture (simulated)")
    save(fig, "104-domains")


# --------------------------------------------------------------- 105 pLDDT
def plddt():
    pos = np.arange(1, 241)
    v = np.where((pos < 45) | ((pos > 100) & (pos < 195)) | (pos > 215),
                 rng.normal(92, 2.0, 240), rng.normal(72, 3.5, 240))
    v[(pos > 62) & (pos < 88)] = rng.normal(52, 4.0, ((pos > 62) & (pos < 88)).sum())
    v = np.clip(v, 28, 98)
    rows = ["pos,plddt"]
    rows += ["%d,%.1f" % v for v in zip(pos[::3], v[::3])]
    dump("105-plddt", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(9.4, 4.4))
    cols = np.where(v > 90, "#0053D6",
                    np.where(v > 70, "#65CBF3",
                             np.where(v > 60, "#FFDB13", "#FF7D45")))
    for i in range(len(pos) - 1):
        ax.plot(pos[i:i + 2], v[i:i + 2], color=cols[i], lw=1.8)
    ax.axhline(90, color="0.6", ls=":", lw=0.9)
    ax.axhline(70, color="0.6", ls=":", lw=0.9)
    ax.text(239, 91.2, "pLDDT 90", fontsize=8, color="0.4", ha="right")
    ax.text(239, 71.2, "pLDDT 70", fontsize=8, color="0.4", ha="right")
    ax.annotate("disordered loop", (75, 50), (100, 38), fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=1))
    ax.set_ylim(25, 100)
    ax.set_xlabel("residue")
    ax.set_ylabel("pLDDT")
    ax.set_title("AlphaFold per-residue confidence, FaDWF4 model (simulated)")
    save(fig, "105-plddt")


# ------------------------------------------------------------------ 106 RMSF
def rmsf():
    res = np.arange(2, 201, 2)
    wt = 0.75 + 0.10 * np.sin(res / 14) + rng.normal(0, 0.05, len(res))
    mut = wt + 0.22 + rng.normal(0, 0.05, len(res))
    loop = (res >= 92) & (res <= 106)
    wt[loop] += 1.15
    mut[loop] += 1.95
    rows = ["residue,rmsf_wt,rmsf_mut"]
    rows += ["%d,%.2f,%.2f" % v for v in zip(res, wt, mut)]
    dump("106-rmsf", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.fill_between(res, wt - 0.14, wt + 0.14, color=CAT[0], alpha=0.18)
    ax.plot(res, wt, color=CAT[0], lw=1.7, label="wild type")
    ax.plot(res, mut, color=CAT[3], lw=1.7, label="dwf4 mutant")
    ax.annotate("substrate channel loop\nmore flexible in mutant",
                (99, 2.9), (126, 2.65), fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=1))
    ax.set_xlabel("residue")
    ax.set_ylabel("RMSF (A)")
    ax.legend(loc="upper left")
    ax.set_title("Per-residue flexibility over 50 ns MD (simulated)")
    save(fig, "106-rmsf")


# -------------------------------------------------------------------- 107 FEL
def fel():
    x = np.linspace(-3.4, 3.4, 130)
    y = np.linspace(-2.4, 2.4, 90)
    X, Y = np.meshgrid(x, y)
    w1 = 2.6 * ((X - 1.25) ** 2 / 1.5 + (Y - 0.5) ** 2 / 0.85)
    w2 = 2.6 * ((X + 1.45) ** 2 / 2.3 + (Y + 0.5) ** 2 / 1.5) + 2.1
    DG = np.minimum(w1, w2)
    rows = ["pc1,pc2,dG_kcal"]
    for xv in np.linspace(-3, 3, 7):
        for yv in np.linspace(-2, 2, 5):
            i = np.argmin(abs(x - xv))
            j = np.argmin(abs(y - yv))
            rows.append("%.1f,%.1f,%.2f" % (x[i], y[j], DG[j, i]))
    dump("107-fel-grid", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.8, 5.6))
    cf = ax.contourf(X, Y, DG, levels=14, cmap="jet_r")
    cs = ax.contour(X, Y, DG, levels=6, colors="white", linewidths=0.6)
    ax.clabel(cs, fmt="%.1f", fontsize=7)
    ax.scatter([1.25, -1.45], [0.5, -0.5], marker="*", s=190, c="white",
               edgecolors="0.2", zorder=5)
    ax.text(1.25, 0.14, "basin A (native)", ha="center", fontsize=9)
    ax.text(-1.45, -0.94, "basin B", ha="center", fontsize=9)
    ax.annotate("", xy=(0.75, 0.28), xytext=(-0.95, -0.32),
                arrowprops=dict(arrowstyle="->", color="white", lw=1.6))
    ax.set_xlabel("PC1 (nm)")
    ax.set_ylabel("PC2 (nm)")
    ax.set_title("Free energy landscape, 100 ns MD (simulated)")
    fig.colorbar(cf, ax=ax, shrink=0.85, label="dG (kcal/mol)")
    save(fig, "107-fel")


# -------------------------------------------------------------------- 108 EMSA
def emsa():
    fig, ax = plt.subplots(figsize=(7.6, 5.6))
    ax.add_patch(plt.Rectangle((0.5, 0.5), 8.6, 8.6, facecolor="#0E0E0E"))
    lanes = {"probe": 1.6, "+protein": 3.3, "+50x cold": 5.0,
             "+mut probe": 6.7, "+antibody": 8.3}

    def band(x0, y0, w, h, it=1.0):
        ax.add_patch(plt.Rectangle((x0 - w / 2, y0 - h / 2), w, h,
                                   facecolor="white", alpha=0.45 + 0.5 * it))

    for name, x0 in lanes.items():
        ax.text(x0, 8.75, name, ha="center", fontsize=8.2, color="white",
                rotation=18)
    band(1.6, 3.4, 1.5, 0.24, 0.9)
    band(3.3, 3.4, 1.5, 0.20, 0.30)
    band(3.3, 5.6, 1.6, 0.26, 0.85)
    band(5.0, 3.4, 1.5, 0.24, 0.85)
    band(5.0, 5.6, 1.6, 0.20, 0.22)
    band(6.7, 3.4, 1.5, 0.20, 0.30)
    band(6.7, 5.6, 1.6, 0.26, 0.82)
    band(8.3, 3.4, 1.5, 0.20, 0.30)
    band(8.3, 5.6, 1.6, 0.24, 0.80)
    band(8.3, 7.0, 1.8, 0.26, 0.88)
    ax.text(9.35, 3.4, "free probe", fontsize=8, color="white", va="center")
    ax.text(9.35, 5.6, "shifted", fontsize=8, color="white", va="center")
    ax.text(9.35, 7.0, "supershifted", fontsize=8, color="white", va="center")
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 9.4)
    ax.axis("off")
    ax.set_title("EMSA: BZR1 binds the DWF4 promoter motif (schematic)")
    save(fig, "108-emsa")


# ------------------------------------------------------- 109 subcellular
def subcell():
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 5.4))

    def cell(ax, mode):
        ax.add_patch(Ellipse((5, 5), 8.6, 6.6, facecolor="#F1F8E9",
                             edgecolor="#33691E", lw=2.2))
        ax.add_patch(Ellipse((5, 5), 2.5, 2.1, facecolor="none",
                             edgecolor="#558B2F", lw=1.6, ls="--"))
        if mode == "control":
            ax.add_patch(Ellipse((5, 5), 8.2, 6.2, facecolor="#A5D6A7",
                                 alpha=0.55, lw=0))
            ax.add_patch(Ellipse((5, 5), 2.3, 1.9, facecolor="#81C784",
                                 alpha=0.55, lw=0))
            ax.text(5, 8.62, "35S::GFP (control)", ha="center", fontsize=10)
            ax.text(5, 1.15, "diffuse signal", ha="center", fontsize=9,
                    color="#33691E")
        else:
            th = np.linspace(0, 2 * np.pi, 200)
            ax.plot(5 + 4.28 * np.cos(th), 5 + 3.28 * np.sin(th),
                    color="#2E7D32", lw=4.5, solid_capstyle="round")
            ax.add_patch(Ellipse((5, 5), 2.4, 2.0, facecolor="#66BB6A", lw=0))
            ax.text(5, 8.62, "DWF4p::GFP", ha="center", fontsize=10)
            ax.text(5, 1.15, "plasma membrane + nucleus", ha="center",
                    fontsize=9, color="#33691E")
        ax.plot([7.6, 9.3], [0.6, 0.6], color="0.2", lw=2)
        ax.text(8.45, 0.15, "20 um", ha="center", fontsize=8)
        ax.set_xlim(0, 11.8)
        ax.set_ylim(-0.4, 9.4)
        ax.axis("off")
    cell(axes[0], "control")
    cell(axes[1], "target")
    fig.suptitle("Subcellular localization of DWF4 promoter:GFP (schematic)",
                 y=0.98)
    save(fig, "109-subcell")


# -------------------------------------------------------- 110 Lineweaver-Burk
def lineweaver():
    s = np.array([0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0])
    v_no = 62 * s / (0.8 + s) + rng.normal(0, 0.8, 8)
    v_comp = 62 * s / (2.4 + s) + rng.normal(0, 0.8, 8)
    v_unc = 27 * s / (0.36 + s) + rng.normal(0, 0.5, 8)
    rows = ["substrate_mM,v_no_inhibitor,v_competitive,v_uncompetitive"]
    for i in range(8):
        rows.append("%.1f,%.1f,%.1f,%.1f" % (s[i], v_no[i], v_comp[i],
                                             v_unc[i]))
    dump("110-michaelis-inhib", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.2, 5.6))
    xs = np.linspace(0, 6, 40)
    for v, col, lab in [(v_no, CAT[0], "none"),
                        (v_comp, CAT[3], "competitive"),
                        (v_unc, CAT[2], "uncompetitive")]:
        ax.scatter(1 / s, 1 / v, s=34, color=col, edgecolors="white", zorder=3)
        A = np.vstack([1 / s, np.ones(8)]).T
        k, b = np.linalg.lstsq(A, 1 / v, rcond=None)[0]
        ax.plot(xs, k * xs + b, color=col, lw=1.8)
        popt, _ = curve_fit(lambda x, vm, km: vm * x / (km + x), s, v,
                            p0=[60.0, 1.0])
        ax.scatter([], [], s=0, label="%s: Vmax=%.0f, Km=%.2f mM"
                   % (lab, popt[0], popt[1]))
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 0.055)
    ax.set_xlabel("1 / [S] (1/mM)")
    ax.set_ylabel("1 / v")
    ax.legend(loc="upper left", fontsize=9)
    ax.set_title("Lineweaver-Burk plot with inhibitors (simulated)")
    save(fig, "110-lineweaver")


# --------------------------------------------------------------------- 111 DSF
def dsf():
    T = np.arange(25, 96, 5)
    apo = 3000 + 42000 / (1 + np.exp(-(T - 52.4) / 2.8)) + rng.normal(0, 500, 15)
    lig = 3000 + 42000 / (1 + np.exp(-(T - 58.1) / 2.8)) + rng.normal(0, 500, 15)
    rows = ["temp_c,rfu_apo,rfu_ligand"]
    rows += ["%d,%.0f,%.0f" % v for v in zip(T, apo, lig)]
    dump("111-dsf", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.8, 4.9))
    ax.plot(T, apo / 1000, "-o", ms=4, color=CAT[0], label="apo FaDWF4")
    ax.plot(T, lig / 1000, "-o", ms=4, color=CAT[3], label="+ brassinolide 10 uM")
    ax.axvline(52.4, color=CAT[0], ls="--", lw=1)
    ax.axvline(58.1, color=CAT[3], ls="--", lw=1)
    ax.annotate("", xy=(58.1, 27), xytext=(52.4, 27),
                arrowprops=dict(arrowstyle="<->", color="0.3"))
    ax.text(55.2, 27.6, "dTm = +5.7 C", ha="center", fontsize=9)
    ax.set_xlabel("temperature (C)")
    ax.set_ylabel("SYPRO fluorescence (x1e3)")
    ax.legend(loc="upper left", fontsize=9)
    ax.set_title("DSF thermal shift assay (simulated)")
    save(fig, "111-dsf")


# ------------------------------------------------------------------- 112 ELISA
def elisa():
    std = np.array([0, 0.078, 0.156, 0.3125, 0.625, 1.25, 2.5, 5.0])
    od = np.array([0.062, 0.118, 0.196, 0.335, 0.552, 0.851, 1.212, 1.549])
    od = od + rng.normal(0, 0.012, 8)

    def fourpl(x, b, t, ic, sl):
        return b + (t - b) / (1 + (x / ic) ** (-sl))

    p, _ = curve_fit(fourpl, std[1:], od[1:], p0=[0.05, 1.7, 0.8, 1.1])
    xs = np.logspace(np.log10(0.03), np.log10(9), 120)
    unk_od = np.array([0.42, 0.86, 1.24])
    unk_conc = p[2] * ((p[1] - p[0]) / (unk_od - p[0]) - 1) ** (1 / -p[3])
    rows = ["standard_ng,od"]
    rows += ["%.3f,%.3f" % v for v in zip(std, od)]
    dump("112-elisa-std", "\n".join(rows))
    rows = ["unknown,od,backcalc_ng_ml"]
    for i, (o, c) in enumerate(zip(unk_od, unk_conc)):
        rows.append("S%d,%.2f,%.2f" % (i + 1, o, c))
    dump("112-elisa-unknowns", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.4, 5.2))
    ax.plot(xs, fourpl(xs, *p), color=CAT[0], lw=1.8, label="4PL fit")
    ax.scatter(std, od, s=42, color=CAT[0], zorder=3, label="standards")
    for i, (o, c) in enumerate(zip(unk_od, unk_conc)):
        ax.scatter([o * 6.4], [o], s=48, color=CAT[3], zorder=3)
        ax.plot([0.03, o * 6.4], [o, o], color=CAT[3], ls=":", lw=1)
        ax.plot([o * 6.4] * 2, [0.05, o], color=CAT[3], ls=":", lw=1)
        ax.text(o * 6.4 + 0.25, o, "S%d: %.2f ng/mL" % (i + 1, c),
                fontsize=8.5, color=CAT[3], va="center")
    ax.set_xscale("log")
    ax.set_xlabel("GA3 concentration (ng/mL)")
    ax.set_ylabel("OD450")
    ax.set_ylim(0, 1.75)
    ax.legend(loc="upper left", fontsize=9)
    ax.set_title("ELISA standard curve and sample back-calculation (simulated)")
    save(fig, "112-elisa")


# ------------------------------------------------------------- 113 fluorescence
def fluor_shift():
    wl = np.arange(305, 451, 5)
    peak = {0: 342, 2: 346, 8: 351, 20: 356}
    inten = {0: 1.0, 2: 0.82, 8: 0.62, 20: 0.45}
    cols = {0: CAT[0], 2: CAT[2], 8: CAT[1], 20: CAT[3]}
    data = {}
    rows_h = ["wavelength_nm,apo,add2,add8,add20"]
    for c in [0, 2, 8, 20]:
        data[c] = inten[c] * np.exp(-0.5 * ((wl - peak[c]) / 17) ** 2) \
            + rng.normal(0, 0.008, len(wl))
    for i in range(len(wl)):
        rows_h.append("%d,%.3f,%.3f,%.3f,%.3f" %
                      (wl[i], data[0][i], data[2][i], data[8][i], data[20][i]))
    dump("113-fluorescence", "\n".join(rows_h))
    fig, ax = plt.subplots(figsize=(7.8, 4.9))
    for c in [0, 2, 8, 20]:
        ax.plot(wl, data[c], color=cols[c], lw=1.8,
                label="%s" % ("apo" if c == 0 else "+%d uM ligand" % c))
        ax.axvline(peak[c], color=cols[c], ls=":", lw=0.9)
    ax.annotate("emission maximum\nred-shifts 342 to 356 nm", (356, 0.40),
                (388, 0.72), fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=1))
    ax.set_xlabel("emission wavelength (nm), ex = 280 nm")
    ax.set_ylabel("normalized fluorescence")
    ax.legend(fontsize=8.5)
    ax.set_title("Intrinsic fluorescence quenching titration (simulated)")
    save(fig, "113-fluor-shift")


# ----------------------------------------------------------- 114 luciferase
def luciferase():
    cons = ["empty vector", "promoter-WT", "promoter-WT\n+ BZR1",
            "promoter-mut", "promoter-mut\n+ BZR1"]
    ratio = np.array([1.0, 2.9, 7.4, 1.1, 1.3])
    sd = np.array([0.12, 0.31, 0.62, 0.14, 0.18])
    rows = ["construct,ratio,sd"]
    for c, r, s_ in zip(cons, ratio, sd):
        rows.append("%s,%.2f,%.2f" % (c.replace("\n", " "), r, s_))
    dump("114-luciferase", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    cols = ["0.75", CAT[0], CAT[3], CAT[2], CAT[1]]
    ax.bar(cons, ratio, color=cols, alpha=0.9, width=0.6,
           yerr=sd, capsize=4)
    for i, (r, s_) in enumerate(zip(ratio, sd)):
        ax.text(i, r + s_ + 0.18, "%.1f" % r, ha="center", fontsize=9)
    ax.annotate("***", (2, 8.45), ha="center", fontsize=11)
    ax.plot([1.75, 2.25], [8.15, 8.15], color="0.2", lw=1.2)
    ax.set_ylabel("LUC / REN ratio (relative)")
    ax.set_ylim(0, 9)
    ax.set_title("Dual-luciferase promoter activation assay (simulated)")
    save(fig, "114-luciferase")


# ------------------------------------------------------------ 115 rarefaction
def rarefaction():
    r = np.arange(0, 40001, 2000)
    curves = {"site A": 86, "site B": 54, "site C": 31}
    rows = ["reads," + ",".join(curves)]
    vals = {k: [] for k in curves}
    for x in r:
        row = [str(x)]
        for k, sm in curves.items():
            v = sm * (1 - np.exp(-x / 9000)) + rng.normal(0, 0.7)
            row.append("%.1f" % max(v, 0))
            vals[k].append(v)
        rows.append(",".join(row))
    dump("115-rarefaction", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.8, 4.9))
    for (k, col) in zip(curves, [CAT[0], CAT[1], CAT[2]]):
        ax.plot(r / 1000, vals[k], "-o", ms=3.5, color=col, lw=1.7, label=k)
    ax.annotate("site A not yet saturated:\nsequence deeper", (38, 84),
                (26, 66), fontsize=9, arrowprops=dict(arrowstyle="->", lw=1))
    ax.set_xlabel("reads sampled (x1e3)")
    ax.set_ylabel("observed ASVs")
    ax.legend(loc="lower right")
    ax.set_title("Rarefaction curves, rhizosphere soils (simulated)")
    save(fig, "115-rarefaction")


# --------------------------------------------------------- 116 rank abundance
def rank_abund():
    ranks = np.arange(1, 26)
    a = 62 * ranks ** -0.55 * rng.uniform(0.9, 1.1, 25)
    b = 40 * ranks ** -0.85 * rng.uniform(0.9, 1.1, 25)
    c = 25 * ranks ** -1.2 * rng.uniform(0.9, 1.1, 25)
    rows = ["rank,treatment_A,treatment_B,treatment_C"]
    for i in range(25):
        rows.append("%d,%.2f,%.2f,%.2f" % (ranks[i], a[i], b[i], c[i]))
    dump("116-rank-abundance", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.6, 4.9))
    for v, col, lab in [(a, CAT[0], "control"), (b, CAT[1], "low N"),
                        (c, CAT[3], "high N")]:
        ax.plot(ranks, v, "-o", ms=3.5, color=col, lw=1.6, label=lab)
    ax.set_yscale("log")
    ax.set_xlabel("species rank (most to least abundant)")
    ax.set_ylabel("relative abundance (%)")
    ax.legend()
    ax.set_title("Rank-abundance (Whittaker) curves (simulated)")
    save(fig, "116-rank-abund")


# ------------------------------------------------------------------ 117 ternary
def ternary():
    anchors = {"bulk soil": [0.72, 0.18, 0.10],
               "rhizosphere": [0.28, 0.58, 0.14],
               "root endophyte": [0.12, 0.20, 0.68]}
    rows = ["sample,frac_bulk,frac_rhizo,frac_endo"]
    pts = []
    pfx = {"bulk soil": "B", "rhizosphere": "R", "root endophyte": "E"}
    for gi, (g, mu) in enumerate(anchors.items()):
        for i in range(6):
            v = rng.dirichlet(np.array(mu) * 22)
            name = "%s%d" % (pfx[g], i + 1)
            pts.append((name, g, *v))
            rows.append("%s,%.2f,%.2f,%.2f" % (name, *v))
    dump("117-ternary", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.2, 6.6))
    ax.plot([0, 1, 0.5, 0], [0, 0, np.sqrt(3) / 2, 0], color="0.25", lw=1.4)
    def tri(a, b, c):
        return b + c / 2, c * np.sqrt(3) / 2
    for f in [0.2, 0.4, 0.6, 0.8]:
        p1 = tri(1 - f, f, 0)
        p2 = tri(0, f, 1 - f)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="0.85", lw=0.7)
        p1 = tri(f, 0, 1 - f)
        p2 = tri(0, f, 1 - f)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="0.85", lw=0.7)
    gcol = {"bulk soil": CAT[3], "rhizosphere": CAT[0], "root endophyte": CAT[2]}
    for name, g, a, b, c in pts:
        x, y = tri(a, b, c)
        ax.scatter([x], [y], s=44, color=gcol[g], edgecolors="white", zorder=3)
    ax.text(0.5, 0.90, "root endophyte", ha="center", fontsize=10)
    ax.text(-0.02, -0.07, "bulk soil", ha="right", fontsize=10)
    ax.text(1.02, -0.07, "rhizosphere", ha="left", fontsize=10)
    ax.set_xlim(-0.15, 1.15)
    ax.set_ylim(-0.12, 1.0)
    ax.axis("off")
    ax.set_title("Ternary plot of community composition (simulated)")
    save(fig, "117-ternary")


# --------------------------------------------------------------------- 118 RDA
def rda():
    groups = ["bulk", "rhizosphere", "endophyte"]
    mu = [(-1.7, 0.9), (1.3, 1.1), (0.6, -1.6)]
    data = []
    for g, (mx, my) in zip(groups, mu):
        for i in range(6):
            data.append(("%s%d" % (g[0].upper(), i + 1), g,
                         rng.normal(mx, 0.42), rng.normal(my, 0.38)))
    envs = [("total N", 1.85, 0.25), ("pH", -1.25, 1.05),
            ("moisture", 0.35, -1.75), ("SOM", 1.15, -0.70)]
    sps = [("Sp1", 1.55, 0.30), ("Sp2", -1.05, 0.95),
           ("Sp3", 0.40, -1.45), ("Sp4", 0.95, -0.45)]
    rows = ["site,group,rda1,rda2"]
    rows += ["%s,%s,%.2f,%.2f" % v for v in data]
    dump("118-rda-sites", "\n".join(rows))
    rows = ["variable,rda1,rda2"]
    rows += ["%s,%.2f,%.2f" % v for v in envs]
    dump("118-rda-arrows", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.6, 6.4))
    gcol = dict(zip(groups, [CAT[3], CAT[0], CAT[2]]))
    for name, g, x, y in data:
        ax.scatter([x], [y], s=48, color=gcol[g], edgecolors="white", label=g
                   if name.endswith("1") else None, zorder=3)
    for name, x, y in envs:
        ax.annotate("", xy=(x, y), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color=CAT[3], lw=1.6))
        ax.text(x * 1.18, y * 1.18, name, fontsize=9, color=CAT[3],
                ha="center")
    for name, x, y in sps:
        ax.annotate("", xy=(x * 0.62, y * 0.62), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color=CAT[0], lw=1.1,
                                    alpha=0.8))
        ax.text(x * 0.62 * 1.2, y * 0.62 * 1.2, name, fontsize=7.5,
                color=CAT[0])
    ax.axhline(0, color="0.85", lw=0.8)
    ax.axvline(0, color="0.85", lw=0.8)
    ax.legend(loc="upper left", fontsize=9)
    ax.set_xlabel("RDA1 (46%)")
    ax.set_ylabel("RDA2 (27%)")
    ax.set_title("RDA of rhizosphere communities (simulated)")
    save(fig, "118-rda")


# -------------------------------------------------------------- 119 LEfSe tree
def lefse():
    phyla = [("Actinobacteriota", CAT[3], 1), ("Proteobacteria", CAT[0], 2),
             ("Acidobacteriota", "0.75", 3), ("Bacteroidota", "0.75", 4)]
    classes = [("Actinomycetes", 0, CAT[3]), ("Coriobacteriia", 1, CAT[3]),
               ("Alphaproteobacteria", 2, CAT[0]), ("Gammaproteobacteria", 3, CAT[0]),
               ("Acidobacteriia", 4, "0.75"), ("Chlorobia", 5, "0.75"),
               ("Bacteroidia", 6, "0.75"), ("Flavobacteriia", 7, "0.75")]
    genus = [("Fa01", 0, CAT[3]), ("Fa02", 1, CAT[3]), ("Fa03", 2, CAT[0]),
             ("Fa04", 2, CAT[0]), ("Fa05", 3, CAT[0]), ("Fa06", 5, "0.75"),
             ("Fa07", 6, "0.75"), ("Fa08", 7, "0.75"), ("Fa09", 4, "0.75"),
             ("Fa10", 3, CAT[0]), ("Fa11", 1, CAT[3]), ("Fa12", 0, CAT[3])]
    rows = ["taxon,rank,parent_index,group"]
    rows += ["%s,phylum,," % p[0] for p in phyla]
    rows += ["%s,class,%d,%s" % (c[0], c[1], "dwarf" if c[2] != "0.75" else "ns")
             for c in classes]
    rows += ["%s,genus,%d,%s" % (g[0], g[1], "dwarf" if g[2] != "0.75" else "ns")
             for g in genus]
    dump("119-lefse", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(8.6, 7.6))
    n1, n2 = len(phyla), len(classes)
    for i, (name, col, _) in enumerate(phyla):
        a0 = 360 * i / n1 + 2
        a1 = 360 * (i + 1) / n1 - 2
        ax.add_patch(Wedge((0, 0), 1.0, a0, a1, width=0.22, facecolor=col,
                           edgecolor="white"))
        am = np.deg2rad((a0 + a1) / 2)
        ax.text(1.18 * np.cos(am), 1.18 * np.sin(am), name, fontsize=8,
                ha="center", va="center", rotation=0, color=col)
    for ci, (name, pi, col) in enumerate(classes):
        w = 360 / n1 / 2
        a0 = 360 * pi / n1 + (ci % 2) * w
        a1 = a0 + w
        ax.add_patch(Wedge((0, 0), 0.74, a0 + 1.2, a1 - 1.2, width=0.18,
                           facecolor=col, edgecolor="white"))
    for i, (name, ci, col) in enumerate(genus):
        k, pi = ci % 2, ci // 2
        frac = 360 * pi / n1 + (k + 0.5) * (360 / n1 / 2)
        am = np.deg2rad(frac)
        r = 0.52
        ax.scatter([r * np.cos(am)], [r * np.sin(am)], s=58, color=col,
                   edgecolors="white", zorder=3)
        ax.text(0.40 * np.cos(am), 0.40 * np.sin(am), name, fontsize=6,
                ha="center", va="center", color="0.35")
    ax.scatter([0], [0], s=60, color="0.3")
    ax.text(0, -1.45, "red: enriched in dwarf group, blue: wild type,\ngray: not significant",
            ha="center", fontsize=9, color="0.4")
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.65, 1.55)
    ax.axis("off")
    ax.set_title("LEfSe-style cladogram of root microbiota (simulated)")
    save(fig, "119-lefse")


# ---------------------------------------------------------------- 120 time-kill
def time_kill():
    t = np.array([0, 2, 4, 6, 8, 12, 18, 24])
    ctrl = 6.4 + rng.normal(0, 0.06, 8)
    abx1 = np.array([6.4, 5.6, 4.9, 4.6, 4.9, 5.5, 6.0, 6.15]) + rng.normal(0, 0.06, 8)
    abx4 = np.array([6.4, 4.6, 3.2, 2.6, 2.3, 2.1, 2.05, 2.0]) + rng.normal(0, 0.06, 8)
    rows = ["time_h,control,abx_1x,abx_4x"]
    for i in range(8):
        rows.append("%d,%.2f,%.2f,%.2f" % (t[i], ctrl[i], abx1[i], abx4[i]))
    dump("120-time-kill", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.8, 4.9))
    ax.plot(t, ctrl, "-o", ms=4.5, color="0.5", label="no antibiotic")
    ax.plot(t, abx1, "-o", ms=4.5, color=CAT[0], label="1 x MIC")
    ax.plot(t, abx4, "-o", ms=4.5, color=CAT[3], label="4 x MIC")
    ax.axhline(2.0, color="0.4", ls="--", lw=1)
    ax.text(23.5, 2.15, "detection limit", fontsize=8.5, color="0.4",
            ha="right")
    ax.set_xlabel("time (h)")
    ax.set_ylabel("log10 (CFU/mL)")
    ax.set_ylim(1.4, 7.1)
    ax.legend(loc="lower left", fontsize=9)
    ax.set_title("Time-kill curves of Pseudomonas isolate (simulated)")
    save(fig, "120-time-kill")


if __name__ == "__main__":
    domains()
    plddt()
    rmsf()
    fel()
    emsa()
    subcell()
    lineweaver()
    dsf()
    elisa()
    fluor_shift()
    luciferase()
    rarefaction()
    rank_abund()
    ternary()
    rda()
    lefse()
    time_kill()
