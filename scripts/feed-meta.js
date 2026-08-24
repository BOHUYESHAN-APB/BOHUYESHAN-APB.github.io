'use strict';

/**
 * 信息流卡片元数据注入
 * 在首页 HTML 渲染后，为每个文章卡片注入字数和预估阅读时间
 * 依赖 hexo-wordcount 插件注册的 wordcount / min2read helper
 */

hexo.extend.filter.register('after_render:html', function (html) {
  // 只处理包含文章卡片的页面（首页、归档页等）
  if (!html || !html.includes('recent-post-item')) return html;

  const posts = this.locals.get('posts');
  if (!posts || posts.length === 0) return html;

  // 获取 hexo-wordcount 注册的 helper
  const wordcountFn = hexo.extend.helper.get('wordcount');
  const min2readFn = hexo.extend.helper.get('min2read');
  if (!wordcountFn || !min2readFn) return html;

  // 构建路径 → 文章对象的映射（同时映射 URL 编码版本）
  const postMap = {};
  posts.forEach(function (post) {
    if (post.path) {
      postMap['/' + post.path] = post;
      postMap[post.path] = post;
      // URL 编码版本（中文路径在 href 中是 percent-encoded）
      const encoded = encodeURI(post.path);
      if (encoded !== post.path) {
        postMap['/' + encoded] = post;
        postMap[encoded] = post;
      }
    }
    if (post.permalink) {
      postMap[post.permalink] = post;
    }
  });

  // 查找所有文章标题链接，收集需要注入的信息
  const titleRegex = /<a class="article-title" href="([^"]*)"[^>]*>/g;
  const injections = [];
  let match;

  while ((match = titleRegex.exec(html)) !== null) {
    const href = match[1];
    const post = postMap[href];
    if (!post || !post.content) continue;

    const wc = wordcountFn(post.content);
    const rt = min2readFn(post.content, { cn: 350, en: 160 });

    injections.push({
      titleIndex: match.index,
      wordcount: wc,
      readtime: rt
    });
  }

  if (injections.length === 0) return html;

  // 从后往前注入，避免索引偏移
  for (let i = injections.length - 1; i >= 0; i--) {
    const item = injections[i];

    // 找到该标题后的 article-meta-wrap 开始标签
    const metaOpenTag = '<div class="article-meta-wrap">';
    const metaStart = html.indexOf(metaOpenTag, item.titleIndex);
    if (metaStart === -1) continue;

    // article-meta-wrap 内部只有 span（无嵌套 div），
    // 所以第一个 </div> 就是它的闭合标签
    const contentStart = metaStart + metaOpenTag.length;
    const metaClose = html.indexOf('</div>', contentStart);
    if (metaClose === -1) continue;

    const metaHtml =
      '<span class="article-meta card-reading-meta">' +
      '<span class="article-meta-separator">|</span>' +
      '<i class="far fa-file-word"></i>' +
      '<span class="card-word-count">' + item.wordcount + '</span>' +
      '<span class="article-meta-label"> 字</span>' +
      '<span class="article-meta-separator">|</span>' +
      '<i class="far fa-clock"></i>' +
      '<span class="card-read-time"> 约 ' + item.readtime + ' 分钟</span>' +
      '</span>';

    html = html.slice(0, metaClose) + metaHtml + html.slice(metaClose);
  }

  return html;
});
