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


if __name__ == "__main__":
    main(sys.argv[1:])
