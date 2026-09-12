# -*- coding: utf-8 -*-
"""ch12a — 真实群体遗传图（174-178）
数据：1001 Genomes GMI-MPI v3.1 imputed SNP matrix (HDF5, TAIR10 坐标)
     positions / positions.attrs['chr_regions'] / snps (SNP x accession, 0/1) / accessions
国家：acc.json (pk = h5 accession id = bigWig id = AraPheno accession_id，同一 id 空间)
"""
import os, sys, csv
import numpy as np
import h5py

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import save

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data-real")
DUMP = os.path.join(HERE, "data_dump", "ch12")
os.makedirs(DUMP, exist_ok=True)
MARK = "Real data: 1001 Genomes GMI-MPI v3.1 SNP matrix"
NCHUNK = 100000  # 内存友好：100k x 1135 的 uint8 块仅 ~110 MB


def country_map():
    out = {}
    with open(os.path.join(DATA, "acc.json")) as f:
        for r in csv.DictReader(f):
            out[int(r["pk"])] = r["country"]
    return out


H5DIR = os.path.join(DATA, "1001_SNP_MATRIX")


def load_meta():
    f = h5py.File(os.path.join(H5DIR, "imputed_snps_binary.hdf5"), "r")
    pos = f["positions"][:]
    regions = f["positions"].attrs["chr_regions"]
    accs = np.array([int(a) for a in f["accessions"][:]])
    return f, pos, regions, accs


def af_scan(f):
    """分块扫描全部 SNP 的 alt 频率 -> npz 缓存（af 值与行号）。10.7M 行只扫一遍。"""
    cache = os.path.join(DUMP, "af_all.npz")
    if os.path.exists(cache):
        z = np.load(cache)
        return z["af"]
    snps = f["snps"]
    n = snps.shape[1]
    af = np.empty(snps.shape[0], dtype=np.float32)
    for s in range(0, snps.shape[0], NCHUNK):
        e = min(s + NCHUNK, snps.shape[0])
        blk = snps[s:e, :]
        af[s:e] = blk.sum(axis=1, dtype=np.float32) / n  # 避免 uint8 mean 的 float64 放大
        if (s // NCHUNK) % 20 == 0:
            print("  af scan %d/%d" % (e, snps.shape[0]), flush=True)
    np.savez_compressed(cache, af=af)
    return af


def fetch_rows(f, idx):
    """按行号取基因型（要求严格升序，保证返回行与 idx 对齐），(m, n_acc) float32"""
    snps = f["snps"]
    if not np.all(np.diff(idx) > 0):
        raise ValueError("fetch_rows requires strictly ascending idx")
    out = np.empty((len(idx), snps.shape[1]), dtype=np.float32)
    step = 50000
    for s in range(0, len(idx), step):
        e = min(s + step, len(idx))
        out[s:e, :] = snps[idx[s:e], :]
    return out


def pick_maf_snps(af, lo=0.05, hi=0.95, target=80000, seed=7):
    rng = np.random.default_rng(seed)
    cand = np.flatnonzero((af >= lo) & (af <= hi))
    if len(cand) > target:
        sel = rng.choice(cand, size=target, replace=False)
        sel = np.sort(sel)
    else:
        sel = cand
    return sel


def fig174_pca(f, af, accs, cm):
    import matplotlib.pyplot as plt
    idx = pick_maf_snps(af)
    print("  PCA on %d SNPs" % len(idx), flush=True)
    n = len(accs)
    grm = np.zeros((n, n), dtype=np.float64)
    step = 50000
    for s in range(0, len(idx), step):
        blk = fetch_rows(f, idx[s:s + step])
        blk -= blk.mean(axis=1, keepdims=True)
        grm += blk.T @ blk
    grm /= len(idx)
    w, V = np.linalg.eigh(grm)
    P = V[:, ::-1][:, :2] * np.sqrt(w[::-1][:2])
    countries = np.array([cm.get(int(a), "?") for a in accs])
    top = [c for c in np.unique(countries) if c != "?" and (countries == c).sum() >= 50]
    order = sorted(top, key=lambda c: -(countries == c).sum())[:6]
    CCOL = ["#1f77b4", "#d62728", "#2ca02c", "#ff7f0e", "#9467bd", "#8c564b"]
    fig, ax = plt.subplots(figsize=(7.2, 5.6))
    rest = ~np.isin(countries, order)
    ax.scatter(P[rest, 0], P[rest, 1], s=8, color="#c7c7c7", alpha=0.6,
               label="other n=%d" % rest.sum(), linewidths=0)
    for c, col in zip(order, CCOL):
        m = countries == c
        ax.scatter(P[m, 0], P[m, 1], s=14, color=col, alpha=0.85,
                   label="%s n=%d" % (c, m.sum()), linewidths=0)
    var = w[::-1][:2] / np.sum(w) * 100
    ax.set_xlabel("PC1 (%.1f%%)" % var[0])
    ax.set_ylabel("PC2 (%.1f%%)" % var[1])
    ax.set_title("Fig 174  Genotype PCA, %d accessions x %d SNPs (MAF 5-95%%)"
                 % (n, len(idx)))
    ax.legend(fontsize=8, markerscale=1.6)
    fig.tight_layout()
    save(fig, "174_real_pca.png", mark=MARK)
    np.savez_compressed(os.path.join(DUMP, "pca174.npz"), P=P, var=var)
    return var, order


def fig175_ld(f, af, pos, regions):
    import matplotlib.pyplot as plt
    c0s, c0e = regions[0]  # Chr1 的行号区间（注意：不是坐标！）
    rows = np.arange(c0s, c0e)
    mm = rows[(af[rows] >= 0.05) & (af[rows] <= 0.95) & (pos[rows] < 5000000)]
    sub = mm[::max(1, len(mm) // 2500)][:2500]
    X = fetch_rows(f, sub)
    X -= X.mean(axis=1, keepdims=True)
    sd = X.std(axis=1, keepdims=True)
    sd[sd == 0] = 1
    Xs = X / sd
    R = Xs @ Xs.T / Xs.shape[1]
    iu = np.triu_indices(len(sub), k=1)
    d = np.abs(pos[sub[iu[0]]].astype(np.int64) - pos[sub[iu[1]]].astype(np.int64))
    r2 = R[iu] ** 2
    keep = (d >= 50) & (d < 20000)
    d, r2 = d[keep], r2[keep]
    edges = np.array([50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000])
    mids, means = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        k = (d >= a) & (d < b)
        mids.append(np.sqrt(a * b))
        means.append(r2[k].mean())
    fig, ax = plt.subplots(figsize=(6.8, 4.8))
    ax.scatter(d, r2, s=3, alpha=0.08, color="#1f77b4", linewidths=0)
    ax.plot(mids, means, "o-", color="#d62728", lw=2, ms=5)
    ax.set_xscale("log")
    ax.set_xlabel("Distance between SNPs on Chr1 (bp, log)")
    ax.set_ylabel("r2 (LD)")
    ax.set_title("Fig 175  LD decay, Chr1 first 5 Mb, %d SNPs x %d accessions"
                 % (len(sub), X.shape[1]))
    ax.annotate("mean r2 in distance bins (red)", (0.03, 0.9), xycoords="axes fraction",
                fontsize=8, color="#d62728")
    fig.tight_layout()
    save(fig, "175_real_ld_decay.png", mark=MARK)
    np.savez_compressed(os.path.join(DUMP, "ld175.npz"), mids=mids, means=means)
    return mids, means


def fig176_fst(f, af, pos, regions, accs, cm):
    import matplotlib.pyplot as plt
    countries = np.array([cm.get(int(a), "?") for a in accs])
    counts = {c: int((countries == c).sum()) for c in np.unique(countries) if c != "?"}
    g1, g2 = sorted(counts, key=lambda c: -counts[c])[:2]
    m1, m2 = countries == g1, countries == g2
    c0s, c0e = regions[0]                  # Chr1 行号区间
    rows = np.arange(c0s, c0e)
    win = 100000
    edges = np.arange(pos[rows][0], pos[rows][-1] + win, win)
    centers, vals = [], []
    snps = f["snps"]
    for a, b in zip(edges[:-1], edges[1:]):
        idx = rows[(pos[rows] >= a) & (pos[rows] < b) &
                   (af[rows] >= 0.05) & (af[rows] <= 0.95)]
        if len(idx) < 20:
            continue
        blk = snps[np.sort(idx), :]
        p1 = blk[:, m1].mean(axis=1)
        p2 = blk[:, m2].mean(axis=1)
        ht = 2 * ((p1 + p2) / 2) * (1 - (p1 + p2) / 2)
        hs = (2 * p1 * (1 - p1) + 2 * p2 * (1 - p2)) / 2
        ok = ht > 0
        fst = (ht[ok] - hs[ok]) / ht[ok]
        centers.append((a + b) / 2 / 1e6)
        vals.append(fst.mean())
    centers, vals = np.array(centers), np.array(vals)
    thr = np.percentile(vals, 95)
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    ax.plot(centers, vals, lw=0.8, color="#1f77b4")
    ax.axhline(vals.mean(), color="k", ls="--", lw=1, label="genome-wide mean %.3f" % vals.mean())
    ax.axhline(thr, color="#d62728", ls=":", lw=1, label="95th pct %.3f" % thr)
    ax.set_xlabel("Position on Chr1 (Mb)")
    ax.set_ylabel("Fst (100 kb windows)")
    ax.set_title("Fig 176  %s (n=%d) vs %s (n=%d), Chr1" % (g1, m1.sum(), g2, m2.sum()))
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, "176_real_fst_chr1.png", mark=MARK)
    return g1, g2, centers, vals, thr


def fig177_sfs(af, n_acc):
    import matplotlib.pyplot as plt
    mac = np.minimum(af, 1 - af)
    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    cnt, edges, _ = ax.hist(mac, bins=1000, range=(0, 0.5), color="#1f77b4")
    ax.set_yscale("log")
    ax.set_xlim(0, 0.1)
    ax.set_xlabel("Minor allele frequency")
    ax.set_ylabel("Number of SNPs (log)")
    k = mac * n_acc
    singletons = int(((k >= 0.5) & (k < 1.5)).sum())
    ax.set_title("Fig 177  Folded SFS (minor allele frequency), all 10.7 M SNPs")
    ax.annotate("singleton-dominated: rare variants far exceed neutral 1/f line",
                (0.3, 0.9), xycoords="axes fraction", fontsize=8)
    fig.tight_layout()
    save(fig, "177_real_sfs.png", mark=MARK)
    return singletons, int((mac > 0).sum())


def fig178_density(pos, regions):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8.2, 3.6))
    colors = ["#1f77b4", "#d62728", "#2ca02c", "#ff7f0e", "#9467bd"]
    ymax = 0
    for ci in range(5):
        s, e = regions[ci]                 # 行号区间
        p = pos[s:e]                       # 该染色体的全部坐标
        w = np.arange(p[0], p[-1] + 1000000, 1000000)
        h, _ = np.histogram(p, bins=w)
        dens = h / 1000.0
        ymax = max(ymax, dens.max())
        ax.fill_between(w[:-1] / 1e6, ci * 22, ci * 22 + dens, step="post",
                        color=colors[ci], alpha=0.75, lw=0)
        ax.text(w[0] / 1e6, ci * 22 + 8, "Chr%d" % (ci + 1), fontsize=8)
    ax.set_xlabel("Position (Mb)")
    ax.set_ylabel("SNPs per kb (window 1 Mb)")
    ax.set_title("Fig 178  SNP density across the 5 chromosomes")
    ax.set_ylim(-2, 5 * 22 + 2)
    ax.set_yticks([])
    fig.tight_layout()
    save(fig, "178_real_snp_density.png", mark=MARK)
    return ymax


if __name__ == "__main__":
    cm = country_map()
    f, pos, regions, accs = load_meta()
    print("accessions:", len(accs), "snps:", len(pos), flush=True)
    af = af_scan(f)
    print("af done", flush=True)
    print("== 174 PCA ==", flush=True)
    var, order = fig174_pca(f, af, accs, cm)
    print("PC1 %.1f%% PC2 %.1f%%, top countries: %s" % (var[0], var[1], order), flush=True)
    print("== 175 LD ==", flush=True)
    mids, means = fig175_ld(f, af, pos, regions)
    print("LD bin means: %s" % np.round(means, 3), flush=True)
    print("== 176 Fst ==", flush=True)
    g1, g2, centers, vals, thr = fig176_fst(f, af, pos, regions, accs, cm)
    print("groups %s(n) vs %s(n), max Fst %.3f at %.2f Mb" %
          (g1, g2, vals.max(), centers[vals.argmax()]), flush=True)
    print("== 177 SFS ==", flush=True)
    singles, ntot = fig177_sfs(af, len(accs))
    print("singletons %d / %d" % (singles, ntot), flush=True)
    print("== 178 density ==", flush=True)
    print("max density %.1f SNPs/kb" % fig178_density(pos, regions), flush=True)
    print("DONE ch12a")
