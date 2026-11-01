---
title: 四种做生物计算的人：回流落在哪一层
description: 把「搞生物计算的那批人」拆成四类：一次性计算、工具与应用开发、算法开发、Agent 应用开发。它们在五个分量上的缺口各不相同，而真正决定分层的不是能力清单，是复用方向——同一个能力面对很多客户，还是一个客户面对很多问题。
publishDate: 2026-10-10
tags: [职场, 技术拆解, 生信技术, Agent]
draft: false
---

<!-- 本文 SVG 配图的主题变量：颜色跟随站点主题（见 src/assets/styles/app.css 的 --primary / --foreground / --muted / --card），.dark 由主题脚本挂在 <html> 上。 -->

<style>
  .fdf-fig {
    --fdf-fg: hsl(var(--foreground));
    --fdf-dim: hsl(var(--muted-foreground));
    --fdf-line: hsl(var(--border));
    --fdf-fill: hsl(var(--muted));
    --fdf-card: hsl(var(--card));
    --fdf-acc: hsl(var(--primary));
    --fdf-warn: hsl(28 88% 44%);
    margin: 2.25rem 0;
  }
  .dark .fdf-fig {
    --fdf-warn: hsl(32 90% 62%);
  }
  .fdf-fig svg {
    display: block;
    width: 100%;
    height: auto;
  }
  .fdf-fig figcaption {
    margin-top: 0.7rem;
    font-size: 0.82em;
    line-height: 1.6;
    color: hsl(var(--muted-foreground));
    text-align: center;
  }
</style>

## 〇、一个场景：一个甲方，四个问题

先摆一个场景。它是拼出来的，不对应任何一家的岗位描述原文。

某个做培养与检测的团队手上有四个问题：

1. **培养物长到什么状态了？** 靠人工看图像，看不过来，不同人的判读还不一致。
2. **这一批是不是污染了？** 和前一个状态判别共用同一套成像流程，但判据不同。
3. **换一个培养体系，检测模型得重训。** 标注、训练、评估的流程和上一次几乎一样。
4. **结果要写成非计算背景的人也能读懂的报告。** 图表版式、结论表述，格式基本固定。

这四件事有一个共同点：它们都不是提出者自己能做的，也都不是纯粹的工程问题。第一件要知道"什么算状态正常"，第二件要知道"污染在图像上长什么样、最容易和什么混淆"，第四件要知道"读者会在哪里读错"。

于是有一个人被派去接这四个问题。他不是这四个问题的提出者；他的位置是**把问题变成可以直接用的东西**。

问题来了：这个人的岗位该叫什么，他算不算 FDE？

## 一、先把「搞生物计算的那批」拆开

[10-10 那篇](/2026/10/10/2026-10-10-01-what-is-fde-five-components-and-nine-stages/)给过一把尺子：

> FDE = 工程能力 × 领域理解 × 现场嵌入 × 端到端交付 × 产品回流。五项相乘，任一项为零则整体退化。

尺子有了，"做生物计算的人算不算 FDE"这个问题才问得出来。但它一问出来就会踩一个坑：**把"那批人"当成一个群体**。

那个群体里至少有四种人：

- **A 一次性计算**：为某个课题算一遍，论文发出来，这件事就结束了。代码留在某台机器上，只有本人跑得起来。
- **B 工具 / 应用开发**：把分析流程封装成别人能直接用的程序。有人用、有人提意见、有人维护。
- **C 算法开发**：懂生物问题的建模者。知道某个生物学问题可以抽象成什么模型、某个统计假设在生物学上站不站得住。
- **D Agent 应用开发**：把一个客户身上的多个生物问题串成一套可复用的交付——判读、判别、报告，共用同一层能力。

区分这四种人的，**不是技术栈**。技术栈描述的是手上有什么工具；这四种人的差别在另一件事上：**做过的东西死没死**。

换句话说，分层的变量是**复用方向**，不是能力高低。这是后面全部推理的支点。

## 二、五个分量在这四类人身上的分布

**A 一次性计算。** 工程"够用"——会调工具、会写脚本，但不迁移、不封装，换台机器就跑不起来。领域理解卡在两端：能读文献、看得懂指标，但**不参与问题的定义，也不做机制解释**——而这一项的权重恰恰压在管线的首尾。现场是缺的：被动接需求，出了问题归因到"数据有问题"。交付是断的：只覆盖管线的中段。第五项为零。

**B 工具 / 应用开发。** 工程强。领域打折，打折的方式值得注意：他的领域知识往往是**二手的**——通过用户反馈学来的，不是自己做实验得来的。这不是缺点，它恰好说明他的**领域理解和现场嵌入是同一件事的两个侧面**。交付强：交的不是一次分析，是一个别人能用的东西。第五项落在领域层。

**C 算法开发。** 工程强，领域强，但领域是**建模级**的——知道问题能抽象成什么模型，不等于知道培养箱里会发生什么。现场最缺。交付视组织而定：在企业里做产品，交付是完整的；在学术组里，往往只交一个方法加一组对照。第五项落在领域层。

**D Agent 应用开发。** 五项全中。现场嵌入是真的——"污染在图像上最容易和什么混淆"这类知识，只有到现场才拿得到。交付是端到端的：从原始数据一直到报告。第五项落在个人层，理由在第四节。

<figure class="fdf-fig">
<svg viewBox="0 0 720 340" role="img" aria-label="四类做生物计算的人在五个分量上的命中矩阵：A 类一次性计算只在中段有东西，B 类工具与应用开发、C 类算法开发都缺在第五项，D 类 Agent 应用开发五项齐全">
  <text x="16" y="20" font-size="13" font-weight="600" fill="var(--fdf-fg)">四类人 × 五个分量：缺口的位置各不相同</text>
  <text x="16" y="40" font-size="11.5" fill="var(--fdf-dim)">读数：A 类只有中段；B 与 C 的缺口都在第五项；D 类五项齐全。</text>
  <text x="202" y="70" font-size="11.5" fill="var(--fdf-dim)" text-anchor="middle">工程</text>
  <text x="314" y="70" font-size="11.5" fill="var(--fdf-dim)" text-anchor="middle">领域</text>
  <text x="426" y="70" font-size="11.5" fill="var(--fdf-dim)" text-anchor="middle">现场</text>
  <text x="538" y="70" font-size="11.5" fill="var(--fdf-dim)" text-anchor="middle">交付</text>
  <text x="650" y="70" font-size="11.5" fill="var(--fdf-dim)" text-anchor="middle">回流</text>
  <text x="16" y="101" font-size="13" font-weight="600" fill="var(--fdf-fg)">A 一次性计算</text>
  <text x="16" y="119" font-size="11.5" fill="var(--fdf-dim)">为课题算一遍</text>
  <rect x="150" y="84" width="104" height="48" rx="7" fill="none" stroke="var(--fdf-warn)" stroke-dasharray="5 3"/>
  <text x="202" y="108" font-size="12" fill="var(--fdf-fg)" text-anchor="middle">够用</text>
  <rect x="262" y="84" width="104" height="48" rx="7" fill="none" stroke="var(--fdf-warn)" stroke-dasharray="5 3"/>
  <text x="314" y="108" font-size="12" fill="var(--fdf-fg)" text-anchor="middle">浅</text>
  <rect x="374" y="84" width="104" height="48" rx="7" fill="none" stroke="var(--fdf-line)" stroke-dasharray="4 3"/>
  <text x="426" y="108" font-size="12" fill="var(--fdf-dim)" text-anchor="middle">缺</text>
  <rect x="486" y="84" width="104" height="48" rx="7" fill="none" stroke="var(--fdf-warn)" stroke-dasharray="5 3"/>
  <text x="538" y="108" font-size="12" fill="var(--fdf-fg)" text-anchor="middle">只中段</text>
  <rect x="598" y="84" width="104" height="48" rx="7" fill="none" stroke="var(--fdf-line)" stroke-dasharray="4 3"/>
  <text x="650" y="108" font-size="12" fill="var(--fdf-dim)" text-anchor="middle">无</text>
  <text x="16" y="157" font-size="13" font-weight="600" fill="var(--fdf-fg)">B 工具 / 应用开发</text>
  <text x="16" y="175" font-size="11.5" fill="var(--fdf-dim)">封装成别人能用的东西</text>
  <rect x="150" y="140" width="104" height="48" rx="7" fill="var(--fdf-fill)" stroke="var(--fdf-acc)"/>
  <text x="202" y="164" font-size="12" fill="var(--fdf-fg)" text-anchor="middle">强</text>
  <rect x="262" y="140" width="104" height="48" rx="7" fill="none" stroke="var(--fdf-warn)" stroke-dasharray="5 3"/>
  <text x="314" y="164" font-size="12" fill="var(--fdf-fg)" text-anchor="middle">中</text>
  <rect x="374" y="140" width="104" height="48" rx="7" fill="var(--fdf-fill)" stroke="var(--fdf-acc)"/>
  <text x="426" y="164" font-size="12" fill="var(--fdf-fg)" text-anchor="middle">真嵌入</text>
  <rect x="486" y="140" width="104" height="48" rx="7" fill="var(--fdf-fill)" stroke="var(--fdf-acc)"/>
  <text x="538" y="164" font-size="12" fill="var(--fdf-fg)" text-anchor="middle">强</text>
  <rect x="598" y="140" width="104" height="48" rx="7" fill="none" stroke="var(--fdf-warn)" stroke-dasharray="5 3"/>
  <text x="650" y="164" font-size="12" fill="var(--fdf-fg)" text-anchor="middle">领域级</text>
  <text x="16" y="213" font-size="13" font-weight="600" fill="var(--fdf-fg)">C 算法开发</text>
  <text x="16" y="231" font-size="11.5" fill="var(--fdf-dim)">懂生物问题的建模者</text>
  <rect x="150" y="196" width="104" height="48" rx="7" fill="var(--fdf-fill)" stroke="var(--fdf-acc)"/>
  <text x="202" y="220" font-size="12" fill="var(--fdf-fg)" text-anchor="middle">强</text>
  <rect x="262" y="196" width="104" height="48" rx="7" fill="var(--fdf-fill)" stroke="var(--fdf-acc)"/>
  <text x="314" y="220" font-size="12" fill="var(--fdf-fg)" text-anchor="middle">强</text>
  <rect x="374" y="196" width="104" height="48" rx="7" fill="none" stroke="var(--fdf-line)" stroke-dasharray="4 3"/>
  <text x="426" y="220" font-size="12" fill="var(--fdf-dim)" text-anchor="middle">缺</text>
  <rect x="486" y="196" width="104" height="48" rx="7" fill="none" stroke="var(--fdf-warn)" stroke-dasharray="5 3"/>
  <text x="538" y="220" font-size="12" fill="var(--fdf-fg)" text-anchor="middle">视组织</text>
  <rect x="598" y="196" width="104" height="48" rx="7" fill="none" stroke="var(--fdf-warn)" stroke-dasharray="5 3"/>
  <text x="650" y="220" font-size="12" fill="var(--fdf-fg)" text-anchor="middle">领域级</text>
  <text x="16" y="269" font-size="13" font-weight="600" fill="var(--fdf-fg)">D Agent 应用开发</text>
  <text x="16" y="287" font-size="11.5" fill="var(--fdf-dim)">多问题串成一套交付</text>
  <rect x="150" y="252" width="104" height="48" rx="7" fill="var(--fdf-fill)" stroke="var(--fdf-acc)"/>
  <text x="202" y="276" font-size="12" fill="var(--fdf-fg)" text-anchor="middle">强</text>
  <rect x="262" y="252" width="104" height="48" rx="7" fill="var(--fdf-fill)" stroke="var(--fdf-acc)"/>
  <text x="314" y="276" font-size="12" fill="var(--fdf-fg)" text-anchor="middle">强</text>
  <rect x="374" y="252" width="104" height="48" rx="7" fill="var(--fdf-fill)" stroke="var(--fdf-acc)"/>
  <text x="426" y="276" font-size="12" fill="var(--fdf-fg)" text-anchor="middle">真嵌入</text>
  <rect x="486" y="252" width="104" height="48" rx="7" fill="var(--fdf-fill)" stroke="var(--fdf-acc)"/>
  <text x="538" y="276" font-size="12" fill="var(--fdf-fg)" text-anchor="middle">强</text>
  <rect x="598" y="252" width="104" height="48" rx="7" fill="var(--fdf-fill)" stroke="var(--fdf-acc)"/>
  <text x="650" y="276" font-size="12" fill="var(--fdf-fg)" text-anchor="middle">个人级</text>
  <rect x="16" y="316" width="16" height="12" rx="3" fill="var(--fdf-fill)" stroke="var(--fdf-acc)"/>
  <text x="38" y="322" font-size="11.5" fill="var(--fdf-dim)">命中</text>
  <rect x="90" y="316" width="16" height="12" rx="3" fill="none" stroke="var(--fdf-warn)" stroke-dasharray="5 3"/>
  <text x="112" y="322" font-size="11.5" fill="var(--fdf-dim)">打折</text>
  <rect x="164" y="316" width="16" height="12" rx="3" fill="none" stroke="var(--fdf-line)" stroke-dasharray="4 3"/>
  <text x="186" y="322" font-size="11.5" fill="var(--fdf-dim)">缺口</text>
</svg>
<figcaption>图 1 · B 和 D 的差别不在能力清单上，只在第五项——这一点值得停一下，因为直觉会告诉你两者很像：都做应用、都要封装、都面对使用者。它们的差别不在做的是什么，在东西给谁用。</figcaption>
</figure>

## 三、第三项不是缺，是换了对象

FDE 的现场是**客户的组织**：流程、政治、历史包袱。做生物计算的现场是**物理世界**：培养条件、批次、菌株状态、成像参数。

让这个替换成立的条件，比"都在现场"窄得多：

> 两者都在你座位之外，而且**不能从手上的数据反推出来**。

客户的组织约束推不出来；"这批图为什么长这样"的答案也不在图像里——它在培养箱那边。这才是"现场"和"远程"的分界。

但两个现场的性质是**相反**的，这一点决定了两种职业能沉淀什么：

| | 边界硬度 | 可文档化 | 沉淀成什么 | 换人之后 |
| --- | --- | --- | --- | --- |
| 客户组织（FDE） | 软，可协商 | 难 | 关系、在场感 | 基本归零 |
| 物理世界（生物计算） | 硬，说不通 | 易 | protocol、SOP、文献 | 大部分保留 |

所以生物领域有 protocol 文化而售前侧没有；也所以做生物计算的人更容易被替代。**唯一不可文档化的那一项是判读**——"这批形态不对劲"、"这个富集结果不能这么读"。它既不在 protocol 里，也不在文献里。

## 四、第五项的判据：复用方向，不是产出物形态

<figure class="fdf-fig">
<svg viewBox="0 0 720 300" role="img" aria-label="交付对象的三种复用方向及其回流归宿：不复用没有回流；复用在能力上属横向，回流落在领域；复用在客户上属纵向，回流落在个人">
  <text x="16" y="20" font-size="13" font-weight="600" fill="var(--fdf-fg)">复用方向决定回流落在哪一层</text>
  <text x="16" y="40" font-size="11.5" fill="var(--fdf-dim)">三种方向：不复用、复用在能力上（横向）、复用在客户上（纵向）。</text>
  <rect x="16" y="58" width="214" height="196" rx="10" fill="none" stroke="var(--fdf-line)"/>
  <text x="123" y="82" font-size="13.5" font-weight="600" fill="var(--fdf-fg)" text-anchor="middle">不复用</text>
  <text x="123" y="101" font-size="11.5" fill="var(--fdf-dim)" text-anchor="middle">一客户 · 一能力 · 一次</text>
  <rect x="70" y="118" width="106" height="26" rx="6" fill="none" stroke="var(--fdf-line)" stroke-dasharray="4 3"/>
  <text x="123" y="135" font-size="11.5" fill="var(--fdf-dim)" text-anchor="middle">A 一次性计算</text>
  <text x="123" y="238" font-size="11.5" fill="var(--fdf-dim)" text-anchor="middle">回流：无 → 不可定价</text>
  <rect x="253" y="58" width="214" height="196" rx="10" fill="none" stroke="var(--fdf-line)"/>
  <text x="360" y="82" font-size="13.5" font-weight="600" fill="var(--fdf-fg)" text-anchor="middle">复用在能力上</text>
  <text x="360" y="101" font-size="11.5" fill="var(--fdf-dim)" text-anchor="middle">横向：一能力 · 多客户</text>
  <rect x="295" y="118" width="130" height="26" rx="6" fill="var(--fdf-fill)" stroke="var(--fdf-acc)"/>
  <text x="360" y="135" font-size="11.5" fill="var(--fdf-fg)" text-anchor="middle">B 工具 / 应用开发</text>
  <rect x="312" y="152" width="96" height="26" rx="6" fill="var(--fdf-fill)" stroke="var(--fdf-acc)"/>
  <text x="360" y="169" font-size="11.5" fill="var(--fdf-fg)" text-anchor="middle">C 算法开发</text>
  <text x="360" y="238" font-size="11.5" fill="var(--fdf-dim)" text-anchor="middle">回流：领域级 → 进公共池</text>
  <rect x="490" y="58" width="214" height="196" rx="10" fill="none" stroke="var(--fdf-line)"/>
  <text x="597" y="82" font-size="13.5" font-weight="600" fill="var(--fdf-fg)" text-anchor="middle">复用在客户上</text>
  <text x="597" y="101" font-size="11.5" fill="var(--fdf-dim)" text-anchor="middle">纵向：一客户 · 多能力</text>
  <rect x="526" y="118" width="142" height="26" rx="6" fill="var(--fdf-fill)" stroke="var(--fdf-acc)"/>
  <text x="597" y="135" font-size="11.5" fill="var(--fdf-fg)" text-anchor="middle">D Agent 应用开发</text>
  <rect x="545" y="152" width="104" height="26" rx="6" fill="var(--fdf-fill)" stroke="var(--fdf-acc)"/>
  <text x="597" y="169" font-size="11.5" fill="var(--fdf-fg)" text-anchor="middle">FDE（参照）</text>
  <text x="597" y="238" font-size="11.5" fill="var(--fdf-dim)" text-anchor="middle">回流：个人级 → 记在本人</text>
  <text x="360" y="282" font-size="12" fill="var(--fdf-fg)" text-anchor="middle">判据：不看产出物的形态（库？应用？agent？），看复用方向。</text>
</svg>
<figcaption>图 2 · 同样的"把代码封装成别人能用的程序"，落在横向就是领域级回流，落在纵向就是个人级回流。</figcaption>
</figure>

三种方向，逐个说清。

**不复用。** A 类。一次做完就结束，没有东西留下。

**复用在能力上（横向）。** 做一次、很多用户用。B 类和 C 类在这里。价值确实在积累，但积累发生在**你和使用者之间没有关系**的地方：用户不向你付费，你也拿不到"下一次更便宜"的回报。你能拿到的是声誉、引用、被知道。这些真的会涨——**涨的是领域给你的，不是你下一次交付的成本优势**。

**复用在客户上（纵向）。** 同一个客户的下一个问题，上一个东西直接能用。D 类在这里。价值实现在**你和同一个客户的关系里**：上次省下来的东西，能直接折进下一次的交付时间或报价。

这条判据能解释一个反直觉的现象：B 类看起来最像 FDE——他做应用、他在现场、他闭环——但他的成功被领域记走了。他做的工具越有用、用的人越多，越说明这件事对**领域**有价值，而不是对他下一次交付有价值。

## 五、岗位描述读不出来的那件事

为什么这是个真问题：**岗位描述写不出交付对象的结构。**

它会写职责、写技术栈、写"与谁协作"，但它不会写三件事——上一个交付的东西现在还在跑吗？这个客户的相邻问题谁接？谁在维护？而恰恰是这三件事决定第五项。

结果是，拿着一份岗位描述，判断不了自己做的是横向还是纵向，而这两条路的十年复利曲线完全不同：前者越做越值钱，后者越做越熟练，但在报价上不动。

能补上这个信息的问题只有一句：

> 「这个原型转化完之后，谁维护它，下一个相邻的问题是不是也走这条路？」

回答"有固定的人和流程在接"，那是纵向结构。
回答"看项目，每个都重新立项"，它迟早退化成横向。

## 六、吃老本不是态度问题

四类里，A 类是唯一没有回流的一类。而 A 类有一个稳定行为：**手里有点代码之后就不再往前走**。

这件事常被读成态度问题，但它有机制。

<figure class="fdf-fig">
<svg viewBox="0 0 720 268" role="img" aria-label="资产载体的两种位置：A 类的资产锁在人身上，只能被租用，定价上限是劳动力价格；B 类与 D 类把资产搬进代码里，可以被购买和继承，定价上限是资产价格">
  <rect x="16" y="56" width="334" height="190" rx="10" fill="none" stroke="var(--fdf-warn)"/>
  <text x="183" y="80" font-size="13.5" font-weight="600" fill="var(--fdf-fg)" text-anchor="middle">A 类：资产在人身上</text>
  <rect x="46" y="98" width="274" height="30" rx="6" fill="var(--fdf-fill)" stroke="var(--fdf-line)"/>
  <text x="183" y="113" font-size="11.5" fill="var(--fdf-fg)" text-anchor="middle">一次性代码（只有本人跑得起来）</text>
  <rect x="46" y="136" width="274" height="30" rx="6" fill="var(--fdf-fill)" stroke="var(--fdf-line)"/>
  <text x="183" y="151" font-size="11.5" fill="var(--fdf-fg)" text-anchor="middle">一次性领域知识（只对这个课题成立）</text>
  <text x="183" y="192" font-size="11.5" fill="var(--fdf-warn)" text-anchor="middle">载体是人 → 只能被租用，不能被购买</text>
  <text x="183" y="216" font-size="12.5" font-weight="600" fill="var(--fdf-fg)" text-anchor="middle">定价上限 = 劳动力价格</text>
  <rect x="370" y="56" width="334" height="190" rx="10" fill="none" stroke="var(--fdf-acc)"/>
  <text x="537" y="80" font-size="13.5" font-weight="600" fill="var(--fdf-fg)" text-anchor="middle">B / D 类：资产在代码里</text>
  <rect x="400" y="98" width="274" height="30" rx="6" fill="var(--fdf-fill)" stroke="var(--fdf-line)"/>
  <text x="537" y="113" font-size="11.5" fill="var(--fdf-fg)" text-anchor="middle">可复用的流水线（别人也跑得起来）</text>
  <rect x="400" y="136" width="274" height="30" rx="6" fill="var(--fdf-fill)" stroke="var(--fdf-line)"/>
  <text x="537" y="151" font-size="11.5" fill="var(--fdf-fg)" text-anchor="middle">工具 / agent（换课题仍然能用）</text>
  <text x="537" y="192" font-size="11.5" fill="var(--fdf-acc)" text-anchor="middle">载体是代码 → 可被购买、可被继承</text>
  <text x="537" y="216" font-size="12.5" font-weight="600" fill="var(--fdf-fg)" text-anchor="middle">定价上限 = 资产价格</text>
</svg>
<figcaption>图 3 · 两栏里的东西其实一样，都是"解决过的问题留下的痕迹"。差别只在痕迹附着在哪里——附着在人身上就只能被租用，附着在代码里才能被交易。</figcaption>
</figure>

A 类的资产是**双重不可迁移**的：一次性的代码不可迁移，一次性的领域知识也不可迁移。关键在于，这种情况下资产的实际载体**是人，不是代码**。而人只能被租用，不能被购买。所以 A 类的定价上限是**劳动力的价格**，不是资产的价格。

B 类和 D 类做的事，本质上是**把资产从人身上搬进代码里**。一旦搬进去，它就能被购买、被继承、被定价。这是 B 类比 A 类值钱的结构性原因——跟能力高低无关，跟努力程度也无关。

而这件事难在：**让产出可复用是一份没人付钱的活。** 写文档、抽参数、做测试、跨平台，全都不计入论文的贡献，也不在交付的验收清单里。所以"不复用"不是懒惰，是一个**还没有被打断的稳态**。要打断它，需要改变的是这份活的价签，不是人的觉悟。

## 七、Agent 这一类为什么特殊

D 类和前三类有一个结构性区别：**D 类的交付物本身，就是对 A 类工作的自动化封装。**

把一次性分析变成可复用资产，过去贵在几个地方：工作流要抽象成步骤、参数要外提、边界条件要写清楚、出错要能让使用者自己诊断。这几件都是"没人付钱"的活。而 Agent 恰好作用在这几件上——它让"描述一个工作流并把它固化下来"的边际成本第一次降到可以顺手完成。

所以 D 类是四类里唯一能**结构性打断 A 类稳态**的角色：A 类的工作，正是它的自动化对象。这不是"让分析更快"，而是"让回流第一次变便宜"。快不改变分配，回流才改变分配。

但有一个限制必须说清：**D 类的纵向复用，是被客户结构托着的。**

横向复用的前提是"有很多用户"，纵向复用的前提是"同一个客户有很多问题"。客户一变多、问题一变散，纵向复用就断了，D 类会立刻退化成 B 类——回流从个人层退回领域层。

所以判断一个 Agent 应用岗的 FDE 含量，不看公司规模、不看名头，看它给你绑的是**一个问题集**，还是**一堆散活**。前者是纵向结构，后者不是。

## 八、回到那个场景

回到开头那四个问题。

第二个、第三个问题的成本低于第一个——不是因为第二个问题更简单，而是因为**上一个的东西还在**。成像流程、标注工具、评估脚本、报告的版式，都直接接得上。这就是纵向复用正在发生。

所以那四个问题，在第四节那条判据下落在纵向一侧。那个人的岗位叫什么名字都不重要，重要的是：**四类人里，他站在 D 那一侧。**

最后收一句。[10-10 那篇](/2026/10/10/2026-10-10-01-what-is-fde-five-components-and-nine-stages/)的结论是：FDE 值钱的地方不在能力清单，在回路的闭合方式。这篇补的是更具体的一句：

> **能力清单可以抄，复用方向抄不了**——因为它不由你的技能决定，由你和交付对象的关系决定。
