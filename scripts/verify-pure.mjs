// Verify Pure build output: posts, redirects, archive compose, RSS.
import { existsSync } from 'node:fs'

const checks = {
  '第六篇文章页': 'dist/2026/09/12/2026-09-12-08-生信图表大全第六篇-用真实公开数据画的22张图/index.html',
  '第五篇(3D)': 'dist/2026/09/12/2026-09-12-05-生信图表大全第五篇-蛋白结构变异与表达验证的40张图/index.html',
  '跳转页样本': 'dist/2026/03/24/2026-03-24-01-AI正在真正进入单细胞生物信息学流程/index.html',
  '/old/ 首页': 'dist/old/index.html',
  '归档PDB': 'dist/old/lib/pdb/6a15.pdb',
  'RSS': 'dist/rss.xml',
  'CNAME': 'dist/CNAME',
  '归档JS': 'dist/js/pdb-viewer.js',
  '字体文件': 'dist/_astro'
}

let bad = 0
for (const [name, path] of Object.entries(checks)) {
  const ok = existsSync(path)
  if (!ok) bad++
  console.log((ok ? '✓ ' : '✗ ') + name)
}
process.exit(bad ? 1 : 0)
