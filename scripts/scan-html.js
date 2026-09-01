'use strict';
// 最终渲染审计：检查文章正文各种未渲染 markdown 残留
// 用法：node scripts/scan-html.js（需先 npx hexo generate）
const fs = require('fs');
const path = require('path');

// 允许从任意 cwd 运行：定位到仓库根
process.chdir(path.join(__dirname, '..'));

function walk(d, o = []) {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    const p = path.join(d, e.name);
    if (e.isDirectory()) walk(p, o);
    else if (e.name === 'index.html') o.push(p);
  }
  return o;
}

const files = walk('public').filter(p => /20\d\d/.test(p) && !/HTML|fun|buckwheat/.test(p));
const findings = [];

for (const f of files) {
  const h = fs.readFileSync(f, 'utf8');
  const am = h.match(/<(?:div|article)[^>]*id="article-container"[^>]*>/);
  if (!am) continue;
  const body = h.slice(am.index);
  const cut = body.indexOf('<div class="pagination-related">');
  let clean = body.slice(0, cut > 0 ? cut : undefined)
    .replace(/<(pre|script|style)[\s\S]*?<\/\1>/g, '')
    .replace(/<code[\s\S]*?<\/code>/g, '')
    .replace(/<div class="mermaid">[\s\S]*?<\/div>/g, '');

  const rel = path.relative('public', f);
  const add = (type, m) => findings.push(`${rel} | ${type} | ...${m.replace(/\s+/g, ' ').slice(0, 80)}`);

  for (const m of clean.match(/\*\*/g) || []) { /* 已确认 0 */ }
  // 裸单星成对（疑似斜体失败）
  let m;
  const re1 = /[^<>]*\*[^*\s][^<>]*?\*[^<>]*/g;
  while ((m = re1.exec(clean))) {
    const t = m[0];
    // 排除正常的多星组合
    if (!t.includes('**')) add('单星对', t);
  }
  // 原始链接
  const re2 = /[^<>]*\[[^\]\n]{1,60}\]\([^)]{1,80}\)[^<>]*/g;
  while ((m = re2.exec(clean))) add('原始链接', m[0]);
  // 删除线
  const re3 = /[^<>]*~~[^<>]*/g;
  while ((m = re3.exec(clean))) add('~~', m[0]);
  // 下划线强调
  const re4 = /[^<>]*__[^<>]{1,40}__[^<>]*/g;
  while ((m = re4.exec(clean))) add('__对__', m[0]);
  // 表格线出现在文本里
  const re5 = /<p>[^<]*\|[^<]*<\/p>/g;
  while ((m = re5.exec(clean))) add('段落含表格线', m[0]);
  // 原始标题符号
  const re6 = /<p>\s*#{1,6} /g;
  while ((m = re6.exec(clean))) add('段落井号', clean.slice(m.index, m.index + 80));
}

console.log(`审计 ${files.length} 个文章页，疑似问题 ${findings.length} 处`);
findings.forEach(x => console.log(x));
