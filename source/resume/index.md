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
</style>

<div class="resume-page">

  <!-- Hero -->
  <div class="r-hero">
    <h1>BoHuYeShan (韩涛)</h1>
    <div class="r-subtitle">生物信息学 · AI Agent 工程 · 科研系统构建</div>
    <div class="r-contact">
      <a href="https://github.com/BOHUYESHAN-APB">GitHub</a>
      <a href="https://github.com/BoHuYeShan">GitHub (个人)</a>
      <a href="https://bohuyeshan.top">博客</a>
      <a href="https://openi.pcl.ac.cn/bhys">OpenI</a>
      <a href="https://orcid.org/0009-0002-8426-0610">ORCID</a>
      <span>bohuyeshan@gmail.com</span>
    </div>
    <a class="r-print-btn" href="/HTML/jianli.html" target="_blank">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
      获取印刷版简历 (A3)
    </a>
  </div>

  <div class="r-section">
    <div class="r-section-title">⭐ 核心亮点</div>
    <div class="r-skills-grid">
      <div class="r-skill-card">
        <h4>研究交付</h4>
        <div class="r-skill-copy">IJMS 第四作者（software + data curation），第一发明人申请发明专利 1 项。</div>
      </div>
      <div class="r-skill-card">
        <h4>候选基因主线</h4>
        <div class="r-skill-copy">围绕苦荞 DWF4 整合同源与局部共线性、表达/共表达、启动子、系统发育和结构预测等多层计算证据，并完成 RNAi 方案的 in-silico 设计。</div>
      </div>
      <div class="r-skill-card">
        <h4>科研 Agent 平台</h4>
        <div class="r-skill-copy">开发 6 个主要编排角色 + 11 个内置子代理的 OpenCode 插件，集成并索引 617 个生物信息与科学技能条目。</div>
      </div>
      <div class="r-skill-card">
        <h4>Linux 发行版工程</h4>
        <div class="r-skill-copy">发起在研的 Linxira OS，已建立 ISO 构建仓库、Pacman hooks、配置中心、官网与文档体系。</div>
      </div>
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

  <!-- 技术能力 -->
  <div class="r-section">
    <div class="r-section-title">⚡ 技术能力</div>
    <div class="r-skills-grid">
      <div class="r-skill-card">
        <h4>主要工作语言与交付</h4>
        <div class="r-skill-copy">以 Python / R / Shell 完成 RNA-seq、系统发育、结构分析与自动化报告；使用 Go / Rust 开展 CLI 与科研工具链重构。</div>
        <div class="r-skill-tags">
          <span class="r-skill-tag">Python</span>
          <span class="r-skill-tag">R</span>
          <span class="r-skill-tag">Go</span>
          <span class="r-skill-tag">Rust</span>
          <span class="r-skill-tag">Shell</span>
        </div>
      </div>
      <div class="r-skill-card">
        <h4>AI 训练与模型迁移</h4>
        <div class="r-skill-copy">在 Ascend 910 与 NVIDIA CUDA 环境开展目标检测及 Transformer/生成模型训练实验，主要可核验交付为 PP-YOLOE+ 的 MindSpore/Ascend 适配。</div>
        <div class="r-skill-tags">
          <span class="r-skill-tag">华为 Ascend 910</span>
          <span class="r-skill-tag">NVIDIA CUDA</span>
          <span class="r-skill-tag">MindSpore</span>
          <span class="r-skill-tag">PaddlePaddle</span>
          <span class="r-skill-tag">PyTorch</span>
          <span class="r-skill-tag">ONNX</span>
        </div>
      </div>
      <div class="r-skill-card">
        <h4>生信分析与结构解释</h4>
        <div class="r-skill-copy">能够把 BLASTP/RBH、DESeq2、WGCNA、GSEA/Mfuzz、motif、系统发育和 AlphaFold 串成候选基因证据链，并完成结构结果解释。</div>
        <div class="r-skill-tags">
          <span class="r-skill-tag">BLASTP/RBH</span>
          <span class="r-skill-tag">DESeq2</span>
          <span class="r-skill-tag">WGCNA</span>
          <span class="r-skill-tag">GSEA/Mfuzz</span>
          <span class="r-skill-tag">Phylogeny</span>
          <span class="r-skill-tag">AlphaFold</span>
        </div>
      </div>
      <div class="r-skill-card">
        <h4>系统与平台工程</h4>
        <div class="r-skill-copy">围绕在研 Linux 发行版与科研 Agent 原型，开展 ISO 构建链路、容器化、CLI、文档和工作流整合。</div>
        <div class="r-skill-tags">
          <span class="r-skill-tag">AI Agent 编排</span>
          <span class="r-skill-tag">Linux 发行版构建</span>
          <span class="r-skill-tag">Pacman Hooks</span>
          <span class="r-skill-tag">Config Hub</span>
          <span class="r-skill-tag">Docker</span>
          <span class="r-skill-tag">Git</span>
        </div>
      </div>
    </div>
  </div>

  <!-- 关键数据 -->
  <div class="r-section">
    <div class="r-section-title">📊 关键数据</div>
    <div class="r-stats">
      <div class="r-stat"><div class="r-num">30+</div><div class="r-label">公开仓库（含 fork）</div></div>
      <div class="r-stat"><div class="r-num">617</div><div class="r-label">集成索引的技能条目</div></div>
      <div class="r-stat"><div class="r-num">6 / 11</div><div class="r-label">主要编排角色 / 内置子代理</div></div>
      <div class="r-stat"><div class="r-num">1</div><div class="r-label">在研 Linux 发行版项目</div></div>
    </div>
  </div>

  <!-- AI 训练 -->
  <div class="r-section">
    <div class="r-section-title">🧠 AI 训练与模型优化</div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">华为 Ascend 910 原生训练</div>
      </div>
      <div class="r-exp-detail">
        在 Ascend 910 环境完成目标检测及若干 Transformer/生成模型训练实验，涉及混合精度与多卡配置。
      </div>
    </div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">NVIDIA GPU 训练与微调</div>
      </div>
      <div class="r-exp-detail">
        <span class="r-hl">PP-YOLO 系列</span>（PP-YOLOE+/v2）及 <span class="r-hl">YOLOv5/v8</span> 训练与微调，结合迁移学习与余弦退火策略。
      </div>
    </div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">竞赛与科研</div>
        <div class="r-meta">主持</div>
      </div>
      <div class="r-exp-detail">
        荞麦种子质量检测项目参加 2025 中国国际大学生创新大赛及“挑战杯”相关申报；负责 <span class="r-hl">PP-YOLOE+</span> 训练与 MindSpore/Ascend 适配。
      </div>
    </div>
  </div>

  <!-- 开源项目 -->
  <div class="r-section">
    <div class="r-section-title">📦 开源项目精选</div>
    <div style="font-size:0.85rem; line-height:1.7; color:#475569; margin-bottom:1.5rem; padding:1rem; background:#f8fafc; border-left:3px solid #3b82f6; border-radius:0 8px 8px 0;">
      <strong style="color:#1e3a8a;">项目主线：</strong> 开发基于 OpenCode 的 Agent 编排插件与科研工作流控制面原型，面向文献获取、数据整理、多组学分析和报告生成提供编排支持；领域工具适配器持续开发。
      <br><br>
      <strong style="color:#1e3a8a;">前沿评估：</strong> 跟踪 Proto、PBCNet2.0 等 AI for Science 工具，形成 MCP/Agent 接入评估与技术笔记，不将第三方基准视为自身系统性能。
    </div>
    <div class="r-project-grid">
      <div class="r-project-card">
        <h4><a href="https://github.com/BOHUYESHAN-APB/openagent-labforge-bio">openagent-labforge-bio</a> <span class="r-badge">主线</span></h4>
        <div class="r-desc"><strong>主线。</strong> OpenCode Agent 编排插件：6 个主要编排角色、11 个内置子代理，集成索引 617 个技能条目。</div>
        <span class="r-lang">Python</span>
      </div>
      <div class="r-project-card">
        <h4><a href="https://github.com/Linxira-OS/linxira-os">Linxira OS</a></h4>
        <div class="r-desc">在研科研 Linux 发行版：已建立 ISO 构建仓库、Pacman hooks、配置中心、官网与文档体系。</div>
        <span class="r-lang">Shell / Python</span>
      </div>
      <div class="r-project-card">
        <h4><a href="https://github.com/BOHUYESHAN-APB/Buckwheat-seed-quality">Buckwheat-seed-quality</a></h4>
        <div class="r-desc">基于 PP-YOLOE+ 的荞麦籽粒检测项目，包含训练记录、桌面推理与 MindSpore/Ascend 适配实验。</div>
        <span class="r-lang">Python / Julia</span>
      </div>
      <div class="r-project-card">
        <h4><a href="https://github.com/Linxira-OS/extendai-lab-Studio">extendai-lab-Studio</a></h4>
        <div class="r-desc">科研工作流控制面原型：实现基础编排与安全校验，领域工具适配持续开发。</div>
        <span class="r-lang">Python</span>
      </div>
      <div class="r-project-card">
        <h4><a href="https://github.com/BOHUYESHAN-APB/VisionDeploy-Studio">VisionDeploy-Studio</a></h4>
        <div class="r-desc">探索 YOLO 多硬件部署与按需环境管理的原型项目。</div>
        <span class="r-lang">Python</span>
      </div>
      <div class="r-project-card">
        <h4><a href="https://github.com/Linxira-OS/extendai-lab-cli">extendai-lab-cli</a></h4>
        <div class="r-desc">多模型 CLI：TUI 交互、缓存与插件扩展，面向科研场景推进 Go / Rust 重构。</div>
        <span class="r-lang">Go / Rust</span>
      </div>
      <div class="r-project-card">
        <h4><a href="https://github.com/BOHUYESHAN-APB/CNN-MicroAI-Colony">CNN-MicroAI-Colony</a></h4>
        <div class="r-desc">微生物菌落检测与计数原型，围绕 PP-YOLO、ONNX 及边缘端部署开展实践。</div>
        <span class="r-lang">Python</span>
      </div>
      <div class="r-project-card">
        <h4><a href="https://github.com/BOHUYESHAN-APB/MicroAGI-Agri">MicroAGI-Agri</a></h4>
        <div class="r-desc">农业 AI 应用，多模态视觉在农业场景的实践探索。</div>
        <span class="r-lang">Python</span>
      </div>
    </div>
  </div>

  <!-- 组织参与 -->
  <div class="r-section">
    <div class="r-section-title">🤝 组织参与</div>
    <ul class="r-org-list">
      <li class="r-org-item"><strong>Linxira OS</strong> — 发起并推进基于 Arch/CachyOS 的在研科研发行版</li>
      <li class="r-org-item"><strong>YeShanBoYun Studio</strong> — 组织成员，参与 NeuroPlex-Nexus 等项目</li>
      <li class="r-org-item"><strong>openagent-labforge-bio</strong> — 主线项目，持续开发维护</li>
      <li class="r-org-item"><strong>OpenI 启智社区</strong> — 活跃训练，公开发布 NPU/GPU 模型</li>
    </ul>
  </div>

  <!-- 生物实验与生信分析 -->
  <div class="r-section">
    <div class="r-section-title">🔬 生物实验与生信分析</div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">独立实验能力</div>
      </div>
      <div class="r-exp-detail">
        接受过<span class="r-hl">植物表型鉴定</span>、<span class="r-hl">RNA 提取与反转录</span>、<span class="r-hl">qRT-PCR</span>、分子克隆和组织培养训练，可按 SOP 独立完成已掌握步骤，并进行实验记录与结果整理。
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
        <br><span style="font-size:0.85rem; color:#64748b;">2025-05-16 公布；法律状态以 CNIPA 最新记录为准。</span>
      </div>
    </div>
  </div>

  <!-- 荣誉 -->
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
        <div class="r-name">2025 互联网+</div>
        <div class="r-meta">省级立项 · 中期检查优秀</div>
      </div>
    </div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">2025 创新创业挑战</div>
        <div class="r-meta">院系资助 · 优秀结题</div>
      </div>
    </div>
  </div>

  <!-- 自我评价 -->
  <div class="r-section">
    <div class="r-section-title">💡 自我评价</div>
    <p style="font-size:0.95rem; color:#475569; line-height:1.8;">
      生物技术专业本科在读，聚焦植物生物信息学、科研 Agent 与 Linux 工程。已在发表论文中承担 Software 和 Data curation 贡献；完成苦荞 DWF4 多层计算证据整合与 RNAi in-silico 设计，并推进 OpenCode Agent 插件和在研科研 Linux 发行版项目。
    </p>
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
    <div style="margin-bottom:0;">
      <div style="font-weight:600; font-size:0.95rem; margin-bottom:0.2rem;">微生物小目标检测算法改进 <span style="font-weight:400; font-size:0.8rem; color:#94a3b8;">在研 · 拟整理为预印本</span></div>
      <div style="font-size:0.9rem; color:#475569; line-height:1.6;">针对微生物菌落检测中<span class="r-hl">小目标检测</span>这一行业惯性难题，从特殊检测算法出发，后续替换为 <span class="r-hl">PP-YOLO</span> 系列并引入改进余弦退火调度与学习率曲线优化，完成<span class="r-hl">华为 Ascend 910</span> 架构适配与训练。</div>
    </div>
  </div>

  <!-- 获取印刷版 -->
  <div class="r-print-section">
    <a href="/HTML/jianli.html" target="_blank">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
      获取印刷版简历 (A3)
    </a>
    <div class="r-print-hint">A3 横向打印 · 左右两页展开即完整简历 · 也可分页打印为两张 A4</div>
  </div>

</div>
