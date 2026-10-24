# sTBook

我的课程笔记库，同时作为 [个人网站](https://guojl06.github.io) 笔记/知识库模块的数据源（wiki 风格，可在线浏览 md / typst / pdf / 图片 / 数据文件）。

## 结构

- 课程文件夹：直接使用中文课程名，如 `数据结构/`、`面向对象程序设计/`、`离散数学（二）/`、`大学物理/`、`小学期AI4S/`。
- [`wiki.yml`](wiki.yml) 记录目录、分组与简介；目录名、网站路径和展示名一致，无需英文名称映射。
- `Assets/`、`module/`：共享图片与 Typst 工具模块，笔记内以相对路径引用，**勿改名**
- `模板/`：简历等模板；`工具脚本/`：OJ→Markdown 等脚本；`杂项/`：个人杂项

## 网站同步

把笔记 push 到本仓库后，网站仓库的 GitHub Action 会自动拉取本仓库并重建
[guojl06.github.io/notes](https://guojl06.github.io/notes/)，无需手动同步。
