"""Import the author's existing manuscripts without modifying the original books."""
from pathlib import Path
import re, json, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent
OUT = ROOT / 'dist'
BOOKS = [
 dict(id='season1', title='可安，向晨', season='第一季', genre='都市 · 青春 · 心动', status='已完结', subtitle='从游戏搭子开始，把喜欢慢慢说出口。', description='一条寻找游戏搭子的帖子，让林向晨的日常里多了一个人。从屏幕那端的陪伴，到想要越过的距离，一段关系在一次次回应中，慢慢有了名字。', folder='可安，向晨', pdf='main.pdf', volumes=['从游戏搭子开始','不该越界的心动','想要说出口','隔着城市拥抱你']),
 dict(id='season2', title='可安，向晨', season='第二季', genre='都市 · 恋爱 · 成长', status='连载中', subtitle='从一句「下次见」开始，把往后的日子继续写下去。', description='热恋之后，他们回到各自的日常。实习、工作、错开的时间，还有迟迟未读的消息。喜欢让两个人走到一起，而理解与沟通，让他们学着一起走下去。', folder='可安，向晨II', pdf='main.pdf', volumes=['未读的夜晚']),
 dict(id='yueyin', title='月隐之证', season='', genre='悬疑 · 推理', status='已完结', subtitle='月光之下，每个人都有未曾说出口的秘密。', description='林歆月踏入月亮山庄，也踏入了一场与往事紧密相连的迷局。当死亡接连发生，信任开始瓦解，她必须穿过谎言与伪装，寻找被隐藏的真相。', folder='月隐之证', pdf='main-updated.pdf', volumes=['月隐之证']),
]

def command_args(text, name):
    """Balanced braces, so typeset groups cannot truncate manuscript text."""
    pattern=re.compile(r'\\'+name+r'\{')
    result=[]
    for m in pattern.finditer(text):
        depth=1; i=m.end(); start=i
        while i<len(text) and depth:
            if text[i]=='{' and text[i-1]!='\\': depth+=1
            if text[i]=='}' and text[i-1]!='\\': depth-=1
            i+=1
        if depth: raise ValueError('Unbalanced '+name)
        value=text[start:i-1]
        value=re.sub(r'\\([%&#_$\{\}])',r'\1',value)
        if re.search(r'\\[a-zA-Z]+',value): raise ValueError('Unhandled TeX in paragraph: '+value[:100])
        result.append(value)
    return result

for b in BOOKS:
    src=SOURCE/b['folder']; chapters=[]
    if b['id']!='yueyin':
        included=re.findall(r'\\include\{([^}]+)\}',(src/'main.tex').read_text(encoding='utf-8-sig'))
        files=[src/(name+'.tex') for name in included]
        for f in files:
            n=int(f.stem[2:]); text=f.read_text(encoding='utf-8-sig')
            title=command_args(text,'chapter')[0]
            paras=command_args(text,'cnpara')
            vol=(n-1)//6+1 if b['id']=='season1' else 5
            chapters.append(dict(number=n,title=title,volume=vol,paragraphs=paras))
    else:
        for f in sorted((src/'chapters_text').glob('ch*.txt')):
            n=int(f.stem[2:]); text=f.read_text(encoding='utf-8-sig').strip()
            lines=text.splitlines(); assert lines[0].startswith('第')
            paras=[p.strip().replace('\n','') for p in re.split(r'\n\s*\n','\n'.join(lines[1:])) if p.strip()]
            chapters.append(dict(number=n,title='',volume=1,paragraphs=paras))
    chapters.sort(key=lambda c:c['number'])
    target=OUT/'data'/b['id']; target.mkdir(parents=True,exist_ok=True)
    expected={f"{c['number']}.json" for c in chapters}
    for stale in target.glob('*.json'):
        if stale.name not in expected: stale.unlink()
    for c in chapters:
        assert c['paragraphs'], c
        (target/f"{c['number']}.json").write_text(json.dumps(c,ensure_ascii=False),encoding='utf-8')
    b['chapters']=[{k:v for k,v in c.items() if k!='paragraphs'} for c in chapters]
    b['wordCount']=sum(sum(len(re.sub(r'\s','',p)) for p in c['paragraphs']) for c in chapters)
    pdf_name=b['id']+'.pdf'; shutil.copy2(src/b['pdf'],OUT/'books'/pdf_name)
    b['pdf']='books/'+pdf_name
    b['pdfSize']=round((OUT/b['pdf']).stat().st_size/1024/1024,1)
    b['cover']='assets/'+b['id']+'.jpg'
    del b['folder']
(OUT/'data'/'books.json').write_text(json.dumps(BOOKS,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{ 'book': b['title']+b['season'], 'chapters':len(b['chapters']), 'characters':b['wordCount']} for b in BOOKS],ensure_ascii=False))
