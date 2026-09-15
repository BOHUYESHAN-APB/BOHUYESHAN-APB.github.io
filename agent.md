# agent.md —— 本仓库写作与内容管理规则

> 本文件是给 AI 助手和未来维护者看的内容管理规范。改动标签体系前必读；与本文件冲突的历史做法一律以本文件为准。

## 一、项目速览

- Astro 7 博客，主题 AstroPaper v6，GitHub Actions 自动部署到 GitHub Pages（自定义域名 bohuyeshan.top）
- 旧站（Hexo/Butterfly 全量历史）归档于仓库 `bohuyeshan-archive`，由本仓库的部署流水线构建后挂在 `bohuyeshan.top/old/` 路径
- 文章目录：`src/content/posts/<年>/<月>/<日>/<YYYY-MM-DD-slug>.md`，**目录结构即 URL**：`/年/月/日/slug/`，移动文件 = 改 URL
- 构建验证：`npm run build`（含 astro check + pagefind）；本地预览：`npm run dev`
- 第三方前端库全量本地自托管（`public/js/`：3dmol、pdb-viewer、mermaid），**不要引入 jsdelivr/cdnjs 外链**

## 二、标签体系（权威定义）

没有分类系统，标签同时承担栏目和主题检索。一篇 3–6 个标签为宜；没有准确标签时宁缺毋滥。

### 现存权威标签（2026-09 清理后，共 25 个）

`图表大全`(7) `科研绘图`(6) `蛋白质`(4) `生信入门`(4) `大模型`(3) `群体遗传`(2) `GWAS`(2) `药物设计`(2) `Linux` `Arch` `安全` `技术选型` `运维` `技术拆解` `昇腾` `AI for Science` `数据工程` `AI制药` `Agent` `编程工具` `生信技术` `重测序` `蛋白质结构` `表观遗传` `结构生物学`

### 硬性规则

1. **优先复用上面的权威标签**；确需新建时遵循同一命名风格（中文主题用中文，专有名词/语言/产品保留英文原名如 Rust、Claude）
2. 同义概念只用映射表右侧的**权威形式**，左侧变体禁止新增：
   - `科研绘图` ← 图表可视化、Nature 风格
   - `图表大全` ← 生信图表大全（原分类名）
   - `AI制药` ← AI 制药（不带空格）
   - `技术选型` ← 方法选型
3. **禁用标签**：`基因`、`AI`、`真实数据`（太泛，无检索价值）
4. front-matter 的 tags 用行内数组或逐行列表均可，但**每项必须是独立标签**，禁止把多个标签写进一个字符串
5. 不要写 `categories` 字段——本主题没有分类系统，写了也不渲染

### 系列约定

「生信图表大全」系列（长期连载）：系列标签固定 `图表大全`，标题用「生信图表大全（第X篇）：…」编号，篇间互链用 `/年/月/日/slug/` 真实路径。

## 三、Front-matter 模板

```yaml
---
title: 文章标题
description: 一到两句话的摘要，会用于 SEO/OG 卡片/RSS，必填且要认真写
pubDatetime: 2026-09-15 09:00:00
timezone: "Asia/Shanghai"
tags: [生信技术, 图表大全]
featured: false   # 可选：置顶到首页 Featured 区
draft: true       # 可选：草稿不发布
---
```

- `title`、`description`、`pubDatetime` 三项必填（schema 校验不过会构建失败）
- 不需要 `katex: true` 之类的开关，公式开箱即用

## 四、正文渲染能力清单

| 内容 | 写法 | 说明 |
| --- | --- | --- |
| 数学公式 | `$行内$` 与 `$$展示$$` | KaTeX 全站启用，无需开关；根号内求和/积分写 `\sum\nolimits_{} ` 防撑高 |
| Mermaid 图 | ```` ```mermaid ```` 代码围栏 | 客户端自动渲染，直接写围栏即可 |
| 蛋白 3D 视图 | `<div class="pdb3d" data-cfg='{...}' style="height:420px"></div>`，其后加 `<script src="/js/3dmol-min.js"></script><script src="/js/pdb-viewer.js"></script>` | 行为：点击加载、全页独占；cfg 里 pdb 路径仅允许本站相对路径（`/old/lib/pdb/*.pdb` 或 `/lib/pdb/*.pdb`） |
| 折叠块 | `<details><summary>标题</summary>内容</details>` | 原生 HTML 折叠；禁止任何 `{% %}` 模板标签语法 |
| 内联 SVG | 直接写 `<svg>` | 管线原样透传 |
| 图片 | 新站图片放 `public/img/<slug>/`，正文引用 `/img/<slug>/x.png` | 旧图在 `/old/img/...`，可直接热链 |
| 站内互链 | 用真实永久路径 `/年/月/日/slug/` | 归档旧文用 `/old/年/月/日/slug/` |

## 五、正文 Markdown 渲染规范（防强调/链接渲染失败）

> 渲染器遵循 CommonMark 侧翼规则：`**` 是"开启"还是"闭合"由两侧字符决定，**中文标点属于 Unicode 标点，会干扰判定**。本仓库没有旧站的自动修复脚本，以下规则靠写时自律。

1. **中文标点一律放在强调符号外侧**（适用于 `**`、`*`、`~~`、`__`）：
   - ✅ `**第一，把流程做快做专业**。`
   - ❌ `**第一，把流程做快做专业。**`（段落末尾恰好能渲染，但不要依赖位置侥幸）
2. **链接 URL 禁止含空格与全角标点**（`：，。？！（）`）；站内链接用真实永久路径；外链含特殊字符用 `<https://...>` 尖括号形式
3. **子列表缩进与父项文字对齐**（无序列表 ≥2 空格，有序列表 ≥3 空格）
4. **表格单元格内禁用裸 `|`**，必要时写 `\|`；表格必须有 `| --- |` 分隔行
5. 行内代码含反引号时用双反引号包裹

## 六、发布与变更须知

- push 到 main 自动部署（构建 + pagefind 索引 + /old/ 引用完整性检查，任何一步失败都不会上线）
- 改 `src/content/posts/` 下的文件路径 = 改 URL，旧链接会 404；站内互链必须同步改
- 改归档站（bohuyeshan-archive 仓库）后需要联动发布：`gh workflow run deploy.yml -R BOHUYESHAN-APB/BOHUYESHAN-APB.github.io`
- 文章页自带：暗色模式、代码复制、图片灯箱、pagefind 搜索；不要在文章里重复造这些轮子
