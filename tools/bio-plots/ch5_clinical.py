# -*- coding: utf-8 -*-
"""Chapter 5 - model/clinical style figures: ROC, KM, DCA, forest plot."""
import numpy as np
import matplotlib.pyplot as plt

from common import save, dump, csv_cols, num, CAT

rng = np.random.default_rng(11)


# --------------------------------------------------------------------- 19 ROC
def roc():
    csv = """sample,label,model_A,model_B,model_C
P1,1,0.97,0.91,0.58
P2,1,0.94,0.83,0.22
P3,1,0.91,0.88,0.71
P4,1,0.88,0.64,0.35
P5,1,0.85,0.79,0.62
P6,1,0.81,0.72,0.15
P7,1,0.76,0.58,0.83
P8,1,0.71,0.45,0.48
P9,1,0.65,0.81,0.29
P10,1,0.60,0.52,0.66
N1,0,0.42,0.49,0.77
N2,0,0.38,0.35,0.11
N3,0,0.33,0.61,0.52
N4,0,0.29,0.28,0.05
N5,0,0.25,0.40,0.90
N6,0,0.21,0.22,0.38
N7,0,0.17,0.31,0.44
N8,0,0.13,0.18,0.59
N9,0,0.09,0.12,0.03
N10,0,0.05,0.26,0.74"""
    dump("19-roc", csv)
    _, c = csv_cols(csv)
    label = np.array([int(v) for v in c["label"]])

    fig, ax = plt.subplots(figsize=(5.8, 5.6))
    for i, m in enumerate(["model_A", "model_B", "model_C"]):
        score = num(c, m)
        order = np.argsort(-score)
        lab = label[order]
        tp = np.cumsum(lab)
        fp = np.cumsum(1 - lab)
        tpr = np.r_[0, tp / tp[-1]]
        fpr = np.r_[0, fp / fp[-1]]
        auc = np.trapezoid(tpr, fpr)
        ax.plot(fpr, tpr, color=CAT[i], lw=2, label="%s  AUC = %.2f" % (m, auc))
    ax.plot([0, 1], [0, 1], color="0.6", ls="--", lw=1.2, label="chance (AUC = 0.50)")
    ax.set_xlabel("false positive rate = FP / (FP + TN)")
    ax.set_ylabel("true positive rate = TP / (TP + FN)")
    ax.set_title("ROC curves under three models")
    ax.legend(loc="lower right")
    save(fig, "19-roc")


# ---------------------------------------------------------------------- 20 KM
def km():
    csv = """patient,group,time_weeks,event
T1,treated,4,1
T2,treated,7,1
T3,treated,10,0
T4,treated,13,1
T5,treated,16,0
T6,treated,19,1
T7,treated,22,1
T8,treated,25,0
T9,treated,28,0
T10,treated,30,0
C1,control,2,1
C2,control,4,1
C3,control,5,0
C4,control,7,1
C5,control,9,1
C6,control,11,1
C7,control,12,0
C8,control,14,1
C9,control,16,1
C10,control,18,0"""
    dump("20-km", csv)
    _, c = csv_cols(csv)

    def curve(group):
        m = np.array(c["group"]) == group
        t = num(c, "time_weeks")[m]
        e = np.array([int(v) for v in c["event"]])[m]
        order = np.argsort(t)
        t, e = t[order], e[order]
        n = len(t)
        s = 1.0
        times, surv = [0.0], [1.0]
        cens_x, cens_y = [], []
        for i in range(n):
            at_risk = int(np.sum(t >= t[i]))
            if e[i] == 1:
                s *= 1 - 1 / at_risk
                times += [t[i], t[i]]
                surv += [surv[-1], s]
            else:
                cens_x.append(t[i])
                cens_y.append(s)
        times.append(t.max() + 1)
        surv.append(s)
        return times, surv, cens_x, cens_y

    fig, ax = plt.subplots(figsize=(6.6, 5.2))
    for i, (g, col) in enumerate([("treated", CAT[2]), ("control", CAT[3])]):
        times, surv, cx, cy = curve(g)
        ax.step(times, surv, where="post", color=col, lw=2.2, label=g)
        ax.scatter(cx, cy, marker="+", s=64, color=col, linewidths=1.6, zorder=3)
    ax.set_xlabel("time (weeks)")
    ax.set_ylabel("survival probability")
    ax.set_ylim(0, 1.05)
    ax.set_title("Kaplan-Meier survival curves (log-rank p = 0.032)")
    ax.text(0.98, 0.5, "+ = censored", transform=ax.transAxes, ha="right", fontsize=9.5,
            color="0.3")
    ax.legend(loc="lower left")
    save(fig, "20-km")


# --------------------------------------------------------------------- 21 DCA
def dca():
    thr = np.round(np.arange(0.1, 0.95, 0.1), 1)
    prevalence = 0.2
    treat_all = prevalence - thr / (1 - thr)
    model_nb = np.array([0.062, 0.096, 0.118, 0.126, 0.124, 0.113, 0.094, 0.068, 0.038])
    csv = "threshold,model_net_benefit,treat_all,treat_none\n"
    csv += "\n".join("%.1f,%.3f,%.3f,0.000" % (t, m, a)
                     for t, m, a in zip(thr, model_nb, treat_all))
    dump("21-dca", csv)

    fig, ax = plt.subplots(figsize=(6.8, 5.2))
    ax.plot(thr, model_nb, color=CAT[0], lw=2.2, marker="o", ms=4, label="prediction model")
    ax.plot(thr, treat_all, color=CAT[1], lw=2, ls="--", label="treat all")
    ax.axhline(0, color="0.55", lw=1.4, ls=":", label="treat none")
    ax.set_xlabel("threshold probability")
    ax.set_ylabel("net benefit")
    ax.set_title("Decision curve analysis (prevalence = 20%)")
    ax.set_ylim(-0.12, 0.22)
    ax.legend()
    ax.text(0.98, 0.60, "model wins where its curve\nis above both defaults",
            transform=ax.transAxes, ha="right", fontsize=9.5, color="0.3")
    save(fig, "21-dca")


# ----------------------------------------------------------------- 22 forest
def forest():
    csv = """study,or,low,high,weight_pct
S1,1.35,0.92,1.98,4.2
S2,1.62,1.10,2.39,5.1
S3,0.88,0.55,1.41,6.3
S4,1.44,1.02,2.03,6.8
S5,1.71,1.22,2.39,7.4
S6,1.28,0.79,2.07,4.8
S7,1.93,1.35,2.76,6.0
S8,1.55,1.08,2.22,6.9
summary,1.45,1.26,1.67,100.0"""
    dump("22-forest", csv)
    _, c = csv_cols(csv)
    names = c["study"]
    orr = num(c, "or")
    lo, hi = num(c, "low"), num(c, "high")
    w = num(c, "weight_pct")

    fig, ax = plt.subplots(figsize=(7.4, 5.4))
    ys = np.arange(len(names))[::-1]
    for i, y in zip(range(len(names) - 1), ys[:-1]):
        ax.plot([lo[i], hi[i]], [y, y], color="0.35", lw=1.4)
        ax.scatter(orr[i], y, s=w[i] * 26, color=CAT[0], edgecolors="0.2", zorder=3)
    # diamond for the pooled estimate
    si = len(names) - 1
    ax.fill([lo[si], orr[si], hi[si], orr[si]], [ys[-1], ys[-1] + 0.28, ys[-1], ys[-1] - 0.28],
            color=CAT[3], edgecolor="0.2", zorder=3)
    ax.axvline(1, color="0.5", ls="--", lw=1.2)
    ax.text(1.03, 7.5, "OR = 1 (no effect)", fontsize=8.5, color="0.4")
    ax.set_yticks(ys, names)
    ax.set_xscale("log")
    ticks = [0.5, 0.75, 1, 1.5, 2, 3]
    ax.set_xticks(ticks, ["0.5", "0.75", "1", "1.5", "2", "3"])
    ax.minorticks_off()
    ax.set_xlabel("odds ratio (log scale)")
    ax.set_title("Forest plot: 8 studies + random-effects summary")
    ax.text(0.02, 0.03, "square area = study weight", transform=ax.transAxes, fontsize=9,
            color="0.35")
    save(fig, "22-forest")


if __name__ == "__main__":
    roc()
    km()
    dca()
    forest()
