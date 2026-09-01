'use strict'

/**
 * CJK 强调分隔符自动修复
 *
 * 背景：marked（hexo-renderer-marked）遵循 CommonMark 侧翼规则，
 *   ** 前是标点且后是汉字/字母 → 无法闭合；前是汉字/字母且后是标点 → 无法开启。
 *   因此「**句子。**后续」「而是**"引用"**——」这类中文写法会原样输出星号。
 * 修复：把紧贴分隔符的一个标点移到分隔符另一侧，视觉几乎无差、渲染恢复。
 * 安全性：只处理成对 ** 且跳过代码块/行内代码/表格竖线；奇数个 ** 的段落不动。
 */

const isWord = c => /\p{L}|\p{N}/u.test(c)
const isPunct = c => /\p{P}|\p{S}/u.test(c)

function fixParagraph (para) {
  const idxs = []
  let i = para.indexOf('**')
  while (i !== -1) { idxs.push(i); i = para.indexOf('**', i + 2) }
  if (idxs.length === 0 || idxs.length % 2 !== 0) return para

  const edits = []
  for (let k = 0; k < idxs.length; k += 2) {
    const open = idxs[k]
    const close = idxs[k + 1]
    if (close === open + 2) continue

    const beforeOpen = open > 0 ? para[open - 1] : ''
    const afterOpen = para[open + 2] || ''
    if (beforeOpen && isWord(beforeOpen) && afterOpen && isPunct(afterOpen) && afterOpen !== '|') {
      edits.push({ pos: open, remove: 3, insert: afterOpen + '**' })
    }

    const beforeClose = para[close - 1] || ''
    const afterClose = para[close + 2] || ''
    if (beforeClose && isPunct(beforeClose) && beforeClose !== '|' && afterClose && isWord(afterClose)) {
      edits.push({ pos: close - 1, remove: 3, insert: '**' + beforeClose })
    }
  }
  if (!edits.length) return para

  edits.sort((a, b) => b.pos - a.pos)
  let out = para
  for (const e of edits) {
    out = out.slice(0, e.pos) + e.insert + out.slice(e.pos + e.remove)
  }
  return out
}

function fixContent (raw) {
  const fm = raw.match(/^---[\s\S]*?---\r?\n/)
  const head = fm ? fm[0] : ''
  const body = raw.slice(head.length)

  const parts = body.split(/(```[\s\S]*?```|~~~[\s\S]*?~~~)/g)
  const outParts = parts.map((part, pi) => {
    if (pi % 2 === 1) return part
    const sub = part.split(/(`[^`\n]+`)/g)
    const outSub = sub.map((s, si) => {
      if (si % 2 === 1) return s
      const paras = s.split(/(\n[ \t]*\n)/)
      return paras.map(p => {
        if (p.startsWith('\n') || p.trim() === '') return p
        return fixParagraph(p)
      }).join('')
    })
    return outSub.join('')
  })
  return head + outParts.join('')
}

hexo.extend.filter.register('before_post_render', data => {
  if (!data || !data.content || !data.content.includes('**')) return data
  data.content = fixContent(data.content)
  return data
}, 1)
