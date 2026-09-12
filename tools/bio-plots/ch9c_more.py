# -*- coding: utf-8 -*-
"""Gallery post 2 - part C: model evaluation, breeding, protein structure."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

from common import save, dump, CAT

rng = np.random.default_rng(99)


# -------------------------------------------------------------------- 67 PR
def pr_curve():
    csv = """sample,label,model_A,model_B
P1,1,0.97,0.90
P2,1,0.94,0.84
P3,1,0.91,0.79
P4,1,0.88,0.72
P5,1,0.85,0.83
P6,1,0.81,0.60
P7,1,0.76,0.66
P8,1,0.71,0.45
P9,1,0.65,0.58
P10,1,0.60,0.51
N1,0,0.42,0.40
N2,0,0.38,0.35
N3,0,0.33,0.55
N4,0,0.29,0.30
N5,0,0.25,0.41
N6,0,0.21,0.24
N7,0,0.17,0.36
N8,0,0.13,0.19
N9,0,0.09,0.12
N10,0,0.05,0.22"""
    dump("67-pr", csv)
    _, c = __import__("common").csv_cols(csv)
    label = np.array([int(v) for v in c["label"]])
    fig, ax = plt.subplots(figsize=(5.8, 5.6))
    for i, m in enumerate(["model_A", "model_B"]):
        order = np.argsort(-np.array(c[m], dtype=float))
        lab = label[order]
        tp = np.cumsum(lab)
        fp = np.cumsum(1 - lab)
        prec = np.r_[1, tp / (tp + fp)]
        rec = np.r_[0, tp / tp[-1]]
        ax.plot(rec, prec, lw=2, color=CAT[i], marker="o", ms=3.5,
                label="%s  AP = %.2f" % (m, np.trapezoid(prec, rec)))
    base = label.mean()
    ax.axhline(base, color="0.6", ls="--", lw=1.1,
               label="no-skill (prevalence = %.1f)" % base)
    ax.set_xlabel("recall (sensitivity)")
    ax.set_ylabel("precision (PPV)")
    ax.set_ylim(0, 1.03)
    ax.set_title("Precision-recall curves, imbalanced setting")
    ax.legend(loc="lower left")
    save(fig, "67-pr")


# --------------------------------------------------------------- 68 confusion
def confusion():
    M = np.array([[52, 4, 1], [6, 38, 5], [2, 7, 45]])
    labels = ["healthy", "dwarf", "wild-type-like"]
    rows = ["true,pred_healthy,pred_dwarf,pred_wildtype"]
    rows += [",".join([l] + [str(v) for v in r]) for l, r in zip(labels, M)]
    dump("68-confusion", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    im = ax.imshow(M, cmap="Blues")
    ax.set_xticks(range(3), ["pred: " + l for l in labels], rotation=15,
                  ha="right", fontsize=9)
    ax.set_yticks(range(3), ["true: " + l for l in labels], fontsize=9)
    ax.grid(False)
    for i in range(3):
        for j in range(3):
            share = M[i, j] / M[i].sum() * 100
            ax.text(j, i, "%d\n(%.0f%%)" % (M[i, j], share), ha="center",
                    va="center", fontsize=9,
                    color="white" if M[i, j] > 30 else "#222")
    fig.colorbar(im, ax=ax, shrink=0.8, label="samples")
    ax.set_title("Confusion matrix, 3-class seedling classifier")
    save(fig, "68-confusion")


# ------------------------------------------------------------------ 69 scree
def scree():
    eig = np.array([3.9, 2.4, 1.3, 0.8, 0.5, 0.4, 0.3, 0.25])
    total = eig.sum()
    rows = ["pc,eigenvalue,var_pct"]
    rows += ["PC%d,%.2f,%.1f" % (i + 1, v, v / total * 100)
             for i, v in enumerate(eig)]
    dump("69-scree", "\n".join(rows))
    x = np.arange(1, 9)
    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    ax.bar(x, eig, color=CAT[0], alpha=0.8, width=0.6)
    ax.axhline(1, color=CAT[3], ls="--", lw=1.2)
    ax.text(7.6, 1.06, "Kaiser criterion (eigenvalue = 1)", fontsize=8.5,
            color=CAT[3], ha="right")
    ax2 = ax.twinx()
    ax2.plot(x, np.cumsum(eig) / total * 100, "-o", color=CAT[1], lw=1.8)
    ax2.set_ylabel("cumulative variance (%)", color=CAT[1])
    ax2.set_ylim(0, 105)
    ax2.spines["right"].set_visible(True)
    ax.annotate("PC1+PC2 = 64%", (2, 3.4), (2.6, 3.7), fontsize=9.5,
                arrowprops=dict(arrowstyle="->", lw=1))
    ax.set_xticks(x, ["PC%d" % i for i in x])
    ax.set_ylabel("eigenvalue")
    ax.set_title("Scree plot: how many PCs to keep")
    save(fig, "69-scree")


# --------------------------------------------------------------- 70 featimp
def featimp():
    feats = [("BZR1_expr", 0.184), ("stem_length", 0.152), ("DWF4_expr", 0.141),
             ("seed_size", 0.118), ("GA20ox_expr", 0.093), ("leaf_angle", 0.072),
             ("brachytic_habit", 0.058), ("CHS_expr", 0.046),
             ("petiole_len", 0.038), ("chlorophyll", 0.031)]
    rows = ["feature,importance"]
    rows += ["%s,%.3f" % f for f in feats]
    dump("70-featimp", "\n".join(rows))
    feats = feats[::-1]
    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    names = [f[0] for f in feats]
    vals = [f[1] for f in feats]
    ax.barh(names, vals, color=CAT[0], alpha=0.85)
    for i, v in enumerate(vals):
        ax.text(v + 0.003, i, "%.3f" % v, va="center", fontsize=8.5)
    ax.set_xlabel("random-forest importance (mean decrease in impurity)")
    ax.set_title("Feature importance for the dwarfism classifier")
    save(fig, "70-featimp")


# ------------------------------------------------------------------ 71 radar
def radar():
    traits = ["yield", "plant_height", "flavonoid", "early_vigor",
              "disease_res", "seed_size"]
    data = {
        "cv_Xia Qiao 1": [0.82, 0.35, 0.74, 0.66, 0.58, 0.80],
        "cv_Yun Qiao 2": [0.74, 0.58, 0.45, 0.72, 0.66, 0.55],
        "cv_local": [0.55, 0.78, 0.60, 0.40, 0.44, 0.62],
    }
    rows = ["trait," + ",".join(data)]
    for i, t in enumerate(traits):
        rows.append("%s,%s" % (t, ",".join("%.2f" % v[i] for v in data.values())))
    dump("71-radar", "\n".join(rows))
    ang = np.linspace(0, 2 * np.pi, len(traits), endpoint=False)
    ang = np.r_[ang, ang[0]]
    fig = plt.figure(figsize=(6.8, 6.2))
    ax = fig.add_subplot(polar=True)
    for i, (name, vals) in enumerate(data.items()):
        v = np.r_[vals, vals[0]]
        ax.plot(ang, v, color=CAT[i], lw=2, label=name)
        ax.fill(ang, v, color=CAT[i], alpha=0.12)
    ax.set_xticks(ang[:-1], traits, fontsize=9.5)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0], ["0.25", "0.5", "0.75", "1"], fontsize=8)
    ax.set_title("Variety comparison across six traits", pad=18)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.16), ncol=3)
    save(fig, "71-radar")


# ---------------------------------------------------------------- 72 gge
def gge():
    envs = ["E1_lowN", "E2_highN", "E3_drought", "E4_irrigated", "E5_lateSown"]
    vars_ = ["V1", "V2", "V3", "V4", "V5", "V6"]
    Y = np.array([
        [3.1, 4.4, 2.8, 4.9, 3.6, 5.1],
        [4.9, 5.2, 4.1, 5.6, 4.4, 5.8],
        [2.2, 3.6, 3.9, 2.6, 4.1, 3.3],
        [5.0, 5.5, 4.3, 5.8, 4.6, 6.0],
        [3.4, 4.1, 4.4, 3.2, 4.6, 3.9],
    ], dtype=float)
    rows = ["environment," + ",".join(vars_)]
    rows += [",".join([e] + ["%.1f" % v for v in r]) for e, r in zip(envs, Y)]
    dump("72-gge", "\n".join(rows))
    M = Y - Y.mean(axis=0)
    U, S, Vt = np.linalg.svd(M, full_matrices=False)
    env_pc = U[:, :2] * S[:2]
    var_pc = Vt.T[:, :2] * S[:2]
    fig, ax = plt.subplots(figsize=(7.4, 6.6))
    for i, v in enumerate(vars_):
        ax.scatter(var_pc[i, 0], var_pc[i, 1], s=64, color=CAT[0],
                   edgecolors="white", zorder=3)
        ax.text(var_pc[i, 0] * 1.12, var_pc[i, 1] * 1.12, v, fontsize=10,
                color=CAT[0], fontweight="bold")
    for j, e in enumerate(envs):
        ax.annotate("", xy=(env_pc[j, 0], env_pc[j, 1]), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color=CAT[3], lw=1.4))
        ax.text(env_pc[j, 0] * 1.14, env_pc[j, 1] * 1.14, e, fontsize=8.5,
                color=CAT[3])
    circ = plt.Circle((0, 0), np.hypot(var_pc[:, 0], var_pc[:, 1]).mean(),
                      fill=False, color=CAT[2], ls="--", lw=1.2)
    ax.add_patch(circ)
    ax.text(0, -np.hypot(var_pc[:, 0], var_pc[:, 1]).mean() - 0.12,
            "mean yield circle", ha="center", fontsize=8.5, color=CAT[2])
    ax.axhline(0, color="0.8", lw=0.8)
    ax.axvline(0, color="0.8", lw=0.8)
    ax.set_xlabel("GGE PC1 (68%)")
    ax.set_ylabel("GGE PC2 (27%)")
    ax.set_title("GGE biplot: arrows = environments, dots = varieties")
    save(fig, "72-gge")


# ---------------------------------------------------------- 73 ramachandran
def ramachandran():
    n = 420
    phi_a, psi_a = rng.normal(-63, 11, n), rng.normal(-43, 10, n)
    phi_b = np.where(rng.uniform(0, 1, n) > 0.5, rng.normal(-120, 16, n),
                     rng.normal(115, 18, n))
    psi_b = rng.normal(128, 16, n)
    phi = np.r_[phi_a, phi_b]
    psi = np.r_[psi_a, psi_b]
    fig, ax = plt.subplots(figsize=(7.0, 6.2))
    for (cx, cy), w, h, col in [
            ([-63, -43], 96, 84, CAT[0]),
            ([-120, 128], 150, 130, CAT[2]),
            ([62, 42], 90, 80, CAT[1])]:
        ax.add_patch(Ellipse((cx, cy), w, h, facecolor=col, alpha=0.10,
                             edgecolor=col, lw=1.1))
    ax.scatter(phi, psi, s=7, color="0.25", alpha=0.55, linewidths=0)
    ax.set_xlim(-180, 180)
    ax.set_ylim(-180, 180)
    ax.set_xticks(range(-180, 181, 60))
    ax.set_yticks(range(-180, 181, 60))
    ax.axhline(0, color="0.75", lw=0.7)
    ax.axvline(0, color="0.75", lw=0.7)
    ax.set_xlabel("phi (degrees)")
    ax.set_ylabel("psi (degrees)")
    ax.set_title("Ramachandran plot, %d residues (simulated)" % len(phi))
    save(fig, "73-ramachandran")


# ------------------------------------------------------------------ 74 rmsd
def rmsd():
    t = np.linspace(0, 10, 40)
    rmsd = 1.2 + 1.9 * (1 - np.exp(-t / 2.4)) + rng.normal(0, 0.07, 40)
    rows = ["time_ns,rmsd_A"]
    rows += ["%.2f,%.2f" % (a, b) for a, b in zip(t, rmsd)]
    dump("74-rmsd", "\n".join(rows))
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.plot(t, rmsd, "-o", ms=3.5, color=CAT[0], alpha=0.75, label="per-frame")
    win = np.convolve(rmsd, np.ones(5) / 5, mode="valid")
    ax.plot(t[4:], win, color=CAT[3], lw=2.2, label="5-frame running mean")
    ax.axhline(rmsd[-8:].mean(), color="0.55", ls=":", lw=1.2)
    ax.text(9.8, rmsd[-8:].mean() + 0.045, "plateau %.2f A" % rmsd[-8:].mean(),
            fontsize=9, color="0.4", ha="right")
    ax.set_xlabel("simulation time (ns)")
    ax.set_ylabel("backbone RMSD (A)")
    ax.set_ylim(0.9, 3.3)
    ax.legend(loc="lower right")
    ax.set_title("MD trajectory: RMSD equilibrates after ~6 ns (simulated)")
    save(fig, "74-rmsd")


if __name__ == "__main__":
    pr_curve()
    confusion()
    scree()
    featimp()
    radar()
    gge()
    ramachandran()
    rmsd()
