# BoHuYeShan 的个人博客

基于 [Hexo](https://hexo.io/zh-cn/) 与 [hexo-theme-butterfly](https://github.com/jerryc127/hexo-theme-butterfly) 构建的个人博客，静态站点部署于 Vercel，经 Cloudflare CDN 加速，并使用 Qexo 提供在线后台管理。

## 站点信息

- 博客地址：[https://bohuyeshan.top](https://bohuyeshan.top)
- 内容定位：学习笔记与技术文章
- 说明：这是本人公开发布的第 4 个个人博客。历史文章均重新整理后发布，不沿用原始时间记录，具有特殊意义的文章除外。

## 技术栈

| 工具 | 用途 |
| --- | --- |
| [Hexo](https://hexo.io/zh-cn/) | 静态博客框架 |
| [hexo-theme-butterfly](https://github.com/jerryc127/hexo-theme-butterfly) | 博客主题（基于官方主题二次定制样式） |
| Node.js | 本地构建与运行环境 |
| Git / GitHub | 源码托管与版本管理 |
| Vercel | 静态站点部署（Serverless） |
| Cloudflare | CDN 加速 |
| Qexo | 博客在线后台管理 |
| VS Code | 日常文章编辑 |

## 部署架构

```text
本地编辑（VS Code / Qexo）
        │
        ▼
Git 推送至 GitHub 仓库
        │
        ▼
Vercel 构建部署（Hexo 静态生成）
        │
        ▼
Cloudflare CDN 加速分发
```

## 快速开始

```bash
# 安装依赖
npm install

# 本地预览
npm run server

# 生成静态文件
npm run build

# 部署至远端
npm run deploy
```

## 分支说明

| 分支 | 说明 |
| --- | --- |
| `master` | 直接对外发布的博客，本地 Git 推送至远端的 Hexo 博客 |
| `main` | 主要内容分支，版本较新 |
| `future` | 备份分支，用于主要内容出现大量错误时恢复 |

## 相关账号

- GitHub（个人项目）：[bohuyeshan](https://github.com/bohuyeshan)

## 许可证

本项目基于 [AGPL-3.0](LICENSE) 许可证开源。
