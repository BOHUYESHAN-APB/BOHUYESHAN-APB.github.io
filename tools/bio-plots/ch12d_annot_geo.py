# -*- coding: utf-8 -*-
"""ch12d — 注释与地理（186-187，替代被验真拦截的甲基化图）
186：10002 假基因组注释的基因模型统计（基因长度 / 外显子数，读本地 GFF）
187：1135 份拟南芥的采集地理分布（acc.json 经纬度）
原计划的甲基化图（27genomes methylation bigWig）经验真发现 release 文件全部为空壳
（nBasesCovered=0），详见第六篇第八章。
"""
import os, sys, csv, gzip
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import save

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data-real")
MARK = "Real data: 1001 Genomes 27genomes annotation + accession metadata"


def gff_genes_exons(acc):
    """返回 (gene_lengths, exons_per_gene)——exon 的 Parent 指向 mRNA，
    需经 mRNA 的 Parent 二跳映射回 gene；基因取其最长转录本的外显子数"""
    path = os.path.join(DATA, "gff", "genes_v05_%d.gff.gz" % acc)
    gene_len, mrna_gene, exon_per_mrna = {}, {}, {}
    with gzip.open(path, "rt") as f:
        for line in f:
            if line[0] == "#":
                continue
            p = line.rstrip("\n").split("\t")
            if p[2] not in ("gene", "mRNA", "exon"):
                continue
            attrs = dict(kv.split("=", 1) for kv in p[8].split(";") if "=" in kv)
            if p[2] == "gene":
                gid = attrs.get("ID")
                if gid:
                    gene_len[gid] = int(p[4]) - int(p[3]) + 1
            elif p[2] == "mRNA":
                mid, gid = attrs.get("ID"), attrs.get("Parent")
                if mid and gid:
                    mrna_gene[mid] = gid
            else:
                mid = attrs.get("Parent")
                if mid:
                    exon_per_mrna[mid] = exon_per_mrna.get(mid, 0) + 1
    exons_per_gene = {}
    for mid, n in exon_per_mrna.items():
        gid = mrna_gene.get(mid)
        if gid in gene_len:
            exons_per_gene[gid] = max(exons_per_gene.get(gid, 0), n)
    return np.array(list(gene_len.values()), dtype=float), \
        np.array([exons_per_gene.get(g, 0) for g in gene_len], dtype=float)


def fig186_gene_models():
    import matplotlib.pyplot as plt
    gl, ec = gff_genes_exons(10002)
    med_len = float(np.median(gl))
    med_ex = float(np.median(ec))
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.2))
    axes[0].hist(gl / 1000.0, bins=80, range=(0, 8), color="#1f77b4")
    axes[0].axvline(med_len / 1000.0, color="#d62728", ls="--", lw=1.4,
                    label="median %.2f kb" % (med_len / 1000.0))
    axes[0].set_xlabel("Gene length (kb)")
    axes[0].set_ylabel("Number of genes")
    axes[0].set_xlim(0, 8)
    axes[0].legend(fontsize=8)
    vals, counts = np.unique(ec, return_counts=True)
    axes[1].bar(vals, counts, color="#2ca02c")
    axes[1].axvline(med_ex, color="#d62728", ls="--", lw=1.4,
                    label="median %d" % med_ex)
    axes[1].set_xlim(0, 20)
    axes[1].set_xlabel("Exons per gene")
    axes[1].set_ylabel("Number of genes")
    axes[1].legend(fontsize=8)
    fig.suptitle("Fig 186  Gene models in genes_v05_10002 (27genomes consensus)",
                 y=1.0)
    fig.tight_layout()
    save(fig, "186_real_gene_models.png", mark=MARK)
    return len(gl), med_len, med_ex


def fig187_geo():
    import matplotlib.pyplot as plt
    import h5py
    with h5py.File(os.path.join(DATA, "1001_SNP_MATRIX",
                                "imputed_snps_binary.hdf5"), "r") as f:
        h5ids = set(int(a) for a in f["accessions"][:])
    ids, lats, lons, ctrys = [], [], [], []
    with open(os.path.join(DATA, "acc.json")) as f:
        for r in csv.DictReader(f):
            try:
                pk = int(r["pk"])
                la = float(r["latitude"])
                lo = float(r["longitude"])
            except (KeyError, ValueError):
                continue
            if pk not in h5ids:
                continue  # 只画基因型矩阵里的 1135 份
            ids.append(pk)
            lats.append(la)
            lons.append(lo)
            ctrys.append(r["country"])
    lats = np.array(lats)
    lons = np.array(lons)
    ctrys = np.array(ctrys)
    CCOL = {"Sweden": "#1f77b4", "Spain": "#ff7f0e", "US": "#8c564b",
            "GER": "#d62728", "Italy": "#2ca02c", "UK": "#9467bd"}
    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    rest = np.array([c not in CCOL for c in ctrys])
    ax.scatter(lons[rest], lats[rest], s=9, color="#c7c7c7", alpha=0.6,
               linewidths=0, label="other n=%d" % rest.sum())
    for c, col in CCOL.items():
        m = ctrys == c
        ax.scatter(lons[m], lats[m], s=13, color=col, alpha=0.85,
                   linewidths=0, label="%s n=%d" % (c, m.sum()))
    ax.set_xlabel("Longitude (deg)")
    ax.set_ylabel("Latitude (deg)")
    ax.set_xlim(-130, 40)
    ax.set_ylim(25, 68)
    ax.set_title("Fig 187  Collection sites of the 1135 sequenced accessions")
    ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    save(fig, "187_real_geo_scatter.png", mark=MARK)
    return len(ids), int(rest.sum())


if __name__ == "__main__":
    print("== 186 gene models ==", flush=True)
    n, med_len, med_ex = fig186_gene_models()
    print("genes %d, median len %.0f bp, median exons %d" % (n, med_len, med_ex),
          flush=True)
    print("== 187 geo ==", flush=True)
    print(fig187_geo(), flush=True)
    print("DONE ch12d")
