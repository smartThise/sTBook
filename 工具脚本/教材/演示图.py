#!/usr/bin/env python3
"""演示图生成器：为教材逐步演示生成统一的SVG序列与trace。

用法：python3 演示图.py [demo_id ...]（无参数生成全部）
输出：数据结构/资料/超级纲要/图片/演示-<id>-NN.svg；首个SVG内嵌 notes-demos.js 的trace JSON。
"""
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path("/Volumes/PortableSSD/Documents/mynotebook")
IMG = ROOT / "数据结构" / "资料" / "超级纲要" / "图片"

# ---------- 视觉体系 ----------
INK = "#22313a"
SUB = "#5c6f68"
FAINT = "#93a39b"
LINE = "#d5dfda"
BG = "#ffffff"
CELL = "#f5f8f6"
CELL_STROKE = "#d9e2dd"
HOT = "#ffe9c4"
HOT_STROKE = "#e0a243"
WRITE = "#d9eaf9"
WRITE_STROKE = "#6d9dd6"
DONE = "#d9f0e2"
DONE_STROKE = "#6cb98d"
BAD = "#fbe4e4"
BAD_STROKE = "#d89393"
PALE = "#eef3f0"
CJK = "PingFang SC, Noto Sans CJK SC, sans-serif"
MONO = "Menlo, Consolas, monospace"

COLOR_RE = re.compile(r"^#[0-9a-f]{3,8}$|^none$|^white$|^black$", re.I)
FONT_RE = re.compile(r"^[a-zA-Z0-9 ,'-]+$")


class Scene:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.el = []

    def _ok(self, k, v):
        if k in ("fill", "stroke"):
            return bool(COLOR_RE.match(v))
        if k == "font-family":
            return bool(FONT_RE.match(v))
        if k == "text-anchor":
            return v in ("start", "middle", "end")
        try:
            return abs(float(v)) <= 10000
        except (TypeError, ValueError):
            return False

    def add(self, tag, text="", **attrs):
        assert tag in ("rect", "circle", "line", "text"), tag
        clean = {}
        for k, v in attrs.items():
            k = k.replace("_", "-")
            assert self._ok(k, str(v)), (k, v)
            clean[k] = str(v)
        self.el.append({"tag": tag, "attrs": clean, "text": str(text)})

    def label(self, x, y, t, size=16, fill=INK, mono=False, anchor="start"):
        self.add("text", x=x, y=y, font_size=size, fill=fill,
                 font_family=(MONO if mono else CJK), text_anchor=anchor, text=t)

    def array(self, x, y, values, states=None, cw=58, ch=42, idx0=0, gap=2, show_idx=True):
        states = states or {}
        for i, v in enumerate(values):
            f, st = states.get(i, (CELL, CELL_STROKE))
            cx = x + i * (cw + gap)
            self.add("rect", x=cx, y=y, width=cw, height=ch, rx=8, fill=f, stroke=st, stroke_width=1.5)
            self.label(cx + cw / 2, y + ch / 2 + 6, str(v), size=17, mono=True, anchor="middle")
            if show_idx:
                self.label(cx + cw / 2, y + ch + 16, str(idx0 + i), size=12, fill=FAINT, mono=True, anchor="middle")

    def pointer(self, cx, y, tag, color=WRITE_STROKE):
        self.add("line", x1=cx, y1=y, x2=cx, y2=y + 14, stroke=color, stroke_width=2)
        self.add("circle", cx=cx, cy=y + 18, r=3.5, fill=color)
        w = max(20, 12 + 8 * len(tag))
        self.add("rect", x=cx - w / 2, y=y + 24, width=w, height=20, rx=6, fill=BG, stroke=color, stroke_width=1.2)
        self.label(cx, y + 39, tag, size=13, fill=color, mono=True, anchor="middle")

    def chip(self, x, y, w, h, t, fill, stroke, size=15, mono=True, tcolor=INK):
        self.add("rect", x=x, y=y, width=w, height=h, rx=8, fill=fill, stroke=stroke, stroke_width=1.5)
        self.label(x + w / 2, y + h / 2 + size * 0.36, t, size=size, mono=mono, anchor="middle", fill=tcolor)

    def bracket(self, x1, x2, y, tag, color=WRITE_STROKE):
        self.add("line", x1=x1, y1=y, x2=x2, y2=y, stroke=color, stroke_width=1.6)
        self.add("line", x1=x1, y1=y - 5, x2=x1, y2=y + 5, stroke=color, stroke_width=1.6)
        self.add("line", x1=x2, y1=y - 5, x2=x2, y2=y + 5, stroke=color, stroke_width=1.6)
        if tag:
            self.label((x1 + x2) / 2, y - 7, tag, size=13, fill=color, mono=True, anchor="middle")


def frame(title, action, reason, question=None, scene=None):
    return {"title": title, "action": action, "reason": reason,
            "question": question or "", "scene": scene}


def validate(frames):
    assert 1 <= len(frames) <= 400
    for f in frames:
        for k in ("title", "action", "reason"):
            assert isinstance(f[k], str) and len(f[k]) <= 3000
        s = f["scene"]
        assert 100 <= s.w <= 2000 and 50 <= s.h <= 2000
        assert len(s.el) <= 1000
        for e in s.el:
            assert e["tag"] in ("rect", "circle", "line", "text")
            for a, v in e["attrs"].items():
                assert len(str(v)) <= 150 and not re.search(r"url\s*\(|[<>]", str(v), re.I), (a, v)
                if a in ("fill", "stroke"):
                    assert COLOR_RE.match(v), (a, v)
                elif a == "font-family":
                    assert FONT_RE.match(v), (a, v)
                elif a == "text-anchor":
                    assert v in ("start", "middle", "end")
                else:
                    assert abs(float(v)) <= 10000, (a, v)
            assert len(e["text"]) <= 1000


def svg_for_frame(demo_title, idx, total, f):
    W = f["scene"].w
    top = 46
    H = top + f["scene"].h + 96
    esc = lambda t: str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
        f'<title>{esc(demo_title)}</title>',
        f'<rect width="{W}" height="{H}" fill="{BG}"/>',
        f'<text x="24" y="30" font-size="18" font-weight="bold" fill="{INK}" font-family="{CJK}">{esc(demo_title)}</text>',
        f'<text x="{W - 24}" y="30" font-size="13" fill="{FAINT}" font-family="{CJK}" text-anchor="end">第 {idx} / {total} 步</text>',
        f'<g transform="translate(0,{top})">',
        f'<text x="24" y="24" font-size="17" font-weight="bold" fill="{INK}" font-family="{CJK}">{idx}. {esc(f["title"])}</text>',
        '<g transform="translate(0,36)">',
    ]
    for e in f["scene"].el:
        a = e["attrs"]
        if e["tag"] == "text":
            parts.append(f'<text x="{a.get("x",0)}" y="{a.get("y",0)}" font-size="{a.get("font-size",16)}"'
                         f' fill="{a.get("fill",INK)}" font-family="{a.get("font-family",CJK)}"'
                         + (f' text-anchor="{a["text-anchor"]}"' if "text-anchor" in a else '')
                         + f'>{esc(e["text"])}</text>')
        elif e["tag"] == "rect":
            parts.append(f'<rect x="{a.get("x",0)}" y="{a.get("y",0)}" width="{a.get("width",0)}" height="{a.get("height",0)}"'
                         f' rx="{a.get("rx",0)}" fill="{a.get("fill","none")}" stroke="{a.get("stroke","none")}"'
                         f' stroke-width="{a.get("stroke-width",1)}"/>')
        elif e["tag"] == "line":
            parts.append(f'<line x1="{a.get("x1",0)}" y1="{a.get("y1",0)}" x2="{a.get("x2",0)}" y2="{a.get("y2",0)}"'
                         f' stroke="{a.get("stroke",INK)}" stroke-width="{a.get("stroke-width",1)}"/>')
        elif e["tag"] == "circle":
            parts.append(f'<circle cx="{a.get("cx",0)}" cy="{a.get("cy",0)}" r="{a.get("r",3)}"'
                         f' fill="{a.get("fill","none")}" stroke="{a.get("stroke","none")}" stroke-width="{a.get("stroke-width",1)}"/>')
    parts.append('</g>')
    parts.append(f'<text x="24" y="{f["scene"].h + 52}" font-size="15" fill="{INK}" font-family="{CJK}">{f["action"]}</text>')
    parts.append(f'<text x="24" y="{f["scene"].h + 76}" font-size="15" fill="{SUB}" font-family="{CJK}">为什么：{f["reason"]}</text>')
    parts.append(f'<line x1="24" y1="{f["scene"].h + 88}" x2="{W - 24}" y2="{f["scene"].h + 88}" stroke="{LINE}"/>')
    parts.append('</g></svg>')
    return "".join(parts)


def write_demo(demo_id, title, frames, outdir=None):
    validate(frames)
    for f in frames:
        sc = f["scene"]
        f["scene"] = {"width": sc.w, "height": sc.h, "elements": sc.el}
    trace = {"version": 1, "id": demo_id, "title": title, "frames": frames}
    meta = json.dumps(trace, ensure_ascii=False, separators=(",", ":"))
    meta = meta.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    total = len(frames)
    for i, f in enumerate(frames, 1):
        sc = f["scene"]
        static_frame = {"title": f["title"], "action": f["action"], "reason": f["reason"],
                        "scene": Scene(sc["width"], sc["height"])}
        static_frame["scene"].el = sc["elements"]
        svg = svg_for_frame(title, i, total, static_frame)
        if i == 1:
            svg = svg.replace("</title>", f'</title><metadata id="stbook-trace">{meta}</metadata>', 1)
        ( (outdir or IMG) / f"演示-{demo_id}-{i:02d}.svg" ).write_text(svg, encoding="utf-8")
    return total


# ---------- 演示：ch01 起泡一趟 ----------

def demo_bubble_pass():
    a = [5, 2, 7, 4, 6, 3, 1]
    frames = []
    W, H = 780, 196
    X, Y, CW = 50, 86, 58

    def scene(values, hot=None, done_upto=None, active=None, note=None):
        sc = Scene(W, H)
        sc.label(X, 30, "第1趟：自左向右逐对检视，逆序即交换", size=15, fill=SUB)
        st = {}
        if done_upto:
            for k in range(done_upto):
                st[k] = (DONE, DONE_STROKE)
        if hot:
            for k in hot:
                st[k] = (HOT, HOT_STROKE)
        if active is not None:
            st[active] = (WRITE, WRITE_STROKE)
        sc.array(X, Y, values, st, cw=CW, ch=44)
        if hot:
            i = hot[0]
            sc.bracket(X + i * (CW + 2), X + (i + 1) * (CW + 2) - 2, Y - 12, f"a[{i}] ? a[{i+1}]", HOT_STROKE)
        if note:
            sc.label(X, 176, note, size=15)
        return sc

    frames.append(frame("扫描开始", "从第0对开始。目标：把本趟最大值推到末尾。",
                        "每完成一对比较，较大者都留在靠右的位置。",
                        "若这对是逆序，会发生什么？", scene(a)))
    for i in range(6):
        hit = a[i] > a[i + 1]
        if hit:
            frames.append(frame(f"比较a[{i}]与a[{i+1}]：{a[i]} > {a[i+1]}",
                                f"逆序，交换两格。", "左项更大，违反非降序；交换后较大者右移一格。",
                                "交换后，较大者下一轮与谁比较？",
                                scene(a, hot=[i, i + 1])))
            a[i], a[i + 1] = a[i + 1], a[i]
            frames.append(frame(f"交换完成：{a[i+1]}占住a[{i+1}]",
                                "较大者继续留在扫描前沿。", "较大者始终骑在扫描线上，一路向右。",
                                "", scene(a, active=i + 1)))
        else:
            frames.append(frame(f"比较a[{i}]与a[{i+1}]：{a[i]} ≤ {a[i+1]}",
                                "本对有序，不交换，扫描线右移。", "非降序的相邻对无需处理。",
                                "", scene(a, hot=[i, i + 1])))
    st = {k: (DONE, DONE_STROKE) for k in range(6)}
    st[6] = (WRITE, WRITE_STROKE)
    frames.append(frame("第1趟结束：7就位", "最大值7推到末尾：比较6次、交换5次。",
                        "扫描中当前最大者始终在扫描前沿，扫完必然落在末尾。",
                        "", scene(a, done_upto=6, active=6)))
    return write_demo("ds01-bubble", "起泡排序：一趟扫描怎样把7推到末尾", frames)


# ---------- 演示：ch01 图灵机加一 ----------

def demo_tm_increase():
    cells = ["#"] * 2 + list("10101111") + ["#"] * 2
    n = len(cells)
    W, H = 780, 278
    X, Y, CW = 24, 118, 61
    frames = []

    def scene(state, head, written, read, note):
        sc = Scene(W, H)
        sc.label(X, 30, "规则：(<,1;0,L,<) (<,0;1,R,>) (<,#;1,R,>) (>,0;0,R,>) (>,#;#,L,h)", size=13, fill=SUB, mono=True)
        for i, c in enumerate(cells):
            cx = X + i * CW
            hot = (i == head)
            tinted = i in written
            sc.add("rect", x=cx, y=Y + 16, width=CW - 6, height=48, rx=8,
                   fill=(HOT if hot else (WRITE if tinted else CELL)),
                   stroke=(HOT_STROKE if hot else (WRITE_STROKE if tinted else CELL_STROKE)), stroke_width=1.5)
            sc.label(cx + (CW - 6) / 2, Y + 46, c, size=18, mono=True, anchor="middle",
                     fill=(INK if c != "#" else FAINT))
            sc.label(cx + (CW - 6) / 2, Y + 80, str(i), size=11, fill=FAINT, mono=True, anchor="middle")
        sc.chip(X + head * CW + (CW - 6) / 2 - 30, Y - 22, 60, 28, state, WRITE, WRITE_STROKE, size=17)
        sc.label(X + head * CW + (CW - 6) / 2, Y + 12, "读写头", size=11, fill=SUB, anchor="middle")
        sc.chip(X, Y + 104, 96, 24, "已改写", WRITE, WRITE_STROKE, size=13, mono=False)
        sc.chip(X + 106, Y + 104, 150, 24, "读写头当前格", HOT, HOT_STROKE, size=13, mono=False)
        sc.label(X, 262, note, size=15)
        return sc

    head = 9
    state = "<"
    written = set()
    step = 0
    while state != "h":
        step += 1
        read = cells[head]
        if state == "<" and read == "1":
            cells[head] = "0"; written.add(head)
            act, why = "读'1'：改写为'0'，左移一格。", "末尾连续的'1'要逐位翻成'0'。"
            head -= 1
        elif state == "<" and read == "0":
            cells[head] = "1"; written.add(head)
            act, why = "读'0'：改写为'1'，右移一格，转入状态>。", "原有的最低位'0'翻成'1'，进位到此为止。"
            head += 1; state = ">"
        elif state == "<" and read == "#":
            cells[head] = "1"; written.add(head)
            act, why = "读'#'：改写为'1'，右移转入状态>。", "全'1'输入靠这条规则补最高位，本例未触发。"
            head += 1; state = ">"
        elif state == ">" and read == "0":
            act, why = "状态>读'0'：不改写，右移一格。", "右行越过刚翻出的'0'，去寻找右边界'#'。"
            head += 1
        elif state == ">" and read == "#":
            act, why = "状态>读'#'：不改写，左移一格，停机。", "右边界说明扫描完成；纸带即输出10110000（175+1）。"
            head -= 1; state = "h"
        else:
            act, why = "状态>读'0'：不改写，右移一格。", "右行越过刚翻出的'0'。"
            head += 1
        note = f"第{step}拍：状态{state if state != 'h' else '>'}读到'{read}'，本拍结束时读写头停在格子{head}。"
        frames.append(frame(f"第{step}拍（状态{state}，读'{read}'）", act, why, "",
                            scene("h" if state == "h" else (">" if state == ">" and read == "#" else state), head, set(written), read, note)))
    return write_demo("ds01-tm", "图灵机加一：10101111如何变成10110000", frames)


# ---------- 演示：ch01 RAM上整除 ----------

def demo_ram_divide():
    steps = [
        (0, 3, 1, "R[3] ← 1：置常数增量。", "循环每轮加的是同一个1。"),
        (1, None, None, "GOTO 4：无条件跳过循环头。", "R[0]=25不为0，直接进入判断。"),
        (4, None, None, "IF R[0] > 0：25 > 0 成立，转[2]。", "c仍为正，还需要减。"),
        (2, 2, 1, "R[2] ← R[2]+R[3]：x=1。", "第一次减法前先计数。"),
        (3, 0, 13, "R[0] ← R[0]−R[1]：25−12=13。", "c减去一个d。"),
        (4, None, None, "13 > 0 成立，转[2]。", "还不够，继续。"),
        (2, 2, 2, "x=2。", "第二次计数。"),
        (3, 0, 1, "13−12=1。", "再减一个d。"),
        (4, None, None, "1 > 0 成立，转[2]。", "1仍是正数，还能再减一次。"),
        (2, 2, 3, "x=3。", "第三次计数。"),
        (3, 0, -11, "1−12=−11。", "下溢：再减就变负。"),
        (4, None, None, "−11 > 0 不成立，顺序执行[5]。", "循环恰好执行了3轮。"),
        (5, 0, 3, "R[0] ← R[2]：结果3复制回R[0]。", "按约定结果存于R[0]。"),
        (6, None, None, "STOP：输出⌈25/12⌉=3。", "快照表高度14，即T(25,12)=14。"),
    ]
    frames = []
    W, H = 720, 212
    X, Y = 40, 92
    cur = [25, 12, 0, 0]

    def scene(r, wr, note, ir, tail):
        sc = Scene(W, H)
        sc.label(X, 30, "[0]R3←1  [1]GOTO4  [2]x++  [3]c-=d  [4]IF R0>0 GOTO2  [5]R0←x  [6]STOP", size=13, fill=SUB, mono=True)
        for i in range(4):
            f, st = (WRITE, WRITE_STROKE) if i == wr else (CELL, CELL_STROKE)
            sc.add("rect", x=X + i * 160, y=Y, width=150, height=54, rx=8, fill=f, stroke=st, stroke_width=1.5)
            sc.label(X + i * 160 + 75, Y + 22, f"R[{i}]", size=12, fill=FAINT, mono=True, anchor="middle")
            sc.label(X + i * 160 + 75, Y + 45, str(r[i]), size=19, mono=True, anchor="middle")
        sc.label(X, 192, note, size=15)
        sc.label(W - X, 192, f"IR=[{ir}]" + (f"  {tail}" if tail else ""), size=15, fill=SUB, mono=True, anchor="end")
        return sc

    frames.append(frame("初值", "R[0]=25、R[1]=12、R[2]=R[3]=0，IR指向[0]。",
                        "任务：教一台只会加减与跳转的机器做上整除⌈25/12⌉。",
                        "循环会执行几轮？", scene(cur, None, "等待执行。", 0, "")))
    for ir, wr, val, act, why in steps:
        if wr is not None:
            cur[wr] = val
        note = f"写入后 R[{wr}] = {val}。" if wr is not None else "本步不写入任何寄存器。"
        frames.append(frame(f"执行[{ir}]", act, why, "", scene(cur, wr, note, ir, "")))
    return write_demo("ds01-ram", "RAM上整除：25÷12的14步快照", frames)




# ---------- 演示：ch02 迭代空间（正方形→三角形→倍增） ----------

def demo_iter_space():
    frames = []
    W, H = 640, 300

    def grid_scene(x, y, cells, cw=22, chh=22, n=8, title=""):
        sc = Scene(W, H)
        sc.label(x, 30, title, size=15, fill=SUB)
        for (i, j, st) in cells:
            f, stc = st
            sc.add("rect", x=x + j * cw, y=y + i * chh, width=cw - 2, height=chh - 2, rx=4,
                   fill=f, stroke=stc, stroke_width=1)
        for k in range(n):
            sc.label(x + k * cw + cw / 2 - 1, y + n * chh + 16, str(k), size=11, fill=FAINT, mono=True, anchor="middle")
        return sc

    DOT = (WRITE, WRITE_STROKE)
    EMPTY = (CELL, CELL_STROKE)
    # 正方形：逐行填充
    for r in range(1, 9):
        cells = [(i, j, DOT if i < r else EMPTY) for i in range(8) for j in range(8)]
        total = sum(8 for _ in range(r))
        frames.append(frame(f"实例A：正方形填到第{r}行", f"外层i={r-1}这一行，内层j跑满8格，新增8个点。",
                            "两层独立，每行都是8点：面积=n²。", "", grid_scene(70, 60, cells, title=f"for i in 0..n-1: for j in 0..n-1    已执行{total}次")))
    # 三角形：逐行填充
    for r in range(1, 9):
        cells = [(i, j, DOT if j < i else EMPTY) for i in range(8) for j in range(8)]
        total = r * (r - 1) // 2 + r - 1
        frames.append(frame(f"实例B：三角形填到第{r}行", f"第{r-1}行只有{i if False else r-1}个点（j<i），新增{r-1}个点。",
                            "行宽逐行加1：点阵是三角形，面积约为正方形的一半，阶不变O(n²)。",
                            "", grid_scene(70, 60, cells, title=f"for i in 0..n-1: for j in 0..i-1    已执行{(r-1)*r//2}次")))
    frames[-1] = frame("实例B完成：三角形", "8行共填0+1+…+7=28个点。",
                       "n=28时28点=8×7/2；一般n行总面积n(n−1)/2，O(n²)。",
                       "", grid_scene(70, 60, [(i, j, DOT if j < i else EMPTY) for i in range(8) for j in range(8)],
                                      title="for i in 0..n-1: for j in 0..i-1    已执行28次"))
    # 倍增行宽
    rows = [1, 2, 4]
    for k, wdt in enumerate(rows, 1):
        cells = []
        for i in range(6):
            w = wdt if i == k - 1 else (rows[min(i, len(rows) - 1)] if i < k else 0)
            for j in range(w):
                cells.append((i, j, DOT))
        cells += [(i, j, EMPTY) for i in range(6) for j in range(8) if all(not (ii == i and jj == j) for ii, jj, _ in cells)]
        frames.append(frame(f"实例D：倍增行宽第{k}行", f"外层i翻倍：第{k}行宽度{i if False else 2**(k-1)}，新增{2**(k-1)}个点。",
                            "行宽1,2,4,8…构成几何级数，总点数由末行支配，O(n)。",
                            "", grid_scene(70, 60, cells, title="for i=1; i<n; i<<=1: for j in 0..i-1")))
    return write_demo("ds02-iter", "循环的点阵：正方形、三角形与倍增", frames)


# ---------- 演示：ch03 最大区间右扫（19元素） ----------

def demo_gs_ls():
    A = [1, -2, 7, 2, 6, -9, 5, 6, -12, -8, 13, 0, -3, 1, -2, 8, 0, -5, 3]
    n = len(A)
    frames = []
    W, H = 1080, 260
    X, Y, CW = 20, 96, 54

    def scene(a, k, s, gs, reset, note, upd=False):
        sc = Scene(W, H)
        st = {}
        for i in range(n):
            if i == k:
                st[i] = (HOT, HOT_STROKE)
            elif i > k:
                st[i] = (PALE, CELL_STROKE)
        if upd:
            st[k] = (WRITE, WRITE_STROKE)
        sc.array(X, Y, a, st, cw=CW, ch=44)
        sc.pointer(X + k * (CW + 2) + CW / 2 - 1, Y - 42, "k", HOT_STROKE)
        sc.label(X, 40, f"已扫区间[{k+1},19)；当前sum={'0' if reset else s}；gs={gs}", size=16, mono=True)
        sc.chip(X, 178, 130, 24, "sum≤0，剪为0", BAD, BAD_STROKE, size=12, mono=False) if reset else None
        sc.label(X, 226, note, size=15)
        return sc

    frames.append(frame("准备", "自右向左扫描；sum=0（以当前下标为起点的最大和），gs=0（接口Ⅰ，允许空区间）。",
                        "sum剪除非正前缀：负的起点对更左的位置毫无帮助。",
                        "读入A[18]=3后，sum与gs各是多少？",
                        scene(A, 18, 0, 0, False, "尚未扫描。")))
    gs = 0
    s_acc = 0
    for i in range(n - 1, -1, -1):
        s_acc += A[i]
        upd = gs < s_acc
        if upd:
            gs = s_acc
        reset = s_acc <= 0
        act = f"sum += A[{i}]={A[i]} → sum={s_acc}" + ("；sum≤0，剪为0" if reset else "")
        if upd:
            act += f"；gs更新为{gs}"
        why = "sum保存以k为起点的最大区间和；gs记录全程最大。" + ("负的sum只会拖累更左的起点，剪除。" if reset else "")
        frames.append(frame(f"k={i}：读入{A[i]}", act, why,
                            f"下一个k={i-1}时，sum会加上哪个数？" if i > 0 else None,
                            scene(A, i, s_acc, gs, reset, act, upd=upd)))
        if reset:
            s_acc = 0
    frames.append(frame("扫描结束", "gs=17，对应区间[10,16)：13,0,−3,1,−2,8。",
                        "三个并列17的区间中，[10,17)长7落选，等长取靠后者。",
                        "", scene(A, -1, 0, 17, False, "最终答案gs=17。")))
    return write_demo("ds03-gs-ls", "最大区间：从右向左一次扫描（19元素实例）", frames)


# ---------- 演示：ch04 向量插入搬移 ----------

def demo_vec_insert():
    v = ["D", "A", "T", "A"]
    frames = []
    W, H = 640, 240
    X, Y, CW = 60, 96, 64

    def scene(vals, hi_from, states, note, extra=None):
        sc = Scene(W, H)
        sc.label(X, 30, "insert(2, 'I')：把后缀[2,4)整体后移一位，再写入I", size=15, fill=SUB)
        for i, val in enumerate(vals):
            if val is None:
                sc.add("rect", x=X + i * (CW + 2), y=Y, width=CW, height=46, rx=8, fill="#fbfdff", stroke=CELL_STROKE, stroke_width=1.2)
                sc.label(X + i * (CW + 2) + CW / 2, Y + 29, "·", size=17, fill=FAINT, anchor="middle")
            else:
                f, st = states.get(i, (CELL, CELL_STROKE))
                sc.add("rect", x=X + i * (CW + 2), y=Y, width=CW, height=46, rx=8, fill=f, stroke=st, stroke_width=1.5)
                sc.label(X + i * (CW + 2) + CW / 2, Y + 29, val, size=18, mono=True, anchor="middle")
            sc.label(X + i * (CW + 2) + CW / 2, Y + 62, str(i), size=12, fill=FAINT, mono=True, anchor="middle")
        if extra:
            extra(sc)
        sc.label(X, 176, note, size=15)
        sc.label(X, 204, "_size = 4 → 5；容量足够，无需扩容", size=14, fill=SUB, mono=True)
        return sc

    def arrow_move(sc, i, color=HOT_STROKE):
        x1 = X + i * (CW + 2) + CW / 2
        sc.add("line", x1=x1, y1=Y - 10, x2=x1 + (CW + 2), y2=Y - 10, stroke=color, stroke_width=1.6)
        sc.add("circle", cx=x1 + (CW + 2), cy=Y - 10, r=3, fill=color)

    frames.append(frame("初态", "向量D A T A，在秩2插入字符I。", "后缀[2,4)（T、A）必须整体右移腾位。",
                        "哪一个元素先搬？", scene(v, 2, {}, "搬移方向：自后向前。")))
    frames.append(frame("搬A（秩3→4）", "先把末尾的A搬到新末位。", "自后向前才不会覆盖尚未搬动的元素。",
                        "", scene(["D", "A", "T", "A", None][:4] + ["A"], 2, {4: (WRITE, WRITE_STROKE)}, "A就位。")))
    v2 = ["D", "A", "T", "A", "A"]
    frames.append(frame("搬T（秩2→3）", "把T搬到秩3。", "继续自后向前。", "",
                        scene(["D", "A", "T", "T", "A"], 2, {3: (WRITE, WRITE_STROKE)}, "T就位，秩2空出。")))
    frames.append(frame("写入I", "把I写入秩2。", "空位已腾出，直接写入。", "",
                        scene(["D", "A", "I", "T", "A"], 2, {2: (WRITE, WRITE_STROKE)}, "I就位。")))
    frames.append(frame("完成", "向量变为D A I T A，规模加一。", "与教材表2.2第15行一致。",
                        "", scene(["D", "A", "I", "T", "A"], 2, {2: (WRITE, WRITE_STROKE)}, "insert(2,'I')完成。")))
    return write_demo("ds04-insert", "向量插入：后缀怎样整体后移", frames)


# ---------- 演示：ch05 二分查找版本C ----------

def demo_binsearch_c():
    K = list("ABCDEFGHIJK")   # n=11
    e = "D"
    frames = []
    W, H = 760, 250
    X, Y, CW = 36, 108, 62

    def scene(lo, hi, mi, act_note, exited=False):
        sc = Scene(W, H)
        sc.label(X, 30, f"binSearch版本C：在有序向量中查'{e}'；不变性：[0,lo)≤e＜[hi,11)", size=15, fill=SUB)
        st = {}
        for i in range(11):
            if i < lo:
                st[i] = (PALE, CELL_STROKE)
            elif i >= hi:
                st[i] = (PALE, CELL_STROKE)
            elif mi is not None and i == mi:
                st[i] = (HOT, HOT_STROKE)
        sc.array(X, Y, K, st, cw=CW, ch=46)
        sc.pointer(X + lo * (CW + 2) + CW / 2 - 1, Y - 40, "lo", WRITE_STROKE) if lo < 11 else None
        sc.pointer(X + (hi - 1) * (CW + 2) + CW / 2 - 1, Y - 40, "hi-1", BAD_STROKE) if hi > 0 else None
        if mi is not None:
            sc.pointer(X + mi * (CW + 2) + CW / 2 - 1, Y + 72, "mi", HOT_STROKE)
        sc.label(X, 190, act_note, size=15)
        sc.label(X, 216, f"lo={lo}，hi={hi}" + (f"，mi={mi}" if mi is not None else "") +
                 ("" if exited else "，区间宽度11→…逐次折半"), size=15, mono=True, fill=SUB)
        return sc

    lo, hi = 0, 11
    frames.append(frame("初始", "lo=0，hi=11，整个向量都是候选。", "不变性两端为空，自然成立。",
                        "mi取多少？", scene(lo, hi, None, "等待第一步。")))
    seq = [(5, "S[5]=F。D<F成立：e只可能在[0,5)，hi=5。", "e<S[mi]分支：一次比较，前缀保留。", 5),
           (2, "S[2]=C。D<C不成立：e只可能在(2,5)，lo=3。", "else分支：lo=mi+1，轴点被排除。", None),
           (4, "S[4]=E。D<E成立：hi=4。", "继续向左收缩。", 4)]
    for it, (mi, act, why, upd) in enumerate(seq, 1):
        frames.append(frame(f"第{it}次迭代：mi={mi}", act, why,
                            f"下一次mi是多少？" if it < 3 else None,
                            scene(lo, hi, mi, act)))
        if mi == 5:
            hi = 5
        elif mi == 2:
            lo = 3
        elif mi == 4:
            hi = 4
        frames.append(frame(f"第{it}次迭代后", f"lo={lo}，hi={hi}。", "候选区间缩小，不变性保持。",
                            "", scene(lo, hi, None, f"区间[{lo},{hi})仍含答案位置。")))
    frames.append(frame("退出：lo==hi==4", "区间宽度为0，返回lo−1=3。", "S[3]=D恰是不大于e的最后一个元素；插入位置是4。", "",
                        scene(4, 4, None, "返回3：即元素D的秩；search('D')=3。", exited=True)))
    return write_demo("ds05-binsearch-c", "二分查找版本C：区间收缩与返回值", frames)



DEMOS = {
    "ds01-bubble": demo_bubble_pass,
    "ds01-tm": demo_tm_increase,
    "ds01-ram": demo_ram_divide,
}


def main(argv):
    ids = argv or list(DEMOS)
    for did in ids:
        n = DEMOS[did]()
        print(f"{did}: {n} frames")


DEMOS.update({
    "ds02-iter": demo_iter_space,
    "ds03-gs-ls": demo_gs_ls,
    "ds04-insert": demo_vec_insert,
    "ds05-binsearch-c": demo_binsearch_c,
})



# ---------- 演示：ch05 uniquify 双指针 ----------

def demo_uniquify():
    a = [3, 3, 5, 5, 5, 5, 8, 8, 13, 13, 13, 13]
    n = len(a)
    frames = []
    W, H = 900, 240
    X, Y, CW = 24, 100, 70

    def scene(i, j, a_cur, act, why, q=None):
        sc = Scene(W, H)
        st = {}
        for k in range(n):
            if k <= i:
                st[k] = (DONE, DONE_STROKE)
            if k == i:
                st[k] = (WRITE, WRITE_STROKE)
            if k == j:
                st[k] = (HOT, HOT_STROKE)
        sc.array(X, Y, a_cur[:n], st, cw=CW, ch=44)
        sc.pointer(X + i * (CW + 2) + CW / 2 - 1, Y - 40, "i", WRITE_STROKE)
        sc.pointer(X + j * (CW + 2) + CW / 2 - 1, Y + 66, "j", HOT_STROKE)
        sc.label(X, 40, f"已确认无重复的前缀：[0, {i}]", size=15, mono=True)
        sc.label(X, 186, act, size=15)
        sc.label(X, 212, "为什么：" + why, size=14, fill=SUB)
        return sc

    i = 0
    a = list(a)
    frames.append(frame("初始", "i=0，j=1。前缀[0,1)天然无重复。", "两个指针分别站在已确认区间的末尾与待检查的位置。", "A[1]=A[0]，j会怎样？",
                        scene(0, 1, a, "等待比较。", "有序向量的重复元素必然相邻，只需比较相邻项。")))
    steps = []
    for j in range(1, n):
        same = a[j] == a[i]
        steps.append((j, same))
    j = 1
    log = []
    while j < n:
        same = a[j] == a[i]
        if same:
            frames.append(frame(f"j={j}：A[{j}]=A[{i}]={a[j]}，重复", "j右移一格，i不动。", "重复元素被跳过，不进入保留区。", "",
                                scene(i, j, a, "跳过。", "与保留区末尾相等者不必保留两份。")))
            j += 1
        else:
            i += 1
            a[i] = a[j]
            frames.append(frame(f"j={j}：A[{j}]={a[j]}是新元素", f"i前移至{i}，A[{i}]=A[{j}]={a[j]}。", "保留区扩张一格，新元素就位。",
                                "", scene(i, j, a, "写入保留区。", "新元素紧接保留区末尾放置，向量保持有序。")))
            j += 1
    frames.append(frame("扫描结束", f"j到达{n}，i={i}；_size更新为{i+1}，向量收缩为{a[:i+1]}。",
                        "12个元素剔重后剩4个，一次线性扫描完成，O(n)。",
                        "", scene(i, n - 1, a, "完成：3, 5, 8, 13。", "每个元素恰好被j访问一次。")))
    return write_demo("ds05-uniquify", "uniquify：双指针一次扫描去重", frames)


# ---------- 演示：ch05 Fibonacci查找 ----------

def demo_fibsearch():
    a = [2, 4, 6, 8, 10, 11, 12]
    e = 11
    frames = []
    W, H = 760, 260
    X, Y, CW = 30, 116, 96

    def scene(lo, hi, mi, fibv, note, exited=False):
        sc = Scene(W, H)
        st = {}
        for k in range(7):
            if mi is not None and k == mi:
                st[k] = (HOT, HOT_STROKE)
            elif k < lo or k >= hi:
                st[k] = (PALE, CELL_STROKE)
        sc.array(X, Y, a, st, cw=CW, ch=46)
        sc.label(X, 40, f"fib.get() = {fibv}；切分点 mi = lo + fib.get() − 1 = {mi}", size=15, mono=True)
        sc.label(X, 194, note, size=15)
        sc.label(X, 220, f"lo={lo}，hi={hi}", size=15, mono=True, fill=SUB)
        return sc

    fibs = [8, 5, 3, 2, 1]
    lo, hi = 0, 7
    fi = 0
    frames.append(frame("准备", "Fib对象从不小于n=7的最小Fibonacci项8开始。", "n取fib(k)−1形式时可反复套用黄金分割切分。",
                        "第一个切分点在哪？", scene(lo, hi, None, 8, "初始。")))
    probes = [(4, 5, "S[4]=10 < 11：e只可能在(4,7)，lo=5。", "深入后半段只需2次比较的一半，所以前段故意放长。"),
              (6, 2, "mi=5+2−1=6：S[6]=12 > 11：e只可能在[5,6)，hi=6。", "深入前半段只需1次比较，故前段短些。"),
              (5, 1, "mi=5+1−1=5：S[5]=11，命中！返回5。", "fibSearch在S[mi]处命中即停。")]
    for k, (mi, fibv, act, why) in enumerate(probes, 1):
        if k == 1:
            pass
        frames.append(frame(f"第{k}次探测：mi={mi}", act, why, "", scene(lo, hi, mi, fibv, act)))
        if k == 1:
            lo = 5
        elif k == 2:
            hi = 6
        else:
            frames.append(frame("命中", "fibSearch(11) = 5，共探测3次（4→6→5）。", "黄金分割切分使平均查找长度略优于二分版本A（7元素：4.00对4.14）。",
                                "", scene(lo, hi, mi, 1, "查找成功。", exited=True)))
    return write_demo("ds05-fibsearch", "Fibonacci查找：切分点4→6→5", frames)


# ---------- 演示：ch05 插值查找 ----------

def demo_interp():
    a = [5, 10, 12, 14, 19, 23, 29, 36, 39, 41, 44, 51, 54, 59, 72, 79, 82, 86, 92]
    e = 50
    frames = []
    W, H = 1080, 270
    X, Y, CW = 16, 118, 54

    def scene(lo, hi, mi, note, formula):
        sc = Scene(W, H)
        st = {}
        for k in range(19):
            if mi is not None and k == mi:
                st[k] = (HOT, HOT_STROKE)
            elif k < lo or k >= hi:
                st[k] = (PALE, CELL_STROKE)
            elif k == lo:
                st[k] = (WRITE, WRITE_STROKE)
        sc.array(X, Y, a, st, cw=CW, ch=46)
        sc.label(X, 40, formula, size=15, mono=True)
        if mi is not None:
            sc.pointer(X + mi * (CW + 2) + CW / 2 - 1, Y + 72, "mi", HOT_STROKE)
        sc.label(X, 240, note, size=15)
        return sc

    lo, hi = 0, 19
    frames.append(frame("初始", "lo=0，hi=19。数组近似均匀分布，秩与数值近似线性。", "插值公式按线性关系猜测目标位置。",
                        "e=50的秩估计是多少？", scene(0, 19, None, "初始。", "mi = lo + (hi−lo)(e−S[lo])/(S[hi]−S[lo])")))
    mi1 = 0 + 18 * (50 - 5) // (92 - 5)
    frames.append(frame(f"第1次插值：mi={mi1}", f"S[{mi1}]=41 < 50：lo={mi1+1}。", "猜测点落在目标左侧，区间右缩。",
                        "", scene(10, 19, mi1, "S[9]=41<50，lo=10。", "mi = 0 + 18×(50−5)/(92−5) = 9")))
    mi2 = 10 + 8 * (50 - 44) // (92 - 44)
    frames.append(frame(f"第2次插值：mi={mi2}", f"S[{mi2}]=51 > 50：hi={mi2}。", "猜测点落在目标右侧，区间左缩。",
                        "", scene(10, 11, mi2, "S[11]=51>50，hi=11。", "mi = 10 + 8×(50−44)/(92−44) = 11")))
    mi3 = 10 + 1 * (50 - 44) // (51 - 44)
    frames.append(frame(f"第3次插值：mi={mi3}", f"S[{mi3}]=44 < 50：lo={mi3+1}=11，lo==hi，退出。", "返回10：不大于50的最大者是44。",
                        "", scene(10, 11, mi3, "退出，search返回10。", "mi = 10 + 1×(50−44)/(51−44) = 10")))
    return write_demo("ds05-interp", "插值查找：3次定位（e=50）", frames)


# ---------- 演示：ch05 位图 ----------

def demo_bitmap():
    frames = []
    W, H = 760, 240
    bits = [0] * 24

    X0 = 40

    def scene(k, note, mark=None, clear=False):
        sc = Scene(W, H)
        sc.label(40, 30, "字节1（位8～15）：k=13 → 字节 13>>3=1，位 13&7=5，掩码 0x80>>5 = 0x04", size=14, fill=SUB, mono=True)
        for i in range(8):
            bit_i = 8 + i
            on = bits[bit_i]
            hot = (bit_i == k)
            sc.add("rect", x=X0 + i * 84, y=80, width=78, height=52, rx=8,
                   fill=(HOT if hot else (DONE if on else CELL)),
                   stroke=(HOT_STROKE if hot else (DONE_STROKE if on else CELL_STROKE)), stroke_width=1.5)
            sc.label(X0 + i * 84 + 39, 112, str(on), size=19, mono=True, anchor="middle")
            sc.label(X0 + i * 84 + 39, 148, str(bit_i), size=12, fill=FAINT, mono=True, anchor="middle")
        sc.label(X0, 196, note, size=15)
        return sc

    frames.append(frame("初始：全0", "24个比特分3个字节存放，初始全0。", '每一位只回答一个"有没有"。', "",
                        scene(None, "位图清零。")))
    bits[13] = 1
    frames.append(frame("set(13)", "定位字节1的第5位，按0x04置1。", "或运算写入，其余位不受影响。",
                        "", scene(13, "第13位变为1。")))
    frames.append(frame("test(13)", "F[k]<size且T[F[k]]==k（快速版）或直接读位：返回1。", "读位即判等，O(1)。",
                        "", scene(13, "test(13) = 1。")))
    bits[13] = 0
    frames.append(frame("clear(13)", "按掩码0x04清0（普通版）；快速版用校验环交换删除。", '清0后该位回到"没有"状态。',
                        "", scene(13, "第13位清0。")))
    return write_demo("ds05-bitmap", '位图：一个比特回答"有没有"', frames)


# ---------- 演示：ch05 筛法 ----------

def demo_sieve():
    N = 30
    nums = list(range(2, N))
    cleared = set()
    frames = []
    W, H = 900, 330
    cols = 10
    cw, chh = 80, 44

    def scene(cross, note, title):
        sc = Scene(W, H)
        sc.label(24, 30, title, size=15, fill=SUB)
        for idx, v in enumerate(nums):
            r, c = divmod(idx, cols)
            x, y = 30 + c * cw, 60 + r * 58
            gone = v in cleared
            hot = (v == cross)
            prime = (not gone) and v > 1
            sc.add("rect", x=x, y=y, width=cw - 8, height=chh, rx=8,
                   fill=(BAD if gone else (HOT if hot else (DONE if prime else CELL))),
                   stroke=(BAD_STROKE if gone else (HOT_STROKE if hot else (DONE_STROKE if prime else CELL_STROKE))), stroke_width=1.5)
            sc.label(x + (cw - 8) / 2, y + 28, str(v), size=16, mono=True, anchor="middle",
                     fill=(FAINT if gone else INK))
        sc.label(24, 250, note, size=15)
        sc.chip(24, 268, 120, 24, "质数", DONE, DONE_STROKE, size=13, mono=False)
        sc.chip(154, 268, 120, 24, "合数", BAD, BAD_STROKE, size=13, mono=False)
        sc.chip(284, 268, 130, 24, "本轮清除", HOT, HOT_STROKE, size=13, mono=False)
        return sc

    frames.append(frame("准备", "2～29各占一格，全部待筛。", "筛法的对象是连续整数区间，天然对应位图。", "",
                        scene(None, "从最小的质数2开始。", "Eratosthenes筛法：n=30")))
    seq = [(2, "从2²=4起，步长2清除：4,6,8,…,28共13个。", [v for v in range(4, N, 2)]),
           (3, "从3²=9起，步长3清除：9,15,21,27为新清除（12,18,24已被2筛过）。", [v for v in range(9, N, 3)]),
           (5, "从5²=25起清除：25（30越界）。", [25]),
           (7, "7²=49>30，筛法终止。", [])]
    for pr, note, cross in seq:
        cleared.update(cross)
        frames.append(frame(f"用质数{pr}筛", note, "小于p²的合数必含更小质因子，已被更早的轮次清除。",
                            "", scene(min(cross) if cross else None, note, f"用{pr}筛之后")))
    frames.append(frame("完成", "剩下10个质数：2,3,5,7,11,13,17,19,23,29。", "内循环总次数Σn/p ≈ n·ln ln n，几乎线性。",
                        "", scene(None, "筛法完成。", "Eratosthenes筛法：n=30")))
    return write_demo("ds05-sieve", "筛法：30以内怎么筛出质数", frames)


DEMOS.update({
    "ds05-uniquify": demo_uniquify,
    "ds05-fibsearch": demo_fibsearch,
    "ds05-interp": demo_interp,
    "ds05-bitmap": demo_bitmap,
    "ds05-sieve": demo_sieve,
})



# ---------- 演示：ch06 跳跃版起泡 ----------

def demo_bubble_jump():
    a = [2, 1, 3, 5, 4, 6, 7]
    n = len(a)
    frames = []
    W, H = 780, 236
    X, Y, CW = 50, 96, 58

    def scene(values, lo, hi, last, hot=None, note=None, newly=None):
        sc = Scene(W, H)
        sc.label(X, 30, f"跳跃版：本趟扫描区间[lo, hi)=[{lo}, {hi})，last={last}", size=15, fill=SUB, mono=True)
        st = {}
        for k in range(n):
            if k >= hi or k < lo:
                st[k] = (DONE, DONE_STROKE)
        if newly is not None:
            st[newly] = (WRITE, WRITE_STROKE)
        if hot:
            for k in hot:
                st[k] = (HOT, HOT_STROKE)
        sc.array(X, Y, values, st, cw=CW, ch=44)
        if hot:
            i = hot[0]
            sc.bracket(X + i * (CW + 2), X + (i + 1) * (CW + 2) - 2, Y - 12, f"a[{i}] ? a[{i+1}]", HOT_STROKE)
        sc.label(X, 210, note, size=15)
        return sc

    lo, hi = 0, n
    frames.append(frame("初态", "lo=0，hi=7。输入仅两处逆序：2>1与5>4。", "跳跃版的看点：一趟扫描能一次跳过多少尾部。",
                        "一趟扫描后last会是多少？", scene(a, lo, hi, 0, note="last每趟初始化为lo。")))
    # pass 1
    last = lo
    swaps = [(1, True), (4, True)]
    trace1 = [(0, False), (1, True), (2, False), (3, False), (4, True), (5, False)]
    for i, sw in trace1:
        if sw:
            a[i - 1], a[i] = a[i], a[i - 1]
            last = i
            frames.append(frame(f"比较a[{i-1}]与a[{i}]：逆序，交换", f"交换后last更新为{i}。",
                                "last记住本趟最后一次交换的位置。", "",
                                scene(a, lo, hi, last, hot=[i - 1, i], newly=i)))
        else:
            frames.append(frame(f"比较a[{i-1}]与a[{i}]：有序", "不交换，继续。", "该对非降序。", "",
                                scene(a, lo, hi, last, hot=[i - 1, i])))
    hi = last
    frames.append(frame("第1趟结束：hi跳到last=4", f"最后交换发生在a[3]与a[4]，后缀[4,7)必然就位，hi=4。",
                        "断言：[lo,last)的元素 < [last] <= (last,hi)的元素。下一趟只扫[0,4)。",
                        "", scene(a, lo, hi, last, note="区间从7缩短到4：跳过了3个元素。")))
    # pass 2
    last = lo
    for i in range(1, hi):
        frames.append(frame(f"第2趟：比较a[{i-1}]与a[{i}]：有序", "不交换。", "前缀已无逆序。", "",
                            scene(a, lo, hi, last, hot=[i - 1, i])))
    hi = last
    frames.append(frame("第2趟结束：last=0，hi=0", "整趟无交换，last保持lo=0，hi=0，循环退出。",
                        "sorted的语义：一趟无交换即整体有序。总耗时：第1趟6次比较、第2趟3次。",
                        "", scene(a, 0, 0, 0, note="最好情况O(n)的来源：一趟发现无逆序即收工。")))
    return write_demo("ds06-jump", "跳跃版起泡：last怎样让区间跳跃收缩", frames)


# ---------- 演示：ch06 二路归并 ----------

def demo_merge():
    A = [1, 3, 6, 7]
    B = [2, 4, 5, 8]
    frames = []
    W, H = 760, 300
    XA, XB, XS, Y, CW = 40, 40, 40, 88, 62

    def scene(Aa, Bb, S, a, b, note, why, done=None):
        sc = Scene(W, H)
        sc.label(XA, 30, "归并：A与B的首元素两两比较，小者优先进入S", size=15, fill=SUB)
        sc.label(XA, 60, "A（前缀副本）", size=13, fill=SUB)
        stA = {a: (HOT, HOT_STROKE)} if a < len(Aa) else {}
        sc.array(XA, Y, Aa, stA, cw=CW, ch=42)
        sc.label(XB, 60, "B（后缀本体）", size=13, fill=SUB)
        stB = {b: (HOT, HOT_STROKE)} if b < len(Bb) else {}
        sc.array(XB + 340, Y, Bb, stB, cw=CW, ch=42)
        sc.label(XS, 178, "S（归并输出，就地覆盖）", size=13, fill=SUB)
        for k in range(8):
            if k < len(S):
                f, stc = (WRITE, WRITE_STROKE)
                sc.add("rect", x=XS + k * (CW + 2), y=190, width=CW, height=42, rx=8, fill=f, stroke=stc, stroke_width=1.5)
                sc.label(XS + k * (CW + 2) + CW / 2, 216, str(S[k]), size=17, mono=True, anchor="middle")
            else:
                sc.add("rect", x=XS + k * (CW + 2), y=190, width=CW, height=42, rx=8, fill="#fbfdff",
                       stroke=CELL_STROKE, stroke_width=1.2)
                sc.label(XS + k * (CW + 2) + CW / 2, 216, "·", size=15, fill=FAINT, anchor="middle")
        sc.label(XA, 266, note, size=15)
        sc.label(XA, 258, why, size=13, fill=SUB) if False else None
        sc.label(XA, 288, "为什么：" + why, size=14, fill=SUB)
        return sc

    S = []
    a = b = 0
    frames.append(frame("准备", "A=[1,3,6,7]已复制出前缀；B=[2,4,5,8]留在原地。", "前缀会被S覆盖，必须先复制；后缀不会被覆盖，可直接使用。",
                        "第一对比较是谁和谁？", scene(A, B, S, 0, 0, "等待首次比较。", "指针a、b分别指向两个首元素。")))
    while a < len(A) and b < len(B):
        if A[a] <= B[b]:
            S.append(A[a]); a += 1
            act, why = f"A[a]={S[-1]} ≤ B[b]，A首元素进入S。", "取等号时优先取A：稳定性由此保证。"
        else:
            S.append(B[b]); b += 1
            act, why = f"B[b]={S[-1]} < A[a]，B首元素进入S。", "较小者归入S，指针右移。"
        frames.append(frame(f"S新增{S[-1]}", act, why, "", scene(A, B, S, a, b, act, why)))
    if a < len(A):
        S += A[a:]
        frames.append(frame("B耗尽：A残余整体归入", f"A剩下的{A[a:]}直接追加进S。", "A本就有序，无需再比较。",
                            "", scene(A, B, S, a, b, "A残余追加。", "B先耗尽的情形；若A先耗尽，B残余本就在S中，无需搬动。")))
    frames.append(frame("归并完成", "S=[1,2,3,4,5,6,7,8]，恰好a+b=4+4=8次输出。", "无论过程如何，总输出次数恒为la+lb=n：归并必为线性。",
                        "", scene(A, B, S, a, b, "二路归并完成。", "比较至多n−1次，输出恰好n次。")))
    return write_demo("ds06-merge", "二路归并：1,3,6,7与2,4,5,8怎样合并", frames)


DEMOS.update({
    "ds06-jump": demo_bubble_jump,
    "ds06-merge": demo_merge,
})



# ---------- 演示：ch07 insertPred 前插入 ----------

def demo_list_insert():
    """A → B，在B之前插入X。节点行距120，指针画为节点间水平线。"""
    frames = []
    W, H = 720, 300
    X0, Y0, NW, NH = 60, 150, 130, 54

    def node_scene(names, link_old, link_new, note, why, step_label='逐步演示'):
        sc = Scene(W, H)
        if step_label:
            sc.label(40, 30, step_label, size=15, fill=SUB)
        pos = {}
        for k, nm in enumerate(names):
            x = X0 + k * (NW + 50)
            pos[nm] = x + NW / 2
            hot = nm in ("X",)
            sc.add("rect", x=x, y=Y0, width=NW, height=NH, rx=10,
                   fill=(WRITE if hot else CELL), stroke=(WRITE_STROKE if hot else CELL_STROKE), stroke_width=1.5)
            sc.label(x + NW / 2, Y0 + 22, nm, size=18, mono=True, anchor="middle")
            sc.label(x + 20, Y0 + 44, "pred", size=10, fill=FAINT, mono=True)
            sc.label(x + NW - 20, Y0 + 44, "succ", size=10, fill=FAINT, mono=True, anchor="end")
        y = Y0 - 18
        for (src, dst, f, stc) in link_old:
            sc.add("line", x1=pos[src], y1=y, x2=pos[dst], y2=y, stroke=(PALE if (src, dst) in [(l[0], l[1]) for l in link_new] else stc), stroke_width=1.4)
        for (src, dst, f, stc) in link_new:
            sc.add("line", x1=pos[src], y1=y, x2=pos[dst], y2=y, stroke=stc, stroke_width=2.2)
            sc.add("circle", cx=pos[dst], cy=y, r=3, fill=stc)
        sc.label(40, 240, note, size=15)
        sc.label(40, 266, "为什么：" + why, size=14, fill=SUB)
        return sc

    A, B, X = "A", "B", "X"
    frames.append(frame("初态", "链表片段A → B。任务：把新节点X插入B之前。", "insertPred需要改动三处指针，次序不可颠倒。",
                        "先改哪一根？", node_scene([A, B], [(A, B, "", CELL_STROKE)], [(A, B, "", CELL_STROKE)], "尚无动作。", "新节点此刻还不存在。", "初态")))
    frames.append(frame("第一步：创建新节点X", "new ListNode(e, pred=B的pred=A, this=B)：X的pred指向A、succ指向B。", "构造时一次性接好两根 outgoing 指针，此后旧链仍完整。",
                        "", node_scene([A, X, B], [(A, B, "", CELL_STROKE)], [(A, X, "", WRITE_STROKE), (X, B, "", WRITE_STROKE)], "X诞生，两根新指针已接好。", "此刻A→B的旧链仍通，列表未被破坏。")))
    frames.append(frame("第二步：pred->succ = x", "让A的succ改指X。", "旧链A→B就此断开，新链A→X接通；此刻若停在半途，B会失联——次序不能颠倒的根源。",
                        "", node_scene([A, X, B], [(A, B, "", CELL_STROKE)], [(A, X, "", WRITE_STROKE), (X, B, "", WRITE_STROKE)], "A→X接通，A→B断开。", "X→B已在第一步接好，B依然可达。")))
    frames.append(frame("第三步：pred = x", "让B的pred改指X。", "反向链补齐，双向链表恢复一致；整个过程O(1)。",
                        "", node_scene([A, X, B], [(A, B, "", CELL_STROKE)], [(A, X, "", WRITE_STROKE), (X, B, "", WRITE_STROKE)], "三步完成：A → X → B。", "局部改动常数个指针，与列表总长无关。")))
    return write_demo("ds07-insert", "前插入：三根指针的次序", frames)


# ---------- 演示：ch07 remove 删除 ----------

def demo_list_remove():
    frames = []
    W, H = 720, 300
    X0, Y0, NW, NH = 40, 150, 120, 54

    def scene(names, links, note, why, marked=None):
        sc = Scene(W, H)
        sc.label(40, 30, "remove(p)：让两侧指针绕过被删节点", size=15, fill=SUB)
        pos = {}
        for k, nm in enumerate(names):
            x = X0 + k * (NW + 46)
            pos[nm] = x + NW / 2
            gone = (nm == marked)
            sc.add("rect", x=x, y=Y0, width=NW, height=NH, rx=10,
                   fill=(BAD if gone else CELL), stroke=(BAD_STROKE if gone else CELL_STROKE), stroke_width=1.5)
            sc.label(x + NW / 2, Y0 + 28, nm, size=18, mono=True, anchor="middle",
                     fill=(FAINT if gone else INK))
        y = Y0 - 18
        for (src, dst, stc) in links:
            sc.add("line", x1=pos[src], y1=y, x2=pos[dst], y2=y, stroke=stc, stroke_width=2.2)
            sc.add("circle", cx=pos[dst], cy=y, r=3, fill=stc)
        sc.label(40, 240, note, size=15)
        sc.label(40, 266, "为什么：" + why, size=14, fill=SUB)
        return sc

    frames.append(frame("初态", "链表片段A → p → C。要删除p。", "p的两侧指针必须先改，否则后续节点失联。",
                        "两根指针各改成什么？", scene(["A", "p", "C"], [("A", "p", CELL_STROKE), ("p", "C", CELL_STROKE)], "尚未动作。", "被删节点的pred、succ分别指向A与C。")))
    frames.append(frame("第一根：p->pred->succ = p->succ", "A的succ越过p改指C。", "正向链绕过p；此刻C还只能通过p的反向链找到。",
                        "", scene(["A", "p", "C"], [("A", "C", WRITE_STROKE), ("p", "C", CELL_STROKE)], "正向链已绕过p。", "反向链尚需第二根。")))
    frames.append(frame("第二根：p->succ->pred = p->pred", "C的pred越过p改指A。", "反向链接通后，p彻底出链；delete释放节点，规模减一。",
                        "", scene(["A", "C"], [("A", "C", WRITE_STROKE)], "A → C，删除完成，O(1)。", "同样只是局部常数根指针，与表长无关。")))
    return write_demo("ds07-remove", "删除节点：让两侧指针绕过它", frames)


DEMOS.update({
    "ds07-insert": demo_list_insert,
    "ds07-remove": demo_list_remove,
})



# ---------- 演示：ch08 进制转换 ----------

def demo_convert():
    frames = []
    W, H = 700, 280
    X, Y, CW = 60, 120, 66

    def scene(stack, popped, note, phase):
        sc = Scene(W, H)
        sc.label(X, 30, "convert(2026, 8)：反复模余入栈、除商更新；再整体弹出", size=15, fill=SUB)
        sc.label(X, 58, "2026 ÷ 8 = 253 … 2；253 ÷ 8 = 31 … 5；31 ÷ 8 = 3 … 7；3 ÷ 8 = 0 … 3", size=14, mono=True, fill=SUB)
        for i, c in enumerate(stack):
            sc.add("rect", x=X + 380, y=Y + i * 56, width=CW, height=48, rx=8,
                   fill=(HOT if i == len(stack) - 1 and phase == "push" else (WRITE if phase == "pop" and i == len(stack) - 1 else CELL)),
                   stroke=CELL_STROKE, stroke_width=1.5)
            sc.label(X + 380 + CW / 2, Y + i * 56 + 30, c, size=18, mono=True, anchor="middle")
        if stack:
            sc.label(X + 380 + CW + 12, Y + (len(stack) - 1) * 56 + 30, "← 栈顶", size=13, fill=FAINT, mono=True)
        sc.label(X, 96, "输出（自高到低）：" + (popped or "（尚无）"), size=16, mono=True)
        sc.label(X, 250, note, size=15)
        return sc

    stack = []
    frames.append(frame("准备", "目标：把十进制2026转成八进制。", "短除法自低向高产生数位：先得到低位，后得到高位——输出顺序恰好相反，正是栈的用武之地。",
                        "第一个入栈的是高位还是低位？", scene([], "", "等待模余。", "push")))
    for d, q, note in [("2", 253, "2026 % 8 = 2，入栈；商253继续。"),
                       ("5", 31, "253 % 8 = 5，入栈；商31继续。"),
                       ("7", 3, "31 % 8 = 7，入栈；商3继续。"),
                       ("3", 0, "3 % 8 = 3，入栈；商0，模余结束。")]:
        stack.append(d)
        frames.append(frame(f"push '{d}'", note, "低位先产生、后输出：入栈暂存。", "",
                            scene(list(stack), "", note, "push")))
    out = []
    for d in ["3", "7", "5", "2"]:
        stack.pop()
        out.append(d)
        frames.append(frame(f"pop '{d}'", f"弹出栈顶'{d}'，作为当前最高位输出。", "栈的LIFO恰好把低位次序反转为高位次序。",
                            "", scene(list(stack), " ".join(out), f"已输出 {' '.join(out)}。", "pop")))
    frames.append(frame("完成", "栈空，输出3752：2026(10) = 3752(8)。", "时间、空间均为O(log n)；相比递归版，手工栈省去了调用栈的常系数。",
                        "", scene([], "3 7 5 2", "转换完成。", "pop")))
    return write_demo("ds08-convert", "进制转换：2026怎样变成3752(8)", frames)


# ---------- 演示：ch08 括号匹配 ----------

def demo_paren():
    expr = "{[()]}"
    frames = []
    W, H = 700, 250
    X, Y, CW = 56, 120, 66

    def scene(i, stack, note, ok=None):
        sc = Scene(W, H)
        sc.label(X, 30, "paren()：左括号一律进栈；右括号必须与栈顶同类", size=15, fill=SUB)
        for k, c in enumerate(expr):
            hot = (k == i)
            sc.add("rect", x=X + k * (CW + 4), y=Y, width=CW, height=46, rx=8,
                   fill=(HOT if hot else (DONE if k < i else CELL)),
                   stroke=(HOT_STROKE if hot else (DONE_STROKE if k < i else CELL_STROKE)), stroke_width=1.5)
            sc.label(X + k * (CW + 4) + CW / 2, Y + 29, c, size=19, mono=True, anchor="middle")
        sc.label(X, 64, "栈（自底向顶）：" + (" ".join(stack) if stack else "（空）"), size=16, mono=True)
        verdict = ""
        if ok is True:
            verdict = "匹配！"
        sc.label(X, 216, note + ("　" + verdict if verdict else ""), size=15)
        return sc

    stack = []
    acts = [("push '{'", "字符0：'{'是左括号，进栈。", "栈里记录的是已扫到、尚未匹配的左括号。"),
            ("push '['", "字符1：'['进栈。", "新左括号只会与最近未被匹配的左括号配对。"),
            ("push '('", "字符2：'('进栈。", '栈顶永远是"最急需配对"的左括号。'),
            ("')'弹出'('", "字符3：')'与栈顶'('同类，弹出。", '消去一对紧邻的成对括号，原表达式匹配与否不受影响。'),
            ("']'弹出'['", "字符4：']'与栈顶'['同类，弹出。", "若类型不同即失配。"),
            ("'}'弹出'{'", "字符5：'}'与栈顶'{'同类，弹出。", "三层嵌套逐层脱壳。"),
            ("扫描结束", "全部扫完且栈空：匹配！若栈非空，则有左括号悬空。", "一趟顺序扫描，绝不回头。")]
    for i, (act, note, why) in enumerate(acts):
        if act.startswith("push"):
            stack.append(expr[i])
        elif act.startswith(("')'", "']'", "'}'")):
            stack.pop()
        frames.append(frame(act, note, why, "", scene(i, stack, note, ok=(i == len(acts) - 1))))
    return write_demo("ds08-paren", '括号匹配：{[()]}怎样通过一个栈', frames)


# ---------- 演示：ch08 表达式求值 ----------

def demo_eval():
    expr = ["1", "+", "2", "*", "3"]
    frames = []
    W, H = 720, 260
    X, Y = 50, 120

    def scene(opnd, optr, i, act, why, rule=''):
        sc = Scene(W, H)
        sc.label(X, 30, "evaluate('1 + 2 * 3')：数栈opnd、符栈optr；读入字符i=" + str(i), size=15, fill=SUB)
        for k, c in enumerate(expr):
            hot = (k == i)
            sc.add("rect", x=X + k * 96, y=Y, width=88, height=42, rx=8,
                   fill=(HOT if hot else (DONE if k < i else CELL)),
                   stroke=(HOT_STROKE if hot else (DONE_STROKE if k < i else CELL_STROKE)), stroke_width=1.5)
            sc.label(X + k * 96 + 44, Y + 27, c, size=18, mono=True, anchor="middle")
        sc.label(X, 82, f"opnd（数栈，自底向顶）：{opnd or '（空）'}", size=15, mono=True)
        sc.label(X, 106, f"optr（符栈，自底向顶）：{' '.join(optr) or '（空）'}", size=15, mono=True)
        sc.chip(X + 440, 208, 210, 24, f"规则：{rule}", WRITE, WRITE_STROKE, size=13, mono=False)
        sc.label(X, 216, act, size=15)
        sc.label(X, 242, "为什么：" + why, size=14, fill=SUB)
        return sc

    opnd, optr = [], []
    frames.append(frame("压入哨兵", "optr压入哨兵'\\0'，充当表达式起止的虚拟运算符。", "括号与哨兵统一处理：开始与结束都是一次优先级比较。",
                        "", scene([], ["\\0"], 0, "optr=[\\0]。", "哨兵让主循环只认一种终止方式。", "初始化")))
    opnd.append("1")
    frames.append(frame("读入1", "操作数直接进数栈。", "数、符分居两栈，互不干扰。", "",
                        scene(["1"], ["\\0"], 0, "opnd=[1]。", "操作数无需比较。")))
    optr.append("+")
    frames.append(frame("读入+：推迟", "prio(\\0, +)=<：栈顶优先级低，+进符栈。", "时机未到，静待右操作数。",
                        "", scene(["1"], ["\\0", "+"], 1, "optr=[$ +]。"[:14] + "+。", "'<'推迟计算。")))
    opnd.append("2")
    frames.append(frame("读入2", "操作数2进数栈。", "继续等待比较时机。", "",
                        scene(["1", "2"], ["\\0", "+"], 2, "opnd=[1 2]。", "'<'之后读入右操作数。")))
    optr.append("*")
    frames.append(frame("读入*：仍推迟", "prio(+, *)=<：乘号优先级更高，进符栈。", "栈内运算符优先级自底向顶递增，正是这一性质使栈顶随时可算。",
                        "", scene(["1", "2"], ["\\0", "+", "*"], 3, "optr=[$ + *]。", "'<'再推迟。")))
    opnd.append("3")
    frames.append(frame("读入3", "操作数3进数栈。", "至此2、3相拥于栈顶，乘法时机成熟。", "",
                        scene(["1", "2", "3"], ["\\0", "+", "*"], 4, "opnd=[1 2 3]。", "等待结束符触发回溯。")))
    opnd = ["1", "6"]; optr = ["\\0", "+"]
    frames.append(frame("遇\\0：执行*", "prio(*, \\0)=>：弹出*与2、3，算得6压回数栈。", "栈顶可算的判定只取决于局部相对优先级。",
                        "", scene(["1", "6"], ["\\0", "+"], 5, "opnd=[1 6]。", "'>'执行计算。")))
    opnd = ["7"]; optr = ["\\0"]
    frames.append(frame("执行+", "prio(+, \\0)=>：弹出+与1、6，算得7压回。", "逐层回溯至哨兵。", "",
                        scene(["7"], ["\\0"], 5, "opnd=[7]。", "'>'再执行。")))
    frames.append(frame("终止", "prio(\\0, \\0)=~：双哨兵相会，符栈弹空，opnd唯一剩值7即结果。", "从创世纪到世界末日：哨兵对标志求值的起与终。",
                        "", scene(["7"], [], 5, "返回7。", "'~'终须了断。")))
    return write_demo("ds08-eval", "表达式求值：1+2*3的两栈协作", frames)


# ---------- 演示：ch08 栈混洗甄别 ----------

def demo_stack_perm():
    B = [3, 1, 2]
    frames = []
    W, H = 700, 250
    X, Y = 56, 120

    def scene(a_next, stack, r, note, ok=None):
        sc = Scene(W, H)
        sc.label(X, 30, "spCheck([3,1,2])：A输入栈只记栈顶；S为中转栈；逐项尝试B操作", size=15, fill=SUB)
        sc.label(X, 58, f"A输入栈顶：{a_next if a_next <= 3 else '已空'}　　目标序列B：3 1 2　　已核对到第{r}项", size=15, mono=True)
        for i, v in enumerate(stack):
            sc.add("rect", x=X + 300, y=Y + i * 56, width=110, height=48, rx=8,
                   fill=(HOT if i == len(stack) - 1 else CELL), stroke=CELL_STROKE, stroke_width=1.5)
            sc.label(X + 355, Y + i * 56 + 30, str(v), size=18, mono=True, anchor="middle")
        if stack:
            sc.label(X + 420, Y + (len(stack) - 1) * 56 + 30, "← 栈顶", size=13, fill=FAINT, mono=True)
        verdict = ""
        if ok is False:
            verdict = "　判定：不是栈混洗（含禁形3 1 2）。"
        if ok is True:
            verdict = "　判定：是栈混洗。"
        sc.label(X, 216, note + verdict, size=15)
        return sc

    stack, A = [], 1
    frames.append(frame("初始", "A输入栈=[1,2,3]（只需记录栈顶1）；S空；目标B=[3,1,2]。", "逐项尝试B操作：目标元素若能腾挪至S顶部就弹出，否则卡住。",
                        "要弹出3，得先把几项压入S？", scene(A, [], 0, "等待核对B[0]=3。")))
    for v in (1, 2, 3):
        stack.append(v); A += 1
    A = 4
    frames.append(frame("连续A操作：push 1,2,3", "栈顶恰为3，随即可B操作。", "目标3之前必须先把1、2压入S暂存。", "",
                        scene(A, [1, 2, 3], 0, "3已到栈顶。")))
    stack.pop()
    frames.append(frame("B操作：弹出3", "S弹出3，与B[0]核对成功；r=1。", "3是最后压入的，最先弹出——符合LIFO。", "",
                        scene(A, [1, 2], 1, "已核对3。")))
    frames.append(frame("核对B[1]=1：卡住", "S顶=2 ≠ 1；A已空（1已在S底），无法把1腾挪到顶部。", "序列3 1 2含禁形：k=3在i=1的前缀中，j=2本应也在其中。",
                        "", scene(4, [1, 2], 1, "卡在r=1。", ok=False)))
    return write_demo("ds08-stackperm", "栈混洗甄别：[3,1,2]为什么卡住", frames)


DEMOS.update({
    "ds08-convert": demo_convert,
    "ds08-paren": demo_paren,
    "ds08-eval": demo_eval,
    "ds08-stackperm": demo_stack_perm,
})



# ---------- 演示：ch09 轮转调度 ----------

def demo_roundrobin():
    q = ["A", "B", "C", "D"]
    frames = []
    W, H = 720, 220
    X, Y, CW = 60, 110, 92

    def scene(queue, front, serve, note, round_no):
        sc = Scene(W, H)
        sc.label(X, 30, f"轮转调度第{round_no}轮：队首出队→接受一个时间片→重新入队", size=15, fill=SUB)
        for k, name in enumerate(queue):
            hot = (k == front) or (serve == name)
            sc.add("rect", x=X + k * (CW + 6), y=Y, width=CW, height=52, rx=10,
                   fill=(HOT if hot else (WRITE if k == len(queue) - 1 and serve else CELL)),
                   stroke=(HOT_STROKE if hot else CELL_STROKE), stroke_width=1.5)
            sc.label(X + k * (CW + 6) + CW / 2, Y + 26, name, size=18, mono=True, anchor="middle")
            if k == front:
                sc.label(X + k * (CW + 6) + CW / 2, Y - 8, "队首→出队", size=12, fill=HOT_STROKE, anchor="middle")
            if k == len(queue) - 1 and serve:
                sc.label(X + k * (CW + 6) + CW / 2, Y + 72, "← 重新入队", size=12, fill=WRITE_STROKE, anchor="middle")
        sc.label(X, 196, note, size=15)
        return sc

    frames.append(frame("初始队列", "A、B、C、D共享一个CPU，按FIFO公平轮转。", "队列保证谁等得最久谁先被服务。",
                        "一轮之后谁排在最前？", scene(q, 0, None, "等待调度。", 1)))
    for rnd in range(2):
        head = q.pop(0)
        frames.append(frame(f"第{rnd+1}轮：{head}出队", f"队首{head}出队，接受一个时间片的服务。", "服务时长quantum有限：一次只服务一小段。",
                            "", scene(q, 0, head, f"{head}正在服务。", rnd + 1)))
        q.append(head)
        frames.append(frame(f"第{rnd+1}轮：{head}重新入队", f"{head}挂到队尾，让位给等待更久的伙伴。", "出队→服务→入队三步，循环往复，公平由此而来。",
                            "", scene(q, 0, None, f"{head}已回到队尾。", rnd + 1)))
    frames.append(frame("公平性", "每轮循环后队列循环左移一格：没有客户会被饿死。", "FIFO次序即公平次序；CPU、打印机等共享资源皆用此法。",
                        "", scene(q, 0, None, "队列回到循环平移后的状态。", 3)))
    return write_demo("ds09-roundrobin", "轮转调度：出队、服务、再入队", frames)


# ---------- 演示：ch09 双栈当队 ----------

def demo_two_stack_queue():
    frames = []
    W, H = 760, 280
    XR, XF, Y, CW = 60, 420, 120, 70

    def scene(R, F, note, why, hotR=None, hotF=None):
        sc = Scene(W, H)
        sc.label(XR, 30, "R栈：只管enqueue（新元素压入R顶）", size=14, fill=SUB)
        for i, v in enumerate(R):
            sc.add("rect", x=XR, y=Y + (3 - i) * 54, width=CW, height=46, rx=8,
                   fill=(HOT if (hotR is not None and i == len(R) - 1 - hotR) else CELL),
                   stroke=CELL_STROKE, stroke_width=1.5)
            sc.label(XR + CW / 2, Y + (3 - i) * 54 + 29, v, size=17, mono=True, anchor="middle")
        sc.label(XF, 30, "F栈：只管dequeue（从F顶弹出）", size=14, fill=SUB)
        for i, v in enumerate(F):
            sc.add("rect", x=XF, y=Y + (3 - i) * 54, width=CW, height=46, rx=8,
                   fill=(HOT if (hotF is not None and i == len(F) - 1 - hotF) else CELL),
                   stroke=CELL_STROKE, stroke_width=1.5)
            sc.label(XF + CW / 2, Y + (3 - i) * 54 + 29, v, size=17, mono=True, anchor="middle")
        sc.label(XR, 252, note, size=15)
        sc.label(XR, 276, "为什么：" + why, size=14, fill=SUB)
        return sc

    R, F = ["A", "B", "C"], []
    frames.append(frame("连续入队A,B,C", "三个新元素依次压入R栈。", "enqueue只碰R，O(1)。", "",
                        scene(R, F, "R=[A,B,C]（C为顶）。", "F仍空，尚无出队需求。")))
    frames.append(frame("首次dequeue：倒腾", "F为空：把R整体逐一弹出压入F——C、B、A依次倒过去。", "倒腾后F顶恰是最早入队的A：FIFO次序由两次LIFO复合而成。",
                        "", scene([], ["C", "B", "A"], "整体倒腾，R清空、F=[C,B,A]。", "仅当F空时才倒腾，次序不会乱。")))
    frames.append(frame("dequeue出A", "弹出F顶A。", "队首是最老的A，先进先出。", "",
                        scene([], ["B", "A"], "弹出A。", "F顶=B，下一无需再倒腾。")))
    R.append("D")
    frames.append(frame("再入队D", "D压入R栈。", "enqueue永远只走R，不碰F。", "",
                        scene(["D"], ["B", "A"], "R=[D]，F=[B,A]。", "两栈分工明确，互不打扰。")))
    frames.append(frame("dequeue出B", "F非空：直接弹F顶B。", "F仍非空时绝不倒腾——这是均摊O(1)的关键纪律。",
                        "", scene(["D"], ["A"], "弹出B。", "每个元素至多被倒腾一次。")))
    return write_demo("ds09-two-stack", "双栈当队：R进F出，倒腾一次", frames)


# ---------- 演示：ch09 直方图单调栈 ----------

def demo_histogram():
    Hh = [2, 1, 4, 5, 1]
    n = len(Hh)
    frames = []
    W, H = 780, 300
    X, Y, BW = 40, 96, 90

    def scene(stack, popped, note, cur=None):
        sc = Scene(W, H)
        sc.label(X, 30, "单调栈求最大矩形：栈内高度自底向顶严格递增", size=15, fill=SUB)
        for k, h in enumerate(Hh):
            hot = (k == cur)
            bh = h * 18
            sc.add("rect", x=X + k * (BW + 12), y=Y + 150 - bh, width=BW, height=bh, rx=4,
                   fill=(HOT if hot else (DONE if k in popped else WRITE if (stack and stack[-1][0] == k) else CELL)),
                   stroke=(HOT_STROKE if hot else CELL_STROKE), stroke_width=1.5)
            sc.label(X + k * (BW + 12) + BW / 2, Y + 166, str(h), size=15, mono=True, anchor="middle")
            sc.label(X + k * (BW + 12) + BW / 2, Y + 184, str(k), size=12, fill=FAINT, mono=True, anchor="middle")
        tops = " ← ".join(f"r{k}(h{Hh[k]})" for k, _ in reversed(stack)) if stack else "（空）"
        sc.label(X, 216, "栈（自底→顶）：" + tops, size=14, mono=True)
        sc.label(X, 266, note, size=15)
        return sc

    stack = []
    popped_done = set()
    frames.append(frame("准备", "直方图[2,1,4,5,1]，加哨兵高度0于两端。", "最大矩形必以某根柱子为高度、向两侧扩展到极限。",
                        "遇到比栈顶矮的柱子时，谁被结算？", scene(stack, set(), "从左向右扫描。")))
    for r, h in enumerate(Hh):
        while stack and Hh[stack[-1][0]] >= h:
            k, _ = stack.pop()
            popped_done.add(k)
            left = stack[-1][0] + 1 if stack else 0
            width = r - left
            area = Hh[k] * width
            frames.append(frame(f"读入h[{r}]={h}：结算r{k}", f"H[{k}]={Hh[k]} ≥ {h}，弹出结算：宽{width}×高{Hh[k]}=面积{area}。",
                                "弹出即知左右边界：新柱提供了右边界，新栈顶提供了左边界。", "",
                                scene(stack, popped_done, f"柱r{k}被结算，面积{area}。", cur=r)))
        stack.append((r, h))
        frames.append(frame(f"h[{r}]={h}入栈", f"H[{r}]高于栈顶，直接入栈。", "保持栈内高度严格递增。",
                            "", scene(stack, popped_done, f"r{r}入栈。", cur=r)))
    # sentinel 0 flushes the rest
    areas = [2, 8, 5, 4]
    k, _ = stack.pop(); popped_done.add(k)
    left = stack[-1][0] + 1 if stack else 0
    area = Hh[k] * (n - left)
    frames.append(frame("哨兵0清栈：结算r4", f"末尾哨兵把滞留的r4结算：宽{n - left}×高1={area}。", "清栈阶段每个滞留柱子的右边界都是n。",
                        "", scene(stack, popped_done, f"全程各块面积：{areas}，最大8。")))
    frames.append(frame("完成", "最大矩形=高度4、宽度2（柱2与柱3），面积8。", "每个柱子至多入栈、出栈各一次：均摊O(n)。",
                        "", scene([], popped_done, "完成：最大矩形面积8。")))
    return write_demo("ds09-histogram", "直方图最大矩形：单调栈结算", frames)


DEMOS.update({
    "ds09-roundrobin": demo_roundrobin,
    "ds09-two-stack": demo_two_stack_queue,
    "ds09-histogram": demo_histogram,
})



# ---------- 演示：ch10 层次遍历 ----------

def demo_level_order():
    # tree: A(B(D,E),C(-,F))
    children = {"A": ["B", "C"], "B": ["D", "E"], "C": ["", "F"], "D": [], "E": [], "F": []}
    frames = []
    W, H = 760, 300
    TX, TY = 80, 110
    pos = {"A": (330, TY), "B": (180, TY + 90), "C": (480, TY + 90), "D": (100, TY + 180), "E": (260, TY + 180), "F": (560, TY + 180)}

    def scene(queue, visited, note, deq=None):
        sc = Scene(W, H)
        sc.label(40, 30, "层次遍历：队列Q；出队→访问→孩子依次入队", size=15, fill=SUB)
        edges = [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F")]
        for (p1, p2) in edges:
            x1, y1 = pos[p1]; x2, y2 = pos[p2]
            sc.add("line", x1=x1, y1=y1 + 26, x2=x2, y2=y2 - 6, stroke=LINE, stroke_width=1.6)
        for nm, (x, y) in pos.items():
            done = nm in visited
            hot = (deq == nm)
            infut = nm in queue
            fill = HOT if hot else (DONE if done else (WRITE if infut else CELL))
            stc = HOT_STROKE if hot else (DONE_STROKE if done else (WRITE_STROKE if infut else CELL_STROKE))
            sc.add("rect", x=x - 34, y=y - 4, width=68, height=40, rx=10, fill=fill, stroke=stc, stroke_width=1.5)
            sc.label(x, y + 22, nm, size=17, mono=True, anchor="middle")
        sc.label(40, 36, "队列Q（自队首向队尾）：" + (" ".join(queue) if queue else "（空）"), size=15, mono=True)
        sc.label(40, 288, note, size=15)
        return sc

    q = ["A"]; visited = []
    frames.append(frame("根入队", "根A入队。", "层次遍历按深度自上而下、同层自左向右；队列的FIFO恰保证这一顺序。",
                        "A出队后谁入队？", scene(q, visited, "Q=[A]。")))
    order = []
    while q:
        v = q.pop(0); visited.append(v); order.append(v)
        kids = [k for k in children.get(v, []) if k]
        note = f"访问{v}" + ("，孩子 " + " ".join(kids) + " 依次入队。" if kids else "，叶节点无孩子。")
        q.extend(kids)
        frames.append(frame(f"出队访问 {v}", note, "先访问者，其孩子先入队——同层次序由入队次序保证。",
                            "", scene(q, visited, note, deq=v)))
    frames.append(frame("完成", f"访问序列：{' '.join(order)}。", "队列FIFO保证：同层节点先访问者的孩子也先入队、先访问。",
                        "", scene([], visited, f"层次遍历序列：{' '.join(order)}。")))
    return write_demo("ds10-level", "层次遍历：队列怎样决定访问次序", frames)


DEMOS.update({"ds10-level": demo_level_order})



# ---------- 演示：ch11 Huffman贪心合并 ----------

def demo_huffman():
    # freq: A=2 B=3 C=5 D=8
    # merges: (A2,B3)->5A ; (C5,5A)->10C ; (D8,10C)->18
    steps = [("合并A2与B3 → 权5", "森林中最小的两个：A(2)、B(3)。合并为新树，权重5。", "贪心：最小的两个配对，保证它们处于最深处。", ["C5", "5A", "D8"], "5A"),
             ("合并C5与5A → 权10", "新的最小两个：C(5)与刚合成的5A。合并为10。", "刚合成的树立即参与后续比较。", ["D8", "10C"], "10C"),
             ("合并D8与10C → 权18", "最后两棵合并为整棵Huffman树，权重18=全部频数和。", "迭代n−1次后森林只剩一棵。", [], "18D")]
    frames = []
    W, H = 740, 250

    def scene(forest, note, hl=None):
        sc = Scene(W, H)
        sc.label(40, 30, "Huffman贪心：森林F中取出权重最小的两棵合并，插回森林", size=15, fill=SUB)
        for k, (nm, wt) in enumerate(forest):
            hot = (nm == hl)
            sc.add("rect", x=60 + k * 150, y=90, width=130, height=64, rx=10,
                   fill=(HOT if hot else CELL), stroke=(HOT_STROKE if hot else CELL_STROKE), stroke_width=1.5)
            sc.label(60 + k * 150 + 65, 118, nm, size=17, mono=True, anchor="middle")
            sc.label(60 + k * 150 + 65, 140, f"w={wt}", size=13, fill=FAINT, mono=True, anchor="middle")
        sc.label(40, 210, note, size=15)
        return sc

    frames.append(frame("初始森林", "四个字符按频数作为单节点树：A2、B3、C5、D8。", "编码目标：总编码长度（带权路径长WPL）最小。",
                        "先合并哪两个？", scene([("A", 2), ("B", 3), ("C", 5), ("D", 8)], "初始：四棵单节点树。")))
    for t, (title, act, why, forest, hl) in enumerate(steps, 1):
        frames.append(frame(title, act, why, "", scene([(nm, int(nm[-1] if nm[-1].isdigit() else 5)) for nm in forest] if forest else [], act, hl)))
    codes = "A=110，B=111，C=10，D=0"
    wpl = 3*2 + 3*3 + 2*5 + 1*8
    frames.append(frame("编码结果", f"WPL = 3×2 + 3×3 + 2×5 + 1×8 = {wpl}。", "频数最高的D只占1位，最低的A占3位：高频短码、低频长码。",
                        "", scene([("D", 8)], f"编码：{codes}；WPL={wpl}。")))
    return write_demo("ds11-huffman", "Huffman贪心合并：2,3,5,8", frames)


DEMOS.update({"ds11-huffman": demo_huffman})



# ---------- 演示：ch12 AVL双旋LR ----------

def demo_avl_lr():
    frames = []
    W, H = 720, 300
    # node positions per stage
    stages = [
        # (nodes{val:(x,y)}, edges[(p,c)], imbalanced, note, act, why)
        ({5: (360, 90), 3: (220, 190)},
         [(5, 3)], None,
         "插入3：成为5的左孩子，树仍平衡（各点|balFac|≤1）。", "insert(3)。", "平衡因子balFac = h左 − h右。"),
        ({5: (360, 90), 3: (220, 190), 4: (290, 190)},
         [(5, 3), (3, 4)], 5,
         "插入4：落在3的右侧。g=5的balFac升到+2，失衡；p=3（较高孩子），v=4（p的较高孩子）。", "insert(4)引发失衡。", "p与v异侧：LR型失衡，需双旋。"),
        ({4: (290, 90), 3: (170, 190), 5: (410, 190)},
         [(4, 3), (4, 5)], None,
         "双旋（zag(p)后zig(g)，等价于rotateAt(v)）：v=4升至根部，3、5各归两侧。", "以v为轴双旋。", "三节点中序3<4<5保持不变——等价变换，上下可变、左右不乱。"),
    ]

    def scene(nodes, edges, gnode, note, act, why):
        sc = Scene(W, H)
        sc.label(40, 30, act, size=15, fill=SUB)
        for (p1, p2) in edges:
            x1, y1 = nodes[p1]; x2, y2 = nodes[p2]
            sc.add("line", x1=x1, y1=y1 + 26, x2=x2, y2=y2 - 8, stroke=LINE, stroke_width=2)
        for val, (x, y) in nodes.items():
            hot = (val == gnode)
            fill = BAD if hot else (WRITE if val == 4 else CELL)
            stc = BAD_STROKE if hot else (WRITE_STROKE if val == 4 else CELL_STROKE)
            sc.add("rect", x=x - 36, y=y - 6, width=72, height=44, rx=10, fill=fill, stroke=stc, stroke_width=1.5)
            sc.label(x, y + 20, str(val), size=18, mono=True, anchor="middle")
        sc.label(40, 266, note, size=15)
        sc.label(40, 290, "为什么：" + why, size=14, fill=SUB)
        return sc

    for (nodes, edges, gnode, note, act, why) in stages:
        frames.append(frame(act, note, why, "", scene(nodes, edges, gnode, note, act, why)))
    frames.append(frame("结果", "AVL性质恢复：新根4的balFac=0，3、5的balFac=0。", "高度复原：插入后的复衡只需局部双旋，更高祖先不受影响。",
                        "", scene(stages[2][0], stages[2][1], None, "双旋完成。", "恢复平衡。", "单旋LL/RR同理：p与v同侧时只需一次旋转。")))
    return write_demo("ds12-avl-lr", "AVL双旋：LR失衡与复衡", frames)


DEMOS.update({"ds12-avl-lr": demo_avl_lr})



# ---------- 演示：ch13 B树插入上溢分裂 ----------

def demo_btree_insert():
    frames = []
    W, H = 760, 280

    def nodebox(x, y, keys, hot=True):
        sc = Scene(W, H)
        w = 46 * len(keys) + 24
        sc.add("rect", x=x, y=y, width=w, height=44, rx=8,
               fill=(HOT if hot else CELL), stroke=(HOT_STROKE if hot else CELL_STROKE), stroke_width=1.5)
        for i, k in enumerate(keys):
            sc.label(x + 20 + 46 * i + 23, y + 28, str(k), size=17, mono=True, anchor="middle")
        return x + w / 2

    def scene(root, kids, note, why):
        sc = Scene(W, H)
        sc.label(40, 30, "3阶B树（(2,3)-树）：节点至多2个关键码、3个分支", size=15, fill=SUB)
        if root:
            rx = nodebox(300, 150, root, hot=True)
            for i, kk in enumerate(kids):
                cx = 120 + i * 220
                nodebox(cx - 45 * len(kk) + 45, 230, kk, hot=False)
                sc.add("line", x1=rx, y1=196, x2=cx, y2=226, stroke=LINE, stroke_width=1.6)
        sc.label(40, 216 if not root else 92, note, size=15)
        sc.label(40, 262, "为什么：" + why, size=14, fill=SUB)
        return sc

    frames.append(frame("插入5", "空树：5成为根，单节点[5]。", "B树插入总是先落在叶节点。", "", scene([5], [], "根=[5]。", "规模1，无上溢。")))
    frames.append(frame("插入8", "8并入根：[5, 8]。", "仍不超过2个关键码，无需分裂。", "", scene([5, 8], [], "根=[5, 8]。", "满载边缘。")))
    frames.append(frame("插入11：上溢！", "[5, 8, 11]有3个关键码，超出上界。", "m=3阶节点关键码上限为m−1=2。", "", scene([5, 8, 11], [], "上溢！必须分裂。", "上溢节点必为叶。")))
    frames.append(frame("分裂：中码上提", "取中间关键码8上提出根；5、11分居两叶。", "分裂后关键码数2×⌈m/2⌉−2≤2m，必然不再上溢；树高+1仅此一种情形。",
                        "", scene([8], [[5], [11]], "分裂完成：根[8]，两叶[5]、[11]。", "外部节点保持理想平衡。")))
    frames.append(frame("插入15", "15大于8，落到右叶：[11, 15]。", "查找自根下行至叶，插入叶内；未上溢则结束。",
                        "", scene([8], [[5], [11, 15]], "完成。", "外部节点仍全部同层。")))
    return write_demo("ds13-btree", "B树插入：[5,8,11]怎样分裂", frames)


DEMOS.update({"ds13-btree": demo_btree_insert})



# ---------- 演示：ch14 kd树平面划分 ----------

def demo_kdtree():
    # points: A(90,150) B(200,90) C(150,220) D(260,200)
    pts = {"A": (90, 150), "B": (200, 90), "C": (150, 220), "D": (260, 200)}
    frames = []
    W, H = 740, 300

    def scene(splits, node, note, rect=None):
        sc = Scene(W, H)
        sc.label(40, 30, "kd树：交替按x、y轴二分平面（左闭右开）", size=15, fill=SUB)
        for (x1, y1, x2, y2, col) in splits:
            sc.add("line", x1=x1, y1=y1, x2=x2, y2=y2, stroke=col, stroke_width=2)
        for nm, (x, y) in pts.items():
            hot = (nm == node)
            sc.add("circle", cx=x, cy=y, r=8, fill=(HOT if hot else WRITE), stroke=(HOT_STROKE if hot else WRITE_STROKE), stroke_width=1.5)
            sc.label(x + 14, y - 8, nm, size=15, mono=True)
        sc.label(40, 272, note, size=15)
        return sc

    xs = sorted(p[0] for p in pts.values())
    medx = xs[1]
    frames.append(frame("第1层：按x轴中位点划分", "四个点的x中位数取C.x=150，画竖直分割线；C归右侧（左闭右开）。", "偶数层取VERTICAL，奇数层取HORIZONTAL。",
                        "", scene([(150, 60, 150, 250, WRITE_STROKE)], "C", "竖线x=150把平面分成两半。")))
    frames.append(frame("第2层：左半按y轴划分", "左半{A, B}：y中位数为A.y=150，画横线。", "每层换一个维度：x→y→x→y……",
                        "", scene([(150, 60, 150, 250, WRITE_STROKE), (60, 150, 148, 150, DONE_STROKE)], "A", "横线y=150分割左半区。")))
    frames.append(frame("第3层：右半按y轴划分", "右半{C, D}：y中位数为D.y=200，画横线。", "递归直至每区至多1点，成为叶子。",
                        "", scene([(150, 60, 150, 250, WRITE_STROKE), (60, 150, 148, 150, DONE_STROKE), (152, 200, 290, 200, DONE_STROKE)], "D", "递归完成：四点四叶。")))
    frames.append(frame("区域查询示意", "查询矩形R：区域region(v)⊆R则整棵子树输出；region(v)∩R=∅则整枝剪除。", "正交范围查询的复杂度O(n^(1-1/d)+r)。",
                        "", scene([(150, 60, 150, 250, WRITE_STROKE), (60, 150, 148, 150, DONE_STROKE), (152, 200, 290, 200, DONE_STROKE)], None, "剪枝依据：区域不相交即排除。")))
    return write_demo("ds14-kdtree", "kd树：平面交替二分", frames)


DEMOS.update({"ds14-kdtree": demo_kdtree})



# ---------- 演示：ch15 线性试探 ----------

def demo_linear_probing():
    M = 7
    frames = []
    W, H = 780, 240
    X, Y, CW = 40, 110, 94

    def scene(table, states, probe=None, note=None):
        sc = Scene(W, H)
        sc.label(X, 30, f"闭散列·线性试探：M={M}，hash(k)=k % {M}", size=15, fill=SUB)
        for i in range(M):
            f, stc = states.get(i, (CELL, CELL_STROKE))
            if probe is not None and i == probe:
                f, stc = HOT, HOT_STROKE
            sc.add("rect", x=X + i * (CW + 4), y=Y, width=CW, height=46, rx=8, fill=f, stroke=stc, stroke_width=1.5)
            sc.label(X + i * (CW + 4) + CW / 2, Y + 29, str(table[i]) if table[i] else "", size=17, mono=True, anchor="middle")
            sc.label(X + i * (CW + 4) + CW / 2, Y + 64, str(i), size=12, fill=FAINT, mono=True, anchor="middle")
        sc.label(X, 200, note, size=15)
        return sc

    table = [None] * M
    writes = []
    frames.append(frame("空表", "7个桶全部为空。", "hash(k) = k % M 定位首选桶。", "12会落在哪个桶？", scene(table, {})))
    table[5] = 12
    frames.append(frame("插入12：直接命中", "12 % 7 = 5，桶[5]空，直接放入。", "无冲突时一次定位。", "",
                        scene(table, {5: (WRITE, WRITE_STROKE)}, probe=5)))
    table[5 + 1] = 26
    frames.append(frame("插入26：冲突后试探", "26 % 7 = 5，桶[5]已被占，试探[6]：空，放入。", "线性试探：依次向后一个桶查找空位。",
                        "", scene(table, {6: (WRITE, WRITE_STROKE)}, probe=6)))
    table[5 + 2 - M] = 19   # (5+2) % M = 0
    frames.append(frame("插入19：连锁试探", "19 % 7 = 5，[5]、[6]接连被占，试探[7%7]=[0]：空，放入。", "注意：19本应落[5]，却安家[0]——聚集把冲突推远了。",
                        "", scene(table, {0: (WRITE, WRITE_STROKE)}, probe=0)))
    frames.append(frame("初级聚集", "桶[5][6][0]连成一片；此后任何hash值落在5、6、0的键都要连环试探。", "初级聚集：键连续的词条占据一段区间，区间内新冲突还会加剧扩张。MAD法/平方试探可缓解。",
                        "", scene(table, {5: (DONE, DONE_STROKE), 6: (DONE, DONE_STROKE), 0: (DONE, DONE_STROKE)}, probe=None)))
    return write_demo("ds15-probing", "线性试探：冲突怎样连成一片", frames)


DEMOS.update({"ds15-probing": demo_linear_probing})



# ---------- 演示：ch17 Dijkstra松弛 ----------

def demo_dijkstra():
    # edges: S->A(10), S->B(3), B->A(4), A->C(2), B->C(8)
    adj = {"S": [("A", 10), ("B", 3)], "B": [("A", 4), ("C", 8)], "A": [("C", 2)], "C": []}
    frames = []
    W, H = 780, 270

    def scene(dist, done, popped, note, relax=None):
        sc = Scene(W, H)
        sc.label(40, 30, "Dijkstra：每步取出dist最小且未定的顶点，松弛其邻居", size=15, fill=SUB)
        sc.label(40, 58, "dist: " + "  ".join(f"{k}={'∞' if dist.get(k) is None else dist[k]}" for k in ["S", "A", "B", "C"]), size=15, mono=True)
        sc.label(40, 84, "已确定: " + (" ".join(done) if done else "（无）"), size=15, mono=True)
        if popped:
            sc.chip(500, 44, 200, 26, f"取出 {popped}", HOT, HOT_STROKE, size=14, mono=True)
        if relax:
            sc.label(40, 240, "松弛：" + relax, size=14, mono=True)
        sc.label(40, 214, note, size=15)
        return sc

    dist = {"S": 0, "A": None, "B": None, "C": None}
    done = []
    frames.append(frame("初始化", "dist[S]=0，其余∞。", "最短路径树从S生长；每个前缀本身就是最短路径。", "",
                        scene(dist, done, None, "等待取出S。")))
    done.append("S")
    frames.append(frame("取出S，松弛邻居", "S出列确定。松弛A：0+10=10；B：0+3=3。", "dist单调下降的候选进入优先队列。", "",
                        scene({"S": 0, "A": 10, "B": 3, "C": None}, done, "S", "A:0+10=10；B:0+3=3")))
    done.append("B")
    frames.append(frame("取出B（dist=3），松弛", "B确定为3。松弛A：min(10, 3+4)=7改进；C：3+8=11。", "经B绕行更短，A的候选值从10降到7。",
                        "", scene({"S": 0, "A": 7, "B": 3, "C": 11}, done, "B", "A:3+4=7；C:3+8=11")))
    done.append("A")
    frames.append(frame("取出A（dist=7），松弛", "A确定为7。松弛C：min(11, 7+2)=9改进。", "S→B→A→C全程9，优于直达绕行。",
                        "", scene({"S": 0, "A": 7, "B": 3, "C": 9}, done, "A", "C:7+2=9")))
    done.append("C")
    frames.append(frame("取出C，结束", "C确定为9。全部顶点确定。", "负权边时本贪心失效——需Bellman-Ford；每对顶点则用Floyd。",
                        "", scene({"S": 0, "A": 7, "B": 3, "C": 9}, done, "C", None)))
    return write_demo("ds17-dijkstra", "Dijkstra：S/A/B/C的松弛过程", frames)


DEMOS.update({"ds17-dijkstra": demo_dijkstra})



# ---------- 演示：ch19 KMP next表 ----------

def demo_kmp_next():
    P = "MAMMIA"
    nxt = [-1, 0, 0, 1, 1, 0, 0]
    frames = []
    W, H = 760, 230

    def scene(j, t, note):
        sc = Scene(W, H)
        sc.label(40, 30, f"next表构造（模式P=MAMMIA）：当前算到j={j}，t={t}", size=15, fill=SUB)
        for k in range(6):
            hot = (k == j - 1)
            sc.add("rect", x=40 + k * 74, y=80, width=66, height=46, rx=8,
                   fill=(HOT if hot else (WRITE if k < j else CELL)),
                   stroke=(HOT_STROKE if hot else (WRITE_STROKE if k < j else CELL_STROKE)), stroke_width=1.5)
            sc.label(40 + k * 74 + 33, 109, P[k], size=18, mono=True, anchor="middle")
            sc.label(40 + k * 74 + 33, 142, f"next[{k}]={nxt[k]}", size=12, mono=True, anchor="middle",
                     fill=(INK if k < j + 1 else FAINT))
        sc.label(40, 200, note, size=15)
        return sc

    frames.append(frame("约定", "next[0] = -1：失配时模式串从最左重启。", "next[j]：P[0,j)中最长真自匹配前缀的长度——失配时j直接跳到next[j]。",
                        "", scene(0, -1, "起点：next[0]=-1。")))
    frames.append(frame("j=3，t=0：P[2]=M=P[0]命中", "t增至1，next[3]=1。", "前缀M已自匹配到位置2。", "",
                        scene(3, 1, "next[3]=1。")))
    frames.append(frame("j=4，t=1：P[3]=M与P[1]=A失配", "回退t=next[1]=0；P[0]=M=P[3]命中，t=1，next[4]=1。", "回退由已算好的next表指引，绝不重扫。",
                        "", scene(4, 1, "next[4]=1。")))
    frames.append(frame("j=5，t=1：P[1]=A与P[4]=I失配", "回退t=next[1]=0；再比P[0]=M与P[4]=I仍失配，t=next[0]=-1，终止。next[5]=0。", "自匹配传递链：回退次序即next表本身。",
                        "", scene(5, 0, "next[5]=0。")))
    frames.append(frame("j=6，t=0：P[0]=M与P[5]=A失配", "t=next[0]=-1终止，next[6]=0。构造完成：next=[-1,0,0,1,1,0]。", "查询时失配于j，j直接跳到next[j]，正文指针i绝不回退。",
                        "", scene(6, 0, "完成：[-1,0,0,1,1,0]。")))
    return write_demo("ds19-kmp", "KMP next表：MAMMIA逐步构造", frames)


DEMOS.update({"ds19-kmp": demo_kmp_next})



# ---------- 演示：ch20 LUG划分 ----------

def demo_partition():
    frames = []
    W, H = 780, 230

    def scene(a, lo, hi, gphase, note, done_idx=None):
        sc = Scene(W, H)
        sc.label(40, 30, f"LUG划分：pivot=6，lo={lo}，hi={hi}，当前向{'左拓展G' if gphase else '右拓展L'}", size=15, fill=SUB)
        for k, v in enumerate(a):
            hot = (k == done_idx)
            fill = (WRITE if hot else (HOT if (k == lo or k == hi - 1) and not hot else CELL))
            stc = (WRITE_STROKE if hot else (HOT_STROKE if (k == lo or k == hi - 1) and not hot else CELL_STROKE))
            sc.add("rect", x=40 + k * 118, y=90, width=110, height=52, rx=8, fill=fill, stroke=stc, stroke_width=1.5)
            sc.label(40 + k * 118 + 55, 122, str(v), size=18, mono=True, anchor="middle")
        sc.label(40, 200, note, size=15)
        return sc

    a = [6, 3, 8, 2, 9, 1]
    frames.append(frame("候选轴点=6", "取A[lo]=6为候选轴点（实际先经随机交换）。L=[0,0)空，G=[6,6)空，中间全是未定U。", "轴点只需n−1次比较、2次移动。",
                        "两端如何交替收缩？", scene(a, 0, 6, True, "未动。")))
    a2 = [1, 3, 8, 2, 9, 1]
    frames.append(frame("G拓展：1归入L端", "6>1：把1搬到左端A[0]，G换向L。", "L=[0,1)={1}≤6；空穴在右端[5]。", "",
                        scene(a2, 0, 5, False, "A=[1,3,8,2,9,·]。")))
    a3 = [1, 3, 8, 2, 9, 8]
    frames.append(frame("L拓展：8归入G端", "3<6留在L；8≥6被甩到右端A[5]，G换向。", "L=[0,2)={1,3}；空穴回到中间[2]。", "",
                        scene(a3, 2, 5, True, "A=[1,3,·,2,9,8]。")))
    a4 = [1, 3, 2, 6, 9, 8]
    frames.append(frame("就位：6落到秩3", "9>6跳过；2<6搬至左端；lo==hi=3，轴点6就位。", "L=[1,3,2]≤6、G=[9,8]>6；就地、线性、不稳定。",
                        "", scene(a4, 3, 4, True, "划分完成：pivot就位秩3。", done_idx=3)))
    return write_demo("ds20-partition", "LUG划分：6怎样各就各位", frames)


DEMOS.update({"ds20-partition": demo_partition})



# ---------- CS演示 ----------

CS_IMG = ROOT / "计算机系统概论" / "资料" / "超级纲要" / "图片"

def demo_cs_overflow():
    """8位补码：127+1=-128。"""
    bits = list("01111111")
    frames = []
    W, H = 740, 230
    X, Y, CW = 52, 100, 82

    def scene(b, note, carry=False):
        sc = Scene(W, H)
        sc.label(X, 30, "8位补码：int8_t a = 127; a = a + 1; 会得到什么？", size=15, fill=SUB)
        for i, c in enumerate(b):
            sc.add("rect", x=X + i * (CW + 4), y=Y, width=CW, height=50, rx=8,
                   fill=(WRITE if (carry and i == 7) else CELL), stroke=CELL_STROKE, stroke_width=1.5)
            sc.label(X + i * (CW + 4) + CW / 2, Y + 31, c, size=19, mono=True, anchor="middle")
            sc.label(X + i * (CW + 4) + CW / 2, Y + 68, f"2^{7-i}", size=11, fill=FAINT, mono=True, anchor="middle")
        sc.chip(X, 176, 220, 26, "符号位=最高位", WRITE, WRITE_STROKE, size=13, mono=False)
        sc.label(X + 240, 192, note, size=15)
        return sc

    frames.append(frame("127 = 01111111", "正数补码即其二进制：最高位0表示非负，数值=64+32+16+8+4+2+1=127。", "8位有符号数的范围是−128到+127。",
                        "127加1后每一位会怎样？", scene(bits, "初始。")))
    b2 = list("10000000")
    frames.append(frame("加1：10000000", "末位+1产生连续进位，得10000000。", "补码规则下最高位是符号位：1开头即负数。",
                        "", scene(b2, "位串变成10000000。", carry=True)))
    frames.append(frame("按补码解释：−128", "10000000的补码值=−(2^7)=−128。127+1没有越过8位边界时会得到129，这里却得到−128：有符号溢出。", "C标准规定有符号溢出是未定义行为；机器层按模256回绕。",
                        "", scene(b2, "a读出为−128。", carry=True)))
    return write_demo("cs02-overflow", "8位补码溢出：127+1=−128", frames, outdir=CS_IMG)


def demo_cs_stack():
    """main→funcA→funcB调用栈压栈与弹栈。"""
    frames = []
    W, H = 720, 280
    X, Y, FW, FH = 90, 60, 340, 52

    def scene(stack, note, why=''):
        sc = Scene(W, H)
        sc.label(X, 30, "调用栈：每次调用压入一帧（参数+局部变量+返回地址），返回弹出一帧", size=15, fill=SUB)
        for i, (nm, ra) in enumerate(stack):
            hot = (i == len(stack) - 1)
            y = Y + i * (FH + 8)
            sc.add("rect", x=X, y=y, width=FW, height=FH, rx=10,
                   fill=(HOT if hot else CELL), stroke=(HOT_STROKE if hot else CELL_STROKE), stroke_width=1.5)
            sc.label(X + 14, y + 22, nm, size=16, mono=True)
            sc.label(X + FW - 14, y + 22, f"返回地址 {ra}", size=13, mono=True, anchor="end", fill=SUB)
        sc.label(X + FW + 20, Y + 24, "栈底", size=13, fill=FAINT)
        sc.label(X + FW + 20, Y + len(stack) * (FH + 8) + 4, "栈顶", size=13, fill=FAINT)
        sc.label(X, 262, note, size=15)
        sc.label(X, 284, "为什么：" + why, size=13, fill=SUB) if False else None
        return sc

    frames.append(frame("main运行中", "栈里只有main帧：局部i=9。", "程序启动时main是栈底。", "",
                        scene([("main()", "0x0700")], "栈深1。")))
    frames.append(frame("调用funcA：压栈", "funcA(i*i)=funcA(81)被调用：压入新帧，含j=81、k、返回地址0x1000。", "返回地址记录调用点下一条指令的地址，返回时跳回。",
                        "", scene([("main()", "0x0700"), ("funcA(j=81,k=27)", "0x1000")], "栈深2。")))
    frames.append(frame("funcA调用funcB：再压栈", "funcB(k+5)=funcB(32)：新帧m=32、返回地址0x1500。", "递归同理：每层自己的参数与局部变量互不干扰。",
                        "", scene([("main()", "0x0700"), ("funcA(j=81,k=27)", "0x1000"), ("funcB(m=32)", "0x1500")], "栈深3。")))
    frames.append(frame("funcB返回：弹栈", "funcB结束：弹出其帧，跳回0x1500回到funcA。", "栈顶帧的返回地址决定回到哪里；数据随帧消失。",
                        "", scene([("main()", "0x0700"), ("funcA(j=81,k=27)", "0x1000")], "栈深2，回到funcA。")))
    frames.append(frame("全部返回", "funcA、main相继返回，栈清空。", "递归深度=最深时的栈帧数——这就是第03章'空间取决于深度'的机器根源。", "",
                        scene([("main()", "0x0700")], "回到main。")))
    return write_demo("cs06-stack", "调用栈：main→funcA→funcB的压栈弹栈", frames, outdir=CS_IMG)


def demo_cs_pagetable():
    """虚拟地址0x12AB经单级页表翻译到物理地址0x3AAB。"""
    frames = []
    W, H = 760, 240
    X, Y = 50, 96

    def scene(vp, pf, note, step_lbl):
        sc = Scene(W, H)
        sc.label(X, 30, step_lbl, size=15, fill=SUB)
        sc.add("rect", x=X, y=Y, width=200, height=48, rx=8, fill=WRITE, stroke=WRITE_STROKE, stroke_width=1.5)
        sc.add("rect", x=X + 104, y=Y, width=96, height=48, rx=0, fill=HOT, stroke=HOT_STROKE, stroke_width=1.5)
        sc.label(X + 52, Y + 30, "0x12", size=17, mono=True, anchor="middle")
        sc.label(X + 152, Y + 30, "AB", size=17, mono=True, anchor="middle")
        sc.label(X + 52, Y + 62, "虚拟页号", size=11, fill=FAINT, anchor="middle")
        sc.label(X + 152, Y + 62, "页内偏移", size=11, fill=FAINT, anchor="middle")
        sc.label(X + 240, Y + 30, "页表：0x12 → 0x3A（驻留、可读）", size=15, mono=True)
        sc.add("rect", x=X + 40, y=Y + 92, width=200, height=48, rx=8, fill=WRITE, stroke=WRITE_STROKE, stroke_width=1.5)
        sc.add("rect", x=X + 144, y=Y + 92, width=96, height=48, rx=0, fill=HOT, stroke=HOT_STROKE, stroke_width=1.5)
        sc.label(X + 92, Y + 122, "0x3A", size=17, mono=True, anchor="middle")
        sc.label(X + 192, Y + 122, "AB", size=17, mono=True, anchor="middle")
        sc.label(X + 92, Y + 154, "物理页框", size=11, fill=FAINT, anchor="middle")
        sc.label(X + 192, Y + 154, "偏移不变", size=11, fill=FAINT, anchor="middle")
        sc.label(X, 216, note, size=15)
        return sc

    frames.append(frame("拆分虚拟地址", "0x12AB=0001001010101011：低8位0xAB是页内偏移，其余0x12是虚拟页号。", "页大小256=2^8，低8位天然是偏移。",
                        "", scene("0x12", "0x3A", "第一步：拆出页号与偏移。", "拆分。")))
    frames.append(frame("查页表替换页号", "页表把虚拟页0x12翻译为物理页框0x3A；偏移原样保留。", "翻译只改页号，页内字节次序不受影响。",
                        "", scene("0x12", "0x3A", "物理地址=0x3A00+0xAB=0x3AAB。", "翻译。")))
    return write_demo("cs11-pagetable", "页表翻译：0x12AB怎样到0x3AAB", frames, outdir=CS_IMG)


DEMOS.update({
    "cs02-overflow": demo_cs_overflow,
    "cs06-stack": demo_cs_stack,
    "cs11-pagetable": demo_cs_pagetable,
})



# ---------- 物理演示 ----------

PH_IMG = ROOT / "大学物理B(2)" / "资料" / "超级纲要" / "图片"

def demo_ph_gauss():
    """点电荷在球心：球面通量Φ=E·4πr²与半径无关。"""
    import math
    frames = []
    W, H = 720, 260
    CX, CY = 250, 150

    def scene(r_px, note, ratio):
        sc = Scene(W, H)
        sc.label(40, 30, f"高斯面：球面半径r={ratio}倍，电场E∝1/r²，通量Φ=E·4πr²", size=15, fill=SUB)
        sc.add("circle", cx=CX, cy=CY, r=r_px, fill="none", stroke=WRITE_STROKE, stroke_width=2)
        sc.add("circle", cx=CX, cy=CY, r=4, fill=HOT_STROKE)
        sc.label(CX + 10, CY - 8, "+q", size=14, mono=True, fill=SUB)
        # field arrows on the sphere
        for ang in range(0, 360, 45):
            rad = ang * 3.14159 / 180
            x1 = CX + r_px * 0.75 * math.cos(rad); y1 = CY + r_px * 0.75 * math.sin(rad)
            x2 = CX + (r_px + 22) * math.cos(rad); y2 = CY + (r_px + 22) * math.sin(rad)
            sc.add("line", x1=x1, y1=y1, x2=x2, y2=y2, stroke=WRITE_STROKE, stroke_width=1.4)
            sc.add("circle", cx=x2, cy=y2, r=2.5, fill=WRITE_STROKE)
        sc.label(470, 120, f"E = kq/r²（r={ratio}倍基准）", size=15, mono=True)
        sc.label(470, 148, "面积 = 4πr²（∝r²）", size=15, mono=True)
        sc.label(470, 176, "Φ = E·4πr² = kq·4π（与r无关）", size=15, mono=True, fill=INK)
        sc.label(40, 238, note, size=15)
        return sc

    frames.append(frame("小球面 r", "以点电荷为球心作小球面，电场处处垂直球面、大小相等。", "通量=E×面积：E按1/r²变弱，面积按r²变大，两者相乘不变。",
                        "换大球面，通量变吗？", scene(60, "小球面：Φ₁。", "1")))
    frames.append(frame("大球面 2r", "半径加倍：E减为1/4，面积增为4倍。", "Φ₂=E/4 × 4A = E·A = Φ₁：通量与半径无关。",
                        "", scene(110, "大球面：Φ₂=Φ₁。", "2")))
    frames.append(frame("高斯定理", "Φ = q/ε₀：通量只由面内电荷决定，与面的大小形状无关。", "库仑定律与高斯定理等价；对称分布时先定方向再算大小。",
                        "", scene(110, "任意闭合曲面同理：只看面内电荷。", "2")))
    return write_demo("ph03-gauss", "高斯面：半径加倍，通量不变", frames, outdir=PH_IMG)


def demo_ph_flux_change():
    """磁铁插入线圈：磁通增大→感应电流阻碍增大。"""
    frames = []
    W, H = 760, 250
    CX, CY = 200, 140

    def scene(magnet_y, arrow, current, note):
        sc = Scene(W, H)
        sc.label(40, 30, "电磁感应：磁铁N极插入线圈，磁通增大，感应电流方向阻碍增大", size=15, fill=SUB)
        # coil: several vertical lines
        for k in range(5):
            sc.add("line", x1=CX - 60 + k * 24, y1=CY - 45, x2=CX - 60 + k * 24, y2=CY + 45, stroke=CELL_STROKE, stroke_width=3)
        # magnet
        sc.add("rect", x=CX - 22, y=magnet_y - 60, width=44, height=40, rx=4, fill="#fbe4e4", stroke=BAD_STROKE, stroke_width=1.5)
        sc.label(CX, magnet_y - 34, "N", size=17, mono=True, anchor="middle", fill=BAD_STROKE)
        sc.add("rect", x=CX - 22, y=magnet_y - 20, width=44, height=40, rx=4, fill=WRITE, stroke=WRITE_STROKE, stroke_width=1.5)
        sc.label(CX, magnet_y + 6, "S", size=17, mono=True, anchor="middle", fill=WRITE_STROKE)
        if arrow:
            sc.add("line", x1=CX + 40, y1=magnet_y - 50, x2=CX + 40, y2=magnet_y - 10, stroke=HOT_STROKE, stroke_width=2)
            sc.add("circle", cx=CX + 40, cy=magnet_y - 10, r=3, fill=HOT_STROKE)
        if current:
            sc.label(CX + 90, CY, "感应电流（逆时针，迎面看）", size=14, fill=SUB)
        sc.label(40, 226, note, size=15)
        return sc

    frames.append(frame("磁铁远处", "N极在线圈上方远处：穿过线圈的磁通接近零。", "感应电流的大小与方向都取决于磁通的变化率，静置时无电流。", "",
                        scene(20, False, False, "磁通≈0。")))
    frames.append(frame("插入中：磁通增大", "N极逼近，向下穿过线圈的磁通增大。", "楞次定律：感应电流的磁场要阻碍磁通的增大——感应磁场方向向上。",
                        "", scene(110, True, False, "磁通增大中。")))
    frames.append(frame("感应电流出现", "由右手定则，从上往下看线圈中电流为逆时针：其磁场向上顶住N极。", "阻碍≠阻止：磁铁仍可插入，只是需要克服斥力做功，机械能转化为电能。",
                        "", scene(150, True, True, "插入过程中持续有感应电流。")))
    return write_demo("ph11-induction", "磁铁插入线圈：磁通与阻碍", frames, outdir=PH_IMG)


def demo_ph_interference():
    """双缝干涉：光程差 δ=d·sinθ，明纹 δ=mλ。"""
    frames = []
    W, H = 780, 270
    SX, SY = 70, 135

    def scene(offset, note, k):
        sc = Scene(W, H)
        sc.label(40, 30, f"双缝干涉：光程差δ=d·sinθ；明纹条件δ=mλ（图中m={k}）", size=15, fill=SUB)
        sc.add("circle", cx=SX - 40, cy=SY, r=6, fill=HOT_STROKE)
        sc.label(SX - 52, SY - 14, "光源", size=13, fill=SUB)
        for slit in (SY - 30, SY + 30):
            sc.add("rect", x=SX + 60, y=slit - 22, width=10, height=18, rx=2, fill=INK)
            sc.add("rect", x=SX + 60, y=slit + 4, width=10, height=18, rx=2, fill=INK)
            sc.add("line", x1=SX - 30, y1=SY, x2=SX + 58, y2=slit, stroke=WRITE_STROKE, stroke_width=1.6)
            sc.add("line", x1=SX + 72, y1=slit, x2=560, y2=SY + offset, stroke=WRITE_STROKE, stroke_width=1.6)
        sc.add("line", x1=560, y1=50, x2=560, y2=220, stroke=CELL_STROKE, stroke_width=3)
        sc.label(566, 60, "屏", size=13, fill=SUB)
        if k is not None:
            sc.add("circle", cx=572, cy=SY + offset, r=6, fill=HOT_STROKE)
            sc.label(588, SY + offset + 4, f"m={k}明纹", size=13, mono=True, fill=INK)
        sc.label(40, 244, note, size=15)
        return sc

    frames.append(frame("中央明纹 m=0", "两缝到屏中央等距：光程差δ=0，两波同相叠加，中央最亮。", "所有波长的m=0都重合在正中。",
                        "", scene(0, "δ=0：中央亮纹。", 0)))
    frames.append(frame("一级明纹 m=1", "向上偏转使δ=d·sinθ恰好等于一个波长λ：同相叠加，一级明纹。", "sinθ=λ/d决定一级明纹的偏角。",
                        "", scene(-64, "δ=λ：一级明纹。", 1)))
    frames.append(frame("暗纹处", "δ=λ/2（半整数）：两波反相相消，屏幕上出现暗纹。", "明暗相间的条纹间距Δy=λL/d，红光比紫光条纹更宽。",
                        "", scene(-32, "δ=λ/2：暗纹（相消）。", None)))
    return write_demo("ph15-interference", "双缝干涉：光程差决定明暗", frames, outdir=PH_IMG)


DEMOS.update({
    "ph03-gauss": demo_ph_gauss,
    "ph11-induction": demo_ph_flux_change,
    "ph15-interference": demo_ph_interference,
})



# ---------- CS演示批2 ----------

def demo_cs_addressing():
    """mov %rax, 0x8(%rbx): 基址+偏移寻址。"""
    frames = []
    W, H = 740, 230
    X, Y = 50, 100

    def scene(base_val, offset, target, note):
        sc = Scene(W, H)
        sc.label(X, 30, "mov %rax, 0x8(%rbx)：目标地址 = (%rbx) + 0x8", size=15, fill=SUB)
        sc.add("rect", x=X, y=Y, width=250, height=46, rx=8, fill=WRITE, stroke=WRITE_STROKE, stroke_width=1.5)
        sc.label(X + 125, Y + 29, f"%rbx = 0x{base_val}", size=17, mono=True, anchor="middle")
        sc.add("rect", x=X + 280, y=Y, width=140, height=46, rx=8, fill=CELL, stroke=CELL_STROKE, stroke_width=1.5)
        sc.label(X + 350, Y + 29, f"+ 0x{offset}", size=17, mono=True, anchor="middle")
        sc.add("rect", x=X + 450, y=Y, width=220, height=46, rx=8, fill=HOT, stroke=HOT_STROKE, stroke_width=1.5)
        sc.label(X + 560, Y + 29, f"目标 0x{target}", size=17, mono=True, anchor="middle")
        sc.label(X, 200, note, size=15)
        return sc

    frames.append(frame("读寄存器基址", "%rbx保存数组首地址0x1000。", "编译器把数组名翻译成基址寄存器。",
                        "偏移0x8对应第几个int？", scene("1000", "8", "1100", "待计算。")))
    frames.append(frame("基址+偏移求和", "0x1000 + 0x8 = 0x1008：第2个int元素（下标2，因int占4字节，偏移=2×4=8）。", "结构体字段、数组下标最终都编译成这种基址+偏移形式。",
                        "", scene("1000", "8", "1008", "%rax写入0x1008。")))
    return write_demo("cs04-addressing", "基址加偏移：0x8(%rbx)指到哪里", frames, outdir=CS_IMG)


def demo_cs_outofbounds():
    """int a[5]; a[10]=7 越界写覆盖相邻变量。"""
    frames = []
    W, H = 780, 240
    X, Y, CW = 40, 100, 90

    def scene(cells, note, hot=None):
        sc = Scene(W, H)
        sc.label(X, 30, "int a[5] 与相邻变量 b 在栈上的布局：a[10]=7 会写到哪里？", size=15, fill=SUB)
        labels = ["a[0]", "a[1]", "a[2]", "a[3]", "a[4]", "b"]
        for i, lb in enumerate(labels):
            hotk = (hot == i)
            sc.add("rect", x=X + i * (CW + 4), y=Y, width=CW, height=52, rx=8,
                   fill=(BAD if hotk else (WRITE if i == 5 else CELL)),
                   stroke=(BAD_STROKE if hotk else (WRITE_STROKE if i == 5 else CELL_STROKE)), stroke_width=1.5)
            sc.label(X + i * (CW + 4) + CW / 2, Y + 27, lb, size=15, mono=True, anchor="middle")
            sc.label(X + i * (CW + 4) + CW / 2, Y + 46, f"+{4*i}", size=11, fill=FAINT, mono=True, anchor="middle")
        sc.label(X, 196, note, size=15)
        return sc

    frames.append(frame("合法范围", "a有5个元素：合法下标0至4，占20字节。", "编译器不做下标检查：a[i]就是取a首地址+4i。",
                        "a[10]的地址是多少？", scene([], None)))
    frames.append(frame("a[10]的地址", "a+4×10=a+40：越出a的20字节，落在b（+20字节处）再往后的位置。", "具体落在哪个变量由布局决定——这正是危险所在：可能改掉b，也可能改掉别的。",
                        "", scene([], "a[10]指向b之后的格子。", hot=5)))
    frames.append(frame("越界写与未定义行为", "C标准把越界访问定义为未定义行为：不检查、不报错、后果随布局。", "防范靠规范与工具：循环边界自查、开启-fsanitize=address等。",
                        "", scene([], "后果不可预知，唯有不越界。")))
    return write_demo("cs07-bounds", "数组越界：a[10]=7写到谁头上", frames, outdir=CS_IMG)


def demo_cs_fork():
    """fork：一次调用两次返回，进程树1→2→3。"""
    frames = []
    W, H = 760, 240

    def scene(nodes, note, hot=None):
        sc = Scene(W, H)
        sc.label(40, 30, "fork：把当前进程复制一份，父子从同一行代码之后各自继续", size=15, fill=SUB)
        pos = {}
        for (pid, x, y) in nodes:
            pos[pid] = (x, y)
            hotk = (pid == hot)
            sc.add("rect", x=x - 46, y=y - 24, width=92, height=48, rx=10,
                   fill=(HOT if hotk else (WRITE if pid > 1 else CELL)),
                   stroke=(HOT_STROKE if hotk else CELL_STROKE), stroke_width=1.5)
            sc.label(x, y + 6, f"pid {pid}", size=15, mono=True, anchor="middle")
        edges = [(1, 2), (1, 3), (2, 3)]
        # only parent-child edges based on nodes present
        present = set(p for p, _, _ in nodes)
        for (a, b) in edges:
            if a in present and b in present and b > a:
                x1, y1 = pos[a]; x2, y2 = pos[b]
                sc.add("line", x1=x1, y1=y1 + 24, x2=x2, y2=y2 - 24, stroke=LINE, stroke_width=1.8)
        sc.label(40, 214, note, size=15)
        return sc

    frames.append(frame("初始：只有pid 1", "父进程pid=1运行中。", "fork之前的代码只执行一次。", "",
                        scene([(1, 380, 70)], "进程树只有根。")))
    frames.append(frame("pid 1调用fork", "复制出一个pid=2：两者从fork返回处继续，fork的返回值不同——父得到孩子的pid，孩子得到0。", "用返回值区分父子，走不同的分支。",
                        "", scene([(1, 260, 70), (2, 500, 70)], "树分出一支。", hot=2)))
    frames.append(frame("pid 2再fork出pid 3", "孩子也可以再fork：树继续生长。", "几次fork就有2^k个进程——面试与OJ常见的计数题。",
                        "", scene([(1, 260, 70), (2, 500, 70), (3, 620, 150)], "三代进程树。", hot=3)))
    return write_demo("cs09-fork", "fork：一次调用，两份进程", frames, outdir=CS_IMG)


DEMOS.update({
    "cs04-addressing": demo_cs_addressing,
    "cs07-bounds": demo_cs_outofbounds,
    "cs09-fork": demo_cs_fork,
})



# ---------- CS批3 + 物理批2 ----------

def demo_cc():
    """cmp与条件码：ZF/SF/OF。"""
    frames = []
    W, H = 740, 210

    def scene(zf, sf, of, note):
        sc = Scene(W, H)
        sc.label(40, 30, "cmp %rax, %rbx：做减法rbx−rax，只写条件码不改寄存器", size=15, fill=SUB)
        for i, (nm, v) in enumerate([("ZF", zf), ("SF", sf), ("OF", of)]):
            sc.add("rect", x=40 + i * 130, y=80, width=118, height=50, rx=8,
                   fill=(WRITE if v else CELL), stroke=CELL_STROKE, stroke_width=1.5)
            sc.label(40 + i * 130 + 59, 100, nm, size=14, fill=FAINT, anchor="middle")
            sc.label(40 + i * 130 + 59, 120, str(v), size=18, mono=True, anchor="middle")
        zf_name = {0: "不相等(jne)", 1: "相等(je)"}[zf]
        sc.label(40, 182, note + f"　跳转判断：ZF=1 → je（相等）。", size=15)
        return sc

    frames.append(frame("cmp后ZF=1：相等", "rbx == rax：减法结果为0，ZF（零标志）置1。", "je/jne只看ZF：相等走je分支。", "",
                        scene(1, 0, 0, "结果为0。")))
    frames.append(frame("cmp后ZF=0：不等", "rbx != rax：结果非0，ZF=0。", "此时jne成立。", "",
                        scene(0, 1, 0, "结果非0（SF=1示意差值为负）。")))
    frames.append(frame("OF：溢出才置1", "OF只在带符号溢出时置1：如127+1=−128。", "无符号比较看CF，带符号比较看SF⊕OF——两条jump系列因此分开。",
                        "", scene(0, 0, 1, "示意溢出情形。")))
    return write_demo("cs05-cc", "条件码：cmp之后ZF/SF/OF", frames, outdir=CS_IMG)


def demo_malloc():
    """malloc(32)在空闲块中切割，free后合并。"""
    frames = []
    W, H = 760, 210
    X, Y, CW = 40, 96, 108

    def scene(blocks, note):
        sc = Scene(W, H)
        sc.label(40, 30, "隐式空闲链表：头部记录块大小与分配位；分配即切割、释放即合并", size=15, fill=SUB)
        x = X
        for (sz, allocated) in blocks:
            w = CW * sz // 16
            sc.add("rect", x=x, y=Y, width=w - 4, height=54, rx=6,
                   fill=(WRITE if allocated else PALE), stroke=(WRITE_STROKE if allocated else FAINT), stroke_width=1.5)
            sc.label(x + (w - 4) / 2, Y + 24, str(sz * 8), size=15, mono=True, anchor="middle")
            sc.label(x + (w - 4) / 2, Y + 42, "已分配" if allocated else "空闲", size=11, anchor="middle",
                     fill=(WRITE_STROKE if allocated else FAINT))
            x += w
        sc.label(40, 188, note, size=15)
        return sc

    blocks = [(8, True), (4, False), (6, True), (8, False), (6, True)]
    frames.append(frame("堆的当前布局", "已有三块分配、两块空闲（各4、8个double字）。", "malloc(32字节)需要4字块：首个放得下的是末尾8字空闲块。", "",
                        scene(blocks, "查找第一个足够大的空闲块。")))
    blocks = [(8, True), (4, False), (6, True), (4, True), (4, False), (6, True)]
    frames.append(frame("切割：前4字分配", "8字空闲块切出4字给malloc，剩下4字仍是空闲块。", "切割让空闲块越来越碎——碎片化由此而来。",
                        "", scene(blocks, "malloc(32)完成。")))
    blocks = [(8, True), (14, False), (6, True)]
    frames.append(frame("free后合并", "释放中间4字块：与两侧空闲块合并成14字大块。", "合并对抗碎片：free不只标记，还要看邻居是否空闲。",
                        "", scene([(8, True), (14, False), (6, True)], "free(中块)并合并。")))
    return write_demo("cs12-malloc", "malloc/free：切割与合并", frames, outdir=CS_IMG)


def demo_ph_capacitor():
    """电容器充电：Q上升、V=Q/C。"""
    frames = []
    W, H = 720, 230
    X, Y = 60, 100

    def scene(q_frac, note, stage):
        sc = Scene(W, H)
        sc.label(40, 30, f"RC充电：Q(t)=CE(1−e^(−t/RC))，阶段：{stage}", size=15, fill=SUB)
        # battery
        sc.add("line", x1=X, y1=Y + 20, x2=X, y2=Y + 60, stroke=INK, stroke_width=2)
        sc.add("line", x1=X - 14, y1=Y + 60, x2=X + 14, y2=Y + 60, stroke=INK, stroke_width=3)
        sc.add("line", x1=X - 7, y1=Y + 72, x2=X + 7, y2=Y + 72, stroke=INK, stroke_width=3)
        sc.add("line", x1=X, y1=Y + 72, x2=X, y2=Y + 110, stroke=INK, stroke_width=2)
        # wires
        sc.add("line", x1=X, y1=Y + 20, x2=X + 220, y2=Y + 20, stroke=INK, stroke_width=2)
        sc.add("line", x1=X, y1=Y + 110, x2=X + 220, y2=Y + 110, stroke=INK, stroke_width=2)
        # capacitor plates: charge markers
        plate = X + 220
        sc.add("line", x1=plate, y1=Y + 20, x2=plate, y2=Y + 52, stroke=INK, stroke_width=2)
        sc.add("line", x1=plate, y1=Y + 78, x2=plate, y2=Y + 110, stroke=INK, stroke_width=2)
        sc.add("line", x1=plate - 12, y1=Y + 52, x2=plate + 12, y2=Y + 52, stroke=INK, stroke_width=3)
        sc.add("line", x1=plate - 12, y1=Y + 78, x2=plate + 12, y2=Y + 78, stroke=INK, stroke_width=3)
        for i in range(q_frac):
            sc.label(plate - 5, Y + 48 - 0, "+", size=14, mono=True, fill=WRITE_STROKE) if False else None
        for i in range(min(q_frac, 6)):
            sc.add("circle", cx=plate - 6, cy=Y + 40 - i * 8, r=3, fill=WRITE_STROKE)
        for i in range(min(q_frac, 6)):
            sc.add("circle", cx=plate + 6, cy=Y + 92 - i * 8, r=3, fill=BAD_STROKE)
        sc.label(plate + 40, Y + 64, f"Q = {q_frac}/6 · CE", size=15, mono=True)
        sc.label(40, 200, note, size=15)
        return sc

    frames.append(frame("接通瞬间 t=0", "Q=0：电容器还没囤电荷，相当于短路，电流最大。", "充电快慢由时间常数τ=RC决定。",
                        "", scene(0, "初始：两板无电荷。", "t=0")))
    frames.append(frame("充电中 t=τ", "Q达0.63CE：板上电荷渐多，排斥同号电荷继续涌入，电流按指数衰减。", "每过一个τ，Q上涨剩余缺口的63%。",
                        "", scene(4, "充电中，电流减小。", "t=τ")))
    frames.append(frame("充满 t→∞", "Q=CE：两板电压等于电源电动势，电流归零。", "电容器隔直流：充满后稳态无电流。",
                        "", scene(6, "充满：Q=CE。", "t→∞")))
    return write_demo("ph08-rc", "RC充电：Q怎样逼近CE", frames, outdir=PH_IMG)


def demo_ph_diffraction():
    """单缝衍射：a·sinθ=mλ暗纹。"""
    frames = []
    W, H = 740, 250

    def scene(theta_px, m, note):
        sc = Scene(W, H)
        sc.label(40, 30, f"单缝衍射：半波带法，暗纹条件 a·sinθ = mλ（图中m={m}）", size=15, fill=SUB)
        sc.add("rect", x=90, y=100, width=14, height=50, rx=2, fill=INK)
        sc.add("line", x1=106, y1=125, x2=430, y2=125 + theta_px, stroke=WRITE_STROKE, stroke_width=1.8)
        sc.add("line", x1=430, y1=125 + theta_px, x2=470, y2=125 + theta_px, stroke=HOT_STROKE, stroke_width=2.5)
        for i in range(1, m + 1):
            yy = 125 + theta_px * i // (m + 1) if m else 125
            sc.add("line", x1=106, y1=125, x2=300, y2=125, stroke=LINE, stroke_width=1) if False else None
        sc.add("line", x1=470, y1=60, x2=470, y2=200, stroke=CELL_STROKE, stroke_width=3)
        sc.label(476, 130 + theta_px, f"m={m}暗纹" if m else "中央明纹", size=14, mono=True, fill=(BAD_STROKE if m else HOT_STROKE))
        sc.label(96, 168, "缝宽a", size=12, fill=SUB)
        sc.label(40, 226, note, size=15)
        return sc

    frames.append(frame("中央明纹 m=0", "θ=0方向：缝内所有半波带的光程差为零，全部同相叠加，中央最亮最宽。", "宽度约2λ/a的亮带。",
                        "", scene(0, 0, "中央：全同相。")))
    frames.append(frame("一级暗纹 m=1", "偏转使缝顶与缝底光程差恰为λ：缝分成2个半波带，逐带相消——该方向全暗。", "a·sinθ=λ定出第一暗纹偏角。",
                        "", scene(46, 1, "半波带两两相消。")))
    frames.append(frame("二级暗纹 m=2", "光程差2λ：3个半波带?不——分成4个半波带，两两相消，再次全暗。", "m越大偏角越大；缝越窄（a小）衍射越显著。",
                        "", scene(88, 2, "暗纹间距Δ=sinθ₂−sinθ₁=λ/a。")))
    return write_demo("ph16-diffraction", "单缝衍射：半波带定暗纹", frames, outdir=PH_IMG)


DEMOS.update({
    "cs05-cc": demo_cc,
    "cs12-malloc": demo_malloc,
    "ph08-rc": demo_ph_capacitor,
    "ph16-diffraction": demo_ph_diffraction,
})



# ---------- CS批4 + 物理批3 ----------

def demo_cs_signal():
    """信号到达打断控制流；不可重入的信号安全。"""
    frames = []
    W, H = 740, 220

    def scene(sig_at, note):
        sc = Scene(W, H)
        sc.label(40, 30, "信号：异步事件打断控制流，执行handler后回到断点", size=15, fill=SUB)
        sc.add("line", x1=60, y1=120, x2=660, y2=120, stroke=INK, stroke_width=2.5)
        sc.label(48, 142, "main()顺序执行", size=13, fill=SUB)
        if sig_at is not None:
            sc.add("circle", cx=sig_at, cy=120, r=7, fill=HOT_STROKE)
            sc.label(sig_at - 14, 96, "SIGINT到达", size=13, fill=HOT_STROKE)
            sc.add("line", x1=sig_at, y1=127, x2=sig_at, y2=160, stroke=HOT_STROKE, stroke_width=1.8)
            sc.add("line", x1=sig_at, y1=160, x2=sig_at + 90, y2=160, stroke=HOT_STROKE, stroke_width=1.8)
            sc.label(sig_at + 18, 180, "handler()执行", size=13, fill=HOT_STROKE)
            sc.add("line", x1=sig_at + 90, y1=160, x2=sig_at + 90, y2=127, stroke=HOT_STROKE, stroke_width=1.8)
        sc.label(40, 206, note, size=15)
        return sc

    frames.append(frame("正常顺序流", "程序按指令顺序推进。", "信号是异步的：任意两条指令之间都可能到达。", "",
                        scene(None, "尚无信号。")))
    frames.append(frame("SIGINT到达：跳handler", "内核在断点保存现场，转去执行信号处理函数。", "处理函数与主流程并发访问同一数据——时序竞态由此而来。",
                        "", scene(400, "处理函数执行中。")))
    frames.append(frame("返回断点", "handler结束，回到断点继续，如同无事发生。", "不可重入的函数（如malloc）不能在handler里安全调用。",
                        "", scene(400, "回到断点。")))
    return write_demo("cs10-signal", "信号：断点、handler与返回", frames, outdir=CS_IMG)


def demo_cs_io_redirect():
    """shell重定向 ls > out.txt：stdout指向文件。"""
    frames = []
    W, H = 740, 220

    def scene(mode, note):
        sc = Scene(W, H)
        sc.label(40, 30, "重定向：同一程序，stdout指向终端还是文件由fd表决定", size=15, fill=SUB)
        sc.add("rect", x=60, y=90, width=150, height=56, rx=10, fill=CELL, stroke=CELL_STROKE, stroke_width=1.5)
        sc.label(135, 118, "ls 进程", size=16, mono=True, anchor="middle")
        sc.add("rect", x=60, y=152, width=150, height=40, rx=8, fill=PALE, stroke=LINE, stroke_width=1.2)
        sc.label(135, 177, "fd 1 = stdout", size=13, mono=True, anchor="middle")
        if mode == "tty":
            sc.add("line", x1=210, y1=172, x2=430, y2=110, stroke=WRITE_STROKE, stroke_width=2)
            sc.add("rect", x=432, y=84, width=200, height=52, rx=10, fill=CELL, stroke=CELL_STROKE, stroke_width=1.5)
            sc.label(532, 116, "终端", size=16, mono=True, anchor="middle")
        else:
            sc.add("line", x1=210, y1=172, x2=430, y2=110, stroke=WRITE_STROKE, stroke_width=2)
            sc.add("rect", x=432, y=84, width=200, height=52, rx=10, fill=WRITE, stroke=WRITE_STROKE, stroke_width=1.5)
            sc.label(532, 108, "out.txt", size=15, mono=True, anchor="middle")
            sc.label(532, 126, "（文件）", size=12, fill=FAINT, anchor="middle")
        sc.label(40, 208, note, size=15)
        return sc

    frames.append(frame("默认：stdout接终端", "进程启动时fd 0/1/2默认指向终端。", "printf写fd 1，屏幕上看得见。",
                        "", scene("tty", "输出上屏。")))
    frames.append(frame("shell执行 ls > out.txt", "fork后、exec前，子进程把fd 1重新open到out.txt。", "ls本身不关心fd 1指向什么——重定向对程序透明。",
                        "", scene("file", "输出进文件。")))
    return write_demo("cs13-redirect", "重定向：fd 1指终端还是文件", frames, outdir=CS_IMG)


def demo_ph_potential():
    """等势面与电场线处处垂直；沿等势面移动不做功。"""
    frames = []
    W, H = 720, 240
    CX, CY = 220, 130

    def scene(r, note):
        sc = Scene(W, H)
        sc.label(40, 30, "点电荷的等势面是同心球面；电场线沿半径，与等势面处处垂直", size=15, fill=SUB)
        for rr in (46, 84, 122):
            sc.add("circle", cx=CX, cy=CY, r=rr, fill="none", stroke=WRITE_STROKE, stroke_width=1.6)
            sc.label(CX + rr * 0.72, CY - rr * 0.72, f"{rr}V", size=12, mono=True, fill=WRITE_STROKE) if rr == 46 else None
        for ang in (0, 60, 120, 180, 240, 300):
            rad = ang * 3.14159 / 180
            sc.add("line", x1=CX + 12 * math.cos(rad), y1=CY + 12 * math.sin(rad),
                   x2=CX + 130 * math.cos(rad), y2=CY + 130 * math.sin(rad),
                   stroke=HOT_STROKE, stroke_width=1.4)
        sc.add("circle", cx=CX, cy=CY, r=4, fill=HOT_STROKE)
        # charge moving along equipotential
        sc.add("circle", cx=CX + 84, cy=CY - 84, r=5, fill=BAD_STROKE)
        sc.add("circle", cx=CX + 84 + 24, cy=CY - 84 - 10, r=5, fill=BAD_STROKE)
        sc.label(CX + 100, CY - 100, "沿等势面移动：W=0", size=13, fill=BAD_STROKE)
        sc.label(40, 216, note, size=15)
        return sc

    frames.append(frame("场线与等势面垂直", "电场线沿半径向外；等势面是同心球面，两者处处正交。", "若不垂直，场强就有沿等势面的分量，电荷会自发移动——矛盾。",
                        "", scene(84, "三圈等势线：内高外低。")))
    frames.append(frame("沿等势面移动不做功", "W = qU = q(V₁−V₂) = 0：电势差为零。", "做功只看起止电势差，与路径无关——静电场是保守场。",
                        "", scene(84, "试探电荷沿等势面滑动：W=0。")))
    return write_demo("ph04-potential", "等势面：电场线处处垂直于它", frames, outdir=PH_IMG)


def demo_ph_amperian():
    """安培环路定理：载流直导线 B∝1/r，环路积分=μ0 I。"""
    frames = []
    W, H = 720, 240
    CX, CY = 200, 130

    def scene(r, note):
        sc = Scene(W, H)
        sc.label(40, 30, "安培环路定理：∮B·dl = μ₀·I(环路包围的电流)", size=15, fill=SUB)
        sc.add("circle", cx=CX, cy=CY, r=5, fill=HOT_STROKE)
        sc.label(CX + 12, CY - 8, "I（流出纸面）", size=13, fill=SUB)
        for rr in (50, 100):
            sc.add("circle", cx=CX, cy=CY, r=rr, fill="none", stroke=(WRITE_STROKE if rr == r else CELL_STROKE), stroke_width=(2 if rr == r else 1.4))
            sc.label(CX + rr * 0.7, CY - rr * 0.7, f"B = μ₀I/2πr" if rr == r else "", size=13, mono=True, fill=WRITE_STROKE)
        # direction arrows on chosen loop
        for ang in (30, 150, 270):
            rad = ang * 3.14159 / 180
            x = CX + r * math.cos(rad); y = CY + r * math.sin(rad)
            sc.add("circle", cx=x, cy=y, r=3, fill=WRITE_STROKE)
        sc.label(420, 110, "对称性：B沿圆周切向", size=15, mono=True)
        sc.label(420, 138, "大小处处相等 ⇒ ∮B·dl = B·2πr", size=15, mono=True)
        sc.label(420, 166, "⇒ B = μ₀I/2πr", size=15, mono=True, fill=INK)
        sc.label(40, 216, note, size=15)
        return sc

    frames.append(frame("对称性先行", "无限长直导线的磁场绕电流成同心圆，方向由右手定则给出。", "先定方向，再谈大小——安培环路的用法。",
                        "", scene(100, "磁感应线是同心圆。")))
    frames.append(frame("取圆形环路", "B沿切向且大小处处相等：环路积分化为B×2πr。", "∮B·dl = μ₀I 解出 B = μ₀I/2πr。",
                        "", scene(100, "环路包围电流I。")))
    frames.append(frame("与半径的关系", "r加倍则B减半；环路不包围电流时积分为零。", "与静电高斯定理对偶：通量/环流只看包围的源。",
                        "", scene(100, "B∝1/r。")))
    return write_demo("ph10-amperian", "安培环路：B·2πr=μ₀I", frames, outdir=PH_IMG)


DEMOS.update({
    "cs10-signal": demo_cs_signal,
    "cs13-redirect": demo_cs_io_redirect,
    "ph04-potential": demo_ph_potential,
    "ph10-amperian": demo_ph_amperian,
})

if __name__ == "__main__":
    main(sys.argv[1:])
