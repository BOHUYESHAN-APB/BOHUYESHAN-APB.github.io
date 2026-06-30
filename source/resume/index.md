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
  .r-skill-tag { background: #eef2ff; color: #4338ca; padding: 0.2rem 0.7rem; border-radius: 16px; font-size: 0.82rem; font-weight: 500; }

  /* Projects */
  .r-project-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }
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
    <div class="r-subtitle">AI 工程 · 生物信息学 · 开源 Linux 发行版构建</div>
    <div class="r-contact">
      <a href="https://github.com/BOHUYESHAN-APB">GitHub</a>
      <a href="https://github.com/BoHuYeShan">GitHub (个人)</a>
      <a href="https://bohuyeshan.top">博客</a>
      <a href="https://openi.pcl.ac.cn/bhys">OpenI</a>
      <a href="https://orcid.org/0009-0002-8426-0610">ORCID</a>
    </div>
    <a class="r-print-btn" href="/HTML/jianli.html" target="_blank">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
      获取印刷版简历 (A3)
    </a>
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
        负责生物信息学数据分析与挖掘。参与十字花科 YABBY 家族基因鉴定、系统发育重建、顺式作用元件预测及转录组差异表达分析; 同期开发微生物菌落 CNN 检测与分类计数流程。
        <br><span class="r-hl">成果</span>: IJMS 期刊论文第四作者 (software + data curation); 以第一发明人申请发明专利 1 项 (基于 CNN 的微生物培养综合识别系统, 申请号 202510091154.4)
      </div>
    </div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">校内实习 — 荞麦矮化基因挖掘</div>
        <div class="r-meta">2026.03 — 2026.06</div>
      </div>
      <div class="r-exp-detail">
        开展荞麦矮化相关基因挖掘与功能分析，关联 <span class="r-hl">Buckwheat-seed-quality</span> 项目。负责从基因组/转录组数据中筛选矮化候选基因，完成差异表达分析与功能注释。
        <br><span class="r-hl">成果</span>: 互联网+ 比赛荞麦推广项目核心成员
      </div>
    </div>
  </div>

  <!-- 技术能力 -->
  <div class="r-section">
    <div class="r-section-title">⚡ 技术能力</div>
    <div class="r-skills-grid">
      <div class="r-skill-card">
        <h4>编程语言</h4>
        <div class="r-skill-tags">
          <span class="r-skill-tag">Python</span>
          <span class="r-skill-tag">Java</span>
          <span class="r-skill-tag">TypeScript/JS</span>
          <span class="r-skill-tag">Rust（学习中）</span>
          <span class="r-skill-tag">Go</span>
          <span class="r-skill-tag">Dart</span>
          <span class="r-skill-tag">Shell</span>
        </div>
      </div>
      <div class="r-skill-card">
        <h4>AI 硬件与框架</h4>
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
        <h4>模型与算法</h4>
        <div class="r-skill-tags">
          <span class="r-skill-tag">LLM 训练</span>
          <span class="r-skill-tag">扩散模型</span>
          <span class="r-skill-tag">Transformer</span>
          <span class="r-skill-tag">PP-YOLO 系列</span>
          <span class="r-skill-tag">YOLOv5/v8</span>
          <span class="r-skill-tag">CNN 分类</span>
          <span class="r-skill-tag">余弦退火 + Restart</span>
          <span class="r-skill-tag">分层动态学习率</span>
        </div>
      </div>
      <div class="r-skill-card">
        <h4>工程与生态</h4>
        <div class="r-skill-tags">
          <span class="r-skill-tag">AI Agent 编排</span>
          <span class="r-skill-tag">API 网关</span>
          <span class="r-skill-tag">Linux 发行版构建</span>
          <span class="r-skill-tag">生物信息学</span>
          <span class="r-skill-tag">Docker</span>
          <span class="r-skill-tag">Git</span>
          <span class="r-skill-tag">OpenI CloudBrain</span>
        </div>
      </div>
    </div>
  </div>

  <!-- 关键数据 -->
  <div class="r-section">
    <div class="r-section-title">📊 关键数据</div>
    <div class="r-stats">
      <div class="r-stat"><div class="r-num">30+</div><div class="r-label">公开仓库</div></div>
      <div class="r-stat"><div class="r-num">617</div><div class="r-label">生信技能</div></div>
      <div class="r-stat"><div class="r-num">5/15</div><div class="r-label">编排器 / Agent</div></div>
      <div class="r-stat"><div class="r-num">2</div><div class="r-label">操作系统项目</div></div>
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
        Ascend 910 上原生训练 <span class="r-hl">LLM、扩散模型、Transformer</span> 及目标检测模型，涵盖混合精度与模型并行优化。
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
        2025 国际大学生创新创业大赛 · "挑战杯" —— 基于 <span class="r-hl">PP-YOLOE+ (L)</span> 的荞麦种子质量检测系统，完成 <span class="r-hl">Paddle/CUDA → MindSpore/Ascend 910</span> 全流程迁移。
      </div>
    </div>
  </div>

  <!-- 开源项目 -->
  <div class="r-section">
    <div class="r-section-title">📦 开源项目精选</div>
    <div class="r-project-grid">
      <div class="r-project-card">
        <h4><a href="https://github.com/BOHUYESHAN-APB/openagent-labforge-bio">openagent-labforge-bio</a> <span class="r-badge">主线</span></h4>
        <div class="r-desc">ExtendAI Lab——OpenCode 智能体编排框架：5 编排器 + 15 Agent + 617 生信技能 + 学术写作管线。</div>
        <span class="r-lang">Python</span>
      </div>
      <div class="r-project-card">
        <h4><a href="https://github.com/Linxira-OS/linxira-os">Linxira OS</a></h4>
        <div class="r-desc">基于 Arch/CachyOS 的科研发行版：Live-build、滚动更新稳定性调整、多内核支持。</div>
        <span class="r-lang">Shell / Python</span>
      </div>
      <div class="r-project-card">
        <h4><a href="https://github.com/BOHUYESHAN-APB/Buckwheat-seed-quality">Buckwheat-seed-quality</a></h4>
        <div class="r-desc">PP-YOLOE+ 荞麦质量检测，余弦退火调度 + Ascend 910 迁移 + 双平台推理。</div>
        <span class="r-lang">Python</span>
      </div>
      <div class="r-project-card">
        <h4><a href="https://github.com/Linxira-OS/extendai-lab-Studio">extendai-lab-Studio</a></h4>
        <div class="r-desc">AI 驱动科研编排与自动化层: 多模型协调、生信/化学分析管线规划、自主研究边界发现。</div>
        <span class="r-lang">Python</span>
      </div>
      <div class="r-project-card">
        <h4><a href="https://github.com/BOHUYESHAN-APB/VisionDeploy-Studio">VisionDeploy-Studio</a></h4>
        <div class="r-desc">CV 模型本地部署助手: YOLO 多硬件加速 (CUDA/XPU/ROCm)、按需环境管理。</div>
        <span class="r-lang">Python</span>
      </div>
      <div class="r-project-card">
        <h4><a href="https://github.com/Linxira-OS/extendai-lab-cli">extendai-lab-cli</a></h4>
        <div class="r-desc">多 LLM 编码代理 CLI：TUI + 插件系统 + 缓存优先架构，纯 Go 实现。</div>
        <span class="r-lang">Go</span>
      </div>
      <div class="r-project-card">
        <h4><a href="https://github.com/BOHUYESHAN-APB/CNN-MicroAI-Colony">CNN-MicroAI-Colony</a></h4>
        <div class="r-desc">CNN 菌落自动分析，华为 NPU + MindSpore 适配，OpenI 云端训练。</div>
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
      <li class="r-org-item"><strong>Linxira OS</strong> — 发起并构建基于 Arch/CachyOS 的科研发行版</li>
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
        生物技术专业背景，独立完成<span class="r-hl">植物表型鉴定</span>、<span class="r-hl">分子克隆</span>、<span class="r-hl">RNA 提取与反转录</span>、<span class="r-hl">qRT-PCR</span>等分子生物学实验；熟悉<span class="r-hl">组织培养</span>、<span class="r-hl">基因组 DNA 提取</span>等植物实验操作。
      </div>
    </div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">生信分析手段</div>
      </div>
      <div class="r-exp-detail">
        独立完成从原始数据到发表级结果的全流程生信分析：RNA-seq 差异表达分析（<span class="r-hl">DESeq2 / edgeR</span>）、基因家族系统发育重建（<span class="r-hl">MEGA / IQ-TREE</span>）、转录组功能注释（<span class="r-hl">GO / KEGG 富集</span>）、<span class="r-hl">WGCNA</span>共表达网络分析、<span class="r-hl">TCGA / GEO</span> 公共数据库检索与挖掘、网络药理学分析与分子对接。掌握 <span class="r-hl">Python / R / Shell</span> 生信脚本编写，GitHub 仓库完整记录分析流程与可复现代码。
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
        Lin Dai, Jinxiang Gao, Cheng Li, <span class="r-hl">韩涛 (Tao Han)</span>, Zhengshu Tian, Yunyun Zhang, Yusong Zhang, Yanqing Luo, Kaiqin Zhao, Xiaoyang Yuan, Canzhi Zhang, Tao Liu, Feng Zu*, Pei Qin*.
        <br><span class="r-hl">International Journal of Molecular Sciences</span>, 27(13), 5740.
        DOI: <a href="https://doi.org/10.3390/ijms27135740" style="color:#2563eb;">10.3390/ijms27135740</a>
        <br><span style="font-size:0.85rem; color:#64748b;">第四作者 · 贡献: software (生物信息分析流程与可视化工具开发)、data curation (基因组/转录组数据整理与质控)</span>
      </div>
    </div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">一种基于卷积神经网络的多算法微生物培养综合识别方法及系统</div>
        <div class="r-meta">发明专利 · 已公布 (13 个月)</div>
      </div>
      <div class="r-exp-detail">
        申请号：202510091154.4 · 云南农业大学 · 公布日期 2025-05-16
        <br><span style="font-size:0.85rem; color:#64748b;">基于 CNN 的多算法微生物培养综合识别方法及系统，涉及微生物菌落检测、分类与计数的自动化流程。专利已进入实审阶段。</span>
      </div>
    </div>
  </div>

  <!-- 荣誉 -->
  <div class="r-section">
    <div class="r-section-title">🏅 荣誉</div>
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
        <div class="r-name">大学生创新创业</div>
        <div class="r-meta">省级立项</div>
      </div>
    </div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">互联网+</div>
        <div class="r-meta">省级立项</div>
      </div>
    </div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">校内科研优秀项目表彰</div>
        <div class="r-meta">基于改进 YOLO 的菌落分析系统</div>
      </div>
    </div>
  </div>

  <!-- 自我评价 -->
  <div class="r-section">
    <div class="r-section-title">💡 自我评价</div>
    <p style="font-size:0.95rem; color:#475569; line-height:1.8;">
      生物技术专业本科在读，独立完成植物实验与分子生物学实验，可独立开展全流程生物信息学分析。IJMS 期刊第四作者 (software + data curation); 第一发明人申请发明专利 1 项 (基于 CNN 的微生物培养综合识别系统)。AI 训练、计算机视觉、生信工具链与 Agent 工程交叉实践，发起 Linxira OS (基于 Arch/CachyOS 的科研发行版)。30+ 公开仓库覆盖 AI、生信、系统软件等方向。
    </p>
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

  <!-- 在研项目与预期成果 -->
  <div class="r-section">
    <div class="r-section-title">📋 在研项目与预期成果</div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">荞麦矮化基因挖掘与功能分析</div>
        <div class="r-meta">预计 2026.09 预印本</div>
      </div>
      <div class="r-exp-detail">
        基于转录组与基因组数据挖掘荞麦矮化相关候选基因，完成差异表达分析与功能注释。计划同步发布于生物学与人工智能预印本平台。
      </div>
    </div>
    <div class="r-exp-item">
      <div class="r-exp-head">
        <div class="r-name">微生物小目标检测算法改进</div>
        <div class="r-meta">预计 2026.09 预印本</div>
      </div>
      <div class="r-exp-detail">
        针对微生物菌落检测中<span class="r-hl">小目标检测</span>这一行业惯性难题，从特殊检测算法出发，后续替换为 <span class="r-hl">PP-YOLO</span> 系列并引入改进余弦退火调度与学习率曲线优化，完成<span class="r-hl">华为 Ascend 910</span> 架构适配与训练。
      </div>
    </div>
  </div>

