---
title: 错误处理就是攻击面：同一个下午，两个运行时的地基被打穿
description: 10 月 21 日，PHP 和 Node.js 在同一个下午各自发了紧急补丁。两个洞都不在你的业务代码里：一个藏在 PHP 的致命错误处理与请求销毁之间，一个藏在 Node 内置的 Brotli 解码器里。前者从 2012 年就在，后者只是一个八字节的缓冲区。
publishDate: 2026-10-29
tags: [安全, 技术拆解, 运维]
draft: false
---

## 〇、同一个下午，两次补丁

2026 年 10 月 21 日，两件事挤在了同一天。

下午 14:00 UTC，PHP 发布 8.5.12、8.4.27、8.3.36、8.2.35，修两个 CVSS 9.2 的漏洞，编号 CVE-2026-109618 与 CVE-2026-109619，合称 PHP2Shell。官方公告里那句话没有留余地：**没有任何完整的缓解措施，升级是唯一安全的选择。**

同一天，Node.js 发布 22.23.4、24.22.1、26.12.1。十条安全公告里，Brotli 这条排第四——排在前面的三条也都是高危。第二天，Imperva 红队放出复现视频：在官方的 Node 24.22.0 Linux arm64 镜像里，一段压缩数据就让应用跑出了本该不存在的文件。

这两个洞隔着一个语言、一个生态、一个运行模型，却长着同一张脸：

- 都不在应用代码里。一个是 PHP 引擎的错误处理路径，一个是 Node 内置的 Brotli 解码器。
- 都不需要账号、不需要交互、不需要应用本身有任何逻辑缺陷。
- 触发它们的东西，都比"业务逻辑"低一层：一个是一段畸形 multipart 请求加一次可控的内存耗尽，一个是一段畸形的 Brotli 压缩流。

把它们放在一起看，会发现一个更麻烦的结论：你写了多少年业务代码，跟这两个洞没关系。它们在业务代码**下面**。

## 一、PHP2Shell：bailout 之后，没人收摊

先把机制说清楚，因为后面所有判断都建在这上面。

PHP 处理"致命错误"的方式不是抛异常，是 `longjmp`——直接跳走，不回头执行后面的清理代码。当一次分配超过 `memory_limit`，PHP 就是这样跳走的。问题在于：**跳走之前，有些状态已经写出去了；跳走之后，负责收摊的那段代码没有执行。**

于是进程里留下了一个指向已释放内存的指针，或者一个计数对不上、但内容没初始化的哈希桶。下一个请求落到同一个 worker 上，读到这份残留状态，就把它当成真的用。

Calif 的写作里给了一个最小、也最清楚的例子，在 `_zend_hash_str_add_or_update_i` 里：

```c
idx = ht->nNumUsed++;
ht->nNumOfElements++;

p = ht->arData + idx;
p->key = zend_string_init(str, len, persistent); /* 这里可能 zend_bailout() */

p->h = ZSTR_H(p->key) = h;
ZVAL_COPY_VALUE(&p->val, pData);
```

计数先加，桶的可见性先建立，然后才去分配 key。如果分配这一步踩到内存上限、直接 bailout，后面的 `key`、`hash`、`zval` 三行赋值全部跳过。但计数已经加了。请求销毁时，销毁逻辑是这样遍历的：

```c
for (p = ht->arData; p != ht->arData + ht->nNumUsed; p++) {
    i_zval_ptr_dtor(&p->val);
    if (p->key) {
        zend_string_release(p->key);
    }
}
```

它信任 `nNumUsed`。于是它把一块**从来没被初始化过**的内存，当成一个活的桶来析构。

这就是整个漏洞家族的原型。Wiz 把它总结成四个可复现的 bug：会话反序列化 use-after-free、进程内存泄露、致命错误回栈 use-after-free、OPcache 类型混淆。它们不是四个独立的错误，是同一个形状的四次出现：

- 第一步：先把状态发布出去（计数加一、指针写进全局）
- 第二步：再做一件可能失败的事（分配内存、解码数据）
- 第三步：最后才初始化、提交或回滚

失败插在第二步和第三步之间，第三步就被跳过。剩下的东西还带着"我是有效的"这个标记。

<figure>
<svg viewBox="0 0 680 330" width="100%" role="img" aria-label="错误路径的形状：状态先发布，失败插在提交之前">
<title>三步顺序一旦被致命错误打断，第三步就被跳过，残留状态仍被视为有效</title>
<defs>
<marker id="ep1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</marker>
</defs>
<rect x="30" y="24" width="196" height="60" rx="8" fill="#0C447C" stroke="#85B7EB" stroke-width="0.5"/>
<text x="128" y="48" font-size="13" font-weight="500" fill="#E6F1FB" text-anchor="middle">① 先发布状态</text>
<text x="128" y="68" font-size="11" fill="#85B7EB" text-anchor="middle">计数 +1 · 指针写进全局</text>
<rect x="258" y="24" width="164" height="60" rx="8" fill="#0C447C" stroke="#85B7EB" stroke-width="0.5"/>
<text x="340" y="48" font-size="13" font-weight="500" fill="#E6F1FB" text-anchor="middle">② 可能失败的一步</text>
<text x="340" y="68" font-size="11" fill="#85B7EB" text-anchor="middle">分配内存 / 解码</text>
<rect x="454" y="24" width="196" height="60" rx="8" fill="#0C447C" stroke="#85B7EB" stroke-width="0.5"/>
<text x="552" y="48" font-size="13" font-weight="500" fill="#E6F1FB" text-anchor="middle">③ 初始化 · 提交 · 回滚</text>
<text x="552" y="68" font-size="11" fill="#85B7EB" text-anchor="middle">把状态标记为完成或撤销</text>
<line x1="228" y1="54" x2="252" y2="54" stroke="#85B7EB" stroke-width="1.5" marker-end="url(#ep1)"/>
<line x1="424" y1="54" x2="448" y2="54" stroke="#85B7EB" stroke-width="1.5" marker-end="url(#ep1)"/>
<line x1="552" y1="86" x2="552" y2="106" stroke="#F7C1C1" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="552" y="120" font-size="11" fill="#F7C1C1" text-anchor="middle">这一步永远不会到达</text>
<line x1="340" y1="86" x2="340" y2="108" stroke="#F7C1C1" stroke-width="1.5" marker-end="url(#ep1)"/>
<text x="352" y="100" font-size="11" fill="currentColor">致命错误：longjmp 直接跳走</text>
<rect x="250" y="112" width="180" height="58" rx="8" fill="#501313" stroke="#F7C1C1" stroke-width="0.5"/>
<text x="340" y="136" font-size="13" font-weight="500" fill="#FCEBEB" text-anchor="middle">②③ 之间断开</text>
<text x="340" y="156" font-size="11" fill="#F7C1C1" text-anchor="middle">回滚没发生，标记还在</text>
<line x1="340" y1="172" x2="340" y2="196" stroke="#F7C1C1" stroke-width="1.5" marker-end="url(#ep1)"/>
<rect x="30" y="200" width="620" height="54" rx="8" fill="#501313" stroke="#F7C1C1" stroke-width="0.5"/>
<text x="340" y="222" font-size="13" font-weight="500" fill="#FCEBEB" text-anchor="middle">请求堆被销毁，但 worker 活着</text>
<text x="340" y="241" font-size="11" fill="#F7C1C1" text-anchor="middle">残留状态仍带着「我是有效的」这个标记，等下一个请求来读它</text>
<line x1="340" y1="256" x2="340" y2="276" stroke="currentColor" stroke-width="1.2" marker-end="url(#ep1)"/>
<rect x="30" y="280" width="190" height="42" rx="6" fill="none" stroke="#F7C1C1" stroke-width="0.5"/>
<text x="125" y="306" font-size="12" fill="currentColor" text-anchor="middle">崩溃</text>
<rect x="245" y="280" width="190" height="42" rx="6" fill="none" stroke="#F7C1C1" stroke-width="0.5"/>
<text x="340" y="306" font-size="12" fill="currentColor" text-anchor="middle">进程内存泄露</text>
<rect x="460" y="280" width="190" height="42" rx="6" fill="none" stroke="#F7C1C1" stroke-width="0.5"/>
<text x="555" y="306" font-size="12" fill="currentColor" text-anchor="middle">未认证远程代码执行</text>
</svg>
<figcaption>四类 bug 都落在同一个位置上：失败插在第二步与第三步之间，第三步就永远不执行。</figcaption>
</figure>

### 为什么一个只输出 OK 的页面也中招

这一点最反直觉，也最要紧。

PHP 在解析 multipart 请求体的时候，会顺带处理"上传进度"（`session.upload_progress`）。这个动作发生在 `php_request_startup()` 里面，**早于任何应用代码执行**。Calif 贴出了 `main/main.c` 里的顺序：

```c
PG(modules_activated) = 0;
php_hash_environment();   /* 解析请求变量和 multipart 输入 */
zend_activate_modules();  /* 正常模块的 RINIT */
PG(modules_activated) = 1;
```

也就是说，session 扩展在 PHP 自己都还没认为"模块已激活"的时候，就已经被拉起来跑过了。而请求销毁时的清理，恰恰是拿这个标志做开关的：

```c
if (PG(modules_activated)) {
    zend_deactivate_modules();
}
shutdown_memory_manager(...);
```

标志还是 0，所以 session 的 `RSHUTDOWN` 不跑；但请求堆照样被销毁。worker 活了下来，手里攥着几个已经指向虚空堆的全局指针。

下一个 multipart 请求进来，只要不带文件部分，就会走到 `MULTIPART_EVENT_END`，而绕过了会重置指针的 `MULTIPART_EVENT_FILE_START`。清理逻辑调用 `php_session_initialize()`，第一件事就是读那个悬空的 session id。

**应用一行代码都没执行。** 甚至不需要 `session_start()`。

### mod_php 和 FPM 的分岔

这里有个很漂亮的细节：同一个洞，在两种 SAPI 下的命运完全不同。

`mod_php` 的请求入口 `php_apache_request_ctor()` 启动失败时会 `zend_bailout()`，跳到外层 handler；但 handler 之后的代码仍然执行，包括 `php_apache_request_dtor(r)`，而它调的就是普通的 `php_request_shutdown(NULL)`。于是：堆被释放、worker 存活、残留状态可被下一个请求消费。

PHP-FPM 走的是另一条路。`fpm_main.c` 里，`php_request_startup()` 失败后直接 `return FPM_EXIT_SOFTWARE`，worker 退出。没有第二个请求，也就没有消费者。

所以 PHP 官方在公告里写得很直白：**风险最高的是 mod_php**，因为那条链能在应用代码之前就跑完。但这不是说 FPM 安全——Calif 后来找到的第三个入口，是"请求启动成功之后、应用自己触发的解码过程"被 fatal 打断。这条路 FPM 也适用，因为启动已经成功，worker 会继续活着接下一个人。

<figure>
<svg viewBox="0 0 680 306" width="100%" role="img" aria-label="同一个启动失败在 mod_php 与 PHP-FPM 下的两种结局">
<title>启动失败之后：mod_php 保留 worker 并复用，PHP-FPM 直接让 worker 退出</title>
<defs>
<marker id="sapi1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</marker>
</defs>
<rect x="240" y="20" width="200" height="46" rx="8" fill="#0C447C" stroke="#85B7EB" stroke-width="0.5"/>
<text x="340" y="38" font-size="13" font-weight="500" fill="#E6F1FB" text-anchor="middle">请求启动失败</text>
<text x="340" y="56" font-size="11" fill="#85B7EB" text-anchor="middle">php_request_startup() == FAILURE</text>
<line x1="290" y1="66" x2="170" y2="94" stroke="#85B7EB" stroke-width="1.5" marker-end="url(#sapi1)"/>
<line x1="390" y1="66" x2="510" y2="94" stroke="#85B7EB" stroke-width="1.5" marker-end="url(#sapi1)"/>
<text x="190" y="92" font-size="12" fill="currentColor" text-anchor="end">mod_php</text>
<text x="490" y="92" font-size="12" fill="currentColor">PHP-FPM</text>
<rect x="30" y="98" width="290" height="44" rx="8" fill="#501313" stroke="#F7C1C1" stroke-width="0.5"/>
<text x="175" y="116" font-size="12" fill="#FCEBEB" text-anchor="middle">bailout 到外层 handler</text>
<text x="175" y="133" font-size="11" fill="#F7C1C1" text-anchor="middle">handler 之后的代码照常执行</text>
<rect x="360" y="98" width="290" height="44" rx="8" fill="#0F6E56" stroke="#9FE1CB" stroke-width="0.5"/>
<text x="505" y="116" font-size="12" fill="#E1F5EE" text-anchor="middle">return FPM_EXIT_SOFTWARE</text>
<text x="505" y="133" font-size="11" fill="#9FE1CB" text-anchor="middle">worker 在这一行退出</text>
<line x1="175" y1="142" x2="175" y2="162" stroke="#F7C1C1" stroke-width="1.5" marker-end="url(#sapi1)"/>
<line x1="505" y1="142" x2="505" y2="162" stroke="#9FE1CB" stroke-width="1.5" marker-end="url(#sapi1)"/>
<rect x="30" y="166" width="290" height="44" rx="8" fill="#501313" stroke="#F7C1C1" stroke-width="0.5"/>
<text x="175" y="184" font-size="12" fill="#FCEBEB" text-anchor="middle">php_request_shutdown() 仍然调用</text>
<text x="175" y="201" font-size="11" fill="#F7C1C1" text-anchor="middle">PG(modules_activated) 还是 0</text>
<rect x="360" y="166" width="290" height="44" rx="8" fill="#0F6E56" stroke="#9FE1CB" stroke-width="0.5"/>
<text x="505" y="184" font-size="12" fill="#E1F5EE" text-anchor="middle">没有第二个请求</text>
<text x="505" y="201" font-size="11" fill="#9FE1CB" text-anchor="middle">也就没有消费者</text>
<line x1="175" y1="210" x2="175" y2="230" stroke="#F7C1C1" stroke-width="1.5" marker-end="url(#sapi1)"/>
<line x1="505" y1="210" x2="505" y2="230" stroke="#9FE1CB" stroke-width="1.5" marker-end="url(#sapi1)"/>
<rect x="30" y="234" width="290" height="44" rx="8" fill="#501313" stroke="#F7C1C1" stroke-width="0.5"/>
<text x="175" y="252" font-size="12" fill="#FCEBEB" text-anchor="middle">session RSHUTDOWN 被跳过</text>
<text x="175" y="269" font-size="11" fill="#F7C1C1" text-anchor="middle">请求堆照样销毁 → 悬空指针留存</text>
<rect x="360" y="234" width="290" height="44" rx="8" fill="#0F6E56" stroke="#9FE1CB" stroke-width="0.5"/>
<text x="505" y="252" font-size="12" fill="#E1F5EE" text-anchor="middle">对启动阶段那条链免疫</text>
<text x="505" y="269" font-size="11" fill="#9FE1CB" text-anchor="middle">启动成功后的 fatal 仍留下活着的 worker</text>
<text x="175" y="296" font-size="11" fill="currentColor" text-anchor="middle">风险最高：应用代码之前就能完成</text>
<text x="505" y="296" font-size="11" fill="currentColor" text-anchor="middle">所以第三个入口两种 SAPI 都中</text>
</svg>
<figcaption>同一个启动失败，两种 SAPI 做出了相反的决定。差别不在漏洞，在那行 <code>return</code>。</figcaption>
</figure>

### Heartbleed 那一半

除了 RCE，PHP2Shell 还有一个独立的泄露原语：内存耗尽把 `PS(id)` 留成了悬空 `zend_string`，下一个请求把它当成活的字符串，按攻击者指定的长度，URL 编码后塞进 `Set-Cookie: PHPSESSID` 响应头。

一次大约 67 KB。内容是那个 worker 当时堆里的东西——可能包括别的请求的密码、token、API key、证书。这个长度由攻击者的输入决定，所以它不是"一次偷 67 KB"这么固定的事，而是一个**可调尺寸的读取窗口**。

这个形状太像 2014 年的 Heartbleed 了：不是拿到了什么权限，是**读到了不该读的内存**。区别在于，Heartbleed 读的是 64 KB 的边界，这里读的是进程的堆。而且它发生在应用层之下，应用日志里几乎什么都不留。

## 二、Node2Shell：一个八字节的缓冲区

Node 那边的问题更小、更具体。

Brotli 是一种压缩格式，Chrome 用它压网页，Node 把它内置进了 `node:zlib`。Node 官方公告的原话是：

> 一个无效的 block switch 被报告为"暂时需要更多输入"，而不是永久的格式错误，所以流式解码器继续把输入字节追加到一个八字节的内部缓冲区。

八字节。一个用来暂存"还没凑够"的定长缓冲，被当成了可以无限追加的地方。越界写，然后就是标准的三件套：崩溃、内存泄露、远程代码执行。

Imperva 的复现路径值得抄下来，因为它标出了**暴露面到底在哪**：

| 应用路径 | 涉及的包 | Node 24.22.0 | Node 24.22.1 |
| --- | --- | --- | --- |
| 消费外部 HTTP 响应 | 内置 `fetch()` | 代码执行，marker 文件出现 | 输入被拒，无 marker |
| 接收请求体 | Express 5.0.0–5.3.0 + body-parser 2.0.1 / 2.3.0 | `raw()` 与 `json()` 下均可执行 | 输入被拒，服务继续运行 |
| 接收请求体 | body-parser 2.0.0–2.3.0 | 同上 | 同上 |

三个限定必须说清楚：

1. **裸的 Node HTTP 服务器不会因为收到 Brotli 请求体就解压。** 得有人配了中间件。
2. **漏洞在 Node 里，不在 Express 里。** 那些中间件版本只是"通往脆弱解码器的路"。
3. **复现不是每次成功。** Imperva 自己写了"execution took multiple attempts in our setup"。这不是一个点一下就中的洞。

修法在 Brotli 上游：`google/brotli` 的一个 commit 让解码器对这种非法转换直接返回格式错误。但 Node 打包了自己那份 Brotli，所以修 Brotli 不够，得升 Node 运行时本身。

这一条是整篇文章里最实用的一句话：**`npm audit` 不会告诉你运行时版本。** 你的 lock 文件里没有 `node`，你的 SBOM 很可能也没有。而这个洞的补丁，恰好只存在于运行时里。

## 三、共同点：正常路径之外的路径

把两个洞并排放：

| | PHP2Shell | Node2Shell |
| --- | --- | --- |
| 位置 | PHP 引擎的错误处理 / 请求销毁 | Node 内置 Brotli 解码器 |
| 触发 | 畸形 multipart + 内存耗尽 | 畸形 Brotli 流 |
| 应用是否参与 | 否（可以在应用代码前完成） | 否（但需要配了解压中间件） |
| 直接后果 | 进程内存泄露 / 越界写 | 越界写 |
| 最坏后果 | 未认证 RCE | RCE |
| 受影响范围 | PHP ≥ 5.4.0 | Node 22 / 24 / 26 全系 |
| 修复位置 | PHP 引擎（并有 7.4/8.0/8.1 的最小回移） | Node 运行时 + Brotli 上游 |

两张表里最刺眼的是"应用是否参与"这一行。

我们平时谈安全，默认的模型是：应用的输入校验有 bug，所以被打了。所以修法是加校验、加参数化查询、加 WAF 规则。这套模型成立的前提是——**攻击面在应用里**。

这两个洞把这个前提掀了。攻击面在应用**下面**，在"请求还没变成你的代码"和"请求已经结束但内存还没收干净"这两段之间。你写多好的业务代码，都不影响这两段。

而且这两段的代码，是全世界的服务器共用的。PHP 在已知服务端语言的网站里占到近七成——不是营销数字，是同一份 C 代码跑在几百万台机器上。

## 四、为什么是现在

这两个洞都老了。PHP2Shell 最早的那条路径可以追到 PHP 5.4.0——2012 年 3 月。十四年。

这十四年里，它不是没被人看见。2020 年有人报过一个相关的 bug（#78876，长变量导致 OOM 和临时文件未清理）；2024 年 OSTIF 和 Quarkslab 做 PHP 审计时又碰到过同类问题，但**没能证明可利用**，所以没修。

真正变的是"从看见到打穿"的成本。

两条独立的线，时间几乎重叠：

**Calif 那条**：8 月 1 日开始审计，几天内就出了第一个 OOM-fatal；8 月 11 日报告给 PHP；8 月 14 日交出 RCE PoC；8 月 15 日 PHP 确认可用；8 月 21 日报告第二个；10 月 21 日补丁发布。

**Wiz 那条**：8 月 19 日发现；8 月 20 日确认 Drupal 未认证 RCE；8 月 21 日确认 WordPress；8 月 24 日报告。

他们是各自独立发现、独立报告的，后来才并到同一次协同披露里。这一点值得记住——不是"一个团队找到了一个洞"，是**两个团队在同一个夏天、用类似的方法、在同一个代码库里各自挖到了同一个家族**。

Wiz 的结论写得很直白：

> 在 AI 之前，这套手工工作很难实现，更难规模化。漏洞利用的复杂度可能不再构成有意义的门槛。

但另一条线的话，更值得抄在墙上。Calif 的研究者在"我们是怎么找到的"那一节里说：

> 初始的 bug 发现没有用任何特殊 harness，也没有用别人拿不到的模型。我专注于自己有背景、熟悉其漏洞历史、并且相信特定 bug 就藏在里面的方向。……LLM 可能读过公开的历史漏洞数据，但在默认的变体分析里，它倾向于从最新、最显眼的 bug 往附近的老代码走。它不会可靠地从二十年前的冷门利用原语开始。**保留你自己对目标漏洞历史的心智目录，才能把提示明确地指向那个方向。**

这段话把"AI 找到了洞"这句流行叙事拆成了两半：

- AI 降低的是**验证成本**——一个假设从"值得怀疑"到"有 PoC"，从几个月变成几天。
- 人的领域知识决定的仍然是**搜索方向**——你知道该往哪看。

两者缺一不可。宣传稿只会写前半句。

## 五、防守方的窗口有多宽

"我们在攻击者之前发现了它"这句话，在新闻稿里出现过很多次。这次有一个反例，值得记住。

PHP 的补丁在 10 月 21 日 14:00 UTC 上线。AWS 的威胁情报团队在 MadPot 里看到的最早利用尝试是 **10 月 17 日**——比披露早四天。10 月 21 日凌晨 2 点（UTC）起，他们已经观察到多个 PoC 在打，来源 IP 各不相同。

所以那句"披露前无人利用"是错的。更准确的说法是：**在补丁可用之前，已经有人在试了，只是还没成功。**

然后是 CISA 的节奏：

- 10 月 26 日，PHP 两个 CVE 进 KEV，联邦机构截止 **10 月 29 日**。
- 10 月 27 日，Node 的 CVE-2026-111497 进 KEV，截止 **11 月 10 日**。

从补丁发布到强制截止，一个 8 天，一个 20 天。这不是"给你时间评估"，这是"按小时算"的另一种写法。

<figure>
<svg viewBox="0 0 680 300" width="100%" role="img" aria-label="补丁发布到强制截止之间的窗口，以及实际利用早于披露">
<title>时间轴：实际利用早于披露，而强制截止只有 8 天与 20 天</title>
<defs>
<marker id="tl2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</marker>
</defs>
<text x="40" y="22" font-size="11" fill="currentColor">PHP2Shell</text>
<line x1="40" y1="40" x2="640" y2="40" stroke="#85B7EB" stroke-width="1.2"/>
<line x1="150" y1="34" x2="150" y2="46" stroke="#F7C1C1" stroke-width="2"/>
<circle cx="150" cy="40" r="4" fill="#F7C1C1"/>
<text x="150" y="62" font-size="10" fill="#F7C1C1" text-anchor="middle">10-17 最早利用尝试</text>
<text x="150" y="74" font-size="9" fill="currentColor" text-anchor="middle">比披露早 4 天</text>
<line x1="300" y1="34" x2="300" y2="46" stroke="#FAC775" stroke-width="2"/>
<circle cx="300" cy="40" r="4" fill="#FAC775"/>
<text x="300" y="62" font-size="10" fill="#FAC775" text-anchor="middle">10-21 14:00 UTC</text>
<text x="300" y="74" font-size="9" fill="currentColor" text-anchor="middle">补丁 + 披露</text>
<line x1="460" y1="34" x2="460" y2="46" stroke="#F7C1C1" stroke-width="2"/>
<circle cx="460" cy="40" r="4" fill="#F7C1C1"/>
<text x="460" y="62" font-size="10" fill="#F7C1C1" text-anchor="middle">10-26 进 KEV</text>
<line x1="570" y1="34" x2="570" y2="46" stroke="#F7C1C1" stroke-width="2"/>
<circle cx="570" cy="40" r="4" fill="#F7C1C1"/>
<text x="570" y="62" font-size="10" fill="#F7C1C1" text-anchor="middle">10-29 联邦截止</text>
<line x1="300" y1="86" x2="570" y2="86" stroke="#FAC775" stroke-width="2" marker-end="url(#tl2)"/>
<text x="435" y="80" font-size="11" fill="#FAC775" text-anchor="middle">8 天</text>
<text x="40" y="112" font-size="11" fill="currentColor">Node2Shell</text>
<line x1="40" y1="130" x2="640" y2="130" stroke="#85B7EB" stroke-width="1.2"/>
<line x1="300" y1="124" x2="300" y2="136" stroke="#9FE1CB" stroke-width="2"/>
<circle cx="300" cy="130" r="4" fill="#9FE1CB"/>
<text x="300" y="152" font-size="10" fill="#9FE1CB" text-anchor="middle">10-21 同一批补丁</text>
<text x="300" y="164" font-size="9" fill="currentColor" text-anchor="middle">22.23.4 / 24.22.1 / 26.12.1</text>
<line x1="470" y1="124" x2="470" y2="136" stroke="#9FE1CB" stroke-width="2"/>
<circle cx="470" cy="130" r="4" fill="#9FE1CB"/>
<text x="470" y="152" font-size="10" fill="#9FE1CB" text-anchor="middle">10-27 进 KEV</text>
<line x1="600" y1="124" x2="600" y2="136" stroke="#9FE1CB" stroke-width="2"/>
<circle cx="600" cy="130" r="4" fill="#9FE1CB"/>
<text x="600" y="152" font-size="10" fill="#9FE1CB" text-anchor="middle">11-10 联邦截止</text>
<line x1="300" y1="176" x2="600" y2="176" stroke="#9FE1CB" stroke-width="2" marker-end="url(#tl2)"/>
<text x="450" y="170" font-size="11" fill="#9FE1CB" text-anchor="middle">20 天</text>
<rect x="40" y="196" width="600" height="46" rx="8" fill="none" stroke="#F7C1C1" stroke-width="0.5" stroke-dasharray="3 3"/>
<text x="340" y="215" font-size="11" fill="#F7C1C1" text-anchor="middle">10 月 17 日已在利用，10 月 21 日 02:00 UTC 起多方 PoC 同时开打</text>
<text x="340" y="232" font-size="10" fill="currentColor" text-anchor="middle">「我们在攻击者之前发现了它」在这条轴上不成立</text>
<text x="40" y="264" font-size="11" fill="currentColor">两端都不是按季度算的：一个 8 天，一个 20 天。</text>
<text x="40" y="282" font-size="11" fill="currentColor">而基础镜像重建这一段，取决于你上一次 pull 是什么时候。</text>
</svg>
<figcaption>两条更新的窗口宽度不同，但都短于多数团队的补丁排队周期。</figcaption>
</figure>

但 KEV 管的是美国联邦机构。对大多数人来说，真正的窗口不是 KEV 给的那个，而是这一段：

**补丁发布 → 你的基础镜像重建 → 你的容器重新部署 → 你的流量真的跑到新版本上。**

这一段里最容易被漏掉的是第三步和第二步之间的缝。因为 PHP 和 Node 都是"运行时"，它们经常不在依赖清单里，而在基础镜像里；基础镜像又经常是"一年前 pull 下来就没动过"的那个。

一个能今天就做的检查，比任何流程图都管用：

```bash
php -v                    # 而不是看你 composer.json 里的 php 约束
node -p process.versions  # 而不是看 package.json 的 engines
```

在**每一个**跑生产流量的镜像里跑一遍。包括那些"我们不直接维护、但是它在跑"的镜像。

## 六、缓解措施的代价：没有免费的补丁

PHP 官方给了不能立刻升级时的临时措施，值得逐条看，因为每一条都在拿一个东西换另一个东西。

**针对 CVE-2026-109618（OOM 那条）：**

- 把 `memory_limit` 设成 `-1`。这直接去掉了"可控的内存耗尽"这个触发器。代价是：内存上限没了，OOM 变成操作系统层面的 OOM killer，或者更糟，变成整机卡死。
- 收紧 `post_max_size`（无上传需求设 8M，有上传设 32M），并在 Web 服务器或代理层限制解码后的请求大小、字段数、multipart 段数、header 数、嵌套深度。代价是：可能打断正常的批量上传。
- 用容器 / cgroup 做可用性边界，并且只杀受影响的 worker。官方特意提醒**不要**用 `RLIMIT_AS` 或 `RLIMIT_DATA`——那会直接造出触发漏洞的那种分配失败。

**针对 CVE-2026-109619（残留全局状态那条）：**

- `session.upload_progress.enabled=0`，并且重启每个 worker。必须写在 `php.ini`、FPM pool 或服务器配置里，不能靠 `ini_set()` 或 `.user.ini`——因为漏洞发生在请求解析阶段，那时应用配置还没生效。
- PHP 8.5 上再加 `fatal_error_backtraces=0`。
- 移除那些"每次请求都会在初始化前发诊断"的无效或废弃配置。官方补了一句很反直觉的话：**用 `error_reporting`、`display_errors` 或 `@` 把诊断藏起来没用。**

然后 10 月 23 日，PHP 又发了一条补充说明：还存在一个更窄的 RCE 向量，要求应用把 `session.serialize_handler` 从 `php_binary` 或 `php_serialize` 在运行时用 `ini_set()` 改成 `php`，同时上传进度还开着。官方判断这个组合在实践中不太可能出现，所以放到常规发布周期里，编号 CVE-2026-115560。

这条补充说明本身就是个提醒：**缓解措施是有适用条件的，不能照抄。** 关掉上传进度能挡住三条已确认的会话路径，挡不住"其他变体"。PHP 官方在公告里也写了这句——补丁才是"从根上消除所有变体"的那个动作。

Node 那边更简单，也更难：在代理或防火墙层拒绝不可信的 Brotli 压缩请求，或者关掉 Brotli 解码，等运行时升级。代价是带宽。

把所有代价放在一起看，会看到同一个结构：

**缓解措施的本质，是关掉一个功能换时间，而关掉的那个功能，通常是性能优化。**

压缩是为了省带宽。OPcache 是为了省 CPU。上传进度是为了体验。这些东西之所以存在，是因为它们值钱。关掉它们，账单没有消失，只是从"安全预算"挪到了"性能预算"。

这和 10-24 那篇讲成本转移是同一个形状：**任何保护都有成本，成本不会消失，只会换一个科目入账。**

## 七、这件事跟不懂 C 的人有什么关系

大部分读者不会去读 `zend_hash.c`，也不需要。但下面三件事，是任何管着一台服务器、一个站点、一个内部工具的人都该知道的。

**第一，运行时是资产，不是背景。**

我们习惯把"版本"理解成框架版本、依赖版本。`package.json`、`composer.json`、`requirements.txt` 里写的东西，看起来就是全部。但真正在跑的 PHP 和 Node，是镜像里的那个二进制。它没有版本号写在你的仓库里，也就没有人给它做 dependabot。

一个具体的后果：这次 Node 的补丁，任何只扫 lock 文件的工具都不会提醒你。它甚至不知道你有 Node。

**第二，谁在替你解压。**

Brotli 这条路最有意思的地方在于：它可以被"消费别人的响应"触发，也可以被"解压别人的请求体"触发。也就是说，一个 Node 服务即便自己从不主动调用解压，只要它用 `fetch()` 去拉一个攻击者能控制的 URL，而对方返回了 Brotli 压缩内容，就可能中招。

"我没开这个功能"这句话，在有中间件、有反向代理、有 CDN 的系统里，通常不成立。数据在到你之前，已经被解压过好几次了。**每一次解压都是一次信任转移。**

**第三，补丁窗口按小时算，不按季度算。**

这个变化不是"大家更急了"，是攻击的成本结构变了。过去，"这个洞太复杂，没人会写利用"是很多团队把高危排在季度末的理由。当利用开发的成本从"一个世界级团队几个月"降到"一个人一周"，这条理由就没了。

Wiz 那句话值得再抄一遍：**复杂度可能不再构成有意义的门槛。**

## 八、留给下一个洞的位置

回头看不长的这几天，最不舒服的不是"又有两个 9.2"，而是它们的形状。

它们都不是"谁把业务代码写错了"。它们是地基里的洞——在异常路径上，在解码器里，在"请求已经结束但内存还没收干净"的那几十毫秒里。地基的问题不会因为你楼上装修得好而消失，也不会因为你用了框架、开了 WAF、写了单元测试而消失。

而在同一个夏天，两个互不相识的团队，用类似的方法，在同一个代码库里挖到了同一个家族。这说明的不是"PHP 很烂"，恰恰相反——说明**这类洞还有多少没被挖出来，取决于有多少人愿意去挖**。Calif 的研究者说得很清楚：他之所以能找到，是因为他知道该往哪看。

于是真正的分水岭不在 10 月 21 日，而在更早：当"验证一个怀疑"变得便宜，剩下的稀缺品就变成了"值得怀疑的方向"。

对防守方来说，这既是好消息也是坏消息。好消息是，那些躺了十四年的洞，终于会被找出来。坏消息是，找出来之后，你有八天。

---

**补记两句口径。** 一是那个流传最广的"70%"：Wiz 写的是"全世界 70% 的网站"，而 PHP 官方与 Calif 的表述是"在已知服务端语言的网站中超过 69%"——分母不一样，前者把不知道服务端语言的站点也算进了分子。二是那个"一次约 67 KB"的内存泄露，数字来自 Imperva 对 PHP2Shell 泄露原语的实测，它取决于当时 worker 的内存布局和攻击者设定的长度，不是固定值。

参考：PHP 官方 [2026 年 10 月 21 日安全公告](https://www.php.net/archive/2026.php#2026-10-21-5) 与 [10 月 23 日补充说明](https://www.php.net/archive/2026.php#2026-10-23-1)；[Wiz 的 PHP2Shell 写作](https://www.wiz.io/blog/php2shell-php-rce)；[Calif 的技术长文](https://calif.io/php2shell/)（含完整披露时间线与 PoC 列表）；[Imperva 的 PHP2Shell 分析](https://www.imperva.com/blog/php2shell-vulnerability-updates/)；[Node.js 10 月 21 日安全发布](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases)；[Imperva 的 Node2Shell 复现](https://www.imperva.com/blog/node2shell-from-brotli-data-to-remote-code-execution/)；[AWS 关于披露前利用的说明](https://aws.amazon.com/blogs/security/amazon-threat-intelligence-identifies-php2shell-exploitation-prior-to-public-disclosure-in-madpot)。