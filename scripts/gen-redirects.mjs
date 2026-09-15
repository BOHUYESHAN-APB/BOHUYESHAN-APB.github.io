// Generates meta-refresh stub pages so pre-migration URLs keep working:
//   bohuyeshan.top/<year>/<month>/<day>/<slug>/  ->  /old/<same path>
// Usage: node scripts/gen-redirects.mjs <old-hexo-public-dir>
//
// Surviving posts are skipped (they exist natively at the same URL). A handful
// of top-level archive pages (resume, gallery, ...) get stubs too.
import { readdirSync, existsSync, mkdirSync, writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const OUT = join(ROOT, "public");
const oldPublic = process.argv[2];
if (!oldPublic) {
  console.error("usage: node scripts/gen-redirects.mjs <old-public-dir>");
  process.exit(1);
}

// survivor paths = the migrated post tree under src/content/posts
const survivors = new Set();
walk(join(ROOT, "src/content/posts"), []).forEach(slugPath =>
  survivors.add(`/${slugPath}/`)
);
function walk(dir, prefix) {
  const out = [];
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = [...prefix, e.name];
    if (e.isDirectory()) out.push(...walk(join(dir, e.name), p));
    else if (e.name.endsWith(".md")) out.push(p.join("/").replace(/\.md$/, ""));
  }
  return out;
}

const stubs = [];
for (const y of readdirSync(oldPublic)) {
  if (!/^20\d\d$/.test(y)) continue;
  for (const mo of readdirSync(join(oldPublic, y))) {
    for (const d of readdirSync(join(oldPublic, y, mo))) {
      for (const slug of readdirSync(join(oldPublic, y, mo, d))) {
        if (!existsSync(join(oldPublic, y, mo, d, slug, "index.html"))) continue;
        const rel = `/${y}/${mo}/${d}/${slug}/`;
        if (survivors.has(rel)) continue;
        stubs.push(rel);
      }
    }
  }
}

// top-level archive pages worth keeping reachable
const TOP_PAGES = [
  "resume",
  "Friends",
  "Gallery",
  "Talks",
  "books",
  "movies",
  "music",
  "fun",
  "buckwheat-project",
  "HTML",
  "CNN-MICROAI-COLONY",
];
for (const name of TOP_PAGES) {
  if (existsSync(join(oldPublic, name, "index.html"))) stubs.push(`/${name}/`);
}

let n = 0;
for (const rel of stubs) {
  const target = `/old${rel}`;
  const file = join(OUT, rel.replace(/^\//, ""), "index.html");
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(
    file,
    `<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>内容已归档迁移</title>
<link rel="canonical" href="${target}">
<meta http-equiv="refresh" content="0; url=${target}">
<style>body{font-family:system-ui,sans-serif;max-width:40rem;margin:4rem auto;padding:0 1rem;color:#444}a{color:#06c}</style>
</head>
<body>
<p>这篇内容已归档迁移至旧站：<a href="${target}">${target}</a></p>
<script>location.replace(${JSON.stringify(target)});</script>
</body>
</html>
`
  );
  n++;
}
console.log(`generated ${n} redirect stubs (skipped ${survivors.size} survivors)`);
