---
title: 简历
date: 2026-06-07 00:00:00
type: resume
---

<style>
  .resume-page { max-width: 900px; margin: 0 auto; padding: 0 1rem; }
  
  /* Hero */
  .r-hero { text-align: center; padding: 3rem 0 2rem; border-bottom: 2px solid #e2e8f0; margin-bottom: 2.5rem; }
  .r-hero h1 { font-size: 2.8rem; font-weight: 800; letter-spacing: -1px; background: linear-gradient(135deg, #1e3a8a, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0.5rem; }
  .r-hero .r-subtitle { font-size: 1.1rem; color: #64748b; font-weight: 500; margin-bottom: 1.2rem; }
  .r-hero .r-contact { display: flex; justify-content: center; flex-wrap: wrap; gap: 0.5rem 1.5rem; font-size: 0.9rem; }
  .r-hero .r-contact a { color: #2563eb; text-decoration: none; font-weight: 500; }
  .r-hero .r-contact a:hover { text-decoration: underline; }
  .r-hero .r-print-btn { display: inline-flex; align-items: center; gap: 0.4rem; margin-top: 1.2rem; padding: 0.6rem 1.5rem; background: #1e3a8a; color: #fff; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 0.9rem; transition: background 0.2s, transform 0.15s; }
  .r-hero .r-print-btn:hover { background: #2563eb; transform: translateY(-2px); }

  /* Section */
  .r-section { margin-bottom: 2.5rem; }
  .r-section-title { font-size: 1.3rem; font-weight: 700; color: #1e3a8a; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; }

  /* Skills grid */
  .r-skills-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; }
  .r-skill-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem 1.2rem; transition: transform 0.15s, box-shadow 0.15s; }
  .r-skill-card:hover { transform: translateY(-3px); box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
  .r-skill-card h4 { font-size: 0.8rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; }
  .r-skill-tags { display: flex; flex-wrap: wrap; gap: 0.3rem; }
  .r-skill-copy { font-size: 0.86rem; color: #475569; line-height: 1.6; margin-bottom: 0.6rem; }
  .r-skill-tag { background: #eef2ff; color: #4338ca; padding: 0.2rem 0.7rem; border-radius: 16px; font-size: 0.82rem; font-weight: 500; }

  /* Projects */
  .r-project-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 0.8rem; }
  .r-project-card { border: 1px solid #e2e8f0; border-radius: 10px; padding: 1.2rem; background: #fafbfc; transition: transform 0.15s, box-shadow 0.15s; }
  .r-project-card:hover { transform: translateY(-3px); box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
  .r-project-card h4 { font-size: 1rem; margin-bottom: 0.3rem; }
  .r-project-card h4 a { color: #2563eb; text-decoration: none; }
  .r-project-card h4 a:hover { text-decoration: underline; }
  .r-project-card .r-desc { font-size: 0.85rem; color: #64748b; line-height: 1.5; margin-bottom: 0.5rem; }
  .r-project-card .r-lang { display: inline-block; font-size: 0.72rem; background: #e0e7ff; color: #3730a3; padding: 0.1rem 0.5rem; border-radius: 4px; font-weight: 500; }
  .r-project-card .r-badge { display: inline-block; font-size: 0.72rem; background: #dcfce7; color: #166534; padding: 0.1rem 0.5rem; border-radius: 4px; font-weight: 500; margin-left: 0.3rem; }

  /* Experience */
  .r-exp-item { margin-bottom: 1.5rem; padding-left: 1.5rem; position: relative; border-left: 3px solid #e2e8f0; }
  .r-exp-item::before { content: ''; position: absolute; left: -7px; top: 0.4rem; width: 10px; height: 10px; background: #3b82f6; border-radius: 50%; border: 3px solid #fff; }
  .r-exp-item:last-child { margin-bottom: 0; }
  .r-exp-head { display: flex; justify-content: space-between; align-items: baseline; gap: 0.5rem; margin-bottom: 0.3rem; }
  .r-exp-head .r-name { font-weight: 600; font-size: 1rem; }
  .r-exp-head .r-meta { font-size: 0.8rem; color: #94a3b8; }
  .r-exp-detail { font-size: 0.9rem; color: #475569; line-height: 1.6; }
  .r-exp-detail .r-hl { color: #2563eb; font-weight: 500; }

  /* Stats */
  .r-stats { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 1rem; }
  .r-stat { text-align: center; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem; }
  .r-stat .r-num { font-size: 1.8rem; font-weight: 800; color: #1e3a8a; line-height: 1.2; }
  .r-stat .r-label { font-size: 0.78rem; color: #64748b; margin-top: 0.3rem; }

  /* Org */
  .r-org-list { list-style: none; }
  .r-org-item { padding: 0.8rem 0; border-bottom: 1px solid #f1f5f9; }
  .r-org-item:last-child { border-bottom: none; }
  .r-org-item strong { color: #1e3a8a; }

  /* Print link */
  .r-print-section { text-align: center; padding: 2rem 0; border-top: 2px solid #e2e8f0; margin-top: 2rem; }
  .r-print-section a { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.8rem 2rem; background: linear-gradient(135deg, #1e3a8a, #2563eb); color: #fff; border-radius: 10px; text-decoration: none; font-weight: 600; font-size: 1rem; transition: transform 0.2s, box-shadow 0.2s; }
  .r-print-section a:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(37,99,235,0.3); }
  .r-print-hint { font-size: 0.8rem; color: #94a3b8; margin-top: 0.5rem; }

  /* Version timeline */
  .r-ver-bar { display: flex; justify-content: center; gap: 1rem; margin: 1rem 0 0.4rem; flex-wrap: wrap; }
  .r-ver-item { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.45rem 1.1rem; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.85rem; font-weight: 600; color: #475569; background: #f8fafc; text-decoration: none; transition: all 0.15s; }
  .r-ver-item:hover { border-color: #2563eb; color: #2563eb; }
  .r-ver-item .r-ver-tag { font-size: 0.72rem; background: #e0e7ff; color: #3730a3; padding: 0.1rem 0.5rem; border-radius: 4px; font-weight: 600; }
  .r-ver-item .r-ver-date { font-size: 0.72rem; color: #94a3b8; font-weight: 400; }
</style>

<div class="resume-page">

  <!-- Hero -->
  <div class="r-hero">
    <h1>BoHuYeShan (韩涛)</h1>
    <div class="r-subtitle">AI 模型训练与部署 · 生物信息学分析 · 分子生物学实验 · 科研工程交付</div>
    <div class="r-contact">
      <a href="https://github.com/BOHUYESHAN-APB">GitHub</a>
      <a href="https://github.com/BoHuYeShan">GitHub (个人)</a>
      <a href="https://bohuyeshan.top">博客</a>
      <a href="https://openi.pcl.ac.cn/bhys">OpenI</a>
      <a href="https://orcid.org/0009-0002-8426-0610">ORCID</a>
      <span>bohuyeshan@gmail.com</span>
    </div>
    <div class="r-ver-bar">
      <a class="r-ver-item" href="/HTML/jianli-v3.html" target="_blank"><span class="r-ver-tag">v3</span> 最新版 (A4)<span class="r-ver-date">2026-08-15 重构</span></a>
      <a class="r-ver-item" href="/HTML/jianli-v2.html" target="_blank"><span class="r-ver-tag">v2</span> 过渡版<span class="r-ver-date">2026-08-15 修订</span></a>
      <a class="r-ver-item" href="/HTML/jianli.html" target="_blank"><span class="r-ver-tag">v1</span> 历史版<span class="r-ver-date">2026-08-15 最后修订</span></a>
    </div>
  </div>

  <!-- 核心成果 -->
  <div class="r-section">
    <div class="r-section-title">🏆 核心成果</div>
    <div class="r-skills-grid">
      <div class="r-skill-card" style="border-color:#bfdbfe; background:#eff6ff;">
        <h4>发表论文</h4>
        <div class="r-skill-copy"><strong>IJMS 期刊论文第四作者</strong>（Software + Data curation）：Brassicaceae YABBY 系统发育与 CRC 介导的柱头发育调控，DOI: 10.3390/ijms27135740。</div>
      </div>
      <div class="r-skill-card" style="border-color:#bfdbfe; background:#eff6ff;">
        <h4>开源项目 · Linxira Bio SDK</h4>
        <div class="r-skill-copy"><strong>主导开发</strong>的本地优先生信分析平台：Rust 原生引擎、94 个分析能力（中英双语文档各 94 份）、28 个 agent skills，AGPL-3.0 开源。</div>
      </div>
      <div class="r-skill-card">
        <h4>发明专利申请</h4>
        <div class="r-skill-copy">第一发明人申请「基于 CNN 的多算法微生物培养综合识别方法及系统」，申请号 202510091154.4。</div>
      </div>
      <div class="r-skill-card">
        <h4>科研 Agent 工程</h4>
        <div class="r-skill-copy">开发 TypeScript/Bun 编排插件，以 6 个用户工作流主代理为核心；当前代码注册 19 个内置 Agent 定义，按需索引 617 个集成技能指令包。</div>
      </div>
    </div>
  </div>

  <!-- 技术能力 -->
  <div class="r-section">
    <div class="r-section-title">⚡ 技术能力</div>
    <div class="r-skills-grid">
      <div class="r-skill-card">
        <h4>AI 训练与模型部署</h4>
        <div class="r-skill-copy">围绕 PP-YOLOE+、PP-YOLO 和 YOLOv5/v8 开展训练、微调、ONNX 导出与边缘推理；完成树莓派 5 NCNN/ONNX 实测对比与菌落检测延迟优化。</div>
        <div class="r-skill-tags">
          <span class="r-skill-tag">PP-YOLOE+</span>
          <span class="r-skill-tag">YOLOv5/v8</span>
          <span class="r-skill-tag">PaddlePaddle</span>
          <span class="r-skill-tag">PyTorch</span>
          <span class="r-skill-tag">ONNX</span>
          <span class="r-skill-tag">NCNN</span>
          <span class="r-skill-tag">MindSpore</span>
        </div>
      </div>
      <div class="r-skill-card">
        <h4>生物信息学分析</h4>
        <div class="r-skill-copy">能把 BLASTP/RBH、DESeq2、WGCNA、GSEA/Mfuzz、motif、系统发育和 AlphaFold 串成候选基因证据链，并完成结构结果解释与可复现交付。</div>
        <div class="r-skill-tags">
          <span class="r-skill-tag">RNA-seq</span>
          <span class="r-skill-tag">BLASTP/RBH</span>
          <span class="r-skill-tag">DESeq2</span>
          <span class="r-skill-tag">WGCNA</span>
          <span class="r-skill-tag">GSEA/Mfuzz</span>
          <span class="r-skill-tag">AlphaFold</span>
          <span class="r-skill-tag">IQ-TREE</span>
        </div>
      </div>
      <div class="r-skill-card">
        <h4>分子生物学实验</h4>
        <div class="r-skill-copy">受过系统实验训练，可按 SOP 独立完成已掌握步骤：表型鉴定、RNA 提取与反转录、qRT-PCR、分子克隆、组织培养，并规范记录与整理结果。</div>
        <div class="r-skill-tags">
          <span class="r-skill-tag">表型鉴定</span>
          <span class="r-skill-tag">RNA 提取</span>
          <span class="r-skill-tag">qRT-PCR</span>
          <span class="r-skill-tag">分子克隆</span>
          <span class="r-skill-tag">组织培养</span>
        </div>
      </div>
      <div class="r-skill-card">
        <h4>系统与工程</h4>
        <div class="r-skill-copy">Linux / Git / Docker 日常交付；发起在研的 Linxira OS 科研发行版规划（双内核、签名仓库）；借助 AI 编程辅助探索 Rust/C++ 热点迁移（自学与原型验证阶段）。</div>
        <div class="r-skill-tags">
          <span class="r-skill-tag">Linux</span>
          <span class="r-skill-tag">Git</span>
          <span class="r-skill-tag">Docker</span>
          <span class="r-skill-tag">Shell</span>
          <span class="r-skill-tag">Rust（自学）</span>
          <span class="r-skill-tag">C++（自学）</span>
        </div>
      </div>
    </div>
  </div>

  <!-- 科研与实习经历 -->
  <div class="r-section">
    <div class="r-section-title">🔬 科研与实习经历</div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">课题组研究助理</div>
        <div class="r-meta">2025.01 — 2026.05</div>
      </div>
      <div class="r-exp-detail">
        在油菜 YABBY 课题中完成十字花科 YABBY 家族鉴定、系统发育树构建、顺式元件扫描与转录组差异表达分析，配套整理图件与分析脚本；同期独立搭建微生物菌落 CNN 检测与分类计数流程。
        <br><span class="r-hl">成果</span>: IJMS 期刊论文第四作者 (software + data curation); 以第一发明人申请发明专利 1 项 (基于 CNN 的微生物培养综合识别系统, 申请号 202510091154.4)
      </div>
    </div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">校内实习 — 荞麦矮化基因挖掘</div>
        <div class="r-meta">2026.03 — 2026.06</div>
      </div>
      <div class="r-exp-detail">
        通过 BLASTP/RBH 筛选 DWF4 直系同源候选，并比较上下游 ±3 基因的局部共线性；整合 24 样本 RNA-seq、WGCNA、GSEA/Mfuzz、启动子 motif、系统发育与 AlphaFold 结构预测。
        <br><span class="r-hl">成果</span>: 形成多层计算证据，完成 350 bp RNAi 靶片段、发卡表达盒与限制性酶切方案的 in-silico 设计；遗传转化和功能验证待完成
      </div>
    </div>
  </div>

  <!-- 发表论文与专利 -->
  <div class="r-section">
    <div class="r-section-title">📄 发表论文与专利</div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">The Phylogeny of Brassicaceae YABBYs and the CRC-Mediated Regulation of Stigma Development in <em>Brassica napus</em></div>
        <div class="r-meta">2026</div>
      </div>
      <div class="r-exp-detail">
        Lin Dai, Jinxiang Gao, Cheng Li, <span class="r-hl">韩涛 (Tao Han)</span>, Zhengshu Tian, Yunyun Zhang, Yusong Zhang, Yanqing Luo, Kaiqin Zhao, Xiaoyan Yuan, Canzhi Zhang, Tao Liu, Feng Zu*, Pei Qin*.
        <br><span class="r-hl">International Journal of Molecular Sciences</span>, 27(13), 5740.
        DOI: <a href="https://doi.org/10.3390/ijms27135740" style="color:#2563eb;">10.3390/ijms27135740</a>
        <br><span style="font-size:0.85rem; color:#64748b;">第四作者；CRediT：Software, Data curation（以论文作者贡献声明为准）</span>
      </div>
    </div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">一种基于卷积神经网络的多算法微生物培养综合识别方法及系统</div>
        <div class="r-meta">发明专利申请 · 第一发明人</div>
      </div>
      <div class="r-exp-detail">
        申请号：202510091154.4 · 云南农业大学 · 公布日期 2025-05-16
        <br><span style="font-size:0.85rem; color:#64748b;">法律状态以 CNIPA 最新记录为准。</span>
      </div>
    </div>
  </div>

  <!-- 开源项目 -->
  <div class="r-section">
    <div class="r-section-title">📦 开源项目精选</div>
    <div style="font-size:0.85rem; line-height:1.7; color:#475569; margin-bottom:1.5rem; padding:1rem; background:#f8fafc; border-left:3px solid #3b82f6; border-radius:0 8px 8px 0;">
      <strong style="color:#1e3a8a;">项目主线：</strong> 主导开发 Linxira Bio SDK（本地优先生信平台），并维护 OpenCode 科研编排插件；发起在研的 Linxira OS 科研工作站发行版。领域工具适配器持续开发。
      <br><br>
      <strong style="color:#1e3a8a;">前沿评估：</strong> 跟踪 Proto、PBCNet2.0 等 AI for Science 工具，形成 MCP/Agent 接入评估与技术笔记，不将第三方基准视为自身系统性能。
    </div>
    <div class="r-project-grid">
      <div class="r-project-card" style="border-color:#bfdbfe; background:#eff6ff;">
        <h4><a href="https://github.com/Linxira-OS/linxira-bio-sdk">Linxira Bio SDK</a> <span class="r-badge">主导开发</span></h4>
        <div class="r-desc"><strong>本地优先生信分析平台</strong>：Rust 原生引擎 + 原生 GUI/CLI + agent skills；94 个分析能力（中英双语文档各 94 份）、28 个 agent skills，AGPL-3.0 开源，CI 含 JSON Schema 验证。</div>
        <span class="r-lang">Rust · Python · R · Java</span>
      </div>
      <div class="r-project-card">
        <h4><a href="https://github.com/BOHUYESHAN-APB/openagent-labforge-bio">openagent-labforge-bio</a> <span class="r-badge">主线</span></h4>
        <div class="r-desc">OpenCode 科研编排插件：权限分层、计划执行、续跑/审查、会话检查点与 MCP；按需索引 617 个集成技能指令包。</div>
        <span class="r-lang">TypeScript / Bun</span>
      </div>
      <div class="r-project-card">
        <h4><a href="https://github.com/Linxira-OS/linxira-os">Linxira OS</a></h4>
        <div class="r-desc">在研科研工作站发行版：仓库边界、双内核策略、科研环境架构与路线图；ISO 构建和兼容性验证待完成。</div>
        <span class="r-lang">Architecture / Roadmap</span>
      </div>
      <div class="r-project-card">
        <h4><a href="https://github.com/BOHUYESHAN-APB/Buckwheat-seed-quality">Buckwheat-seed-quality</a></h4>
        <div class="r-desc">PP-YOLOE+ 荞麦籽粒检测与桌面/批量推理；树莓派 5 的 20 图同机测试中，NCNN CPU 延迟约为 ONNX Runtime CPU 的 1/1.83。</div>
        <span class="r-lang">Python / Kotlin</span>
      </div>
      <div class="r-project-card">
        <h4><a href="https://github.com/BOHUYESHAN-APB/CNN-MicroAI-Colony">CNN-MicroAI-Colony</a></h4>
        <div class="r-desc">菌落检测、抑菌圈分析和多端推理原型；5 图小样本工程测试中，平衡版 CPU 延迟由 2539 ms 降至 1884 ms。</div>
        <span class="r-lang">Python</span>
      </div>
    </div>
  </div>

  <!-- AI 训练 -->
  <div class="r-section">
    <div class="r-section-title">🧠 模型训练与部署实践</div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">目标检测训练与边缘推理</div>
      </div>
      <div class="r-exp-detail">
        围绕 PP-YOLOE+、PP-YOLO 和 YOLOv5/v8 开展训练、微调、ONNX 导出及 Android/树莓派推理实践；比较余弦退火、Restart 和分段式学习率策略，结合训练曲线记录进行小样本调参。
      </div>
    </div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">异构硬件迁移</div>
      </div>
      <div class="r-exp-detail">
        使用 CUDA/Paddle/PyTorch 开展实验；搭建 Ascend/OpenI/MindSpore 数据准备、参数解析与 dry-run 调度脚手架，完整训练指标待补齐。
      </div>
    </div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">竞赛与科研</div>
        <div class="r-meta">主持</div>
      </div>
      <div class="r-exp-detail">
        荞麦种子质量检测项目参加 2025 中国国际大学生创新大赛及"挑战杯"相关申报；负责 <span class="r-hl">PP-YOLOE+</span> 训练、推理工具和迁移脚手架实践。
      </div>
    </div>
  </div>

  <!-- 生物实验与生信分析 -->
  <div class="r-section">
    <div class="r-section-title">🔬 生物实验与生信分析</div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">独立实验能力</div>
      </div>
      <div class="r-exp-detail">
        接受过<span class="r-hl">植物表型鉴定</span>、<span class="r-hl">RNA 提取与反转录</span>、<span class="r-hl">qRT-PCR</span>、<span class="r-hl">分子克隆</span>和<span class="r-hl">组织培养</span>训练，可按 SOP 独立完成已掌握步骤，并进行实验记录与结果整理。
      </div>
    </div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">生信分析手段</div>
      </div>
      <div class="r-exp-detail">
        可独立完成植物 <strong>RNA-seq</strong>、候选基因筛选、<strong>系统发育</strong>与结构预测的可复现分析，覆盖 BLASTP/RBH、MAFFT/IQ-TREE、HISAT2/featureCounts/DESeq2、WGCNA、GSEA/Mfuzz、motif/JASPAR 与 AlphaFold；正在扩展 TCGA/GEO、网络药理学和分子模拟工作流。
      </div>
    </div>
  </div>

  <!-- 关键数据 -->
  <div class="r-section">
    <div class="r-section-title">📊 关键数据</div>
    <div class="r-stats">
      <div class="r-stat"><div class="r-num">1</div><div class="r-label">IJMS 期刊论文</div></div>
      <div class="r-stat"><div class="r-num">94</div><div class="r-label">Bio SDK 分析能力</div></div>
      <div class="r-stat"><div class="r-num">28</div><div class="r-label">Bio SDK agent skills</div></div>
      <div class="r-stat"><div class="r-num">1</div><div class="r-label">第一发明人专利申请</div></div>
      <div class="r-stat"><div class="r-num">24</div><div class="r-label">DWF4 分析样本</div></div>
      <div class="r-stat"><div class="r-num">617</div><div class="r-label">集成索引的技能指令包</div></div>
    </div>
  </div>

  <!-- 教育 -->
  <div class="r-section">
    <div class="r-section-title">🎓 教育</div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">云南农业大学</div>
        <div class="r-meta">本科在读 · 预计 2027.09 毕业</div>
      </div>
      <div class="r-exp-detail">生物技术专业</div>
    </div>
  </div>

  <!-- 求职信息 -->
  <div class="r-section">
    <div class="r-section-title">📌 求职信息</div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">科研数据分析 / 生物信息学分析</div>
      </div>
      <div class="r-exp-detail">面向科研数据清洗、统计与可视化、生物信息学分析及自动化报告等工作。</div>
    </div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">实验室助理 / 科研助理</div>
      </div>
      <div class="r-exp-detail">可按 SOP 完成已掌握的实验步骤，并承担实验记录、样本与数据整理及结果分析。</div>
    </div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">求职地点与到岗时间</div>
      </div>
      <div class="r-exp-detail">昆明优先，其他省会城市可考虑；面试通过后两周内到岗。</div>
    </div>
  </div>

  <!-- 组织参与 -->
  <div class="r-section">
    <div class="r-section-title">🤝 组织参与</div>
    <ul class="r-org-list">
      <li class="r-org-item"><strong>Linxira OS</strong> — 发起并推进基于 Arch/CachyOS 的科研工作站发行版规划；Bio SDK 主导开发</li>
      <li class="r-org-item"><strong>YeShanBoYun Studio</strong> — 组织成员，参与 NeuroPlex-Nexus 等项目</li>
      <li class="r-org-item"><strong>openagent-labforge-bio</strong> — 主线项目，持续开发维护</li>
      <li class="r-org-item"><strong>OpenI 启智社区</strong> — 公开保存部分 NPU/GPU 任务与模型记录</li>
    </ul>
  </div>

  <!-- 竞赛 -->
  <div class="r-section">
    <div class="r-section-title">🏅 竞赛项目经历</div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">2025 国际大学生创新创业大赛</div>
        <div class="r-meta">人工智能赛道主持</div>
      </div>
    </div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">2025 "挑战杯"全国竞赛</div>
        <div class="r-meta">人工智能赛道负责人 · 省级立项</div>
      </div>
    </div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">2025 大学生创新创业训练项目</div>
        <div class="r-meta">省级立项 · 中期检查优秀</div>
      </div>
    </div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">2025 互联网+ / 创新创业挑战</div>
        <div class="r-meta">省级立项 · 院系资助 · 优秀结题</div>
      </div>
    </div>
  </div>

  <!-- 在研项目与预期成果 -->
  <div class="r-section">
    <div class="r-section-title">📋 在研项目与预期成果</div>
    <div style="margin-bottom:1.2rem;">
      <div style="font-weight:600; font-size:0.95rem; margin-bottom:0.2rem;">AI 驱动药物虚拟筛选自动化管线 <span style="font-weight:400; font-size:0.8rem; color:#94a3b8;">2026.06 — 持续 · 前沿方法集成</span></div>
      <div style="font-size:0.9rem; color:#475569; line-height:1.6;">设计靶点检索、网络药理学、分子对接、分子动力学与报告生成的 Agent 工作流；正在评估 <span class="r-hl">PBCNet2.0</span> 等亲和力预测方法的接入可行性，尚未形成实验验证或性能结论。</div>
    </div>
    <div style="margin-bottom:1.2rem;">
      <div style="font-weight:600; font-size:0.95rem; margin-bottom:0.2rem;">荞麦矮化基因挖掘与功能分析 <span style="font-weight:400; font-size:0.8rem; color:#94a3b8;">在研 · 拟整理为预印本</span></div>
      <div style="font-size:0.9rem; color:#475569; line-height:1.6;">整合 24 样本 RNA-seq、同源与局部共线性、共表达、启动子、系统发育和结构预测证据；功能验证待完成。</div>
    </div>
    <div style="margin-bottom:1.2rem;">
      <div style="font-weight:600; font-size:0.95rem; margin-bottom:0.2rem;">微生物小目标检测算法改进 <span style="font-weight:400; font-size:0.8rem; color:#94a3b8;">在研 · 拟整理为预印本</span></div>
      <div style="font-size:0.9rem; color:#475569; line-height:1.6;">围绕微生物菌落小目标检测，持续比较 <span class="r-hl">PP-YOLO</span> 系列训练与学习率策略；已搭建 Ascend/OpenI/MindSpore 迁移脚手架，完整训练与评测结果待补齐。</div>
    </div>
    <div style="margin-top:1.2rem;">
      <div style="font-weight:600; font-size:0.95rem; margin-bottom:0.2rem;">Python / R 性能热点跨语言迁移 <span style="font-weight:400; font-size:0.8rem; color:#94a3b8;">自学 · 原型验证</span></div>
      <div style="font-size:0.9rem; color:#475569; line-height:1.6;">借助 AI 编程辅助梳理文件解析、表格处理和计算热点，尝试以 Rust/C++ 重写受解释器与单线程限制的模块；目前不声明统一性能结论。</div>
    </div>
  </div>

  <!-- 获取印刷版 -->
  <div class="r-print-section">
    <a href="/HTML/jianli-v2.html" target="_blank">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
      获取印刷版简历 (v3 · A4)
    </a>
    <div class="r-ver-bar">
      <a class="r-ver-item" href="/HTML/jianli-v3.html" target="_blank"><span class="r-ver-tag">v3</span> 最新版 (A4)<span class="r-ver-date">2026-08-15 重构</span></a>
      <a class="r-ver-item" href="/HTML/jianli-v2.html" target="_blank"><span class="r-ver-tag">v2</span> 过渡版<span class="r-ver-date">2026-08-15 修订</span></a>
      <a class="r-ver-item" href="/HTML/jianli.html" target="_blank"><span class="r-ver-tag">v1</span> 历史版<span class="r-ver-date">2026-08-15 最后修订</span></a>
    </div>
    <div class="r-print-hint">A4 双面打印 · 左右两页展开即完整简历</div>
  </div>

</div>