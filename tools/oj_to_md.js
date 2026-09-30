/* =====================================================================
 * 清华 OJ 题目批量保存为 Markdown  (v2 - iframe 渲染版)
 *
 * 原理：TriUOJ 是 SPA，题目正文由 JS 动态加载，fetch 只能拿到空壳。
 *      本脚本用隐藏 iframe 加载每道题，等 JS 渲染完成后读取真实 DOM。
 *
 * 使用方法：
 *   1. Chrome / Edge 登录 OJ，打开任一题目页
 *      (如 https://oj.cs.tsinghua.edu.cn/course/90/contest/1038/problem/0)
 *   2. F12 → Console
 *   3. 粘贴本脚本回车
 *   4. 弹窗选择 OOP/HW 文件夹（或新建）
 *   5. 等待 5 道题完成
 * ===================================================================== */
(async () => {
  'use strict';

  const m = location.href.match(/course\/(\d+)\/contest\/(\d+)/);
  if (!m) {
    console.error('❌ 请在 OJ contest 页面运行（URL 含 course/xx/contest/yy）');
    return;
  }
  const [, course, contest] = m;
  const base = `https://oj.cs.tsinghua.edu.cn/course/${course}/contest/${contest}`;
  console.log(`🔍 course=${course}, contest=${contest}`);

  // ---------- 加载 Turndown ----------
  if (!window.TurndownService) {
    console.log('⏳ 加载 Turndown…');
    await new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = 'https://cdn.jsdelivr.net/npm/turndown@7.1.2/dist/turndown.js';
      s.onload = resolve;
      s.onerror = () => {
        s.src = 'https://unpkg.com/turndown@7.1.2/dist/turndown.js';
        s.onload = resolve;
        s.onerror = () => reject(new Error('Turndown 加载失败'));
      };
      document.head.appendChild(s);
    });
  }
  const td = new TurndownService({
    headingStyle: 'atx', codeBlockStyle: 'fenced',
    bulletListMarker: '-', emDelimiter: '_',
  });
  td.addRule('keepPre', {
    filter: ['pre'],
    replacement: (_, node) => '\n\n```\n' + node.textContent + '\n```\n\n',
  });
  // 去掉页脚等噪声
  td.remove(['script', 'style', 'nav', 'footer', 'header', 'noscript']);

  // ---------- 选文件夹 ----------
  let dir = null;
  if (window.showDirectoryPicker) {
    try {
      dir = await window.showDirectoryPicker({ mode: 'readwrite' });
      console.log(`📂 文件夹: ${dir.name}`);
    } catch (e) {
      console.warn('⚠️ 未选文件夹，改用普通下载');
    }
  }
  // 写入：文件夹 dir/<folderName>/<fileName>，无文件夹API时退化为 <folderName>_<fileName>
  async function saveFile(folderName, fileName, content) {
    if (dir) {
      const sub = await dir.getDirectoryHandle(folderName, { create: true });
      const fh = await sub.getFileHandle(fileName, { create: true });
      const w = await fh.createWritable();
      await w.write(content); await w.close();
    } else {
      const a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob([content], { type: 'text/markdown;charset=utf-8' }));
      a.download = `${folderName}/${fileName}`.replace('/', '_'); // 普通下载无法建子目录，用前缀
      a.click();
      setTimeout(() => URL.revokeObjectURL(a.href), 1000);
    }
  }

  // ---------- iframe 渲染题目 ----------
  function loadIframe(url) {
    return new Promise((resolve, reject) => {
      const iframe = document.createElement('iframe');
      iframe.style.cssText = 'position:fixed;right:0;bottom:0;width:500px;height:400px;border:1px solid #0a0;z-index:99999;opacity:.6;';
      iframe.src = url;
      iframe.onload = () => resolve(iframe);
      iframe.onerror = () => reject(new Error('iframe 加载失败（可能被 X-Frame-Options 拦截）'));
      document.body.appendChild(iframe);
      setTimeout(() => reject(new Error('iframe 加载超时')), 15000);
    });
  }

  // 等待正文出现（轮询 DOM 直到内容稳定）
  async function waitForContent(getBody, { minLen = 300, stableMs = 1200, timeout = 12000 } = {}) {
    const start = Date.now();
    let lastLen = -1, stableSince = start;
    while (Date.now() - start < timeout) {
      await new Promise(r => setTimeout(r, 300));
      const len = getBody().innerHTML.length;
      if (len >= minLen) {
        if (len === lastLen) {
          if (Date.now() - stableSince >= stableMs) return true;
        } else {
          stableSince = Date.now();
        }
      }
      lastLen = len;
    }
    return false;
  }

  // 正文选择器（按优先级）
  function extractContent(doc) {
    const sels = [
      '.problem-content', '.problem-body', '.problem-statement',
      '.markdown-body', '.problem-detail', '.problem',
      '[class*="problem"][class*="content"]',
      'article', 'main', '.content', '#app',
    ];
    for (const sel of sels) {
      const el = doc.querySelector(sel);
      if (el && el.innerText.trim().length > 100) {
        // 去掉明显是导航/页脚的子节点
        el.querySelectorAll('nav,footer,header,.navbar,.footer,.sidebar,nav,script,style').forEach(n => n.remove());
        return { el, via: sel };
      }
    }
    return { el: doc.body, via: 'body(兜底)' };
  }

  function extractTitle(doc, idx) {
    const t = doc.querySelector('h1,h2,.title,.problem-title,[class*="title"]')?.textContent;
    return (t || `Problem ${idx}`).trim().replace(/\s+/g, ' ').slice(0, 120);
  }

  // ---------- 主循环 ----------
  const N = 5;
  for (let i = 0; i < N; i++) {
    const url = `${base}/problem/${i}`;
    console.log(`\n➡️ [${i + 1}/${N}] ${url}`);
    let iframe;
    try {
      iframe = await loadIframe(url);
      const idoc = iframe.contentDocument;
      await waitForContent(() => idoc.body);
      // 再额外等一会儿确保 Markdown 渲染完成
      await new Promise(r => setTimeout(r, 1500));

      const { el, via } = extractContent(idoc);
      const title = extractTitle(idoc, i);
      const preview = el.innerText.replace(/\s+/g, ' ').slice(0, 80);
      console.log(`   📝 ${title}\n   选择器: ${via} | 预览: ${preview}…`);

      const bodyMd = td.turndown(el.innerHTML);
      const md =
        `# ${title}\n\n` +
        `> 来源: <${url}>\n` +
        `> course ${course} · contest ${contest} · problem ${i}\n\n---\n\n` +
        `${bodyMd.trim()}\n`;
      await saveFile(`Problem_${i}.md`, md);
      console.log(`   ✅ 已保存 Problem_${i}.md`);
    } catch (e) {
      console.error(`   ❌ 第 ${i} 题失败: ${e.message}`);
      console.error('   若是 X-Frame-Options 拦截，请告诉我，我改用 API 方案');
    } finally {
      if (iframe) iframe.remove();
    }
    await new Promise(r => setTimeout(r, 800));
  }
  console.log('\n🎉 完成！');
})();
