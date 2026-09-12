# -*- coding: utf-8 -*-
"""ch12b — 真实 GWAS 图（179-182）
数据：1001 Genomes v3.1 SNP matrix（TAIR10 坐标）+ AraPheno 表型 292（4 天根长，127 份）
基因：Ensembl Plants TAIR10 GFF3（TAIR10 坐标，与 SNP 矩阵同坐标系）
"""
import os, sys, csv, gzip
import numpy as np
import h5py
from scipy import stats as sstats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import save

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data-real")
DUMP = os.path.join(HERE, "data_dump", "ch12")
os.makedirs(DUMP, exist_ok=True)
MARK = "Real data: 1001 Genomes SNP matrix + AraPheno GT pheno 292"
NCHUNK = 200000  # 200k x 127 float32 ~100 MB，内存友好


def load_pheno(accs_h5):
    acc2val, meta, latmap = {}, {}, {}
    with open(os.path.join(DATA, "pheno292.txt")) as f:
        for r in csv.DictReader(f):
            aid = int(r["accession_id"])
            acc2val[aid] = float(r["phenotype_value"])
            meta[aid] = r["accession_country"]
            try:
                latmap[aid] = float(r["accession_latitude"])
            except (KeyError, ValueError):
                latmap[aid] = np.nan
    cols, vals, ctry, lat = [], [], [], []
    for j, a in enumerate(accs_h5):
        if int(a) in acc2val:
            cols.append(j)
            vals.append(acc2val[int(a)])
            ctry.append(meta[int(a)])
            lat.append(latmap[int(a)])
    return np.array(cols), np.array(vals), np.array(ctry), np.array(lat)


def gwas_scan(f, cols, y):
    """全基因组分块线性回归 SNP ~ 根长；返回 beta, t, p（缓存 npz）"""
    cache = os.path.join(DUMP, "gwas_pheno292.npz")
    if os.path.exists(cache):
        z = np.load(cache)
        return z["beta"], z["t"], z["p"]
    snps = f["snps"]
    n = len(cols)
    yc = y - y.mean()
    syy = float(yc @ yc)
    beta = np.empty(snps.shape[0], dtype=np.float32)
    tstat = np.empty(snps.shape[0], dtype=np.float32)
    pval = np.empty(snps.shape[0], dtype=np.float32)
    for s in range(0, snps.shape[0], NCHUNK):
        e = min(s + NCHUNK, snps.shape[0])
        X = snps[s:e, cols].astype(np.float32)
        xc = X - X.mean(axis=1, keepdims=True)
        sxx = (xc * xc).sum(axis=1)
        b = (xc @ yc) / np.maximum(sxx, 1e-9)
        ssr = sxx * b * b                      # 回归平方和
        sse = syy - ssr                        # 残差平方和（已中心化）
        r2 = np.clip(ssr / syy, 0, 1)
        with np.errstate(invalid="ignore", divide="ignore"):
            t = b * np.sqrt((n - 2) * sxx / np.maximum(sse, 1e-9))
        p = 2 * sstats.t.sf(np.abs(t), n - 2)
        afc = X.mean(axis=1)                   # 127 份内的 alt 频率
        maf_ok = (afc >= 0.05) & (afc <= 0.95)
        p = np.where(maf_ok, p, 1.0)           # 未过 MAF 过滤的位点记 p=1
        beta[s:e], tstat[s:e], pval[s:e] = b, t, p
        if (s // NCHUNK) % 5 == 0:
            print("  gwas %d/%d" % (e, snps.shape[0]), flush=True)
    np.savez_compressed(cache, beta=beta, t=tstat, p=pval)
    return beta, tstat, pval


def parse_tair10_genes(lo, hi, chr_name):
    """Ensembl GFF3: TAIR10 基因 (region 内) -> [(start,end,strand,name)]
    Ensembl 的 seqid 是 '1'..'5'，入参 'Chr4' 需要剥前缀"""
    chr_num = chr_name.replace("Chr", "")
    path = os.path.join(DATA, "tair10_gff.gz")
    out = []
    with gzip.open(path, "rt") as f:
        for line in f:
            if line[0] == "#":
                continue
            p = line.split("\t")
            if p[2] != "gene" or p[0] != chr_num:
                continue
            s, e = int(p[3]), int(p[4])
            if e < lo or s > hi:
                continue
            attrs = p[8]
            name = attrs.split("gene_id=")[-1].split(";")[0].strip()
            out.append((s, e, p[6], name))
    return out


def fig179_pheno(y, ctry, lat):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    ax.scatter(lat, y, s=26, color="#1f77b4", alpha=0.75,
               edgecolor="k", linewidth=0.4)
    ok = ~np.isnan(lat)
    k, b = np.polyfit(lat[ok], y[ok], 1)
    r = float(np.corrcoef(lat[ok], y[ok])[0, 1])
    xs = np.array([np.nanmin(lat[ok]), np.nanmax(lat[ok])])
    ax.plot(xs, k * xs + b, "--", color="#d62728", lw=1.6,
            label="linear fit: %.2f cm/deg, r = %.2f" % (k, r))
    ax.set_xlabel("Collection latitude (deg N)")
    ax.set_ylabel("Root length day 4 (cm)")
    ax.set_title("Fig 179  Root length vs collection latitude (AraPheno GT292)")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    save(fig, "179_real_pheno_by_country.png", mark=MARK)
    return float(k), r, int(ok.sum()), float(y.mean()), float(y.std())


def fig180_manhattan(p, pos, regions, n_acc):
    import matplotlib.pyplot as plt
    m = p < 1
    nl = -np.log10(p[m])
    xs, cols, ticks = [], [], []
    off = 0
    for ci in range(5):
        s, e = regions[ci]                     # 行号区间（不是坐标！）
        rows = np.arange(s, e)
        k = rows[m[rows]]
        x = off + (pos[k] - pos[rows][0]) / 1e6
        xs.append(x)
        cols.append(np.full(len(k), "#1f77b4" if ci % 2 == 0 else "#6baed6"))
        ticks.append((off + (pos[rows][-1] - pos[rows][0]) / 2e6, ci + 1))
        off = (x.max() if len(x) else off) + 4
    xs = np.concatenate(xs)
    cols = np.concatenate(cols)
    M = int(m.sum())
    bonf = -np.log10(0.05 / M)
    imax = int(nl.argmax())
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    ax.scatter(xs, nl, s=2.5, c=cols, linewidths=0)
    ax.axhline(bonf, color="#d62728", ls="--", lw=1,
               label="Bonferroni 0.05 (%.1f)" % bonf)
    ax.scatter([xs[imax]], [nl[imax]], s=40, facecolor="none", edgecolor="#d62728", lw=1.4)
    ax.annotate("top -log10p=%.1f" % nl[imax], (xs[imax], nl[imax]),
                textcoords="offset points", xytext=(6, 4), fontsize=8, color="#d62728")
    ax.set_xticks([t[0] for t in ticks])
    ax.set_xticklabels(["Chr%d" % t[1] for t in ticks])
    ax.set_xlabel("Chromosome (Mb, concatenated)")
    ax.set_ylabel("-log10(p)")
    ax.set_title("Fig 180  GWAS Manhattan, root length day 4, %d accessions x %d SNPs"
                 % (n_acc, M))
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    save(fig, "180_real_manhattan.png", mark=MARK)
    return M, bonf, float(nl.max())


def fig181_qq(p):
    import matplotlib.pyplot as plt
    pv = np.sort(p[p < 1])
    n = len(pv)
    exp_q = -np.log10(np.arange(1, n + 1) / (n + 1))
    obs_q = -np.log10(pv)
    lam = float(np.median(sstats.chi2.isf(pv, 1)) / sstats.chi2.isf(0.5, 1))
    fig, ax = plt.subplots(figsize=(5.4, 5.0))
    ax.scatter(exp_q, obs_q, s=5, color="#1f77b4", alpha=0.6, linewidths=0)
    lim = max(exp_q.max(), obs_q.max()) * 1.05
    ax.plot([0, lim], [0, lim], "k--", lw=1)
    ax.set_xlabel("Expected -log10(p)")
    ax.set_ylabel("Observed -log10(p)")
    ax.set_title("Fig 181  QQ plot, root length GWAS")
    ax.annotate("genomic inflation lambda = %.2f" % lam, (0.05, 0.9),
                xycoords="axes fraction", fontsize=9)
    fig.tight_layout()
    save(fig, "181_real_qq.png", mark=MARK)
    return lam


def fig182_region(f, pos, regions, beta, p, top_idx):
    import matplotlib.pyplot as plt
    ti = top_idx
    chr_name = "Chr?"
    for ci in range(5):
        s, e = regions[ci]                     # 行号区间
        if s <= ti < e:
            chr_name = "Chr%d" % (ci + 1)
            break
    lo, hi = pos[ti] - 50000, pos[ti] + 50000
    idx = np.flatnonzero((pos >= lo) & (pos < hi))
    X = f["snps"][idx, :]
    j = int(np.flatnonzero(idx == ti)[0])       # 顶尖 SNP 在 region 行里的位置
    xv = X[j, :].astype(np.float32)
    Xc = X - X.mean(axis=1, keepdims=True)
    xv = xv - xv.mean()
    sxx = (Xc * Xc).sum(axis=1)
    r = (Xc @ xv) / np.sqrt(np.maximum(sxx * (xv @ xv), 1e-36))
    r2 = np.clip(r * r, 0, 1)
    d = pos[np.sort(idx)]
    nl = -np.log10(np.maximum(p[np.sort(idx)], 1e-300))
    genes = parse_tair10_genes(lo, hi, chr_name)
    order = np.argsort(-r2)
    fig, (ax, axg) = plt.subplots(2, 1, figsize=(8.6, 5.0), sharex=True,
                                  gridspec_kw={"height_ratios": [3.4, 1], "hspace": 0.08})
    ax.scatter(d[order] / 1e3, nl[order], s=14, linewidths=0,
               c=np.clip(r2[order], 0, 1), cmap="Blues", vmin=0, vmax=1)
    ax.axvline(pos[ti] / 1e3, color="#d62728", ls=":", lw=1)
    ax.set_ylabel("-log10(p)")
    ax.set_title("Fig 182  Region plot +/-50 kb of top SNP (r2 shading), %s:%d" % (chr_name, pos[ti]))
    for s, e, strand, name in genes:
        ycol = "#2ca02c"
        axg.hlines(0.6, s / 1e3, e / 1e3, color=ycol, lw=6)
        xd = (e / 1e3 + 0.6) if strand == "+" else (s / 1e3 - 0.6)
        axg.annotate(name, (xd, 0.6), fontsize=6.5, va="center",
                     ha="left" if strand == "+" else "right")
    axg.set_ylim(0, 1)
    axg.set_yticks([])
    axg.set_xlabel("Position on %s (kb)" % chr_name)
    fig.tight_layout()
    save(fig, "182_real_region.png", mark=MARK)
    return chr_name, int(pos[ti]), len(genes)


if __name__ == "__main__":
    fh5 = h5py.File(os.path.join(DATA, "1001_SNP_MATRIX", "imputed_snps_binary.hdf5"), "r")
    pos = fh5["positions"][:]
    regions = fh5["positions"].attrs["chr_regions"]
    accs = np.array([int(a) for a in fh5["accessions"][:]])
    cols, y, ctry, lat = load_pheno(accs)
    print("pheno accessions in matrix:", len(cols), flush=True)
    print("== 179 pheno ==", flush=True)
    slope, pr, nph, mu, sd = fig179_pheno(y, ctry, lat)
    print("latitude cline: slope %.3f cm/deg, r=%.3f, n=%d, mean %.2f sd %.2f"
          % (slope, pr, nph, mu, sd), flush=True)
    print("== GWAS scan ==", flush=True)
    beta, t, p = gwas_scan(fh5, cols, y)
    ok = (p > 0) & (p < 1) & np.isfinite(p)
    print("valid p (MAF-filtered): %d, min p %.3g" % (int(ok.sum()), float(p[ok].min())), flush=True)
    print("== 180 Manhattan ==", flush=True)
    M, bonf, nmax = fig180_manhattan(np.where(ok, p, 1.0), pos, regions, len(cols))
    print("M=%d bonf=%.1f top=%.1f" % (M, bonf, nmax), flush=True)
    print("== 181 QQ ==", flush=True)
    lam = fig181_qq(np.where(ok, p, 1.0))
    print("lambda %.3f" % lam, flush=True)
    print("== 182 region ==", flush=True)
    ti = int(np.argmin(np.where(ok, p, 1.0)))
    chr_name, tpos, ngene = fig182_region(fh5, pos, regions, beta, np.where(ok, p, 1.0), ti)
    print("top SNP %s:%d, genes in region: %d" % (chr_name, tpos, ngene), flush=True)
    print("DONE ch12b")
