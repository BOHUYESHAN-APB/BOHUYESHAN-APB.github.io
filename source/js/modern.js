/**
 * 现代化 UI 动效包（渐进增强）
 * 1. 阅读进度条：仅文章页显示
 * 2. 滚动入场动画：IntersectionObserver，一次性触发，支持 stagger
 * 3. 尊重 prefers-reduced-motion；无 JS 时内容照常可见
 */
(function () {
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches

  /* ---------- 阅读进度条 ---------- */
  var bar = null
  var ticking = false

  function ensureBar() {
    if (bar || !document.getElementById('post')) return
    bar = document.createElement('div')
    bar.id = 'read-progress'
    document.body.appendChild(bar)
  }

  function updateBar() {
    ticking = false
    if (!bar) return
    var doc = document.documentElement
    var max = doc.scrollHeight - doc.clientHeight
    var ratio = max > 0 ? Math.min(doc.scrollTop / max, 1) : 0
    bar.style.transform = 'scaleX(' + ratio + ')'
  }

  window.addEventListener('scroll', function () {
    ensureBar()
    if (!ticking) {
      ticking = true
      requestAnimationFrame(updateBar)
    }
  }, { passive: true })
  ensureBar()
  updateBar()

  /* ---------- 滚动入场 ---------- */
  var targets = [].slice.call(
    document.querySelectorAll('.recent-post-item, #aside-content .card-widget')
  )

  if (!('IntersectionObserver' in window) || reduced) return

  // 仅对首屏外的元素启用入场动画，避免首屏闪动
  var vh = window.innerHeight
  targets = targets.filter(function (el) {
    return el.getBoundingClientRect().top > vh
  })

  targets.forEach(function (el, i) {
    el.classList.add('reveal')
    el.style.transitionDelay = Math.min(i * 60, 360) + 'ms'
  })

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed')
        io.unobserve(entry.target)
      }
    })
  }, { rootMargin: '200px 0px 25% 0px' })

  targets.forEach(function (el) { io.observe(el) })
})()
