# -*- coding: utf-8 -*-
"""Gallery post 5 part B: SIMULATED prediction / mutation figures.

143 PAE heatmap, 146 mutation lollipop, 147 substitution-tolerance matrix,
148 ddG bars, 149 secondary-structure track, 151 pocket-volume bars,
152 conservation profile (pocket tick positions taken from the real 6A15
pocket computation in ch11a), 153 docking scores/poses,
154 interface contact-frequency heatmap.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from common import save, dump, csv_cols, num

N = 520  # DWF4-like protein length used across figures

# real pocket residues within 5 A of cholesterol, computed from PDB 6A15
# (ch11a_struct.py figure 136 dump)
POCKET = [84, 112, 113, 116, 120, 124, 125, 126, 213, 216, 217, 307, 308,
          310, 311, 314, 315, 381, 383, 384, 385, 497, 498]


# ------------------------------------------------------------------ 143 PAE
def pae():
    rng = np.random.default_rng(5143)
    i = np.arange(N)[:, None]
    j = np.arange(N)[None, :]
    sep = np.abs(i - j)
    base = 0.8 + 4.0 * (sep / N) ** 1.7
    loop = ((i > 300) & (i < 322)) | ((j > 300) & (j < 322))
    M = base + rng.normal(0, 0.3, (N, N)) + loop * np.where(sep > 25, 2.6, 0)
    M = np.clip(M, 0.3, 9.0)
    fig, ax = plt.subplots(figsize=(6.6, 5.6))
    im = ax.imshow(M, cmap="viridis", origin="lower", vmin=0, vmax=9,
                   extent=[1, N, 1, N])
    ax.plot([1, N], [1, N], color="white", lw=0.6, alpha=0.7)
    ax.set_xlabel("scored residue")
    ax.set_ylabel("aligned residue")
    ax.set_title("Predicted aligned error (PAE) of a simulated AlphaFold run\n"
                 "single-domain protein: low PAE along diagonal, "
                 "noisy loop 301-321 (simulated)")
    fig.colorbar(im, ax=ax, shrink=0.85, label="PAE (A)")
    save(fig, "143-pae-map")
    rows = ["residue_i,residue_j,PAE_A"]
    for a in range(60, N, 60):
        for b in range(60, N, 60):
            rows.append("%d,%d,%.1f" % (a, b, M[a - 1, b - 1]))
    dump("143-pae", "\n".join(rows))


# --------------------------------------------------------- 146 lollipop
def lollipop():
    rng = np.random.default_rng(5146)
    pos = sorted(rng.choice(np.arange(35, 505), 22, replace=False).tolist())
    pos[7] = 256   # pocket glycine (G256L analog)
    pos[15] = 385  # pocket histidine
    pos = sorted(set(pos))
    sc = np.clip(rng.beta(1.7, 3.1, len(pos)), 0.03, 0.97)
    sc[pos.index(256)] = 0.93
    sc[pos.index(385)] = 0.86
    cls = np.where(sc > 0.5, "loss_of_function",
                   np.where(sc > 0.3, "hypomorphic", "neutral"))
    cols = np.where(sc > 0.5, "#C44E52",
                    np.where(sc > 0.3, "#DD8452", "#9AA0A6"))
    fig, ax = plt.subplots(figsize=(9.4, 4.4))
    ax.vlines(pos, 0, sc, color=cols, lw=1.6)
    ax.scatter(pos, sc, s=44, c=cols, zorder=3)
    for p, s in [(256, 0.93), (385, 0.86)]:
        ax.annotate("G%dL" % p if p == 256 else "H%dN" % p,
                    (p, s), textcoords="offset points", xytext=(-6, 9),
                    fontsize=8.5, color="0.25")
    ax.set_xlabel("residue position")
    ax.set_ylabel("deleteriousness score")
    ax.set_ylim(0, 1.05)
    ax.set_title("Missense mutations along the 520-residue protein, "
                 "lollipop height = predicted\n deleteriousness "
                 "(simulated, 23 variants)")
    for lab, c in [("loss of function", "#C44E52"),
                   ("hypomorphic", "#DD8452"), ("neutral", "#9AA0A6")]:
        ax.scatter([], [], c=c, label=lab)
    ax.legend(loc="upper left", ncol=3)
    save(fig, "146-mutation-lollipop")
    rows = ["position,score,class"]
    for p, s, k in zip(pos, sc, cls):
        rows.append("%d,%.2f,%s" % (p, s, k))
    dump("146-lollipop", "\n".join(rows))


# ------------------------------------------------- 147 substitution matrix
def subsmatrix():
    rng = np.random.default_rng(5147)
    AA = list("ACDEFGHIKLMNPQRSTVWY")
    kd = dict(zip(AA, [1.8, 2.5, -3.5, -3.5, 2.8, -0.4, -3.2, 4.5, -3.9,
                       3.8, 1.9, -3.5, -1.6, -3.5, -4.5, -0.8, -0.7, 4.2,
                       -0.9, -1.3]))
    pos = set("KRH")
    neg = set("DE")
    M = np.zeros((20, 20))
    for a in range(20):
        for b in range(20):
            if a == b:
                continue
            d = abs(kd[AA[a]] - kd[AA[b]])
            charge = 2.2 if ((AA[a] in pos and AA[b] in neg) or
                             (AA[a] in neg and AA[b] in pos)) else 0.0
            pro = 1.5 if "P" in (AA[a], AA[b]) else 0.0
            cys = 1.2 if "C" in (AA[a], AA[b]) else 0.0
            M[a, b] = 0.45 * d + charge + pro + cys + rng.normal(0, 0.25)
    M = np.clip((M + M.T) / 2, 0, None)
    np.fill_diagonal(M, 0.0)
    fig, ax = plt.subplots(figsize=(7.0, 6.0))
    im = ax.imshow(M, cmap="magma_r")
    ax.set_xticks(range(20), AA)
    ax.set_yticks(range(20), AA)
    ax.set_xlabel("to residue")
    ax.set_ylabel("from residue")
    ax.set_title("Mean structure-disruption score for every amino-acid\n"
                 "substitution in the active-site environment (simulated)")
    fig.colorbar(im, ax=ax, shrink=0.85, label="mean ddG (kcal/mol)")
    save(fig, "147-substitution-matrix")
    rows = ["from\\\\to," + ",".join(AA)]
    for a in range(20):
        rows.append(AA[a] + "," + ",".join("%.1f" % M[a, b] for b in range(20)))
    dump("147-subs-matrix", "\n".join(rows))


# -------------------------------------------------------------- 148 ddG
def ddg():
    txt = """mutant,ddG_kcal_mol,se
G256A,0.4,0.1
G256V,1.2,0.2
G256L,2.9,0.3
F84A,1.8,0.2
F84Y,0.5,0.1
H385A,3.4,0.3
H385N,1.6,0.2
V216A,0.8,0.1
V216F,2.1,0.2
S307A,0.3,0.1
T315A,0.2,0.1
L384P,4.1,0.4"""
    h, c = csv_cols(txt)
    mut = c["mutant"]
    v = num(c, "ddG_kcal_mol")
    e = num(c, "se")
    cols = np.where(v > 2.0, "#C44E52", "#4C72B0")
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    ax.bar(range(len(mut)), v, yerr=e, capsize=3, color=cols, width=0.62)
    ax.axhline(2.0, ls="--", color="0.35", lw=1)
    ax.text(len(mut) - 0.4, 2.08, "destabilizing threshold ddG = 2.0",
            ha="right", fontsize=8.5, color="0.35")
    ax.set_xticks(range(len(mut)), mut, rotation=45, ha="right", fontsize=8.5)
    ax.set_ylabel("ddG (kcal/mol)")
    ax.set_title("Predicted stability change of 12 pocket mutants\n"
                 "red = above the 2.0 kcal/mol destabilizing threshold "
                 "(simulated)")
    save(fig, "148-ddg-bars")
    dump("148-ddg", txt)


# ------------------------------------------------------ 149 SS track
def sstrack():
    seg = """start,end,type,label
34,46,helix,A
60,72,helix,B
90,102,helix,B'
110,116,sheet,b1
130,136,helix,C
148,160,helix,D
190,205,helix,E
210,216,sheet,b2
220,236,helix,F
250,262,helix,G
292,330,helix,I
342,352,helix,J
360,368,sheet,b3
380,395,helix,K'
420,432,helix,meander
452,462,helix,heme loop
500,508,sheet,b4"""
    srs = """start,end,label
96,106,SRS1
208,218,SRS2
248,262,SRS3
316,326,SRS4
388,398,SRS5"""
    h1, c1 = csv_cols(seg)
    h2, c2 = csv_cols(srs)
    rng = np.random.default_rng(5149)
    x = np.arange(1, N + 1)
    dis = np.clip(0.12 + 0.5 * np.exp(-((x - 40) / 45.0) ** 2)
                  + 0.45 * np.exp(-((x - 311) / 16.0) ** 2)
                  + 0.55 * np.exp(-((x - 516) / 26.0) ** 2)
                  + rng.normal(0, 0.045, N), 0.01, 0.98)
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(9.6, 4.6),
                                  sharex=True,
                                  gridspec_kw=dict(height_ratios=[1.5, 1]))
    cmap = dict(helix="#4C72B0", sheet="#DD8452")
    for s, e, t in zip(num(c1, "start"), num(c1, "end"), c1["type"]):
        ax.add_patch(Rectangle((s, 0.32), e - s + 1, 0.36,
                               color=cmap[t], lw=0))
    for s, e, lab in zip(num(c2, "start"), num(c2, "end"), c2["label"]):
        ax.add_patch(Rectangle((s, 0.78), e - s + 1, 0.16,
                               color="#55A868", alpha=0.85, lw=0))
        ax.text((s + e) / 2, 0.70, lab, ha="center", fontsize=7.5,
                color="#2d6a4f")
    ax.add_patch(Rectangle((1, 0.10), N, 0.14, color="#E3E6EA", lw=0))
    ax.text(2, 0.245, "coil / unannotated", fontsize=7.5, color="0.4",
            va="center")
    for p, lab in [(256, "G256"), (385, "H385"), (462, "heme Cys")]:
        ax.axvline(p, color="0.3", lw=0.8, ls=":")
        ax.text(p, -0.06, lab, ha="center", fontsize=7.5, color="0.3")
    ax.set_ylim(-0.12, 1.02)
    ax.set_yticks([])
    for lab, c in [("helix", "#4C72B0"), ("sheet", "#DD8452"),
                   ("SRS 1-5", "#55A868")]:
        ax.add_patch(Rectangle((0, 0), 0, 0, color=c, label=lab))
    ax.legend(loc="lower right", ncol=3, fontsize=8)
    ax.set_title("Secondary-structure and substrate-recognition-site "
                 "annotation track (simulated layout)")
    ax2.plot(x, dis, color="#8172B3", lw=1.1)
    ax2.fill_between(x, dis, color="#8172B3", alpha=0.15)
    ax2.set_ylabel("disorder")
    ax2.set_xlabel("residue")
    ax2.set_ylim(0, 1)
    save(fig, "149-ss-track")
    rows = ["residue,disorder"] + \
           ["%d,%.2f" % (i + 1, dis[i]) for i in range(4, N, 40)]
    dump("149-ss", "\n".join(rows))


# ------------------------------------------------- 151 pocket-volume bars
def pocketvol():
    txt = """variant,pocket_volume_A3
WT,975
G256A,921
G256V,806
G256L,648
F84A,1078
F215W,892
H385N,1055
V216F,742"""
    h, c = csv_cols(txt)
    v = num(c, "pocket_volume_A3")
    labs = c["variant"]
    cols = ["#4C72B0" if l == "WT" else
            ("#C44E52" if x < 700 else "#9AA0A6") for l, x in zip(labs, v)]
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    ax.bar(range(len(v)), v, color=cols, width=0.6)
    ax.axhline(405, ls="--", color="#e08a2e", lw=1.4)
    ax.text(0.02, 405, "cholesterol molecular volume ~ 405 A^3",
            fontsize=8.5, color="#b06a1a", va="bottom")
    for i, x in enumerate(v):
        ax.text(i, x + 14, "%d" % x, ha="center", fontsize=8)
    ax.set_xticks(range(len(v)), labs, rotation=30, ha="right")
    ax.set_ylabel("pocket volume (A^3)")
    ax.set_ylim(0, 1150)
    ax.set_title("Substrate-pocket volume of WT and pocket mutants\n"
                 "red = too tight for the ligand (simulated, "
                 "CASTp-style measurements)")
    save(fig, "151-pocket-volume")
    dump("151-pocket-volume", txt)


# -------------------------------------------------- 152 conservation
def conservation():
    rng = np.random.default_rng(5152)
    x = np.arange(1, N + 1)
    cons = np.clip(0.58 + rng.normal(0, 0.10, N), 0.25, 0.9)
    for p in POCKET:
        cons[p - 1] = np.clip(0.90 + rng.normal(0, 0.03), 0.85, 0.98)
    heme = (x >= 448) & (x <= 468)
    cons[heme] = np.clip(cons[heme] + 0.25, 0, 0.97)
    pk = np.array([cons[p - 1] for p in POCKET])
    fig, ax = plt.subplots(figsize=(9.6, 4.2))
    ax.plot(x, cons, color="#4C72B0", lw=1.0)
    ax.scatter(POCKET, pk, s=30, color="#C44E52", zorder=3,
               label="pocket residues (real positions from PDB 6A15)")
    ax.axvspan(448, 468, color="#8172B3", alpha=0.14,
               label="heme-binding region")
    ax.set_xlabel("residue")
    ax.set_ylabel("conservation (0-1)")
    ax.set_ylim(0.15, 1.02)
    ax.legend(loc="lower right", fontsize=8.5)
    ax.set_title("Sequence-conservation profile across the protein family\n"
                 "pocket and heme-binding residues sit on conserved peaks "
                 "(simulated values, real pocket positions)")
    save(fig, "152-conservation")
    rows = ["residue,conservation"] + \
           ["%d,%.2f" % (i + 1, cons[i]) for i in range(4, N, 40)] + \
           ["---pocket---"] + \
           ["%d,%.2f" % (p, cons[p - 1]) for p in POCKET]
    dump("152-conservation", "\n".join(rows))


# ---------------------------------------------------------- 153 docking
def docking():
    rng = np.random.default_rng(5153)
    poses = np.arange(1, 31)
    # two clusters: near-native (low rmsd, best scores) + decoys
    near_n = 9
    rmsd = np.concatenate([1.1 + rng.normal(0, 0.22, near_n),
                           5.0 + rng.normal(0, 1.1, 30 - near_n)])
    score = np.concatenate([-9.6 + 0.25 * (rmsd[:near_n] - 1.1)
                            + rng.normal(0, 0.25, near_n),
                            -6.8 + rng.normal(0, 0.55, 30 - near_n)])
    score = np.clip(score, -11.5, -5.0)
    cpd = """compound,score_kcal_mol
cholesterol,-9.3
22-OH-cholesterol,-8.8
6-deoxocathasterone,-8.1
6-deoxoteasterone,-7.2
campestanol,-6.4
stigmasterol,-5.9"""
    h2, c2 = csv_cols(cpd)
    s2 = num(c2, "score_kcal_mol")
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.4),
                                  gridspec_kw=dict(wspace=0.3))
    cols = np.where(rmsd < 2.5, "#C44E52", "#9AA0A6")
    ax.scatter(poses, score, c=cols, s=46, zorder=3)
    ax.axhspan(-11.5, -9.0, color="#C44E52", alpha=0.07)
    ax.text(1.2, -9.15, "near-native cluster", fontsize=8.5, color="#a03a3a")
    ax.set_xlabel("pose rank")
    ax.set_ylabel("docking score (kcal/mol)")
    ax.set_ylim(-11.5, -5.0)
    ax.set_title("Top-30 docking poses")
    ax2.barh(range(len(s2)), s2, color="#4C72B0", height=0.62)
    ax2.set_yticks(range(len(s2)), c2["compound"], fontsize=8.5)
    ax2.set_xlim(-11.5, 0)
    ax2.axvline(-7.0, ls="--", color="0.4", lw=1)
    ax2.text(-6.9, 0.0, "binding cutoff -7.0", fontsize=8, color="0.4")
    ax2.set_xlabel("best score (kcal/mol)")
    ax2.set_title("Substrate-analog screening")
    fig.suptitle("Molecular-docking readout: pose clustering and compound "
                 "ranking (simulated)", y=1.02)
    save(fig, "153-docking")
    rows = ["pose,rmsd_A,score_kcal_mol"] + \
           ["%d,%.2f,%.2f" % (p, r, s)
            for p, r, s in zip(poses, rmsd, score)]
    dump("153-docking-poses", "\n".join(rows))
    dump("153-docking-compounds", cpd)


# ------------------------------------------------- 154 interface contacts
def interface():
    rng = np.random.default_rng(5154)
    A = list("DFIKVWYHMRE")
    B = list("VLIFYDEHKRW")
    na, nb = len(A), len(B)
    M = np.clip(rng.beta(1.4, 2.4, (na, nb)) * 1.15, 0, 1)
    M[3:6, 4:7] = np.clip(M[3:6, 4:7] + 0.55, 0, 1)  # hot-spot core
    M[8:10, 2:4] = np.clip(M[8:10, 2:4] + 0.35, 0, 1)
    fig, ax = plt.subplots(figsize=(6.8, 5.8))
    im = ax.imshow(M, cmap="YlOrRd", vmin=0, vmax=1)
    ax.add_patch(Rectangle((3.5 - 0.5, 3.5 - 0.5), 3, 3, fill=False,
                           ec="#2b5f8a", lw=1.8))
    ax.text(4.5, 7.1, "hot-spot core", color="#2b5f8a", fontsize=8.5,
            ha="center")
    ax.set_xticks(range(nb), B)
    ax.set_yticks(range(na), A)
    ax.set_xlabel("partner-B interface residues")
    ax.set_ylabel("protein-A interface residues")
    ax.set_title("Interface contact frequency over an MD trajectory\n"
                 "cell = fraction of frames in contact (simulated)")
    fig.colorbar(im, ax=ax, shrink=0.85, label="contact frequency")
    save(fig, "154-interface-contacts")
    rows = ["A\\\\B," + ",".join(B)]
    for a in range(na):
        rows.append(A[a] + "," + ",".join("%.2f" % M[a, b] for b in range(nb)))
    dump("154-interface", "\n".join(rows))


if __name__ == "__main__":
    pae()
    lollipop()
    subsmatrix()
    ddg()
    sstrack()
    pocketvol()
    conservation()
    docking()
    interface()
