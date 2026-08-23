/**
 * 站点加载屏控制器
 * - window load 后淡出并移除 #site-loader
 * - 4 秒兜底：即使有资源卡住也不会永久挡住内容
 */
(function () {
  var loader = document.getElementById('site-loader')
  if (!loader) return

  var finished = false
  var finish = function () {
    if (finished) return
    finished = true
    loader.classList.add('done')
    setTimeout(function () {
      if (loader.parentNode) loader.parentNode.removeChild(loader)
    }, 650)
  }

  if (document.readyState === 'complete') {
    finish()
  } else {
    window.addEventListener('load', finish)
    setTimeout(finish, 4000)
  }
})()
