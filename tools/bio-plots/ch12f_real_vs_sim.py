# -*- coding: utf-8 -*-
"""ch12f — 真实 vs 模拟对照章（192-195）
左/实线：本篇真实数据；右/虚线：同图型的模拟数据（教学演示）
复用缓存：pca174.npz / ld175.npz / rpk_tissue10002.csv / gwas_pheno292.npz
"""
import os, sys, csv
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import save

HERE = os.path.dirname(os.path.abspath(__file__))
DUMP = os.path.join(HERE, "data_dump", "ch12")
MIX1 = "Left: real 1001 Genomes data. Right: simulated, for teaching only"
MIX2 = "Solid/real: 1001 Genomes data. Dashed/simulated: teaching only"


def fig192_pca():
    import matplotlib.pyplot as plt
    z = np.load(os.path.join(DUMP, "pca174.npz"))
    P, var = z["P"], z["var"]
    rng = np.random.default_rng(11)
    n_pop, n_ind, m = 3, 200, 50000
    freqs = rng.uniform(0.1, 0.9, (n_pop, m))
    G = np.empty((n_pop * n_ind, m), dtype=np.float32)
    for k in range(n_pop):
        G[k * n_ind:(k + 1) * n_ind] = rng.binomial(1, freqs[k], (n_ind, m))
    G -= G.mean(axis=0)
    G /= G.std(axis=0) + 1e-9
    C = G @ G.T / m                       # 合并起来做一次 PCA，三个亚群才会分堆
    w, V = np.linalg.eigh(C)
    Xs = V[:, ::-1][:, :2] * np.sqrt(w[::-1][:2])
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.8))
    axes[0].scatter(P[:, 0], P[:, 1], s=6, c="#1f77b4", alpha=0.4, linewidths=0)
    axes[0].set_title("Real: 1135 accessions (1001 Genomes)")
    axes[0].set_xlabel("PC1 (%.1f%%)" % var[0])
    axes[0].set_ylabel("PC2 (%.1f%%)" % var[1])
    axes[1].scatter(Xs[:, 0], Xs[:, 1], s=6, c="#d62728", alpha=0.4, linewidths=0)
    axes[1].set_title("Simulated: 3 subpopulations x 200")
    axes[1].set_xlabel("PC1")
    axes[1].set_ylabel("PC2")
    for ax in axes:
        ax.set_aspect("equal")
    fig.suptitle("Fig 192  Genotype PCA, real vs simulated", y=1.0)
    fig.tight_layout()
    save(fig, "192_sim_vs_real_pca.png", mark=MIX1)


def fig193_heatmap():
    import matplotlib.pyplot as plt
    with open(os.path.join(DUMP, "rpk_tissue10002.csv")) as f:
        rd = list(csv.reader(f))
    mat = np.array([[float(x) for x in r[1:]] for r in rd[1:]])
    mu = mat.mean(axis=1, keepdims=True)
    sd = mat.std(axis=1, keepdims=True)
    z = (mat - mu) / sd
    rng = np.random.default_rng(12)
    sim = rng.normal(0, 1, z.shape)
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 5.2))
    for ax, M, t, cm in [(axes[0], z, "Real: acc. 10002, 15 genes x 4 tissues", "RdYlBu_r"),
                         (axes[1], sim, "Simulated: same shape, N(0,1)", "RdYlBu_r")]:
        im = ax.imshow(M, cmap=cm, vmin=-2, vmax=2, aspect="auto")
        ax.set_title(t, fontsize=9)
        fig.colorbar(im, ax=ax, shrink=0.7)
    fig.suptitle("Fig 193  Expression heatmap, real vs simulated", y=0.98)
    fig.tight_layout()
    save(fig, "193_sim_vs_real_heatmap.png", mark=MIX1)


def fig194_ld():
    import matplotlib.pyplot as plt
    z = np.load(os.path.join(DUMP, "ld175.npz"))
    mids, means = z["mids"], z["means"]
    rng = np.random.default_rng(13)
    n_hap, n_loci = 600, 400
    rho = 1 / 1500.0
    dist = np.cumsum(rng.uniform(30, 80, n_loci))
    pool1 = rng.binomial(1, 0.5, n_loci)
    pool2 = rng.binomial(1, 0.5, n_loci)
    anc = np.zeros((n_hap, n_loci), dtype=np.int8)
    anc[:, 0] = rng.integers(0, 2, n_hap)
    for i in range(1, n_loci):
        switch = rng.random(n_hap) < 1 - np.exp(-rho * (dist[i] - dist[i - 1]))
        anc[:, i] = np.where(switch, 1 - anc[:, i - 1], anc[:, i - 1])
    H = np.where(anc == 0, pool1, pool2).astype(np.float64)
    H -= H.mean(axis=0)
    H /= H.std(axis=0) + 1e-9
    R = H.T @ H / n_hap
    iu = np.triu_indices(n_loci, k=1)
    d = np.abs(dist[iu[0]] - dist[iu[1]])
    r2 = R[iu] ** 2
    edges = np.array([50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000])
    s_mids, s_means = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        k = (d >= a) & (d < b)
        s_mids.append(np.sqrt(a * b))
        s_means.append(r2[k].mean())
    fig, ax = plt.subplots(figsize=(6.8, 4.8))
    ax.plot(mids, means, "o-", color="#d62728", lw=2, label="Real: Chr1, 1001 Genomes")
    ax.plot(s_mids, s_means, "s--", color="#7f7f7f", lw=2,
            label="Simulated: ancestry-switch haplotypes")
    ax.set_xscale("log")
    ax.set_xlabel("Distance (bp, log)")
    ax.set_ylabel("Mean r2 in bin")
    ax.set_title("Fig 194  LD decay, real vs simulated")
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, "194_sim_vs_real_ld.png", mark=MIX2)
    return float(means[0]), float(s_means[0]), float(means[-1]), float(s_means[-1])


def fig195_qq():
    import matplotlib.pyplot as plt
    z = np.load(os.path.join(DUMP, "gwas_pheno292.npz"))
    p = z["p"]
    pv = np.sort(p[(p > 0) & (p < 1)])
    n = len(pv)
    exp_q = -np.log10(np.arange(1, n + 1) / (n + 1))
    obs = -np.log10(pv)
    rng = np.random.default_rng(14)
    p_sim = np.sort(rng.uniform(1e-12, 1, n))
    obs_sim = -np.log10(p_sim)
    fig, ax = plt.subplots(figsize=(5.8, 5.4))
    ax.scatter(exp_q, obs_sim, s=4, c="#7f7f7f", alpha=0.5, linewidths=0,
               label="Simulated: uniform null")
    ax.scatter(exp_q, obs, s=4, c="#1f77b4", alpha=0.5, linewidths=0,
               label="Real: root length GWAS")
    lim = max(obs.max(), exp_q.max()) * 1.05
    ax.plot([0, lim], [0, lim], "k--", lw=1)
    ax.set_xlabel("Expected -log10(p)")
    ax.set_ylabel("Observed -log10(p)")
    ax.set_title("Fig 195  QQ plot, real vs simulated null")
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    save(fig, "195_sim_vs_real_qq.png", mark=MIX2)
    return float(obs.max()), float(obs_sim.max())


if __name__ == "__main__":
    print("== 192 PCA ==", flush=True)
    fig192_pca()
    print("== 193 heatmap ==", flush=True)
    fig193_heatmap()
    print("== 194 LD ==", flush=True)
    r = fig194_ld()
    print("first/last bin means real vs sim:", np.round(r, 3), flush=True)
    print("== 195 QQ ==", flush=True)
    print("max -log10p real vs sim:", fig195_qq(), flush=True)
    print("DONE ch12f")
