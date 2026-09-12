# -*- coding: utf-8 -*-
"""ch12e — 4LSX 真实结构图（189 接触图 / 190 B因子 / 191 界面ΔSASA）
数据：PDB 4LSX（BRI1-BAK1-BL 复合物晶体结构，2.35 MB 原文件）
注：188 号图为网页内嵌 3D 交互查看器（pdb-viewer.js），无 PNG。
"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import save

HERE = os.path.dirname(os.path.abspath(__file__))
PDB = os.path.join(HERE, "data-real", "4LSX.pdb")
MARK = "Real structure data: PDB 4LSX"
CONTACT = 4.5


def parse_pdb(path):
    """-> chains {cid: [(resseq, resname) 首见顺序去重]}, coords/bf/a2r {cid};
       a2r[atom] = 该链残基列表下标；非水 HETATM（配体/糖链）单独返回"""
    chains, res_idx = {}, {}
    coords, bf, a2r = {}, {}, {}
    het = []
    with open(path) as f:
        for line in f:
            rec = line[:6]
            if rec == "HETATM":
                rn = line[17:20].strip()
                if rn != "HOH":
                    het.append((rn, line[21],
                                float(line[30:38]), float(line[38:46]), float(line[46:54])))
                continue
            if rec != "ATOM  ":
                continue
            elem = line[76:78].strip()
            if elem == "H":
                continue
            cid = line[21]
            rs, rn = int(line[22:26]), line[17:20].strip()
            if cid not in chains:
                chains[cid] = []
                res_idx[cid] = {}
                coords[cid], bf[cid], a2r[cid] = [], [], []
            if rs not in res_idx[cid]:
                res_idx[cid][rs] = len(chains[cid])
                chains[cid].append((rs, rn))
            a2r[cid].append(res_idx[cid][rs])
            coords[cid].append((float(line[30:38]), float(line[38:46]), float(line[46:54])))
            bf[cid].append(float(line[60:66]))
    for cid in chains:
        coords[cid] = np.array(coords[cid])
        bf[cid] = np.array(bf[cid])
        a2r[cid] = np.array(a2r[cid], dtype=int)
    return chains, coords, bf, a2r, het


def asa(xyz, elems, r_probe=1.4, npts=92):
    from scipy.spatial import cKDTree
    vdW = {"C": 1.7, "N": 1.55, "O": 1.52, "S": 1.8}
    r = np.array([vdW.get(e, 1.7) for e in elems])
    ga = np.pi * (3 - np.sqrt(5))
    i = np.arange(npts)
    z = 1 - 2 * (i + 0.5) / npts
    sphere = np.stack([np.cos(ga * i) * np.sqrt(1 - z * z),
                       np.sin(ga * i) * np.sqrt(1 - z * z), z], axis=1)
    probe = (r[:, None, None] + r_probe) * sphere[None, :, :]
    tree = cKDTree(xyz)
    asa = np.zeros(len(xyz))
    for a in range(len(xyz)):
        neigh = tree.query_ball_point(xyz[a], r[a] + 2 * r_probe + 1.7)
        test = xyz[a] + probe[a]
        blocked = np.zeros(npts, dtype=bool)
        for b in neigh:
            if b == a:
                continue
            blocked |= (np.einsum("ij,ij->i", test - xyz[b], test - xyz[b]) <
                        (r[b] + r_probe) ** 2)
        asa[a] = 4 * np.pi * (r[a] + r_probe) ** 2 * (~blocked).sum() / npts
    return asa


def fig189_contact(chains, coords, a2r):
    import matplotlib.pyplot as plt
    ca, cb = "A", "C"  # 4LSX: A/C 与 B/D 各为一个 BRI1-SERK1 异源二聚体
    from scipy.spatial import cKDTree
    ta, tb = cKDTree(coords[ca]), cKDTree(coords[cb])
    pairs = ta.query_ball_tree(tb, CONTACT)
    res_pairs = set()
    for ia, lst in enumerate(pairs):
        for ib in lst:
            res_pairs.add((int(a2r[ca][ia]), int(a2r[cb][ib])))
    na, nb = len(chains[ca]), len(chains[cb])
    mat = np.zeros((na, nb), dtype=bool)
    for ia, ib in res_pairs:
        mat[ia, ib] = True
    ia_res = sorted({i for i, _ in res_pairs})
    ib_res = sorted({j for _, j in res_pairs})
    fig, ax = plt.subplots(figsize=(6.4, 6.0))
    ax.imshow(mat.T, cmap="Blues", origin="lower", aspect="auto", interpolation="nearest")
    ax.set_xlim(min(ia_res) - 8, na + 8)
    ax.set_ylim(min(ib_res) - 8, nb + 8)
    ax.set_xlabel("BRI1 residues (chain A, sequential index)")
    ax.set_ylabel("SERK1 residues (chain C, sequential index)")
    ax.set_title("Fig 189  BRI1-SERK1 interface contact map, heavy atoms < %.1f A" % CONTACT)
    ax.annotate("%d residue pairs, %d BRI1 + %d SERK1 interface residues\n"
                "(axis window cropped to the interface region)"
                % (len(res_pairs), len(ia_res), len(ib_res)),
                (0.02, 0.96), xycoords="axes fraction", fontsize=8)
    fig.tight_layout()
    save(fig, "189_real_4lsx_contactmap.png", mark=MARK)
    return res_pairs, ia_res, ib_res


def fig190_bfactor(chains, coords, bf, a2r, ia_res, ib_res):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    means = {}
    for cid, col, lab, iface in [("A", "#1f77b4", "BRI1 (A)", ia_res),
                                 ("C", "#d62728", "SERK1 (C)", ib_res)]:
        per = np.array([bf[cid][a2r[cid] == i].mean() for i in range(len(chains[cid]))])
        means[cid] = (per.mean(), float(per[iface].mean()))
        ax.plot(range(len(per)), per, lw=0.9, color=col, alpha=0.75, label=lab)
        ax.scatter(iface, per[iface], s=16, color=col, edgecolor="k",
                   linewidth=0.4, zorder=3)
    ax.set_xlabel("Sequential residue index")
    ax.set_ylabel("Mean residue B factor (A^2)")
    ax.set_title("Fig 190  Per-residue B factor, interface residues outlined (dots)")
    ax.annotate("BRI1 mean %.1f, interface %.1f | SERK1 mean %.1f, interface %.1f"
                % (means["A"][0], means["A"][1], means["C"][0], means["C"][1]),
                (0.02, 0.93), xycoords="axes fraction", fontsize=8)
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, "190_real_4lsx_bfactor.png", mark=MARK)
    return means


def fig191_dasa(chains, coords, bf, a2r, elems_of):
    import matplotlib.pyplot as plt
    xyz = np.vstack([coords["A"], coords["C"]])
    el = elems_of["A"] + elems_of["C"]
    asa_complex = asa(xyz, el)
    asa_a = asa(coords["A"], elems_of["A"])
    asa_c = asa(coords["C"], elems_of["C"])
    da = np.concatenate([asa_a - asa_complex[:len(asa_a)],
                         asa_c - asa_complex[len(asa_a):]])
    cid_all = np.array(["A"] * len(asa_a) + ["C"] * len(asa_c))
    a2r_all = np.concatenate([a2r["A"], a2r["C"] + len(chains["A"])])
    na = len(chains["A"])
    res_da = np.zeros(na + len(chains["C"]))
    for v, ci, ri in zip(da, cid_all, a2r_all):
        res_da[ri] += v
    bsa_a = float(res_da[:na].sum())
    bsa_c = float(res_da[na:].sum())
    top = np.argsort(-res_da)[:15]
    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    cols = ["#1f77b4" if t < na else "#d62728" for t in top]
    ax.bar(range(len(top)), res_da[top], color=cols)
    ax.set_xticks(range(len(top)))
    ax.set_xticklabels([("%d" % t) if t < na else ("%d" % (t - na)) for t in top], fontsize=8)
    ax.set_xlabel("Residue index (blue = BRI1 chain A, red = SERK1 chain C)")
    ax.set_ylabel("Buried ASA per residue (A^2)")
    ax.set_title("Fig 191  Top 15 interface residues by buried area, 4LSX")
    ax.annotate("BSA: BRI1 side %.0f A^2, SERK1 side %.0f A^2 (Shrake-Rupley, 92 points)"
                % (bsa_a, bsa_c), (0.98, 0.955), xycoords="axes fraction", fontsize=8,
                ha="right")
    fig.tight_layout()
    save(fig, "191_real_4lsx_dasa.png", mark=MARK)
    return bsa_a, bsa_c, [(int(t) if t < na else int(t - na)) for t in top]


if __name__ == "__main__":
    print("parse PDB...", flush=True)
    with open(PDB) as f:
        txt = f.readlines()
    elems_of = {"A": [], "C": []}
    chains, coords, bf, a2r, het = parse_pdb(PDB)
    for line in txt:
        if line[:6] == "ATOM  " and line[21] in elems_of and line[76:78].strip() != "H":
            elems_of[line[21]].append(line[76:78].strip())
    print("chains:", {c: len(chains[c]) for c in chains}, "het:", het[:3], flush=True)
    print("== 189 contact map ==", flush=True)
    res_pairs, ia, ib = fig189_contact(chains, coords, a2r)
    print("pairs %d, iface A %d B %d" % (len(res_pairs), len(ia), len(ib)), flush=True)
    print("== 190 bfactor ==", flush=True)
    print("means:", fig190_bfactor(chains, coords, bf, a2r, ia, ib), flush=True)
    print("== 191 dasa (慢, 逐原子球面) ==", flush=True)
    bsa = fig191_dasa(chains, coords, bf, a2r, elems_of)
    print("BSA", bsa[:2], "top", bsa[2], flush=True)
    print("DONE ch12e")
