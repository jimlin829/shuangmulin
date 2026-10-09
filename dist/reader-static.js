(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const main = $('main');
  const escapeHTML = text => String(text).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const read = key => { try { return JSON.parse(localStorage.getItem('shuangmulin:' + key)); } catch { return null; } };
  const save = (key, value) => { try { localStorage.setItem('shuangmulin:' + key, JSON.stringify(value)); } catch {} };
  let size = Math.min(28, Math.max(16, Number(read('size')) || 20));
  let theme = read('theme') === 'night' ? 'night' : 'day';
  let toastTimer;
  function settings() {
    document.body.style.setProperty('--reader-size', size + 'px');
    document.body.dataset.theme = theme;
    $('theme-toggle').textContent = theme === 'night' ? '日读' : '夜读';
    $('theme-toggle').setAttribute('aria-pressed', String(theme === 'night'));
    $('smaller').disabled = size <= 16; $('larger').disabled = size >= 28;
  }
  function toast(message) {
    $('reader-toast').textContent = message; $('reader-toast').hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(() => $('reader-toast').hidden = true, 1500);
  }
  settings();
  $('smaller').onclick = () => { size = Math.max(16, size - 2); settings(); save('size',size); toast('字号 '+size); };
  $('larger').onclick = () => { size = Math.min(28, size + 2); settings(); save('size',size); toast('字号 '+size); };
  $('theme-toggle').onclick = () => { theme = theme === 'night' ? 'day' : 'night'; settings(); save('theme',theme); };
  const dialog = $('contents-dialog');
  $('open-contents').onclick = () => dialog.showModal();
  $('close-contents').onclick = () => dialog.close();
  dialog.addEventListener('click', event => { if (event.target === dialog) { const r=dialog.getBoundingClientRect(); if(event.clientX<r.left || event.clientX>r.right || event.clientY<r.top || event.clientY>r.bottom) dialog.close(); } });
  $('open-contents').disabled = false;
  $('bottom-contents').onclick = event => { event.preventDefault(); dialog.showModal(); };
  save(document.body.dataset.book, {chapter:Number(document.body.dataset.chapter)});
})();