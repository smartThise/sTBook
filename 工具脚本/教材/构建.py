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
    ap.add_argument("--public-only", action="store_true", help="只构建公开版，保留含课内作业的本地完整版本")
    args = ap.parse_args()
    entries = {entry["course"]: entry for entry in json.loads((ROOT / "教材清单.json").read_text())["books"]}
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
        entry = entries[course]
        private = set(entry.get("private_chapters", []))
        public_chapters = [chapter for chapter in chapters if chapter.name not in private]
        assert set(entry["chapters"]) == {chapter.name for chapter in public_chapters}, "教材清单与公开章节不一致"
        for src in public_chapters if args.public_only else chapters:
            target = src.with_suffix(".typ")
            subprocess.run(["pandoc", str(src.name), "--from=markdown+tex_math_dollars", "--to=typst", "--wrap=none", "--fail-if-warnings", "--output", target.name], cwd=folder, check=True)
            # Pandoc 的图片相对路径与 Markdown 位置一致；Math 使用原生 Typst 数学。
        def write_main(selected, target):
            main_typ = '#import "../../../module/教材.typ": textbook\n'
            main_typ += f'#show: textbook.with(title: [{course}], subtitle: [概念 · 推导 · 原图 · 例题 · 自测])\n\n'
            for chapter in selected:
                number = int(chapter.name[:2])
                include = f'include "{chapter.with_suffix(".typ").name}"'
                if number in (0, 95, 96):
                    main_typ += '#{ set heading(numbering: none); ' + include + ' }\n'
                else:
                    main_typ += f'#counter(heading).update({number - 1})\n#{include}\n'
            (folder / target).write_text(main_typ, encoding="utf-8")

        def compile_pdf(source, target):
            if not args.no_pdf:
                subprocess.run(["typst", "compile", "--root", str(ROOT), *font_args, source, target], cwd=folder, check=True)

        if not args.public_only:
            write_main(chapters, "main.typ")
            compile_pdf("main.typ", f"{course}·超级纲要.pdf")
        if private:
            write_main(public_chapters, entry["typst"])
            compile_pdf(entry["typst"], entry["pdf"])
        elif args.public_only:
            write_main(chapters, "main.typ")
            compile_pdf("main.typ", f"{course}·超级纲要.pdf")
        report.append({"course": course, "chapters": len(chapters), "characters": sum(len(p.read_text()) for p in chapters), "folder": str(folder.relative_to(ROOT))})
    output = ROOT / "outputs/three-course-books"
    output.mkdir(parents=True, exist_ok=True)
    (output / "build.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
