#!/usr/bin/env python3
"""演示图生成器：为教材逐步演示生成统一的SVG序列与trace。

用法：python3 演示图.py [demo_id ...]（无参数生成全部）
输出：数据结构/资料/超级纲要/图片/演示-<id>-NN.svg；首个SVG内嵌 notes-demos.js 的trace JSON。
"""
import json
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


def write_demo(demo_id, title, frames):
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
        (IMG / f"演示-{demo_id}-{i:02d}.svg").write_text(svg, encoding="utf-8")
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

if __name__ == "__main__":
    main(sys.argv[1:])
