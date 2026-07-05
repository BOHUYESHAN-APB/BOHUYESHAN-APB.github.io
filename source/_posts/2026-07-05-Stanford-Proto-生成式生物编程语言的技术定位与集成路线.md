---
title: "Stanford Proto：生成式生物编程语言的技术定位——它到底是什么，以及怎么融入 AI Agent 工作站"
date: 2026-07-05
tags:
  - Proto
  - AI-Agent
  - 生物信息学
  - MCP
  - 生成式生物学
categories:
  - 技术分析
---

## 一个关键问题：它到底是不是"编程语言"？

2026 年 6 月 22 日，Stanford 大学 Brian Hie 实验室开源了一个项目，叫 **Proto**。论文标题写的是 "A high-level programming language for generative biology"，官网也说 "Proto is a high-level programming language"。

但如果你 `pip install proto-language` 然后写代码，你会发现写的是标准的 Python。

```
pip install git+https://github.com/evo-design/proto-language.git
python your_program.py
```

所以第一个要搞清楚的问题：**它到底是不是一门新的编程语言？**

答案是否定的——严格来说，**Proto 不是一个独立的编程语言，而是一个嵌入在 Python 中的领域特定框架（eDSL）**。它没有发明新语法、没有自己的编译器或解释器。它提供了一套完整的领域词汇（7 个原语）和组合规则，使用者不是在"写 Python"，而是在用这套词汇**声明**一个生物设计问题。

类比一下就清楚了：

| 项目 | 本质上 | 但被称为 |
|------|--------|----------|
| **Proto** | Python 领域特定框架 | "生物编程语言" |
| **SQLAlchemy** | Python ORM 库 | "数据库语言" |
| **TensorFlow** | Python 深度学习库 | "AI 编程框架" |
| **Dockerfile** | 文本配置文件 | "基础设施即代码" |

把 Proto 称为"编程语言"是论文写作中的一种概念定性——强调它**有自己完整的思维模型和词汇体系**，而不是说你需要学一门新语法。就像你学 SQLAlchemy 时需要理解"什么是 ORM、什么是 session、什么是 declarative base"一样，学 Proto 需要理解它的 7 个原语。

## 7 个原语：Proto 的思维模型

Proto 的核心不是语法，而是它定义的问题分解方式：

```
Sequence → Segment → Construct → Generator → Constraint → Optimizer → Program
```

- **Sequence** — 一个带类型的字符串（DNA/RNA/蛋白质），是可设计的基本单元
- **Segment** — 一个设计区域，持有候选序列和结果序列
- **Construct** — 多个 Segment 的有序组合（比如启动子 + 编码区）
- **Generator** — 提出新序列候选（从随机突变到 ESM2/ProteinMPNN）
- **Constraint** — 给序列打分（GC 含量、pLDDT、结合强度…）
- **Optimizer** — 驱动 propose–score–refine 循环的搜索策略
- **Program** — 顶层编排器，组合多个 Optimizer 阶段

关键区别在这：**传统编程是"先做 A，再做 B，再做 C"的线性步骤。Proto 是"声明你要什么条件，声明怎么生成候选，声明怎么搜索，然后组合起来跑"。** 它是**面向对象 + 声明式组合**，不是面向过程。

一个具体的例子——设计一个 80aa 的蛋白质，要求高结构置信度 + 均衡氨基酸组成：

```python
from proto_language.core import Segment, Construct, Constraint, Program
from proto_language.generator import ESM2Generator, ESM2GeneratorConfig
from proto_language.optimizer import MCMCOptimizer, MCMCOptimizerConfig
from proto_language.constraint import (
    structure_plddt_constraint, balanced_aa_constraint,
)
from proto_tools.transforms.masking import MaskingStrategy

protein = Segment(length=80, sequence_type="protein")
construct = Construct(segments=[protein])

gen = ESM2Generator(ESM2GeneratorConfig(
    masking_strategy=MaskingStrategy(num_mutations=3)
))
gen.assign(protein)

constraints = [
    Constraint(inputs=[protein], function=structure_plddt_constraint,
               function_config={"structure_tool": "esmfold"}, weight=2.0),
    Constraint(inputs=[protein], function=balanced_aa_constraint,
               function_config={}, weight=1.0),
]

optimizer = MCMCOptimizer(
    constructs=[construct], generators=[gen], constraints=constraints,
    config=MCMCOptimizerConfig(num_steps=200, num_results=5),
)
Program(optimizers=[optimizer], num_results=5).run()
```

这段代码**没有**说"第一步用 ESMFold 预测结构，第二步算 pLDDT，第三步计算氨基酸组成"。它说的是："我要一个 80aa 的蛋白质，结构置信度高的权重是 2，氨基酸均衡的权重是 1，用 ESM2 加随机突变来生成候选，用 MCMC 来搜。"

这个区别就是 Proto 的核心设计哲学：**声明约束，而不是编写步骤。**

## 编译型还是解释型？面向对象还是面向过程？

- **解释型**（纯 Python 运行时，没有编译步骤）
- **面向对象 + 声明式组合**（不是面向过程）
- 所有组件都通过 `BaseConfig` + `ConfigField` 模式配置，通过 `@constraint`、`@generator`、`@optimizer` 装饰器注册

## AI 友好性：它真正的杀手锏

Proto 最值得注意的设计特征不是它的"语言"属性，而是它**对 AI agent 的友好程度**。我翻过它的仓库后，发现这是目前见过的对 AI 协作设计最彻底的开源项目之一：

| 特性 | 说明 |
|------|------|
| **AGENTS.md / CLAUDE.md / GEMINI.md** | 专门给 Claude、Gemini 等 AI 看的项目指南 |
| **.claude/skills/** | 预制了 write-program、implement-constraint 等 AI coding skill |
| **MCP Server** | proto-client 自带 MCP 接口，AI 通过自然语言直接调用 80+ 生信工具 |
| **代码模式高度一致** | 所有约束/生成器/优化器都走装饰器注册 + BaseConfig 模式 |
| **CONTRIBUTING.md 明确写** | "Coding agents are very helpful for this!" |

这意味着什么？**AI（Claude、GPT 等）已经非常擅长写 Python，不需要学新语法。** Proto 作为一个 Python 框架而不是一门新语言，反而降低了 AI 的使用门槛——AI 可以直接读取文档和现有代码模式，准确生成 Proto 程序。

而 MCP 接口更进一步：AI 甚至不需要写 Python 代码，直接通过自然语言调用 Proto 工具。比如你对 AI 说"用 ESMFold 预测这个序列的结构"，它就能通过 MCP 调用 Proto 的 ESMFold 工具返回结果。

## MIT 许可：为什么这对我们很重要

Proto 采用 MIT 协议，这是最宽松的开源许可证之一。这意味着：

- ✅ 自由使用，商业/科研都行
- ✅ 修改源码，内部二次开发
- ✅ Fork 出来做自己的定制分支
- ✅ 将其生态反向纳入我们的技术栈

对于一个正在构建 AI Agent 科研自动化平台的团队来说，这很关键——我们不只是在"用"Proto，而是在考虑**把它作为技术栈的一层来吸纳**。

## 四层集成路线

基于前面的分析，把 Proto 纳入我们现有的工作站体系，可以分为四个由浅入深的层次：

### 第一层：MCP 工具接入（最快，立即能用）

Proto 官方的 MCP 服务器在 `proto-client` 中，安装后连接 `https://mcp.evodesign.org/mcp`，即可获得 80+ 生信工具的 MCP 接口。我们的 Agent 编排器已经支持 MCP 协议，加入后 Agent 可以直接调用 ESMFold、ProteinMPNN、BLAST 等工具。

需要：注册 Proto Bio 账号获取 API key。

### 第二层：Skill 封装（核心价值）

我们的工作站已有 617 个生信技能。Proto 的 constraint/generator/optimizer 天然可以映射为技能单元：
- 每个 Constraint → 一个技能（"GC 含量分析""结构置信度评估"…）
- 每个 Generator → 一个技能（"ESM2 序列生成""随机突变"…）
- 每个 Program → 一个工作流

这相当于把 Proto 的 120+ 工具变成了我们技能库的扩展，而且不需要重新造轮子。

### 第三层：Fork 定制（中长期）

MIT 协议允许我们 fork proto-language 或 proto-tools，针对特定生信任务做定制化约束，或者连接我们自己的工具链（比如 extendai-lab-Studio 的工作流编排）。

### 第四层：生态反向包容（长期愿景）

不是单向使用，而是双向融合：
- 贡献开源（中文文档、示例程序）
- 贡献新的 constraint/generator（基于我们已有的模型）
- 用 Proto 的 MCP server 模式标准化我们自己的工具暴露

## 对我们的技术路线的价值

回到最实际的问题：这事对我们有什么用？

**技术上**，Proto 的 propose–score–refine 循环天然适配 Agent 的 think–act–observe 循环。我们的 Agent 现在能"想"（规划分析路径），但还不能自动"执行"（运行生信工具）。把 Proto 作为 Agent 的"执行层"，相当于给了 Agent 一双手。

**简历上**，Proto 是 Stanford 2026 年 6 月刚发布的 MIT 开源项目，能将其纳入技术栈，体现的是对前沿生成式生物学工具的跟进能力、AI Agent + Bioinformatics 的交叉定位，以及开源生态的参与感。

**认知上**，搞清楚 Proto "不是一门新编程语言而是一套生物设计思维模型"这个定位，比往简历上写一行"掌握 Proto"重要得多——前者说明你真的理解了它，后者只是堆关键词。

## 总结

Proto 最有趣的地方在于：**它用"编程语言"的外壳，包裹了一个"生物序列设计的思维模型"。** 它不是让你学新语法，而是让你换一种方式思考生物设计问题——从"怎么一步步做"变成"声明你要什么条件"。

对于一个正在构建 AI Agent + 生信自动化平台的人来说，这种思维方式比具体的工具更有价值。而 Proto 的 MIT 许可、MCP 接口、AI 友好设计，都让它的生态可以被我们反向吸纳——不只是调用，而是融入。

后续我会接着写：如何实际把 Proto 的 MCP 服务接入我们的编排器，以及第一个集成示例的完整过程。
