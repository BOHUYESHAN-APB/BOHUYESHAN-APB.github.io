---
title: "Software is over?：一周重造 Adobe 的现场记录"
description: 开源组织 storytold 一周内放出七个 Rust 写的 Adobe 清洁室重造版，主创放话「Software is over」、一个月 100% parity。HN 实测几乎不可用，但「一周七个可安装的 MIT 应用」是真实的新基线；真正值得盯的是素材互通与 agent 接口两根线。
publishDate: 2026-10-07
tags: [技术选型, 编程工具, 技术拆解]
---

## 〇、一句狂言和七个仓库

先看时间线，因为它本身就是新闻。GitHub 组织 storytold 的 PhotoCraft 仓库创建于 **2026 年 9 月 30 日**；一周之内，七个仓库全部上线：PhotoCraft（对标 Photoshop）、VectorCraft（Illustrator）、FilmCraft（Premiere）、LightCraft（Lightroom）、PrintCraft（Acrobat）、EffectCraft（After Effects）、DesignCraft（InDesign）——全部「pure Rust 清洁室重造」，MIT/Apache 双许可，无遥测，桌面端免登录直接装（[官网](https://getartcraft.com/apps)、[GitHub](https://github.com/storytold)）。

主创（HN 账号 echelon）在 Reddit 上的原话更猛：

> Software is over. But for real. I just one-shotted Photoshop. The whole thing.
> 软件终结了。这次是真的。我一口气把 Photoshop 整个做出来了。

以及：一个月内达到 Beta、约 100% 功能对齐；接下来还要重造 Microsoft Office、AutoCAD、Solidworks——「Everything can be open source multiplatform Rust now. Party like it's 1999.」

中文社交平台的传播版本更简洁：「Adobe 天塌了，全套 Adobe 软件，开源实现。」

一周、七个应用、一句「软件终结了」。这个组合该怎么读？先看实物，再下结论。

## 一、实物检验：HN 的两极

这个项目上了 [Hacker News](https://news.ycombinator.com/item?id=49958850)（118 分、179 条评论），评论区几乎是一场立场分流。

**差评方的证据最具体。** 一位多年设计/影视从业者（jenniferhooley）拿自己的真实项目实测 PhotoCraft，结论是「literally nothing works」：文字选择器与光标错位；字号滑块拖三秒无反应；全界面卡顿；文件夹展开不了；快捷键全部失灵；移动对象冻结后消失；面板点错就再也找不回来。另一位直接定性：「AI 生产的、破碎的软件，标题与描述与事实的距离可以叫欺骗。」

**好评方也不是完全没有。** 一位用户（amadeus88）的理由很实在：LightCraft 竟然支持 Lightroom 的预设——这是其他免费替代品都没有的；「如果作者把蒙版修好、再把本地 AI 用于蒙版，我可能真会退订 Adobe。没错它是个 vibe-code 出来的烂摊子，可 Adobe 自己的软件也烂得很。」还有人（ioma8）说得更轻描淡写：他自己花几小时就用 Rust 撸了一个只含自用功能的 Photoshop，用了九个月，全 PSD 支持、图层、文字，没问题。

**而中间那条最值得记住的评论是**（nonethewiser）：

> 这事相当疯狂。只是我们已经对 AI 麻木了。三年前要是冒出来这么个东西，你会目瞪口呆，那会是重大新闻。

这句话把整件事的性质说对了：**评价它的正确坐标系，不是「和 Photoshop 比」，而是「和三周前比」。** 一周内产出七个可安装、可运行、开源无遥测的应用骨架——无论多烂，这条基线本身是三个月前的人类团队做不到的。烂是真的，基线移动也是真的；两个真话并不打架。

## 二、为什么重造 Photoshop ≠ 重造 Excel

HN 里最好的一条技术判断来自 dofm，值得整段转述：Excel 可以被 slop-code 复刻，因为它是一个「可实现完备测试」的应用；**但 Photoshop 不是一个应用，它是一种介质（a surface and a medium）**——它有手感、有响应性格、有 dodge and burn 级别的肌肉记忆；高端修图师不换 Affinity（哪怕已经免费）的原因不是功能差距，是「手感不对」。

这条判断有两个来自从业者的旁证。printpdf 库的维护者（fschuett）提醒：仅仅「PDF 导出」这一件事，正确的字体编码与子集化就花了他几个月的试错，「别低估 QA 和测试的工程量」。CAD 领域的开发者（qchris）则指出 Solidworks 的护城河在几何内核：开源的 OpenCASCADE 不如 Parasolid，自己从头写一个参数化内核「难得要命」——这正是为什么全行业都买内核而不是自研。

另一条关于护城河的评论（bergen）说得同样准：Adobe 的护城河是**行业标准地位**——海量的教程视频、与打印机/相机/小众格式的对接、招聘时「会 Adobe」作为通用技能。换掉它意味着整个行业重新学一遍、重新对接一遍。

把这三条合起来，正好回到一个更准的判断（也是中文评论区里那位首评的潜台词——「界面不支持中文，不如用同样免费的 Affinity」）：**单点工具的战争早就打完了，GIMP、Krita、Inkscape、Blender、Darktable 全都在，Affinity 免费之后连「付费单点替代品」都有了。缺的从来不是第七个单点工具，缺的是套件之间那条看不见的线。**

## 三、真正值得盯的：两根线

这套 Craft 真正有意思的地方，不在七个图标任何一个里面，而在它们之间——以及它们对外的两个接口。

**第一根线：素材的通用语。** Adobe 最擅长的一件事，从来不是某个软件的功能，而是一套素材在多个软件之间快速流转——从修图到排版到剪辑，拖过去就能用。这是二十年格式与生态沉淀出来的能力（.psd、.ai、动态链接、素材库）。PhotoCraft 的卖点里写着「real PSD files」——清洁室读写真实 PSD——这直接是在攻格式的护城河。如果八个 Craft 共享同一套数据层与色彩管理，开源世界第一次有了「套件级」的素材流转。**这条线通了，单点工具的二十年劣势才有机会翻盘；不通，七个应用只是七个更好的 GIMP。**

**第二根线：agent 接口。** 官网页脚写着一行小字：**Agent-ready**。这不是我的引申，是它们自己的赌注。HN 评论区当场就有人接住了（aus10d）：「我特别想要能被 agent 或 CLI 程序化操控的版本——用命令行操作 dwg 和 xlsx 文件，那才叫棒。」注意这个需求的方向：**agent 需要的不是又一套 GUI，而是稳定的数据接口和脚本面。** 闭源软件给不了这个（Adobe 的脚本接口是它自己的方言），开源套件天然可以：数据层全开放，每个操作可编程。如果素材可以在多个软件间自动流转、由 agent 调度——「素材在软件间拖拽」升级成「素材在软件间自动流水」——那才是 Adobe 结构性睡不着觉的场景。

## 四、反向的一根刺

但这次讨论里最锋利的一句，指向的其实是另一个方向（tonyedgecombe）：

> Adobe 的问题不在于我们用 AI 造的工具替换他们的工具，而在于我们用「使用 AI」替换了「使用他们的工具」。

翻译过来：重造 Photoshop 是在争夺旧战场的旧址；而修图、剪辑、排版这些动作本身，正在被生成模型整体绕过。八个 Craft 做得再好，也还是在给一个可能正在缩小的需求池供货。另一位评论者（hypfer）的注脚更黑色幽默——UI 做得这么像，Adobe 大概会报复；「我猜这个行业没料到，他们自己的 IP 洗白工具，最终洗白的是他们自己的 IP。」

## 五、一个月之约

主创承诺「一个月内 Beta、约 100% 对齐」。这是个罕见的**可证伪**的狂言——2026 年 11 月初见分晓，到时候回来对账即可。

在那天之前，这份现场记录的结论分三层：

- **营销层**：「Software is over」「one-shotted the whole thing」是标准的注意力话术，alpha 当 beta 卖，建议按 slop 处理；
- **产品层**：实测确实几乎不可用；但「一周、七个、可安装、MIT、无遥测」是真实的新基线——三年前这是天方夜谭，现在只是一个狂人的周末项目。软件没有终结，**软件的生产成本曲线在塌**，这件事本身比这套软件可用与否重要得多；
- **战略层**：真正值得盯的是那两根线——素材的通用语与 agent 的接口。谁先做通（不管是 Craft、Blender 生态、还是某个还没冒头的套件），谁就拿到下一代创作工作流的地基。到那时，对手盘上站的可能不是「开源版 Adobe」，而是「根本不需要 Adobe 的工作流」。

软件没 over。是写软件这件事，开始 over 我们对「一家软件公司」的想象了。

## 附

- 官方：[getartcraft.com/apps](https://getartcraft.com/apps)、[GitHub org: storytold](https://github.com/storytold)（PhotoCraft 仓库 2026-09-30 创建；PhotoCraft 为 Apache-2.0，VectorCraft 为 MIT OR Apache-2.0；「一周/commit 数」为写作时点的仓库公开信息）
- 社区检验与引语：[HN 讨论](https://news.ycombinator.com/item?id=49958850)（jenniferhooley、amadeus88、ioma8、dofm、fschuett、qchris、bergen、aus10d、tonyedgecombe、hypfer、nonethewiser 及主创 echelon 的回复均出自该帖）；主创 Reddit 表态转引自帖内链接，未逐一核原帖
- 侧写：[Gigazine 报道](https://gigazine.net/gsc_news/en/20261005-artcraft-crafting-apps)、中文分析[《Crafting Apps 上线 7 款纯 Rust 创意软件套件》](https://www.ic.work/article/crafting-apps-photo-craft-rust-creative-suite-analysis)（「现实落差」立场）
- Affinity 免费化说法来自 HN 评论与中文首评的转述，官方定价未逐一复核
