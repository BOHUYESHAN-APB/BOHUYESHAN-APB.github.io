# agent.md —— 本仓库写作与内容管理规则

> 本文件是给 AI 助手和未来维护者看的内容管理规范。改动标签体系前必读；与本文件冲突的历史做法一律以本文件为准。

## 一、项目速览

- Astro 博客，主题 Astro Theme Pure（pnpm 管理），GitHub Actions 自动部署到 GitHub Pages（自定义域名 bohuyeshan.top）
- 旧站（Hexo/Butterfly 全量历史）归档于仓库 `bohuyeshan-archive`，由本仓库的部署流水线构建后挂在 `bohuyeshan.top/old/` 路径
- 文章目录：`src/content/blog/<年>/<月>/<日>/<slug>.md`，**目录结构即 URL**：`/年/月/日/slug/`，移动文件 = 改 URL
- 构建验证：`npx astro build`（含 pagefind 搜索索引生成）；本地预览：`pnpm dev`
- 第三方前端库全量本地自托管（`public/js/`：3dmol、pdb-viewer、mermaid），**不要引入 jsdelivr/cdnjs 外链**

## 二、标签体系（权威定义）

没有独立分类系统，标签同时承担栏目和主题检索。一篇 3–6 个标签为宜。

### 现存权威标签（2026-09 清理后）

`图表大全` `科研绘图` `蛋白质` `生信入门` `大模型` `群体遗传` `GWAS` `药物设计` `Linux` `Arch` `安全` `技术选型` `运维` `技术拆解` `昇腾` `AI for Science` `数据工程` `AI制药` `Agent` `编程工具` `生信技术` `重测序` `蛋白质结构` `表观遗传` `结构生物学`

### 硬性规则

1. **优先复用权威标签**；新建时中文主题用中文，专有名词保留英文原名（Rust、Claude）
2. 禁用变体：`图表可视化`→科研绘图、`Nature 风格`→科研绘图、`AI 制药`→AI制药、`方法选型`→技术选型、`生信图表大全`→图表大全
3. **禁用标签**：`基因`、`AI`、`真实数据`（无检索价值）
4. front-matter 的 tags 是数组，**每项一个独立标签**，禁止拼接
5. 注意：schema 会自动去重，但保留大小写（GWAS 不会变 gwas）

### 系列约定

「生信图表大全」系列：系列标签固定 `图表大全`，标题用「生信图表大全（第X篇）：…」编号，长文可放入 `src/content/docs/` 文档系统。

## 三、Front-matter 模板

```yaml
---
title: 文章标题（≤120 字符）
description: 一到两句摘要，用于 SEO/OG/RSS，必填
publishDate: 2026-09-15
tags: [生信技术, 图表大全]
draft: false        # 可选
featured: false     # 本主题无此字段，纯占位不要写
---
```

- `title`、`description`、`publishDate` 必填（zod schema 校验，失败构建报错）
- 数学公式开箱即用（remark-math + KaTeX 已内置），无需开关

## 四、正文渲染能力清单

| 内容 | 写法 | 说明 |
| --- | --- | --- |
| 数学公式 | `$行内$` 与 `$$展示$$` | KaTeX 全站启用 |
| Mermaid 图 | ```` ```mermaid ```` 围栏 | remark 插件转占位 + 本地 mermaid.min.js 客户端渲染 |
| 蛋白 3D 视图 | `<div class="pdb3d" data-cfg='{...}' style="height:420px"></div>`，其后加 `<script src="/js/3dmol-min.js"></script><script src="/js/pdb-viewer.js"></script>` | 点击加载、全页独占；pdb 路径仅允许本站相对路径 |
| 折叠块 | `<details><summary>标题</summary>内容</details>` | 禁止任何 `{% %}` 模板标签语法 |
| 内联 SVG | 直接写 `<svg>` | 原样透传 |
| 图片 | 新站图片放 `public/img/<slug>/`，引用 `/img/<slug>/x.png` | 旧图在 `/old/img/...` 可直接热链 |
| 站内互链 | 真实永久路径 `/年/月/日/slug/` | 归档旧文用 `/old/年/月/日/slug/` |
| 分享 | 文章底部自动生成：微信二维码 / 微博 / QQ | 微信二维码构建期生成，无外部服务 |

## 五、正文 Markdown 渲染规范

> CommonMark 侧翼规则：`**` 的开闭由两侧字符决定，中文标点属于 Unicode 标点会干扰判定。写时自律：

1. **中文标点一律放在强调符号外侧**：✅ `**第一，做快做专业**。` ❌ `**第一，做快做专业。**`
2. **链接 URL 禁止空格与全角标点**；站内链接用真实永久路径；外链特殊字符用 `<https://...>` 形式
3. **子列表缩进与父项对齐**（无序 ≥2 空格，有序 ≥3 空格）
4. 表格单元格内裸 `|` 写 `\|`；必须有 `| --- |` 分隔行
5. 行内代码含反引号用双反引号包裹

## 六、发布与变更须知

- push 到 main 自动部署：构建 → pagefind → /old/ 组合 → 引用完整性检查，任一失败不上线
- 改归档站后联动发布：`gh workflow run deploy.yml -R BOHUYESHAN-APB/BOHUYESHAN-APB.github.io`
- 本地无 Google/CDN 依赖：字体（fontsource variable）、图标、搜索全部本地
- 修改 `src/content/blog/` 内文件路径 = 修改 URL，站内互链必须同步
