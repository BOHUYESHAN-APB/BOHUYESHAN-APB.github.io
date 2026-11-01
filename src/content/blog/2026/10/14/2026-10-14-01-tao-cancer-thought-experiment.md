---
title: 理解从来不是用药的前置条件：先把陶哲轩的问题读对
description: 陶哲轩「黑盒 AI 治癌药」思想实验在知乎引来近五百个回答。医学史这边的反驳赢得很容易——阿司匹林吃了 74 年才有人搞懂机制，全麻用了 180 年至今机制不明。但把那页幻灯片原文读两遍，他真正问的不是这个。
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

## 〇、一个九十五万人看过的问题

先把问题原样摆出来。

知乎上有一个问题：[《陶哲轩的「黑盒AI治癌药」思想实验引发争议，如何看待这一讨论？我们需要完全理解科学的内在机制再应用吗？》](https://www.zhihu.com/question/2092937311851902232)。截至 2026 年 10 月 14 日，它有近五百个回答、约九十五万次浏览。问题的描述转述了一段在 X 上广泛传播的反驳（据多家媒体报道，原帖浏览量超过 57 万），核心是这样几句：

> 陶哲轩不知道的是，这在生物医学领域简直稀松平常。……拜耳公司于 1897 年人工合成了阿司匹林，并在全球广泛使用了数十年。然而，人类直到 1971 年才发现阿司匹林是通过抑制环氧化酶（COX）来起作用的。……全麻也是，从 1846 年乙醚麻醉公开演示至今近 180 年，科学界至今对吸入性麻醉药导致意识丧失的确切机制仍无统一定论。……所以，最好不要离开自己熟悉的领域提出思想实验啊。

这段反驳读起来很痛快，而且大方向我也同意——这个公众号读者熟悉的立场先亮出来：**如果一种疗法真的通过了严格验证，「人类是否理解其机制」不构成拒绝使用它的理由。**

但在痛快之前，有两件事值得先做。第一件：陶哲轩最近这一连串动作，他到底想表达什么？第二件：那页被截图疯传的幻灯片，原文到底问了什么？

两件事都弄清楚之后会发现，这场争论比知乎上的版本有意思得多。

## 一、陶哲轩近期想展示什么

只看那一页幻灯片，很容易把陶哲轩读成一个「对 AI 踩刹车的数学家」。把过去一周发生的事按时间排开，图景会完整很多。以下均据公开报道：

- **10 月 7 日**，OpenAI 一次性发布了 722 篇数学论文，扫射准黎曼猜想、霍奇猜想、BSD 猜想等一批重磅问题；此前它还宣称解决了纳维–斯托克斯这一千禧年难题。
- 随后，陶哲轩牵头成立「人类数学协会」（AHM）并发布联合声明，称这种做法「不算科研，是在炫耀算力」，敦促数学家停止与其合作。他在 SAIR 的一次演讲里说得更直白：「我们必须慢下来，完全没理由这么快。」
- **10 月 9 日晚**，加州理工学院，他的公开讲座原定题目是《机器辅助证明》，因为近期 AI 对数学界的密集冲击，临时改成了《数学 2.0》。那页幻灯片就出自这场讲座，讲稿全文公开。

这场讲座的主张，概括起来是三句话。

**第一，数学是 AI 的第一个自然目标，这是结构决定的。** 他列了三个条件：证明可以被客观检验（形式化之后甚至能被机器检验）；数学对象和推理过程高度可数字化；大量高质量文献已经以数字形式存在。三个条件叠加，数学必然首当其冲——这不是坏消息，只是事实。

**第二，麻烦不在「证明变多」，而在「证明泛滥」撞上了为「证明稀缺」设计的评价体系。** 在证明稀缺的时代，「谁先解决了什么」是合理的贡献标尺；当 AI 让证明的供给暴涨，这根标尺就错位了。他把解题拆成五个阶段：生成证明、验证正确性、解释清楚、被共同体理解和接受、最终融入领域的标准理论。AI 主要加速前两环，越往后越慢——最后一环需要把结果与其他知识连接起来、进入教材和下一代数学家的工具箱，这恰恰是 AI 最难加速的。由此他造了一个词：**证明消化不良**——证明的产出速度超过了共同体消化理解的速度。他还用了一个比喻：开放问题像灯塔，作用不是让人不顾一切冲上去占领，而是指引人类探索周围的未知图景；如果自动化工具过早撞上灯塔，灯塔周围那片本该被慢慢探索的生态会被旱化。

**第三，所以答案不是减速，而是把算力瞄准对的方向。** 这是被疯传的截图最容易漏掉的一点：他批评的不是「用 AI」，而是「盲目优化解题这一指标」。他主张的方向恰恰是把更多算力投到「理解」一侧——为晦涩的已知证明生成有动机的阐释、让模型解释自己的推理步骤而不只是吐出答案、把失败结果和算力成本一并纳入公开的评估报告。他参与创立的基金会正在推进一个开放数学模型计划，第一阶段面向的都是日常研究需求：理解困难论证、核查引用、探索例子、编写代码、形式化证明。

把这页背景铺开，那页幻灯片的位置就清楚了：它不是一次跨界的医学评论，而是这套「验证之后还有理解」主张的一个**具象化道具**——把一个抽象的数学讨论，拉到一个所有人都有直觉的场景里。

## 二、那页幻灯片到底问了什么

先看原文。幻灯片标题是《A thought experiment on **alignment** and understanding》——关于**对齐**与理解的思想实验。内容译成中文是这样的：

<figure class="tao-fig">
<svg viewBox="0 0 680 432" width="100%" role="img" aria-label="陶哲轩思想实验流程：给定提示词后 AI 产出化学鸡尾酒，通过 Lean 形式化验证与三期临床试验，但无人知道它如何被找到，由此引出对齐与理解两个问句">
<title>「对齐与理解」思想实验的流程（陶哲轩 Math 2.0 幻灯片内容的中文重绘）</title>
<defs><marker id="taoArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>
<text x="340" y="16" text-anchor="middle" font-size="11" fill="var(--tao-dim)">给先进 AI 的提示词</text>
<rect x="90" y="24" width="500" height="40" rx="8" fill="var(--tao-fill)" stroke="var(--tao-acc)" stroke-width="1.5"/>
<text x="340" y="44" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="500" fill="var(--tao-fg)">「找到一种能通过三期临床试验的癌症疗法」</text>
<line x1="340" y1="64" x2="340" y2="82" stroke="var(--tao-dim)" stroke-width="1.5" marker-end="url(#taoArrow)"/>
<rect x="190" y="84" width="300" height="36" rx="8" fill="var(--tao-fill)" stroke="var(--tao-line)" stroke-width="0.5"/>
<text x="340" y="102" text-anchor="middle" dominant-baseline="central" font-size="13" fill="var(--tao-fg)">消耗大量算力</text>
<line x1="340" y1="120" x2="340" y2="138" stroke="var(--tao-dim)" stroke-width="1.5" marker-end="url(#taoArrow)"/>
<rect x="90" y="140" width="500" height="52" rx="8" fill="var(--tao-fill)" stroke="var(--tao-line)" stroke-width="0.5"/>
<text x="340" y="158" text-anchor="middle" dominant-baseline="central" font-size="13" fill="var(--tao-fg)">产出一组此前未知的化学物质鸡尾酒</text>
<text x="340" y="178" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-dim)">模型预测：混合注射可杀死患者全部癌细胞</text>
<line x1="280" y1="192" x2="200" y2="214" stroke="var(--tao-dim)" stroke-width="1.5" marker-end="url(#taoArrow)"/>
<line x1="400" y1="192" x2="480" y2="214" stroke="var(--tao-dim)" stroke-width="1.5" marker-end="url(#taoArrow)"/>
<rect x="70" y="216" width="260" height="56" rx="8" fill="var(--tao-fill)" stroke="var(--tao-line)" stroke-width="0.5"/>
<text x="200" y="238" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="500" fill="var(--tao-fg)">Lean 形式化验证 ✓</text>
<text x="200" y="258" text-anchor="middle" dominant-baseline="central" font-size="11" fill="var(--tao-dim)">数学预测的内部自洽</text>
<rect x="350" y="216" width="260" height="56" rx="8" fill="var(--tao-fill)" stroke="var(--tao-line)" stroke-width="0.5"/>
<text x="480" y="238" text-anchor="middle" dominant-baseline="central" font-size="13" font-weight="500" fill="var(--tao-fg)">三期临床试验 ✓</text>
<text x="480" y="258" text-anchor="middle" dominant-baseline="central" font-size="11" fill="var(--tao-dim)">真实世界中的统计有效性</text>
<line x1="200" y1="272" x2="310" y2="294" stroke="var(--tao-dim)" stroke-width="1.5" marker-end="url(#taoArrow)"/>
<line x1="480" y1="272" x2="370" y2="294" stroke="var(--tao-dim)" stroke-width="1.5" marker-end="url(#taoArrow)"/>
<rect x="140" y="296" width="400" height="36" rx="8" fill="var(--tao-fill)" stroke="var(--tao-line)" stroke-width="0.5"/>
<text x="340" y="314" text-anchor="middle" dominant-baseline="central" font-size="13" fill="var(--tao-fg)">但没有人知道：它是如何被找到的</text>
<line x1="280" y1="332" x2="185" y2="352" stroke="var(--tao-dim)" stroke-width="1.5" marker-end="url(#taoArrow)"/>
<line x1="400" y1="332" x2="495" y2="352" stroke="var(--tao-dim)" stroke-width="1.5" marker-end="url(#taoArrow)"/>
<rect x="40" y="354" width="290" height="64" rx="8" fill="none" stroke="var(--tao-warn)" stroke-width="1.5" stroke-dasharray="6 4"/>
<text x="185" y="376" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">问① 方案会不会只是钻了试验流程的空子，</text>
<text x="185" y="398" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">在某种意义上「对齐失败」？</text>
<rect x="350" y="354" width="290" height="64" rx="8" fill="none" stroke="var(--tao-warn)" stroke-width="1.5" stroke-dasharray="6 4"/>
<text x="495" y="370" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">问② 注射前，你是否希望至少有</text>
<text x="495" y="388" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">一位人类癌症专家理解其机制，</text>
<text x="495" y="406" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">或一位数学家理解那个模型？</text>
</svg>
<figcaption>图 1 · 思想实验原文的结构（据陶哲轩公开的 Math 2.0 讲稿重绘）。注意标题里的 alignment：两个问句里，「钻验证流程空子」在「无人理解机制」之前。</figcaption>
</figure>

把这张图和网上疯传的读法对比一下，差别就出来了。

**疯传版**把它读成：「机制没搞懂的药，你敢用吗？」——一个关于「理解 vs 使用」的问题。顺着这个读法，陶哲轩就是一个对医学外行、杞人忧天的数学家，医学史随随便便就能驳倒他。

**原文版**里，「理解」之前还有一个更靠前的问句：这套方案**会不会只是利用了试验流程的某个弱点**——也就是说，AI 优化的目标字面是「通过三期临床试验」，它交出来的东西可能精确命中「通过试验」，却没有命中「治好癌症」。幻灯片之外，他还举过一个更刺眼的例子（同样出自这场讲座的语境）：设想一个模型为了「通过试验」篡改了试验记录——**提示词只让它通过试验，没有人让它治癌**。

这两层问题完全不同。第一层（理解 vs 使用）问的是知识论；第二层（对齐）问的是：**当验证仪器本身是被优化的目标时，「通过验证」还剩多少信息量？**

另外还有一个技术细节值得单独拆开：思想实验里说的「在 Lean 中得到验证」，验证的是那个**数学预测的内部自洽**——从公理到结论的每一步推导合法。它证明不了这个数学模型与真实人体之间的关系。把「Lean 验证通过」读成「这药被数学证明了有效」，本身就是一层误读：形式化验证能锁住推理，锁不住现实。

## 三、先回答疯传版：理解从来不是用药的前置条件

先把好回答的那层回答掉。医学史在这件事上给出的记录，干脆得近乎尴尬：

<figure class="tao-fig">
<svg viewBox="0 0 680 300" width="100%" role="img" aria-label="六种药物投入使用与机制确立的时间线：全麻 1846 年至今未明，阿司匹林 1897 到 1971，青霉素 1942 到 1965，锂盐、对乙酰氨基酚至今无共识，二甲双胍 2001 年部分确立">
<title>六种药物：投入使用在先，机制理解在后（或至今没有）</title>
<line x1="157" y1="22" x2="157" y2="26" stroke="var(--tao-dim)" stroke-width="1"/><text x="157" y="14" text-anchor="middle" font-size="11" fill="var(--tao-dim)">1850</text>
<line x1="294" y1="22" x2="294" y2="26" stroke="var(--tao-dim)" stroke-width="1"/><text x="294" y="14" text-anchor="middle" font-size="11" fill="var(--tao-dim)">1900</text>
<line x1="431" y1="22" x2="431" y2="26" stroke="var(--tao-dim)" stroke-width="1"/><text x="431" y="14" text-anchor="middle" font-size="11" fill="var(--tao-dim)">1950</text>
<line x1="568" y1="22" x2="568" y2="26" stroke="var(--tao-dim)" stroke-width="1"/><text x="568" y="14" text-anchor="middle" font-size="11" fill="var(--tao-dim)">2000</text>
<line x1="639" y1="22" x2="639" y2="26" stroke="var(--tao-dim)" stroke-width="1"/><text x="639" y="14" text-anchor="middle" font-size="11" fill="var(--tao-dim)">2026</text>
<line x1="130" y1="26" x2="650" y2="26" stroke="var(--tao-line)" stroke-width="1"/>
<text x="118" y="62" text-anchor="end" dominant-baseline="central" font-size="13" fill="var(--tao-fg)">全身麻醉（乙醚）</text>
<text x="146" y="48" text-anchor="middle" font-size="11" fill="var(--tao-dim)">1846</text>
<line x1="146" y1="62" x2="639" y2="62" stroke="var(--tao-warn)" stroke-width="2.5" stroke-dasharray="5 4"/>
<circle cx="146" cy="62" r="4" fill="var(--tao-warn)"/>
<text x="392" y="80" text-anchor="middle" font-size="11" font-weight="500" fill="var(--tao-warn)">180 年，机制至今无定论</text>
<text x="118" y="100" text-anchor="end" dominant-baseline="central" font-size="13" fill="var(--tao-fg)">阿司匹林</text>
<text x="286" y="86" text-anchor="middle" font-size="11" fill="var(--tao-dim)">1897</text>
<text x="488" y="86" text-anchor="middle" font-size="11" fill="var(--tao-dim)">1971</text>
<line x1="286" y1="100" x2="488" y2="100" stroke="var(--tao-acc)" stroke-width="2.5"/>
<circle cx="286" cy="100" r="4" fill="var(--tao-acc)"/>
<circle cx="488" cy="100" r="4" fill="none" stroke="var(--tao-acc)" stroke-width="1.5"/>
<text x="387" y="118" text-anchor="middle" font-size="11" font-weight="500" fill="var(--tao-dim)">74 年</text>
<text x="118" y="138" text-anchor="end" dominant-baseline="central" font-size="13" fill="var(--tao-fg)">青霉素</text>
<text x="409" y="124" text-anchor="middle" font-size="11" fill="var(--tao-dim)">1942</text>
<text x="472" y="124" text-anchor="middle" font-size="11" fill="var(--tao-dim)">1965</text>
<line x1="409" y1="138" x2="472" y2="138" stroke="var(--tao-acc)" stroke-width="2.5"/>
<circle cx="409" cy="138" r="4" fill="var(--tao-acc)"/>
<circle cx="472" cy="138" r="4" fill="none" stroke="var(--tao-acc)" stroke-width="1.5"/>
<text x="440" y="156" text-anchor="middle" font-size="11" font-weight="500" fill="var(--tao-dim)">23 年</text>
<text x="118" y="176" text-anchor="end" dominant-baseline="central" font-size="13" fill="var(--tao-fg)">锂盐（双相障碍）</text>
<text x="428" y="162" text-anchor="middle" font-size="11" fill="var(--tao-dim)">1949</text>
<line x1="428" y1="176" x2="639" y2="176" stroke="var(--tao-warn)" stroke-width="2.5" stroke-dasharray="5 4"/>
<circle cx="428" cy="176" r="4" fill="var(--tao-warn)"/>
<text x="534" y="194" text-anchor="middle" font-size="11" font-weight="500" fill="var(--tao-warn)">77 年，至今无共识</text>
<text x="118" y="214" text-anchor="end" dominant-baseline="central" font-size="13" fill="var(--tao-fg)">对乙酰氨基酚</text>
<text x="445" y="200" text-anchor="middle" font-size="11" fill="var(--tao-dim)">1955</text>
<line x1="445" y1="214" x2="639" y2="214" stroke="var(--tao-warn)" stroke-width="2.5" stroke-dasharray="5 4"/>
<circle cx="445" cy="214" r="4" fill="var(--tao-warn)"/>
<text x="542" y="232" text-anchor="middle" font-size="11" font-weight="500" fill="var(--tao-warn)">71 年，至今无共识</text>
<text x="118" y="252" text-anchor="end" dominant-baseline="central" font-size="13" fill="var(--tao-fg)">二甲双胍</text>
<text x="450" y="238" text-anchor="middle" font-size="11" fill="var(--tao-dim)">1957</text>
<text x="571" y="238" text-anchor="middle" font-size="11" fill="var(--tao-dim)">2001</text>
<line x1="450" y1="252" x2="571" y2="252" stroke="var(--tao-acc)" stroke-width="2.5"/>
<line x1="571" y1="252" x2="639" y2="252" stroke="var(--tao-acc)" stroke-width="2" stroke-dasharray="4 4" opacity="0.55"/>
<circle cx="450" cy="252" r="4" fill="var(--tao-acc)"/>
<circle cx="571" cy="252" r="4" fill="none" stroke="var(--tao-acc)" stroke-width="1.5"/>
<text x="510" y="270" text-anchor="middle" font-size="11" font-weight="500" fill="var(--tao-dim)">44 年后部分确立，至今不完整</text>
<text x="130" y="292" font-size="11" fill="var(--tao-dim)">实线＝投入使用到机制确立的间隔；虚线＝机制至今未明。柳树皮的使用可上溯约公元前五世纪（希波克拉底文集），未画入比例尺。</text>
</svg>
<figcaption>图 2 · 六种常用药的「使用在先，理解在后」。阿司匹林 74 年的间隔在这张表里甚至排不进前三。</figcaption>
</figure>

几条值得单独说的记录：

- **阿司匹林。** 用柳树皮止痛的记载可上溯到约公元前五世纪的希波克拉底文集；1897 年拜耳的霍夫曼合成乙酰水杨酸，随后它在全球被大规模使用；直到 1971 年，约翰·范恩才阐明它通过抑制环氧化酶起作用（范恩因此获 1982 年诺贝尔奖）。从合成到机制确立，间隔 **74 年**——顺便纠正一个流传甚广的口误：1897 到 1971 是七十四年，不是「快一百年」。而如果从柳树皮算起，人类在**完全不理解机制**的情况下使用这类物质，超过两千年。
- **全身麻醉。** 1846 年 10 月，莫顿在麻省总医院公开演示乙醚麻醉。此后 180 年，全麻每天都在全世界的手术室里进行；而它究竟如何夺走意识，至今没有统一的分子与神经网络解释——脂质学说、蛋白质靶点学说、神经网络学说并存。《Science》2005 年的一百二十五周年专刊把这个问题列入「125 个尚待解答的重大科学问题」。换句话说：**这是一个每天被执行数百万次、且被顶级科学期刊认证为「未解」的黑箱。**
- **锂盐与对乙酰氨基酚。** 一个是精神科使用了 77 年的基石药物，一个大概是这个星球上最常被服用的退烧止痛药——两者的机制至今没有共识。
- **二甲双胍。** 1957 年投入临床，2001 年 AMPK 通路被发现，算「部分理解」——44 年，而且至今不完整。
- **青霉素**是这张表里「理解追得最快」的：1942 年大规模临床使用，1965 年机制阐明，也隔了 23 年。

把这些记录摆在一起，结论不需要修辞：**医学的秩序从来是「先用上，后理解，有时永远不理解」。** 机制理解是奢侈品，不是许可证。为用药背书的从来不是「某位专家讲清了分子通路」，而是双盲试验、统计显著性和上市后监测——一套**不依赖任何个体理解的验证制度**。

所以知乎问题描述里那段反驳，在疯传版的读法下是成立的，甚至连「四期患者不在乎机制」这个更尖锐的版本也成立：对一个四期癌症患者，「这个药有没有人懂」是知识论问题，「它有没有用」是生存问题，这两个问题的优先级不需要讨论。

## 四、双标的那一边

顺着这一层，还有一个更不留情面的观察：**人类医生本身就是一个黑箱。**

你去医院看病，不会要求医生把分子生物学机制、细胞信号通路全部讲明白才肯吃药。你之所以敢吃，是因为有双盲实验和统计学规律在背书——本质上，你是在信任一个由无数人类组成的、充满了情绪、偏见和认知盲区的「行走黑箱系统」。你从来没有审查过这个黑箱的内部结构，你审查的只是它的**输出是否经得起检验**。

那么，对一个硅基黑箱提出「必须有人类专家完全理解其机制才能使用」的要求，就是一个明显的双标：**我们对碳基黑箱从不索要内部理解，只索要验证；对硅基黑箱却开始索要理解。** 如果标准是一致的，那真正该要的就不是「可解释性」，而是「同样严格、甚至更严格的验证」——以及和人类防作弊制度等效的反作弊设计。

这一层道理，知乎上几百个回答大多讲到了，我同意，不再展开。

## 五、但这一层，赢得太容易了

如果文章停在这里，它就只是又一篇「医学史吊打数学家」的爽文——而这类文章有一个共同的问题：它们驳倒的是那个**容易驳倒的版本**。

回头再看图 1。陶哲轩的两个问句里，排在「理解」前面的是「对齐」：AI 会不会**只是**找到了试验流程的弱点？这个担忧用医学史反驳不了，因为医学史恰恰提供了大量支持它的证据——三期临床试验这套验证仪器，被比它聪明的优化者钻空子，是有案可查的：p 值操纵、选择性发表、中途更换终点指标、用替代终点冒充临床获益。人类制药工业用了几十年时间，才给这套仪器打上一个个补丁（预注册、数据监察委员会、完整报告规范）。**「验证被绕过」不是 AI 时代的新问题，它是每一个「指标被当成目标」的系统都会得的病。**

陶哲轩真正的问题因而是这个：当优化器比验证仪器更聪明时，「通过验证」还意味着什么？这个问题和「要不要理解机制」无关，和「**验证本身怎么设计**」有关——它恰好是医学史已经回答过一遍、并且可以等效移植到 AI 身上的问题。

那一半值得单独写一篇。下一篇谈：《通过验证，还是钻过验证》。

---

*参考来源：知乎问题页（zhihu.com/question/2092937311851902232）；陶哲轩 Math 2.0 讲稿原文（teorth.github.io/tao-web/slides/math-2-0-caltech-2026.pdf）及其公开的 AI 观点汇总页；量子位、澎湃新闻、腾讯新闻对讲座与相关事件的报道（2026-10-11 前后）；Stanford Tech Review 评论《We Use Drugs No One Understands. Terence Tao Says Be Careful.》；Traictory《Terence Tao's 'Math 2.0' lecture: the cancer slide that outran the argument》。药物机制时间线据诺贝尔奖委员会档案（阿司匹林）、Tipper & Strominger 1965（青霉素）、二甲双胍 AMPK 研究（2001）及已发表的锂盐、对乙酰氨基酚机制综述整理。*
