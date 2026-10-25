#!/usr/bin/env python3
"""三册教材：Markdown → Typst → PDF，同正文、可离线重建。"""
import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COURSES = ["计算机系统概论", "数据结构", "大学物理B(2)"]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--course", choices=COURSES, action="append")
    ap.add_argument("--no-pdf", action="store_true")
    args = ap.parse_args()
    report = []
    font_args = []
    if not args.no_pdf:
        fonts = subprocess.check_output(["typst", "fonts"], text=True).splitlines()
        for key, choices in [("cjk-serif", ["Songti SC", "Noto Serif CJK SC", "Noto Sans CJK SC"]), ("cjk-sans", ["PingFang SC", "Noto Sans CJK SC", "Noto Serif CJK SC"]), ("mono", ["Menlo", "DejaVu Sans Mono", "Liberation Mono"])]:
            match = next((f for f in choices if f in fonts), None)
            if not match:
                raise SystemExit(f"缺少字体：请安装 {choices}")
            font_args += ["--input", f"{key}={match}"]
    for course in args.course or COURSES:
        folder = ROOT / course / "资料" / "超级纲要"
        chapters = sorted(folder.glob("[0-9][0-9]-*.md"))
        if not chapters:
            raise SystemExit(f"没有正文：{course}")
        for src in chapters:
            target = src.with_suffix(".typ")
            subprocess.run(["pandoc", str(src.name), "--from=markdown+tex_math_dollars", "--to=typst", "--wrap=none", "--fail-if-warnings", "--output", target.name], cwd=folder, check=True)
            # Pandoc 的图片相对路径与 Markdown 位置一致；Math 使用原生 Typst 数学。
        main_typ = '#import "../../../module/教材.typ": textbook\n'
        main_typ += f'#show: textbook.with(title: [{course}], subtitle: [概念 · 推导 · 原图 · 例题 · 自测])\n\n'
        for chapter in chapters:
            number = int(chapter.name[:2])
            include = f'include "{chapter.with_suffix(".typ").name}"'
            if number in (0, 95, 96):
                main_typ += '#{ set heading(numbering: none); ' + include + ' }\n'
            else:
                # Keep printed chapter numbers equal to the canonical filenames
                # used by cross-references in both Wiki and PDF. The reader's
                # introduction and source appendix don't consume a chapter.
                main_typ += f'#counter(heading).update({number - 1})\n#{include}\n'
        (folder / "main.typ").write_text(main_typ, encoding="utf-8")
        if not args.no_pdf:
            subprocess.run(["typst", "compile", "--root", str(ROOT), *font_args, "main.typ", f"{course}·超级纲要.pdf"], cwd=folder, check=True)
        report.append({"course": course, "chapters": len(chapters), "characters": sum(len(p.read_text()) for p in chapters), "folder": str(folder.relative_to(ROOT))})
    output = ROOT / "outputs/three-course-books"
    output.mkdir(parents=True, exist_ok=True)
    (output / "build.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
