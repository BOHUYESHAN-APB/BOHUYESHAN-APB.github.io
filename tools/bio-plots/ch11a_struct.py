# -*- coding: utf-8 -*-
"""Gallery post 5 part A: figures rendered from REAL structure coordinates.

134 ca-trace line, 135 wireframe, 136 pocket stick, 137 space-filling,
138 simplified ribbon (all PDB 6A15), 144 contact map (6A15),
145 WT/mutant superposition (1BI5 vs 1I89), 150 pocket mapping (6A15),
155 per-residue SASA (6A15, Shrake-Rupley).
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from scipy.spatial import cKDTree
from scipy.interpolate import make_interp_spline

from common import save, dump

REL = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "source", "lib", "pdb") + os.sep

ELEMCOL = {"C": "#9aa3ad", "N": "#3369c3", "O": "#dd4b39",
           "S": "#e8b636", "FE": "#e07b39", "P": "#f08a5d"}
RAD = {"C": 1.70, "N": 1.55, "O": 1.52, "S": 1.80, "FE": 1.45, "P": 1.80}


def parse(fn):
    atoms = []
    for ln in open(REL + fn, encoding="ascii", errors="ignore"):
        rec = ln[:6]
        if rec in ("ATOM  ", "HETATM"):
            atoms.append(dict(
                het=rec.startswith("HET"),
                name=ln[12:16].strip(), resn=ln[17:20].strip(),
                chain=ln[21], resi=int(ln[22:26]),
                xyz=(float(ln[30:38]), float(ln[38:46]), float(ln[46:54])),
                b=float(ln[60:66]), elem=ln[76:78].strip() or ln[12:16].strip()[0]))
    return atoms


def poly(atoms, chain="A"):
    return [a for a in atoms if a["chain"] == chain and not a["het"]]


def cas(atoms, chain="A"):
    return [a for a in atoms if a["chain"] == chain and not a["het"]
            and a["name"] == "CA"]


def segs_by_res(atoms, lw):
    """Line segments within each residue following file order + peptide C-N."""
    segs, cols = [], []
    byres = {}
    for a in atoms:
        byres.setdefault((a["chain"], a["resi"]), []).append(a)
    prev_c = None
    for key in sorted(byres, key=lambda k: (k[0], k[1])):
        lst = byres[key]
        for i in range(len(lst) - 1):
            segs.append([lst[i]["xyz"], lst[i + 1]["xyz"]])
            cols.append(ELEMCOL.get(lst[i]["elem"], "#9aa3ad"))
        if prev_c is not None and lst[0]["name"] == "N":
            segs.append([prev_c, lst[0]["xyz"]])
            cols.append("#c3c3c3")
        for a in lst:
            if a["name"] == "C":
                prev_c = a["xyz"]
    return Line3DCollection(segs, colors=cols, linewidths=lw)


def view3d(fig, azim=-70, elev=12):
    ax = fig.add_subplot(111, projection="3d")
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    ax.set_box_aspect((1, 1, 1))
    # 3D panes reserve big blank margins; let artists overflow so the
    # tight-crop in save() keeps the molecule centered instead
    fig.subplots_adjust(left=-0.12, right=1.12, top=1.06, bottom=-0.06)
    return ax


# ------------------------------------------------------------ 134 CA trace
def ca_trace():
    atoms = parse("6a15.pdb")
    ca = cas(atoms)
    P = np.array([a["xyz"] for a in ca])
    fig = plt.figure(figsize=(8.2, 6.6))
    ax = view3d(fig)
    pts = np.concatenate([P[:-1, None, :], P[1:, None, :]], axis=1)
    cmap = matplotlib.colormaps["viridis"]
    cols = [cmap(i / (len(P) - 2)) for i in range(len(P) - 1)]
    ax.add_collection3d(Line3DCollection(pts, colors=cols, linewidths=2.2))
    ax.text(*P[0], " N", color="0.35", fontsize=9)
    ax.text(*P[-1], " C", color="0.35", fontsize=9)
    m, M = P.min(0), P.max(0)
    ctr, span = (m + M) / 2, (M - m).max() / 2 * 1.05
    ax.set_xlim(ctr[0] - span, ctr[0] + span)
    ax.set_ylim(ctr[1] - span, ctr[1] + span)
    ax.set_zlim(ctr[2] - span, ctr[2] + span)
    ax.set_title("C-alpha trace of CYP90B1 / DWF4 (%d residues, "
                 "PDB 6A15, real data)" % len(P))
    save(fig, "134-ca-trace", mark="Real structure data: PDB 6A15")


# --------------------------------------------------------- 135 wireframe
def wireframe():
    atoms = parse("6a15.pdb")
    pa = poly(atoms)
    fig = plt.figure(figsize=(8.2, 6.6))
    ax = view3d(fig)
    ax.add_collection3d(segs_by_res(pa, 0.6))
    P = np.array([a["xyz"] for a in pa])
    m, M = P.min(0), P.max(0)
    ctr, span = (m + M) / 2, (M - m).max() / 2 * 1.05
    ax.set_xlim(ctr[0] - span, ctr[0] + span)
    ax.set_ylim(ctr[1] - span, ctr[1] + span)
    ax.set_zlim(ctr[2] - span, ctr[2] + span)
    ax.set_title("Wireframe of CYP90B1 (backbone + side chains, "
                 "PDB 6A15, real data)")
    save(fig, "135-wireframe", mark="Real structure data: PDB 6A15")


# ------------------------------------------------------- 136 pocket stick
def pocket_stick():
    atoms = parse("6a15.pdb")
    lig = [a for a in atoms if a["het"] and a["resn"] == "CLR"]
    heme = [a for a in atoms if a["het"] and a["resn"] == "HEM"]
    L = np.array([a["xyz"] for a in lig])
    pa = poly(atoms)
    byres = {}
    for a in pa:
        byres.setdefault(a["resi"], []).append(a)
    pocket = []
    for ri, lst in byres.items():
        X = np.array([a["xyz"] for a in lst])
        d = np.linalg.norm(X[:, None, :] - L[None, :, :], axis=-1).min()
        if d <= 5.0:
            pocket.append((ri, lst[0]["resn"], d))
    fig = plt.figure(figsize=(8.6, 7.0))
    ax = view3d(fig, azim=-96, elev=16)
    ax.add_collection3d(segs_by_res([a for ri, _, _ in pocket
                                     for a in byres[ri]], 2.4))
    ax.add_collection3d(Line3DCollection(
        [[lig[i]["xyz"], lig[i + 1]["xyz"]] for i in range(len(lig) - 1)],
        colors="#e08a2e", linewidths=3.0))
    ax.add_collection3d(Line3DCollection(
        [[heme[i]["xyz"], heme[i + 1]["xyz"]] for i in range(len(heme) - 1)],
        colors="#c44e52", linewidths=3.0))
    for ri, rn, d in pocket:
        a = [x for x in byres[ri] if x["name"] == "CA"]
        if a:
            ax.text(*a[0]["xyz"], " %s%d" % (rn, ri), fontsize=6.6,
                    color="0.25")
    allp = np.array([a["xyz"] for a in lig + heme] +
                    [a["xyz"] for ri, _, _ in pocket for a in byres[ri]])
    m, M = allp.min(0), allp.max(0)
    ctr, span = (m + M) / 2, (M - m).max() / 2 * 1.12
    ax.set_xlim(ctr[0] - span, ctr[0] + span)
    ax.set_ylim(ctr[1] - span, ctr[1] + span)
    ax.set_zlim(ctr[2] - span, ctr[2] + span)
    ax.set_title("Cholesterol-binding pocket of CYP90B1: pocket residues "
                 "(%d within 5 A) as sticks\norange = cholesterol, red = "
                 "heme (PDB 6A15, real data)" % len(pocket))
    save(fig, "136-pocket-stick", mark="Real structure data: PDB 6A15")
    rows = ["residue,dist_to_ligand_A"]
    for ri, rn, d in sorted(pocket):
        rows.append("%s%d,%.2f" % (rn, ri, d))
    dump("136-pocket-residues", "\n".join(rows))


# -------------------------------------------------------- 137 spacefill
def spacefill():
    atoms = [a for a in parse("6a15.pdb")
             if (not a["het"] or a["resn"] in ("HEM", "CLR"))]
    P = np.array([a["xyz"] for a in atoms])
    r = np.array([RAD.get(a["elem"], 1.7) for a in atoms])
    c = [ELEMCOL.get(a["elem"], "#9aa3ad") for a in atoms]
    fig = plt.figure(figsize=(8.4, 6.8))
    ax = view3d(fig)
    ax.scatter(P[:, 0], P[:, 1], P[:, 2], s=(r * 26) ** 1.6 / 6,
               c=c, linewidths=0)
    m, M = P.min(0), P.max(0)
    ctr, span = (m + M) / 2, (M - m).max() / 2 * 1.08
    ax.set_xlim(ctr[0] - span, ctr[0] + span)
    ax.set_ylim(ctr[1] - span, ctr[1] + span)
    ax.set_zlim(ctr[2] - span, ctr[2] + span)
    ax.set_title("Space-filling (CPK) model of CYP90B1 with heme and "
                 "cholesterol\n(PDB 6A15, real data)")
    save(fig, "137-spacefill", mark="Real structure data: PDB 6A15")


# ---------------------------------------------------------- 138 ribbon
def ribbon():
    ca = cas(parse("6a15.pdb"))
    P = np.array([a["xyz"] for a in ca])
    t = np.zeros(len(P))
    t[1:] = np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))
    ts = np.linspace(t[0], t[-1], 800)
    S = make_interp_spline(t, P, k=3)(ts)
    fig = plt.figure(figsize=(8.2, 6.6))
    ax = view3d(fig)
    pts = np.concatenate([S[:-1, None, :], S[1:, None, :]], axis=1)
    cmap = matplotlib.colormaps["cool"]
    ax.add_collection3d(Line3DCollection(
        pts, colors=[cmap(i / (len(S) - 2)) for i in range(len(S) - 1)],
        linewidths=6.5))
    m, M = P.min(0), P.max(0)
    ctr, span = (m + M) / 2, (M - m).max() / 2 * 1.05
    ax.set_xlim(ctr[0] - span, ctr[0] + span)
    ax.set_ylim(ctr[1] - span, ctr[1] + span)
    ax.set_zlim(ctr[2] - span, ctr[2] + span)
    ax.set_title("Simplified ribbon of CYP90B1 (smoothed C-alpha path, "
                 "PDB 6A15, real data)")
    save(fig, "138-ribbon", mark="Real structure data: PDB 6A15")


# ------------------------------------------------------- 144 contact map
def contact_map():
    ca = cas(parse("6a15.pdb"))
    P = np.array([a["xyz"] for a in ca])
    D = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=-1)
    fig, ax = plt.subplots(figsize=(6.9, 6.2))
    im = ax.imshow(D, cmap="viridis_r", vmin=4, vmax=45)
    ax.contour(np.arange(len(P)), np.arange(len(P)), (D < 8).astype(float),
               levels=[0.5], colors="black", linewidths=0.3)
    ax.set_xlabel("residue i")
    ax.set_ylabel("residue j")
    ax.set_title("C-alpha distance map of CYP90B1, black = contacts < 8 A"
                 "\n(PDB 6A15, real data, %d residues)" % len(P))
    fig.colorbar(im, ax=ax, shrink=0.85, label="distance (A)")
    save(fig, "144-contact-map", mark="Real structure data: PDB 6A15")


# -------------------------------------------------- 145 superposition
def kabsch(P, Q):
    pc, qc = P.mean(0), Q.mean(0)
    H = (P - pc).T @ (Q - qc)
    U, _, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1, 1, d]) @ U.T
    return (P - pc) @ R + qc


def superpose():
    w = cas(parse("1bi5.pdb"))
    m = cas(parse("1i89.pdb"), chain="A")
    wi = {a["resi"]: a for a in w}
    mi = {a["resi"]: a for a in m}
    common = sorted(set(wi) & set(mi))
    Q = np.array([wi[i]["xyz"] for i in common])   # WT
    P = np.array([mi[i]["xyz"] for i in common])   # mutant G256L
    Pt = kabsch(P, Q)
    dev = np.linalg.norm(Pt - Q, axis=1)
    g = float(np.sqrt((dev ** 2).mean()))
    fig = plt.figure(figsize=(10.8, 6.0))
    ax = view3d(fig, azim=-60, elev=14)
    # blue solid underneath, red dashed on top: gaps in the dashes let the
    # near-coincident WT trace show through instead of being hidden
    for X, col, ls, lw in [(Q, "#4C72B0", "solid", 2.0),
                           (Pt, "#C44E52", (0, (5, 4)), 1.8)]:
        pts = np.concatenate([X[:-1, None, :], X[1:, None, :]], axis=1)
        ax.add_collection3d(Line3DCollection([pts[i] for i in
                                              range(0, len(pts), 3)],
                                             colors=col, linewidths=lw,
                                             linestyles=ls))
    m_, M_ = Q.min(0), Q.max(0)
    ctr, span = (m_ + M_) / 2, (M_ - m_).max() / 2 * 1.05
    ax.set_xlim(ctr[0] - span, ctr[0] + span)
    ax.set_ylim(ctr[1] - span, ctr[1] + span)
    ax.set_zlim(ctr[2] - span, ctr[2] + span)
    ax.set_title("1BI5 (WT, blue) vs 1I89 (G256L, red) superposed C-alpha "
                 "traces\n%d common residues, global RMSD %.2f A (real data)"
                 % (len(common), g))
    save(fig, "145-superpose",
         mark="Real structures: PDB 1BI5 (WT) vs 1I89 (G256L)")
    rows = ["residue,dev_A", "G256,%.2f" % dev[common.index(256)]]
    top = np.argsort(dev)[-8:]
    for k in sorted(top):
        rows.append("%s%d,%.2f" % (wi[common[k]]["resn"], common[k], dev[k]))
    dump("145-superpose-dev", "\n".join(rows))


# ---------------------------------------------------- 150 pocket mapping
def pocket_map():
    atoms = parse("6a15.pdb")
    lig = [a for a in atoms if a["het"] and a["resn"] == "CLR"]
    heme = [a for a in atoms if a["het"] and a["resn"] == "HEM"]
    L = np.array([a["xyz"] for a in lig])
    H = np.array([a["xyz"] for a in heme])
    pa = poly(atoms)
    byres = {}
    for a in pa:
        byres.setdefault(a["resi"], []).append(a)
    pk = []
    for ri, lst in byres.items():
        X = np.array([a["xyz"] for a in lst])
        if np.linalg.norm(X[:, None, :] - L[None, :, :],
                          axis=-1).min() <= 5.0:
            pk += lst
    fig = plt.figure(figsize=(8.4, 6.8))
    ax = view3d(fig, azim=-96, elev=16)
    ca = [a for a in pa if a["name"] == "CA"]
    P = np.array([a["xyz"] for a in ca])
    pts = np.concatenate([P[:-1, None, :], P[1:, None, :]], axis=1)
    ax.add_collection3d(Line3DCollection(pts, colors="0.78", linewidths=1.2))
    X = np.array([a["xyz"] for a in pk])
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], s=26, c="#C44E52",
               depthshade=True, linewidths=0)
    ax.scatter(L[:, 0], L[:, 1], L[:, 2], s=64, c="#e08a2e",
               depthshade=True, linewidths=0)
    ax.scatter(H[:, 0], H[:, 1], H[:, 2], s=40, c="#8172B3",
               depthshade=True, linewidths=0)
    m_, M_ = P.min(0), P.max(0)
    ctr, span = (m_ + M_) / 2, (M_ - m_).max() / 2 * 1.05
    ax.set_xlim(ctr[0] - span, ctr[0] + span)
    ax.set_ylim(ctr[1] - span, ctr[1] + span)
    ax.set_zlim(ctr[2] - span, ctr[2] + span)
    ax.set_title("Pocket residues (red) mapped on the CYP90B1 structure\n"
                 "orange = cholesterol, purple = heme (PDB 6A15, real data)")
    save(fig, "150-pocket-map", mark="Real structure data: PDB 6A15")


# ------------------------------------------------------------- 155 SASA
def sasa():
    atoms = parse("6a15.pdb")
    keep = [a for a in atoms if (not a["het"] or a["resn"] in ("HEM", "CLR"))]
    X = np.array([a["xyz"] for a in keep])
    r = np.array([RAD.get(a["elem"], 1.7) + 1.4 for a in keep])
    n = 92
    k = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * k / n)
    gg = np.pi * (1 + 5 ** 0.5)
    theta = gg * k
    SP = np.c_[np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi),
               np.cos(phi)] * r[:, None, None]
    pts = (SP + X[:, None, :]).reshape(-1, 3)
    tree = cKDTree(X)
    frac = np.ones(len(keep))
    rad = r.copy()
    lists = tree.query_ball_point(pts, rad.repeat(n), workers=-1)
    cnt = np.array([len(l) for l in lists]).reshape(len(keep), n)
    frac = (cnt == 0).mean(1)
    area = 4 * np.pi * r ** 2 * frac
    per = {}
    names = {}
    for a, s_ in zip(keep, area):
        if a["name"] != "HOH":
            per[a["resi"]] = per.get(a["resi"], 0) + s_
            names[a["resi"]] = a["resn"]
    ris = sorted(per)
    vals = np.array([per[i] for i in ris])
    dump("155-sasa", "\n".join(
        ["residue,sasa_A2"] +
        ["%s%d,%.1f" % (names[i], i, per[i]) for i in ris]))
    lig = np.array([a["xyz"] for a in atoms
                    if a["het"] and a["resn"] == "CLR"])
    pocket = set()
    for a in keep:
        if np.linalg.norm(np.array(a["xyz"])[None, :] - lig,
                          axis=1).min() <= 5.0:
            pocket.add(a["resi"])
    fig, ax = plt.subplots(figsize=(9.6, 4.2))
    ax.plot(ris, vals, color="#4C72B0", lw=1.1)
    k = np.convolve(vals, np.ones(9) / 9, mode="same")
    ax.plot(ris, k, color="#DD8452", lw=2.0, label="9-residue running mean")
    pkv = [(i, per[i]) for i in ris if i in pocket]
    ax.scatter([p[0] for p in pkv], [p[1] for p in pkv], s=22,
               color="#C44E52", label="pocket residues (< 5 A from ligand)",
               zorder=3)
    ax.set_xlabel("residue")
    ax.set_ylabel("SASA (A^2)")
    ax.legend(fontsize=8.5, loc="upper right")
    ax.set_title("Per-residue solvent accessibility (Shrake-Rupley) of "
                 "CYP90B1 (PDB 6A15, real data)")
    save(fig, "155-sasa", mark="Real structure data: PDB 6A15")


if __name__ == "__main__":
    ca_trace()
    wireframe()
    pocket_stick()
    spacefill()
    ribbon()
    contact_map()
    superpose()
    pocket_map()
    sasa()
