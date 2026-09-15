// One-shot migration: Hexo posts -> AstroPaper content collection.
// Usage: node scripts/migrate.mjs <hexo-source/_posts-dir>
//
// - front-matter: title/date/tags -> title/pubDatetime/tags (+ derived description)
// - {% hideToggle %} Hexo tags -> <details><summary>
// - site-absolute refs rewritten into the /old/ archive namespace
//   (](/img/, ](/lib/, "pdb" attrs, and ](/2026/... links NOT pointing at a
//   surviving post)
// - chart-series posts get a footer link to their archived original
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join, dirname, basename } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const OUT = join(ROOT, "src/content/posts");
const hexoPosts = process.argv[2];
if (!hexoPosts) {
  console.error("usage: node scripts/migrate.mjs <hexo-source/_posts-dir>");
  process.exit(1);
}

const SOURCES = [
  "2026-08-05-01-生信工作站的底座之争-滚动内核还是LTS内核.md",
  "2026-08-20-01-训练大模型教会我的事-后来都用在了生物医药上.md",
  "2026-08-21-01-LLM的数据清洗是减法-AI制药的数据清洗是手术.md",
  "2026-08-22-02-看着百花齐放其实就几个祖宗-主流Agent体系对照.md",
  "2026-09-10-01-群体重测序分析入门-从FASTQ到选择清除.md",
  "2026-09-12-01-生信图表大全第一篇-41张图的坐标轴参数与绘制语言.md",
  "2026-09-12-02-生信图表大全第二篇-群体遗传比较基因组与单细胞的33张图.md",
  "2026-09-12-03-生信图表大全第三篇-从测序QC到空间组学的29张图.md",
  "2026-09-12-04-生信图表大全第四篇-从蛋白互作到AI多组学的30张图.md",
  "2026-09-12-05-生信图表大全第五篇-蛋白结构变异与表达验证的40张图.md",
  "2026-09-12-08-生信图表大全第六篇-用真实公开数据画的22张图.md",
  "2026-09-13-01-生信图表大全第七篇-把190张图重画成Nature风格.md",
];
const CHART_POSTS = new Set(SOURCES.slice(5));
const FEATURED = new Set([
  "2026-09-13-01-生信图表大全第七篇-把190张图重画成Nature风格.md",
]);

function parseScalar(v) {
  v = v.trim();
  // flow-style YAML list: [a, b, c]
  if (v.startsWith("[") && v.endsWith("]")) {
    return v
      .slice(1, -1)
      .split(",")
      .map(t => t.trim().replace(/^["']|["']$/g, ""))
      .filter(Boolean);
  }
  return v.replace(/^["']|["']$/g, "");
}

function parseFrontMatter(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!m) return { fm: {}, body: text };
  const fm = {};
  let curKey = null;
  for (const line of m[1].split(/\r?\n/)) {
    const item = line.match(/^\s*-\s+(.*)$/);
    if (item && curKey) {
      fm[curKey] = [...(fm[curKey] || []), parseScalar(item[1])];
      continue;
    }
    const kv = line.match(/^([A-Za-z_][\w-]*):\s*(.*)$/);
    if (kv) {
      curKey = kv[1];
      const v = kv[2].trim();
      fm[curKey] = v === "" ? null : parseScalar(v);
    }
  }
  return { fm, body: text.slice(m[0].length) };
}

const safeDecode = s => {
  try {
    return decodeURIComponent(s);
  } catch {
    return s;
  }
};

function describe(body, title) {
  for (const raw of body.split(/\r?\n/)) {
    const line = raw.trim();
    if (!line) continue;
    if (/^(#|!\[|>|\{%|<|```|\||---)/.test(line)) continue;
    const text = line
      .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1")
      .replace(/[*`_~]/g, "")
      .trim();
    if (text.length < 8) continue;
    return text.length > 110 ? text.slice(0, 108) + "…" : text;
  }
  return title;
}

const leftovers = [];

// links between surviving posts keep their root URL; the survivor set is
// exactly the set of posts this script emits
const survivorPaths = new Set(
  SOURCES.map(f => {
    const slug = basename(f, ".md");
    const dm = slug.match(/^(\d{4})-(\d{2})-(\d{2})/);
    return dm ? `/${dm[1]}/${dm[2]}/${dm[3]}/${slug}/` : null;
  }).filter(Boolean)
);

let ok = 0;

for (const file of SOURCES) {
  const raw = readFileSync(join(hexoPosts, file), "utf8");
  const { fm, body: rawBody } = parseFrontMatter(raw);
  const slug = basename(file, ".md");
  const dm = slug.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (!dm) {
    console.error(`skip (no date in filename): ${file}`);
    continue;
  }
  const [, y, mo, d] = dm;
  const seq = slug.match(/^\d{4}-\d{2}-\d{2}-(\d{2})-/);
  const hour = String(7 + (seq ? parseInt(seq[1], 10) : 5)).padStart(2, "0");
  const postPath = `/${y}/${mo}/${d}/${slug}/`;

  let body = rawBody;

  // Hexo tag plugins -> plain HTML
  body = body.replace(
    /^\{%\s*hideToggle\s+(.+?)\s*%\}[ \t]*$/gm,
    (_m, t) => `<details>\n<summary>${t}</summary>\n`
  );
  body = body.replace(/^\{%\s*endhideToggle\s*%\}[ \t]*$/gm, "</details>");
  body = body.replace(/(<\/summary>)\n(?!\n)/g, "$1\n\n");
  body = body.replace(/([^\n])\n<\/details>/g, "$1\n\n</details>");

  // static assets -> /old/ namespace
  body = body.replaceAll("](/img/", "](/old/img/");
  body = body.replaceAll("](/lib/", "](/old/lib/");
  body = body.replace(/(['"])\/lib\/pdb\//g, "$1/old/lib/pdb/");

  // internal post links -> /old/, unless the target itself survived
  body = body.replace(/\]\((\/20\d\d\/[^)\s]+)\)/g, (m, p1) => {
    const dec = safeDecode(p1);
    const norm = dec.endsWith("/") ? dec : `${dec}/`;
    const selfPath = safeDecode(postPath);
    if (norm === selfPath) return `](${p1})`;
    if (survivorPaths.has(norm)) return m;
    return `](/old/${p1})`;
  });

  // audit: any remaining site-absolute link that was not converted
  for (const m of body.matchAll(/\]\((\/[^)s][^)]*)\)/g)) {
    if (!m[1].startsWith("/old/") && !/^\/20\d\d\/[^/]+\/[^/]+\/[^/]+\//.test(m[1]))
      leftovers.push(`${file}: ${m[1]}`);
  }

  // chart series: link back to the archived original
  if (CHART_POSTS.has(file)) {
    body += `\n\n---\n\n> **原文存档**：本文初版发布于旧站（Butterfly 主题）。如遇图表、代码高亮或 3D 交互显示异常，请查阅 [完整存档版](${postPath.replace(/^\/(.*)\/$/, "/old/$1")})。\n`;
  }

  const title = (fm.title || "").replace(/^["']|["']$/g, "");
  // categories fold into tags so the old taxonomy stays browsable
  const CATEGORY_ALIASES = { 生信图表大全: "图表大全" };
  const TAG_ALIASES = { "图表可视化": "科研绘图", "AI 制药": "AI制药", "Nature 风格": "科研绘图", "方法选型": "技术选型" };
  const DROP_TAGS = new Set(["基因", "AI", "真实数据"]);
  const rawTags = Array.isArray(fm.tags) ? fm.tags : fm.tags ? [fm.tags] : [];
  const rawCats = Array.isArray(fm.categories)
    ? fm.categories
    : fm.categories
      ? [fm.categories]
      : [];
  const tags = [
    ...new Set(
      [...rawTags, ...rawCats.map(c => CATEGORY_ALIASES[c] || c)]
        .map(t => String(t).trim())
        .filter(Boolean)
        .map(t => TAG_ALIASES[t] || t)
        .filter(t => !DROP_TAGS.has(t))
    ),
  ];
  const fmOut = [
    "---",
    `title: ${JSON.stringify(title)}`,
    `description: ${JSON.stringify(describe(rawBody, title))}`,
    `pubDatetime: ${y}-${mo}-${d} ${hour}:00:00`,
    'timezone: "Asia/Shanghai"',
    tags.length ? `tags: [${tags.map(t => JSON.stringify(t)).join(", ")}]` : null,
    FEATURED.has(file) ? "featured: true" : null,
    "---",
  ]
    .filter(Boolean)
    .join("\n");

  const outDir = join(OUT, y, mo, d);
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, `${slug}.md`), `${fmOut}\n\n${body}`);
  ok++;
  console.log(`ok ${postPath}`);
}

console.log(`\nmigrated ${ok}/${SOURCES.length} posts`);
if (leftovers.length) {
  console.log("\nleftover site-absolute links (review):");
  for (const l of leftovers) console.log("  " + l);
}
