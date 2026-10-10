---
title: 何为 FDE：五个分量、九个阶段与一条判定线
description: FDE 常被解释成「懂技术、懂业务、能出差」——三句形容词，一个都不能检验。这篇把它拆到可判定的粒度：五个分量构成一个乘积模型，任一为 0 则整体退化；再用一条九段生物信息管线检验这五项，并说明溢价为什么不均匀地压在首尾两端。
publishDate: 2026-10-10
tags: [职场, 技术拆解, 生信技术]
draft: false
---

<!-- 本文 SVG 配图的主题变量：颜色跟随站点主题（见 src/assets/styles/app.css 的 --primary / --foreground / --muted），.dark 由主题脚本挂在 <html> 上。 -->

<style>
  .fde-fig {
    --fde-fg: hsl(var(--foreground));
    --fde-dim: hsl(var(--muted-foreground));
    --fde-line: hsl(var(--border));
    --fde-fill: hsl(var(--muted));
    --fde-acc: hsl(var(--primary));
    --fde-warn: hsl(28 88% 44%);
    margin: 2.25rem 0;
  }
  .dark .fde-fig {
    --fde-warn: hsl(32 90% 62%);
  }
  .fde-fig svg {
    display: block;
    width: 100%;
    height: auto;
  }
  .fde-fig figcaption {
    margin-top: 0.7rem;
    font-size: 0.82em;
    line-height: 1.6;
    color: hsl(var(--muted-foreground));
    text-align: center;
  }
  .fde-c1 {
    --fde-c: hsl(205 72% 40%);
  }
  .fde-c2 {
    --fde-c: hsl(158 52% 30%);
  }
  .fde-c3 {
    --fde-c: hsl(30 84% 38%);
  }
  .fde-c4 {
    --fde-c: hsl(264 52% 48%);
  }
  .fde-c5 {
    --fde-c: hsl(340 62% 44%);
  }
  .dark .fde-c1 {
    --fde-c: hsl(205 78% 68%);
  }
  .dark .fde-c2 {
    --fde-c: hsl(158 48% 58%);
  }
  .dark .fde-c3 {
    --fde-c: hsl(34 88% 64%);
  }
  .dark .fde-c4 {
    --fde-c: hsl(266 64% 76%);
  }
  .dark .fde-c5 {
    --fde-c: hsl(342 66% 72%);
  }
</style>

## 〇、一个被叫烂了的词

今年秋招，FDE 从招聘软件里的一个生词变成了热词。AI 公司把它从数据公司那里借过来，贴在了「把模型送进客户现场」的角色上；媒体开始算岗位增速，培训号开始卖课。热度上来了，定义没跟上——翻遍能找到的解释，基本是三句话：**懂技术、懂业务、能出差**。

这三句全是形容词。形容词的问题是没法检验：一个人是不是「懂业务」，取决于谁在评价；「能出差」更省事，直接把工作地点当成了能力。一个不能被检验的定义，最后一定会变成一顶谁都戴得上的帽子——这正是它此刻正在发生的事。

这篇要做的是一件更窄的活：**把这个角色拆到可判定的粒度**。拆法是把 FDE 展开成五个分量：

**FDE = 工程能力 × 领域理解 × 现场嵌入 × 端到端交付 × 产品回流**

（五个分量的英文首字母有两对撞车——Domain 与 Delivery、Field 与 Feedback——所以下文一律用中文词，不套缩写，免得读混。）

后面按这个顺序走：先说每个分量买的是什么、缺了会退化成什么；再说为什么这五项是**乘数**而不是加数，以及乘法模型自己会在哪里失效；最后拿一条真实的九段管线把它跑一遍——从问题定义一直跑到生物学解释。

先把话说在前面：**五个分量的拆法是本文的分析框架，不是哪家公司的官方定义。** 它的合法性不来自权威，来自它能不能被证伪——下一节每个分量都给一条可观察的判据；凡是给不出来的，我承认那只是形容词。

## 一、这个词从哪来

FDE 不是 AI 时代的发明。把这个具名角色追到源头，是 Palantir：这家公司把自己的工程师派进客户设施，一待数周甚至数月，在客户的内网里写生产代码。公司内部把他们叫 Delta，与写平台的产品工程师（Dev）相区分——**Dev 是「一个能力卖给很多客户」，Delta 是「一个客户身上做很多能力」**（[Palantir 官方博客《Dev versus Delta》](https://blog.palantir.com/dev-versus-delta-demystifying-engineering-roles-at-palantir-ad44c2a6e87)）。「forward deployed」这个说法借自军事用语，指的是部署在前线、而非留在后方基地的单位。

Palantir 自己反复澄清的一件事，恰好是这篇要拆的核心：Delta 不是咨询顾问。「顾问通常交付一次性的分析、建议或方案，而我们和客户一起建的是能持续改进的长期方案」；另一位前线工程师说得更直白——**这份工作做的是把已有的软件产品部署出去、换成客户的业务结果**，技术工作量「远多于咨询」（[《A Day in the Life of a Palantir FDSE》](https://blog.palantir.com/a-day-in-the-life-of-a-palantir-forward-deployed-software-engineer-45ef2de257b1)）。

仔细看这段公司内部定义，五个分量里有四个已经在了：工程（写生产代码）、领域（拿业务结果）、现场（驻在客户那儿）、交付（部署出去）。第五个——**产品回流**——同样是官方定义的一部分，不是外部附加的善意：Palantir 明确写着，前线工程师有责任把现场的技术认知带回产品团队，「我们一些最有价值的产品能力，就是从现场这么长出来的」。

所以下面这五个分量不是凭空发明，而是把一个公司定义里本来就有、但混在一起说的东西逐项拆开，各自配上判据。拆开的理由很实际：**混着说的时候，你没法判断一个人缺的到底是哪一项。**

## 二、五个分量：把形容词换成判据


<figure class="fde-fig">
<svg viewBox="0 0 720 400" role="img" aria-label="FDE 的五个分量：工程能力、领域理解、现场嵌入、端到端交付、产品回流，以及各自缺位后的退化形态">
  <text x="16" y="20" font-size="13" font-weight="600" fill="var(--fde-fg)">五个分量：每一个都要可判定，而不是可形容</text>
  <g class="fde-c1">
    <rect x="16" y="36" width="688" height="64" rx="10" fill="var(--fde-c)" fill-opacity="0.07" stroke="var(--fde-c)" stroke-opacity="0.4"/>
    <rect x="16" y="36" width="5" height="64" rx="2.5" fill="var(--fde-c)"/>
    <rect x="42" y="50" width="46" height="36" rx="8" fill="var(--fde-c)" fill-opacity="0.16"/>
    <text x="65" y="74" font-size="15" font-weight="600" text-anchor="middle" fill="var(--fde-c)">01</text>
    <text x="104" y="62" font-size="15" font-weight="600" fill="var(--fde-fg)">工程能力 · Engineering</text>
    <text x="104" y="84" font-size="12" fill="var(--fde-dim)">买的是：能把方案变成在跑的系统，而不是只能演示的原型</text>
    <text x="688" y="74" font-size="12" text-anchor="end" fill="var(--fde-dim)">缺位 → 报告工厂</text>
  </g>
  <g class="fde-c2">
    <rect x="16" y="108" width="688" height="64" rx="10" fill="var(--fde-c)" fill-opacity="0.07" stroke="var(--fde-c)" stroke-opacity="0.4"/>
    <rect x="16" y="108" width="5" height="64" rx="2.5" fill="var(--fde-c)"/>
    <rect x="42" y="122" width="46" height="36" rx="8" fill="var(--fde-c)" fill-opacity="0.16"/>
    <text x="65" y="146" font-size="15" font-weight="600" text-anchor="middle" fill="var(--fde-c)">02</text>
    <text x="104" y="134" font-size="15" font-weight="600" fill="var(--fde-fg)">领域理解 · Domain</text>
    <text x="104" y="156" font-size="12" fill="var(--fde-dim)">买的是：把「帮我看看」翻译成可判定、可证伪的问题</text>
    <text x="688" y="146" font-size="12" text-anchor="end" fill="var(--fde-dim)">缺位 → 需求翻译机</text>
  </g>
  <g class="fde-c3">
    <rect x="16" y="180" width="688" height="64" rx="10" fill="var(--fde-c)" fill-opacity="0.07" stroke="var(--fde-c)" stroke-opacity="0.4"/>
    <rect x="16" y="180" width="5" height="64" rx="2.5" fill="var(--fde-c)"/>
    <rect x="42" y="194" width="46" height="36" rx="8" fill="var(--fde-c)" fill-opacity="0.16"/>
    <text x="65" y="218" font-size="15" font-weight="600" text-anchor="middle" fill="var(--fde-c)">03</text>
    <text x="104" y="206" font-size="15" font-weight="600" fill="var(--fde-fg)">现场嵌入 · Field</text>
    <text x="104" y="228" font-size="12" fill="var(--fde-dim)">买的是：见过真实数据的脏，而不是二手需求里的干净</text>
    <text x="688" y="218" font-size="12" text-anchor="end" fill="var(--fde-dim)">缺位 → 远程猜测</text>
  </g>
  <g class="fde-c4">
    <rect x="16" y="252" width="688" height="64" rx="10" fill="var(--fde-c)" fill-opacity="0.07" stroke="var(--fde-c)" stroke-opacity="0.4"/>
    <rect x="16" y="252" width="5" height="64" rx="2.5" fill="var(--fde-c)"/>
    <rect x="42" y="266" width="46" height="36" rx="8" fill="var(--fde-c)" fill-opacity="0.16"/>
    <text x="65" y="290" font-size="15" font-weight="600" text-anchor="middle" fill="var(--fde-c)">04</text>
    <text x="104" y="278" font-size="15" font-weight="600" fill="var(--fde-fg)">端到端交付 · Delivery</text>
    <text x="104" y="300" font-size="12" fill="var(--fde-dim)">买的是：从定义到结果一个人兜住，没有「不归我这段」</text>
    <text x="688" y="290" font-size="12" text-anchor="end" fill="var(--fde-dim)">缺位 → 接口工程师</text>
  </g>
  <g class="fde-c5">
    <rect x="16" y="324" width="688" height="64" rx="10" fill="var(--fde-c)" fill-opacity="0.07" stroke="var(--fde-c)" stroke-opacity="0.4"/>
    <rect x="16" y="324" width="5" height="64" rx="2.5" fill="var(--fde-c)"/>
    <rect x="42" y="338" width="46" height="36" rx="8" fill="var(--fde-c)" fill-opacity="0.16"/>
    <text x="65" y="362" font-size="15" font-weight="600" text-anchor="middle" fill="var(--fde-c)">05</text>
    <text x="104" y="350" font-size="15" font-weight="600" fill="var(--fde-fg)">产品回流 · Feedback</text>
    <text x="104" y="372" font-size="12" fill="var(--fde-dim)">买的是：第二个同类客户比第一个更快，而不是从零重来</text>
    <text x="688" y="362" font-size="12" text-anchor="end" fill="var(--fde-dim)">缺位 → 定制作坊</text>
  </g>
</svg>
<figcaption>图 1 · 五个分量与各自的退化形态。右栏那一列不是修辞：每一项缺位，都会稳定地退化成一个已经存在的职业——这也是它可检验的依据。</figcaption>
</figure>


逐条说清楚，每条给一个可观察信号。

**工程能力（Engineering）**——买的是能把方案变成在跑的系统，而不是能跑通的 demo。判据很简单：**他交出去的东西，别人不看说明能不能跑起来？** 出问题的时候，他能不能自己定位到哪一层？这一项在 AI 时代反而更容易被高估：能生成代码，和能交付系统之间隔着依赖、权限、日志、可复现。模型降低的是「写」的门槛，不是「交付」的门槛。

**领域理解（Domain）**——把「帮我分析一下」翻译成可判定、可证伪的问题。判据：**把客户的一段口语转述成几条可执行的判定点，客户点头吗？** 这是五个分量里唯一无法在短期内自学的——它按在这个行业里待过的时长计价。市场用「医学背景优先」这类条件给它明码标价，不是客套。

**现场嵌入（Field）**——见过真实数据的脏。判据：**他上一次被真实数据打脸，是什么时候？** 这一项最容易被误解成「出差」。驻场只是形式，实质是**接触到未经整理的输入分布**。反过来也成立：远程也能做到现场嵌入——只要你敢让客户把原始数据直接递过来，而不是先做成一张漂亮的表。

**端到端交付（Delivery）**——从定义到结果一个人负责。判据：**交付件出问题的时候，客户找的是他，还是别人？** 「端到端」不是要求一个人做完所有事，而是要求没有一段是「不归我管」的。

**产品回流（Feedback）**——第二个同类客户要比第一个快。判据：**同一个问题第二次出现时，是从零开始，还是从组件开始？** 这一项最常被跳过，因为它不在交付路径上——它属于交付之后的动作，没人催，也没有对应的工时。

## 三、乘法模型：为什么是乘积，不是求和


<figure class="fde-fig">
<svg viewBox="0 0 720 320" role="img" aria-label="乘积模型的三种情形：五项齐全得 1.00，一项打折得 0.50，一项归零则整体为 0">
  <text x="16" y="20" font-size="13" font-weight="600" fill="var(--fde-fg)">乘积模型：任一分量为 0，整条链的输出就是 0</text>
  <text x="16" y="40" font-size="11.5" fill="var(--fde-dim)">每个分量归一化到 [0,1]：0 = 缺位，0.5 = 存在但不足以闭环。这是启发式的门限模型，不是打分尺。</text>
  <g class="fde-c1"><text x="192" y="68" font-size="11.5" text-anchor="middle" fill="var(--fde-c)">工程</text></g>
  <g class="fde-c2"><text x="254" y="68" font-size="11.5" text-anchor="middle" fill="var(--fde-c)">领域</text></g>
  <g class="fde-c3"><text x="316" y="68" font-size="11.5" text-anchor="middle" fill="var(--fde-c)">现场</text></g>
  <g class="fde-c4"><text x="378" y="68" font-size="11.5" text-anchor="middle" fill="var(--fde-c)">交付</text></g>
  <g class="fde-c5"><text x="440" y="68" font-size="11.5" text-anchor="middle" fill="var(--fde-c)">回流</text></g>
  <text x="16" y="105" font-size="13" font-weight="600" fill="var(--fde-fg)">五项齐全</text>
  <text x="16" y="122" font-size="11" fill="var(--fde-dim)">五个维度都非零</text>
  <g class="fde-c1"><rect x="170" y="84" width="44" height="32" rx="7" fill="var(--fde-c)" fill-opacity="0.8"/></g>
  <g class="fde-c2"><rect x="232" y="84" width="44" height="32" rx="7" fill="var(--fde-c)" fill-opacity="0.8"/></g>
  <g class="fde-c3"><rect x="294" y="84" width="44" height="32" rx="7" fill="var(--fde-c)" fill-opacity="0.8"/></g>
  <g class="fde-c4"><rect x="356" y="84" width="44" height="32" rx="7" fill="var(--fde-c)" fill-opacity="0.8"/></g>
  <g class="fde-c5"><rect x="418" y="84" width="44" height="32" rx="7" fill="var(--fde-c)" fill-opacity="0.8"/></g>
  <text x="223" y="106" font-size="13" text-anchor="middle" fill="var(--fde-dim)">×</text>
  <text x="285" y="106" font-size="13" text-anchor="middle" fill="var(--fde-dim)">×</text>
  <text x="347" y="106" font-size="13" text-anchor="middle" fill="var(--fde-dim)">×</text>
  <text x="409" y="106" font-size="13" text-anchor="middle" fill="var(--fde-dim)">×</text>
  <text x="468" y="107" font-size="15" text-anchor="middle" fill="var(--fde-fg)">=</text>
  <rect x="490" y="78" width="76" height="44" rx="10" fill="var(--fde-acc)" fill-opacity="0.85"/>
  <text x="528" y="106" font-size="15" font-weight="600" text-anchor="middle" fill="hsl(var(--background))">1.00</text>
  <text x="584" y="106" font-size="12.5" fill="var(--fde-fg)">FDE 成立</text>
  <text x="16" y="185" font-size="13" font-weight="600" fill="var(--fde-fg)">一项打折</text>
  <text x="16" y="202" font-size="11" fill="var(--fde-dim)">交付只有一半，能上线但不能闭环</text>
  <g class="fde-c1"><rect x="170" y="164" width="44" height="32" rx="7" fill="var(--fde-c)" fill-opacity="0.8"/></g>
  <g class="fde-c2"><rect x="232" y="164" width="44" height="32" rx="7" fill="var(--fde-c)" fill-opacity="0.8"/></g>
  <g class="fde-c3"><rect x="294" y="164" width="44" height="32" rx="7" fill="var(--fde-c)" fill-opacity="0.8"/></g>
  <g class="fde-c4">
    <rect x="356" y="164" width="44" height="32" rx="7" fill="var(--fde-c)" fill-opacity="0.22" stroke="var(--fde-c)" stroke-dasharray="3 3"/>
    <text x="378" y="186" font-size="11" text-anchor="middle" fill="var(--fde-dim)">0.5</text>
  </g>
  <g class="fde-c5"><rect x="418" y="164" width="44" height="32" rx="7" fill="var(--fde-c)" fill-opacity="0.8"/></g>
  <text x="223" y="186" font-size="13" text-anchor="middle" fill="var(--fde-dim)">×</text>
  <text x="285" y="186" font-size="13" text-anchor="middle" fill="var(--fde-dim)">×</text>
  <text x="347" y="186" font-size="13" text-anchor="middle" fill="var(--fde-dim)">×</text>
  <text x="409" y="186" font-size="13" text-anchor="middle" fill="var(--fde-dim)">×</text>
  <text x="468" y="187" font-size="15" text-anchor="middle" fill="var(--fde-fg)">=</text>
  <rect x="490" y="158" width="76" height="44" rx="10" fill="var(--fde-acc)" fill-opacity="0.22"/>
  <text x="528" y="186" font-size="15" font-weight="600" text-anchor="middle" fill="var(--fde-fg)">0.50</text>
  <text x="584" y="186" font-size="12.5" fill="var(--fde-fg)">能交付，不闭环</text>
  <text x="16" y="265" font-size="13" font-weight="600" fill="var(--fde-fg)">一项归零</text>
  <text x="16" y="282" font-size="11" fill="var(--fde-dim)">领域理解缺位，其余四项再高也无用</text>
  <g class="fde-c1"><rect x="170" y="244" width="44" height="32" rx="7" fill="var(--fde-c)" fill-opacity="0.8"/></g>
  <g class="fde-c2">
    <rect x="232" y="244" width="44" height="32" rx="7" fill="none" stroke="var(--fde-dim)" stroke-opacity="0.7" stroke-dasharray="3 3"/>
    <text x="254" y="266" font-size="11" text-anchor="middle" fill="var(--fde-dim)">0</text>
  </g>
  <g class="fde-c3"><rect x="294" y="244" width="44" height="32" rx="7" fill="var(--fde-c)" fill-opacity="0.8"/></g>
  <g class="fde-c4"><rect x="356" y="244" width="44" height="32" rx="7" fill="var(--fde-c)" fill-opacity="0.8"/></g>
  <g class="fde-c5"><rect x="418" y="244" width="44" height="32" rx="7" fill="var(--fde-c)" fill-opacity="0.8"/></g>
  <text x="223" y="266" font-size="13" text-anchor="middle" fill="var(--fde-dim)">×</text>
  <text x="285" y="266" font-size="13" text-anchor="middle" fill="var(--fde-dim)">×</text>
  <text x="347" y="266" font-size="13" text-anchor="middle" fill="var(--fde-dim)">×</text>
  <text x="409" y="266" font-size="13" text-anchor="middle" fill="var(--fde-dim)">×</text>
  <text x="468" y="267" font-size="15" text-anchor="middle" fill="var(--fde-fg)">=</text>
  <rect x="490" y="238" width="76" height="44" rx="10" fill="none" stroke="var(--fde-dim)" stroke-opacity="0.7" stroke-dasharray="4 3"/>
  <text x="528" y="266" font-size="15" font-weight="600" text-anchor="middle" fill="var(--fde-dim)">0.00</text>
  <text x="584" y="266" font-size="12.5" fill="var(--fde-fg)">退化为外包实现</text>
  <text x="16" y="306" font-size="11.5" fill="var(--fde-dim)">同样的总投入下，把五项拉平比让某一项突出更划算；而任何一项归零，其余四项再高也只是 0。</text>
</svg>
<figcaption>图 2 · 三种情形。注意中间那一行：交付打折到一半，结果是 0.50，不是 4.5 除以 5——乘积模型不给平均值留位置。</figcaption>
</figure>


把五个分量各自归一化到 [0,1] 之后，先声明模型的边界：它是**启发式**的，不是测量仪器。它要表达的是门限性质（gate），不提供精确的边际替代率。

乘法的解释力落在三个推论上。

**推论一：缺位不可补偿。** 加性模型会暗示「工程能力可以补偿领域理解的缺失」——五项加起来分数够高就行。现实不承认这种补偿：**五个分量里任何一个为 0，其余四项再高，输出也是 0。** 纯技术团队做行业交付反复失败，根本原因在这里——不是不够努力，是结构上不通。这一条和另一句常被引用的话同构：0 乘以 N，仍然是 0。

**推论二：补短板比拉长板划算。** 在总投入固定的约束下，乘积的极大值出现在五项相等处，而不是某一项突出处：同样是 4.0 的总投入，五项都是 0.8 得到 0.328，而「四项 1.0 + 一项 0」得到 0。这是木桶效应的算式版本，但它比木桶更硬——木桶只是打不满，乘积是直接归零。

**推论三：这个模型自己会在三处失效，得提前认下来。**

- **分量之间不独立。** 现场嵌入会提升领域理解，端到端交付会暴露产品缺口从而触发回流。真实系统里五项是相互增强的。它的门限性质来自「缺位即失效」这一条观察，不来自数学上的独立性——所以我不用它做任何精确计算。
- **归一化本身是主观的。** 没有公认的尺子能把「领域理解」量到 0.7。所以这个模型只能用于定性比较（判断一个人缺的是哪一项），不能用于打分排名。
- **它是关于角色的模型，不是关于人的模型。** 同一个人在不同项目里，五项的值不相同。一旦把它人格化——「这个人就是个 0.6」——它就退回了形容词，等于白拆。

先把自己的边界画出来，这个模型才不至于变成新的万能话术。

## 四、九段管线：一条能验证这五项的试金石

抽象讨论没法验证。下面拿一条真实的分析管线来跑：从一句「帮我看看这批样本有什么差异」，跑到一句能写进论文的生物学解释。全程九段：

**问题定义 → 数据检索 → 数据下载 → QC → 数据处理 → 统计分析 → 可视化 → 文献验证 → 生物学解释**


<figure class="fde-fig">
<svg viewBox="0 0 720 224" role="img" aria-label="九段分析管线：前端定义问题、中段保证过程、后端坐实结论，并有三条回退线">
  <defs>
    <marker id="f3-ar" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L5,3 L0,6 z" fill="var(--fde-dim)" fill-opacity="0.6"/>
    </marker>
    <marker id="f3-lp" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
      <path d="M0,0 L6,3.5 L0,7 z" fill="var(--fde-warn)"/>
    </marker>
  </defs>
  <text x="16" y="18" font-size="13" font-weight="600" fill="var(--fde-fg)">九段管线：每一段都能外包，只有「该退回哪一段」不能</text>
  <text x="122" y="38" font-size="11.5" text-anchor="middle" fill="var(--fde-dim)">① 先把问题问对</text>
  <text x="399" y="38" font-size="11.5" text-anchor="middle" fill="var(--fde-dim)">② 把过程做对</text>
  <text x="633" y="38" font-size="11.5" text-anchor="middle" fill="var(--fde-dim)">③ 把结论坐实</text>
  <rect x="8" y="46" width="228" height="78" rx="10" fill="var(--fde-fill)" fill-opacity="0.7" stroke="var(--fde-line)" stroke-dasharray="4 4"/>
  <rect x="250" y="46" width="298" height="78" rx="10" fill="var(--fde-fill)" fill-opacity="0.7" stroke="var(--fde-line)" stroke-dasharray="4 4"/>
  <rect x="562" y="46" width="142" height="78" rx="10" fill="var(--fde-fill)" fill-opacity="0.7" stroke="var(--fde-line)" stroke-dasharray="4 4"/>
  <g class="fde-c2">
    <rect x="16" y="58" width="64" height="52" rx="9" fill="var(--fde-c)" fill-opacity="0.12" stroke="var(--fde-c)" stroke-opacity="0.55"/>
    <text x="48" y="79" font-size="11" font-weight="600" text-anchor="middle" fill="var(--fde-fg)">问题定义</text>
    <text x="48" y="94" font-size="9" text-anchor="middle" fill="var(--fde-dim)">scoping</text>
  </g>
  <line x1="82" y1="84" x2="92" y2="84" stroke="var(--fde-dim)" stroke-opacity="0.5" stroke-width="1.2" marker-end="url(#f3-ar)"/>
  <g class="fde-c2">
    <rect x="94" y="58" width="64" height="52" rx="9" fill="var(--fde-c)" fill-opacity="0.12" stroke="var(--fde-c)" stroke-opacity="0.55"/>
    <text x="126" y="79" font-size="11" font-weight="600" text-anchor="middle" fill="var(--fde-fg)">数据检索</text>
    <text x="126" y="94" font-size="9" text-anchor="middle" fill="var(--fde-dim)">retrieval</text>
  </g>
  <line x1="160" y1="84" x2="170" y2="84" stroke="var(--fde-dim)" stroke-opacity="0.5" stroke-width="1.2" marker-end="url(#f3-ar)"/>
  <g class="fde-c1">
    <rect x="172" y="58" width="64" height="52" rx="9" fill="var(--fde-c)" fill-opacity="0.12" stroke="var(--fde-c)" stroke-opacity="0.55"/>
    <text x="204" y="79" font-size="11" font-weight="600" text-anchor="middle" fill="var(--fde-fg)">数据下载</text>
    <text x="204" y="94" font-size="9" text-anchor="middle" fill="var(--fde-dim)">download</text>
  </g>
  <line x1="238" y1="84" x2="248" y2="84" stroke="var(--fde-dim)" stroke-opacity="0.5" stroke-width="1.2" marker-end="url(#f3-ar)"/>
  <g class="fde-c1">
    <rect x="250" y="58" width="64" height="52" rx="9" fill="var(--fde-c)" fill-opacity="0.12" stroke="var(--fde-c)" stroke-opacity="0.55"/>
    <text x="282" y="79" font-size="11" font-weight="600" text-anchor="middle" fill="var(--fde-fg)">质控</text>
    <text x="282" y="94" font-size="9" text-anchor="middle" fill="var(--fde-dim)">QC</text>
  </g>
  <line x1="316" y1="84" x2="326" y2="84" stroke="var(--fde-dim)" stroke-opacity="0.5" stroke-width="1.2" marker-end="url(#f3-ar)"/>
  <g class="fde-c1">
    <rect x="328" y="58" width="64" height="52" rx="9" fill="var(--fde-c)" fill-opacity="0.12" stroke="var(--fde-c)" stroke-opacity="0.55"/>
    <text x="360" y="79" font-size="11" font-weight="600" text-anchor="middle" fill="var(--fde-fg)">数据处理</text>
    <text x="360" y="94" font-size="9" text-anchor="middle" fill="var(--fde-dim)">processing</text>
  </g>
  <line x1="394" y1="84" x2="404" y2="84" stroke="var(--fde-dim)" stroke-opacity="0.5" stroke-width="1.2" marker-end="url(#f3-ar)"/>
  <g class="fde-c1">
    <rect x="406" y="58" width="64" height="52" rx="9" fill="var(--fde-c)" fill-opacity="0.12" stroke="var(--fde-c)" stroke-opacity="0.55"/>
    <text x="438" y="79" font-size="11" font-weight="600" text-anchor="middle" fill="var(--fde-fg)">统计分析</text>
    <text x="438" y="94" font-size="9" text-anchor="middle" fill="var(--fde-dim)">statistics</text>
  </g>
  <line x1="472" y1="84" x2="482" y2="84" stroke="var(--fde-dim)" stroke-opacity="0.5" stroke-width="1.2" marker-end="url(#f3-ar)"/>
  <g class="fde-c1">
    <rect x="484" y="58" width="64" height="52" rx="9" fill="var(--fde-c)" fill-opacity="0.12" stroke="var(--fde-c)" stroke-opacity="0.55"/>
    <text x="516" y="79" font-size="11" font-weight="600" text-anchor="middle" fill="var(--fde-fg)">可视化</text>
    <text x="516" y="94" font-size="9" text-anchor="middle" fill="var(--fde-dim)">plots</text>
  </g>
  <line x1="550" y1="84" x2="560" y2="84" stroke="var(--fde-dim)" stroke-opacity="0.5" stroke-width="1.2" marker-end="url(#f3-ar)"/>
  <g class="fde-c2">
    <rect x="562" y="58" width="64" height="52" rx="9" fill="var(--fde-c)" fill-opacity="0.12" stroke="var(--fde-c)" stroke-opacity="0.55"/>
    <text x="594" y="79" font-size="11" font-weight="600" text-anchor="middle" fill="var(--fde-fg)">文献验证</text>
    <text x="594" y="94" font-size="9" text-anchor="middle" fill="var(--fde-dim)">literature</text>
  </g>
  <line x1="628" y1="84" x2="638" y2="84" stroke="var(--fde-dim)" stroke-opacity="0.5" stroke-width="1.2" marker-end="url(#f3-ar)"/>
  <g class="fde-c5">
    <rect x="640" y="58" width="64" height="52" rx="9" fill="var(--fde-c)" fill-opacity="0.12" stroke="var(--fde-c)" stroke-opacity="0.55"/>
    <text x="672" y="79" font-size="10" font-weight="600" text-anchor="middle" fill="var(--fde-fg)">生物学解释</text>
    <text x="672" y="94" font-size="9" text-anchor="middle" fill="var(--fde-dim)">biology</text>
  </g>
  <path d="M 672 110 Q 473 190 274 110" fill="none" stroke="var(--fde-warn)" stroke-width="1.4" stroke-dasharray="5 4" marker-end="url(#f3-lp)"/>
  <path d="M 290 110 Q 208 242 126 110" fill="none" stroke="var(--fde-warn)" stroke-width="1.4" stroke-dasharray="5 4" marker-end="url(#f3-lp)"/>
  <path d="M 594 110 Q 321 298 48 110" fill="none" stroke="var(--fde-warn)" stroke-width="1.4" stroke-dasharray="5 4" marker-end="url(#f3-lp)"/>
  <g>
    <rect x="383" y="124" width="180" height="20" rx="7" fill="hsl(var(--background))" stroke="var(--fde-warn)" stroke-opacity="0.45"/>
    <text x="473" y="138" font-size="11" text-anchor="middle" fill="var(--fde-fg)">回环 C · 机制冲突 → 回查污染</text>
  </g>
  <g>
    <rect x="113" y="150" width="190" height="20" rx="7" fill="hsl(var(--background))" stroke="var(--fde-warn)" stroke-opacity="0.45"/>
    <text x="208" y="164" font-size="11" text-anchor="middle" fill="var(--fde-fg)">回环 A · 质控不过 → 回查数据源</text>
  </g>
  <g>
    <rect x="226" y="178" width="190" height="20" rx="7" fill="hsl(var(--background))" stroke="var(--fde-warn)" stroke-opacity="0.45"/>
    <text x="321" y="192" font-size="11" text-anchor="middle" fill="var(--fde-fg)">回环 B · 文献对不上 → 重问问题</text>
  </g>
</svg>
<figcaption>图 3 · 九段与三条回退线。节点描边用的是该阶段的主要考核分量（蓝＝工程、绿＝领域、红＝回流），连线上的箭头才是流水线方向——三个虚线回环才是这条管线真正的控制逻辑。</figcaption>
</figure>


九段可以归成三簇：**前端（1–3）决定做什么，中段（4–7）决定做对没有，后端（8–9）决定结论是不是真的。**

| 阶段 | 这一段在干什么 | 主要考核 | 典型失败 | 交付物 |
| --- | --- | --- | --- | --- |
| ① 问题定义 | 把「看看有什么差异」改成可回答的问题 | 领域 · 现场 | 问题本身不可证伪 | 分析计划与判定点 |
| ② 数据检索 | 定位可用的数据集 | 领域 | 把「能下到」当成「能用」；物种/组织/平台不匹配 | 数据集清单 + 入选理由 |
| ③ 数据下载 | 取回原始数据 | 工程 | 只存文件不存校验和，三个月后无法复现 | 原始数据 + 来源与校验记录 |
| ④ QC | 判断数据能不能用 | 工程 · 领域 | 指标全绿就当可用，不看生物学合理性 | QC 报告 + 剔除决策 |
| ⑤ 数据处理 | 比对、定量、归一化 | 工程 | 参数不留痕，手敲命令行当管线 | 可重跑的处理流程 |
| ⑥ 统计分析 | 建模与检验 | 工程 · 领域 | 直接跑差异分析，不检验设计假设 | 统计结果 + 前提说明 |
| ⑦ 可视化 | 把结果变成能判读的图 | 工程 · 领域 | 图能看，但坐标截断、单位混用 | 图表 + 图注 |
| ⑧ 文献验证 | 与既有知识对表 | 领域 | 跳过这一步，把噪声当发现 | 证据等级评价 |
| ⑨ 生物学解释 | 把统计结果翻译成机制假说 | 领域 · 交付 · 回流 | 结论越出数据能支撑的范围 | 可检验的假说 + 下一步实验 |

**前端决定做什么。** 问题定义这一段最贵，也最容易被跳过。判据只有一条：**能不能说出「什么结果会让我认为假设是错的」？** 如果说不出来，后面八段的努力都会变成给一个不可证伪的愿望找证据。数据检索不是搜索，是排除——真正的产出是**入选理由**，理由比清单重要。数据下载可以完全交给脚本，但有一条不可让步：记录来源、版本、校验和。今天省下的五行元数据，三个月后会变成没法复现的整条结论。

**中段几乎全是工程活，也恰好是 AI 压缩得最狠的部分。** QC 报告、比对定量、统计检验、画图，工具链和模型已经能覆盖大半。但每一段都留着一道不能外包的缝：QC 的缝是「指标全绿不等于数据可用」，要看样本聚类是否按处理而不是按批次分开；处理的缝是参数要留痕；统计的缝是先检验设计假设（配对、批次、重复数）再跑差异；可视化的缝是——图能看，不等于图没骗人，坐标截断、单位混用、把 n=3 画成 n=30，全都在这一缝里。

**后端几乎全靠领域理解。** 文献验证的作用不是「支持我的结论」，是**给结论定证据等级**。生物学解释则是把统计结果翻译成机制假说，并且明确说出哪一部分是数据支撑的、哪一部分是推测——这一段最容易越界：数据说「表达上升」，解释会说「通路被激活」，再往下就变成「因此可以作为靶点」。每越一级，需要的新证据多一层。

**然后是最关键的一点：这条管线不是线性的。** 它有三条回退线。

- **回环 A：质控不过，退到「数据检索」**——换数据集，而不是硬着头皮往下做。硬做出来的结果不是错，是**不可解释**：你不知道最后那个差异来自生物学，还是来自你没剔除的那批样本。
- **回环 B：文献对不上，退到「问题定义」**——很可能问题本身就问错了。典型情形是把批次差异当成处理效应，而这个问题在一开始就该用配对设计避掉。
- **回环 C：机制冲突，退到「QC」**——先排查污染与批次效应，再谈生物学。看到「显著的、但和已知机制完全相反的」结果，第一反应应该是回查数据，而不是准备推翻教科书。

这三条回退线，是整条管线上唯一无法外包的部分。**每一段的具体动作都可以外包——下载可以写脚本，统计可以调包，画图可以用模板；唯独「判断该退回哪一段」，必须由一个同时懂数据和懂生物的人来做。** 这就是 FDE 在一条分析管线里的位置：不是跑得最快的人，是决定下一步跑哪一段的人。

还有一个关于长度的观察：**九段，大致是一个人能独立走完的最大长度。** 再长——需要跨组协调、跨系统权限、跨季度排期——就必须交给组织。这既解释了 FDE 为什么天然是「一个人的带宽」，也解释了它为什么在现在重新变得可行：中段被压缩之后，一个人终于能把这九段握在手里。

## 五、分量 × 阶段：溢价为什么不均匀

把五个分量和九个阶段交叉起来（图 4、下表），能读出三件事。


<figure class="fde-fig">
<svg viewBox="0 0 720 452" role="img" aria-label="九段管线与五个分量的责任矩阵：领域理解集中在首尾，工程能力占据中段，产品回流只出现在最后一段">
  <text x="16" y="18" font-size="13" font-weight="600" fill="var(--fde-fg)">哪一段在考核哪个分量：主责 / 参与 / 无关</text>
  <text x="16" y="38" font-size="11.5" fill="var(--fde-dim)">读数：领域理解压在首尾两端，工程能力占据中段，产品回流只出现在最后一段。</text>
  <g class="fde-c1"><text x="208" y="64" font-size="12" font-weight="600" text-anchor="middle" fill="var(--fde-c)">工程</text></g>
  <g class="fde-c2"><text x="308" y="64" font-size="12" font-weight="600" text-anchor="middle" fill="var(--fde-c)">领域</text></g>
  <g class="fde-c3"><text x="408" y="64" font-size="12" font-weight="600" text-anchor="middle" fill="var(--fde-c)">现场</text></g>
  <g class="fde-c4"><text x="508" y="64" font-size="12" font-weight="600" text-anchor="middle" fill="var(--fde-c)">交付</text></g>
  <g class="fde-c5"><text x="608" y="64" font-size="12" font-weight="600" text-anchor="middle" fill="var(--fde-c)">回流</text></g>
  <g stroke="var(--fde-line)" stroke-opacity="0.5" stroke-dasharray="3 4">
    <line x1="158" y1="78" x2="158" y2="420"/>
    <line x1="258" y1="78" x2="258" y2="420"/>
    <line x1="358" y1="78" x2="358" y2="420"/>
    <line x1="458" y1="78" x2="458" y2="420"/>
    <line x1="558" y1="78" x2="558" y2="420"/>
  </g>
  <g stroke="var(--fde-line)" stroke-opacity="0.7">
    <line x1="16" y1="78" x2="704" y2="78"/>
    <line x1="16" y1="116" x2="704" y2="116"/>
    <line x1="16" y1="154" x2="704" y2="154"/>
    <line x1="16" y1="192" x2="704" y2="192"/>
    <line x1="16" y1="230" x2="704" y2="230"/>
    <line x1="16" y1="268" x2="704" y2="268"/>
    <line x1="16" y1="306" x2="704" y2="306"/>
    <line x1="16" y1="344" x2="704" y2="344"/>
    <line x1="16" y1="382" x2="704" y2="382"/>
    <line x1="16" y1="420" x2="704" y2="420"/>
  </g>
  <text x="16" y="101" font-size="11.5" fill="var(--fde-fg)">① 问题定义</text>
  <text x="16" y="139" font-size="11.5" fill="var(--fde-fg)">② 数据检索</text>
  <text x="16" y="177" font-size="11.5" fill="var(--fde-fg)">③ 数据下载</text>
  <text x="16" y="215" font-size="11.5" fill="var(--fde-fg)">④ 质控 QC</text>
  <text x="16" y="253" font-size="11.5" fill="var(--fde-fg)">⑤ 数据处理</text>
  <text x="16" y="291" font-size="11.5" fill="var(--fde-fg)">⑥ 统计分析</text>
  <text x="16" y="329" font-size="11.5" fill="var(--fde-fg)">⑦ 可视化</text>
  <text x="16" y="367" font-size="11.5" fill="var(--fde-fg)">⑧ 文献验证</text>
  <text x="16" y="405" font-size="11.5" fill="var(--fde-fg)">⑨ 生物学解释</text>
  <g class="fde-c1">
    <rect x="180" y="87" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.18"/>
    <text x="208" y="101" font-size="11" text-anchor="middle" fill="var(--fde-dim)">参与</text>
  </g>
  <g class="fde-c2">
    <rect x="280" y="87" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.85"/>
    <text x="308" y="101" font-size="11" font-weight="600" text-anchor="middle" fill="hsl(var(--background))">主责</text>
  </g>
  <g class="fde-c3">
    <rect x="380" y="87" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.85"/>
    <text x="408" y="101" font-size="11" font-weight="600" text-anchor="middle" fill="hsl(var(--background))">主责</text>
  </g>
  <text x="508" y="101" font-size="12" text-anchor="middle" fill="var(--fde-dim)">·</text>
  <text x="608" y="101" font-size="12" text-anchor="middle" fill="var(--fde-dim)">·</text>
  <g class="fde-c1">
    <rect x="180" y="125" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.18"/>
    <text x="208" y="139" font-size="11" text-anchor="middle" fill="var(--fde-dim)">参与</text>
  </g>
  <g class="fde-c2">
    <rect x="280" y="125" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.85"/>
    <text x="308" y="139" font-size="11" font-weight="600" text-anchor="middle" fill="hsl(var(--background))">主责</text>
  </g>
  <g class="fde-c3">
    <rect x="380" y="125" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.18"/>
    <text x="408" y="139" font-size="11" text-anchor="middle" fill="var(--fde-dim)">参与</text>
  </g>
  <text x="508" y="139" font-size="12" text-anchor="middle" fill="var(--fde-dim)">·</text>
  <text x="608" y="139" font-size="12" text-anchor="middle" fill="var(--fde-dim)">·</text>
  <g class="fde-c1">
    <rect x="180" y="163" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.85"/>
    <text x="208" y="177" font-size="11" font-weight="600" text-anchor="middle" fill="hsl(var(--background))">主责</text>
  </g>
  <text x="308" y="177" font-size="12" text-anchor="middle" fill="var(--fde-dim)">·</text>
  <text x="408" y="177" font-size="12" text-anchor="middle" fill="var(--fde-dim)">·</text>
  <g class="fde-c4">
    <rect x="480" y="163" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.18"/>
    <text x="508" y="177" font-size="11" text-anchor="middle" fill="var(--fde-dim)">参与</text>
  </g>
  <text x="608" y="177" font-size="12" text-anchor="middle" fill="var(--fde-dim)">·</text>
  <g class="fde-c1">
    <rect x="180" y="201" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.85"/>
    <text x="208" y="215" font-size="11" font-weight="600" text-anchor="middle" fill="hsl(var(--background))">主责</text>
  </g>
  <g class="fde-c2">
    <rect x="280" y="201" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.85"/>
    <text x="308" y="215" font-size="11" font-weight="600" text-anchor="middle" fill="hsl(var(--background))">主责</text>
  </g>
  <g class="fde-c3">
    <rect x="380" y="201" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.18"/>
    <text x="408" y="215" font-size="11" text-anchor="middle" fill="var(--fde-dim)">参与</text>
  </g>
  <text x="508" y="215" font-size="12" text-anchor="middle" fill="var(--fde-dim)">·</text>
  <text x="608" y="215" font-size="12" text-anchor="middle" fill="var(--fde-dim)">·</text>
  <g class="fde-c1">
    <rect x="180" y="239" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.85"/>
    <text x="208" y="253" font-size="11" font-weight="600" text-anchor="middle" fill="hsl(var(--background))">主责</text>
  </g>
  <g class="fde-c2">
    <rect x="280" y="239" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.18"/>
    <text x="308" y="253" font-size="11" text-anchor="middle" fill="var(--fde-dim)">参与</text>
  </g>
  <text x="408" y="253" font-size="12" text-anchor="middle" fill="var(--fde-dim)">·</text>
  <g class="fde-c4">
    <rect x="480" y="239" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.18"/>
    <text x="508" y="253" font-size="11" text-anchor="middle" fill="var(--fde-dim)">参与</text>
  </g>
  <text x="608" y="253" font-size="12" text-anchor="middle" fill="var(--fde-dim)">·</text>
  <g class="fde-c1">
    <rect x="180" y="277" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.85"/>
    <text x="208" y="291" font-size="11" font-weight="600" text-anchor="middle" fill="hsl(var(--background))">主责</text>
  </g>
  <g class="fde-c2">
    <rect x="280" y="277" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.85"/>
    <text x="308" y="291" font-size="11" font-weight="600" text-anchor="middle" fill="hsl(var(--background))">主责</text>
  </g>
  <text x="408" y="291" font-size="12" text-anchor="middle" fill="var(--fde-dim)">·</text>
  <g class="fde-c4">
    <rect x="480" y="277" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.18"/>
    <text x="508" y="291" font-size="11" text-anchor="middle" fill="var(--fde-dim)">参与</text>
  </g>
  <text x="608" y="291" font-size="12" text-anchor="middle" fill="var(--fde-dim)">·</text>
  <g class="fde-c1">
    <rect x="180" y="315" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.85"/>
    <text x="208" y="329" font-size="11" font-weight="600" text-anchor="middle" fill="hsl(var(--background))">主责</text>
  </g>
  <g class="fde-c2">
    <rect x="280" y="315" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.18"/>
    <text x="308" y="329" font-size="11" text-anchor="middle" fill="var(--fde-dim)">参与</text>
  </g>
  <g class="fde-c3">
    <rect x="380" y="315" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.18"/>
    <text x="408" y="329" font-size="11" text-anchor="middle" fill="var(--fde-dim)">参与</text>
  </g>
  <g class="fde-c4">
    <rect x="480" y="315" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.18"/>
    <text x="508" y="329" font-size="11" text-anchor="middle" fill="var(--fde-dim)">参与</text>
  </g>
  <text x="608" y="329" font-size="12" text-anchor="middle" fill="var(--fde-dim)">·</text>
  <text x="208" y="367" font-size="12" text-anchor="middle" fill="var(--fde-dim)">·</text>
  <g class="fde-c2">
    <rect x="280" y="353" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.85"/>
    <text x="308" y="367" font-size="11" font-weight="600" text-anchor="middle" fill="hsl(var(--background))">主责</text>
  </g>
  <text x="408" y="367" font-size="12" text-anchor="middle" fill="var(--fde-dim)">·</text>
  <g class="fde-c4">
    <rect x="480" y="353" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.18"/>
    <text x="508" y="367" font-size="11" text-anchor="middle" fill="var(--fde-dim)">参与</text>
  </g>
  <g class="fde-c5">
    <rect x="580" y="353" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.18"/>
    <text x="608" y="367" font-size="11" text-anchor="middle" fill="var(--fde-dim)">参与</text>
  </g>
  <text x="208" y="405" font-size="12" text-anchor="middle" fill="var(--fde-dim)">·</text>
  <g class="fde-c2">
    <rect x="280" y="391" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.85"/>
    <text x="308" y="405" font-size="11" font-weight="600" text-anchor="middle" fill="hsl(var(--background))">主责</text>
  </g>
  <text x="408" y="405" font-size="12" text-anchor="middle" fill="var(--fde-dim)">·</text>
  <g class="fde-c4">
    <rect x="480" y="391" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.85"/>
    <text x="508" y="405" font-size="11" font-weight="600" text-anchor="middle" fill="hsl(var(--background))">主责</text>
  </g>
  <g class="fde-c5">
    <rect x="580" y="391" width="56" height="20" rx="6" fill="var(--fde-c)" fill-opacity="0.85"/>
    <text x="608" y="405" font-size="11" font-weight="600" text-anchor="middle" fill="hsl(var(--background))">主责</text>
  </g>
  <text x="16" y="440" font-size="11" fill="var(--fde-dim)">判定为定性权重，用于比较分布，不构成精确打分。列色与图 1、图 2 一致。</text>
</svg>
<figcaption>图 4 · 分量 × 阶段矩阵（数一数列里的「主责」）：领域理解 5 个、工程能力 5 个、现场 1 个、交付 1 个、产品回流 1 个。交付在九段里几乎每段都是「参与」，但只有到第 ⑨ 段才成为主责——这就是「端到端」的真实形状。</figcaption>
</figure>


**第一，领域理解的权重压在首尾两端。** 第 ① 段（问题定义）和最后两段（文献验证、生物学解释）几乎全靠领域知识；中间六段里，它是配角。也就是说，一个人的行业经验真正被用到的地方，是这条管线的入口和出口。

**第二，工程能力占据中段。** 第 ③ 到 ⑦ 段，工程能力是主责——下载、处理、统计、画图，全是把已经想清楚的事做出来。

**第三，产品回流只出现在最后一段。** 九段里只有第 ⑨ 段它是主责，因为它是唯一不在交付路径上的分量。

三件事合起来解释了一个反直觉的分布：**FDE 的溢价不在中间的执行段，而在两端。** 而 AI 恰好把中间那一段压缩得最狠——下载、处理、统计、可视化，工具链和模型已经能覆盖大半，压缩空间几近见底。两端的空间最小：把模糊愿望翻译成可证伪的问题，要的是行业经验；把统计结果翻译成机制假说并说清边界，要的是对既有文献的熟悉。前者买不到，后者读得慢。

所以「模型变强了，FDE 会不会消失」这个问题，问法本身就有毛病：模型变强，削掉的是中间那六段——那六段本来就最便宜。留下来的两段，正好是定价最高的两段。前一篇讲过市场为什么这样定价（[谈谈 FDE：站在甲方、技术与 AI 中间的向导](/2026/09/15/2026-09-15-01-fde-forward-deployed-engineer/)），这一篇讲的是能力为什么这样分布——两件事互相印证，不是同一件事说两遍。

## 六、伪 FDE 的五个信号

前一篇写的是这个模式在组织层面怎么失效（认知断流、单点依赖、边界漂移、合规红线）。这一节换个轴：**能力层面怎么伪装**。五个信号与五个分量一一对应，每个都可观察。

| 缺的分量 | 伪装形态 | 观察到的信号 |
| --- | --- | --- |
| 工程能力 | 报告工厂 | 交付物永远是文档、流程图、方案，没有能跑起来的东西 |
| 领域理解 | 需求翻译机 | 从不质疑问题本身，问什么答什么，「你说怎么做我就怎么做」 |
| 现场嵌入 | 二手判断 | 所有判断都基于别人转述的口径和截图，没碰过原始数据 |
| 端到端交付 | 接口工程师 | 永远只交一段，接缝处总有人接；被要求「从头跑一遍」时答不上来 |
| 产品回流 | 定制作坊 | 第二个同类客户，比第一个更慢 |

第五个信号最狠，也最好测：**同一个问题第二次遇到时，是更快还是更慢。** 更快，说明第一次的认知被沉淀了；更慢，说明第一次只留下了代码，没留下理解。这个信号不需要看任何简历。

有一点要说清楚：伪装不等于欺骗。多数「伪 FDE」不是装出来的，是**缺位而不自知**——一个人把工程能力做到 1.0，会自然地觉得自己什么都能接，因为短板恰好在他看不见的那一侧。这也是为什么五个分量要分别配判据：不是为了评判别人，是为了让自己知道缺的是哪一项。

## 七、结语：定义比工具活得久

三个条件让这个老位置在现在被重新定价——实现成本坍缩、接口标准化、组织流程滞后。这一层前一篇已经展开过，不重复。这里只说另一件事：**热度会退，定义不会。**

工具从 PPT 换成模型 API，还会换成 agent 工作流；管线的中段会被继续压缩，首尾两端的判断权不会移交出去。五个分量和三条回退线，是这轮变化里最稳定的部分——因为它们描述的不是技术栈，而是**谁在什么位置上做判断**。

对生物背景的读者还有一句：这五项里，领域理解和现场嵌入是你已经握着的资产，工程能力是唯一需要补、也补得动的一项——而且现在补的速度比三年前快得多。缺工程能力的人做不了 FDE；但只有工程能力的人，做的是另一份工作。

最后回到开头那三句形容词。它们不是错的，是不可检验。「懂技术、懂业务、能出差」之所以流行，是因为它谁都能说、谁都能往自己身上套。**把它换成五个能看出来、能问出来的判据**，这个角色才从一顶帽子，变回一个位置。

## 数据与出处

- **角色的来源与官方定义**：[Palantir 官方博客《Dev versus Delta: Demystifying engineering roles at Palantir》](https://blog.palantir.com/dev-versus-delta-demystifying-engineering-roles-at-palantir-ad44c2a6e87)（Dev 与 Delta 的分工、「一个能力卖给很多客户」对「一个客户身上做很多能力」、与咨询顾问的分界、前线代码回流产品的机制）；[《A Day in the Life of a Palantir Forward Deployed Software Engineer》](https://blog.palantir.com/a-day-in-the-life-of-a-palantir-forward-deployed-software-engineer-45ef2de257b1)（前线工程师的日常、技术工作量的量级、现场认知回流产品）。检索关键词：`Palantir Forward Deployed Engineer Dev Delta`。
- **「forward deployed」借自军事用语、以及 OpenAI / Anthropic / Google Cloud 等公司同岗招聘的现状**：其中一份行业汇编见 [The Forward Deployed Engineer](https://www.theforwarddeployed.io/what-is-a-forward-deployed-engineer)。注意这类站点同时提供咨询与付费服务，引用它只取事实陈述，不取判断。
- **五个分量、乘积模型、九段管线与三条回退线**：本文的分析框架，不是任何公司的官方定义。它来自作者在真实分析管线上的观察，未经同行评议。其中九段管线的划分按常规生信分析流程整理。
- **岗位薪酬与市场定价的一手调查**（生物技术本科 6–9K、FDE 12K 起、异地同岗 20–25K、医学背景明码加价）：见前一篇 [《谈谈 FDE：站在甲方、技术与 AI 中间的向导》](/2026/09/15/2026-09-15-01-fde-forward-deployed-engineer/)。那篇负责市场口径，这篇负责能力口径，两篇的数据不混用。
