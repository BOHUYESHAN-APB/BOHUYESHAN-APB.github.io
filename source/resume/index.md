---
title: 简历
date: 2026-06-07 00:00:00
type: resume
---

<style>
  .resume-page { max-width: 900px; margin: 0 auto; padding: 0 1rem; }
  .r-hero { text-align: center; padding: 3rem 0 2rem; border-bottom: 2px solid #e2e8f0; margin-bottom: 2.5rem; }
  .r-hero h1 { font-size: 2.8rem; font-weight: 800; letter-spacing: -1px; background: linear-gradient(135deg, #1e3a8a, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0.5rem; }
  .r-hero .r-subtitle { font-size: 1.1rem; color: #64748b; font-weight: 500; margin-bottom: 1.2rem; }
  .r-hero .r-contact { display: flex; justify-content: center; flex-wrap: wrap; gap: 0.5rem 1.5rem; font-size: 0.9rem; }
  .r-hero .r-contact a { color: #2563eb; text-decoration: none; font-weight: 500; }
  .r-hero .r-contact a:hover { text-decoration: underline; }
  .r-section { margin-bottom: 2.5rem; }
  .r-section-title { font-size: 1.3rem; font-weight: 700; color: #1e3a8a; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; }
  .r-ver-primary { display: flex; align-items: center; gap: 1rem; padding: 1.1rem 1.4rem; border: 2px solid #bfdbfe; background: linear-gradient(135deg, #eff6ff, #f8fafc); border-radius: 12px; text-decoration: none; margin-bottom: 0.9rem; transition: transform 0.15s, box-shadow 0.15s; }
  .r-ver-primary:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(37,99,235,0.15); }
  .r-ver-primary .r-ver-tag { background: #1e3a8a; color: #fff; font-size: 0.78rem; font-weight: 700; padding: 0.28rem 0.7rem; border-radius: 6px; white-space: nowrap; }
  .r-ver-primary-title { font-weight: 700; color: #101a33; font-size: 1.02rem; display: block; }
  .r-ver-primary-desc { font-size: 0.83rem; color: #64748b; margin-top: 0.15rem; display: block; }
  .r-ver-primary-cta { margin-left: auto; color: #2563eb; font-weight: 600; font-size: 0.88rem; white-space: nowrap; }
  .r-ver-old { display: flex; align-items: center; flex-wrap: wrap; gap: 0.6rem; font-size: 0.86rem; color: #475569; }
  .r-ver-old select { padding: 0.45rem 0.8rem; border: 1px solid #cbd5e1; border-radius: 8px; background: #f8fafc; color: #334155; font-size: 0.85rem; cursor: pointer; }
  .r-ver-old select:hover { border-color: #2563eb; }
  @media (max-width: 600px) {
    .r-ver-primary { flex-direction: column; align-items: flex-start; gap: 0.6rem; }
    .r-ver-primary-cta { margin-left: 0; }
  }
  .r-grid-3 { display: grid; grid-template-columns: repeat(6, 1fr); gap: 1rem; }
  .r-grid-3 > * { grid-column: span 2; }
  .r-grid-3 > .r-w2 { grid-column: span 3; }
  .r-grid-3 > .r-w3 { grid-column: span 6; }
  @media (max-width: 900px) { .r-grid-3 { grid-template-columns: repeat(2, 1fr); } .r-grid-3 > *, .r-grid-3 > .r-w2 { grid-column: auto; } .r-grid-3 > .r-w3 { grid-column: 1 / -1; } }
  @media (max-width: 600px) { .r-grid-3 { grid-template-columns: 1fr; } .r-grid-3 > *, .r-grid-3 > .r-w2, .r-grid-3 > .r-w3 { grid-column: auto; } }
  .r-skill-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem 1.2rem; transition: transform 0.15s, box-shadow 0.15s; }
  .r-skill-card:hover { transform: translateY(-3px); box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
  .r-skill-card h4 { font-size: 0.8rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; }
  .r-skill-tags { display: flex; flex-wrap: wrap; gap: 0.3rem; }
  .r-skill-copy { font-size: 0.86rem; color: #475569; line-height: 1.6; margin-bottom: 0.6rem; }
  .r-skill-tag { background: #eef2ff; color: #4338ca; padding: 0.2rem 0.7rem; border-radius: 16px; font-size: 0.82rem; font-weight: 500; }
  .r-project-card { border: 1px solid #e2e8f0; border-radius: 10px; padding: 1.2rem; background: #fafbfc; transition: transform 0.15s, box-shadow 0.15s; }
  .r-project-card:hover { transform: translateY(-3px); box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
  .r-project-card h4 { font-size: 1rem; margin-bottom: 0.3rem; }
  .r-project-card h4 a { color: #2563eb; text-decoration: none; }
  .r-project-card h4 a:hover { text-decoration: underline; }
  .r-project-card .r-desc { font-size: 0.85rem; color: #64748b; line-height: 1.5; margin-bottom: 0.5rem; }
  .r-project-card .r-lang { display: inline-block; font-size: 0.72rem; background: #e0e7ff; color: #3730a3; padding: 0.1rem 0.5rem; border-radius: 4px; font-weight: 500; }
  .r-project-card .r-badge { display: inline-block; font-size: 0.72rem; background: #dcfce7; color: #166534; padding: 0.1rem 0.5rem; border-radius: 4px; font-weight: 500; margin-left: 0.3rem; }
  .r-links { font-size: 0.78rem; margin: 0.35rem 0 0.45rem; color: #94a3b8; }
  .r-links a { color: #2563eb; text-decoration: none; font-weight: 600; margin-right: 0.8rem; }
  .r-links a:hover { text-decoration: underline; }
  .r-exp-item { margin-bottom: 1.5rem; padding-left: 1.5rem; position: relative; border-left: 3px solid #e2e8f0; }
  .r-exp-item::before { content: ''; position: absolute; left: -7px; top: 0.4rem; width: 10px; height: 10px; background: #3b82f6; border-radius: 50%; border: 3px solid #fff; }
  .r-exp-item:last-child { margin-bottom: 0; }
  .r-exp-head { display: flex; justify-content: space-between; align-items: baseline; gap: 0.5rem; margin-bottom: 0.3rem; flex-wrap: wrap; }
  .r-exp-head .r-name { font-weight: 600; font-size: 1rem; }
  .r-exp-head .r-meta { font-size: 0.8rem; color: #94a3b8; }
  .r-exp-detail { font-size: 0.9rem; color: #475569; line-height: 1.6; }
  .r-exp-detail .r-hl { color: #2563eb; font-weight: 500; }
  .r-stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
  @media (max-width: 900px) { .r-stats { grid-template-columns: repeat(2, 1fr); } }
  @media (max-width: 480px) { .r-stats { grid-template-columns: repeat(2, 1fr); } }
  .r-stat { text-align: center; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem; }
  .r-stat .r-num { font-size: 1.8rem; font-weight: 800; color: #1e3a8a; line-height: 1.2; }
  .r-stat .r-label { font-size: 0.78rem; color: #64748b; margin-top: 0.3rem; }
  .r-org-list { list-style: none; padding: 0; }
  .r-org-item { padding: 0.8rem 0; border-bottom: 1px solid #f1f5f9; }
  .r-org-item:last-child { border-bottom: none; }
  .r-org-item strong { color: #1e3a8a; }
  .r-org-item a { color: #2563eb; text-decoration: none; font-weight: 500; }
  .r-org-item a:hover { text-decoration: underline; }
  .r-link-note { font-size: 0.85rem; line-height: 1.7; color: #475569; margin-bottom: 1.2rem; padding: 1rem; background: #f8fafc; border-left: 3px solid #3b82f6; border-radius: 0 8px 8px 0; }
  .r-link-group { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem 1.2rem; }
  .r-link-group h4 { font-size: 0.8rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem; }
  .r-link-group ul { list-style: none; padding: 0; margin: 0; }
  .r-link-group li { padding: 0.28rem 0; font-size: 0.88rem; color: #475569; }
  .r-link-group li a { color: #2563eb; text-decoration: none; font-weight: 500; }
  .r-link-group li a:hover { text-decoration: underline; }
  .r-chart-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1.1rem 1.2rem; transition: transform 0.15s, box-shadow 0.15s; }
  .r-chart-card:hover { transform: translateY(-3px); box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
  .r-chart-card h4 { font-size: 0.92rem; color: #101a33; margin-bottom: 0.2rem; display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; flex-wrap: wrap; }
  .r-chart-card .r-chart-sub { font-size: 0.76rem; color: #94a3b8; margin-bottom: 0.6rem; }
  .r-chart-badge { font-size: 0.72rem; background: #dcfce7; color: #166534; padding: 0.15rem 0.55rem; border-radius: 999px; font-weight: 700; white-space: nowrap; }
  .r-chart-card svg { width: 100%; height: auto; display: block; }
  .r-chart-card .bar { transform-box: fill-box; transform-origin: left center; animation: rGrow 1.1s cubic-bezier(0.22, 0.61, 0.36, 1) both; }
  .r-chart-card .bar.d1 { animation-delay: 0.15s; }
  .r-chart-card .bar.d2 { animation-delay: 0.35s; }
  .r-chart-card .bar.d3 { animation-delay: 0.55s; }
  .r-chart-card .bar.d4 { animation-delay: 0.75s; }
  @keyframes rGrow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
  @media (prefers-reduced-motion: reduce) { .r-chart-card .bar { animation: none; } }
  .r-chart-foot { font-size: 0.75rem; color: #94a3b8; margin-top: 0.5rem; }
  .r-print-section { text-align: center; padding: 2rem 0; border-top: 2px solid #e2e8f0; margin-top: 2rem; }
  .r-print-section a { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.8rem 2rem; background: linear-gradient(135deg, #1e3a8a, #2563eb); color: #fff; border-radius: 10px; text-decoration: none; font-weight: 600; font-size: 1rem; transition: transform 0.2s, box-shadow 0.2s; }
  .r-print-section a:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(37,99,235,0.3); }
  .r-print-hint { font-size: 0.8rem; color: #94a3b8; margin-top: 0.5rem; }
</style>
<div class="resume-page">
<div class="r-hero">
<h1>BoHuYeShan (韩涛)</h1>
<div class="r-subtitle">AI 模型训练与部署 · 生物信息学分析 · 分子生物学实验 · 科研工程交付</div>
<div class="r-contact">
<a href="https://github.com/BOHUYESHAN-APB">GitHub</a>
<a href="https://github.com/Linxira-OS">Linxira-OS (开源组织)</a>
<a href="https://github.com/BoHuYeShan">GitHub (个人)</a>
<a href="https://bohuyeshan.top">博客</a>
<a href="https://openi.pcl.ac.cn/bhys">OpenI</a>
<a href="https://orcid.org/0009-0002-8426-0610">ORCID</a>
<span>bohuyeshan@163.com / bohuyeshan@gmail.com</span>
</div>
</div>
<div class="r-section">
<div class="r-section-title">🗂️ 简历版本</div>
<a class="r-ver-primary" href="/HTML/resume-lab.html" target="_blank">
<span class="r-ver-tag">实验 / 检测岗</span>
<span>
<span class="r-ver-primary-title">实验与检测岗位 · A4 双页</span>
<span class="r-ver-primary-desc">以微生物培养、油菜与荞麦课题为主体，按「实验设计 → 实验操作 → 数据与产出」展开个人实验能力 · 一键导出 PDF</span>
</span>
<span class="r-ver-primary-cta">在线查看 / 导出 PDF →</span>
</a>
<a class="r-ver-primary" href="/HTML/resume-tech.html" target="_blank">
<span class="r-ver-tag">生信 / AI 工程岗</span>
<span>
<span class="r-ver-primary-title">生信与 AI 工程岗位 · A4 双页</span>
<span class="r-ver-primary-desc">生物信息学分析 · AI 训练部署 · Agent 与 SDK 工程 · 科研工程交付 · 一键导出 PDF</span>
</span>
<span class="r-ver-primary-cta">在线查看 / 导出 PDF →</span>
</a>
<a class="r-ver-primary" href="/HTML/resume-full.html" target="_blank">
<span class="r-ver-tag">综合海投</span>
<span>
<span class="r-ver-primary-title">招聘平台标准模板 · A4 双页</span>
<span class="r-ver-primary-desc">全能力展示 · 多岗位并列 · 标准模板骨架 · 适合招聘平台广撒网 · 一键导出 PDF</span>
</span>
<span class="r-ver-primary-cta">在线查看 / 导出 PDF →</span>
</a>
<div class="r-ver-old">
<label for="r-ver-select">归档旧版：</label>
<select id="r-ver-select" onchange="if(this.value){window.open(this.value,'_blank');this.selectedIndex=0;}">
<option value="">— 选择归档版本 —</option>
<option value="/HTML/resume-archived-01.html">旧版 · 科研支持定位</option>
<option value="/HTML/resume-archived-02.html">旧版 · 工程交付定位</option>
</select>
</div>
</div>
<div class="r-section">
<div class="r-section-title">🏆 核心成果</div>
<div class="r-grid-3">
<div class="r-skill-card r-w2" style="border-color:#bfdbfe; background:#eff6ff;">
<h4>发表论文</h4>
<div class="r-skill-copy"><strong>IJMS 期刊论文第四作者</strong>（Software + Data curation）：Brassicaceae YABBY 系统发育与 CRC 介导的柱头发育调控，DOI: 10.3390/ijms27135740。</div>
</div>
<div class="r-skill-card r-w2" style="border-color:#bfdbfe; background:#eff6ff;">
<h4>开源项目 · Linxira Bio SDK</h4>
<div class="r-skill-copy"><strong>主导开发</strong>的本地优先生信分析平台：Rust 原生引擎、94 个分析能力、28 个 agent skills、Windows/Debian/Arch 三平台，AGPL-3.0 开源，配套独立官网。</div>
</div>
<div class="r-skill-card r-w2">
<h4>发明专利 · 实质审查中</h4>
<div class="r-skill-copy">第一发明人申请「基于 CNN 的多算法微生物培养综合识别方法及系统」，申请号 202510091154.4；已公开并进入实质审查。</div>
</div>
<div class="r-skill-card r-w2">
<h4>科研 Agent 工程</h4>
<div class="r-skill-copy">开发 TypeScript/Bun 编排插件，以 6 个用户工作流主代理为核心；当前代码注册 19 个内置 Agent 定义，按需索引 617 个集成技能指令包。</div>
</div>
</div>
</div>
<div class="r-section">
<div class="r-section-title">📈 量化成果 · 数据一览</div>
<div class="r-grid-3">
<div class="r-chart-card">
<h4>树莓派 5 边缘推理延迟 <span class="r-chart-badge">1.83× 提速</span></h4>
<div class="r-chart-sub">Buckwheat-seed-quality · 20 图同机实测（CPU 推理，毫秒/图）</div>
<svg viewBox="0 0 340 118" role="img" aria-label="树莓派5边缘推理延迟对比：ONNX Runtime 561毫秒，NCNN 307毫秒">
<line x1="100" y1="16" x2="320" y2="16" stroke="#e2e8f0" stroke-width="1"/>
<text x="92" y="45" text-anchor="end" font-size="11" fill="#475569">ONNX Runtime</text>
<rect class="bar" x="100" y="29" width="210" height="22" rx="4" fill="#94a3b8"/>
<text x="304" y="45" text-anchor="end" font-size="11" fill="#fff" font-weight="700">561 ms</text>
<text x="92" y="87" text-anchor="end" font-size="11" fill="#475569">NCNN</text>
<rect class="bar d1" x="100" y="71" width="115" height="22" rx="4" fill="#2563eb"/>
<text x="223" y="87" font-size="11" fill="#1e3a8a" font-weight="700">307 ms</text>
<text x="320" y="108" text-anchor="end" font-size="10" fill="#94a3b8">延迟 ↓ 45%</text>
</svg>
</div>
<div class="r-chart-card">
<h4>菌落检测 CPU 延迟优化 <span class="r-chart-badge">↓ 26% 延迟</span></h4>
<div class="r-chart-sub">CNN-MicroAI-Colony · 5 图小样本工程测试（平衡版，毫秒/图）</div>
<svg viewBox="0 0 340 118" role="img" aria-label="菌落检测CPU延迟优化：优化前2539毫秒，优化后1884毫秒">
<line x1="100" y1="16" x2="320" y2="16" stroke="#e2e8f0" stroke-width="1"/>
<text x="92" y="45" text-anchor="end" font-size="11" fill="#475569">优化前</text>
<rect class="bar" x="100" y="29" width="210" height="22" rx="4" fill="#94a3b8"/>
<text x="304" y="45" text-anchor="end" font-size="11" fill="#fff" font-weight="700">2539 ms</text>
<text x="92" y="87" text-anchor="end" font-size="11" fill="#475569">优化后</text>
<rect class="bar d1" x="100" y="71" width="156" height="22" rx="4" fill="#2563eb"/>
<text x="264" y="87" font-size="11" fill="#1e3a8a" font-weight="700">1884 ms</text>
<text x="320" y="108" text-anchor="end" font-size="10" fill="#94a3b8">同机同源工程测试</text>
</svg>
</div>
<div class="r-chart-card">
<h4>Linxira 开源生态规模 <span class="r-chart-badge">26 仓库</span></h4>
<div class="r-chart-sub">Linxira-OS 组织 · 自研交付物统计（项）</div>
<svg viewBox="0 0 340 146" role="img" aria-label="Linxira开源生态规模：双语文档108、分析能力94、agent skills 28、开源仓库26、签名工具17">
<text x="110" y="26" text-anchor="end" font-size="11" fill="#475569">双语文档</text>
<rect class="bar" x="118" y="14" width="190" height="16" rx="4" fill="#1e3a8a"/>
<text x="316" y="26" font-size="11" fill="#1e3a8a" font-weight="700">108</text>
<text x="110" y="52" text-anchor="end" font-size="11" fill="#475569">分析能力</text>
<rect class="bar d1" x="118" y="40" width="165" height="16" rx="4" fill="#2563eb"/>
<text x="291" y="52" font-size="11" fill="#1e3a8a" font-weight="700">94</text>
<text x="110" y="78" text-anchor="end" font-size="11" fill="#475569">agent skills</text>
<rect class="bar d2" x="118" y="66" width="49" height="16" rx="4" fill="#3b82f6"/>
<text x="175" y="78" font-size="11" fill="#1e3a8a" font-weight="700">28</text>
<text x="110" y="104" text-anchor="end" font-size="11" fill="#475569">开源仓库</text>
<rect class="bar d3" x="118" y="92" width="46" height="16" rx="4" fill="#60a5fa"/>
<text x="172" y="104" font-size="11" fill="#1e3a8a" font-weight="700">26</text>
<text x="110" y="130" text-anchor="end" font-size="11" fill="#475569">签名工具</text>
<rect class="bar d4" x="118" y="118" width="30" height="16" rx="4" fill="#93c5fd"/>
<text x="156" y="130" font-size="11" fill="#1e3a8a" font-weight="700">17</text>
</svg>
<div class="r-chart-foot">另：617 个技能指令包按需索引 · 19 个内置 Agent 定义 · 15+ 模型提供商接入（Zeta）</div>
</div>
</div>
</div>
<div class="r-section">
<div class="r-section-title">⚡ 技术能力</div>
<div class="r-grid-3">
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
<div class="r-skill-copy">日常以 Linux/Git/Docker 交付。发起 <strong>Linxira OS</strong> 科研工作站发行版：KDE Plasma 桌面直接基于 Arch 官方仓库构建，双内核（linux + linux-lts）为滚动更新兜底，Timeshift 快照 + grub-btrfs 回滚，自有签名密钥的 [linxira] 仓库发布 17 个自研工具，93 款审核软件目录；Podman/Distrobox/Apptainer 容器化科研复现开箱即用，无头模式一键释放算力。借助 AI 编程辅助探索 Rust/C++ 热点迁移（原型验证阶段）。</div>
<div class="r-skill-tags">
<span class="r-skill-tag">Arch Linux</span>
<span class="r-skill-tag">KDE Plasma</span>
<span class="r-skill-tag">Podman</span>
<span class="r-skill-tag">Timeshift/btrfs</span>
<span class="r-skill-tag">Git</span>
<span class="r-skill-tag">Docker</span>
<span class="r-skill-tag">Rust（自学）</span>
</div>
</div>
<div class="r-skill-card">
<h4>Agent 与自动化工程</h4>
<div class="r-skill-copy">以 TypeScript/Bun 开发 OpenCode 科研编排插件（权限分层、计划执行、会话检查点、MCP）；构建 AI API 聚合与统一网关原型（Rust/Go），支持 OpenAI/Claude/Gemini 多协议互转与微信 / 飞书 / Telegram bot 接入。</div>
<div class="r-skill-tags">
<span class="r-skill-tag">TypeScript / Bun</span>
<span class="r-skill-tag">MCP</span>
<span class="r-skill-tag">OpenCode 插件</span>
<span class="r-skill-tag">Bot 接口</span>
<span class="r-skill-tag">API 网关</span>
<span class="r-skill-tag">Astro（官网）</span>
</div>
</div>
<div class="r-skill-card">
<h4>传统办公 · 古法办公</h4>
<div class="r-skill-copy">全国计算机等级考试二级 <strong>MS Office</strong> 与 <strong>WPS Office</strong> 双科目完整通过；可在完全无 AI 辅助状态下独立完成 Word、Excel、PPT 全流程办公交付。</div>
<div class="r-skill-tags">
<span class="r-skill-tag">Word</span>
<span class="r-skill-tag">Excel</span>
<span class="r-skill-tag">PPT</span>
<span class="r-skill-tag">WPS</span>
<span class="r-skill-tag">计算机二级</span>
</div>
</div>
</div>
</div>
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
<div class="r-meta">发明专利申请 · 第一发明人 · 实质审查中</div>
</div>
<div class="r-exp-detail">
申请号：202510091154.4 · 云南农业大学 · 2025-05-16 公开 · 2025-06-03 进入实质审查
<br><span style="font-size:0.85rem; color:#64748b;">已公开、可检索，实质审查中——人工智能类专利授权周期较长，法律状态以 CNIPA 最新记录为准。</span>
</div>
</div>
</div>
<div class="r-section">
<div class="r-section-title">📦 开源项目精选</div>
<div class="r-link-note" style="margin-bottom:1.5rem;">
<strong style="color:#1e3a8a;">项目主线：</strong> 围绕 Linxira 开源组织构建科研基础设施生态——主导开发 <strong>Linxira Bio SDK</strong>（本地优先生信平台）与 <strong>Linxira Zeta</strong>（终端编码代理），发起在研的 <strong>Linxira OS</strong> 科研工作站发行版；同时维护 OpenCode 科研编排插件。组织下共 26 个开源仓库，三个主线项目均有独立官网（见各卡片链接）。
<br><br>
<strong style="color:#1e3a8a;">前沿评估：</strong> 跟踪 Proto、PBCNet2.0 等 AI for Science 工具，形成 MCP/Agent 接入评估与技术笔记，不将第三方基准视为自身系统性能。
</div>
<div class="r-grid-3 r-project-grid">
<div class="r-project-card" style="border-color:#bfdbfe; background:#eff6ff;">
<h4><a href="https://github.com/Linxira-OS/linxira-bio-sdk">Linxira Bio SDK</a> <span class="r-badge">主导开发</span></h4>
<div class="r-desc"><strong>本地优先、开箱即用的生信分析平台</strong>：Rust 原生引擎 + 原生 GUI/CLI + agent skills；支持 FASTA / FASTQ / GFF / VCF / BED / CSV / PDB 导入，覆盖质控 → 修剪 → 比对 → 变异 → 富集 → 报告全流程；表格、SVG 图表与交互式结构查看器，可导出 CSV/TSV/JSON/XLSX 及 HTML/PDF 论文级报告；94 个分析能力、28 个 agent skills、中英双语文档；Windows / Debian / Arch 三平台，AGPL-3.0 开源，CI 含 JSON Schema 验证。</div>
<div class="r-links"><a href="https://github.com/Linxira-OS/linxira-bio-sdk" target="_blank">GitHub</a><a href="https://linxira-os.github.io/bio-sdk/zh/" target="_blank">官网 ↗</a></div>
<span class="r-lang">Rust · Python · R · Java</span>
</div>
<div class="r-project-card" style="border-color:#bfdbfe; background:#eff6ff;">
<h4><a href="https://github.com/Linxira-OS/linxira-zeta">Linxira Zeta</a> <span class="r-badge">主导开发</span></h4>
<div class="r-desc"><strong>终端 AI 编码代理（OMP 兼容发行版）</strong>：原生 Rust 引擎驱动，子代理、计划模式、LSP/DAP、事后记忆与 hashline 编辑；主线同步 OMP 上游并移植 Pi 高级能力；提供交互式 TUI、Print/JSON、RPC、SDK 四种运行模式，Web UI 与 CLI 共享持久会话；支持 15+ 模型提供商，可接入微信 / 飞书 / Telegram bot。</div>
<div class="r-links"><a href="https://github.com/Linxira-OS/linxira-zeta" target="_blank">GitHub</a><a href="https://linxira-os.github.io/zeta/zh/" target="_blank">官网 ↗</a></div>
<span class="r-lang">TypeScript · Rust</span>
</div>
<div class="r-project-card">
<h4><a href="https://github.com/Linxira-OS/linxira-os">Linxira OS</a></h4>
<div class="r-desc"><strong>面向理学的 Linux 发行版（在研）</strong>：KDE Plasma 桌面直接基于 Arch 官方仓库构建；双内核（linux + linux-lts）兜底滚动更新，Timeshift 快照 + grub-btrfs 回滚；[linxira] 签名仓库以自有密钥发布 17 个自研工具（Welcome → Config Hub 全链路）；93 款审核软件目录勾选即装；Podman / Distrobox / Apptainer 容器化科研复现与无头模式；中文（Fcitx5）开箱即用。ISO 构建与兼容性验证推进中。</div>
<div class="r-links"><a href="https://github.com/Linxira-OS/linxira-os" target="_blank">GitHub</a><a href="https://linxira-os.github.io/zh/" target="_blank">官网 ↗</a></div>
<span class="r-lang">Arch · Shell · Python</span>
</div>
<div class="r-project-card">
<h4><a href="https://github.com/BOHUYESHAN-APB/openagent-labforge-bio">openagent-labforge-bio</a> <span class="r-badge">主线</span></h4>
<div class="r-desc">OpenCode 科研编排插件：权限分层、计划执行、续跑/审查、会话检查点与 MCP；按需索引 617 个集成技能指令包。</div>
<div class="r-links"><a href="https://github.com/BOHUYESHAN-APB/openagent-labforge-bio" target="_blank">GitHub</a></div>
<span class="r-lang">TypeScript / Bun</span>
</div>
<div class="r-project-card">
<h4><a href="https://github.com/Linxira-OS/extendai-lab-Studio">extendai-lab-Studio</a></h4>
<div class="r-desc">科研控制面原型：OpenCode 生命周期桥、安全检查、本地认证与受限规模统计。</div>
<div class="r-links"><a href="https://github.com/Linxira-OS/extendai-lab-Studio" target="_blank">GitHub</a></div>
<span class="r-lang">Python / TypeScript</span>
</div>
<div class="r-project-card">
<h4><a href="https://github.com/BOHUYESHAN-APB/Buckwheat-seed-quality">Buckwheat-seed-quality</a></h4>
<div class="r-desc">PP-YOLOE+ 荞麦籽粒检测与桌面/批量推理；树莓派 5 的 20 图同机测试中，NCNN CPU 延迟约为 ONNX Runtime CPU 的 1/1.83。</div>
<div class="r-links"><a href="https://github.com/BOHUYESHAN-APB/Buckwheat-seed-quality" target="_blank">GitHub</a></div>
<span class="r-lang">Python / Kotlin</span>
</div>
<div class="r-project-card r-w3">
<h4><a href="https://github.com/BOHUYESHAN-APB/CNN-MicroAI-Colony">CNN-MicroAI-Colony</a></h4>
<div class="r-desc">菌落检测、抑菌圈分析和多端推理原型；5 图小样本工程测试中，平衡版 CPU 延迟由 2539 ms 降至 1884 ms。</div>
<div class="r-links"><a href="https://github.com/BOHUYESHAN-APB/CNN-MicroAI-Colony" target="_blank">GitHub</a></div>
<span class="r-lang">Python / ONNX</span>
</div>
</div>
</div>
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
<div class="r-section">
<div class="r-section-title">📊 关键数据</div>
<div class="r-stats">
<div class="r-stat"><div class="r-num">1</div><div class="r-label">IJMS 期刊论文</div></div>
<div class="r-stat"><div class="r-num">94</div><div class="r-label">Bio SDK 分析能力</div></div>
<div class="r-stat"><div class="r-num">28</div><div class="r-label">Bio SDK agent skills</div></div>
<div class="r-stat"><div class="r-num">1</div><div class="r-label">第一发明人专利申请</div></div>
<div class="r-stat"><div class="r-num">24</div><div class="r-label">DWF4 分析样本</div></div>
<div class="r-stat"><div class="r-num">617</div><div class="r-label">集成索引的技能指令包</div></div>
<div class="r-stat"><div class="r-num">17</div><div class="r-label">Linxira 自研签名工具</div></div>
<div class="r-stat"><div class="r-num">26</div><div class="r-label">Linxira-OS 开源仓库</div></div>
</div>
</div>
<div class="r-section">
<div class="r-section-title">🎓 教育</div>
<div class="r-exp-item">
<div class="r-exp-head">
<div class="r-name">云南农业大学</div>
<div class="r-meta">本科在读 · 2027届 · 2027.06 毕业</div>
</div>
<div class="r-exp-detail">生物技术专业</div>
</div>
</div>
<div class="r-section">
<div class="r-section-title">📌 求职信息</div>
<div class="r-exp-item">
<div class="r-exp-head">
<div class="r-name">生物信息工程师 / 生物信息学分析</div>
<div class="r-meta">首选</div>
</div>
<div class="r-exp-detail">面向 RNA-seq、组学分析、公共数据库挖掘与生信流程开发，交付可复现分析与自动化报告。</div>
</div>
<div class="r-exp-item">
<div class="r-exp-head">
<div class="r-name">AI Agent 开发工程师 / 科研软件工程师</div>
</div>
<div class="r-exp-detail">科研 Agent 编排（OpenCode/MCP）、生信工具链与 SDK 开发（Rust/TypeScript）、实验室信息化与自动化工作流。</div>
</div>
<div class="r-exp-item">
<div class="r-exp-head">
<div class="r-name">AI 制药（AIDD）算法 / 计算生物学</div>
</div>
<div class="r-exp-detail">药物虚拟筛选、分子对接与动力学管线、网络药理学、蛋白质结构预测（AlphaFold）。</div>
</div>
<div class="r-exp-item">
<div class="r-exp-head">
<div class="r-name">分析技术员 · 分子岗</div>
</div>
<div class="r-exp-detail">核酸提取、qRT-PCR、分子克隆与组培，分子检测与分析。</div>
</div>
<div class="r-exp-item">
<div class="r-exp-head">
<div class="r-name">分析技术员 · 理化岗</div>
</div>
<div class="r-exp-detail">菌落计数、形态学鉴别、抑菌圈测量，样品检测与报告。</div>
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
<div class="r-section">
<div class="r-section-title">🤝 组织参与</div>
<ul class="r-org-list">
<li class="r-org-item"><strong>Linxira OS</strong> — 发起并推进面向理学的 Linux 发行版（Arch 基线、双内核、[linxira] 签名仓库、容器化科研复现）；主导开发 Bio SDK 与 Zeta，组织下 26 个开源仓库 · <a href="https://linxira-os.github.io/zh/" target="_blank">官网</a></li>
<li class="r-org-item"><strong>YeShanBoYun Studio</strong> — 组织成员，参与 NeuroPlex-Nexus 等项目</li>
<li class="r-org-item"><strong>openagent-labforge-bio</strong> — 主线项目，持续开发维护</li>
<li class="r-org-item"><strong>OpenI 启智社区</strong> — 公开保存部分 NPU/GPU 任务与模型记录</li>
</ul>
</div>
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
<div class="r-section">
<div class="r-section-title">📋 在研项目与预期成果</div>
<div class="r-exp-item">
<div class="r-exp-head">
<div class="r-name">AI 驱动药物虚拟筛选自动化管线</div>
<div class="r-meta">2026.06 — 持续 · 前沿方法集成</div>
</div>
<div class="r-exp-detail">设计靶点检索、网络药理学、分子对接、分子动力学与报告生成的 Agent 工作流；正在评估 <span class="r-hl">PBCNet2.0</span> 等亲和力预测方法的接入可行性，尚未形成实验验证或性能结论。</div>
</div>
<div class="r-exp-item">
<div class="r-exp-head">
<div class="r-name">荞麦矮化基因挖掘与功能分析</div>
<div class="r-meta">在研 · 拟整理为预印本</div>
</div>
<div class="r-exp-detail">整合 24 样本 RNA-seq、同源与局部共线性、共表达、启动子、系统发育和结构预测证据；功能验证待完成。</div>
</div>
<div class="r-exp-item">
<div class="r-exp-head">
<div class="r-name">微生物小目标检测算法改进</div>
<div class="r-meta">在研 · 拟整理为预印本</div>
</div>
<div class="r-exp-detail">围绕微生物菌落小目标检测，持续比较 <span class="r-hl">PP-YOLO</span> 系列训练与学习率策略；已搭建 Ascend/OpenI/MindSpore 迁移脚手架，完整训练与评测结果待补齐。</div>
</div>
<div class="r-exp-item">
<div class="r-exp-head">
<div class="r-name">Python / R 性能热点跨语言迁移</div>
<div class="r-meta">自学 · 原型验证</div>
</div>
<div class="r-exp-detail">借助 AI 编程辅助梳理文件解析、表格处理和计算热点，尝试以 Rust/C++ 重写受解释器与单线程限制的模块；目前不声明统一性能结论。</div>
</div>
</div>
<div class="r-section">
<div class="r-section-title">🔗 全部链接 · 一页直达</div>
<div class="r-grid-3">
<div class="r-link-group">
<h4>简历版本</h4>
<ul>
<li><a href="/HTML/resume-lab.html" target="_blank">实验 / 检测岗 · A4</a></li>
<li><a href="/HTML/resume-tech.html" target="_blank">生信 / AI 工程岗 · A4</a></li>
<li><a href="/HTML/resume-full.html" target="_blank">综合海投 · A4</a></li>
<li><a href="/HTML/resume-archived-01.html" target="_blank">归档 · 科研支持定位</a></li>
<li><a href="/HTML/resume-archived-02.html" target="_blank">归档 · 工程交付定位</a></li>
</ul>
</div>
<div class="r-link-group">
<h4>GitHub</h4>
<ul>
<li><a href="https://github.com/BOHUYESHAN-APB" target="_blank">BOHUYESHAN-APB（主账号）</a></li>
<li><a href="https://github.com/Linxira-OS" target="_blank">Linxira-OS（开源组织 · 26 仓库）</a></li>
<li><a href="https://github.com/BoHuYeShan" target="_blank">BoHuYeShan（个人）</a></li>
</ul>
</div>
<div class="r-link-group">
<h4>项目官网</h4>
<ul>
<li><a href="https://linxira-os.github.io/zh/" target="_blank">Linxira OS（科研工作站发行版）</a></li>
<li><a href="https://linxira-os.github.io/zeta/zh/" target="_blank">Linxira Zeta（终端编码代理）</a></li>
<li><a href="https://linxira-os.github.io/bio-sdk/zh/" target="_blank">Linxira Bio SDK（生信分析平台）</a></li>
</ul>
</div>
<div class="r-link-group">
<h4>主要仓库 · Linxira-OS</h4>
<ul>
<li><a href="https://github.com/Linxira-OS/linxira-bio-sdk" target="_blank">linxira-bio-sdk</a> · <a href="https://github.com/Linxira-OS/linxira-zeta" target="_blank">linxira-zeta</a></li>
<li><a href="https://github.com/Linxira-OS/linxira-os" target="_blank">linxira-os</a> · <a href="https://github.com/Linxira-OS/extendai-lab-Studio" target="_blank">extendai-lab-Studio</a></li>
<li><a href="https://github.com/Linxira-OS/linxira-pulse" target="_blank">linxira-pulse</a>（系统级 AI 助手）</li>
<li><a href="https://github.com/Linxira-OS/linxira-skills" target="_blank">linxira-skills</a> · <a href="https://github.com/Linxira-OS/linxira-catalog" target="_blank">linxira-catalog</a></li>
<li><a href="https://github.com/Linxira-OS/linxira-welcome" target="_blank">linxira-welcome</a> · <a href="https://github.com/Linxira-OS/linxira-config-hub" target="_blank">linxira-config-hub</a></li>
</ul>
</div>
<div class="r-link-group">
<h4>主要仓库 · 个人</h4>
<ul>
<li><a href="https://github.com/BOHUYESHAN-APB/openagent-labforge-bio" target="_blank">openagent-labforge-bio</a></li>
<li><a href="https://github.com/BOHUYESHAN-APB/Buckwheat-seed-quality" target="_blank">Buckwheat-seed-quality</a> · <a href="https://github.com/BOHUYESHAN-APB/CNN-MicroAI-Colony" target="_blank">CNN-MicroAI-Colony</a></li>
<li><a href="https://github.com/BOHUYESHAN-APB/MicroAGI-Agri" target="_blank">MicroAGI-Agri</a> · <a href="https://github.com/BOHUYESHAN-APB/extendai-lab" target="_blank">extendai-lab</a></li>
<li><a href="https://github.com/BOHUYESHAN-APB/lcu-ai-mod" target="_blank">lcu-ai-mod</a>（AI Minecraft 伴侣）</li>
</ul>
</div>
<div class="r-link-group">
<h4>论文与学术</h4>
<ul>
<li><a href="https://doi.org/10.3390/ijms27135740" target="_blank">IJMS 论文（DOI: 10.3390/ijms27135740）</a></li>
<li><a href="https://orcid.org/0009-0002-8426-0610" target="_blank">ORCID 主页</a></li>
<li><a href="https://openi.pcl.ac.cn/bhys" target="_blank">OpenI 启智社区</a></li>
</ul>
</div>
<div class="r-link-group r-w3">
<h4>博客与联系</h4>
<ul>
<li><a href="https://bohuyeshan.top" target="_blank">个人博客 bohuyeshan.top</a></li>
<li>邮箱：bohuyeshan@163.com（主）· bohuyeshan@gmail.com</li>
</ul>
</div>
</div>
</div>
<div class="r-print-section">
<div style="display:flex;justify-content:center;flex-wrap:wrap;gap:0.8rem;">
<a href="/HTML/resume-lab.html" target="_blank">
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
获取印刷版简历 (实验 / 检测岗 · A4)
</a>
<a href="/HTML/resume-tech.html" target="_blank">
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
获取印刷版简历 (生信 / AI 工程岗 · A4)
</a>
<a href="/HTML/resume-full.html" target="_blank">
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
获取印刷版简历 (综合海投 · A4)
</a>
</div>
<div class="r-print-hint">A4 双面打印 · 左右两页展开即完整简历 · 三个版本对应不同投递场景，按岗位选择；归档旧版请使用上方「简历版本」下拉菜单</div>
</div>
</div>
