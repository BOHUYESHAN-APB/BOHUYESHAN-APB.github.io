# -*- coding: utf-8 -*-
"""ch12c — 真实表达数据图（181-183）
数据：1001 Genomes 27genomes release 的 RNA-seq bigWig（远程范围查询，不下载数据体）
坐标：各 accession 自己的假基因组注释 genes_v05_<acc>.gff.gz（AGI Name 跨假基因组稳定）
"""
import os, sys, csv, gzip
import concurrent.futures as cf
import numpy as np
import pyBigWig

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import save

BASE = "https://1001genomes.org/data/1001Gp/27genomes/releases/current/rnaseq/"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data-real")
DUMP = os.path.join(HERE, "data_dump", "ch12")
os.makedirs(DUMP, exist_ok=True)
MARK = "Real data: 1001 Genomes 27genomes RNA-seq (bigWig)"

PANEL = [
    ("AT1G01060", "LHY"), ("AT2G46830", "CCA1"), ("AT5G61380", "TOC1"),
    ("AT5G10140", "FLC"), ("AT1G65480", "FT"), ("AT2G45660", "SOC1"),
    ("AT1G69120", "AP1"), ("AT5G61850", "LFY"), ("AT2G14610", "PR1"),
    ("AT5G52310", "RD29A"), ("AT1G67090", "RBCS1A"), ("AT4G25530", "FWA"),
    ("AT5G49160", "MET1"), ("AT1G01010", None),
]  # AT4G07300 (DDM1) 不在 27genomes 共识注释集中，故不收录
TISSUES = ["Rosette", "Seedlings", "Flowers", "Pollen"]


def load_manifest():
    m = {}
    with open(os.path.join(DATA, "rnaseq_manifest.txt")) as f:
        for line in f:
            name = line.strip()
            parts = name.split(".")
            tissue, acc = parts[0], int(parts[1])
            if parts[-2] in ("F", "R"):  # 链向文件都收：F/R 求平均近似总覆盖
                m.setdefault((tissue, acc), []).append(name)
    return m


def gene_coords(acc):
    """解析 genes_v05_<acc>.gff.gz -> {AGI: (seqid, start0, end, length_kb)}"""
    path = os.path.join(DATA, "gff", "genes_v05_%d.gff.gz" % acc)
    out = {}
    with gzip.open(path, "rt") as f:
        for line in f:
            if line[0] == "#":
                continue
            p = line.rstrip("\n").split("\t")
            if p[2] != "gene":
                continue
            attrs = dict(kv.split("=", 1) for kv in p[8].split(";") if "=" in kv)
            name = attrs.get("Name")
            if name:
                s, e = int(p[3]) - 1, int(p[4])
                out[name] = (p[0], s, e, (e - s) / 1000.0)
    return out


def open_bw(fname):
    last = None
    for _ in range(3):
        try:
            bw = pyBigWig.open(BASE + fname)
            bw.chroms()  # 触发索引读取
            return bw
        except Exception as e:  # 远程偶发失败重试
            last = e
    raise last


def rpk_vector(acc, tissue, manifest):
    """一个 accession 一个组织的基因面板 RPK 向量（同组织多批次取均值）"""
    coords = gene_coords(acc)
    files = manifest.get((tissue, acc))
    if not files:
        return None
    sums = []
    for fn in files:
        try:
            bw = open_bw(fn)
        except Exception as e:
            print("  skip broken %s: %s" % (fn, e), flush=True)
            continue
        row = np.zeros(len(PANEL))
        for i, (agi, _sym) in enumerate(PANEL):
            if agi not in coords:
                row[i] = np.nan
                continue
            seqid, s, e, _kb = coords[agi]
            if seqid not in bw.chroms():
                row[i] = np.nan
                continue
            v = bw.stats(seqid, s, e, type="sum", nBins=1)[0]
            row[i] = 0.0 if v is None else v
        bw.close()
        sums.append(row)
    raw = np.mean(sums, axis=0)
    kb = np.array([coords[a][3] if a in coords else np.nan for a, _ in PANEL])
    return raw / kb  # RPK


def _validated(acc, tissue, ext):
    """tissue 白名单 + realpath 包含校验，路径不得逃出 DUMP"""
    if tissue not in TISSUES:
        raise ValueError("bad tissue %r" % tissue)
    base = os.path.realpath(DUMP)
    p = os.path.join(base, "part_%d_%s%s" % (int(acc), tissue, ext))
    if os.path.commonpath([base, os.path.realpath(p)]) != base:
        raise ValueError("path escapes dump dir")
    return p


def get_matrix(accs_tissues, tag):
    """缓存两级：part_<acc>_<tissue>.npz 每查询即落盘（并行 6 线程），
    另写合并 CSV（savetxt）供复用与复现"""
    manifest = load_manifest()
    parts = os.path.join(os.path.realpath(DUMP), "rpk_parts")
    os.makedirs(parts, exist_ok=True)

    def fetch_part(acc, tissue):
        p, k = _validated(acc, tissue, ".npz"), "%d_%s" % (acc, tissue)
        p = os.path.join(parts, os.path.basename(p))
        if os.path.exists(p):
            return k, np.load(p)["v"]
        if os.environ.get("CH12_FAST") == "1":
            return k, None  # 快速模式：只吃缓存，缺的跳过
        v = rpk_vector(acc, tissue, manifest)
        if v is None:
            return k, None
        np.savez_compressed(p, v=v)
        print("  queried", k, flush=True)
        return k, v

    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        res = list(ex.map(fetch_part, [a for a, _ in accs_tissues],
                          [t for _, t in accs_tissues]))
    kept, cols = [], []
    for k, v in res:
        if v is not None:
            kept.append(k)
            cols.append(v)
    mat = np.array(cols).T  # genes x samples
    cache = os.path.join(os.path.realpath(DUMP), "rpk_" + tag + ".csv")
    rows = [[agi] + ["%.4f" % x for x in mat[i]]
            for i, agi in enumerate([a for a, _ in PANEL])]
    np.savetxt(cache, np.array(rows, dtype=object), fmt="%s", delimiter=",",
               header=",".join(kept), comments="")
    return kept, mat.T


def country_map():
    out = {}
    with open(os.path.join(DATA, "acc.json")) as f:
        for r in csv.DictReader(f):
            out[int(r["pk"])] = r["country"]
    return out


def zrows(mat):
    mu = np.nanmean(mat, axis=1, keepdims=True)
    sd = np.nanstd(mat, axis=1, keepdims=True)
    sd[sd == 0] = 1.0
    return (mat - mu) / sd


def rowlabel(i):
    agi, sym = PANEL[i]
    return ("%s %s" % (sym, agi)) if sym else agi


def fig181_tissue_heatmap():
    import matplotlib.pyplot as plt
    acc = 10002
    keys, mat = get_matrix([(acc, t) for t in TISSUES], "tissue10002")
    # mat: (样本 x 基因)；热图需要 (基因 x 组织) 的行内 z
    z = zrows(mat.T)
    fig, ax = plt.subplots(figsize=(6.4, 6.0))
    im = ax.imshow(z, cmap="RdYlBu_r", vmin=-2, vmax=2, aspect="auto")
    ax.set_xticks(range(len(keys)))
    ax.set_xticklabels(keys, rotation=30, ha="right")
    ax.set_yticks(range(len(PANEL)))
    ax.set_yticklabels([rowlabel(i) for i in range(len(PANEL))], fontsize=8)
    for i in range(z.shape[0]):
        for j in range(z.shape[1]):
            v = z[i, j]
            ax.text(j, i, "%.1f" % v, ha="center", va="center", fontsize=7,
                    color="white" if abs(v) > 1.4 else "black")
    cb = fig.colorbar(im, ax=ax, shrink=0.75)
    cb.set_label("Row z-score of RPK")
    ax.set_title("Fig 183  14-gene panel across 4 tissues, acc. 10002 (TueWal-2)")
    fig.tight_layout()
    save(fig, "183_real_tissue_heatmap.png", mark=MARK)
    return mat, keys


def fig182_acc_pca():
    import matplotlib.pyplot as plt
    manifest = load_manifest()
    rosette = sorted({a for (t, a) in manifest if t == "Rosette"})
    keys, mat = get_matrix([(a, "Rosette") for a in rosette], "rosette_accs")
    if len(keys) < 8:
        print("  [fig184] only %d accessions cached, skip" % len(keys), flush=True)
        return keys, np.zeros((len(keys), 2)), np.zeros(2)
    X = np.nan_to_num(zrows(mat.T).T)  # accessions x genes，按基因标准化
    Xc = X - X.mean(axis=0, keepdims=True)
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    P = U[:, :2] * S[:2]
    cm = country_map()
    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    COUNTRIES = ["GER", "SWE", "FRA", "ESP", "UK", "US"]
    CCOL = {"GER": "#1f77b4", "SWE": "#2ca02c", "FRA": "#d62728", "ESP": "#ff7f0e",
            "UK": "#9467bd", "US": "#8c564b"}
    for (acc, _t), (x, y) in zip([(int(k.split("_")[0]), None) for k in keys], P):
        c = cm.get(acc, "?")
        col = CCOL.get(c, "#7f7f7f")
        ax.scatter(x, y, s=55, color=col, edgecolor="k", linewidth=0.5, zorder=3)
        ax.annotate(str(acc), (x, y), textcoords="offset points", xytext=(4, 3), fontsize=7)
    handles = [plt.Line2D([], [], marker="o", ls="", color=CCOL[c],
               label="%s n=%d" % (c, sum(1 for k in keys if cm.get(int(k.split("_")[0])) == c)))
               for c in COUNTRIES if sum(1 for k in keys if cm.get(int(k.split("_")[0])) == c) > 0]
    other = sum(1 for k in keys if cm.get(int(k.split("_")[0]), "?") not in COUNTRIES)
    if other:
        handles.append(plt.Line2D([], [], marker="o", ls="", color="#7f7f7f", label="other n=%d" % other))
    ax.legend(handles=handles, fontsize=8, loc="best")
    var = S**2 / np.sum(S**2) * 100
    ax.set_xlabel("PC1 (%.0f%% var)" % var[0])
    ax.set_ylabel("PC2 (%.0f%% var)" % var[1])
    ax.set_title("Fig 184  PCA of %d accessions, rosette panel expression" % len(keys))
    fig.tight_layout()
    save(fig, "184_real_expression_pca.png", mark=MARK)
    return keys, P, var


def fig183_flc_tracks():
    import matplotlib.pyplot as plt
    acc = 10002
    coords = gene_coords(acc)
    seqid, s, e, _ = coords["AT5G10140"]  # FLC
    pad = 3000
    lo, hi = max(0, s - pad), e + pad
    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    colors = {"Rosette": "#2ca02c", "Seedlings": "#1f77b4", "Flowers": "#d62728", "Pollen": "#9467bd"}
    peaks = {}
    for t in TISSUES:
        files = load_manifest().get((t, acc), [])
        profs = []
        for fn in files:
            bw = open_bw(fn)
            iv = bw.intervals(seqid, lo, hi)
            bw.close()
            if not iv:
                continue
            pos = np.arange(lo, hi, 50)
            cov = np.zeros(len(pos))
            for st, en, v in iv:
                i0, i1 = max(0, (st - lo) // 50), min(len(pos), max(1, (en - lo) // 50))
                cov[i0:i1] = np.maximum(cov[i0:i1], v)
            profs.append(cov)
        prof = np.mean(profs, axis=0)
        peaks[t] = float(prof.max())
        ax.fill_between(np.arange(lo, hi, 50), 0, prof, step="post",
                        alpha=0.55, color=colors[t], label=t)
    ax.axvspan(s, e, color="k", alpha=0.08)
    ax.annotate("FLC body", (s, ax.get_ylim()[1] * 0.92), fontsize=8)
    ax.set_xlim(lo, hi)
    ax.set_xlabel("Position on %s (bp)" % seqid)
    ax.set_ylabel("Coverage (mean of F/R files)")
    ax.set_title("Fig 185  FLC (AT5G10140) +/-3 kb, acc. 10002, 4 tissues")
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, "185_real_flc_coverage.png", mark=MARK)
    return (seqid, s, e), peaks


if __name__ == "__main__":
    print("== 181 tissue heatmap ==", flush=True)
    mat, keys = fig181_tissue_heatmap()
    print("raw RPK col sums:", np.round(mat.sum(axis=0), 1), flush=True)
    print("== 182 accession PCA ==", flush=True)
    keys2, P, var = fig182_acc_pca()
    print("PC1/PC2 var%%: %.1f %.1f" % (var[0], var[1]), flush=True)
    print("== 183 FLC tracks ==", flush=True)
    locus, peaks = fig183_flc_tracks()
    print("locus", locus, "peaks", {k: round(v, 1) for k, v in peaks.items()}, flush=True)
    print("DONE ch12c")
