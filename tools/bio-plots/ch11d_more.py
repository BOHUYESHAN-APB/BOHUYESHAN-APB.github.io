# -*- coding: utf-8 -*-
"""Gallery post 5 part D: 10 add-on figures (164-173).

164 Ramachandran plot (real, 6A15 backbone torsions),
165 per-residue B-factor (real, 6A15),
166 per-residue contact number (real, 6A15),
167 MD RMSD/Rg traces (simulated),
168 hydrogen-bond occupancy heatmap (simulated),
169 2D ligand-interaction diagram (simulated drawing, real pocket list),
170 co-evolution contacts vs real contact map (simulated scores,
    real contacts from 6A15),
171 qPCR melt-curve peaks (simulated),
172 RT-PCR cycle-linearity check (simulated),
173 Western blot with densitometry (simulated).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle

from common import save, dump, csv_cols, num

REL = __file__.replace("ch11d_more.py", "..", 1).replace(
    "ch11d_more.py", "..", 1)
REL = REL + "/source/lib/pdb/" if False else None
import os
PDBDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "..", "source", "lib", "pdb") + os.sep


def parse(fn):
    atoms = []
    for ln in open(PDBDIR + fn, encoding="ascii", errors="ignore"):
        if ln[:6] in ("ATOM  ", "HETATM"):
            atoms.append(dict(
                het=ln[:6].startswith("HET"),
                name=ln[12:16].strip(), resn=ln[17:20].strip(),
                chain=ln[21], resi=int(ln[22:26]),
                xyz=(float(ln[30:38]), float(ln[38:46]), float(ln[46:54])),
                b=float(ln[60:66]),
                elem=ln[76:78].strip() or ln[12:16].strip()[0]))
    return atoms


# ------------------------------------------------- 164 Ramachandran
def dihedral(p0, p1, p2, p3):
    b0 = np.array(p0) - np.array(p1)
    b1 = np.array(p2) - np.array(p1)
    b2 = np.array(p3) - np.array(p2)
    b1n = b1 / np.linalg.norm(b1)
    v = b0 - np.dot(b0, b1n) * b1n
    w = b2 - np.dot(b2, b1n) * b1n
    x = np.dot(v, w)
    y = np.dot(np.cross(b1n, v), w)
    return np.degrees(np.arctan2(y, x))


def ramachandran():
    atoms = [a for a in parse("6a15.pdb")
             if a["chain"] == "A" and not a["het"]
             and a["name"] in ("N", "CA", "C", "O")]
    byres = {}
    for a in atoms:
        byres.setdefault(a["resi"], []).append(a)
    ris = sorted(byres)
    phi, psi, resn = [], [], []
    for i, r in enumerate(ris[:-1]):
        d = {a["name"]: np.array(a["xyz"]) for a in byres[r]}
        dn = {a["name"]: np.array(a["xyz"]) for a in byres[ris[i + 1]]}
        if all(k in d for k in ("N", "CA", "C")) and "N" in dn and i > 0 \
                and "C" in {a["name"] for a in byres[ris[i - 1]]}:
            dc = {a["name"]: np.array(a["xyz"])
                  for a in byres[ris[i - 1]]}
            phi.append(dihedral(dc["C"], d["N"], d["CA"], d["C"]))
            psi.append(dihedral(d["N"], d["CA"], d["C"], dn["N"]))
            resn.append([a["resn"] for a in byres[r]][0])
    phi, psi = np.array(phi), np.array(psi)
    gly = np.array([r == "GLY" for r in resn])
    pro = np.array([r == "PRO" for r in resn])
    gen = ~(gly | pro)
    regions = [("alphaR", -63, -45), ("beta", -120, 130), ("alphaL", 57, 42)]
    fav_r, allow_r = 30, 45
    # 近似归类：残基按最近区域计数（教学示意，非 Richardson 标准轮廓判定）
    counts = {name: 0 for name, _, _ in regions}
    other = 0
    for p, s in zip(phi, psi):
        ds = [np.sqrt(((p - cx + 180) % 360 - 180) ** 2 + (s - cy) ** 2)
              for _, cx, cy in regions]
        k = int(np.argmin(ds))
        if ds[k] <= allow_r:
            counts[regions[k][0]] += 1
        else:
            other += 1
    fig, ax = plt.subplots(figsize=(6.8, 6.4))
    for _, cx, cy in regions:
        ax.add_patch(Ellipse((cx, cy), 2 * allow_r, 2 * allow_r,
                             fc="#dbe9f6", ec="none", zorder=0))
        ax.add_patch(Ellipse((cx, cy), 2 * fav_r, 2 * fav_r,
                             fc="#9dc3e6", ec="none", zorder=1, alpha=0.8))
    ax.scatter(phi[gen & ~gly & ~pro], psi[gen], s=12, c="#2b4a6f",
               zorder=3, label="general (%d)" % gen.sum())
    ax.scatter(phi[gly], psi[gly], s=12, c="#DD8452", zorder=3,
               label="GLY (%d)" % gly.sum())
    ax.scatter(phi[pro], psi[pro], s=12, c="#55A868", zorder=3,
               label="PRO (%d)" % pro.sum())
    ax.annotate("alphaR", (-63, 8), ha="center", fontsize=9, color="#31597e")
    ax.annotate("beta", (-120, 168), ha="center", fontsize=9,
                color="#31597e")
    ax.annotate("alphaL", (57, 5), ha="center", fontsize=9, color="#31597e")
    ax.set_xlim(-180, 180)
    ax.set_ylim(-180, 180)
    ax.set_xticks(range(-180, 181, 90))
    ax.set_yticks(range(-180, 181, 90))
    ax.set_xlabel("phi (deg)")
    ax.set_ylabel("psi (deg)")
    ax.legend(loc="lower left", fontsize=8.5)
    ax.set_title("Ramachandran plot of CYP90B1 (PDB 6A15, real data)\n"
                 "%d residues: alphaR %d, beta %d, alphaL %d, "
                 "other %d" % (len(phi), counts["alphaR"], counts["beta"],
                               counts["alphaL"], other))
    save(fig, "164-ramachandran", mark="Real structure data: PDB 6A15")
    dump("164-ramachandran",
         "residues_plotted,%d\nalphaR,%d\nbeta,%d\nalphaL,%d\nother,%d"
         % (len(phi), counts["alphaR"], counts["beta"], counts["alphaL"],
            other))


# --------------------------------------------------- 165 B-factor
def bfactor():
    atoms = [a for a in parse("6a15.pdb")
             if a["chain"] == "A" and not a["het"]]
    per = {}
    for a in atoms:
        per.setdefault(a["resi"], []).append(a["b"])
    ris = sorted(per)
    b = np.array([np.mean(per[r]) for r in ris])
    mu = b.mean()
    hot = ris[int(np.argmax(np.convolve(b, np.ones(9) / 9, "same")))]
    fig, ax = plt.subplots(figsize=(9.6, 4.2))
    ax.plot(ris, b, color="#4C72B0", lw=0.9)
    k = np.convolve(b, np.ones(9) / 9, "same")
    ax.plot(ris, k, color="#DD8452", lw=2.0, label="9-residue running mean")
    ax.axhline(mu, ls="--", color="0.4", lw=1,
               label="mean B = %.1f A^2" % mu)
    ax.set_xlabel("residue")
    ax.set_ylabel("B-factor (A^2)")
    ax.legend(fontsize=8.5)
    ax.set_title("Per-residue B-factor of CYP90B1 (PDB 6A15, real data)\n"
                 "crystallographic mobility; running-mean peak at "
                 "residue %d" % hot)
    save(fig, "165-bfactor", mark="Real structure data: PDB 6A15")
    dump("165-bfactor",
         "mean_B,%.1f\nmedian_B,%.1f\nmax_running_peak_residue,%d\n"
         "max_running_peak_B,%.1f"
         % (mu, np.median(b), hot, k.max()))


# ------------------------------------------- 166 contact number
def contactnum():
    ca = [a for a in parse("6a15.pdb")
          if a["chain"] == "A" and not a["het"] and a["name"] == "CA"]
    ris = [a["resi"] for a in ca]
    P = np.array([a["xyz"] for a in ca])
    D = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=-1)
    idx = np.abs(np.arange(len(ris))[:, None] - np.arange(len(ris))[None, :])
    n = ((D < 8.0) & (idx >= 4)).sum(1)
    top = np.argsort(n)[-5:][::-1]
    fig, ax = plt.subplots(figsize=(9.6, 4.2))
    ax.plot(ris, n, color="#4C72B0", lw=0.9, label="contact count (<8 A)")
    k = np.convolve(n, np.ones(9) / 9, "same")
    ax.plot(ris, k, color="#DD8452", lw=2.0, label="9-residue running mean")
    ax.scatter([ris[i] for i in top], [n[i] for i in top], s=26,
               color="#C44E52", zorder=3, label="5 most-buried residues")
    ax.set_xlabel("residue")
    ax.set_ylabel("contacts per residue")
    ax.legend(fontsize=8.5)
    ax.set_title("Per-residue contact number of CYP90B1 (PDB 6A15, "
                 "real data)\nC-alpha neighbours within 8 A, |i-j| >= 4; "
                 "core peaks vs the SASA valleys of fig.155")
    save(fig, "166-contact-number", mark="Real structure data: PDB 6A15")
    rows = ["residue,contacts"] + \
           ["%d,%d" % (ris[i], n[i]) for i in top]
    dump("166-contact-number",
         "\n".join(["# 5 most buried"] + rows +
                   ["mean_contacts,%.1f" % n.mean()]))


# ------------------------------------------- 167 MD RMSD/Rg
def mdtrace():
    rng = np.random.default_rng(5167)
    t = np.linspace(0, 100, 501)
    rmsd = 0.75 + 1.05 * (1 - np.exp(-t / 22)) + rng.normal(0, 0.045, len(t))
    rg = 23.6 + 0.55 * (1 - np.exp(-t / 30)) + rng.normal(0, 0.05, len(t))
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8.4, 5.2), sharex=True)
    a1.plot(t, rmsd, color="#4C72B0", lw=1.0)
    a1.set_ylabel("RMSD (A)")
    a1.axhline(1.8, ls="--", color="0.4", lw=0.9)
    a1.text(2, 1.84, "plateau ~1.8 A", fontsize=8.5, color="0.4")
    a2.plot(t, rg, color="#55A868", lw=1.0)
    a2.set_ylabel("Rg (A)")
    a2.set_xlabel("time (ns)")
    a2.set_ylim(23.2, 24.6)
    fig.suptitle("100 ns molecular dynamics: backbone RMSD and radius of "
                 "gyration (simulated)", y=1.0)
    save(fig, "167-md-trace")
    dump("167-md",
         "rmsd_start,%.2f\nrmsd_plateau,%.2f\nrg_start,%.2f\nrg_end,%.2f"
         % (rmsd[:10].mean(), rmsd[-50:].mean(), rg[:10].mean(),
            rg[-50:].mean()))


# ------------------------------------- 168 H-bond occupancy
def hbond():
    rng = np.random.default_rng(5168)
    don = ["A21-N", "A25-O", "I68-N", "S72-OG", "H102-NE2", "T115-OG1",
           "E144-OE1", "K186-NZ", "S232-OG", "Y307-OH", "K310-NZ", "H385-NE2"]
    acc = ["CLR-O3", "HEM-O1D", "A21-O", "A24-O", "I68-O", "S72-O",
           "H102-O", "E144-OE2", "K186-O", "S232-O", "Y307-O", "T315-OG1"]
    M = np.clip(rng.beta(0.9, 3.2, (12, 12)), 0, 0.85)
    M[0, 0] = 0.78  # A21-N ... CLR-O3, the anchoring H-bond
    M[9, 0] = 0.42
    fig, ax = plt.subplots(figsize=(7.4, 6.2))
    im = ax.imshow(M, cmap="PuBu", vmin=0, vmax=0.9)
    ax.set_xticks(range(12), acc, rotation=45, ha="right", fontsize=7.5)
    ax.set_yticks(range(12), don, fontsize=7.5)
    ax.set_xlabel("acceptor")
    ax.set_ylabel("donor")
    ax.set_title("Hydrogen-bond occupancy of the binding site over an MD "
                 "trajectory (simulated)")
    fig.colorbar(im, ax=ax, shrink=0.8, label="fraction of frames")
    save(fig, "168-hbond-occupancy")
    rows = ["donor,acceptor,occupancy", "A21-N,CLR-O3,%.2f" % M[0, 0],
            "Y307-OH,CLR-O3,%.2f" % M[9, 0]]
    dump("168-hbond", "\n".join(rows))


# --------------------------------- 169 2D ligand interaction
def lig2d():
    pocket = [("PHE84", 3.85), ("TYR112", 3.60), ("MET125", 4.39),
              ("VAL216", 3.55), ("VAL217", 3.74), ("MET213", 3.93),
              ("SER307", 3.64), ("LEU308", 3.91), ("PHE310", 3.70),
              ("ALA311", 4.14), ("THR315", 3.79), ("VAL381", 3.87),
              ("PHE383", 3.17), ("LEU384", 4.03), ("HIS385", 2.88),
              ("PRO497", 4.30), ("PHE498", 4.71)]
    fig, ax = plt.subplots(figsize=(8.6, 6.2))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.25, 1.25)
    ax.axis("off")
    ax.add_patch(Rectangle((-0.55, -0.42), 1.10, 0.84,
                           fc="#f6e3c5", ec="#b06a1a", lw=1.6))
    ax.text(0, 0.24, "cholesterol", ha="center", fontsize=11,
            color="#7a4a12", weight="bold")
    for k in range(4):
        ax.plot([-0.36 + k * 0.24, -0.36 + k * 0.24],
                [-0.42, 0.42], color="#b06a1a", lw=0.7, alpha=0.5)
    ring = np.linspace(0, 2 * np.pi, len(pocket), endpoint=False)
    for (name, dist), th in zip(pocket, ring):
        x, y = 1.12 * np.cos(th), 0.94 * np.sin(th)
        hyd = name[0] in "VLIMAPF" and name not in ("SER307", "THR315",
                                                    "HIS385")
        col = "#9AA0A6" if hyd else "#3369c3"
        ax.plot([0.56 * np.sign(x) if abs(x) > 0.56 else 0.56 * np.cos(th),
                 x * 0.82], [0.42 * np.sign(y) if abs(y) > 0.42 else 0.0,
                             y * 0.82], color=col, lw=1.2, alpha=0.75)
        ax.scatter([x], [y], s=340, fc="white", ec=col, lw=1.2, zorder=3)
        ax.text(x, y, name, ha="center", va="center", fontsize=7.0,
                color="0.15", zorder=4)
    ax.scatter([], [], s=60, c="#9AA0A6",
               label="hydrophobic / van der Waals contact")
    ax.scatter([], [], s=60, c="#3369c3", label="polar contact / near polar")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=2,
              fontsize=8.5, frameon=False)
    ax.set_title("2D protein-ligand interaction map of the cholesterol "
                 "pocket\n(simulated drawing; residue list and distances "
                 "are real, PDB 6A15)")
    save(fig, "169-ligand-2d")
    dump("169-ligand-2d", "residue,dist_to_CLR_A\n" + "\n".join(
        "%s,%.2f" % (n, d) for n, d in pocket))


# ------------------------------- 170 coevolution vs contacts
def coevol():
    ca = [a for a in parse("6a15.pdb")
          if a["chain"] == "A" and not a["het"] and a["name"] == "CA"]
    P = np.array([a["xyz"] for a in ca])
    D = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=-1)
    L = len(P)
    iu = np.triu_indices(L, 9)
    true = (D[iu] < 8.0)
    rng = np.random.default_rng(5170)
    score = rng.normal(0, 1, len(iu[0]))
    boost = np.where(true, 2.1, 0) + 1.6 * np.exp(-np.abs(
        iu[0] - iu[1]) / 18.0)
    score = score + boost
    order = np.argsort(score)[::-1]
    topk = order[:60]
    prec = true[topk].mean()
    fig, ax = plt.subplots(figsize=(6.6, 6.2))
    ax.scatter(iu[1][~true], iu[0][~true], s=2.5, c="0.85", linewidths=0)
    ax.scatter(iu[1][true], iu[0][true], s=5, c="#4C72B0", linewidths=0,
               label="real contact (<8 A)")
    sel = topk
    hit = true[sel]
    ax.scatter(iu[1][sel[hit]], iu[0][sel[hit]], s=9, c="#C44E52",
               linewidths=0, label="co-evolution top-60 hit")
    ax.scatter(iu[1][sel[~hit]], iu[0][sel[~hit]], s=9, c="#DD8452",
               marker="x", linewidths=0.8,
               label="co-evolution top-60 miss")
    ax.set_xlim(0, L)
    ax.set_ylim(L, 0)
    ax.set_xlabel("residue i")
    ax.set_ylabel("residue j")
    ax.set_title("Co-evolution score vs real C-alpha contacts (CYP90B1)\n"
                 "top-60 pairs: precision %.0f%% (scores simulated, "
                 "contacts real)" % (100 * prec))
    ax.legend(loc="upper right", fontsize=8)
    save(fig, "170-coevolution-contacts",
         mark="Contacts real (PDB 6A15), MI scores simulated")
    dump("170-coevolution", "top60_precision,%.2f\ntrue_contacts,%d"
         % (prec, int(true.sum())))


# ------------------------------------------ 171 melt curve
def melt():
    rng = np.random.default_rng(5171)
    T = np.linspace(70, 95, 251)
    pk = lambda c, w: np.exp(-((T - c) / w) ** 2)
    clean = pk(84.5, 0.75) + 0.02 * rng.normal(0, 1, len(T))
    dirty = 0.92 * pk(84.5, 0.75) + 0.30 * pk(76.0, 0.9) \
        + 0.02 * rng.normal(0, 1, len(T))
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    ax.plot(T, clean, color="#4C72B0", lw=1.4, label="clean reaction")
    ax.plot(T, dirty, color="#C44E52", lw=1.4,
            label="reaction with primer-dimer")
    ax.annotate("specific product\ntm 84.5 C", (84.5, 1.0),
                textcoords="offset points", xytext=(8, -6), fontsize=9)
    ax.annotate("primer-dimer\n76.0 C", (76.0, 0.30),
                textcoords="offset points", xytext=(-58, 10), fontsize=9,
                color="#a03a3a")
    ax.set_xlabel("temperature (C)")
    ax.set_ylabel("-d(F)/dT")
    ax.legend(fontsize=8.5)
    ax.set_title("qPCR melt curves: one sharp peak = one amplicon "
                 "(simulated)")
    save(fig, "171-melt-curve")
    dump("171-melt", "specific_tm,84.5\nprimer_dimer_tm,76.0\n"
         "dimer_peak_fraction,0.30")


# ------------------------------------- 172 cycle linearity
def cyclelin():
    rng = np.random.default_rng(5172)
    cyc = np.arange(20, 39)
    gray = np.where(cyc <= 32, 0.10 * (cyc - 20) + rng.normal(0, 0.012, len(cyc)),
                    1.30 + rng.normal(0, 0.015, len(cyc)))
    lin = cyc <= 32
    k, b = np.polyfit(cyc[lin], gray[lin], 1)
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax.plot(cyc, gray, "o-", color="#4C72B0", ms=5, lw=1.2)
    ax.plot(cyc[lin], k * cyc[lin] + b, ls="--", color="0.5", lw=1)
    ax.axvspan(26, 30, color="#55A868", alpha=0.12)
    ax.text(28, 0.18, "linear range,\npick 28 cycles", ha="center",
            fontsize=9, color="#2d6a4f")
    ax.set_xlabel("cycle number")
    ax.set_ylabel("band intensity (a.u.)")
    ax.set_title("Semi-quantitative RT-PCR: keep the cycle count inside "
                 "the\nexponential phase (simulated)")
    save(fig, "172-cycle-linearity")
    dump("172-cycle", "linear_upto,32\nslope_per_cycle,%.3f\n"
         "chosen_cycle,28" % k)


# ------------------------------------------ 173 Western blot
def western():
    rng = np.random.default_rng(5173)
    lanes = ["WT", "dwf4-1", "dwf4-2", "comp"]
    target = np.array([1.00, 0.31, 0.52, 0.79])
    actin = np.array([0.98, 1.02, 0.97, 1.01])
    fig = plt.figure(figsize=(8.6, 5.6))
    gs = fig.add_gridspec(2, 1, height_ratios=[2.6, 1.0], hspace=0.42)
    axg = fig.add_subplot(gs[0])
    axg.add_patch(Rectangle((0.25, 0), 4.55, 2.0, fc="0.04", ec="0.3"))
    marks = [(1.62, "50 kDa"), (1.10, "37 kDa")]
    for yy, lab in marks:
        axg.add_patch(Rectangle((0.42, yy - 0.045), 0.26, 0.09,
                                fc="0.85", ec="none"))
        axg.text(0.55, yy + 0.07, lab, fontsize=6.5, color="0.8",
                 ha="center")
    for i, g in enumerate(target):
        cx = 1.35 + i * 0.85
        inten = 0.26 + 0.60 * g
        axg.add_patch(Rectangle((cx - 0.16, 1.52), 0.32, 0.20,
                                fc=str(min(0.92, inten)), ec="none"))
        axg.add_patch(Rectangle((cx - 0.16, 1.00), 0.32, 0.20,
                                fc=str(min(0.92, 0.30 + 0.62 * actin[i])),
                                ec="none"))
    axg.text(0.68, 1.62, "DWF4-3xFLAG 48 kDa", fontsize=7.5, color="0.75",
             va="center")
    axg.text(0.68, 1.10, "actin 45 kDa", fontsize=7.5, color="0.75",
             va="center")
    axg.set_xticks([0.55] + [1.35 + i * 0.85 for i in range(4)],
                   ["M"] + lanes)
    axg.set_yticks([])
    axg.set_xlim(0.15, 4.9)
    axg.set_ylim(-0.06, 2.06)
    axg.set_title("Western blot of tagged DWF4 (simulated)")
    axb = fig.add_subplot(gs[1])
    rel = target / actin
    rel = rel / rel[0]
    axb.bar(range(4), rel, color=["#4C72B0", "#C44E52", "#C44E52",
                                  "#55A868"], width=0.6)
    axb.axhline(1.0, ls="--", color="0.4", lw=0.9)
    axb.set_xticks(range(4), lanes)
    axb.set_ylabel("DWF4 / actin (rel. WT)")
    for i, v in enumerate(rel):
        axb.text(i, v + 0.03, "%.2f" % v, ha="center", fontsize=8.5)
    axb.set_title("Densitometry")
    save(fig, "173-western-blot")
    dump("173-western",
         "\n".join("lane,%s,rel_%.2f" % (l, v)
                   for l, v in zip(lanes, rel)))


if __name__ == "__main__":
    ramachandran()
    bfactor()
    contactnum()
    mdtrace()
    hbond()
    lig2d()
    coevol()
    melt()
    cyclelin()
    western()
