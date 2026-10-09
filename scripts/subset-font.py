from pathlib import Path
from fontTools import subset
ROOT=Path(__file__).resolve().parents[1]
chars=''.join(p.read_text(encoding='utf-8') for p in (ROOT/'dist').rglob('*') if p.suffix in ('.html','.js','.json'))
chars+=''.join(chr(i) for i in range(32,127))+'第一二三四五六七八九十章卷霜木林著未读的夜晚'
font=subset.load_font(str(ROOT.parent/'月隐之证/fonts/SourceHanSerifCN-Regular.otf'),subset.Options())
opts=subset.Options(); opts.flavor='woff2'; opts.name_IDs=[0,1,2,3,4,5,6,13,14]
s=subset.Subsetter(options=opts); s.populate(text=chars); s.subset(font)
for record in font['name'].names:
    if record.nameID in (1,3,4,6,16):
        record.string=('ShuangmulinBookSerif' if record.nameID==6 else 'Shuangmulin Book Serif').encode(record.getEncoding())
if 'CFF ' in font:
    font['CFF '].cff.fontNames=['ShuangmulinBookSerif']
    top=font['CFF '].cff.topDictIndex[0]
    top.FamilyName='Shuangmulin Book Serif'; top.FullName='Shuangmulin Book Serif'
font.flavor='woff2'; font.save(str(ROOT/'dist/assets/book-serif.woff2'))
print('Subset serif font saved.')
