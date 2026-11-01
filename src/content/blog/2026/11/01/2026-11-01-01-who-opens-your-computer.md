---
title: 谁替你打开电脑：Agent 入口之争的完整地图
description: 一个人的注意力只有 3–5 个活跃窗口，而操作系统、ADE、Harness、Bot、中转站五层楼都在争当那个唯一的入口。DSH 把这件事写得最清楚，市场份额却远不如把 Agent 塞进办公套件的字节、阿里、腾讯。这篇拆开五层楼、四种赞助货币，和一条正在塌陷的中间层。
publishDate: 2026-11-01
tags: [Agent, 大模型, 技术拆解]
draft: false
---

## 〇、三个数字

先把三个数字摆在一起，它们分别来自需求、市场和资助结构。

**三到五。** DeepSeek Harness 团队在那份 Super-agent 架构说明里写：一个人通常只能同时跟进 3 到 5 个活跃 Session。再多，就没有精力管下去了。

**47.6%。** IDC 的 2025 年中国 AI 编程市场份额报告里，阿里排第一。同一份报告给出市场规模：2025 年 3.99 亿元，2026 年底预计 11.73 亿元。

**2365 万美元。** Omarchy 官网挂出的数字，Omacom 基金会累计收到的承诺。赞助人名单里有 Meta、DigitalOcean、阿里云、OpenAI、OpenRouter、OrcaRouter，还有一笔 150 万美元的 Grok tokens。

第一个数字说的是**人**：注意力是上限。第二个说的是**市场**：赢家不是架构最清晰的那家。第三个说的是**钱**：资助这块地的人，已经换了一批。

这篇想做的事，是把这三件事连成一张图。

## 一、需求侧：人只有三到五个窗口

先把这个约束说清楚，因为后面所有的产品形态都是它的解。

DSH 那份说明里有一句话，比它的五个模块都重要：

> 单任务的上限取决于模型能力，多任务的上限取决于人的注意力。

他们的观察是，一个人通常只能同时跟进 3 到 5 个活跃 Session。这个数字没有给样本量和测量方法，只能算观察；但每一个同时开过四个对话窗口的人，都知道它大概是真的。第四个窗口里，你已经不记得前面说过什么了。

有意思的是，同样的判断在三个完全不同的地方各出现了一次。

**Anthropic 那边**，Felix Rieseberg 在九月底那篇讲自己重做主页的文章里写：

> 我给每个项目配了一个 Claude，由它去管任务、调查和线程。我们谈目标更多，谈怎么实现更少。

他的做法是一个 Project 统管一堆线程，60 多个线程在云端各有一台电脑，共享一个文件夹和一份记忆。这还是"一个入口"——只不过入口是 Project，不是 Session。

**DS-Bot 那边**，入口是群聊里的 Chief。你只跟 Chief 说话，它决定把活派给哪个 bot；bot 之间用 @ 接力，群聊有独立记忆。

**ADE 那边**，入口是整个工作台。Zeta 的定义是 agent development environment（ADE），不是"带聊天面板的 IDE"；它把会话定为工作单位，把终端、编辑器、插件和 `agent://` mesh 收进同一个界面。

三个产品，三个层级，同一个形状：**用户面对一个入口，背后是很多个执行者。**

这就是需求侧的全部。它不需要被论证，只需要被承认：人的注意力是稀缺资源，而 Agent 越多，稀缺得越快。

## 二、供给侧：五层楼都在争同一个入口

于是每一层都想成为那个入口。

<figure>
<svg viewBox="0 0 680 330" width="100%" role="img" aria-label="争夺同一个入口的五层楼">
<title>操作系统、ADE、Harness、Bot、中转站五层，各自都在往"唯一入口"的位置上挤</title>
<defs>
<marker id="fl1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</marker>
</defs>
<rect x="230" y="18" width="220" height="46" rx="8" fill="#633806" stroke="#FAC775" stroke-width="0.5"/>
<text x="340" y="38" font-size="13" font-weight="500" fill="#FAEEDA" text-anchor="middle">唯一的入口</text>
<text x="340" y="55" font-size="10" fill="#FAC775" text-anchor="middle">用户的注意力只够放在这里</text>
<line x1="340" y1="64" x2="340" y2="86" stroke="#FAC775" stroke-width="1.5" marker-end="url(#fl1)"/>
<rect x="30" y="90" width="120" height="52" rx="6" fill="#0C447C" stroke="#85B7EB" stroke-width="0.5"/>
<text x="90" y="110" font-size="11" font-weight="500" fill="#E6F1FB" text-anchor="middle">操作系统</text>
<text x="90" y="127" font-size="10" fill="#85B7EB" text-anchor="middle">Omarchy</text>
<rect x="164" y="90" width="120" height="52" rx="6" fill="#0C447C" stroke="#85B7EB" stroke-width="0.5"/>
<text x="224" y="110" font-size="11" font-weight="500" fill="#E6F1FB" text-anchor="middle">ADE / 工作台</text>
<text x="224" y="127" font-size="10" fill="#85B7EB" text-anchor="middle">Zeta</text>
<rect x="298" y="90" width="120" height="52" rx="6" fill="#0C447C" stroke="#85B7EB" stroke-width="0.5"/>
<text x="358" y="110" font-size="11" font-weight="500" fill="#E6F1FB" text-anchor="middle">Harness</text>
<text x="358" y="127" font-size="10" fill="#85B7EB" text-anchor="middle">DeepSeek Harness</text>
<rect x="432" y="90" width="120" height="52" rx="6" fill="#0C447C" stroke="#85B7EB" stroke-width="0.5"/>
<text x="492" y="110" font-size="11" font-weight="500" fill="#E6F1FB" text-anchor="middle">Bot / 群聊</text>
<text x="492" y="127" font-size="10" fill="#85B7EB" text-anchor="middle">DS-Bot / 豆包工作</text>
<rect x="566" y="90" width="84" height="52" rx="6" fill="#0C447C" stroke="#85B7EB" stroke-width="0.5"/>
<text x="608" y="110" font-size="11" font-weight="500" fill="#E6F1FB" text-anchor="middle">中转站</text>
<text x="608" y="127" font-size="10" fill="#85B7EB" text-anchor="middle">OpenCode</text>
<line x1="90" y1="142" x2="200" y2="176" stroke="#85B7EB" stroke-width="1.2" marker-end="url(#fl1)"/>
<line x1="224" y1="142" x2="280" y2="176" stroke="#85B7EB" stroke-width="1.2" marker-end="url(#fl1)"/>
<line x1="358" y1="142" x2="358" y2="176" stroke="#85B7EB" stroke-width="1.2" marker-end="url(#fl1)"/>
<line x1="492" y1="142" x2="436" y2="176" stroke="#85B7EB" stroke-width="1.2" marker-end="url(#fl1)"/>
<line x1="608" y1="142" x2="516" y2="176" stroke="#85B7EB" stroke-width="1.2" marker-end="url(#fl1)"/>
<rect x="180" y="180" width="320" height="44" rx="8" fill="#501313" stroke="#F7C1C1" stroke-width="0.5"/>
<text x="340" y="199" font-size="12" fill="#FCEBEB" text-anchor="middle">共同的动作：把别人的能力收进自己的默认路径</text>
<text x="340" y="216" font-size="10" fill="#F7C1C1" text-anchor="middle">插件 → 内置；会话 → 项目；模型 → 订阅；工具 → 市场</text>
<line x1="340" y1="224" x2="340" y2="244" stroke="#F7C1C1" stroke-width="1.5" marker-end="url(#fl1)"/>
<rect x="120" y="248" width="440" height="40" rx="8" fill="#0F6E56" stroke="#9FE1CB" stroke-width="0.5"/>
<text x="340" y="266" font-size="12" fill="#E1F5EE" text-anchor="middle">代价：中间层被跳过，用户只看见最上面那一层</text>
<text x="340" y="281" font-size="10" fill="#9FE1CB" text-anchor="middle">开源项目、社区插件、独立维护者，都在这一层</text>
<text x="340" y="312" font-size="11" fill="currentColor" text-anchor="middle">五层不是并列的，是同一场入口之争的五个楼层。</text>
</svg>
<figcaption>每一层都在做同一件事：把下面的能力收上来，变成自己的默认路径。</figcaption>
</figure>

| 层 | 代表 | 它卖的东西 | 它的失败模式 |
| --- | --- | --- | --- |
| 操作系统 | Omarchy | 默认 agent、默认主题、默认工具链 | 硬件兼容、发行版政治 |
| ADE / 工作台 | Zeta | 会话、插件、终端、mesh | 多仓库仍是多个 workspace |
| Harness | DeepSeek Harness | Router/Worker、事件、权限 | 只有规范，没有分发 |
| Bot / 群聊 | DS-Bot、豆包工作 | 一个 Chief、一个群、一份记忆 | 费用、上下文、信任 |
| 中转站 | OpenCode Zen、Command Code | 一个 API key、一张账单 | 上游降价、封禁、第一方替代 |

看起来是五个赛道，其实是同一场比赛：**谁把入口做进用户的默认路径，谁就拿到下一层的分发。**

### OS 这一层：为什么是 Linux

五层楼里，操作系统这一层看起来最不像"入口"，但它离 agent 最近。

2026 年这条线上的动作很密集：Canonical 在 6 月把 NVIDIA 的 OpenShell 运行时打包成 snap，给 Ubuntu 上的 agent 工作流做隔离、策略检查和资源计量；Ubuntu 的 2026 路线图把"本地推理 + agentic workflow"写成 OS 级能力；5 月底又发了针对 Google Cloud TPU 优化的 Ubuntu 镜像。SUSE 提了 agentic OS 的架构要求——策略、权限、回滚、审计、人工批准；阿里云 Linux 4 也出了 Agentic Edition。加上 Omarchy 这种"首次启动选 agent"的发行版，OS 层已经明确在争"默认 agent"的位置。

为什么是 Linux？因为 agent 需要的四件事，Linux 天生就有：

- **文本即接口**：配置是文本，日志是文本，包管理是文本；agent 能读、能改、能 diff。
- **可组合**：shell、管道、systemd、容器，把"做一件事"拆成可重放的步骤。
- **无头**：服务器没有桌面，agent 本来就应该跑在 SSH 后面。
- **可隔离**：namespace、cgroup、seccomp、容器，给"能执行命令的模型"划边界。

但"agent 原生"不是一个发行版标签，是一套**策略**：权限、计量、审计、回滚、人工批准。谁能把这套策略做成默认值，谁就拿到了 OS 层的入口。Ubuntu 用 snap 做隔离和更新，Omarchy 用"首次启动选 agent"做默认值，方向不同，争的是同一件事。

还有一个样本值得单独记：Linxira OS。它选的路线不是"首次启动选谁"，而是把 agent 的权限从主用户里分出来——独立的用户与用户组、按职责划分的 scoped capability、可审计可回收可枚举，而不是 sudo 临时提权。发行版本身不是概念：ISO 和 WSL 镜像都已经发布，93 款审核软件、签名仓库、双内核 + Timeshift 快照、无头模式都在里面；权限矩阵则是它正在落地的方向，按设计说明会在落地后公开。

更值得记的是它把"退出"写进了设计。底座是纯上游 Arch，所以整个系统可以拆成四层：签名源（迁到任何 pacman 系成本几乎为零）、Linxira 包层（普通 Arch 包，成本低）、桌面与会话接线（成本中等，冲突最集中）、引导与快照策略（成本最高，也是唯一可能让机器开不了机的一层）。因此"把上层迁到另一台 Arch 上"在理论上是可行的——反过来，把 Linxira 装到已有的 Arch 上，ISO 装机路径已经走通过一次；真正的一键接管工具还在路线图里，没有实现，而且设计成"先只读探测、再出计划、不满足就拒绝"，引导器改动必须单独确认。

那句原则值得抄下来：**一个会拒绝的接管工具，比一个到处都能用但会把人锁在门外的接管工具，要有用得多。**

这给"入口"提供了一个反例：入口不一定是牢笼。只要底座是开放的、上层是可迁移的，默认值可以同时是出口。问题是，大多数厂商没有动力这么做——退出太容易，留存就太难。

## 三、DSH 把这件事写得最清楚

在这一轮里，DeepSeek Harness 那份架构说明的位置很特殊：它不是产品发布，是一份**规范**。

这份说明里有一句话，比五个模块本身更重要：

> 相似的设计约束会导出相似的架构选择。

这句话解释了为什么 Omarchy、Felix 的 Projects、DS-Bot 的 Chief、Zeta 的 ADE 会长得越来越像。不是互相抄，是约束相同：人的注意力有限、环境事件不断、执行必须隔离、状态必须持久、失败必须能恢复。约束相同，解就会收敛。

所以这一轮真正稀缺的不是架构，是**把架构写成可比较、可移植、可批评的规范**。架构大家都在做；把它命名、分节、给出边界和实验的，只有少数。DSH 做的就是这件事——五个模块里没有一个新理论，但它把趋同的实践写成了可以被别人引用、反驳、移植的文本。

标准不是它发明的，是它先描述清楚的。那份说明的标题是《Exploring Super-agent Design: Towards a More Autonomous Agent System》——它先给了这件事一个名字，再给了它五个模块和两组实验。

但标准这件事，光有描述不够，还得有人背书。没有背书的规范只是一个好想法；有大厂背书、有真实负载、有下游愿意接，才会变成行业标准。DSH 的位置恰好卡在中间：它有 DeepSeek 的背书和内部负载，但分发还没起来。所以它能定义语言，还没能定义市场。

五个模块，每一个都能在操作系统里找到原型：

- **双层架构**：Router 管连续性和分派，Worker 管隔离执行。Router 不干活，Worker 不对话。
- **事件驱动**：Trigger 取代提示词；Fast Path / Slow Path 两级过滤；订阅 + 直通；Inline & Spill 管上下文；链式召回做多跳检索；投机执行提前动手。
- **面向人的交互**：`run()` 改成 `start()`，半双工变全双工；不同信道不同带宽，IM 一条回复不超过 100 词。
- **计算、状态与环境的分离**：计算无状态进容器，状态进数据库，环境留在原地，端侧只放一个 daemon。
- **Watchdog**：主系统之外挂一个独立的 Session，用定时消息驱动，判断"有没有实质进展"。

这五条不是概念拼盘，它们各自有实验支撑。那份说明里给了两组数：一组是消融——约 300 条消息、20 个工作请求、5 次运行，Super-agent 的 p50/p95 是 12.4/15.7 分钟，单 Session 方案在提示词中性时 p95 到 29.5 分钟，改成"优先委派"后仍然更慢；去掉直通机制，完成时间基本不变，但 Router 的决定数增加约 30%，读缓存 token 从 2323 万涨到 3177 万。另一组是 Router 的批处理——把 Trigger 到达速率从每分钟 1 条加到 40 条，平均 batch 从 1.0 升到 2.8，单次请求耗时只从 2.5 秒升到 3.9 秒，单个决定分摊的推理时间反而从 6.4 秒降到 1.6 秒。

这组数说明的不是"架构更好"，而是**架构把成本挪到了哪里**：用更多 token 换更短、更稳的完成时间；用直通省下 Router 的推理；用批处理把拥堵变成吞吐。

它最锋利的一句判断不是关于模型的：

> Session 应当是系统的实现细节，而不应是用户的认知负担。

这句话把过去两年 Agent 产品的默认形态掀了。现在几乎所有产品都是一个对话窗口等于一个 Session，用户自己负责记住"X 的上下文里有没有 Y"。DSH 说这是从 LLM API 继承下来的设计惯性——API 以 Session 为单位计费，产品就以为交互也该以 Session 为单位。

但规范强，不等于实现全。这个原型的 README 自己写得很清楚：文章里的一些设计是未来方向，原型里没有实现；它目前是一个**面向单个 GitHub 仓库**的主动 agent，监听 GitHub 和飞书，判断请求、开 Ticket、在独立 Session 里执行。

所以它是一份**先于实现的规范**。这既是它的价值，也是它的问题。

## 四、市场：赢的是分发，不是架构

现在把那三个数字里的第二个展开。

IDC 的 2025 年中国 AI 编程市场份额报告给出了一个很直白的排名：阿里第一，47.6%。整个市场 3.99 亿元，2026 年底预计 11.73 亿元。

这个榜单里都有谁：阿里云通义灵码 / Qoder、百度文心快码、腾讯云 CodeBuddy、字节 Trae、微软 GitHub Copilot、亚马逊 Q Developer、智谱 CodeGeeX、商汤 Raccoon、亚信图灵程序员。

没有 DeepSeek Harness。

把这几家的分发入口摊开，会看到它们根本不在同一个货架上竞争：

| 产品 | 归属 | 用户从哪里遇到它 |
| --- | --- | --- |
| 通义灵码 / Qoder | 阿里云 | 云控制台、IDE 插件、阿里云账号 |
| CodeBuddy | 腾讯云 | 腾讯云账号、微信小程序生态 |
| Trae / 豆包工作 | 字节 | 豆包 App、飞书、抖音生态 |
| 文心快码 | 百度 | 百度智能云、IDE 插件 |

这张表解释了一个常被误读的现象：**它们不是"更好的 Agent"赢了，是"更近的入口"赢了。** 用户在云控制台里点一下就能用，不需要知道什么是 harness。

这不奇怪，因为 IDC 量的是"AI 编程产品"的收入，不是一个 harness 的装机量——**口径不同**。但口径不同不影响一个事实：在国内开发者的日常里，占主导的是被塞进现有产品的那几款，不是架构最清晰的那一款。

字节这条线更典型。2026 年 8 月，TRAE、扣子团队整体并入豆包体系；8 月 25 日，"豆包工作"正式发布，和飞书深度打通，能读本地文件、操作软件、在虚拟桌面里点鼠标。豆包 App 的月活按 QuestMobile 2026 年 Q1 的口径是 3.82 亿，日均 token 消耗 120 万亿以上（厂商口径）。

一个人要装几个东西？一个豆包就够了。他不需要知道 Router 和 Worker 的区别。

DSH 的份额没有被审计过的数字。业内流传的说法是个位数百分比，也有"不到 8%"的估计，但没有公开口径，我不想把它写成统计结论——**能确认的是它不在第一梯队**。这句话的分量已经够了。

## 五、为什么"劣质 Agent"能赢

"劣质"是技术视角的评价。换成用户视角，那些产品至少做对了三件事。

**第一，预装。** 打开飞书就有，打开 IDE 就有，打开云控制台就有。用户不需要"再装一个东西"。而"再装一个东西"这个动作，在真实的 adoption 漏斗里，能筛掉九成的人。

**第二，账号。** 企业已经买了阿里云、腾讯云、字节的套餐，Agent 是套餐里的一项。采购不需要新立项，不需要新合同，不需要新的安全评估。**分发的最小单位不是安装包，是已有的合同。**

**第三，发票。** 这一条最不性感，也最要命。个人开发者可以刷信用卡订阅，企业不能。企业要发票、要合规、要等保、要私有化、要数据不出境。谁能开票，谁就能进企业；谁进企业，谁就有份额。

豆包工作是这三条同时成立的极端案例：2026 年 8 月 25 日发布，和飞书深度打通；此前的 8 月，TRAE 和扣子团队整体并入豆包体系。用户不需要装新软件，因为飞书已经开着；不需要新账号，因为豆包账号已经登着；不需要新合同，因为企业已经在用这套办公套件。**安装、账号、发票，三步全为零。**

技术视角看，这些产品可能架构粗糙、上下文管理原始、多任务能力弱。但它们赢在了**用户不需要做决定**。

这里有一个残酷的换算：一个架构领先两代的产品，和一个"打开就有"的产品，在获客成本上差的不是两倍，是一个数量级。而获客成本最终会变成研发预算，研发预算再变成下一代架构。**分发不是架构的结果，是架构的输入。**

## 六、补贴的货币变了

现在看第三个数字。

Omarchy 的赞助页把这轮资助结构直接印了出来，它自己把这页叫"Backed by the oligarchy"：

| 档位 | 例子 | 给的是什么 |
| --- | --- | --- |
| Founding Patrons（每人 100 万美元） | Tobi Lütke、Patrick Collison、Michael Dell、Jack Dorsey、Drew Houston | 现金 |
| Founding Corporate（100 万/年 ×3，或 150 万美元 tokens） | Meta Superintelligence Labs、DigitalOcean、阿里云、SpaceXSI | 现金 / tokens |
| Distinguished Corporate（10 万/年 ×3，或 15 万美元 tokens） | 1Password、37signals、Fireworks、OpenAI、OpenRouter、OrcaRouter、Namespace、Greptile | 现金 / tokens |

累计承诺 2365 万美元。

注意最后一列。**这一轮的赞助货币不只有现金，还有 tokens。**

150 万美元的 Grok tokens，对 xAI 的边际成本远低于 150 万美元——推理本来就要跑，闲置的算力也要折旧。但这笔"钱"同时完成了四件事：

1. 资助了一个有 133 万次 ISO 下载、4.6 万 star 的项目；
2. 在这个项目的默认 agent 列表里，给自己的 agent 留了一个位置；
3. 拿到了真实工作负载的评测数据；
4. 把一笔营销预算，记成了生态投入。

**一笔账，四个科目。** 这是现金赞助做不到的。

而独立开发者发不了这种货币。他只能掏现金，或者掏自己的时间。所以"赞助"这件事的门槛，在这一轮变成了：**你有没有一种边际成本接近零、但对方愿意收的东西。**

模型厂商有。云厂商有。中转站有一点（额度）。独立开发者没有。

## 七、中转站：依附点，也是最脆弱的一环

你说 OpenCode 和 Command Code 也是中转站，这个判断对，而且它们活得还不错。看它们的定价就明白这层生意怎么做。

**OpenCode** 有两条线：Zen 是按量网关，官方说按成本卖、只加 4.4% + $0.30 的支付通道费；Go 是 10 美元/月，封顶 12 美元/5 小时、30 美元/周、60 美元/月。它明确写"Use with any agent"——**网关和 agent 是两层**。

**Command Code** 是订阅制：GOAT 10 美元/月换 70 美元额度，覆盖 33–50 个模型，按模型谈不同倍数，旗舰能到 7 倍；自己也有桌面 agent、`/skills`、`/memory`、工具调用修复。它宣称 10 万+ 开发者、4 万+ 付费、130T+ tokens。

两家的共同点：**自己不生产模型，靠"批发—零售"的差和支付关系活着。**

而且它们的调用量不是小数目。OpenCode 的公开数据页显示，2026 年 11 月第一周，单是 `deepseek-v4.1-flash` 就跑了 124 万亿 token；排在后面的 GLM-5.3-Flash 是 6.4 万亿，不到它的 6%。

<figure>
<svg viewBox="0 0 680 330" width="100%" role="img" aria-label="OpenCode 2026 年 11 月第一周的模型 token 用量">
<title>OpenCode 周 token 用量：榜首一根柱子就是 124 万亿</title>
<text x="30" y="22" font-size="11" fill="currentColor">OpenCode 周 token 用量（2026-11-01 当周，单位：T = 万亿）</text>
<rect x="250" y="44" width="380" height="14" rx="2" fill="#0C447C"/>
<text x="30" y="55" font-size="10.5" fill="#E6F1FB">deepseek-v4.1-flash</text>
<text x="646" y="55" font-size="10" fill="#E6F1FB" text-anchor="end">124T</text>
<rect x="250" y="74" width="21" height="14" rx="2" fill="#633806"/>
<text x="30" y="85" font-size="10.5" fill="currentColor">muse-spark-1.3-contributor</text>
<text x="646" y="85" font-size="10" fill="currentColor" text-anchor="end">7.0T</text>
<rect x="250" y="104" width="20" height="14" rx="2" fill="#633806"/>
<text x="30" y="115" font-size="10.5" fill="currentColor">glm-5.3-flash</text>
<text x="646" y="115" font-size="10" fill="currentColor" text-anchor="end">6.4T</text>
<rect x="250" y="134" width="17" height="14" rx="2" fill="#633806"/>
<text x="30" y="145" font-size="10.5" fill="currentColor">beam-1.0-501b-a23b</text>
<text x="646" y="145" font-size="10" fill="currentColor" text-anchor="end">5.4T</text>
<rect x="250" y="164" width="12" height="14" rx="2" fill="#633806"/>
<text x="30" y="175" font-size="10.5" fill="currentColor">mimo-v2.6-flash</text>
<text x="646" y="175" font-size="10" fill="currentColor" text-anchor="end">3.8T</text>
<rect x="250" y="194" width="6" height="14" rx="2" fill="#633806"/>
<text x="30" y="205" font-size="10.5" fill="currentColor">iceman</text>
<text x="646" y="205" font-size="10" fill="currentColor" text-anchor="end">1.7T</text>
<rect x="250" y="224" width="5" height="14" rx="2" fill="#0C447C"/>
<text x="30" y="235" font-size="10.5" fill="#E6F1FB">deepseek-v4.1-flash-1017</text>
<text x="646" y="235" font-size="10" fill="#E6F1FB" text-anchor="end">1.4T</text>
<rect x="250" y="254" width="3" height="14" rx="2" fill="#633806"/>
<text x="30" y="265" font-size="10.5" fill="currentColor">gpt-6-luna</text>
<text x="646" y="265" font-size="10" fill="currentColor" text-anchor="end">924B</text>
<line x1="30" y1="284" x2="650" y2="284" stroke="currentColor" stroke-width="0.5" opacity="0.4"/>
<text x="30" y="300" font-size="10" fill="currentColor">口径：输入 + 输出 + 推理 + 缓存 token；只统计 OpenCode 用户，不代表全市场。</text>
<text x="30" y="316" font-size="10" fill="currentColor">数据：OpenCode Data（opencode.ai/data），2026-11-01。</text>
</svg>
<figcaption>榜首一根柱子就是 124 万亿 token/周；第二名不到它的 6%。这不是模型排行榜，是一个入口的吞吐量。</figcaption>
</figure>

这个量级解释了两件事：为什么中转站有生意——需求真实存在；以及为什么它们必须自部署——按量转卖的成本结构里，租金和利用率决定生死。

但自部署不等于独立。服务器是租的，机房是别人的，电是别人的。它们依旧是依附于云服务厂商的那一批，只不过依附点从"模型 API"往下挪了一层，变成了"算力租约"。

这层的护城河不是模型，是账单：信用卡、订阅、封顶、退款、发票、多模型比价。模型厂商不愿意为十万个小开发者做零售计费，所以这层有存在价值。

但它的议价能力最弱：

- 上游降价，它的差就薄了；
- 上游封禁或限流，它的供给就断了；
- 上游推出第一方 agent 并把价格打到零，它的存在理由就没了。

据公开表述，DeepSeek 还表示可以帮助其他厂商部署模型——这句话的潜台词是，模型厂商卖的不只是 API，还有部署能力。于是这条链变成：模型厂商卖部署，中转站租云自部署，开发者买订阅。每一层都在替上一层分担资本开支，也每一层都在被上一层卡住脖子。

算力这层还有一个容易被忽略的变量：DeepSeek 把生产用的推理框架 [DeepInfer](https://github.com/deepseek-ai/DeepInfer) 开源了（Apache-2.0，支持 NVIDIA SM100 和昇腾 950）。此前披露的经营数据是单卡每小时收入 38 美元——和同等算力拿去挖矿的收益比，这个数字高得不像话。它说明的不是"模型很赚钱"，是**推理的工程效率可以改变一张卡的用途**。

这也解释了为什么租服务器是常态：服务器是重资产，买卡只是第一笔，后面还有机房、电力、网络、运维、折旧；租赁把资本开支变成运营开支。轻资产的中转站因此能活，但也因此永远被租约和电价卡着。资金来源和算力来源，在这里变成了同一个导向：谁能让单位算力产出更高，谁就有资格补贴；谁只能转租，谁就只能赚差价。

有一种在圈内流传的说法：一定数量的 GB300，就能覆盖全世界"总量"意义上的 token 用量。这个说法只在"总量"口径下成立——它算的是 token 数，不是智能；真要把前沿模型的推理也算进去，成本立刻上一个量级。但它点出了一个事实：**开源模型的推理正在变成一种可以按吨卖的大宗商品。**

所以中转站看起来是赞助者，实际上是**整条链上最先感受到压力的一环**：对上游没有定价权，对下游没有锁定力。厂商越卷，它的利润越先被压薄；利润薄到撑不住，依附它的独立开发者就要重新找依附点。

## 八、依附结构：从云到模型，再到中转站

把依附点排成一张表，会看到每一轮的"买的东西"都不一样。

先看上一轮的样本：Rust 和 Linux。两者都有基金会，背后是一排商业公司，也有大量散点开发者。但它们的共同点是——**代码就是产品**。资助者买的是"这门语言继续存在""这个内核继续维护"，而不是"用户第一次打开时用我的服务"。所以中立性可以靠结构实现：捐赠者众多、没有一个人握着方向盘、代码本身可以被任何公司使用而不改变其行为。

这一轮的变量是：底座变成了一个每季度都在变的模型。代码还是开源的，但**行为不是**。

| 依附点 | 它买什么 | 它怎么失效 |
| --- | --- | --- |
| 云厂商 | 工作负载最终落在自己机房的概率 | 多云策略、自建、迁移 |
| 基金会 | 中立性本身 | 捐赠集中度上升，投票权跟着钱走 |
| 商业公司 | 自己产品需要的上游能力 | 战略转向、被收购 |
| 模型厂商 | 默认值：文档首例、脚手架、推荐模型 | 第一方功能直接覆盖你 |
| 中转站 | 差价与支付关系 | 价格战、封禁、合规 |

关键不在数量，在**可替代性**。

云厂商不给你钱，你还能换一家云；模型厂商不给你额度，你也可以换模型——但换完之后，你的产品行为会变，因为底座换了。这是前几轮没有的性质：**换赞助商不改变产品，换模型厂商会改变产品。**

所以"中立"要重新定义。不是资助者多，而是**没有任何一个资助者能用第一方功能替代你**。

Omarchy 的做法是把中立放在产品层：首次启动让你从 Claude、Codex、Copilot、Crush、xAI、Hermes、Muse、oh-my-pi、OpenClaw、OpenCode、OpenRouter、pi-mono 里挑一个默认 agent。产品层确实中立。但资助层不中立——名单上同时坐着这些 agent 的厂商。

这不矛盾，也不虚伪。它只是说明：**产品层的中立，和资助层的中立，是两件事。** 前者可以设计，后者只能靠结构。

## 九、中间层塌陷

把上面这些放在一起，会得到一个比"开源会不会死"更准确的判断。

开源要分三层看：

| 层 | 会不会消失 | 真实风险 |
| --- | --- | --- |
| 代码 | 不会 | 许可证还在，仓库还在，fork 还在 |
| 维护者 | 会 | 被雇佣、被赞助、被收编，全职投入变成兼职 |
| 分发 | 会 | 插件市场、skills 仓库、脚手架默认值被平台接管 |

危险的不是代码消失，是**维护这份代码的人**和**别人找到这份代码的路径**同时被接管。代码还在，但没人有整块时间维护，也没人从默认入口进来——这是"活着但不再生长"的状态，比删库更常见。

于是真正被挤掉的是中间层：hobby 项目活得下去，大厂第一方项目活得很好，夹在中间、靠一个小团队和一套商业计划支撑的那一层被挤掉。

判断标准不是"还有没有开源项目"，而是"**还有没有不依附于任何一家的全职维护者**"。

但"塌陷"不等于"清零"。开源的潮流不会结束，开源模型和闭源模型的斗争也不会结束——只要闭源模型还在定价，开源模型就永远有存在的理由；只要还有一家厂商不愿意把命脉交给别人，中立层就永远有客户。被挤掉的是中间那层的商业模式，不是开源这件事本身。

这个形状和 10-19 那篇讲就业中间层是同一个结构，只是换了一个市场：两头都活着，中间那层被抽走了梯子。

## 十、Felix 的三篇：执行便宜之后

Anthropic 的 Felix Rieseberg 这两个月写了三篇，正好构成一条线。

**第一篇，10 月 27 日，《Hunger beats tenure》**（5 分钟阅读，不是长文）。他这个月不再让候选人做传统编程题了——注意，这是他作为 hiring manager 自己的做法，不是 Anthropic 的全公司政策。理由：一道 React 小题，Claude 已经做得比人好；团队里最有影响力的人，成功和这些测试成绩无关。

他看到的趋势是：资历浅的工程师正在超过写代码更好、工龄更长的人。

> Hunger beats tenure.

新人有两个东西：新鲜的眼光，和没人在乎你怎么想。前者是优势——1991 年 James March 就写过，组织依赖"持续流入的幼稚与无知"；后者是短板——过去执行很贵，你得先熬出地位，公司才肯押注你的想法。

但现在：

> Execution isn't expensive anymore.

他给的五条建议是：盯业务影响而不是待办清单；想一个激进的点子；用一个周末做出能跑的原型；一个原型只讲一个好点子；用好你的新鲜视角。

例子是 Claude Code 的图形界面：两位较新的工程师用一个周末做出原型，大约八天后首个公开版本上线。

**第二篇，10 月 13 日，《How to be more ambitious》**（8 分钟）。他把"更有野心"拆成四种：

- **Speed**：同样的活更快做完。这是 AI 经济价值的基本盘，但不需要创造力。
- **Altitude**：往上走一层，考虑结果而不是任务。他以前让 Claude 修单个崩溃，后来让 Claude"让我们的应用不崩"。
- **Depth**：用领域顶尖专家的工具和方法，而不是换一套词汇。他有一条很硬的建议：**不要让模型自己评判自己，坚持外部验证。**
- **Range**：从多个领域借视角。把名词换成动词，再"组一个剧组"。

**第三篇，9 月 27 日，《Made by mechanical means》**（13 分钟）。他重做自己的主页，没碰代码、没开 GitHub、没跑本地命令：60 多个线程在云端各有一台电脑，共享一个文件夹和一份记忆，互相做对抗式 QA。

> 我给每个项目配了一个 Claude……我们谈目标更多，谈怎么实现更少。

> 我不读那些代码。

这三篇合起来，其实在描述同一次迁移：**入口从"会话"变成了"目标"。**

第一篇说执行便宜了，所以资历不值钱；第二篇说价值在 Altitude，也就是"你定义的那个目标"；第三篇说产品形态已经跟上了——一个 Project 管一堆线程，人只谈目标。

他为什么敢这么讲？因为"野心"这件事本身有研究支撑。Locke 和 Latham 把 35 年的目标设定研究捋了一遍，结论是：给出**具体的、难的目标**，比笼统地说"尽力而为"表现更好。Dantzig 把黑板上的两道题当作业交上去，因为不知道那是未解问题；四分钟一英里的纪录破了之后，46 天内就有人重复。这些例子都在说同一件事：**人不是被能力限制，是被"什么算可能"限制。**

而模型恰好擅长把"什么算可能"往前推一格。所以"更有野心"不是鸡汤，是一种可以被工程化的方法：把目标抬高、把工具换成专家用的、把验证交给外部。

这和 DSH 的 Router/Worker 是同一件事的两种说法：一个从组织行为讲，一个从系统架构讲。

## 十一、hunger 打得过 tenure，打不过 default

但这里要加一个限定，否则会得出一个过于乐观的结论。

**执行便宜了，分发没有便宜。**

一个周末能做出原型，这是真的。原型被谁看见、被谁的插件市场收录、被谁的脚手架默认推荐——这三件事一件都没变便宜。Felix 招人时可以看 portfolio 里的原型，因为他是入口；独立开发者的原型没有这个入口。

所以：

> Hunger beats tenure，但 hunger 打不过 default。

在公司内部，这句话成立，因为公司本身就是一个入口：你的原型只要能说服你的 manager，就能拿到分发。在市场上，这句话要打折：你的原型要说服的不是一个人，是一个排序算法、一个采购流程、一个默认配置。

这也解释了为什么"新人优势"和"开源困境"会同时出现：**供给端在爆炸，需求端的注意力没有变。** 原型越多，被看见的概率越低；被看见的概率越低，默认值的价值越高。

## 十二、真正的分岔：按仓库分，还是按 Agent 分

多仓库这件事，看起来是"支持几个目录"，其实是一个架构选择：**你把什么当作分区单位。**

两种常见的分法：

- **按仓库分**：一个仓库一个 workspace、一个 session，入口是仓库列表。跨仓库要么加额外根目录，要么开一个跨仓库任务面板。
- **按 Agent 分**：一个 Agent 一个持久身份、一份自己的上下文记忆（可增可减，存成 JSONC 这类可读配置），多个 Agent 组群，各自维护各自的部分，入口是群。

DSH 的官方逻辑给了第三种答案：**按任务 / 线程分**。Session 是实现细节，Router 管连续性和分派，Worker 管隔离执行，事件按 Thread 订阅直通。仓库、Agent、记忆都是这个结构里的资源，不是分区单位。

这三种分法一对比，就能看出"一个入口"为什么难：入口不是 UI，是**绑定关系**——哪个 Agent 拥有哪个仓库、哪份记忆、哪条线程。没有这个绑定标准，每个产品都得自己发明一套。

Zeta 现在的状态，正好卡在这条缝上。当前版本 1.4.7，`main/` 目录是 AGPL-3.0，其余是 MIT。

**能用的部分。** 一个仓库、一个入口是通的。GUI 把所有注册过的项目列在同一个壳里；一个会话可以用 `/add-dir` 挂额外根目录；核心的 `agent://` mesh 支持同机跨进程发消息、同机会话互发，`agent://all` 可以做广播；10 秒心跳、60 秒过期，角色里预留了 `team-host` 和 `team-member`。

**编排在插件里，而且真的能跑。** 共享房间、任务认领、文件预留、lead + workers 的编排，在可选插件 `pi-messenger` 里。它不是"文档里存在"：`zetacode plugin link` 装上即启用，`plugin doctor` 通过，真实加载器零错误注册了 1 个工具和 3 个命令；crew 不会后台常驻，只有显式调用 `pi_messenger` 或 `/teamagent` 才起子进程。

之所以用一个外部插件来做这套编排，不是为了省事，是两条更硬的理由：**开源社区的意义就是避免重复开发**——别人已经把 lead+workers 写出来了，重写一遍不会更好；以及**这套设计真的有用**——共享房间、任务认领、文件预留，恰好是"多个 Agent 各自维护自己的上下文"所需要的最小结构。这次移植还把上游 v0.15.2 之后的三个修复补了回来，INDEX 里记了上游 SHA，冒烟测试变成了永久测试。

**没闭合的部分。**

- 多仓库仍是多个 workspace、多个 session，跨仓库任务面板还在 roadmap 里。
- 插件不是默认安装：没有商店、没有推荐清单，`marketplace` 和 `discover` 都是空的；装上即启用，但"装"这个动作要用户自己做。
- 离 DSH Agent Teams 还有三条硬差距：worker 是子进程（`spawn zetacode`），不是可续传的会话，没有 ACP；状态在插件私有 JSON 里，不在会话日志里，崩了不可恢复、不可审计；单机、单 cwd，没有跨仓跨机。

所以现在的雏形是"能用"，不是"完成"。而且这不只是 Zeta 的问题：OMP 上游也在等 DSH 这边的官方标准，社区已经有真实的跨 harness 插件移植案例——大家都在等一个**绑定规范**：仓库、Agent、上下文、线程，四者怎么对应。

DSH 先把规范写了出来，这是它最值钱的地方；但它自己也只是原型。Zeta 这种 ADE 的选择是：先把能用的部分做出来，同时等上游把标准定下来。这个"等"不是消极，是这一层的真实成本——**你在一个还没定标准的楼层上盖房子，就得随时准备重做绑定。**

顺带一句：这条线上我们自己也交过学费。先做过一个 OpenCode 插件和一个 Rust 运行时，最后都并回了 Zeta——因为它们各自只解决了五层楼里的一层，而用户要的是整栋楼。

## 十三、接下来：三种情景

不给预测，给三种可以分别观察的情景。

**情景 A：模型厂商第一方吞掉入口。**
模型厂商把 harness、bot、工作台一起做进自己的产品，用 tokens 补贴换默认值。中转站的差价被压平，社区插件被内置，中间层最先消失。判断信号：第一方插件替代社区插件的速度、免费额度的覆盖范围。

**情景 B：中转站联合成"多模型中立层"。**
像 OpenRouter 那样，把"一个 API key 跑所有模型"做成基础设施，靠支付和路由活着。模型厂商需要它触达长尾，它需要模型厂商供货。判断信号：中转站的毛利、被封禁的频率、是否开始做自己的 agent。

**情景 C：OS / ADE 成为新的中立层。**
像 Omarchy 那样，把 agent 变成操作系统的公民，谁来都行；像 Zeta 那样，把会话、插件、终端收进一个工作台。判断信号：默认 agent 是否可换、插件市场是否开放、赞助人是否分散。

这也是为什么"多家并存"不是一句口号。奥特曼在十月末那场 Cheeky Pint 里说，他不要一个全知全能的神，要很多个略超人类智慧的 AI 组成社会；把这个说法挪到产业上，就是多家模型、多家厂商相互制衡，比一家独占更可控。

三种情景不互斥。更可能的是：A 吃掉大部分，B 活在长尾，C 守住一小块"我要自己控制"的人。

这三种情景之前，还有一个前置变量：**绑定标准**。如果 DSH / OMP 这一系先把"仓库—Agent—上下文—线程"的对应关系定下来，ADE 和 harness 就能长在同一套语义上，社区移植也会从"一个个搬插件"变成"按规范接"；如果标准一直定不下来，每一层都会继续造自己的绑定，入口之争就会退化成适配之争。谁定标准，谁就拿到了下一层的默认值。

## 十四、看什么：六个可查的量

不给结论，给六个能查的东西。

1. **默认安装率**：一个新用户从零到用上 Agent，需要几步？超过三步，分发就还没解决。
2. **企业采购份额**：IDC 这类报告的排名，比任何发布会都诚实。
3. **插件市场排序**：社区插件在第一屏出现的比例。这个比例下降，说明平台开始收口。
4. **资助集中度**：一个项目前三大资助方占比。超过一半，中立性就开始变成修辞。
5. **中转站毛利**：这条链上最早出问题的一环。
6. **权重可及性**：open weights 是不是真的能改。下载不等于 fork。

## 十五、入口是新的内核

回到开头那三个数字。

3–5 个窗口，是人的上限；47.6%，是分发的答案；2365 万美元，是资助的结构。三个数字指向同一件事：**这一轮竞争的核心不是模型能力，是入口。**

入口这个东西，表面上是产品设计，底层是分发，最底层是账单。谁能定义"第一次打开时用谁"，谁就拿到了后面所有的默认值。

而这件事对一个写代码的人来说，意味着两件相反的事。

坏消息是：**架构的清晰度不再是护城河。** 你可以把 Router/Worker 写得比谁都清楚，把 Inline/Spill 讲得比谁都透，但如果用户打开电脑时看不见你，这些都不会变成份额。

但还有一层：趋同不可怕，可怕的是趋同之后没有名字。有了名字，别人才可以比较、移植、反驳；没有名字，每一家都要重新发明一遍词汇，而重新发明的那套永远长不出生态。

好消息是：**执行便宜之后，定义问题的能力变贵了。** Felix 说的 Altitude，DSH 说的"Session 不该是认知负担"，其实是同一件事——谁能在更高的抽象层上把问题说清楚，谁就值得被放进那个入口。

这套架构越像操作系统，这个问题就越绕不开：**内核是谁的。**

仓库可以 fork，默认值不行。规范可以抄，但先把它写下来的那个人，定义了后来者讨论它的语言。

---

**口径说明。** 文中"3 到 5 个活跃 Session"来自 DSH 团队的观察，没有样本量与测量方法，不能当作统计结论。IDC 的 47.6% 是其 2025 年中国 AI 编程产品市场份额口径，量的是产品收入，不等于 harness 的装机量；DSH 的具体份额没有审计数字，文中只写"不在第一梯队"，不引用未经核实的百分比。豆包的 3.82 亿月活与 120 万亿日均 token 来自厂商与第三方口径混用，仅作量级参考。Omarchy 的 2365 万美元是官网列出的"承诺"总额，不等于已到账现金，其中包含 tokens 形式的赞助。OpenCode 与 Command Code 的定价、倍数与用户数均来自其官网或公开评测，未独立复现。Felix Rieseberg 的三篇原文分别发表于 2026 年 10 月 27 日、10 月 13 日、9 月 27 日。Zeta 一节基于 1.4.7 源码与 README（2026-10-30）的只读核对，并用真实 CLI 复跑了插件安装与加载链路；"多仓库仍是多个 workspace""跨进程共享房间与团队编排在插件里""插件不默认安装、无商店"三条已确认；"核心有 mesh 与 agent://all 广播"同样已确认。OpenCode 的 token 数据来自其公开数据页 2026-11-01 当周口径，只代表 OpenCode 用户，不代表全市场。DeepInfer 的 38 美元/卡/小时来自此前披露的经营数据（10-24 那篇已拆过），不是仓库 README 里的数字；Ubuntu、SUSE、阿里云 Linux 的 agent 动作来自各自 2026 年的公开博客与路线图，"agentic OS"在业内没有统一定义。Linxira OS 一节基于其官网、文档与两篇设计说明（2026-09-27、2026-09-22）；其中"一键接管到已有 Arch"仍是路线图规划，尚未实现，文中已注明；已发布的是 ISO 与 WSL 镜像、93 款审核软件、签名仓库与快照机制。

参考：[Hunger beats tenure](https://felixrieseberg.com/hunger-beats-tenure-advice-for-junior-engineers/)、[How to be more ambitious](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/)、[Made by mechanical means](https://felixrieseberg.com/made-by-mechanical-means/)；[Omarchy](https://omarchy.org/) 与其赞助人页；[OpenCode Zen](https://opencode.ai/zen)、[OpenCode Go](https://opencode.ai/go)、[OpenCode Data](https://opencode.ai/zh/data)；[Command Code](https://commandcode.ai)；[dsh-superagent 原型](https://github.com/deepseek-ai/dsh-superagent-prototype)（含《Exploring Super-agent Design》一文所指的原型）；[pi-messenger 上游](https://github.com/nicobailon/pi-messenger)；[DeepInfer](https://github.com/deepseek-ai/DeepInfer)；[Canonical 的 OpenShell snap](https://canonical.com/blog/nvidia-openshell-ubuntu-announcement)、[Ubuntu 的 AI 路线图](https://discourse.ubuntu.com/t/the-future-of-ai-in-ubuntu/81130)；[Linxira OS](https://linxira-os.github.io/zh/)、[就地接管的设计说明](https://linxira-os.github.io/zh/blog/arch-adoption/)、[agent 权限与 Omarchy 的对比](https://linxira-os.github.io/zh/blog/omarchy-agents-and-full-bootstrap/)；IDC 2025 年中国 AI 编程市场份额报告。
