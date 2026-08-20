'use strict'

/**
 * Server-side KaTeX rendering.
 *
 * hexo-renderer-marked does not process LaTeX: it turns underscores into
 * <em>, strips backslashes, etc. We protect math with alphanumeric tokens
 * BEFORE markdown rendering and replace them with rendered KaTeX HTML AFTER
 * rendering. Only runs for posts/pages that opt in via `katex: true`.
 */

const katex = require('katex')

let seq = 0
const mathBlocks = new Map()

function protect (data) {
  if (!data.katex) return
  seq = 0
  mathBlocks.clear()

  let content = data.content

  // Mask fenced code blocks so `$` inside them is never treated as math
  const codeBlocks = []
  content = content.replace(/```[\s\S]*?```/g, m => {
    const token = `KXCODE${seq++}`
    codeBlocks.push([token, m])
    return token
  })

  // Display math $$...$$
  content = content.replace(/\$\$([\s\S]+?)\$\$/g, (m, math) => {
    const token = `KXBLK${seq++}`
    mathBlocks.set(token, { math: math.trim(), display: true })
    return token
  })

  // Inline math $...$ (single line, no dollars inside)
  content = content.replace(/(^|[^\\$])\$([^$\n]+?)\$/g, (m, pre, math) => {
    const token = `KXINL${seq++}`
    mathBlocks.set(token, { math, display: false })
    return pre + token
  })

  // Restore code blocks (tokens are alphanumeric, no `$`, safe)
  for (const [token, block] of codeBlocks) {
    content = content.replace(token, block)
  }

  data.content = content
}

function restore (data) {
  if (!data.katex) return
  let content = data.content

  for (const [token, { math, display }] of mathBlocks) {
    const html = katex.renderToString(math, { displayMode: display, throwOnError: false })
    content = content.split(token).join(html)
  }

  data.content = content
}

hexo.extend.filter.register('before_post_render', protect)
hexo.extend.filter.register('after_post_render', restore, 5)