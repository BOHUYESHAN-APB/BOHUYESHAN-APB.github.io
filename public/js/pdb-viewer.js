/* 生信图表大全第五篇：内嵌 3Dmol 蛋白结构查看器（点击加载 + 全页独占）
 * 用法：文章里放 <div class="pdb3d" data-cfg='{...}' style="height:420px"></div>
 * cfg: {pdb:"/lib/pdb/6a15.pdb", bg:"white",
 *        styles:[{sel:{}, style:{cartoon:{color:'spectrum'}}}, ...],
 *        resLabels:{sel:{...}}, zoom:{sel:{...}}}
 * 行为：页面加载时只摆「点击加载」按钮（不建 WebGL 上下文，不拉结构文件）；
 *       点击后才 fetch PDB 并建 viewer。
 * 独占：同一时间全页只保留一个活着的 3D 视图——打开新的会自动销毁上一个
 *       （WEBGL_lose_context 释放上下文 + 移除 canvas + 恢复按钮），否则多
 *       个 WebGL 上下文同时活着会把页面拖卡。
 * 位置：创建 viewer 前把容器设为 position:relative + overflow:hidden，
 *       canvas 绝对定位锚在容器内部——否则 3Dmol 的 canvas 会锚到文档顶。
 * 安全：pdb 路径只允许本站相对路径（拒绝 .. 与绝对 URL），不向第三方发请求。
 */
(function () {
  'use strict';

  var active = null;      // 当前已加载的视图 { el, viewer }
  var controller = null;  // 进行中的 fetch（切走时中断）

  function makeButton(el) {
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.textContent = '▶ 点击加载 3D 视图（左键拖拽旋转 · 滚轮缩放 · 右键平移）';
    btn.title = '同一时间只保留一个 3D 视图：打开新的会自动关闭上一个';
    btn.setAttribute('style',
      'display:block;margin:' + Math.max(0, (el.clientHeight || 420) / 2 - 22)
      + 'px auto;padding:11px 22px;font-size:14px;cursor:pointer;'
      + 'border:1px solid #c8ced6;border-radius:22px;background:#fff;'
      + 'color:#45506b');
    btn.addEventListener('click', function () { load(el); });
    el.appendChild(btn);
  }

  function arm(el) {
    if (el.__pdb3dDone) return;
    el.__pdb3dDone = true;
    var cfg;
    try { cfg = JSON.parse(el.getAttribute('data-cfg')); }
    catch (e) {
      el.textContent = 'data-cfg 解析失败';
      return;
    }
    var src = String(cfg.pdb || '');
    if (!/^\/[A-Za-z0-9_\-./]+\.pdb$/.test(src) || src.indexOf('..') >= 0) {
      el.textContent = '无效的结构文件路径（仅允许本站相对路径）';
      return;
    }
    el.__cfg = cfg;
    el.__src = src;
    makeButton(el);
  }

  function closeActive() {
    if (!active) return;
    var el = active.el;
    try {
      var cv = el.querySelector('canvas');
      if (cv) {
        var gl = cv.getContext('webgl2') || cv.getContext('webgl') ||
                 cv.getContext('experimental-webgl');
        var ext = gl && gl.getExtension('WEBGL_lose_context');
        if (ext) ext.loseContext();   // 真正释放 WebGL 上下文
      }
    } catch (e) {}
    try { if (active.viewer) active.viewer.clear(); } catch (e) {}
    el.innerHTML = '';
    makeButton(el);                    // 旧容器恢复成按钮，随时可再打开
    active = null;
  }

  function load(el) {
    if (active && active.el === el) return;
    closeActive();
    if (controller) controller.abort();
    controller = new AbortController();
    var cfg = el.__cfg, src = el.__src;
    el.textContent = '正在加载结构 ' + src.split('/').pop() + ' …';
    fetch(src, { signal: controller.signal }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.text();
    }).then(function (text) {
      if (typeof $3Dmol === 'undefined') throw new Error('3Dmol 未加载');
      while (el.firstChild) el.removeChild(el.firstChild);
      // 关键：容器必须是定位元素，否则 3Dmol 的绝对定位 canvas 会飞到文档顶
      el.style.position = 'relative';
      el.style.overflow = 'hidden';
      var viewer = $3Dmol.createViewer(el, {
        backgroundColor: cfg.bg || 'white'
      });
      viewer.addModel(text, 'pdb');
      (cfg.styles || []).forEach(function (s) {
        viewer.addStyle(s.sel || {}, s.style || {});
      });
      if (cfg.resLabels) viewer.addResLabels(cfg.resLabels.sel || {});
      if (cfg.zoom && cfg.zoom.sel) viewer.zoomTo(cfg.zoom.sel);
      else viewer.zoomTo();
      viewer.render();
      viewer.resize();
      var cv = el.querySelector('canvas');
      if (cv) {
        cv.style.position = 'absolute';
        cv.style.left = '0';
        cv.style.top = '0';
      }
      active = { el: el, viewer: viewer };
    }).catch(function (e) {
      if (e && e.name === 'AbortError') {   // 被新视图切走：恢复按钮即可
        el.innerHTML = '';
        makeButton(el);
        return;
      }
      el.innerHTML = '<div style="padding:24px;color:#c33;font-size:14px;'
        + 'text-align:center">结构加载失败：' + e.message
        + '<br>可从 RCSB PDB 下载后本地查看，静态版见本节上方配图。</div>';
    });
  }

  function boot() {
    if (window.__pdb3dBooted) return;
    window.__pdb3dBooted = true;
    var divs = Array.prototype.slice.call(document.querySelectorAll('.pdb3d'));
    if (!divs.length) return;
    if (typeof $3Dmol === 'undefined') {
      divs.forEach(function (el) {
        el.innerHTML = '<div style="padding:24px;color:#888;font-size:14px;'
          + 'text-align:center">3D 渲染库未加载（需要 JavaScript）。静态版图见本节上方配图。</div>';
      });
      return;
    }
    divs.forEach(arm);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
  window.addEventListener('load', boot);
})();
