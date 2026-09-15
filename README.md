# bohuyeshan.top

生物信息 × AI 技术博客，基于 [Astro](https://astro.build) + [AstroPaper](https://github.com/satnaing/astro-paper) v6。

- 站点：`https://bohuyeshan.top`（GitHub Pages，Actions 自动部署）
- 文章：`src/content/posts/<年>/<月>/<日>/<slug>.md`，URL 与迁移前的 Hexo 完全一致
- 旧站归档：仓库 [bohuyeshan-archive](https://github.com/BOHUYESHAN-APB/bohuyeshan-archive)（Hexo，`root: /old/`），由本仓库的部署流水线构建后组合到 `/old/` 路径
- 旧链接兼容：`scripts/gen-redirects.mjs` 生成的跳转页在 `public/<旧路径>/index.html`

## 常用命令

```bash
npm install        # 安装依赖
npm run dev        # 本地开发
npm run build      # 构建到 dist/（含 pagefind 搜索索引）
npm run preview    # 预览构建产物
```

## 迁移相关脚本

```bash
node scripts/migrate.mjs <hexo-source/_posts-dir>      # Hexo 文章 -> 内容集合（一次性）
node scripts/gen-redirects.mjs <old-public-dir>        # 重新生成旧链接跳转页
node scripts/check-old-links.mjs dist                  # 校验 /old/ 引用（CI 也会跑）
```

新增文章直接在 `src/content/posts/` 按日期目录放置 markdown，front-matter 需要 `title`、`description`、`pubDatetime`。
