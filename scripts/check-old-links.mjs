// CI gate: every /old/... reference in post/page sources must resolve to a
// real file inside the composed dist. Fails the build on any dead link.
// Usage: node scripts/check-old-links.mjs <dist-dir>
import { readFileSync, readdirSync, existsSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const dist = process.argv[2];
if (!dist) {
  console.error("usage: node scripts/check-old-links.mjs <dist-dir>");
  process.exit(1);
}

const refs = new Set();
const scan = dir => {
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) scan(p);
    else if (/\.mdx?$/.test(e.name)) {
      const text = readFileSync(p, "utf8");
      for (const m of text.matchAll(/[("'`]\s*(\/old\/[^)"'\s<>]+)/g))
        refs.add(m[1].replace(/[.,;:]+$/, ""));
    }
  }
};
scan(join(ROOT, "src/content"));

const missing = [];
for (const ref of refs) {
  const rel = ref.slice("/old/".length);
  const base = join(dist, "old", rel);
  const hit =
    existsSync(base) ||
    existsSync(join(base, "index.html")) ||
    existsSync(`${base}.html`);
  if (!hit) missing.push(ref);
}

console.log(`/old/ references checked: ${refs.size}, missing: ${missing.length}`);
if (missing.length) {
  for (const m of missing) console.log("  MISSING " + m);
  process.exit(1);
}
