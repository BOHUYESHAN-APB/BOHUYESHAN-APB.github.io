// One-shot: convert the AstroPaper-era migrated posts (bohuyeshan-new repo)
// into Astro Theme Pure's blog collection.
// Usage: node scripts/migrate-pure.mjs <bohuyeshan-new-src-content-posts>
//
// Front-matter mapping: pubDatetime -> publishDate; timezone dropped;
// title/description/tags carried over; featured dropped (Pure has no flag).
// Body text is already final (paths point at /old/, details converted).
import { readFileSync, writeFileSync, mkdirSync, readdirSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..')
const OUT = join(ROOT, 'src/content/blog')
const srcDir = process.argv[2]
if (!srcDir) {
  console.error('usage: node scripts/migrate-pure.mjs <converted-posts-dir>')
  process.exit(1)
}

function walk(dir) {
  const out = []
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, e.name)
    if (e.isDirectory()) out.push(...walk(p))
    else if (e.name.endsWith('.md')) out.push(p)
  }
  return out
}

const files = walk(srcDir)
let ok = 0
for (const file of files) {
  const raw = readFileSync(file, 'utf8')
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/)
  if (!m) continue
  const fm = {}
  for (const line of m[1].split(/\r?\n/)) {
    const kv = line.match(/^([A-Za-z_][\w-]*):\s*(.*)$/)
    if (kv) fm[kv[1]] = kv[2].trim()
  }
  const body = raw.slice(m[0].length)
  const publishDate = (fm.pubDatetime || '').replace(/"/g, '')
  const outFm = [
    '---',
    `title: ${fm.title || "''"}`,
    `description: ${fm.description || "''"}`,
    `publishDate: ${publishDate || '2026-09-15'}`,
    `tags: ${fm.tags || '[]'}`,
    '---'
  ].join('\n')
  const rel = file.split('posts')[1].replace(/^[\\/]/, '')
  const out = join(OUT, rel)
  mkdirSync(dirname(out), { recursive: true })
  writeFileSync(out, `${outFm}\n${body}`)
  ok++
}
console.log(`migrated ${ok}/${files.length} posts into Pure blog collection`)
