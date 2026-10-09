/* Compatibility for previously shared reader.html?book=...&chapter=... links. */
(() => {
  const params = new URLSearchParams(location.search);
  const routes = JSON.parse(document.getElementById('reader-routes').textContent);
  const book = params.get('book');
  if (!Object.prototype.hasOwnProperty.call(routes, book)) return;
  const chapters = routes[book];
  const number = params.get('chapter') || Object.keys(chapters)[0];
  if (Object.prototype.hasOwnProperty.call(chapters, number)) {
    location.replace(chapters[number]);
  } else {
    document.getElementById('reader-message').textContent = '没有找到这一章，请从下面的作品入口重新选择。';
  }
})();
