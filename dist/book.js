/* Reading positions are kept on this device, independently for each book. */
try {
  const link = document.querySelector('.start-reading');
  const saved = JSON.parse(localStorage.getItem('shuangmulin:' + link.dataset.book) || 'null');
  if (saved && Number.isInteger(saved.chapter) && document.querySelector(`.chapter-list a[href="read-${link.dataset.book}-${saved.chapter}.html"]`)) {
    link.href = `read-${link.dataset.book}-${saved.chapter}.html`;
    link.textContent = `接着读 · 第 ${saved.chapter} 章 ↗`;
  }
} catch { /* Private browsing and unavailable storage still permit reading. */ }
