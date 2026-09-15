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
| 视频 | 文件放 `public/media/<slug>/`，正文写 `<video controls src="/media/<slug>/x.mp4"></video>` | 单文件 ≤50MB；更大用 B 站 iframe 外链 |
| 音频 | 文件放 `public/media/<slug>/`，正文写 `<audio controls src="/media/<slug>/x.mp3"></audio>` | 单文件 ≤50MB |
| 站内互链 | 真实永久路径 `/年/月/日/slug/` | 归档旧文用 `/old/年/月/日/slug/` |
| 分享 | 文章底部自动生成：微信二维码 / 微博 / QQ | 微信二维码构建期生成，无外部服务 |

### 文章资产规则

1. **目录与路径**：所有随文资产放 `public/` 下（`public/img/<slug>/`、`public/media/<slug>/`），正文引用一律用根绝对路径（`/img/…`、`/media/…`）。`public/` 内文件原样部署到站点根，构建不做任何改写。
2. **不要用图床/CDN 外链**：全站资源本地自托管，外链图床随时会死链。
3. **大小纪律**：单文件超过 50MB GitHub 会告警、超 100MB 直接拒收，且大文件永久留在 git 历史里。截图先压缩再提交（PNG 截图转 JPG/WebP 可缩一个量级）；大视频一律 B 站外链（`<iframe>` 直接过境即可）。
4. **封面图**：不使用 front-matter 的 `heroImage` 字段（它要求数据管线内解析，与 `public/` 约定冲突）；封面直接用正文首图。
5. **文件名**：全小写 + 连字符，避免空格、中文、大小写混用——线上是 Linux 大小写敏感环境。

## 五、正文 Markdown 渲染规范

> CommonMark 侧翼规则：`**` 的开闭由两侧字符决定，中文标点属于 Unicode 标点会干扰判定。写时自律：

1. **中文标点一律放在强调符号外侧**：✅ `**第一，做快做专业**。` ❌ `**第一，做快做专业。**`
2. **链接 URL 禁止空格与全角标点**；站内链接用真实永久路径；外链特殊字符用 `<https://...>` 形式
3. **子列表缩进与父项对齐**（无序 ≥2 空格，有序 ≥3 空格）
4. 表格单元格内裸 `|` 写 `\|`；必须有 `| --- |` 分隔行
5. 行内代码含反引号用双反引号包裹
6. **禁止写入会随时间过期的状态描述**（如「明年毕业」「最近在准备 X」）：About、首页、站点描述里只放长期成立的表述；时间点只允许作为文章主题本身出现（publishDate、事件日期）

## 六、发布与变更须知

- **发布纪律（最高优先级）**：新文章与内容修改先在本地预览（`pnpm dev`），经用户确认满意后才 `git push` 发布。写好但未确认的文章一律 `draft: true`——dev 环境可见、线上不渲染、不进 RSS。未经确认不得 push 任何内容变更
- push 到 main 自动部署：构建 → pagefind → /old/ 组合 → 引用完整性检查，任一失败不上线
- 改归档站后联动发布：`gh workflow run deploy.yml -R BOHUYESHAN-APB/BOHUYESHAN-APB.github.io`
- 本地无 Google/CDN 依赖：字体（fontsource variable）、图标、搜索全部本地
- 修改 `src/content/blog/` 内文件路径 = 修改 URL，站内互链必须同步
- **主题升级注意**：astro-pure 是 npm 依赖，`src/components/` 里有本地覆盖组件，升级版本后需对照上游逐一复查：
  - `PostPreview.astro` / `ArticleBottom.astro`：文章链接改为根级日期 URL（`/${id}/`），上游默认 `/blog/<id>` 与按路径前两段拼链接，在本站会 404
  - `Copyright.astro`：中文标签 + 底部入口改指 `/support/`
  - `PFSearch.astro`：PagefindUI 中文界面
- URL 规范为根级日期制（`/YYYY/MM/DD/slug/`），内容目录同样按日期分层（`src/content/blog/YYYY/MM/DD/`），本地管理与线上路径一一对应；不采用主题默认的 `/blog/` 前缀

## 七、给予支持（/support）

- 支持页在 `src/pages/support/index.astro`，文章底部版权卡下方固定入口「给予支持 ☕」指到这里
- 赞赏渠道集中在 `src/site.config.ts` 的 `sponsor` 导出：微信/支付宝收款码（图片放 `public/img/sponsor/`，配置里填根路径）、爱发电、Buy Me a Coffee、GitHub Sponsors——**留空的渠道自动隐藏，不会出现空位**
- 不花钱的支持（Star/关注/分享/RSS）是真实链接，不要动
