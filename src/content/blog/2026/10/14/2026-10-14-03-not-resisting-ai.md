---
title: 他们抵制的不是 AI：两份声明、722 篇论文与一道限流令
description: 媒体把过去一个月的数学界压缩成「数学家抵制 AI」——但只要读原文，这个概括就是错的。两份声明的靶子都是公司行为；722 篇论文真正挤占的是志愿者审核这种公共品；而「数学的主体性」这个大问题，靠抵制是建构不出来的。
publishDate: 2026-10-14
tags: [大模型, 观点评论, 科学史]
draft: false
---

<!-- 本文 SVG 配图的主题变量：颜色跟随站点主题（见 src/assets/styles/app.css 的 --primary / --foreground / --muted / --border），.dark 由主题脚本挂在 <html> 上。 -->

<style>
  .tao-fig {
    --tao-fg: hsl(var(--foreground));
    --tao-dim: hsl(var(--muted-foreground));
    --tao-line: hsl(var(--border));
    --tao-fill: hsl(var(--muted));
    --tao-acc: hsl(var(--primary));
    --tao-warn: hsl(28 88% 44%);
    margin: 2.25rem 0;
  }
  .dark .tao-fig {
    --tao-warn: hsl(32 90% 62%);
  }
  .tao-fig svg {
    display: block;
    width: 100%;
    height: auto;
  }
  .tao-fig figcaption {
    margin-top: 0.7rem;
    font-size: 0.82em;
    line-height: 1.6;
    color: hsl(var(--muted-foreground));
    text-align: center;
  }
</style>

## 〇、一个月里的五件事

上一篇谈了陶哲轩那个「黑盒 AI 治癌药」思想实验，以及它在传播中被读歪的过程。但那页幻灯片不是孤立事件——它是一连串事件里被单独截出来的一帧。把过去一个月按时间排开：

<figure class="tao-fig">
<svg viewBox="0 0 680 210" width="100%" role="img" aria-label="事件时间线：2025 年 9 月莱顿研讨会，2026 年中莱顿宣言发布，2026 年 9 月 11 日 25 位菲尔兹奖得主声明，10 月 1 日 arXiv 限流令，10 月 6 日 OpenAI 发布 722 篇论文，10 月 9 日陶哲轩 Math 2.0 讲座">
<title>数学界与 AI 的一个月：五件事的时间线</title>
<line x1="40" y1="105" x2="650" y2="105" stroke="var(--tao-line)" stroke-width="1.5"/>
<text x="75" y="34" text-anchor="middle" font-size="11" font-weight="500" fill="var(--tao-fg)">2025-09</text>
<text x="75" y="50" text-anchor="middle" font-size="11" fill="var(--tao-dim)">莱顿研讨会</text>
<line x1="75" y1="60" x2="75" y2="100" stroke="var(--tao-dim)" stroke-width="1"/>
<circle cx="75" cy="105" r="4" fill="var(--tao-acc)"/>
<circle cx="183" cy="105" r="4" fill="var(--tao-acc)"/>
<line x1="183" y1="110" x2="183" y2="142" stroke="var(--tao-dim)" stroke-width="1"/>
<text x="183" y="156" text-anchor="middle" font-size="11" font-weight="500" fill="var(--tao-fg)">2026 年中</text>
<text x="183" y="172" text-anchor="middle" font-size="11" fill="var(--tao-dim)">《莱顿宣言》发布</text>
<text x="291" y="34" text-anchor="middle" font-size="11" font-weight="500" fill="var(--tao-fg)">2026-09-11</text>
<text x="291" y="50" text-anchor="middle" font-size="11" fill="var(--tao-dim)">25 位菲尔兹奖得主声明</text>
<line x1="291" y1="60" x2="291" y2="100" stroke="var(--tao-dim)" stroke-width="1"/>
<circle cx="291" cy="105" r="4" fill="var(--tao-acc)"/>
<circle cx="399" cy="105" r="4" fill="var(--tao-acc)"/>
<line x1="399" y1="110" x2="399" y2="142" stroke="var(--tao-dim)" stroke-width="1"/>
<text x="399" y="156" text-anchor="middle" font-size="11" font-weight="500" fill="var(--tao-fg)">2026-10-01</text>
<text x="399" y="172" text-anchor="middle" font-size="11" fill="var(--tao-dim)">arXiv 限流令</text>
<text x="507" y="34" text-anchor="middle" font-size="11" font-weight="500" fill="var(--tao-fg)">2026-10-06</text>
<text x="507" y="50" text-anchor="middle" font-size="11" fill="var(--tao-dim)">OpenAI 发布 722 篇</text>
<line x1="507" y1="60" x2="507" y2="100" stroke="var(--tao-dim)" stroke-width="1"/>
<circle cx="507" cy="105" r="4.5" fill="var(--tao-warn)"/>
<circle cx="615" cy="105" r="4" fill="var(--tao-acc)"/>
<line x1="615" y1="110" x2="615" y2="142" stroke="var(--tao-dim)" stroke-width="1"/>
<text x="615" y="156" text-anchor="middle" font-size="11" font-weight="500" fill="var(--tao-fg)">2026-10-09</text>
<text x="615" y="172" text-anchor="middle" font-size="11" fill="var(--tao-dim)">Math 2.0 讲座</text>
<text x="40" y="200" font-size="10" fill="var(--tao-dim)">节点均匀排布，未按时间比例。以下均据公开报道。</text>
</svg>
<figcaption>图 1 · 一个月里的五件事（另有一次会议是它们的共同源头）。媒体把这串事件压缩成「数学家抵制 AI」——这个概括是错的，下面逐层拆开。</figcaption>
</figure>

这条线上有两种完全不同的动作：一种是**发声明**（莱顿宣言、25 位菲尔兹奖得主声明、以及随后陶哲轩牵头成立的「人类数学协会」），另一种是**平台限流**（arXiv）。把它们混为一谈，就会得到一个粗糙的结论：数学界在抵制 AI。

但只要读原文，这个结论站不住。

## 一、两份声明，靶子都是公司行为

先看《莱顿宣言》。它源于 2025 年 9 月荷兰莱顿的一场研讨会，16 人工作组花了八个月成文，发布后有 150 多位各国教授签署、24 小时内联署破千，并获国际数学联盟背书。它点名的风险清单是：AI 公司有「强烈的商业动机夸大其产品的能力」；成果「按市场时间线而非同行评议的时间线」发布；用特定数学任务误导性地充当通用推理能力的指标；模型吞食论文训练却不给署名。

再看 9 月 11 日那份 25 位菲尔兹奖得主的《人工智能在数学中的严重错位》。导火索是 OpenAI 宣称用一万个智能体、耗时 88 小时「完成」了纳维–斯托克斯千禧年难题的证明。声明的核心论点是：用「攻克多少著名难题」做模型能力基准，是一种危险的**指标替代**——一个著名问题之所以重要，不是因为最后那个「对/错」的结论，而是因为它充当知识版图上的灯塔：解决它意味着新洞见和新方法，随后需要漫长的演讲、讨论和简化，才能沉淀成教科书、进入下一代数学家的工具箱。批量生产「真/假」结论，「可能不是在孕育新的思想，反而可能摧毁孕育思想的沃土」。

但请注意，同一份声明里白纸黑字写着：**「AI 具有加强和加速真正数学研究与理解的潜力」**，并明确表示不主张拒绝 AI。

所以这两份文件的精确对象是：**公司把数学当作营销道具和投资筹码的行为**，而不是 AI 技术本身。宣言共同作者、哥伦比亚大学的 Michael Harris 对法新社说得最直白：各大实验室「在进行一场生死竞争……它们在**利用数学**吸引投资」。他还特别批评了一件事——OpenAI 前脚刚发布陶哲轩夸奖其产品的视频，后脚就把「解题数量」当广告打：「总是把同一个人当作数学的传声筒，这不健康。」

这个细节很有说服力：陶哲轩本人**亲自用 AI、公开承认 AI 的潜力、甚至为其站过台**，然后牵头写了抵制的声明。如果把他的立场读成「反 AI」，就没法解释这些事实；只有把抵制的对象读准——**反对的是消耗性的商业营销，不是加速本身**——所有事实才同时成立。

## 二、722 篇论文与一道限流令：被挤占的是公共品

10 月 6 日，OpenAI 在 GitHub 一次性发布 722 篇 AI 生成的数学论文，涵盖 372 组成果，扫射黎曼猜想、霍奇猜想等一批未解难题；部分证明附 Lean 形式化验证，官方口径是平均每项成果约消耗 ChatGPT Pro 三小时的推理量。

这件事的争议焦点，媒体大多放在「AI 到底做没做对」。但另一组数字揭示了真正的受力点：

<figure class="tao-fig">
<svg viewBox="0 0 680 280" width="100%" role="img" aria-label="arXiv 单月投稿量：2016 年 9 月 9869 篇，2024 年 9 月 20569 篇，2026 年 9 月 40363 篇">
<title>arXiv 单月投稿量：两年翻倍</title>
<text x="340" y="18" text-anchor="middle" font-size="12" font-weight="500" fill="var(--tao-fg)">arXiv 单月投稿量（每年 9 月）</text>
<rect x="110" y="153" width="90" height="37" rx="3" fill="var(--tao-acc)"/>
<text x="155" y="143" text-anchor="middle" font-size="12" font-weight="500" fill="var(--tao-fg)">9,869</text>
<text x="155" y="208" text-anchor="middle" font-size="11" fill="var(--tao-dim)">2016-09</text>
<rect x="300" y="114" width="90" height="76" rx="3" fill="var(--tao-acc)"/>
<text x="345" y="104" text-anchor="middle" font-size="12" font-weight="500" fill="var(--tao-fg)">20,569</text>
<text x="345" y="208" text-anchor="middle" font-size="11" fill="var(--tao-dim)">2024-09</text>
<rect x="490" y="40" width="90" height="150" rx="3" fill="var(--tao-warn)"/>
<text x="535" y="30" text-anchor="middle" font-size="12" font-weight="500" fill="var(--tao-fg)">40,363</text>
<text x="535" y="208" text-anchor="middle" font-size="11" fill="var(--tao-dim)">2026-09</text>
<line x1="80" y1="190" x2="620" y2="190" stroke="var(--tao-line)" stroke-width="1.5"/>
<text x="80" y="236" font-size="11" fill="var(--tao-dim)">同期产生近 9,000 张审核工单；cs.AI 类投稿两年增长超 6 倍。</text>
<text x="80" y="254" font-size="11" fill="var(--tao-dim)">2026-10-01 起：每人每月限投 2 篇、同时在审不超过 3 篇，被拒也占额度。</text>
<text x="80" y="272" font-size="11" fill="var(--tao-warn)">漏洞：配额只算实际提交者——团队可用不同合著者提交绕过，独立学者全额承受。</text>
</svg>
<figcaption>图 2 · arXiv 单月投稿量两年翻倍，审核是靠志愿者完成的公共劳动。限流令是平台的止血措施，但止血带扎在了所有人身上。</figcaption>
</figure>

arXiv 的内容审核由志愿者完成——这是一种**公共品**。过去，一个研究者能写多少篇论文存在生理上限，志愿者只需盯住少数异常高频的投稿者。AI 把这个前提打破了：论文的边际生产成本趋近于零，40,363 篇月投稿和近 9,000 张工单压在同一个志愿者体系上。10 月 1 日，arXiv 宣布全学科限流：每人每月最多投 2 篇，同时在审不超过 3 篇，被拒同样消耗额度。

注意这个措施的性质：它不是对 AI 的立场声明，而是**社区治理**——和小区电梯限载、马路限行是同一类动作。它的副作用也同样现实：配额只计算实际提交者，于是有团队的研究机构可以换不同合著者提交来绕过限额，而独立学者全额承受成本。审核资源被工业化量产挤占，止血带却扎在所有人身上——这是治理粗糙的代价，但它首先说明：**数学界真正在应对的，是公共品的承载力危机，而不是「AI 会不会做数学」的存在论危机。**

Anthropic 的数学家 Levent Alpöge 对 722 篇的评论补了另一角：这可能使「部分数学家的在研课题被 AI 抢先完成」。这句话值得记住——它不是「AI 做错了」，而是「AI 可能做对了，而且先于某个具体的人」。后者引发的痛感，和前者的技术问题，完全是两回事。

## 三、形式科学与自然科学的分野

为什么同样面对 AI，数学界的痛感比别的学科尖锐这么多？知乎该问题下有一位答主的框架，我认为切中了要害（以下为转述并略作整理）：**形式科学和自然科学，根本就是两种学科。**

<figure class="tao-fig">
<svg viewBox="0 0 680 292" width="100%" role="img" aria-label="形式科学与自然科学的对比：研究对象、判定标准、理解的地位、AI 的冲击点四个方面">
<title>形式科学与自然科学的分野</title>
<text x="185" y="22" text-anchor="middle" font-size="13" font-weight="500" fill="var(--tao-fg)">形式科学（数学）</text>
<rect x="40" y="34" width="290" height="240" rx="8" fill="var(--tao-fill)" stroke="var(--tao-line)" stroke-width="0.5"/>
<text x="56" y="58" font-size="11" fill="var(--tao-dim)">研究对象</text>
<text x="56" y="76" font-size="12" fill="var(--tao-fg)">人为构造的抽象结构</text>
<text x="56" y="106" font-size="11" fill="var(--tao-dim)">判定标准</text>
<text x="56" y="124" font-size="12" fill="var(--tao-fg)">证明（可被机械检验）</text>
<text x="56" y="154" font-size="11" fill="var(--tao-dim)">「理解」的地位</text>
<text x="56" y="172" font-size="12" fill="var(--tao-fg)">理解即目的本身——</text>
<text x="56" y="188" font-size="12" fill="var(--tao-fg)">绕过理解的答案近乎无效</text>
<text x="56" y="218" font-size="11" fill="var(--tao-dim)">AI 的冲击点</text>
<text x="56" y="236" font-size="12" fill="var(--tao-fg)">产出端被直接替代：</text>
<text x="56" y="252" font-size="12" fill="var(--tao-fg)">答案先于理解抵达</text>
<text x="495" y="22" text-anchor="middle" font-size="13" font-weight="500" fill="var(--tao-fg)">自然科学（应用）</text>
<rect x="350" y="34" width="290" height="240" rx="8" fill="var(--tao-fill)" stroke="var(--tao-line)" stroke-width="0.5"/>
<text x="366" y="58" font-size="11" fill="var(--tao-dim)">研究对象</text>
<text x="366" y="76" font-size="12" fill="var(--tao-fg)">现实存在的实际客体</text>
<text x="366" y="106" font-size="11" fill="var(--tao-dim)">判定标准</text>
<text x="366" y="124" font-size="12" fill="var(--tao-fg)">可验证的观察与实验</text>
<text x="366" y="154" font-size="11" fill="var(--tao-dim)">「理解」的地位</text>
<text x="366" y="172" font-size="12" fill="var(--tao-fg)">理解是奢侈品——</text>
<text x="366" y="188" font-size="12" fill="var(--tao-fg)">实践可以长期领先理论</text>
<text x="366" y="218" font-size="11" fill="var(--tao-dim)">AI 的冲击点</text>
<text x="366" y="236" font-size="12" fill="var(--tao-fg)">量变探索被加速：</text>
<text x="366" y="252" font-size="12" fill="var(--tao-fg)">堆量开发的成本趋近于零</text>
</svg>
<figcaption>图 3 · 两种学科对「理解」的态度完全不同。上一篇的医学史已经演示过右栏：阿司匹林用了 74 年才有人搞懂机制，没人觉得那 74 年的用药无效。</figcaption>
</figure>

自然科学的腰身上是柔软的：**没有任何一位现代自然科学家，会认为自己对世界的理解可以对抗一个能被反复验证的观察。** 能理解、并基于理解做进一步的设计开发，当然是最好的结果；但理解不了而疗效真实，绝大多数人的反应是「发现了一个新领域」，而不是「这东西不该存在」。实际问题存在主体性，解决问题的方法不存在主体性——没人真的在意应用科学用什么方法把问题解决，人们唯一担心的，是这个解法是不是「瞎猫碰上死耗子」、能不能**持续**。（这句担心，恰好就是本系列篇二的主题：靠什么区分「可持续的命中」和「一次性的运气」？靠验证设计，不靠理解。）

而且 AI 给自然科学的补位，恰好补在它最吃力的环节。自然科学里大量进展来自**量变探索**——筛选、扫描、暴力试错的堆量开发，而人类的「灵机一动」，多半只是在少数场景跳过了这段量变。当 AI 把量变的成本压到趋近于零，自然科学没有理由不拥抱它。这就像当年结构生物学拥抱冷冻电镜：施一公实验室是拥抱新工具最坚决的代表之一，拿到了巨大的窗口期优势；而当机时普及、条件成熟，「能解结构」从少数组的壁垒变成了整个学科的公共能力。这不是某个人的得失，而是**技术扩散的一般形状**——先拥抱者赢得窗口，工具普及后学科整体受益。数学大概率走同一条路，只是痛感更强。

因为数学是另一栏的学科：理解即目的。一个绕过了人类理解的「答案」，在自然科学里是待解释的现象，在数学里近乎无效——这也正是「主体性」问题只在形式科学里成立的原因。

## 四、赋魅：旁观者的「有用」与参与者的「价值」

但「主体性」这个词需要再拆一层。同一位答主给了一个更尖锐的观察：数学的主体性，某种意义上是一种**赋魅**的结果——这里说的「赋魅」，是指**价值需要被建构、而某些价值只有内行才能识别**。

<figure class="tao-fig">
<svg viewBox="0 0 680 288" width="100%" role="img" aria-label="同一对象的两层价值：旁观者感知直接层（好看、有用、能解题），参与者识别建构层（笔触、方法、传承），当 AI 能量产直接层，建构层的价值如何向旁观者证明">
<title>旁观者的「有用」与参与者的「价值」</title>
<defs><marker id="taoArrow2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>
<rect x="190" y="20" width="300" height="40" rx="8" fill="var(--tao-fill)" stroke="var(--tao-line)" stroke-width="0.5"/>
<text x="340" y="40" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="500" fill="var(--tao-fg)">同一幅画 · 同一副字 · 同一条定理</text>
<line x1="300" y1="60" x2="190" y2="92" stroke="var(--tao-dim)" stroke-width="1.5" marker-end="url(#taoArrow2)"/>
<line x1="380" y1="60" x2="490" y2="92" stroke="var(--tao-dim)" stroke-width="1.5" marker-end="url(#taoArrow2)"/>
<rect x="40" y="94" width="280" height="116" rx="8" fill="var(--tao-fill)" stroke="var(--tao-line)" stroke-width="0.5"/>
<text x="180" y="116" text-anchor="middle" font-size="12" font-weight="500" fill="var(--tao-fg)">旁观者 · 直接层</text>
<text x="180" y="138" text-anchor="middle" font-size="12" fill="var(--tao-fg)">「好看」「有用」「能解题」</text>
<text x="180" y="162" text-anchor="middle" font-size="11" fill="var(--tao-dim)">无需任何训练即可感知</text>
<text x="180" y="182" text-anchor="middle" font-size="11" fill="var(--tao-dim)">赏心悦目、拿来即用</text>
<rect x="360" y="94" width="280" height="116" rx="8" fill="var(--tao-fill)" stroke="var(--tao-acc)" stroke-width="1.5"/>
<text x="500" y="116" text-anchor="middle" font-size="12" font-weight="500" fill="var(--tao-fg)">参与者 · 建构层</text>
<text x="500" y="138" text-anchor="middle" font-size="12" fill="var(--tao-fg)">笔触 · 法度 · 方法 · 传承</text>
<text x="500" y="162" text-anchor="middle" font-size="11" fill="var(--tao-dim)">需要训练才能识别</text>
<text x="500" y="182" text-anchor="middle" font-size="11" fill="var(--tao-dim)">原作与赝品在此分层</text>
<rect x="90" y="232" width="500" height="40" rx="8" fill="none" stroke="var(--tao-warn)" stroke-width="1.5" stroke-dasharray="6 4"/>
<text x="340" y="252" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">当 AI 能批量产出直接层——建构层的价值，如何向旁观者证明？</text>
</svg>
<figcaption>图 4 · 两层价值的分离。绘画如此（AI 生图之争），书法如此（江湖体之争），数学亦如此。</figcaption>
</figure>

看两个现成的例子。一幅画，我觉得好看，它对我就有「赏心悦目」的价值；但如果没有基本的鉴赏训练，我看不懂笔触、看不出达成笔触需要的功夫，甚至分不清原作和低质赝品——从绘画共同体的标准看，这层更深的价值对我就是不存在的。AI 生图之争，争的就是这两层。一副字同理：外行看着「好看」的江湖体，可能每一笔都无法可依——书法层面的价值判断，同样需要训练才能做出。

这两个例子可以无缝衔接到数学：一条 AI 生成的证明，**直接层**（结论对不对、题解没解出来）是可以外包给机器检验的；**建构层**（方法新不新、和既有理论连不连、能不能进教科书）只有内行能评估。而数学的麻烦在于：绝大多数人的数学水平，停在直接层都不到的位置——他们连「题被解出来了」都无从感知，只能靠「千禧年难题」这类标签来想象价值。

所以，旁观者的「有用」和参与者的「价值」到底并驾齐驱，还是各有高低？答主的判断是：这个高低之分，本身就是建构出来的——是共同体长期叙事、教育和制度安排的结果。赋魅不是贬义词，它只是一种提醒：**这层价值是建构的，就可能被解构，也必须被重新建构。**

## 五、数学要向旁观者重新证明自己的价值

把三层合起来，数学此刻面对的真实处境是：

**其一，应用层面它很难靠「有用」自证。** 纳维–斯托克斯方程的全局正则性是否成立，对下游学科的工程实践几乎没有影响——模拟照跑、飞机照飞。邓煜等人从微观粒子系统严格推导流体方程的工作（希尔伯特第六问题的核心进展），对分子动力学模拟的影响同样接近于零：**实践总是比理论领先一小步；实践能被理论解释，从不意味着实践要等理论颁发出场许可。** 这条路，篇一已经走通过一遍。

**其二，生产层面它守不住稀缺性。** 722 篇论文证明了解题的边际成本可以趋近于零，而 arXiv 限流令证明了共同体目前只有「限载」这一种粗糙的防御。靠抵制公司建构不出价值，靠限制工具同样建构不出来——正如当年没人能靠限制冷冻电镜来保住结构生物学的旧壁垒。

**其三，主体性层面它必须回答一个从未真正被迫回答的问题：** 纯数学除了对从业者本身，是否还有超过 AI 的价值？如果有，用什么向旁观者展示？

这个问题没有现成答案，但可以排除几个错误答案。向旁观者喊「你们不懂它的美」是无效的——建构层的价值本来就只对能识别它的人敞开，喊不改变这个事实。把「AI 会犯错」当作价值的来源也不成立——验证机越来越便宜，这条路在篇二已经封死。唯一站得住的方向，恰恰是陶哲轩在 Math 2.0 里指的那条：把 AI 的算力**引向理解一侧**——为晦涩的证明生成阐释、把结果连回知识的版图、让下一代人还能被训练出来。换句话说：**数学要向旁观者证明的价值，不在「答案」里，在「理解被传承」里；而这件事，AI 恰好可以是最强的杠杆，只要你肯把它瞄准对的地方。**

数学家们这个月的声明、限流和讲座，与其说是抵制，不如说是一个学科在重新议定自己价值的开场哨。

---

*参考来源：知乎问题页（zhihu.com/question/2092937311851902232）及该问题下答主讨论（第三、四节框架经转述整理）；《莱顿宣言》相关报道（AFP/Geo News、Indian Express）；25 位菲尔兹奖得主《人工智能在数学中的严重错位》声明及报道；arXiv 官方博客《Fair Moderation, Equitable Access, and AI》（2026-10-01）及虎嗅、InfoQ、DeepTech 报道；OpenAI 722 篇数学论文相关报道（腾讯新闻、量子位）；陶哲轩 Math 2.0 讲稿（teorth.github.io/tao-web/slides/math-2-0-caltech-2026.pdf）。*
