from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, parse_qs, unquote
import json, hashlib, urllib.request
ROOT=Path(__file__).resolve().parents[1]; DIST=ROOT/'dist'
books=json.loads((DIST/'data/books.json').read_text(encoding='utf-8'))
byid={b['id']:b for b in books}
assert len(books)==3 and len(byid)==3
assert max(c['number'] for c in byid['season1']['chapters'])==24
assert min(c['number'] for c in byid['season2']['chapters'])==25
total=0
class ChapterText(HTMLParser):
    def __init__(self):
        super().__init__(); self.in_article=False; self.in_paragraph=False; self.paragraphs=[]; self.part=[]
    def handle_starttag(self,tag,attrs):
        if tag=='article' and dict(attrs).get('class')=='prose': self.in_article=True
        if tag=='p' and self.in_article: self.in_paragraph=True; self.part=[]
    def handle_data(self,data):
        if self.in_paragraph: self.part.append(data)
    def handle_endtag(self,tag):
        if tag=='p' and self.in_paragraph:
            self.paragraphs.append(''.join(self.part)); self.in_paragraph=False
        if tag=='article':self.in_article=False
for b in books:
    assert len({c['number'] for c in b['chapters']})==len(b['chapters'])
    actual={p.stem for p in (DIST/'data'/b['id']).glob('*.json')}
    assert actual=={str(c['number']) for c in b['chapters']}
    for c in b['chapters']:
        data=json.loads((DIST/'data'/b['id']/f"{c['number']}.json").read_text(encoding='utf-8'))
        assert data['title']==c['title'] and data['paragraphs']
        assert all(isinstance(p,str) and p.strip() for p in data['paragraphs'])
        chapter_page=DIST/f"read-{b['id']}-{c['number']}.html"
        parser=ChapterText(); parser.feed(chapter_page.read_text(encoding='utf-8'))
        assert parser.paragraphs==data['paragraphs'],f'Missing or changed static text: {chapter_page.name}'
        total+=1
    pdf=DIST/b['pdf']; assert pdf.read_bytes().startswith(b'%PDF-')
    request=urllib.request.Request('http://127.0.0.1:4173/'+b['pdf'],method='HEAD')
    with urllib.request.urlopen(request) as r:
        assert r.status==200 and int(r.headers['Content-Length'])==pdf.stat().st_size
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        for key in ('src','href'):
            value=attrs.get(key,'')
            if not value or value.startswith(('#','http:','https:','data:')):continue
            u=urlsplit(value); assert (DIST/unquote(u.path)).is_file(),value
            if u.path=='reader.html' and u.query:
                q=parse_qs(u.query); b=byid[q['book'][0]]
                assert int(q['chapter'][0]) in [c['number'] for c in b['chapters']],value
for file in DIST.glob('*.html'): Links().feed(file.read_text(encoding='utf-8'))
assert 'fetch(' not in (DIST/'reader-static.js').read_text(encoding='utf-8')
print(f'PASS: {len(books)} independent books, {total} complete HTML chapters matching manuscripts, no reader fetch, all page assets/links, and 3 PDF responses.')
