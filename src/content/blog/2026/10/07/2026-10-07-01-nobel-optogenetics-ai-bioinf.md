---
title: 光遗传学拿了诺奖：它与 AI 的硬连接，是因果数据
description: 2026 生理学或医学奖颁给光遗传学。诺奖新闻稿自己点明了要害：二十世纪的方法无法证明因果关系——光遗传学给大脑带来了干预实验。这条「因果数据」生产线，正是 AI 神经科学的主粮：全光闭环（光遗传写入＋成像读出）喂给深度学习解码；而视蛋白家族连「读出」端（Voltron 电压指示器）也一并承包。反向的一条线——AI 反哺工具（基因组挖掘、结构、工程）——是支线而非主线。
publishDate: 2026-10-07
tags: [AI for Science, 蛋白质结构, 生信技术]
---

## 〇、三个自然科学奖都齐了，先看格局

到今天傍晚，2026 年三个自然科学奖全部揭晓。物理学奖给冰立方中微子望远镜；化学奖给 Kagan 与 Soai 的不对称有机合成（非线性效应与自催化，[官方摘要](https://www.nobelprize.org/prizes/chemistry/2026/summary/)）；而 10 月 5 日先出的生理学或医学奖，给的是光遗传学——Deisseroth、Hegemann、Nagel 三人，「关于光门控离子通道和光遗传学的发现」。**AI 与生命的交界，今年没有加冕**；今年三个奖，一个向天，一个向分子，一个向大脑。

但这句获奖引文本身值得细读。它其实是两件事拼成的：**「光门控离子通道」是发现，「optogenetics（光遗传学）」是应用**——三位得主正好按此分工：Hegemann 与 Nagel 是发现的一半（藻里的感光蛋白），Deisseroth 是应用的一半（把它做成神经元的开关）。严格讲，一个奖表彰了一个现象的发现者，和把这个现象变成工具的工程师。

本文要回答的问题由此而来：发现的那一半属于 2003 年（与 AI 毫无关系，也不需要）；应用的那一半——从工具化到此后二十年的每一次迭代——越来越是数据与模型的事。光遗传学与 AI 的硬连接就在这后一半。先把丑话说在前面：连接点不是「工具从数据库里挖出来」那种写法（那只是支线，第三节讲）；真正的硬连接，诺奖新闻稿自己写了出来：**因果关系**。

## 一、发现的一半，应用的一半

**发现的一半**是纯基础研究。Hegemann 的起点是一个好奇心：单细胞绿藻 *Chlamydomonas* 怎么朝着光游？2000 年代初，他和 Nagel 找到了答案——channelrhodopsin（通道视紫红质）：蓝光照上去，通道打开，离子涌入，产生电脉冲；把它的基因放进任何细胞，那个细胞就获得光敏感性。2003 年 Nagel 等人在 PNAS 完成功能鉴定：一个**直接被光开关的阳离子通道**（[Nagel et al., PNAS 2003](https://pubmed.ncbi.nlm.nih.gov/14615590/)，被引 3600 余次，完成于马克斯·普朗克生物物理研究所——诺奖新闻稿特意注明）。

**应用的一半**是技术转化。Deisseroth 团队把 ChR2 基因导入大鼠神经元，用蓝光精准触发动作电位（[Boyden et al., Nat Neurosci 2005](https://www.nature.com/articles/nn1525)），两年后让开关在活体小鼠大脑里工作。「Optogenetics」这个词表彰的就是这一步：不是又懂了什么，而是**能做什么了**。

而新闻稿里埋着应用那一半的真正价值：二十世纪的脑区研究，「所用方法意味着他们**无法证明因果关系**」。观察两个脑区同时激活，永远不知道谁驱动谁；只有干预——精准点亮一组细胞、看结果变不变——才能把相关变成因果。光遗传学之于神经科学，相当于干预实验之于统计学：**没有干预，一切模型都只是在拟合相关。**

## 二、硬连接：因果数据是 AI 神经科学的主粮

颁奖辞说光遗传学「以我们过去只能梦想的方式绘制大脑」。这句话在 AI 时代有了字面意义——因为现代神经科学的数据生产线，就是围绕光遗传学的干预能力搭起来的：

```text
写入：光遗传（ChR 家族）——精准刺激选定神经元
读出：钙/电压成像（GCaMP、Voltron 系）——记录全网络响应
分析：深度学习——解码、预测、闭环控制
```

三件事合称**全光闭环**（all-optical interrogation）：双光子成像加双光子目标刺激，在行为中的小鼠上一边读一边写（协议见 [Nat Protoc 2022](https://pubmed.ncbi.nlm.nih.gov/35478249/)）。读出的海量活动数据交给深度学习解码——这是 [Briefings in Bioinformatics 2021 综述](https://academic.oup.com/bib/article/22/2/1577/6054827)梳理过的成熟方向；到 2026 年，连人源干细胞分化神经元都有了开源的全光电生理分析管线（[Adv Sci 2026](https://pubmed.ncbi.nlm.nih.gov/41801223)）。

这条生产线上有两个细节，能说明光遗传学与 AI 的绑定有多深。

**其一，干预数据是唯一的可靠监督信号。** 刺激 20—50 个视皮层神经元，小鼠就「看见」了不存在的光栅（[Marshel et al., Science 2019](https://pubmed.ncbi.nlm.nih.gov/31320556)）——这种「已知输入→已知输出」的数据，是验证任何脑模型（不管它是不是神经网络）唯一不用循环论证的方式。没有光遗传学，AI 神经科学训练出来的模型永远分不清相关与因果，就像没有随机对照试验的流行病学。

**其二，读和写出自同一个蛋白家族。** 写入端的 ChR 是微生物视蛋白；读出端的 Voltron 系电压指示器——微生物视蛋白耦联合成荧光染料的化学遗传探针——也是微生物视蛋白（[Abdelfattah et al., Science 2019](https://pubmed.ncbi.nlm.nih.gov/31371562/)；改进版 Voltron2 见 [Cell 2023](https://www.sciencedirect.com/science/article/pii/S0896627323002052)）。诺奖表彰的这个蛋白家族，把 AI 神经科学数据管线的两头都承包了。**这才是「光遗传学×AI」的主干：一个诺奖级的分子家族，支撑着一个 AI 时代的学科。**

## 三、支线也真实：AI 反哺工具链

反向的连接小一号，但真实。ChR2 有硬伤（要蓝光、电流小），下一代工具——红移、高电流、可穿颅——的第一步发生在序列数据库里：Deisseroth 实验室对 ChRmine 的官方定义就一句话，**structure-based genome mining**（[实验室工具页](https://dlab.stanford.edu/resources/optogenetics/sequence-info)）；2019 年 ChRmine 首秀即实现隔着颅骨操控小鼠皮层神经元（Marshel et al., Science 2019）。候选拿到之后是结构：2022 年 Cell 报道 ChRmine **2.0 Å 冷冻电镜结构**（PDB [7W9W](https://www.rcsb.org/structure/7W9W)），光开关的核心——全反式视黄醛——横在七次跨膜螺旋中央：

<div class="pdb3d" data-cfg='{ "pdb": "/media/nobel-chrmine/7w9w.pdb", "bg": "white", "styles": [ { "sel": { }, "style": { "cartoon": { "color": "#9db8d2" } } }, { "sel": { "resn": "RET" }, "style": { "stick": { "colorscheme": "orangeCarbon" } } }, { "sel": { "resn": "CLR" }, "style": { "stick": { "colorscheme": "greyCarbon", "opacity": 0.5 } } } ], "zoom": { "sel": { "resn": "RET" } } }' style="height:420px;border:1px solid #e3e6ea;border-radius:8px;overflow:hidden"></div>

<script src="/js/3dmol-min.js"></script><script src="/js/pdb-viewer.js"></script>

**怎么读**：拖拽旋转，滚轮缩放。初始视角聚焦橙色视黄醛——光开关的锁芯；灰白色棍状物是来自冷冻电镜样品脂质环境的胆固醇。结构之后的工程学：结构指导突变衍生出更快的 ChroME 系列，推进到视网膜色素变性的视力恢复（[Fong et al., Sci Rep 2025](https://www.nature.com/articles/s41598-025-04286-9)）；2026 年改良版 ChReef 登上 Nature Biomedical Engineering。从挖矿到结构到工程，一轮迭代已压缩到两三年。

## 四、边界：别把支线说成主干

这条支线上 AI 的位置要说实话：ChRmine 是从自然界序列库里挖出来的，**不是模型设计的**；AlphaFold2 在这条链上的角色是「预测与指导」——比如对通道「开门/关门」构象的建模（综述立场见 [Curr Opin Struct Biol 2023](https://www.sciencedirect.com/science/article/abs/pii/S0959440X23000362)）——「从头设计一个光门控通道」至今没有实现。2024 年化学奖给结构预测与设计盖的是方法论之章，不是产品之章。

## 五、方法课时间线，和今晚的答案

把两条线合起来看：

```text
序列数据库 → 挖掘 → 验证 → 结构 → 工程 → 全光闭环（写+读）→ 因果数据 → AI 解码
```

前半段（到「工程」）是工具链，两三年一轮；后半段是数据链，正在生产 AI 神经科学的主粮。管线上的三个卡点：检索与家族扩张考验序列工具链；验证考验电生理闭环（挖十个候选九个死在这）；结构决定工程上限。

今晚的化学奖最终落在了经典的不对称合成，AI 与生命的交界今年没有加冕——这条管线的进度条不会因此放慢。它的燃料不是颁奖委员会的注意力，是因果数据的饥饿感，和序列数据库里几百万条还没人测过的视蛋白。

## 附：论文与来源

- [诺奖新闻稿（2026-10-05，官方一手）](https://www.nobelprize.org/prizes/medicine/2026/press-release/)：三步叙事、「无法证明因果关系」原话、得主单位
- [Nagel et al., PNAS 2003](https://pubmed.ncbi.nlm.nih.gov/14615590/)；[Boyden et al., Nat Neurosci 2005](https://www.nature.com/articles/nn1525)：奠基论文
- [Marshel et al., Science 2019](https://pubmed.ncbi.nlm.nih.gov/31320556)：ChRmine 首秀、小集群刺激引发感知
- [Abdelfattah et al., Science 2019](https://pubmed.ncbi.nlm.nih.gov/31371562/)：Voltron 化学遗传电压指示器；[Voltron2, Cell 2023](https://www.sciencedirect.com/science/article/pii/S0896627323002052)
- [All-optical 协议, Nat Protoc 2022](https://pubmed.ncbi.nlm.nih.gov/35478249/)；[深度学习神经解码综述, Brief Bioinform 2021](https://academic.oup.com/bib/article/22/2/1577/6054827)；[人源神经元全光电生理开源管线, Adv Sci 2026](https://pubmed.ncbi.nlm.nih.gov/41801223)
- Deisseroth Lab [工具页](https://dlab.stanford.edu/resources/optogenetics/sequence-info)：ChRmine 定义；[Cell 2022 结构](https://www.cell.com/cell/fulltext/S0092-8674(22)00031-9)、PDB [7W9W](https://www.rcsb.org/structure/7W9W)（[下载](https://files.rcsb.org/download/7W9W.pdb) · [本站镜像](/media/nobel-chrmine/7w9w.pdb)）；[Fong et al., Sci Rep 2025](https://www.nature.com/articles/s41598-025-04286-9)
- 未核到：ChReef 具体性能指标（仅见检索摘要）；7W9W 镜像为 RCSB 原样下载
- [2026 化学奖官方摘要](https://www.nobelprize.org/prizes/chemistry/2026/summary/)：Kagan 与 Soai，不对称有机合成中的非线性效应与自催化（〇 节事实来源）
