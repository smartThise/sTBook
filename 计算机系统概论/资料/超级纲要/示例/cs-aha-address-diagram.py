from pathlib import Path
from html import escape
out=Path(__file__).resolve().parents[1]/'图片/cs-aha-07-addresspaths.svg'
items=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="680" viewBox="0 0 1200 680">',
'<defs><marker id="a" markerWidth="9" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="#34738d"/></marker></defs>',
'<rect width="1200" height="680" fill="white"/>',
'<style>text{font-family:"Arial Unicode MS","PingFang SC","Noto Sans CJK SC",sans-serif;fill:#173442}.mono{font-family:monospace}</style>']
def text(x,y,s,size=18,anchor='start',cls=''):
 items.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" class="{cls}">{escape(s)}</text>')
def box(x,y,w,h,fill='#f3f7fa',stroke='#829ba8'):
 items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}" stroke="{stroke}"/>')
def arrow(x1,y1,x2,y2):
 items.append(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="#34738d" stroke-width="2.5" marker-end="url(#a)"/>')
text(35,38,'同样读取第1行第2列：连续矩阵与指针表',25)
box(20,62,555,590,'#fbfdfe');box(595,62,585,590,'#fbfdfe')
text(42,99,'连续矩阵 m[3][4]',22);text(42,130,'每项 int 4字节；行跨度16字节',17)
text(618,99,'p 指向三根 int 指针',22);text(618,130,'指针表从0x5000开始；每根指针8字节',17)
for r in range(3):
 y=165+r*82
 text(43,y+29,f'第{r}行',17)
 for c in range(4):
  x=140+c*103;chosen=r==1 and c==2
  box(x,y,95,62,'#ffe5bd' if chosen else '#e9f1f5')
  text(x+47.5,y+25,str((r+1)*10+c),20,'middle')
  text(x+47.5,y+49,f'0x{0x1000+(r*4+c)*4:04X}',14,'middle','mono')
 ptr=0x7000 if r==0 else (0x9000 if r==1 else 0xB000)
 x=617
 box(x,y,169,62,'#fff0cf' if r==1 else '#eef5f8')
 text(x+12,y+24,f'p[{r}] = 0x{ptr:04X}',17)
 text(x+12,y+48,f'位于0x{0x5000+r*8:04X}',15)
 arrow(789,y+31,862,y+31)
 for c in range(4):
  cx=875+c*70;chosen=r==1 and c==2
  box(cx,y,64,62,'#ffe5bd' if chosen else '#e9f1f5')
  text(cx+32,y+25,str((r+1)*10+c),20,'middle')
  text(cx+32,y+49,f'0x{ptr+c*4:04X}',12,'middle','mono')
text(42,453,'1. 算出第二行：0x1000 + 16 = 0x1010',17)
text(42,490,'2. 再跨两项：0x1010 + 8 = 0x1018',17)
text(42,527,'3. 从0x1018读取一个int，得到22',17)
text(42,581,'0x1010处是整数20，没有另存一根行指针。',16)
text(618,453,'1. 读表项：0x5000 + 1×8 = 0x5008',17)
text(618,490,'2. 表项给出行起点0x9000',17)
text(618,527,'3. 再到0x9000 + 2×4 = 0x9008，读得22',17)
text(618,581,'行可分散；先读指针，再沿它读取int。',16)
text(42,620,'橙色标最终读取的对象；所有地址为本例手算值。',16)
items.append('</svg>')
out.write_text('\n'.join(items))
print(out)
