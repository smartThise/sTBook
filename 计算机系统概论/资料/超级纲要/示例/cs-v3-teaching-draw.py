"""Static state diagrams. Run directly; no book build or external packages needed."""
from pathlib import Path
from html import escape
OUT=Path(__file__).resolve().parent.parent/'图片'
def t(x,y,s,size=22,color='#172c40',anchor='start'):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(str(s))}</text>'
def box(x,y,w,h,fill='#fff',stroke='#667c90'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def ar(x,y,u,v,color='#56748c'):
 return f'<path d="M{x},{y} L{u},{v}" fill="none" stroke="{color}" stroke-width="2.5" marker-end="url(#arrow)"/>'
def save(name,w,h,p):
 h0=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="#56748c"/></marker></defs><rect width="100%" height="100%" fill="#fafcfe"/><g font-family="PingFang SC,Noto Sans CJK SC,Arial,sans-serif">'
 (OUT/name).write_text((h0+''.join(p)+'</g></svg>').replace('→',' -> ').replace('←',' <- ').replace('×','*').replace('²','^2'))
def row(y,label,vals,x=285,cw=80,colors=None):
 p=[t(22,y+31,label,21)]
 for i,v in enumerate(vals):
  p+=[box(x+i*cw,y,cw-5,45,colors[i] if colors else '#fff'),t(x+i*cw+(cw-5)/2,y+30,v,21,anchor='middle')]
 return p

p=[t(22,40,'八位补码：先读位权，再做固定宽度加法',27)]
p+=row(85,'补码位权',[-128,64,32,16,8,4,2,1])
for k,(lab,bits) in enumerate([('+37','00100101'),('逐位取反','11011010'),('再加1：编码-37','11011011')]):p+=row(160+k*75,lab,list(bits))
p+=[t(22,415,'250+10：下表从低位i=0向高位i=7传播进位',23)]
for k,(lab,vals) in enumerate([('位i',list(range(8))),('传入进位',[0,0,1,0,1,1,1,1]),('本列和',[0,2,1,2,2,2,2,2]),('结果位（低位在左）',[0,0,1,0,0,0,0,0]),('传出进位',[0,1,0,1,1,1,1,1])]):p+=row(450+k*65,lab,vals)
p+=[t(22,825,'从高位倒读结果00000100=4；最后进位1落在第9位，被截掉。',22)]
save('cs-v3-02-bits.svg',1000,865,p)

p=[t(22,40,'5.25编码binary32：先求数值，再放位域',27)]
for y,title,detail in [(90,'5.25 = 101.01（二进制）','5=101；0.25=.01'),(190,'101.01 = 1.0101 × 2²','小数点左移2格，E=2'),(290,'q = E+127 = 129 = 10000001','s=0；F保存隐藏1之后的0101')]:
 p+=[box(25,y,940,72,'#e3f0fb'),t(45,y+30,title,23),t(45,y+58,detail,20)]
p+=[t(22,425,'抽象32位串（不是小端字节顺序）',23)]
for x,w,lab,v,c in [(25,90,'s：1位','0','#ffe5c5'),(125,260,'q：8位','10000001','#d4efdf'),(395,570,'F：23位','01010000000000000000000','#e3f0fb')]:
 p+=[t(x,470,lab,21),box(x,485,w,60,c),t(x+w/2,525,v,22,anchor='middle')]
p+=[t(22,610,'位串十六进制：40 A8 00 00；小端内存低地址到高地址：00 00 A8 40。',21),t(22,655,'反解：(1+1/4+1/16) × 4 = 1.3125 × 4 = 5.25。',22)]
save('cs-v3-03-float.svg',1000,700,p)

p=[t(22,40,'rax的八个字节：从高位到低位排列',27)]
states=[('初始',['11','22','33','44','55','66','77','88']),('写al=AA',['11','22','33','44','55','66','77','AA']),('写ax=BBBB',['11','22','33','44','55','66','BB','BB']),('写eax=CCCCDDDD',['00','00','00','00','CC','CC','DD','DD'])]
for k,(lab,v) in enumerate(states):p+=row(85+k*67,lab,v,x=290,cw=78)
p+=[t(22,405,'交换：保存旧值以后才覆盖内存',25)]
for k,(lab,v) in enumerate([('初始',['未知','未知',7,19]),('加载*p',[7,'未知',7,19]),('加载*q',[7,19,7,19]),('写*p=rdx',[7,19,19,19]),('写*q=rax',[7,19,19,7])]):p+=row(470+k*65,lab,v,x=380,cw=135)
for i,lab in enumerate(['rax','rdx','内存0x1000','内存0x2000']):p+=[t(380+i*135+65,450,lab,18,anchor='middle')]
p+=[t(22,845,'第三行后两处都19也没丢7，因为旧7仍在rax。',22)]
save('cs-v3-04-registers.svg',1000,890,p)

p=[t(22,40,'n=3,val=4：每次跳回顶部之前都推进i',27)]
nodes=[(330,80,300,65,'初始化 i=0,x=0'),(330,210,300,65,'顶部检查 i<n？'),(330,340,300,65,'x加2'),(330,470,300,65,'内部检查 x>val？'),(710,470,220,65,'x再加3'),(330,620,300,65,'i加1，回顶部'),(710,210,220,65,'退出，返回x')]
for x,y,w,h,s in nodes:p+=[box(x,y,w,h,'#e3f0fb'),t(x+w/2,y+40,s,23,anchor='middle')]
for a,b,c,d in [(480,145,480,205),(480,275,480,335),(480,405,480,465),(630,500,705,500),(480,535,480,615),(630,242,705,242)]:p+=[ar(a,b,c,d)]
p+=[ar(820,535,620,615),t(650,230,'否',21),t(490,305,'是',21),t(650,487,'是',21),t(490,580,'否',21),f'<path d="M330,652 L240,652 L240,242 L325,242" stroke="#56748c" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>',t(22,760,'本例每轮末(i,x)：(1,2)、(2,4)、(3,9)。',24),t(22,810,'顶部第四次看见3>=3，直接退出，不再多加2。',23)]
save('cs-v3-05-flow.svg',1000,855,p)

p=[t(22,40,'combine调用helper：每个栈格8字节，低地址在下面',26)]
for k,(addr,v) in enumerate([('0x7FF8','外部调用者返回地址'),('0x7FF0','保存的旧rbx=99'),('0x7FE8','回combine的返回地址')]):
 y=110+k*100;p+=[t(22,y+45,addr,23),box(165,y,350,78,'#e3f0fb'),t(340,y+46,v,23,anchor='middle')]
p+=[t(22,445,'helper入口：rsp=0x7FE8；rbx=5。',22)]
for k,(lab,sp) in enumerate([('combine入口','7FF8'),('push rbx','7FF0'),('call helper','7FE8'),('helper ret','7FF0'),('pop rbx','7FF8'),('combine ret','8000')]):
 y=105+k*65;p+=[t(560,y+30,lab,21),box(800,y,160,45,'#d4efdf'),t(880,y+31,'0x'+sp,21,anchor='middle')]
p+=[t(22,560,'helper返回10后：add把rax变15；pop恢复rbx为99；ret不改rax。',22),t(22,610,'rsp只恢复位置，不自动把刚释放栈格的旧字节清零。',22)]
save('cs-v3-06-stack.svg',1000,655,p)

p=[t(22,40,'相同成员，不同顺序：每格1字节',27)]
for k,(lab,labels,colors) in enumerate([
 ('A：char,double,int',['c']+['填']*7+['d']*8+['i']*4+['填']*4,['#ffe5c5']+['#e7e9ed']*7+['#d4efdf']*8+['#d9eafa']*4+['#e7e9ed']*4),
 ('B：double,int,char',['d']*8+['i']*4+['c']+['填']*3,['#d4efdf']*8+['#d9eafa']*4+['#ffe5c5']+['#e7e9ed']*3)]):
 y=115+k*180;p+=[t(22,y-25,lab,23)]
 for i,(lab2,c) in enumerate(zip(labels,colors)):
  x=110+i*35;p+=[t(x+16,y-4,i,15,anchor='middle'),box(x,y+8,32,48,c),t(x+16,y+40,lab2,18,anchor='middle')]
p+=[t(22,530,'A共24字节，对齐8；B共16字节，对齐8。灰格是内部/尾部填充。',22),t(22,585,'数组中的第二项要按整个sizeof跨过去，不能只加成员净大小13。',22)]
save('cs-v3-07-layout.svg',1000,630,p)

p=[t(22,40,'近相对call：五字节指令，位移相对下一条',27)]
for i,(a,b) in enumerate([('400100','E8'),('400101','FB'),('400102','00'),('400103','00'),('400104','00')]):
 x=30+i*165;p+=[t(x+70,110,'0x'+a,21,anchor='middle'),box(x,130,140,70,'#ffe5c5' if i==0 else '#d9eafa'),t(x+70,175,b,28,anchor='middle')]
p+=[box(30,265,920,80,'#e3f0fb'),t(50,300,'目标S：0x400200',25),t(50,330,'下一条：0x400105；位移：0x400200 - 0x400105 = 0xFB',22),ar(430,210,430,255),t(30,410,'小端字段 FB 00 00 00 解码为 +251。',24),t(30,465,'CPU核对：0x400105 + 0xFB = 0x400200。',24),t(30,525,'若误从call起点减，会错算0x100，实际跳到0x400205。',23)]
save('cs-v3-08-relocation.svg',1000,575,p)

p=[t(22,40,'两条无条件fork：创建关系不等于运行先后',27)]
for a,b,c,d in [(500,165,260,260),(500,165,750,260),(260,355,260,450)]:p+=[ar(a,b,c,d)]
for x,y,title,ret in [(350,80,'P (PID100)','r1=101, r2=102'),(110,265,'C1 (PID101)','r1=0, r2=103'),(600,265,'C2 (PID102)','r1=101, r2=0'),(110,455,'C3 (PID103)','r1=0, r2=0')]:
 p+=[box(x,y,300,90,'#d9eafa'),t(x+150,y+35,title,24,anchor='middle'),t(x+150,y+70,ret,23,anchor='middle')]
p+=[t(80,220,'P第一次fork',21),t(685,220,'P第二次fork',21),t(280,420,'C1第二次fork',21),t(22,620,'PID只是示意编号。C2继承已执行第一条后的r1，不重跑程序。',22)]
save('cs-v3-09-fork.svg',1000,670,p)

p=[t(22,40,'信号先到时：坏的等待丢窗口，正确等待保留挂起',25)]
bad=['读done=0，决定等待','信号递送：done=1','处理函数已返回','主程序才进入pause','没有后续信号，睡住']
good=['先屏蔽：blocked=1','raise：pending=1，flag=0','检查flag=0','sigsuspend原子解除并等待','挂起信号递送：flag=1','返回后先恢复屏蔽，再重查']
p+=[t(45,100,'检查后再pause',24),t(530,100,'屏蔽后sigsuspend',24)]
for col,vals in enumerate([bad,good]):
 for k,s in enumerate(vals):
  x=25+col*500;y=130+k*80;p+=[box(x,y,460,58,'#ffe2dc' if col==0 else '#d4efdf'),t(x+14,y+36,s,21)]
  if k<len(vals)-1:p+=[ar(x+230,y+60,x+230,y+76)]
p+=[t(22,690,'flag/requested是程序状态；pending是内核的待递送通知，不能混为一格。',21)]
save('cs-v3-10-signals.svg',1030,735,p)

p=[t(22,40,'写时复制：父子虚拟地址不变，父映射和内容改变',26)]
for col,lab in enumerate(['写入前','父写入20后']):
 x=25+col*500;p+=[t(x,100,lab,25)]
 for y,s in [(145,'父：VA0x0520 / VPN5'),(285,'子：VA0x0520 / VPN5')]:p+=[box(x,y,265,65,'#d9eafa'),t(x+12,y+38,s,19)]
 if col==0:
  p+=[box(x+310,210,150,105,'#d4efdf'),t(x+385,245,'物理页框9',21,anchor='middle'),t(x+385,280,'偏移0x20: 7',20,anchor='middle'),ar(x+267,177,x+305,240),ar(x+267,317,x+305,285)]
 else:
  for y,page,v in [(145,'12 (0x0C)',20),(285,'9',7)]:
   p+=[box(x+310,y,150,85,'#d4efdf'),t(x+385,y+29,'页框'+page,18,anchor='middle'),t(x+385,y+62,'偏移0x20: '+str(v),20,anchor='middle'),ar(x+267,y+33,x+305,y+33)]
p+=[t(22,470,'页大小256字节，偏移0x20。页框12按十进制编号，即0x0C。',22),t(22,525,'父物理位置0x0C20值20；子物理位置0x0920值7。',22),t(22,580,'顺序：分新页并复制 → 改父映射 → 重试父写入；子映射不改。',21)]
save('cs-v3-11-cow.svg',1030,625,p)

p=[t(22,40,'128字节教学堆：右端不包含；灰蓝块空闲',27)]
states=[('初始',[('空闲',128)]),('分A32',[('A',32),('空闲',96)]),('分B40',[('A',32),('B',40),('空闲',56)]),('分C24',[('A',32),('B',40),('C',24),('空闲',32)]),('释放B',[('A',32),('空闲',40),('C',24),('空闲',32)]),('释放A并合并',[('空闲',72),('C',24),('空闲',32)]),('请求D64，给72',[('D',72),('C',24),('空闲',32)]),('释放C并合并',[('D',72),('空闲',56)]),('释放D并合并',[('空闲',128)])]
for k,(lab,blocks) in enumerate(states):
 y=95+k*83;x=230;off=0;p+=[t(22,y+38,lab,21)]
 for name,size in blocks:
  w=size*5.7;p+=[box(x,y,w-2,52,'#e3f0fb' if name=='空闲' else '#d4efdf'),t(x+w/2,y+33,f'{name}{size}',19,anchor='middle'),t(x,y+73,off,16)]
  x+=w;off+=size
 p+=[t(x,y+73,128,16,anchor='end')]
p+=[t(22,900,'最小空闲块24；D占72时，剩8不能单独分块。块大小已含管理开销。',21)]
save('cs-v3-12-heap.svg',1000,945,p)

p=[t(22,40,'短读：只有绿色格属于当前已读有效数据',27)]
for k,(lab,done) in enumerate([('r=4，done=4',4),('r=3，done=7',7),('r=3，done=10',10)]):
 p+=row(100+k*90,lab,list('ABCDEFGHIJ'),x=250,cw=70,colors=['#d4efdf' if i<done else '#fff' for i in range(10)])
p+=[t(22,425,'短写ABCDE：下一次只写尚未接受的后缀',25)]
for k,(lab,done) in enumerate([('r=2，done=2',2),('r=2，done=4',4),('r=1，done=5',5)]):
 p+=row(470+k*85,lab,list('ABCDE'),x=300,cw=110,colors=['#d4efdf' if i<done else '#fff' for i in range(5)])
p+=[t(22,790,'第二次写从buf+2开始，长度3；不把AB再发一次。',22)]
save('cs-v3-13-shortio.svg',1000,835,p)

p=[t(22,40,'最后状态：fd1/fd3共用O1，fd2独用O2',27)]
for y,s in [(110,'fd1'),(255,'fd3 = dup(fd1)'),(400,'fd2 = open同路径')]:
 p+=[box(25,y,290,65,'#d9eafa'),t(170,y+40,s,22,anchor='middle')]
for x,y,s1,s2 in [(470,140,'O1 偏移5','已按次序读AB、CD、E'),(470,370,'O2 偏移1','只读了A')]:
 p+=[box(x,y,470,90,'#d4efdf'),t(x+235,y+36,s1,25,anchor='middle'),t(x+235,y+69,s2,21,anchor='middle')]
p+=[ar(317,143,465,173),ar(317,288,465,205),ar(317,433,465,415),box(455,550,475,75,'#ffe5c5'),t(690,596,'同一文件内容 ABCDEF',25,anchor='middle'),'<path d="M945,185 L990,185 L990,585 L935,585" fill="none" stroke="#56748c" stroke-width="2.5" marker-end="url(#arrow)"/>',ar(705,462,780,545),t(22,700,'两次open有两个偏移盒子；dup只多一根指向O1的引用。',22)]
save('cs-v3-13-fd.svg',1000,745,p)

p=[t(22,40,'两消费者被唤醒：先取得锁者可能已取走唯一元素',25)]
states=[('都在等','无',0,'等待','等待'),('放入并广播','生产者',1,'可唤醒','可唤醒'),('C1先取得锁','C1',1,'wait返回','等锁'),('C1取出并解锁','无',0,'完成get','等锁'),('C2终于取得锁','C2',0,'已离开','while重查为空'),('C2再次wait','无',0,'无关','释放锁，再等待')]
for i,lab in enumerate(['发生什么','锁归谁','count','C1','C2']):p+=[t([25,285,465,595,790][i],95,lab,22)]
for k,state in enumerate(states):
 y=125+k*86
 for x,w,val in zip([20,280,455,590,785],[250,165,125,185,205],state):
  p+=[box(x,y,w-5,62,'#e3f0fb'),t(x+10,y+39,val,20)]
p+=[t(22,700,'通知不预留元素；返回条件等待前，要重新取得同一把锁。',22)]
save('cs-v3-15-wait.svg',1030,745,p)

p=[t(22,40,'直接映射缓存：B=8，S=4，每组一行',27)]
p+=[t(22,90,'t=标记，B0=地址0..7，B1=8..15，B4=32..39。',22)]
states=[('0：未命中','t0/B0','无效','无效','无效'),('4：命中','t0/B0','无效','无效','无效'),('8：未命中','t0/B0','t0/B1','无效','无效'),('0：命中','t0/B0','t0/B1','无效','无效'),('32：未命中','t1/B4','t0/B1','无效','无效'),('0：未命中','t0/B0','t0/B1','无效','无效')]
for i in range(4):p+=[t(290+i*170+75,150,'组'+str(i),22,anchor='middle')]
for k,(lab,*vals) in enumerate(states):p+=row(180+k*83,lab,vals,x=290,cw=170)
p+=[t(22,735,'组2、3仍空，0与32也要在组0互相替换；不是“总容量已满”。',22)]
save('cs-v3-16-cache.svg',1030,780,p)

p=[t(22,40,'sum({4,-2,7},3)：地址、位串与累加器同时跟',26)]
for i,(addr,val) in enumerate([('0x1000','4'),('0x1008','-2'),('0x1010','7')]):
 x=250+i*235;p+=[t(x+100,105,addr,23,anchor='middle'),box(x,125,200,70,'#d4efdf'),t(x+100,168,val+' (long8字节)',22,anchor='middle')]
p+=[t(22,260,'-2的64位位串：0xFFFFFFFFFFFFFFFE。',23)]
for k,(lab,ra,rd) in enumerate([('初始化',0,0),('加地址1000的4',4,1),('加地址1008的-2',2,2),('加地址1010的7',9,3),('cmp 3-3=0，退出',9,3)]):
 y=315+k*75;p+=[t(22,y+33,lab,22),box(400,y,220,50,'#e3f0fb'),t(420,y+34,'rax='+str(ra),23),box(670,y,220,50,'#ffe5c5'),t(690,y+34,'rdx(i)='+str(rd),23)]
save('cs-v3-17-sum.svg',1000,740,p)

p=[t(22,40,'popcount(13)：下行留低位，回程才把低位加回来',26)]
p+=[t(50,95,'进入顺序',24),t(670,95,'返回后本层结果',24)]
for k,(n,bit,ans) in enumerate([(13,1,3),(6,0,2),(3,1,2),(1,1,1),(0,None,0)]):
 y=125+k*100;p+=[box(40,y,390,65,'#e3f0fb'),t(60,y+40,f'x={n}，'+('基础情况返回0' if bit is None else f'留下低位{bit}'),23),box(630,y,320,65,'#d4efdf'),t(650,y+40,f'x={n}层返回{ans}',23)]
 if k<4:p+=[ar(235,y+68,235,y+97),ar(790,y+97,790,y+68)]
p+=[t(22,700,'最外层最终恢复原rbx=99；结果rax=3。不是所有层都保留相同n。',22)]
save('cs-v3-18-popcount.svg',1000,745,p)

p=[t(22,40,'malloc 10个int：范围[0x1000,0x1028)，每项4字节',25)]
for i in range(11):
 x=35+i*86;c='#d4efdf' if i<10 else '#ffd6cc'
 p+=[t(x+37,115,'i='+str(i),20,anchor='middle'),box(x,135,76,65,c,'#bb4633' if i==10 else '#667c90'),t(x+37,176,str(i),22,anchor='middle')]
p+=[t(35,250,'0x1000',22),t(800,250,'0x1024',22),t(890,300,'0x1028：尾后',20,anchor='end'),ar(932,205,930,270)]
for k,(s,c) in enumerate([('i=9：写0x1024..0x1027，仍合法','#d4efdf'),('i=10：写0x1028..0x102B，第一次越界','#ffd6cc'),('之后free：可能此时才发现之前的损坏','#ffe5c5')]):
 y=370+k*95;p+=[box(35,y,920,65,c),t(55,y+40,s,24)]
p+=[t(22,710,'红格在对象之外；它实际属于谁，不由这个程序的分配请求决定。',22)]
save('cs-v3-19-boundary.svg',1030,755,p)
