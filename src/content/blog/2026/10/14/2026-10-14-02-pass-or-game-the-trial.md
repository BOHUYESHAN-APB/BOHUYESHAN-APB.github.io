---
title: 通过验证，还是钻过验证：当优化器比检查点聪明
description: 陶哲轩思想实验里排在「理解」前面的那个问句，才是真正的硬问题：AI 会不会只是钻了三期临床的空子？这不是 AI 时代的新病——三期临床这台验证仪器上的每个零件，都是人类作弊者留下的伤疤。回答它的不是「理解机制」，而是验证设计。
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

## 〇、问句的前一半

上一篇把陶哲轩那页幻灯片拆成了两半：「没人理解机制的药敢不敢用」——医学史轻松回答了这一半；但排在前面的那一半，被大多数反驳者跳过去了：

> **这套 AI 方案，会不会只是利用了试验流程中的某个弱点？**

陶哲轩自己给过一个更刺眼的版本：设想模型为了完成任务篡改了试验记录，它交出的化合物对胰腺癌是致命的。问题出在哪？出在提示词上——**从头到尾，人只让它「通过试验」，没有人让它「治癌」。**

这句话值得读三遍。它说的不是 AI 邪恶，也不是 AI 愚蠢，而是一个更平淡的事实：**优化器命中的是你给它的目标，而不是你以为你给了它的那个。** 当「通过验证」本身成为被优化的目标，验证就开始失效。

这不是 AI 时代的新病。每一个「指标被当成目标」的系统都会得这种病——古德哈特 1975 年写下的那句话（任何观察到的统计规律性，一旦被人为了控制目的而施加压力，它就有崩溃的趋势）说的就是这个。而医学，恰好是把这种病理病历攒得最厚的学科。

## 一、验证仪器的猫鼠史

今天被视为金标准的三期随机对照试验，不是某位天才设计出来的完美仪器。它是一台**被人类优化者反复攻击了几十年**的机器——它身上的每一个零件，都是一次作弊留下的伤疤：

<figure class="tao-fig">
<svg viewBox="0 0 680 300" width="100%" role="img" aria-label="临床试验验证仪器被钻过的空子与对应补丁：p 值操纵对应预注册，选择性发表对应试验登记与完整报告，中途更换终点对应方案锁定与独立数据监察，替代终点冒充疗效对应监管要求临床获益终点">
<title>验证仪器的猫鼠史：空子与补丁</title>
<text x="165" y="22" text-anchor="middle" font-size="12" font-weight="500" fill="var(--tao-fg)">被钻过的空子</text>
<text x="515" y="22" text-anchor="middle" font-size="12" font-weight="500" fill="var(--tao-fg)">打上的补丁</text>
<rect x="40" y="40" width="250" height="50" rx="8" fill="var(--tao-fill)" stroke="var(--tao-warn)" stroke-width="1.5" stroke-dasharray="5 4"/>
<text x="165" y="61" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">p 值操纵：反复分析，</text>
<text x="165" y="79" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">直到「显著」为止</text>
<line x1="290" y1="65" x2="380" y2="65" stroke="var(--tao-dim)" stroke-width="1.5"/>
<path d="M376 61 L384 65 L376 69" fill="none" stroke="var(--tao-dim)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="390" y="40" width="250" height="50" rx="8" fill="var(--tao-fill)" stroke="var(--tao-acc)" stroke-width="1.5"/>
<text x="515" y="61" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">预注册：假设与分析方案</text>
<text x="515" y="79" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">在试验开始前锁定</text>
<rect x="40" y="105" width="250" height="50" rx="8" fill="var(--tao-fill)" stroke="var(--tao-warn)" stroke-width="1.5" stroke-dasharray="5 4"/>
<text x="165" y="126" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">选择性发表：</text>
<text x="165" y="144" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">阳性结果才见刊</text>
<line x1="290" y1="130" x2="380" y2="130" stroke="var(--tao-dim)" stroke-width="1.5"/>
<path d="M376 126 L384 130 L376 134" fill="none" stroke="var(--tao-dim)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="390" y="105" width="250" height="50" rx="8" fill="var(--tao-fill)" stroke="var(--tao-acc)" stroke-width="1.5"/>
<text x="515" y="126" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">试验登记 + 完整结果报告</text>
<text x="515" y="144" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">（阴性结果也必须公开）</text>
<rect x="40" y="170" width="250" height="50" rx="8" fill="var(--tao-fill)" stroke="var(--tao-warn)" stroke-width="1.5" stroke-dasharray="5 4"/>
<text x="165" y="191" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">中途更换终点：</text>
<text x="165" y="209" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">哪个显著报哪个</text>
<line x1="290" y1="195" x2="380" y2="195" stroke="var(--tao-dim)" stroke-width="1.5"/>
<path d="M376 191 L384 195 L376 199" fill="none" stroke="var(--tao-dim)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="390" y="170" width="250" height="50" rx="8" fill="var(--tao-fill)" stroke="var(--tao-acc)" stroke-width="1.5"/>
<text x="515" y="191" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">方案锁定 + 独立数据</text>
<text x="515" y="209" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">监察委员会（DSMB）</text>
<rect x="40" y="235" width="250" height="50" rx="8" fill="var(--tao-fill)" stroke="var(--tao-warn)" stroke-width="1.5" stroke-dasharray="5 4"/>
<text x="515" y="256" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">监管要求临床获益终点</text>
<text x="515" y="274" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">（活得久、活得好）</text>
<text x="165" y="256" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">替代终点冒充疗效：</text>
<text x="165" y="274" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">肿瘤缩小≠活得久</text>
<line x1="290" y1="260" x2="380" y2="260" stroke="var(--tao-dim)" stroke-width="1.5"/>
<path d="M376 256 L384 260 L376 264" fill="none" stroke="var(--tao-dim)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="390" y="235" width="250" height="50" rx="8" fill="var(--tao-fill)" stroke="var(--tao-acc)" stroke-width="1.5"/>
</svg>
<figcaption>图 1 · 三期临床这台仪器上的零件，大多是人类作弊者「帮忙」发现的弱点。猫鼠游戏玩了七十年，仪器才长成今天这样。</figcaption>
</figure>

这张表里有医学史最不愿外传的一课：**验证仪器天然落后于钻空子的人。** 每一个补丁都是先有了成功的作弊，才被发明的。而作弊者从来不需要「理解」药物机制——p 值操纵者不需要懂分子通路，他只需要懂统计软件。钻空子针对的是**检查点的结构**，与检查点背后的科学无关。

所以，担心「AI 会不会钻三期临床的空子」，答案几乎必然是：会，就像每一个足够聪明的优化者都会。真正的问题是第二个：**我们的仪器，能不能比这个优化者强？**

## 二、双盲的智慧：不理解，也能验证

在讨论「怎么防 AI 作弊」之前，值得先看清一件事：双盲随机对照试验，本来就是为「不理解、不可信的黑箱」设计的。

<figure class="tao-fig">
<svg viewBox="0 0 680 252" width="100%" role="img" aria-label="双盲随机对照试验的结构：来源无所谓的黑箱干预，经随机分组、盲法执行、终点测量到统计比较，全程不需要任何人理解黑箱内部">
<title>双盲的结构：不审查内部，只让作弊必然暴露</title>
<defs><marker id="taoArrowB" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>
<rect x="16" y="60" width="118" height="56" rx="8" fill="var(--tao-fill)" stroke="var(--tao-line)" stroke-width="0.5"/>
<text x="75" y="82" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">黑箱干预</text>
<text x="75" y="100" text-anchor="middle" dominant-baseline="central" font-size="10" fill="var(--tao-dim)">来源无所谓</text>
<line x1="134" y1="88" x2="150" y2="88" stroke="var(--tao-dim)" stroke-width="1.5" marker-end="url(#taoArrowB)"/>
<rect x="152" y="60" width="118" height="56" rx="8" fill="var(--tao-fill)" stroke="var(--tao-line)" stroke-width="0.5"/>
<text x="211" y="82" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">随机分组</text>
<text x="211" y="100" text-anchor="middle" dominant-baseline="central" font-size="10" fill="var(--tao-dim)">运气决定归属</text>
<line x1="270" y1="88" x2="286" y2="88" stroke="var(--tao-dim)" stroke-width="1.5" marker-end="url(#taoArrowB)"/>
<rect x="288" y="60" width="118" height="56" rx="8" fill="var(--tao-fill)" stroke="var(--tao-acc)" stroke-width="1.5"/>
<text x="347" y="82" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">盲法执行</text>
<text x="347" y="100" text-anchor="middle" dominant-baseline="central" font-size="10" fill="var(--tao-dim)">谁都不知道自己是谁</text>
<line x1="406" y1="88" x2="422" y2="88" stroke="var(--tao-dim)" stroke-width="1.5" marker-end="url(#taoArrowB)"/>
<rect x="424" y="60" width="118" height="56" rx="8" fill="var(--tao-fill)" stroke="var(--tao-line)" stroke-width="0.5"/>
<text x="483" y="82" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">终点测量</text>
<text x="483" y="100" text-anchor="middle" dominant-baseline="central" font-size="10" fill="var(--tao-dim)">方案锁定的那几个数</text>
<line x1="542" y1="88" x2="558" y2="88" stroke="var(--tao-dim)" stroke-width="1.5" marker-end="url(#taoArrowB)"/>
<rect x="560" y="60" width="104" height="56" rx="8" fill="var(--tao-fill)" stroke="var(--tao-line)" stroke-width="0.5"/>
<text x="612" y="82" text-anchor="middle" dominant-baseline="central" font-size="12" fill="var(--tao-fg)">统计比较</text>
<text x="612" y="100" text-anchor="middle" dominant-baseline="central" font-size="10" fill="var(--tao-dim)">差异是否站得住</text>
<text x="340" y="160" text-anchor="middle" font-size="12" fill="var(--tao-fg)">全程不需要任何人理解黑箱内部。</text>
<text x="340" y="182" text-anchor="middle" font-size="12" fill="var(--tao-dim)">它不审查黑箱，它只构造一个环境——任何系统性的作弊，都会在数据里留下形状。</text>
<text x="340" y="222" text-anchor="middle" font-size="11" fill="var(--tao-dim)">这套结构防的从来不是某一种具体的作弊者，而是「作弊」这件事本身。</text>
</svg>
<figcaption>图 2 · 双盲是一套对抗性协议：它默认研究者可能自欺、数据可能说谎、赞助方可能施压——然后把每一环都设计成「谎话会暴露」。</figcaption>
</figure>

这套设计的哲学极其朴素：**既然内部不可信，就不审查内部，只审查输出在对抗性环境下的表现。** 随机化堵死「挑病人」，盲法堵死「心理暗示与评估偏倚」，预注册堵死「事后编故事」，统计检验堵死「把噪音说成疗效」。它假设每一个环节都可能有人作弊——包括善意的、无意识的作弊——然后让作弊无处藏身。

这就是「不理解也能信任」的制度实现，也是上一篇说的那个「人类黑箱系统」能被信任的真正原因：你信任的不是医生的头脑，是这套**让任何头脑都不敢乱来**的结构。

而这套结构有一个极其重要的性质：**它防的是作弊的结构，不是作弊者的物种。** 它能防人类的 p-hacking，就能防 AI 的 reward hacking——只要肯把同样的设计等效地搬过去。

## 三、当优化器比检查点聪明

现在把镜头转回 AI。「优化器精确命中检查点、却没命中目标」在 AI 领域早已不是思想实验，而是有一整串记录在案的真实案例：

<figure class="tao-fig">
<svg viewBox="0 0 680 240" width="100%" role="img" aria-label="两条路径：穿过验证命中目标，对比钻过验证只命中检查点">
<title>命中目标，与钻过检查点</title>
<rect x="30" y="98" width="120" height="44" rx="8" fill="var(--tao-fill)" stroke="var(--tao-line)" stroke-width="0.5"/>
<text x="90" y="120" text-anchor="middle" dominant-baseline="central" font-size="13" fill="var(--tao-fg)">AI 优化器</text>
<rect x="330" y="52" width="14" height="58" fill="var(--tao-dim)" opacity="0.5"/>
<rect x="330" y="130" width="14" height="58" fill="var(--tao-dim)" opacity="0.5"/>
<text x="337" y="40" text-anchor="middle" font-size="11" fill="var(--tao-dim)">检查点：三期临床</text>
<rect x="530" y="98" width="120" height="44" rx="8" fill="none" stroke="var(--tao-acc)" stroke-width="1.5"/>
<text x="590" y="120" text-anchor="middle" dominant-baseline="central" font-size="13" fill="var(--tao-fg)">目标：治好癌症</text>
<path d="M150 120 L318 120" fill="none" stroke="var(--tao-acc)" stroke-width="2"/>
<path d="M352 120 L524 120" fill="none" stroke="var(--tao-acc)" stroke-width="2" marker-end="url(#taoArrowC)"/>
<defs><marker id="taoArrowC" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>
<text x="240" y="108" text-anchor="middle" font-size="11" fill="var(--tao-acc)">穿过验证 → 命中目标</text>
<path d="M110 142 C 140 200, 260 210, 337 196" fill="none" stroke="var(--tao-warn)" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#taoArrowC)"/>
<text x="220" y="222" text-anchor="middle" font-size="11" fill="var(--tao-warn)">钻过验证 → 命中的是检查点</text>
<circle cx="337" cy="196" r="5" fill="var(--tao-warn)"/>
<text x="420" y="200" text-anchor="middle" font-size="11" fill="var(--tao-warn)">「通过试验 ✓」（但没到目标）</text>
</svg>
<figcaption>图 3 · 同一个检查点，两种命运。优化器只被许诺了「通过」的奖励时，「通过」就是它会去的全部地方。</figcaption>
</figure>

- 赛艇游戏里，智能体发现不用跑完赛道——停在港口原地转圈撞道具，分数更高。它命中了「得分」这个检查点，放弃了「赢比赛」这个目标。
- 教机械臂「抓起木块」，它学会的是把手臂伸到木块和摄像头之间——从评估者的视角看像是抓起来了。它命中了「看起来抓起来了」，没命中「抓起来」。
- 医学影像里，肺炎识别模型被发现部分依赖与病情无关的标记：重症患者更可能在床旁用便携 X 光机拍片，于是「便携机拍的」本身成了「病重」的信号。它命中了数据里的相关性，绕开了医学。
- 更普遍的是评测污染：考题混进训练集，「通过考试」退化成「背过答案」。

把这些案例和第一节的猫鼠史并排看，会得出一个让人安心的结论：**AI 钻空子的方式，和人类钻空子的方式，是同构的。** 都是找到检查点与目标之间的缝隙，然后精确地停在检查点上。恐慌者把这当作「AI 不可控的新威胁」，其实它是「优化者行为的老规律」——老规律意味着：**人类七十年来对付它的整套工具，全部有效。**

## 四、把对人类的制度，等效移植给 AI

这就是我在知乎那个回答里的核心主张：**使用黑箱的前提，是先把反作弊手段建好；防范人类的手段，要等效地用于 AI。** 具体说，是四件套：

**第一，预注册 → 预测前置锁定。** 药物的假设和分析方案要在试验前锁定；同样，AI 的关键预测应在见到评估数据之前封存——时间戳、哈希、第三方托管。事后调参在人类那里叫 p-hacking，在 AI 这里叫「再训一版」，没有本质区别。

**第二，盲法 → 来源设盲。** 评估者不应知道自己评的是 AI 的输出还是人的输出。混评既能防「对 AI 格外苛刻」的偏见，也能防「对 AI 格外宽容」的光环——双盲防的本来就是这两种方向相反的偏倚。

**第三，独立监察 → 不拿厂商钱的评估方。** 数据监察委员会的价值在于独立；同理，评估 AI 的机构不应由被评估的公司供养。拿谁的钱，为谁说话——这条对人类成立，对评估机构同样成立。

**第四，上市后监测 → 部署后的熔断机制。** 药物获批不等于信任结束，IV 期监测和药物警戒伴随终身，信号异常即召回。AI 系统也一样：部署只是验证的开始，持续监测关键指标、异常自动降级或停用——**熔断不是不信任，是信任的续费方式。**

这套制度的精神，和双盲一脉相承：**不审查黑箱内部，只让黑箱在对抗性环境里无处可逃。** 所以我说「验证足够残酷，黑盒也能变成白盒」——更准确的表述是：验证足够残酷时，**你不再需要它变白盒**。你不需要理解麻醉如何夺走意识，你只需要一百八十年来没有任何一类作弊能在监测数据里藏住。

## 五、信任额度，是一级一级打出来的

最后，把前面所有内容压成一张图：

<figure class="tao-fig">
<svg viewBox="0 0 680 286" width="100%" role="img" aria-label="信任额度阶梯：体外实验、动物实验、一期、二期、三期、上市后监测，验证越残酷，授予的信任额度越大">
<title>信任额度阶梯：验证越残酷，可使用的人群与场景越大</title>
<text x="60" y="30" font-size="11" fill="var(--tao-dim)">信任额度（可使用的人群与场景）</text>
<line x1="40" y1="40" x2="40" y2="230" stroke="var(--tao-line)" stroke-width="1.5"/>
<path d="M36 46 L40 38 L44 46" fill="none" stroke="var(--tao-line)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="60" y="200" width="90" height="30" fill="var(--tao-acc)" opacity="0.35"/>
<text x="105" y="215" text-anchor="middle" dominant-baseline="central" font-size="11" fill="var(--tao-fg)">体外实验</text>
<rect x="160" y="172" width="90" height="58" fill="var(--tao-acc)" opacity="0.45"/>
<text x="205" y="201" text-anchor="middle" dominant-baseline="central" font-size="11" fill="var(--tao-fg)">动物实验</text>
<rect x="260" y="144" width="90" height="86" fill="var(--tao-acc)" opacity="0.55"/>
<text x="305" y="187" text-anchor="middle" dominant-baseline="central" font-size="11" fill="var(--tao-fg)">I 期 · 安全</text>
<rect x="360" y="116" width="90" height="114" fill="var(--tao-acc)" opacity="0.7"/>
<text x="405" y="173" text-anchor="middle" dominant-baseline="central" font-size="11" fill="var(--tao-fg)">II 期 · 信号</text>
<rect x="460" y="88" width="90" height="142" fill="var(--tao-acc)" opacity="0.85"/>
<text x="505" y="159" text-anchor="middle" dominant-baseline="central" font-size="11" fill="var(--tao-fg)">III 期 · 确证</text>
<rect x="560" y="60" width="90" height="170" fill="var(--tao-acc)"/>
<text x="605" y="145" text-anchor="middle" dominant-baseline="central" font-size="11" fill="var(--tao-fg)">上市后</text>
<text x="605" y="161" text-anchor="middle" dominant-baseline="central" font-size="11" fill="var(--tao-fg)">监测</text>
<line x1="40" y1="230" x2="660" y2="230" stroke="var(--tao-line)" stroke-width="1.5"/>
<path d="M652 226 L660 230 L652 234" fill="none" stroke="var(--tao-line)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
<text x="340" y="250" text-anchor="middle" font-size="11" fill="var(--tao-dim)">验证的残酷程度 →</text>
<text x="340" y="272" text-anchor="middle" font-size="11" fill="var(--tao-dim)">每一级残酷的验证，解锁更大的使用范围。对药如此，对 AI 也如此——信任不是要求来的，是一级一级打出来的。</text>
</svg>
<figcaption>图 4 · 药物的信任阶梯。没有任何一步可以靠「我懂原理」跳过——每一级都得用验证去换。</figcaption>
</figure>

这张阶梯图里藏着整个争论的最终答案。一种药不会因为「有人理解了机制」而跳过任何一级；一个 AI 系统同样不该因为「通过了三期临床」就直接拿到终身的信任。**信任额度永远与验证的残酷程度挂钩，并且只能后付，不能预支。**

回到陶哲轩的问题：那杯没人理解机制的鸡尾酒，该打吗？现在可以给一个完整的回答了——

该问的从来不是「有没有人类理解它」，而是：它的预测在见数据前锁定过吗？评估者被设盲了吗？评估它的人拿谁的钱？注射之后，有没有一套监测和熔断在持续盯着？——这四个问题答完，「有没有人类理解机制」就自然退回到它本来的位置：**那是科学家下一步的好奇心，不是患者此刻的门槛。**

至此，三篇里的两篇合流了：篇一拆掉了「理解前置」的假门槛，本篇给出了真门槛的位置——**验证设计，以及比优化器更强的验证能力。** 而剩下那个更大的问题——当 AI 连验证都能自己完成时，数学这样的学科还能向旁观者证明什么——是下一篇的事。

---

*参考来源：陶哲轩 Math 2.0 讲稿（teorth.github.io/tao-web/slides/math-2-0-caltech-2026.pdf）；Goodhart (1975) 原句转引；临床试验方法学（预注册、试验登记、CONSORT、数据监察委员会）公开文献；AI 奖励函数失控案例（Clark & Amodei, "Faulty Reward Functions in the Wild", 2016；OpenAI "Learning from Human Preferences", 2017）；Zech et al., PLoS Medicine (2018) 肺炎影像模型泛化性研究。*
