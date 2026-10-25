"""Generate the static teaching diagrams for DS chapters 01 to 10."""
from pathlib import Path
from html import escape
OUT=Path(__file__).resolve().parent.parent/'图片'
OUT.mkdir(exist_ok=True)
def t(x,y,s,size=22,color='#172c40',anchor='start'):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(str(s))}</text>'
def box(x,y,w,h,fill='#fff',stroke='#667c90'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def save(name,w,h,parts):
 head=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="#56748c"/></marker></defs><rect width="100%" height="100%" fill="#fafcfe"/><g font-family="PingFang SC,Noto Sans CJK SC,Arial,sans-serif">'
 (OUT/name).write_text((head+''.join(parts)+'</g></svg>').replace('→',' -> ').replace('←',' <- '))
def row(y,label,vals,colors=None,hit=-1,x=290,cw=110):
 p=[t(24,y+33,label)]
 for i,v in enumerate(vals):
  c=colors[i] if colors else '#fff'
  p+=[box(x+i*cw,y,cw-8,48,c,'#dc7a26' if i==hit else '#667c90'),t(x+i*cw+(cw-8)/2,y+32,v,22,anchor='middle')]
 return p
def arrow(x,y,u,v):
 return f'<path d="M{x},{y} L{u},{v}" stroke="#56748c" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>'

p=[t(24,42,'求和：绿色已经加过，橙框即将读取',27)]
for k,s in enumerate([0,6,4,9,10]):
 p+=row(85+k*90,f'i={k}, s={s}',[6,-2,5,1],['#d4efdf' if j<k else '#fff' for j in range(4)],hit=k)
p+=[t(341,550,'0',19,anchor='middle'),t(451,550,'1',19,anchor='middle'),t(561,550,'2',19,anchor='middle'),t(671,550,'3',19,anchor='middle'),t(24,625,'i=4只表示到达尾后边界；不读取不存在的a[4]。',22)]
save('ds-v3-01-sum.svg',1000,665,p)

p=[t(24,42,'循环次数：每个点都是一次主体操作',27)]
for i in range(5):
 p+=[t(30,105+i*55,f'i={i}')]
 for j in range(i):p+=[f'<circle cx="{170+j*55}" cy="{98+i*55}" r="10" fill="#287ba6"/>']
 p+=[t(460,105+i*55,f'{i}次')]
p+=[t(24,400,'0+1+2+3+4=10',25),t(24,465,'翻倍：数值1→32，只有5次更新',25)]
for i,val in enumerate([1,2,4,8,16,32]):
 x=24+i*155;p+=[box(x,500,105,52,'#e3f0fb'),t(x+52,536,val,24,anchor='middle'),t(x+52,590,f'k={i}',20,anchor='middle')]
 if i<5:p+=[arrow(x+112,525,x+148,525)]
save('ds-v3-02-count.svg',1000,630,p)

p=[t(24,42,'递归求[4,1,7]之和：进入后留下待办，返回后完成待办',26)]
states=[('进入i=0',['i=0：等返回后加4']),('进入i=1',['i=0：等返回后加4','i=1：等返回后加1']),('进入i=2',['i=0：等返回后加4','i=1：等返回后加1','i=2：等返回后加7']),('i=3返回0',['i=0：等返回后加4','i=1：等返回后加1','i=2：7+0=7']),('回到i=1',['i=0：等返回后加4','i=1：1+7=8']),('回到i=0',['i=0：4+8=12'])]
for k,(lab,frames) in enumerate(states):
 col=k%3;r=k//3;x=24+col*330;y=90+r*300
 p+=[t(x,y,lab,23)]
 for j,s in enumerate(frames):p+=[box(x,y+25+j*65,305,54,'#e3f0fb'),t(x+12,y+60+j*65,s,19)]
p+=[t(24,710,'每框是一次尚未返回的调用；数组仍是同一份。',22)]
save('ds-v3-03-recursion.svg',1030,750,p)

p=[t(24,42,'下标1前插15：先保住右边还没搬走的数据',27)]
vals=[[10,20,30,40,'空'],[10,20,30,40,40],[10,20,30,30,40],[10,20,20,30,40],[10,15,20,30,40]]
labels=['开始，size=4','写a[4]=a[3]','写a[3]=a[2]','写a[2]=a[1]','写a[1]=15，size=5']
for k,v in enumerate(vals):p+=row(85+k*85,labels[k],v,hit=[-1,4,3,2,1][k],cw=105)
p+=[t(24,560,'先向右搬后缀，再填空位。重复值只是搬迁中的副本。',22)]
save('ds-v3-04-shift.svg',1000,600,p)

p=[t(24,42,'lower_bound([1,3,3,7,9],3)：找第一个不小于3的位置',25)]
states=[('lo=0, hi=5, mid=2',['#fff']*5,2),('3不小于3 → hi=2',['#fff']*2+['#d9eafa']*3,1),('3不小于3 → hi=1',['#fff']+['#d9eafa']*4,0),('1小于3 → lo=1',['#d4efdf']+['#d9eafa']*4,-1)]
for k,(s,c,h) in enumerate(states):p+=row(95+k*100,s,[1,3,3,7,9],c,h,x=365,cw=105)
p+=[t(24,545,'绿色：已确认小于目标。蓝色：已确认不小于目标。',21),t(24,585,'白色：还没分类。最后lo=hi=1，返回边界1。',21)]
save('ds-v3-05-binary.svg',1000,625,p)

p=[t(24,42,'插入排序[4,1,3,2]：橙框是本次写入位置',26)]
states=[('开始',[4,1,3,2],-1),('x=1，右移4',[4,4,3,2],1),('写回x=1',[1,4,3,2],0),('x=3，右移4',[1,4,4,2],2),('写回x=3',[1,3,4,2],1),('x=2，右移4',[1,3,4,4],3),('继续右移3',[1,3,3,4],2),('写回x=2',[1,2,3,4],1)]
for k,(s,v,h) in enumerate(states):p+=row(85+k*72,s,v,hit=h,x=300)
save('ds-v3-06-insertion.svg',850,700,p)

p=[t(24,42,'归并排序[2,4,1,3]：先拆开，等子问题返回后再合并',25)]
for x,y,txt in [(395,75,'[2,4,1,3]'),(180,175,'[2,4]'),(610,175,'[1,3]'),(90,275,'[2]'),(290,275,'[4]'),(520,275,'[1]'),(720,275,'[3]')]:
 p+=[box(x,y,160,48,'#e3f0fb'),t(x+80,y+32,txt,23,anchor='middle')]
for a,b,c,d in [(420,130,260,170),(535,130,680,170),(220,230,170,270),(280,230,360,270),(650,230,600,270),(710,230,790,270)]:p+=[arrow(a,b,c,d)]
p+=[t(24,380,'最后合并：L=[2,4]，R=[1,3]；橙框是这次输出',23)]
for k,(s,v) in enumerate([('取右1，j=1',[1,'空','空','空']),('取左2，i=1',[1,2,'空','空']),('取右3，j=2',[1,2,3,'空']),('右空，接剩余4',[1,2,3,4])]):p+=row(415+k*75,s,v,hit=k,x=340)
save('ds-v3-06-merge.svg',1000,745,p)

p=[t(24,42,'在B之前插X：四根字段逐次写入',27)]
states=[('0 旧表，X未接入','B','未设','未设','A'),('1 X.pred=A','B','A','未设','A'),('2 X.succ=B','B','A','B','A'),('3 A.succ=X','X','A','B','A'),('4 B.pred=X，接好','X','A','B','X')]
for k,(lab,asu,xpr,xsu,bpr) in enumerate(states):
 y=88+k*150;p+=[t(24,y+35,lab,22)]
 for x,title,line1,line2 in [(330,'A','pred=原前驱','succ='+asu),(545,'X','pred='+xpr,'succ='+xsu),(760,'B','pred='+bpr,'succ=原后继')]:
  p+=[box(x,y,190,112,'#d4efdf' if k==4 else '#fff'),t(x+95,y+29,title,24,anchor='middle'),t(x+12,y+65,line1,20),t(x+12,y+94,line2,20)]
p+=[t(24,875,'每个框的pred/succ是两格独立地址；一次赋值只改其中一格。',21),t(24,915,'最终四条：A.succ=X；X.pred=A；X.succ=B；B.pred=X。',21)]
save('ds-v3-07-links.svg',1000,955,p)

p=[t(24,42,'单向反转：prev管已反转部分，cur管尚未处理部分',26)]
for k,(lab,left,right) in enumerate([('开始','空','A → B → C → 空'),('先存B，再改A.next','A → 空','B → C → 空'),('先存C，再改B.next','B → A → 空','C → 空'),('先存空，再改C.next','C → B → A → 空','空')]):
 y=95+k*120;p+=[t(24,y,lab,22),box(30,y+20,445,60,'#d4efdf'),t(50,y+60,'prev: '+left,22),box(505,y+20,465,60,'#e3f0fb'),t(525,y+60,'cur: '+right,22)]
save('ds-v3-07-reverse.svg',1000,590,p)

p=[t(24,42,'3*(2+4)：O等运算，V存值；都从底写到顶',26)]
states=[('读3','空','3'),('读*','*','3'),('读(','* , (','3'),('读2','* , (','3 , 2'),('读+','* , ( , +','3 , 2'),('读4','* , ( , +','3 , 2 , 4'),('遇)，执行2+4','* , (','3 , 6'),('丢弃配对(','*','3 , 6'),('结束，执行3*6','空','18')]
for k,(lab,o,v) in enumerate(states):
 y=85+k*75;p+=[t(24,y+35,lab,21),box(320,y,285,50,'#e3f0fb'),t(335,y+34,'O: '+o,22),box(635,y,320,50,'#d4efdf'),t(650,y+34,'V: '+v,22)]
save('ds-v3-08-expression.svg',1000,800,p)

p=[t(24,42,'双栈队列：只在out空时转移',27)]
states=[('入A,B,C','A,B,C','空'),('转C','A,B','C'),('转B','A','C,B'),('转A','空','C,B,A'),('弹out，返回A','空','C,B'),('再入D','D','C,B'),('弹out，返回B','D','C')]
for k,(lab,a,b) in enumerate(states):
 y=85+k*72;p+=[t(24,y+34,lab,22),box(310,y,270,48,'#e3f0fb'),t(325,y+33,'in: '+a,22),box(615,y,340,48,'#d4efdf'),t(630,y+33,'out: '+b,22)]
p+=[t(24,635,'队列顺序=out从顶到底，再接in从底到顶。',22)]
save('ds-v3-09-queues.svg',1000,680,p)

p=[t(24,42,'同一棵树：左/右位置固定，输出顺序由访问时机决定',25)]
positions={'A':(500,105),'B':(280,225),'C':(720,225),'D':(160,345),'E':(400,345),'F':(840,345)}
for a,b in [('A','B'),('A','C'),('B','D'),('B','E'),('C','F')]:
 x,y=positions[a];u,v=positions[b];p+=[f'<line x1="{x}" y1="{y+20}" x2="{u}" y2="{v-25}" stroke="#58758d" stroke-width="3"/>']
for label,(x,y) in positions.items():p+=[f'<circle cx="{x}" cy="{y}" r="29" fill="#e3f0fb" stroke="#287ba6" stroke-width="2"/>',t(x,y+8,label,25,anchor='middle')]
p+=[t(260,430,'先序：A B D E C F（根、左、右）',24),t(260,480,'中序：D B E A C F（左、根、右）',24),t(260,530,'后序：D E B F C A（左、右、根）',24),t(24,600,'重建根A：先序首项是根；中序根的位置分开左右子树。',23)]
p+=row(635,'先序',[ 'A','B','D','E','C','F'],['#ffe5c5']+['#d4efdf']*3+['#d9eafa']*2,x=250,cw=110)
p+=row(715,'中序',['D','B','E','A','C','F'],['#d4efdf']*3+['#ffe5c5']+['#d9eafa']*2,x=250,cw=110)
p+=[t(24,815,'绿：左子树三项。橙：根A。蓝：右子树两项。',22)]
save('ds-v3-10-tree.svg',1000,855,p)
