# -*- coding: utf-8 -*-
"""ch12d — 真实甲基化图（184-185）stub test"""
import os, sys, csv
import numpy as np
import pyBigWig

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import save

MBASE = "https://1001genomes.org/data/1001Gp/27genomes/releases/current/methylation/"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data-real")
DUMP = os.path.join(HERE, "data_dump", "ch12")
MARK = "Real data: 1001 Genomes 27genomes methylomes (bigWig)"

GROUPS = {
    "clock": [("AT1G01060", "LHY"), ("AT2G46830", "CCA1"), ("AT5G61380", "TOC1")],
    "floral": [("AT5G10140", "FLC"), ("AT1G65480", "FT"), ("AT2G45660", "SOC1"),
               ("AT1G69120", "AP1"), ("AT5G61850", "LFY"), ("AT4G25530", "FWA")],
    "stress": [("AT2G14610", "PR1"), ("AT5G52310", "RD29A")],
    "photo": [("AT1G67090", "RBCS1A")],
    "chromatin": [("AT5G49160", "MET1")],
    "other": [("AT1G01010", None)],
}
GCOLOR = {"clock": "#1f77b4", "floral": "#d62728", "stress": "#2ca02c",
          "photo": "#8c564b", "chromatin": "#9467bd", "other": "#7f7f7f"}
ACCS11 = [10002, 6024, 6909, 6966, 8236, 9075, 9537, 9543, 9728, 9888, 9905]
KNOWN_ACCS = frozenset(ACCS11)
CTXS = frozenset(["CG", "CHG", "CHH"])
SUFFIX = {"CG": "CGmeth.bw", "CHG": "CHGmeth.bw", "CHH": "CHHmeth.bw"}
DATA_REAL = os.path.realpath(DATA)


def gff_path(acc):
    """accession 白名单 + 规范化路径校验，禁止逃出 data-real 目录"""
    acc = int(acc)
    if acc not in KNOWN_ACCS:
        raise ValueError("unexpected accession id %r" % acc)
    p = os.path.join(DATA_REAL, "gff", "genes_v05_%d.gff.gz" % acc)
    if os.path.commonpath([DATA_REAL, os.path.realpath(p)]) != DATA_REAL:
        raise ValueError("path escapes data dir")
    return p


def gene_coords(acc):
    import gzip
    out = {}
    with gzip.open(gff_path(acc), "rt") as f:
        for line in f:
            if line[0] == "#":
                continue
            p = line.rstrip("\n").split("\t")
            if p[2] != "gene":
                continue
            attrs = dict(kv.split("=", 1) for kv in p[8].split(";") if "=" in kv)
            if attrs.get("Name"):
                out[attrs["Name"]] = (p[0], int(p[3]) - 1, int(p[4]))
    return out


def open_m(acc, ctx):
    if ctx not in CTXS:
        raise ValueError("bad context %r" % ctx)
    url = MBASE + ("%d." % int(acc)) + SUFFIX[ctx]
    bw = pyBigWig.open(url)
    bw.chroms()
    return bw


def cg_genebody_matrix():
    """11 accessions x 面板基因 的基因体 CG 平均甲基化（缓存 CSV）"""
    cache = os.path.join(DUMP, "cg_genebody.csv")
    if os.path.exists(cache):
        with open(cache) as f:
            rd = list(csv.reader(f))
        accs = [int(x) for x in rd[0][1:]]
        genes = [r[0] for r in rd[1:]]
        mat = np.array([[float(x) for x in r[1:]] for r in rd[1:]])
        return accs, genes, mat
    genes = [agi for g in GROUPS.values() for agi, _ in g]
    cols, kept = [], []
    for acc in ACCS11:
        coords = gene_coords(acc)
        bw = open_m(acc, "CG")
        row = np.zeros(len(genes))
        for i, agi in enumerate(genes):
            if agi not in coords:
                row[i] = np.nan  # 该 accession 的注释缺此基因
                continue
            seqid, s, e = coords[agi]
            if seqid not in bw.chroms():
                row[i] = np.nan
                continue
            v = bw.stats(seqid, s, e, type="mean", nBins=1)[0]
            row[i] = np.nan if v is None else v
        bw.close()
        cols.append(row)
        kept.append(acc)
        print("  CG", acc, flush=True)
    mat = np.array(cols).T  # genes x accs
    rows = [[agi] + ["%.4f" % x for x in mat[i]] for i, agi in enumerate(genes)]
    np.savetxt(cache, np.array(rows, dtype=object), fmt="%s", delimiter=",",
               header="gene," + ",".join(str(a) for a in kept), comments="")
    return kept, genes, mat


def fig186_fwa_profile():
    import matplotlib.pyplot as plt
    acc = 10002
    coords = gene_coords(acc)
    seqid, s, e = coords["AT4G25530"]  # FWA
    pad = 2000
    lo, hi = max(0, s - pad), e + pad
    fig, axes = plt.subplots(3, 1, figsize=(8.2, 5.6), sharex=True,
                             gridspec_kw={"hspace": 0.12})
    stats = {}
    for ax, ctx in zip(axes, ["CG", "CHG", "CHH"]):
        bw = open_m(acc, ctx)
        arr = np.array(bw.values(seqid, lo, hi), dtype=float)
        bw.close()
        mask = ~np.isnan(arr)
        pos = np.arange(lo, hi)[mask]
        v = arr[mask]
        ax.scatter(pos, v, s=5, color={"CG": "#1f77b4", "CHG": "#d62728",
                                       "CHH": "#2ca02c"}[ctx], alpha=0.7, linewidths=0)
        ax.axvspan(s, e, color="k", alpha=0.07)
        ax.set_ylim(-0.05, 1.05)
        ax.set_ylabel(ctx + "\nmeth. level", fontsize=8)
        body = v[(pos >= s) & (pos < e)]
        prom = v[(pos >= s - pad) & (pos < s)]
        stats[ctx] = (int(mask.sum()), float(body.mean()) if len(body) else float("nan"),
                      float(prom.mean()) if len(prom) else float("nan"))
    axes[0].annotate("FWA gene body", (s + 50, 0.9), fontsize=8)
    axes[-1].set_xlabel("Position on " + seqid + " (bp)")
    axes[0].set_title("Fig 186  Single-C methylation at FWA (AT4G25530) +/-2 kb, acc. 10002")
    fig.tight_layout()
    save(fig, "186_real_fwa_methylation.png", mark=MARK)
    return (seqid, s, e), stats


def fig187_meth_expr():
    import matplotlib.pyplot as plt
    accs, genes, cg = cg_genebody_matrix()  # genes x accs
    with open(os.path.join(DUMP, "rpk_rosette_accs.csv")) as f:
        rd = list(csv.reader(f))
    hdr = [int(k.split("_")[0]) for k in rd[0]]
    agis = [r[0] for r in rd[1:]]
    rpk = np.array([[float(x) for x in r[1:]] for r in rd[1:]])  # genes x accs
    col = [hdr.index(a) for a in accs]
    rpk = rpk[:, col]
    gene_of = {g: i for i, g in enumerate(genes)}
    ridx = {g: i for i, g in enumerate(agis)}
    xs, ys, cs, labs = [], [], [], []
    for gname, lst in GROUPS.items():
        for agi, sym in lst:
            if agi in gene_of and agi in ridx:
                for j in range(len(accs)):
                    x = cg[gene_of[agi], j]
                    y = rpk[ridx[agi], j]
                    if not (np.isnan(x) or np.isnan(y)):
                        xs.append(x)
                        ys.append(np.log2(y + 1))
                        cs.append(GCOLOR[gname])
                        labs.append(gname if not sym else gname + " (" + sym + ")")
    xs, ys, cs, labs = map(np.array, (xs, ys, cs, labs))
    r = float(np.corrcoef(xs, ys)[0, 1])
    rho = float(np.corrcoef(np.argsort(np.argsort(xs)), np.argsort(np.argsort(ys)))[0, 1])
    fig, ax = plt.subplots(figsize=(6.8, 5.2))
    seen = set()
    for x, y, c, lab in zip(xs, ys, cs, labs):
        if lab not in seen:
            ax.scatter(x, y, s=34, color=c, label=lab, alpha=0.85, linewidths=0)
            seen.add(lab)
        else:
            ax.scatter(x, y, s=34, color=c, alpha=0.85, linewidths=0)
    ax.set_xlabel("Gene-body CG methylation (mean, 0-1)")
    ax.set_ylabel("log2(Rosette RPK + 1)")
    ax.set_title("Fig 187  CG methylation vs rosette expression, panel genes x 11 accessions")
    ax.legend(fontsize=7.5, loc="best")
    ax.annotate("Pearson r = %.2f, Spearman rho = %.2f, n = %d" % (r, rho, len(xs)),
                (0.02, 0.02), xycoords="axes fraction", fontsize=8)
    fig.tight_layout()
    save(fig, "187_real_meth_vs_expr.png", mark=MARK)
    return r, rho, int(len(xs))


if __name__ == "__main__":
    print("== 186 FWA profile ==", flush=True)
    locus, stats = fig186_fwa_profile()
    print("locus", locus, flush=True)
    for k, (n, b, p) in stats.items():
        print("  %s: nC=%d body=%.3f prom=%.3f" % (k, n, b, p), flush=True)
    print("== 187 meth vs expr ==", flush=True)
    r, rho, n = fig187_meth_expr()
    print("r=%.3f rho=%.3f n=%d" % (r, rho, n), flush=True)
    print("DONE ch12d")
