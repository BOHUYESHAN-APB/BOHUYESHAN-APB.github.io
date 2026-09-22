# agent.md —— 本仓库写作与内容管理规则

> 本文件是给 AI 助手和未来维护者看的内容管理规范。改动标签体系前必读；与本文件冲突的历史做法一律以本文件为准。

## 一、项目速览

- Astro 博客，主题 Astro Theme Pure（pnpm 管理），GitHub Actions 自动部署到 GitHub Pages（自定义域名 bohuyeshan.top）
- 旧站（Hexo/Butterfly 全量历史）归档于仓库 `bohuyeshan-archive`，由本仓库的部署流水线构建后挂在 `bohuyeshan.top/old/` 路径
- 文章目录：`src/content/blog/<年>/<月>/<日>/<slug>.md`，**目录结构即 URL**：`/年/月/日/slug/`，移动文件 = 改 URL
- **文章 .md 文件名一律英文**：全小写 + 连字符，格式 `YYYY-MM-DD-NN-english-slug.md`（如 `2026-09-15-01-fde-forward-deployed-engineer.md`）；中文写在 front-matter 的 title 里，不进文件名。改名迁移过的文章（含 12 篇 Hexo 迁移文），旧中文 URL 由 `public/<旧路径>/index.html` 跳转页承接，新建文章无需再兼容中文路径
- 构建验证：`npx astro build`（含 pagefind 搜索索引生成）；本地预览：`pnpm dev`
- 第三方前端库全量本地自托管（`public/js/`：3dmol、pdb-viewer、mermaid），**不要引入 jsdelivr/cdnjs 外链**

## 二、标签体系（权威定义）

没有独立分类系统，标签同时承担栏目和主题检索。一篇 3–6 个标签为宜。

### 现存权威标签（2026-09 清理后）

`图表大全` `科研绘图` `蛋白质` `生信入门` `大模型` `群体遗传` `GWAS` `药物设计` `Linux` `Arch` `安全` `技术选型` `运维` `技术拆解` `技术考古` `昇腾` `AI for Science` `数据工程` `AI制药` `Agent` `编程工具` `生信技术` `重测序` `蛋白质结构` `表观遗传` `结构生物学`

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

1. **中文标点与强调符号**：astro.config.ts 已装 `remark-cjk-friendly`，`**……很重要。**后面` 这类「标点收尾粗体」（CommonMark 原生渲染失败、星号裸奔）在站内已由渲染层自动修复，新旧文章都生效——**不要再用改文字的方式修站内渲染问题**。但 GitHub 等未装此插件的渲染器仍会失败，写作时优先把标点放在强调符号外侧：✅ `**……很重要**。后面` ❌ `**……很重要。**后面`
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

## 八、简历打印版（归档仓库 source/HTML/）维护经验

- **不自夸原则（用户明确要求）**：简历与 /resume/ 各页不得出现「主导」「主导开发」类字样——哪怕属实也不写，措辞用「开发」「维护」或直接列项目名；项目真实度由 GitHub 仓库自证。同理，过新（当月才做）的项目不要写成简历经历条目
- **量版面空隙要量叶子元素**：`.section` 常被 `flex:1` 拉伸、`.side-col`/`.main-col` 是 flex 等高容器，`offsetTop+offsetHeight` 量到的是盒子底不是内容底。要量 `.tl-item`/`.job-block`/`.method-grid`/`.proj-grid`/`.mini-grid` 等叶子块的真实底边；且必须在**自托管字体正确加载**（`await document.fonts.ready`）后测，回退字体行宽不同会差几十像素
- **往两页简历中间插区块 = 高危 div 平衡操作**：多写一个 `</div>` 会把 `.a4-page` 提前闭合，第二页脱离 `.a4-sheet` 变成 body 子元素——症状是两页上下堆叠、`.a4-page + .a4-page` 选择器全部失效。改完必须用 `pages[1].previousElementSibling === pages[0]` 验证相邻关系
- tech 版第二页间距选择器必须写 `> .section`（子元素是 div 不是 section 标签，裸 `section` 选择器永远不命中——这个坑踩过两次）
- 归档仓库 push 后需手动触发主站组合部署：`gh workflow run deploy.yml -R BOHUYESHAN-APB/BOHUYESHAN-APB.github.io`，完成后从线上（加 `?v=` 破缓存）用 `msedge --headless=new --no-pdf-header-footer --print-to-pdf` 重新生成桌面「简历打印」三份 PDF
- **归档路径转正机制（用户 2026.09 确认）**：新博客仓库部署时自动拉取归档仓库（bohuyeshan-archive）并把路径转正——线上 `/resume/*` 等旧路径 404 的问题不要在归档仓库侧修，等新仓库流水线转正即可；转正前，简历打印版上的查验地址指向实际落点 `/old/resume/projects`


## 九、对外口径管理（2026-09-22）

- `bohuyeshan.top/llms.txt`（本仓库 `public/llms.txt`）与 GitHub profile 仓库 `BOHUYESHAN-APB/BOHUYESHAN-APB` 是对外身份与口径的唯一来源。
- 权威口径：Agent 定义 **19 = 8 主编排 + 11 专家**（openagent-labforge-bio `src/config/constants.ts`）；生信技能 **617 / 87 类**（`resources/bioSkills` 实测）。旧印刷品中的 17 / 88 为过时数字。
- 修改简历三版、仓库描述、README 中任何对外数字时，必须同步 `public/llms.txt`。
- `public/robots.txt`：不拦普通爬取；注释仅声明不建议训练（注释会被解析器剥掉，**不可作为引导通道**）。`Sitemap:` 行指向 sitemap-index.xml。
- **发现链路规范（2026-09-22 晚修订，依据现行 llms.txt 提案与爬虫实测）**：
  - 进站 ≠ 读 llms.txt/robots.txt。chatbox 抓首页正文与 meta description；礼貌爬虫读 robots.txt 只看指令不看注释；主动探测 /llms.txt 的只有部分 coding agent 与文档向工具。
  - 载体优先级：**首页可见正文 + 首页 meta description**（`src/pages/index.astro` 的 meta.description 与"关于"区 🧭 块，改口径必须同步）> HTML `<link rel="describedby" type="text/plain" href="/llms.txt">`（BaseLayout，规范形式；`rel="llms"` 为非标准自造，已废弃）> HTTP `Link: </llms.txt>; rel="describedby"` 响应头（**已放弃**：源站 GitHub Pages 无法设自定义头，Cloudflare 无管理入口——2026-09-22 用户确认登不上；`meta http-equiv="Link"` 为 HTML5 废弃通道不可用。三类 agent 已由前三层覆盖，缺口可接受）> robots.txt Sitemap 行。
  - sitemap 不列 llms.txt（非 HTML 页，Astro sitemap 插件只收路由，收益近零，不做）。