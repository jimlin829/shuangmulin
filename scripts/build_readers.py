"""Put complete chapter text in HTML; reading must not depend on a fetch."""
import json, re, html

def build_readers(books, template, head, out):
    esc=html.escape
    routes={}
    for book in books:
        full=book['title']+(' · '+book['season'] if book['season'] else '')
        url=lambda n:f"read-{book['id']}-{n}.html"
        routes[book['id']]={str(c['number']):url(c['number']) for c in book['chapters']}
        for index,meta in enumerate(book['chapters']):
            c=json.loads((out/'data'/book['id']/f"{meta['number']}.json").read_text(encoding='utf-8'))
            num=c['number']; label=f'第 {num} 章'; title=c['title'] or label
            prev=book['chapters'][index-1] if index else None
            next=book['chapters'][index+1] if index+1<len(book['chapters']) else None
            body=f'<div class="reader-chapter-meta">{esc(full)}'+(' · '+label if c['title'] else '')+f'</div><h1 class="reader-heading">{esc(title)}</h1><p class="reader-byline">霜木林 著</p>'
            body+='<article class="prose" aria-label="章节正文">'+''.join('<p>'+esc(p)+'</p>' for p in c['paragraphs'])+'</article>'
            if not next:
                ending='已读到最新章，故事还在继续。' if book['status']=='连载中' else '第一季完。新的日常，在第二季继续。' if book['id']=='season1' else '全文完。感谢你读到这里。'
                body+='<p class="chapter-end">'+ending+'</p>'
            left=f'<a class="button secondary" href="{url(prev["number"])}">← 上一章</a>' if prev else f'<a class="button secondary" href="book-{book["id"]}.html">← 本书首页</a>'
            right=f'<a class="button" href="{url(next["number"])}">下一章 →</a>' if next else '<a class="button" href="book-season2.html">第二季 →</a>' if book['id']=='season1' else '<a class="button" href="index.html#library">回到书架 →</a>'
            body+=f'<nav class="chapter-navigation" aria-label="章节导航">{left}<a class="tool-button" id="bottom-contents" href="book-{book["id"]}.html#contents">目录</a>{right}</nav>'
            groups=[]
            for v in sorted(set(item['volume'] for item in book['chapters'])):
                name=book['volumes'][v-1 if book['id']=='season1' else 0]
                links=''.join(f'<li><a href="{url(item["number"])}"'+(' aria-current="page"' if item['number']==num else '')+f'><span class="chapter-no">第 {item["number"]} 章</span><span class="chapter-title">{esc(item["title"] or "第 "+str(item["number"])+" 章")}</span></a></li>' for item in book['chapters'] if item['volume']==v)
                groups.append('<details class="volume"'+(' open' if v==c['volume'] else '')+'><summary>'+('' if book['id']=='yueyin' else f'第 {v} 卷 · ')+esc(name)+'</summary><ol class="chapter-list">'+links+'</ol></details>')
            page=re.sub(r'^.*?</head>',lambda _:head(label+' '+c['title']+' · '+full,c['paragraphs'][0][:150]),template,count=1,flags=re.S)
            page=page.replace('<body class="reader-page">',f'<body class="reader-page" data-book="{book["id"]}" data-chapter="{num}">')
            page=re.sub(r'(<main class="reader-main" id="main">).*?(</main>)',lambda m:m[1]+body+m[2],page,flags=re.S)
            page=page.replace('<a id="reader-book-link" class="reader-title-link" href="index.html#library">在线阅读</a>',f'<a id="reader-book-link" class="reader-title-link" href="book-{book["id"]}.html">{esc(full)}</a>')
            page=page.replace('<h2 id="contents-title">章节目录</h2>',f'<h2 id="contents-title">{esc(full)}</h2>')
            page=page.replace('<div id="dialog-chapters"></div>','<div id="dialog-chapters">'+''.join(groups)+'</div>')
            page=page.replace('<a id="reader-download" class="text-link" href="index.html#library">',f'<a id="reader-download" class="text-link" href="{book["pdf"]}" download="{esc(full)}.pdf">')
            page=re.sub(r'<noscript>.*?</noscript>','',page,flags=re.S)
            page=page.replace('src="reader.js"','src="reader-static.js"')
            (out/url(num)).write_text(page,encoding='utf-8')
    # Preserve old bookmarks without fetching a manifest or manuscript.
    links=''.join(f'<p><a class="text-link" href="read-{b["id"]}-{b["chapters"][0]["number"]}.html">{esc(b["title"]+(" · "+b["season"] if b["season"] else ""))}</a></p>' for b in books)
    legacy=head('在线阅读','选择一本霜木林的小说，继续阅读。')+'<body><main class="wrap error" id="main"><h1>翻开一本故事</h1><p id="reader-message">选择你想阅读的作品。</p>'+links+'<a class="text-link" href="index.html#library">回到书架 →</a></main><script id="reader-routes" type="application/json">'+json.dumps(routes,ensure_ascii=False).replace('<','\\u003c')+'</script><script src="reader.js" defer></script></body></html>'
    (out/'reader.html').write_text(legacy,encoding='utf-8')
