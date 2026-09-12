---
title: 拆 Bio SDK（三）：schema 门禁、只读的环境计划，和会让发版失败的许可证
date: 2026-09-12 23:40:00
tags:
  - 架构
  - Rust
  - 本地优先
  - Bio SDK
categories:
  - 技术拆解

---

[第一篇](/2026/08/19/2026-08-19-05-拆Bio-SDK-一个不生成脚本的本地生信工具链是怎么搭的/)立论，[第二篇](/2026/09/12/2026-09-12-06-拆Bio-SDK-二-一条命令从JSON任务到结果图表中间经过了什么/)看数据怎么流，这篇回答最后那个问题：**一条"入口汇成一条道、输出只有一个信封"的路，凭什么跑两年不烂尾？**答案不在某个算法里，而在一堆"拦着事情发生"的机制里——schema 门禁、只读的环境计划、会让构建直接失败的许可证检查。拆的时候我对照 v1.0.1 的 README 与文档树；文中对环境计划各档的解释是基于档名的维度解读，精确边界以仓库 `RUNTIME_MANAGEMENT.md` 为准。

<!-- more -->

本系列共三篇：[第一篇（概览与观点）](/2026/08/19/2026-08-19-05-拆Bio-SDK-一个不生成脚本的本地生信工具链是怎么搭的/) · [第二篇（执行链路）](/2026/09/12/2026-09-12-06-拆Bio-SDK-二-一条命令从JSON任务到结果图表中间经过了什么/) · 第三篇（约束机制，即本篇）。

## 一、能力合约怎么运转：schema 是门禁，不是注释

第二篇说过每个能力带版本号（`sequence.stats.v1` 这类）、输出统一 JSON。撑住这件事的是一整条 CI 链：

- `schemas/` 里所有能力与结果的 JSON Schema **钉死在 Draft 2020-12**——不追新版本，校验器行为就不会漂；
- `scripts/validate-repository.py` 校验整个仓库的合约一致性；
- `scripts/generate_third_party_notices.py --check-config` 校验第三方许可配置；
- 校验器自己也被锁在 `requirements-ci.txt` 的固定版本上。

最后一条最容易被忽略但最狠：**校验工具本身不升级**。校验器的解析规则一变，昨天还能过的仓库今天就红，整个"合约"就没了公信力。能力版本升级时，v1 的输出按承诺保持可读——这是"CLI 合约稳定后才发 Python SDK"那句话能兑现的前提。

## 二、七档四模式，但整件事只读

环境计划值得单独一节，因为它太容易被理解成"帮我装环境"。先拆两个维度：**七档**（`local-core`、`scripting`、`managed-runtimes`、`containers`、`sequence-search`、`genomics-cli`、`full-local`）回答"要不要什么"，是范围的粒度；**四模式**（`use-existing`、`managed-user`、`project-isolated`、`system-missing-only`）回答"东西放哪、动谁的系统"，是落点的粒度。档位管范围、模式管落点，两个维度一组合，一份计划就是一张可以逐行审的清单——`environment plan sequence-search --mode managed-user --json` 输出的就是这张清单本身。

然后是最关键的约束：**计划是只读的**。文档原话是"Environment plans are read-only; installation is a separate, explicitly approved capability"——`environment.apply.v1` 至今还是计划中的能力，当前版本能预览、不能安装；想把清单变成真的环境，那是另一个需要显式批准的能力。README 还留了个细节：下载走 `GITHUB_PROXY` 环境变量指定的可信代理。把"规划"和"安装"切成两个合约，是整个 SDK 里我最想抄的一刀——**审计划和执行计划的人，可以不是同一个**。

## 三、pack 解剖：工作流的随身行李

`workflows/` 下的第三方工作流（跑 DESeq2 这类）不是裸脚本，而是带着四件行李发布：**自己的 schema、测试、锁文件、许可声明**。`linxira-bio workflow run` 在调用本地解释器之前先验证这套行李；`workflow packs --json` 把仓库里所有 pack 的状态列成清单。

配套的两条纪律同样重要：**发行版不捆绑第三方解释器、包、数据库或模型**——R 的 DESeq2、Python 的 Biopython/NumPy 都只是"已编目、未再分发"的依赖，装没装、哪个版本，由用户机器上的运行时管理决定。所以"已编目"不等于"已安装"，更不等于"可分析"。这三态的区分把责任切干净了：SDK 负责目录与验证，用户机器负责存在性。

## 四、发版门禁全链：许可证错了，构建直接失败

这是我最想抄的一整套。第一篇列过它的五级许可分级（记录 SPDX 与源仓库 → 确认与 AGPL-3.0-or-later 兼容 → 优先 MIT/Apache/BSD/ISC/Zlib → LGPL/MPL/GPL/模型权重/数据库条款单独审查 → 拒绝专有与模糊条款），这次补全执行链：

1. `deny.toml` 管 Rust 依赖的日常合规（cargo-deny）；
2. 发版走 `scripts/stage-release.py`：解析锁定的目标相关发布图，生成 `THIRD_PARTY_DEPENDENCIES.json` 和 `.txt`；
3. **缺失、歧义、过期或被修改的许可证文本，直接让发版失败**——不是警告，是失败。

还有两个容易漏的点。其一，SDK 自己是 **AGPL-3.0-or-later**，并且注明网络使用需提供源码——它拿最严的许可要求自己，才有立场对依赖挑三拣四。其二，**source policy**：GPTomics/bioSkills 是主要方法与示例来源，BioTender-max/awesome-bio-agent-skills 是发现索引；上游要过 **provenance、license、科学正确性、可执行行为**四项审查才算数，未过审的只是"研究输入"，全部隔离在 `.research/` 目录、**不得进入发版**。AI 时代拼装开源组件的工具越来越多，这套流程把合规做成了发版流程的一部分，而不是README 里的一句免责声明。

## 五、平台与 WSL 分工：连"不支持"都白纸黑字

平台矩阵上一篇给过结论（Windows 主平台，Debian/Arch 受支持，macOS 明确不是测试或打包目标），这篇补 WSL 两个发行版的角色差：**WSL Debian 是兼容提供者**，负责让老生信组件能跑；**WSL Arch 是当前平台提供方和未来 Linxira WSL 基础**——一个守存量，一个做增量。一个"未来基础"的措辞是有承诺含义的：新东西会先落在 Arch 侧，Debian 不承担演进职责。加上 `ARCHITECTURE.md`、`AI_AND_SDK.md`、`DATA_FORMATS.md`、`DEPENDENCY_NOTICES.md` 这套文档树，"什么在哪、支持到哪、不做什么"全部有地方可查。

## 收束

三篇拆完，回到第一篇那句结论：**生信工具不缺算法，缺的是把"测过、锁过、审计过"变成默认的工程纪律**。这篇补上的就是"锁"和"审计"的本体——schema 钉死校验器版本、环境计划只读、pack 三态分责、许可证失败即停、上游四审不过不发版。单看每一条都只是工程常识，难的是在"快出功能"的诱惑面前全部照办。这套约束机器和五十几个能力相比毫不性感，但它才是那个"交给别人跑也不报错"的承诺真正晒在太阳底下的部分。
