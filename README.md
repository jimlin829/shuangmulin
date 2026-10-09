# 霜木林的个人书房

冰蓝色作者网站，包含作者介绍、三本独立作品、分章阅读和 PDF 下载。

## 三本作品

- `season1`：《可安，向晨》第一季，第 1–24 章。
- `season2`：《可安，向晨》第二季，第 25–28 章，连载中。
- `yueyin`：《月隐之证》，第 1–13 章。

两季独立拥有封面、书籍页面、目录、阅读记录和 PDF。正文保留原稿内容。网站不收集访客信息，阅读章节、字号和夜读偏好仅保存在访客设备的浏览器中。

## 本地预览

用 Python 在本文件夹运行 `python -m http.server 4173 --directory dist`，然后打开 `http://localhost:4173`。每一章的正文直接包含在 HTML 文件里，不需要另行请求 JSON；也可以直接打开 `dist/index.html` 阅读本地副本。

## 文件结构

- `dist/`：可部署的完整静态网站。
- `dist/data/books.json`：三本书的目录和介绍。
- `dist/data/<book>/<chapter>.json`：逐章正文。
- `dist/read-<book>-<chapter>.html`：含完整正文和上下章链接的独立阅读页；无 JavaScript 也能阅读。JavaScript 只增强字号、夜读、目录弹窗和本机阅读记录。
- `dist/reader.html`：兼容旧的带书籍和章节参数的链接，跳转到对应完整章节页。
- `dist/books/`：供读者下载的三个 PDF 文件。
- `dist/assets/`：原作者 logo、PDF 首页渲染的封面、自绘冰霜「林」图标及字体。
- `scripts/import-books.py`：从相邻的三本小说目录导入正文和 PDF，以各本 `main.tex` 实际引用的章节为准。
- `scripts/build-pages.py`：生成首页和独立书籍页。
- `scripts/subset-font.py`：按已导入的文本缩减思源宋体，仅包含本站用字。

## 更新内容

先把新章节加入对应小说的 `main.tex`，再运行 `scripts/import-books.py` 和 `scripts/build-pages.py`。如果加入了新的汉字，再运行 `scripts/subset-font.py`（需要 `fonttools[woff]`）。首页最新章入口在 `scripts/build-pages.py` 中生成。修改后重新发布网站，线上版本才会更新。

源小说文件不会被这些脚本改动。书籍封面是现有 PDF 的第一页；更新 PDF 封面后请同步重新渲染 `dist/assets/` 下对应的 JPG。

## 设计

遵循 Taste Skill，以原生 CSS 实现文学出版式编排。设计差异度 6、动效 3、信息密度 3：非对称书封构图、错落书架、纸白与冰蓝、宋体正文与清楚的阅读导航。动效仅用于交互反馈，尊重减少动态效果偏好。阅读器有独立日读、夜读主题。
