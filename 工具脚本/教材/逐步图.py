#!/usr/bin/env python3
"""同一份操作记录生成纸面连续图与网页逐步播放器数据。"""
import html
import json
import math
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INK, MUTED, LINE = '#25332f', '#596c64', '#c6d2cc'
GREEN, ORANGE, BLUE = '#d7eee3', '#ffe2b6', '#dceaf7'


def el(tag, text='', **attrs):
    return {'tag': tag, 'attrs': {k.replace('_', '-'): str(v) for k, v in attrs.items()}, 'text': str(text)}


def label(text, x=20, y=25, size=17, color=INK):
    return el('text', text, x=x, y=y, font_size=size, fill=color,
              font_family='PingFang SC, Noto Sans CJK SC, sans-serif')


def row(values, y=55, name='数组', active=(), notes=None, colors=None, x0=140, cellwidth=None):
    out = [label(name, 20, y+27)]
    width = cellwidth or min(82, 630/max(1, len(values)))
    for i, v in enumerate(values):
        x = x0+i*width
        out += [el('rect', x=x, y=y, width=width-3, height=42, rx=3,
                   fill=ORANGE if i in active else (colors or {}).get(i,'#f5f8f6'), stroke=LINE),
                label(v, x+10, y+28), label(i, x+10, y+60, 12, MUTED)]
        if notes and i in notes:
            out.append(label(notes[i], x+5, y-9, 13, MUTED))
    if not values:
        out.append(label('空', 150, y+27, 16, MUTED))
    return out


def tree(nodes, edges, active=()):
    # nodes: id -> (value, x, y, optional fill)
    out = []
    for a, b in edges:
        na, nb = nodes[a], nodes[b]
        out.append(el('line', x1=na[1], y1=na[2], x2=nb[1], y2=nb[2], stroke=LINE, stroke_width=3))
    for key, node in nodes.items():
        value, x, y = node[:3]
        out += [el('circle', cx=x, cy=y, r=22, fill=ORANGE if key in active else GREEN, stroke=INK),
                label(value, x-12, y+6)]
    return out


def heap_tree(a, active=()):
    nodes, edges = {}, []
    for i, v in enumerate(a):
        depth = int(math.log2(i+1))
        position = i-(2**depth-1)
        nodes[str(i)] = (v, 800*(position+.5)/2**depth, 40+depth*67)
        if i:
            edges.append((str((i-1)//2), str(i)))
    return tree(nodes, edges, tuple(str(i) for i in active)) + row(a, 255, '对应数组', active)


def frame(title, action, reason, scene, height=200, question=''):
    return {'title': title, 'action': action, 'reason': reason, 'question': question,
            'scene': {'width': 800, 'height': height, 'elements': scene}}


def svg_element(e):
    attrs = ' '.join(f'{k}="{html.escape(v, quote=True)}"' for k, v in e['attrs'].items())
    return f'<{e["tag"]} {attrs}>{html.escape(e.get("text", ""))}</{e["tag"]}>'


def wrap_text(text, limit=43):
    return [text[i:i+limit] for i in range(0, len(text), limit)]


def export(course, chapter, key, title, frames):
    folder = ROOT/course/'资料/超级纲要'
    pictures = folder/'图片'
    pictures.mkdir(exist_ok=True)
    paths = []
    questions={
        'ds-binary':{'比较区间中点':'这次应改lo还是hi？如果中点正好等于3，为什么还要继续？'},
        'ds-insertion':{'只执行一次右移':'数组中暂时重复的值是怎么来的？待插入值还保存在什么地方？'},
        'ds-expression':{'数字4进数栈':'读到右括号时，先弹括号还是先算加法？哪一个数应先弹出？'},
        'ds-avl':{'插入20':'20在10右侧、10在30左侧，第一旋应在谁身上做？'},
        'ds-queue':{'入队C':'要先出A，应把几个元素从入栈倒到出栈？能只倒C就返回吗？'},
        'cs-atomic-race':{'A原子写回':'B现在写回的是共享量的最新值加1，还是它早已算好的局部值？'}
    }
    for f in frames:
        f['question']=questions.get(key,{}).get(f['title'],'')
    for start in range(len(frames)):
        chunk = frames[start:start+1]
        content, cursor = [], 45
        for offset, f in enumerate(chunk, start):
            local = [label(f'{offset+1}. {f["title"]}', 20, 26, 20)]
            shift = 48
            local.append(f'<g transform="translate(0,{shift})">'+''.join(svg_element(e) for e in f['scene']['elements'])+'</g>')
            text_y = shift+f['scene']['height']+25
            for text in [f['action'], '原因：'+f['reason']]:
                for line in wrap_text(text):
                    local.append(svg_element(label(line, 20, text_y, 16)))
                    text_y += 25
            local.append(svg_element(el('line', x1=20, y1=text_y+10, x2=780, y2=text_y+10, stroke=LINE)))
            content.append(f'<g transform="translate(0,{cursor})">'+''.join(svg_element(x) if isinstance(x,dict) else x for x in local)+'</g>')
            cursor += text_y+42
        meta = ''
        if start == 0:
            data = {'version': 1, 'id': key, 'title': title, 'frames': frames}
            meta = '<metadata id="stbook-trace">'+html.escape(json.dumps(data,ensure_ascii=False,separators=(',',':')))+'</metadata>'
        name = f'演示-{key}-{start+1:02}.svg'
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 {cursor}" width="800" height="{cursor}"><title>{html.escape(title)}</title>{meta}<rect width="800" height="{cursor}" fill="#ffffff"/>'+svg_element(label(title,20,28,19))+''.join(content)+'</svg>'
        (pictures/name).write_text(svg, encoding='utf-8')
        paths.append(name)
    return {'course':course, 'chapter':chapter, 'id':key, 'title':title,
            'images':paths, 'steps':len(frames)}


def binary():
    a, lo, hi, frames = [1,3,3,7,9], 0, 5, []
    def snapshot(title, action, why, mid=None):
        scene = row(a, 65, 'a，下标在下方', () if mid is None else (mid,),colors={i:GREEN if i<lo else BLUE if i>=hi else '#f5f8f6' for i in range(len(a))})
        scene += [label(f'目标值 x=3；尚未分类的元素区间 [{lo}, {hi})',20,25),
                  label(f'lo={lo}，hi={hi}'+('' if mid is None else f'，mid={mid}，a[mid]={a[mid]}'),20,170)]
        frames.append(frame(title,action,why,scene,195))
    snapshot('先保留全部未分类元素','lo=0，hi=5。目标是第一个不小于3的元素位置。','答案边界可能在闭区间[lo,hi]内；右端5是全部元素都小于3时的返回位置。')
    while lo<hi:
        mid=(lo+hi)//2
        snapshot('比较区间中点', f'mid=⌊({lo}+{hi})/2⌋={mid}，比较{a[mid]}与3。','中点由整数除法向下取整，始终落在非空的未分类元素区间。',mid)
        if a[mid]<3:
            old=lo;lo=mid+1
            snapshot('排除中点及其左侧',f'lo从{old}改成{lo}，hi保持{hi}。','有序性保证中点及更左边都小于3，不能是第一个不小于3的位置。')
        else:
            old=hi;hi=mid
            snapshot('把中点归入已知右区',f'hi从{old}改成{hi}，lo保持{lo}。','中点满足要求，前面还可能有3；a[hi:]均不小于3，hi本身仍可作为最终答案边界。')
    snapshot('边界相遇，返回1','lo=hi=1，a[1]=3；下标0的值1小于3。','循环区间为空，左边全小于3，当前位置及其右边全不小于3。')
    return frames


def insertion():
    a, fs=[4,1,3,2], []
    fs.append(frame('尚未开始插入','只有a[0]=4构成已排序前缀。','单个元素本来就是有序的。',row(a),145))
    for i in range(1,len(a)):
        key=a[i]; j=i
        def add(title,action,reason,active=()):
            fs.append(frame(title,action,reason,row(a,55,'数组',active)+[label(f'暂存x={key}；本轮i={i}；待填位置j={j}',20,25)],145))
        add('先把待插入元素存起来',f'x=a[{i}]={key}，j={i}。','后续右移会覆盖原位置，暂存可防止丢失这个值。',(i,))
        while j>0:
            add('与左侧元素比较',f'比较a[{j-1}]={a[j-1]}是否大于x={key}。','前缀已经有序；只有较大的元素需要向右让出位置。',(j-1,))
            if a[j-1]<=key: break
            v=a[j-1];a[j]=v;j-=1
            add('只执行一次右移',f'a[{j+1}]←{v}；j变成{j}，暂存x仍是{key}。','重复值是搬移时的临时状态，待填位置由j记录，待填值仍保存在x中。',(j,j+1))
        a[j]=key
        add('填入空出的位置',f'a[{j}]←x={key}，前{i+1}项已有序。','左侧元素不大于x，右移过的元素均大于x。',(j,))
    return fs


def merge():
    a=[2,4,1,3];fs=[]
    fs.append(frame('先确定两个有序段','左段[2,4]，右段[1,3]；辅助输出初始为空。','本例只演示归并这一步；两段内部已经有序。',row(a,55,'原数组'),145))
    left,right,out=[2,4],[1,3],[];i=j=0
    while i<len(left) or j<len(right):
        l=left[i] if i<len(left) else None;r=right[j] if j<len(right) else None
        if r is None or (l is not None and l<=r):
            chosen=l;side='左';i+=1
        else:chosen=r;side='右';j+=1
        out.append(chosen)
        scene=row(left,35,'左段',() if i==len(left) else (i,))+row(right,135,'右段',() if j==len(right) else(j,))+row(out,235,'已写输出')
        fs.append(frame('取剩余部分中较小的首项',f'比较左首{l if l is not None else "已用完"}和右首{r if r is not None else "已用完"}，取{side}侧{chosen}。',f'两段各自有序，所以未用元素中的最小值必在两个首项之中；现有输出仍有序。',scene,325))
    fs.append(frame('把结果写回目标区间','a[0:4]被[1,2,3,4]替换。','输出恰好使用了左右两段的全部元素，没有遗漏或重复。',row(out),145))
    return fs


def vector():
    fs=[];old=['空','空'];new=[]
    fs.append(frame('容量2，长度0','size=0，capacity=2。','容量表示分配的格数；长度表示已经存入的元素数。',row(old,55,'旧数组'),145))
    for i,v in enumerate([10,20]):
        old[i]=v
        fs.append(frame(f'写入{v}',f'old[{i}]←{v}，size={i+1}。','尚有空位，因此不必搬动已有元素。',row(old,55,'旧数组',(i,)),145))
    new=['空']*4
    fs.append(frame('再插入30前，先分配4格','旧数组已满，另申请容量4的新数组；size仍为2。','扩容不是让旧数组凭空变长，而是取得一块新空间。',row(old,35,'旧数组')+row(new,135,'新数组'),230))
    for i in range(2):
        new[i]=old[i]
        fs.append(frame('搬移一个已有元素',f'new[{i}]←old[{i}]={old[i]}。','必须保留已有元素的先后顺序；此时两个数组暂时同时存在。',row(old,35,'旧数组',(i,))+row(new,135,'新数组',(i,)),230))
    new[2]=30
    fs.append(frame('切换存储并写入30','新数组成为有效存储，旧空间释放；new[2]←30，size=3。','有效元素是前3格，第4格只有容量，还不属于序列。',row(new,55,'有效数组',(2,)),145))
    return fs


def queue():
    ins=[];outs=[];fs=[];held=None
    def add(t,a,r):fs.append(frame(t,a,r,row(ins,35,'入栈：底→顶')+row(outs,135,'出栈：底→顶')+row([] if held is None else [held],235,'暂存/返回 x'),330))
    add('两个栈均为空','队列初始为空。','入栈接收新元素；出栈的栈顶作为队首。')
    for x in 'ABC':ins.append(x);add(f'入队{x}',f'把{x}压入入栈。','新元素在已有元素之后到达，不应抢先出队。')
    while ins:
        x=ins.pop();held=x;add(f'从入栈弹出{x}',f'暂存x={x}，尚未压入出栈。','出栈为空时才整批倒转；先后次序因此反转一次。')
        outs.append(x);held=None;add(f'把{x}压入出栈',f'出栈现在是{outs}，右端为栈顶。','要先完成整批转移，最早进入的A才能来到栈顶。')
    x=outs.pop();held=x;add('真正出队A','从出栈弹出A，返回给调用者。','A最先入队，所以应当最先离开；B成为下一队首。')
    return fs


def expression():
    nums=[];ops=['#'];fs=[];a=b=None
    def add(t,action,reason,pos):
        fs.append(frame(t,action,reason,[label('输入：3 * ( 2 + 4 ) #；当前读取 '+pos,20,25)]+row(nums,65,'数栈：底→顶')+row(ops,165,'符号栈：底→顶')+row(['未取' if v is None else v for v in [a,b]],265,'弹出后：左/右'),365))
    add('开始，先放哨兵#','数栈为空，符号栈只有#。','哨兵标记栈底，输入末尾#负责触发剩余运算。','3')
    nums.append(3);add('数字3进数栈','读取3后，转到*。','数字是运算对象，直接保留到后续运算。','*')
    ops.append('*');add('乘号进符号栈','栈顶#，压入*。','目前没有可先执行的旧运算。','(')
    ops.append('(');add('左括号进符号栈','压入(，暂时阻止括号外的*参与归约。','括号内应先计算，尚未得到右操作数的*要等待。','2')
    nums.append(2);add('数字2进数栈','读取2。','括号内第一个运算对象是2。','+')
    ops.append('+');add('加号进符号栈','读取+，栈顶(，压入+。','左括号只划分区域，不进行数值运算。','4')
    nums.append(4);add('数字4进数栈','读取4。','加法现在已有两个操作数，但仍等下一符号确定归约。',')')
    ops.pop();add('先取出待执行的加号','符号栈弹出+，数栈暂时不变。','右括号要求先完成它配对左括号里面的运算。',')')
    b=nums.pop();add('先弹出右操作数4','暂存b=4。','后进栈的是右操作数；减法和除法尤其不能交换。',')')
    a=nums.pop();add('再弹出左操作数2','暂存a=2，b=4，执行刚取出的加号。','两个操作数必须按原表达式的左右顺序组合。',')')
    nums.append(a+b);a=b=None;add('把计算结果6压回','2+4=6，右括号仍未消耗。','一个子表达式归约成一个数，供外层运算使用。',')')
    ops.pop();add('匹配括号并消耗右括号','只弹出(；不弹出数值6。','括号完成控制作用，不是算术操作符。','#')
    ops.pop();add('取出待执行的乘号','末尾#触发弹出*，数栈仍为[3,6]。','所有括号已关闭，符号栈中真实运算仍须完成。','#')
    b=nums.pop();add('弹出乘法的右操作数6','暂存b=6。','末尾#优先级低，要求执行尚未完成的乘法。','#')
    a=nums.pop();add('弹出左操作数3','暂存a=3，b=6，计算3×6。','此时括号内已经完成，乘法的两个对象都已确定。','#')
    nums.append(a*b);a=b=None;add('结果18压回数栈','数栈只剩18，符号栈只剩#。','所有真实操作符均已执行。','#')
    ops.pop();add('哨兵相遇，结束','输入#与栈底#匹配；返回18。','合法表达式结束时应恰好留下一个数，不能有多余括号或操作符。','结束')
    return fs


def avl():
    fs=[]
    states=[
        ('插入30',{'g':(30,400,40)},[],(),'根只有一个节点，左右空树高度均为−1。'),
        ('插入10',{'g':(30,400,40),'p':(10,240,125)},[('g','p')],('p',),'10小于30，成为30的左孩子。'),
        ('插入20',{'g':(30,400,40),'p':(10,240,125),'x':(20,320,210)},[('g','p'),('p','x')],('x',),'20小于30但大于10，成为10的右孩子；30左右高度差为2。'),
        ('先左旋10',{'g':(30,400,40),'x':(20,240,125),'p':(10,160,210)},[('g','x'),('x','p')],('x','p'),'20接替10原来的位置，10成为20左孩子；本例20原来的左子树为空。'),
        ('再右旋30',{'x':(20,400,40),'p':(10,240,125),'g':(30,560,125)},[('x','p'),('x','g')],('x','g'),'20升为根，30成为20右孩子；20原来的右子树为空，接到30左侧。')]
    for title,n,e,active,reason in states:
        bottom=max(node[2] for node in n.values())+55
        actions={'插入30':'根指向新节点30。','插入10':'30的左孩子指向新节点10。',
                 '插入20':'10的右孩子指向新节点20；失衡点为30。',
                 '先左旋10':'30的左孩子改成20；10的右孩子改为空；20的左孩子改成10。',
                 '再右旋30':'根改成20；30的左孩子改为空；20的右孩子改成30。'}
        fs.append(frame(title,actions[title],reason,tree(n,e,active)+[label('中序次序始终为已插入键的升序；旋转不改变键值。',20,bottom)],bottom+30))
    return fs


def heap():
    a=[4,1,3,2];fs=[]
    def add(t,action,why,active=()):fs.append(frame(t,action,why,heap_tree(a,active),340))
    add('建堆前','数组按层序对应图中的完全二叉树。','数组下标i的孩子在2i+1和2i+2，超出长度的孩子不存在。')
    for i in range(len(a)//2-1,-1,-1):
        j=i
        while 2*j+1<len(a):
            c=2*j+1
            if c+1<len(a) and a[c+1]>a[c]:c+=1
            add('选择较大的孩子',f'父下标{j}的值{a[j]}，较大孩子下标{c}的值{a[c]}。','父若需下移，就与较大孩子交换，才能保证换上来的父不小于另一孩子。',(j,c))
            if a[j]>=a[c]:add('这一子树已经满足堆序',f'{a[j]}≥{a[c]}，停止本次下滤。','两个孩子的子树此前都已成堆。',(j,c));break
            a[j],a[c]=a[c],a[j];add('交换父与孩子',f'交换下标{j}和{c}。','原父值只可能继续在它移入的子树中违背堆序。',(j,c));j=c
    maximum=a[0];last=a.pop();add('删除末尾格，暂存其值',f'最大值{maximum}已经暂存返回；另取末尾值{last}。','物理删除必须发生在末尾，才能保留完全二叉树的形状。')
    a[0]=last;add('末尾值补根',f'根暂时写为{last}。','形状正确后，再通过下滤恢复大小关系。',(0,))
    j=0
    while 2*j+1<len(a):
        c=2*j+1
        if c+1<len(a) and a[c+1]>a[c]:c+=1
        add('重新选择较大孩子',f'比较父{a[j]}与孩子{a[c]}。','仍按较大的孩子决定是否下滤。',(j,c))
        if a[j]>=a[c]:break
        a[j],a[c]=a[c],a[j];add('下滤交换',f'交换下标{j}与{c}。','交换后上层满足堆序，继续检查原父值落到的位置。',(j,c));j=c
    add('删除最大值完成',f'返回{maximum}，剩余堆为{a}。','形状与堆序都已恢复；数组整体不必从大到小排列。')
    return fs


def kmp():
    text, pattern='ABABABAC','ABABAC';pi=[0,0,1,2,3,0];i=j=0;fs=[]
    def match_scene(show_pi=False):
        out=[label(f'i={i}，j={j}，模式起点对齐文本下标 i−j={i-j}',20,25)]
        out+=row(list(text),65,'文本 T',() if i==len(text) else(i,),colors={k:GREEN for k in range(i-j,i)},cellwidth=70)
        out+=row(list(pattern),165,'模式 P',() if j==len(pattern) else(j,),colors={k:GREEN for k in range(j)},x0=140+70*(i-j),cellwidth=70)
        if show_pi:out+=row(pi,265,'前缀函数 π',cellwidth=70)
        return out
    while i<len(text):
        scene=match_scene(True)
        same=text[i]==pattern[j]
        fs.append(frame('比较两个当前字符',f'i={i}，j={j}；T[i]={text[i]}，P[j]={pattern[j]}，'+('相同。' if same else '不同。'),'绿色为已经确认匹配的前缀，橙色两格纵向对齐，正是这次比较的字符。',scene,355))
        if same:
            i+=1;j+=1
            fs.append(frame('同时向后移动',f'i←{i}，j←{j}。','刚比较的字符已匹配，匹配前缀长度增加1，模式的起始对齐位置不变。',match_scene(),255))
            if j==len(pattern):
                fs.append(frame('模式完整出现',f'起点=i−j={i}−{j}={i-j}，把2记入结果。','i已移到尾后位置8，j等于模式长度6，前面连续6个字符都已确认匹配。',row(list(text),55,'文本',(2,3,4,5,6,7)),155))
                j=pi[j-1]
                fs.append(frame('保留可重叠前缀，再检查文本是否结束','j←π[5]=0；i=8已到文本末尾，返回所有起点[2]。','完整匹配后通常保留最长真前后缀以继续找重叠；本模式该长度恰为0。',row(list(text),55,'文本',colors={k:GREEN for k in range(2,8)})+[label('结果=[2]；下一待比位置i=8；保留前缀长度j=0。',20,160)],190));break
        elif j:
            old=j;j=pi[j-1]
            fs.append(frame('只退模式位置，文本不回退',f'j←π[{old-1}]={j}；i仍为{i}；模式向右移动{old-j}格。','已匹配的ABABA有最长相同真前后缀ABA，长度3；这3个字符可以直接保留。',match_scene(),255))
        else:
            i+=1
    return fs


def dijkstra():
    edges={'S':[('A',4),('B',1)],'A':[('T',1)],'B':[('A',2),('T',5)],'T':[]}
    coords={'S':(80,100),'A':(280,40),'B':(280,180),'T':(510,100)}
    dist={'S':0,'A':math.inf,'B':math.inf,'T':math.inf};previous={v:None for v in dist};done=set();fs=[]
    def add(title,act,why,edge=None):
        scene=[]
        for u,items in edges.items():
            for v,w in items:
                x,y=coords[u];xx,yy=coords[v]
                dx,dy=xx-x,yy-y;length=math.hypot(dx,dy)
                scene += arrow(x+28*dx/length,y+28*dy/length,xx-28*dx/length,yy-28*dy/length,'#a76322' if edge==(u,v) else LINE)
                scene += [label(f'{u}→{v}: {w}',(x+xx)/2+(12 if x==xx else -15),(y+yy)/2-8,12)]
        for v,(x,y) in coords.items():
            scene += [el('circle',cx=x,cy=y,r=28,fill=GREEN if v in done else '#f5f8f6',stroke=INK),label(v,x-8,y+6)]
        scene.append(label('点   距离d   前驱',610,25,15))
        for i,v in enumerate(['S','A','B','T']):
            scene += [label(v,620,65+45*i),label('∞' if math.isinf(dist[v]) else str(dist[v]),675,65+45*i),label(previous[v] or '无',745,65+45*i)]
        scene += [label('绿色＝距离已确定；边标签明确写出方向。',20,270,15)]
        fs.append(frame(title,act,why,scene,295))
    add('初始化距离','d[S]=0，其他点为∞，确定集合为空。','∞表示目前还没有找到从S到该点的路径。')
    while len(done)<4:
        u=min((v for v in dist if v not in done),key=lambda v:dist[v]);done.add(u)
        add('取出未确定点中距离最小者',f'选{u}，d[{u}]={dist[u]}，将其标绿。','本图边权都非负，绕经尚未确定点的路径不可能把这个最小值变小。')
        for v,w in edges[u]:
            cand=dist[u]+w;old=dist[v]
            if v not in done and cand<old:
                dist[v]=cand;previous[v]=u;action=f'd[{v}]从'+('∞' if math.isinf(old) else str(old))+f'改为{dist[u]}+{w}={cand}，前驱改为{u}。'
            else:action=f'候选值{dist[u]}+{w}={cand}，不小于现值{old}，保持。'
            add('检查一条出边并松弛',action,f'尝试把当前到{u}的路径后面接上{u}→{v}；只保留更短的候选。',(u,v))
    add('全部确定','最短路径S→B→A→T长度为1+2+1=4。','每次改距离也应记录前驱；逆向读前驱才能恢复具体路径。')
    return fs


def endian():
    memory=['未写']*4;remaining=0x12345678;fs=[]
    def add(t,act,why,active=()):
        scene=row(memory,70,'低地址→高地址',active,{i:hex(0x1000+i) for i in range(4)})
        scene += [label(f'尚未取出的部分：0x{remaining:08X}',20,25),label('格子下方0、1、2、3表示相对起始地址的字节偏移。',20,185,14)]
        fs.append(frame(t,act,why,scene,210))
    add('要保存数值0x12345678','规定对象4字节，从0x1000起，采用小端。','小端规定最低权重字节先存入最低地址；没有改变数值。')
    for i in range(4):
        byte=remaining & 255
        memory[i]=f'{byte:02X}'
        add('取最低8位并写入一格',f'第{i+1}次取出0x{byte:02X}，写到地址0x{0x1000+i:X}。','一个字节8位；与0xFF按位与保留低8位，其余位变成0。',(i,))
        remaining >>= 8
        add('丢掉已经保存的低字节','无符号右移8位，让下一字节来到最低位置。','右移8位相当于整数除以256并舍去余数，已经保存的余数不再重复处理。')
    add('读回验证','从最高权重字节起拼回12、34、56、78，得到原数。','按地址看到的78、56、34、12，是存储次序；通常书写的12345678，是数值位权次序。')
    return fs


def atomic_race():
    fs=[]; shared=5;registers=['未读','未读']
    def add(t,act,why,active=()):
        fs.append(frame(t,act,why,row([shared],35,'原子共享量 x')+row(registers,145,'线程A / 线程B',active),240))
    add('初值5，两个线程各加1','每个线程的程序都是：原子load、局部加1、原子store。','每一次load/store各自不可分割，但三步合起来仍可被另一个线程插入。')
    registers[0]=shared;add('A读取共享量','A的局部副本a←x=5。','读取不会给共享量加锁；此后A只在自己的局部副本上计算。',(0,))
    registers[1]=shared;add('B也读取共享量','B的局部副本b←x=5。','A还未写回，所以B读到同一个初值。',(1,))
    registers[0]+=1;add('A局部加1','a←a+1=6，共享x仍是5。','寄存器或局部变量的改变没有自动写回共享对象。',(0,))
    registers[1]+=1;add('B局部加1','b←b+1=6，共享x仍是5。','B独立计算，尚不知道A也打算存入6。',(1,))
    shared=registers[0];add('A原子写回','x.store(a)，共享x变成6。','写回这一步不可分割，但写入的是此前算好的局部结果。',(0,))
    shared=registers[1];add('B原子写回','x.store(b)，共享x仍为6。','B用6覆盖6，没有把现有共享值再加1，所以丢失一次业务更新。',(1,))
    add('与原子fetch_add作对照','如果两线程各执行一次fetch_add(1)，最终才保证7。','本图故意使用原子变量避免C/C++数据竞争的未定义行为；普通int版本不能靠此图预测标准语义。')
    return fs


def arrow(x,y,xx,yy,color=INK):
    angle=math.atan2(yy-y,xx-x);length=10
    return [el('line',x1=x,y1=y,x2=xx,y2=yy,stroke=color,stroke_width=3)]+[
        el('line',x1=xx,y1=yy,x2=xx-length*math.cos(angle+d),y2=yy-length*math.sin(angle+d),stroke=color,stroke_width=3) for d in [-.45,.45]]


def rod():
    base=[el('line',x1=120,y1=250,x2=680,y2=250,stroke=INK,stroke_width=6),
          label('−L',100,280),label('O：x=0',365,280),label('+L',680,280),
          el('circle',cx=400,cy=90,r=5,fill=INK),label('P=(0,y)，y>0',420,85),
          el('line',x1=400,y1=90,x2=400,y2=250,stroke=LINE),label('y',410,175),
          label('均匀正电荷细棒，线密度 λ',20,45)]
    fs=[]
    def add(t,act,why,extra=()):fs.append(frame(t,act,why,base+list(extra),310))
    add('先固定几何关系','棒从−L到+L，观察点P在正上方。','L是半长；y是观察点的高度，积分时P不移动。')
    source=[el('rect',x=555,y=239,width=18,height=22,fill=ORANGE,stroke=INK),label('x处，宽dx',555,220)]
    add('切出一个正电荷小段','取x处长度dx的小段，电量dq=λdx。','线密度λ的单位是C/m，乘小段长度m后得到C。',source)
    displacement=source+arrow(564,246,405,96,'#497563')+[label('R=(-x,y)',490,150)]
    add('从源指向观察点','位移R的水平分量−x，竖直分量y；距离R=√(x²+y²)。','源在P右下方，从源走到P需要向左x，再向上y。',displacement)
    field=displacement+arrow(400,90,320,12,'#a76322')+[label('dE',290,26)]
    add('把场向量投影到竖直方向','dE大小=kλdx/R²；竖直比例=y/R，故dEy=kλy dx/R³。','单位方向向量的竖直分量是y/R；投影使分母多出一个R。',field)
    pair=[el('rect',x=226,y=239,width=18,height=22,fill=ORANGE,stroke=INK),label('−x处同样宽dx',180,220)]+arrow(400,90,480,12,'#a76322')
    add('配上镜像小段','−x与+x的电量相同、距离相同，两支场的水平分量大小相等方向相反。','每一个右半段都有左半段配对，才能对整个积分断言水平分量为0。',field+pair)
    add('相加后只剩竖直分量','一对小段贡献2dEy；只积右半棒0≤x≤L，再乘2。','两支竖直分量同向，必须相加；配对抵消的是水平分量。',source+pair[:2]+arrow(400,90,400,5,'#497563')+[label('合场朝上',420,35)])
    return fs


def main():
    cases=[('05-查找二分与位图.md','ds-binary','二分：找到第一个不小于3的位置',binary),
           ('06-排序稳定性与逆序对.md','ds-insertion','插入排序：暂存、右移、填入',insertion),
           ('06-排序稳定性与逆序对.md','ds-merge','归并：两个有序段怎样合成一段',merge),
           ('04-向量扩容与摊还分析.md','ds-vector','向量扩容：旧数组与新数组同时出现',vector),
           ('09-队列双栈与单调结构.md','ds-queue','双栈队列：整批倒转以后再出队',queue),
           ('08-栈表达式与Catalan数.md','ds-expression','3×(2+4)：两只栈怎样求值',expression),
           ('12-BST与AVL树.md','ds-avl','AVL的LR修复：两次旋转分别做什么',avl),
           ('18-优先级队列与堆.md','ds-heap','最大堆：建堆和删除最大值',heap),
           ('19-字符串KMP与匹配.md','ds-kmp','KMP：失败时保留已经匹配的字符',kmp),
           ('17-最短路与最小生成树.md','ds-dijkstra','Dijkstra：一次只检查一条出边',dijkstra)]
    reports=[export('数据结构',chapter,key,title,fn()) for chapter,key,title,fn in cases]
    reports += [export('计算机系统概论','01-位字节地址与端序.md','cs-endian','小端：一次写入一个字节',endian()),
                export('计算机系统概论','14-线程与并发.md','cs-atomic-race','两次原子读写为什么仍会丢失更新',atomic_race()),
                export('大学物理B(2)','02-库仑叠加与连续电荷.md','physics-rod','细棒电场：源、位移、投影与对称配对',rod())]
    # 纸面状态图按单状态分开，避免多栏画布把关键标签缩到约6pt。
    pictures=ROOT/'数据结构/资料/超级纲要/图片'
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    original=pictures/'ds-v3-11-huffman.svg'
    if original.exists():
        for i,(x,y) in enumerate([(0,0),(500,0),(0,290),(500,290)],1):
            svg=ET.parse(original).getroot()
            svg.set('width','500');svg.set('height','290');svg.set('viewBox',f'{x} {y} 500 290')
            ET.ElementTree(svg).write(pictures/f'ds-v3-11-huffman-step-{i}.svg',encoding='unicode')
    for name,old,new in [('ds-v3-14-interval-segment.svg','12','14'),
                         ('ds-v3-14-segment-query.svg','12','14'),
                         ('ds-v3-14-segment-update.svg','12','14'),
                         ('ds-v3-16-low.svg','13','14')]:
        path=pictures/name
        if path.exists():
            svg=ET.parse(path)
            for element in svg.getroot().iter():
                if element.tag.endswith('text') and element.get('font-size')==old:
                    element.set('font-size',new)
                if element.tag.endswith('text') and (element.text or '').startswith('绿：整段取摘要'):
                    if name=='ds-v3-14-segment-query.svg':
                        element.text='绿：本次查询直接取这一段的和；灰：与查询范围不相交'
                    elif name=='ds-v3-14-segment-update.svg':
                        element.text='橙：本次修改后需要重算的节点；其余节点保持原值'
            svg.write(path,encoding='unicode')
    out=ROOT/'outputs/three-course-books/teaching-v3'
    out.mkdir(exist_ok=True,parents=True)
    (out/'演示清单.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')
    print('已生成可复演的操作记录与纸面图。')


if __name__=='__main__':main()
