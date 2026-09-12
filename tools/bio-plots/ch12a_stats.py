# -*- coding: utf-8 -*-
"""ch12a 的补充统计：Fst 全基因组均值/95分位、SNP 密度均值/冠军窗口（图注用）"""
import os, sys
import numpy as np
import h5py

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch12a_pop_real import DATA, af_scan, country_map, load_meta

DUMP = os.path.join(HERE_D := os.path.dirname(os.path.abspath(__file__)),
                    "data_dump", "ch12")


def main():
    f, pos, regions, accs = load_meta()
    af = af_scan(f)
    cm = country_map()
    countries = np.array([cm.get(int(a), "?") for a in accs])
    counts = {c: int((countries == c).sum()) for c in np.unique(countries) if c != "?"}
    g1, g2 = sorted(counts, key=lambda c: -counts[c])[:2]
    m1, m2 = countries == g1, countries == g2
    print("groups:", g1, m1.sum(), "vs", g2, m2.sum(), flush=True)

    c0s, c0e = regions[0]
    rows = np.arange(c0s, c0e)
    win = 100000
    edges = np.arange(pos[rows][0], pos[rows][-1] + win, win)
    snps = f["snps"]
    vals, centers = [], []
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
        vals.append(((ht[ok] - hs[ok]) / ht[ok]).mean())
        centers.append((a + b) / 2 / 1e6)
    vals = np.array(vals)
    print("fst mean %.3f p95 %.3f max %.3f at %.2f Mb" %
          (vals.mean(), np.percentile(vals, 95), vals.max(),
           centers[int(vals.argmax())]), flush=True)

    dens_all, dens_max, dens_chr = [], 0, 0
    for ci in range(5):
        s, e = regions[ci]
        p = pos[s:e]
        w = np.arange(p[0], p[-1] + 1000000, 1000000)
        h, _ = np.histogram(p, bins=w)
        dens = h / 1000.0
        if dens.max() > dens_max:
            dens_max, dens_chr = float(dens.max()), ci + 1
        dens_all.append(dens.sum() / (len(w) - 1))
    print("density: overall approx %.1f SNPs/kb, max %.1f at Chr%d" %
          (float(np.mean(dens_all)), dens_max, dens_chr), flush=True)


if __name__ == "__main__":
    main()
