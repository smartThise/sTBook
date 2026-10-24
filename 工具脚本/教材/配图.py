#!/usr/bin/env python3
"""生成本书原创矢量示意图；需 Matplotlib，中文字体用 --font 指定。"""
from pathlib import Path
import argparse
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, fontManager
from matplotlib.patches import FancyBboxPatch
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--font',required=True);a=p.parse_args()
fontManager.addfont(a.font);name=FontProperties(fname=a.font).get_name()
plt.rcParams.update({'font.family':name,'font.size':10,'axes.unicode_minus':False,'svg.fonttype':'path','axes.spines.top':False,'axes.spines.right':False})
BLUE='#236881';RED='#c34c43';GRAY='#667781';GREEN='#2b876d'
def save(course,name,fig):
 out=ROOT/course/'资料/超级纲要/图片';out.mkdir(parents=True,exist_ok=True)
 target=out/(name+'.svg')
 fig.savefig(target,bbox_inches='tight',facecolor='white');plt.close(fig)
 target.write_text('\n'.join(line.rstrip() for line in target.read_text().splitlines())+'\n')

# 场和势不是同一个图。
x=np.linspace(0,3,600);E=np.where(x<=1,x,1/np.maximum(x,1e-12)**2);V=np.where(x<=1,(3-x*x)/2,1/np.maximum(x,1e-12))
f,ax=plt.subplots(1,2,figsize=(8,3));ax[0].plot(x,E,color=BLUE,lw=2);ax[0].set(xlabel='距离 r / R',ylabel='场强 / (kQ/R²)',title='均匀带电绝缘球：场强');ax[1].plot(x,V,color=RED,lw=2);ax[1].set(xlabel='距离 r / R',ylabel='电势 / (kQ/R)',title='同一个球：电势')
for q in ax:q.axvline(1,color=GRAY,ls=':',lw=1);q.grid(alpha=.2)
save('大学物理B(2)','本书示意-均匀球场与势',f)
u=np.linspace(-3,3,1800);envelope=np.sinc(u)**2;fringes=np.cos(3*np.pi*u)**2
f,ax=plt.subplots(1,2,figsize=(8,3));ax[0].plot(u,envelope,color=BLUE);ax[0].set(title='单缝：中央峰宽，旁峰较弱',xlabel='a sinθ / λ',ylabel='I / I(0)');ax[1].plot(u,envelope*fringes,color=GREEN);ax[1].plot(u,envelope,'--',color=RED,lw=1);ax[1].set(title='有限宽双缝：条纹乘衍射包络',xlabel='a sinθ / λ',ylabel='归一化强度')
for q in ax:q.grid(alpha=.2);q.set_ylim(-.03,1.08)
save('大学物理B(2)','本书示意-衍射与干涉包络',f)
x=np.linspace(0,1,700);f,ax=plt.subplots(1,2,figsize=(8,3))
for n,col in [(1,BLUE),(2,RED),(3,GREEN)]:ax[0].plot(x,np.sqrt(2)*np.sin(n*np.pi*x),label=f'n = {n}',color=col);ax[1].plot(x,2*np.sin(n*np.pi*x)**2,label=f'n = {n}',color=col)
ax[0].set(title='无限阱波函数（L归一为1）',xlabel='x / L',ylabel='ψ × √L');ax[1].set(title='概率密度不是波函数本身',xlabel='x / L',ylabel='|ψ|² × L')
for q in ax:q.legend(fontsize=8);q.grid(alpha=.2)
save('大学物理B(2)','本书示意-势阱波函数与密度',f)

n=np.arange(2,41);f,ax=plt.subplots(figsize=(7,3.6))
for y,label,col in [(n,'n',BLUE),(n*np.log2(n),'n log₂n',GREEN),(n*n,'n²',RED),(2.0**n,'2ⁿ',GRAY)]:ax.semilogy(n,y,label=label,color=col)
ax.set(xlabel='输入规模 n',ylabel='操作量（对数纵轴）',title='增长快慢：纵轴每大格都是乘一个倍数');ax.legend();ax.grid(alpha=.2);save('数据结构','本书示意-复杂度增长',f)
X='ABCBDAB';Y='BDCABA';d=np.zeros((len(X)+1,len(Y)+1),dtype=int)
for i,c in enumerate(X,1):
 for j,e in enumerate(Y,1):d[i,j]=d[i-1,j-1]+1 if c==e else max(d[i-1,j],d[i,j-1])
f,ax=plt.subplots(figsize=(5.5,4.7));ax.imshow(d,cmap='Blues',vmin=0,vmax=5);ax.set_xticks(range(len(Y)+1),['空']+list(Y));ax.set_yticks(range(len(X)+1),['空']+list(X))
for i in range(d.shape[0]):
 for j in range(d.shape[1]):ax.text(j,i,str(d[i,j]),ha='center',va='center',color='white' if d[i,j]>=3 else '#18394c')
ax.set(title='LCS前缀表：右下角是4',xlabel='Y 的前缀',ylabel='X 的前缀');save('数据结构','本书示意-LCS逐格表',f)

# 用三个数把LR两次旋转画出来。
f,ax=plt.subplots(figsize=(8,3.1));ax.set_xlim(0,12);ax.set_ylim(0,4);ax.axis('off')
def tree(nodes,edges,title,center):
 for a,b in edges:ax.plot([nodes[a][0],nodes[b][0]],[nodes[a][1],nodes[b][1]],color=GRAY,zorder=1)
 for key,(xx,yy) in nodes.items():ax.scatter([xx],[yy],s=650,color=BLUE,zorder=2);ax.text(xx,yy,str(key),color='white',ha='center',va='center',zorder=3)
 ax.text(center,3.6,title,ha='center',fontsize=11)
tree({30:(1.8,2.7),10:(.8,1.7),20:(1.5,.7)},[(30,10),(10,20)],'插入后：LR失衡',1.5)
tree({30:(5.5,2.7),20:(4.5,1.7),10:(3.8,.7)},[(30,20),(20,10)],'先左旋10',5)
tree({20:(9.8,2.7),10:(8.8,1.4),30:(10.8,1.4)},[(20,10),(20,30)],'再右旋30',9.8)
for x0,x1 in [(2.5,3.3),(6.3,8)]:ax.annotate('',xy=(x1,2),xytext=(x0,2),arrowprops={'arrowstyle':'->','color':RED,'lw':2})
save('数据结构','本书示意-AVL双旋',f)

f,ax=plt.subplots(figsize=(8,2.7));ax.set_xlim(0,10);ax.set_ylim(0,3);ax.axis('off')
for j,(name,x,y,col) in enumerate([('虚拟地址',.1,1.3,BLUE),('页号 → 页框号',3.6,2.05,GREEN),('页内偏移不变',3.6,.55,GRAY),('物理地址',7.2,1.3,BLUE)]):
 ax.add_patch(FancyBboxPatch((x,y),2.5,.55,boxstyle='round,pad=.08',edgecolor=col,facecolor='#f0f6f8'));ax.text(x+1.25,y+.275,name,ha='center',va='center',fontsize=10)
for a,b in [((2.6,1.6),(3.5,2.25)),((2.6,1.6),(3.5,.8)),((6.2,2.25),(7.1,1.6)),((6.2,.8),(7.1,1.6))]:ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','color':GRAY})
ax.text(5,2.9,'4 KiB页：0x12345 → VPN 0x12 + 偏移0x345',ha='center');ax.text(5,.02,'若页框号为0x9a，最终物理地址为0x9a345',ha='center');save('计算机系统概论','本书示意-地址翻译',f)
f,ax=plt.subplots(figsize=(8,2.8));ax.set_xlim(0,16);ax.set_ylim(-.7,2);ax.axis('off')
for yy,start,step,label,col in [(1.2,0,1,'较小数量级：格点密',BLUE),(.1,0,2,'较大数量级：间隔翻倍',RED)]:
 xs=np.arange(start,16,step);ax.plot([0,15.5],[yy,yy],color=GRAY,lw=1);ax.scatter(xs,np.full_like(xs,yy,dtype=float),color=col,s=30);ax.text(0,yy+.3,label,color=col)
ax.text(0,-.6,'示意相邻可表示数的间隔；真实浮点间隔取决于指数，非均匀分布。');save('计算机系统概论','本书示意-浮点格点',f)
print('8幅原创SVG已生成；字体已转轮廓，离线阅读不依赖该中文字体。')
