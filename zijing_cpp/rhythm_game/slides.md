---
marp: true
theme: default
paginate: true
style: |
  section { font-size: 24px; }
  h1 { color: #e0847a; font-size: 36px; }
  h2 { color: #b0604a; font-size: 28px; }
  h3 { color: #c07060; font-size: 26px; }
  code { font-size: 18px; }
  table { font-size: 18px; }
  .columns { display: flex; gap: 40px; }
  .columns > div { flex: 1; }
  .en { color: #888; font-size: 20px; margin-top: 2px; }
---

# aeacrA

基于 raylib 下落式节奏游戏
A falling rhythm game built with raylib

---

# 项目概览 / Project Overview

**游戏类型**：6 轨下落式节奏游戏（类 Arcaea）
**Game Type**: 6-lane falling rhythm game (Arcaea-style)

**渲染引擎**：raylib 5.5
**Rendering Engine**: raylib 5.5

**开发环境**：macOS + Clang++ 17 + VS Code + Makefile
**Development Environment**: macOS + Clang++ 17 + VS Code + Makefile

**代码规模**：14 个头文件，11 个源文件
**Code Scale**: 14 headers, 11 source files

**外部依赖**：raylib、aubio（音频特征分析）
**Dependencies**: raylib, aubio (audio feature analysis)

---

# 项目结构 / Project Structure

```
aeacrA/
├── include/              # 头文件
│   ├── Config.h          # 全局常量
│   ├── Chart.h           # 谱面
│   ├── ChartGenerator.h  # 谱面生成
│   ├── JsonParser.h      # JSON 解析
│   ├── Judge.h           # 判定
│   ├── InputManager.h    # 输入管理器
│   ├── AudioManager.h    # 音频播放
│   ├── ParticleSystem.h  # 粒子特效
│   ├── Renderer.h        # 透视渲染器
│   ├── SongManager.h     # 歌曲库管理
│   ├── SongEntry.h       # 歌曲数据条目
│   ├── FilePicker.h      # 文件选择器接口
│   └── Game.h            # 游戏
├── src/                  # 实现
├── charts/               # 手写谱面
└── songs/                # 导入歌曲
```

---

# 架构 / Architecture

- `Chart` — 谱面数据 / Chart data (Note list, JSON serialization)
- `JudgeSystem` — 判定 / Judgment (PERFECT / GREAT / GOOD / MISS)
- `Renderer` — 渲染 / Rendering (perspective, HUD, menus)
- `AudioManager` — 音乐流播放 / Music stream playback & beat pulse
- `InputManager` — 按键事件 / Key press/release events
- `ParticleSystem` — 粒子特效 / Particle effects (explosion/spiral/fire)
- `SongManager` — 歌曲管理 / Song scanning, import, chart generation
- `FilePicker` — 文件选择器 / Native file picker (Obj-C++ bridge)

弱耦合：Renderer 不依赖 Judge，InputManager 不依赖 Chart
Loosely coupled: Renderer has no dependency on Judge, InputManager none on Chart

---

# 状态机 / State Machine

```
        ┌──────────┐
        │   MENU   │◀──────────────────────┐
        └────┬─────┘                       │
        Enter│                     ESC/完成  │
        ┌────▼─────┐              ┌────────┴───┐
        │  SELECT  │──── Enter ──▶│  PLAYING   │
        └────┬─────┘              └──────┬─────┘
        I键  │                       完成  │
        ┌────▼──────┐            ┌───────▼───┐
        │ IMPORTING │            │  RESULT   │
        └───────────┘            └───────────┘
```

5 个状态枚举，由用户输入驱动转换
5-state enum driven by user input transitions

`autoplay_` 标志在 PLAYING 内切换手动/自动，无需额外状态
`autoplay_` flag toggles manual/auto within PLAYING — no extra state needed

---

# 创新点 ① 多级判定 / Multi-tier Judgment

| 判定 | 时间窗口 | 得分 |
|------|---------|------|
| PERFECT | ≤ 45ms | 350 |
| GREAT | ≤ 90ms | 200 |
| GOOD | ≤ 140ms | 100 |
| MISS | > 140ms | 0（断 Combo） |

四级时间窗口判定：越精准得分越高
Four-tier timing window: the more precise, the higher the score

超时未按自动 MISS；空按（无对应音符）也触发 MISS
Expired notes auto-MISS; empty presses (no matching note) also trigger MISS

---

# 创新点 ① Hold 双段判定 / Hold Dual Judgment

```
按下 ────── 持续按住 ────── 松开
 │                           │
 ├─ 头部判定 (head judge) ───┤─ 尾部判定 (tail judge)
```

头部：按键时刻 vs 音符到达时刻 → 四级判定
Head: press time vs note arrival → four-tier judgment

尾部：松开时刻 vs Hold 结束时刻 → 独立二次判定，两次得分
Tail: release time vs hold end → independent second judgment, scored twice

早松超出窗口直接 MISS，保证长按的挑战性
Early release beyond window triggers MISS, ensuring hold note challenge

---

# 创新点 ② Obj-C++ 文件选择器 / Obj-C++ File Picker

```cpp
// FilePicker.h — C++ 接口 / C++ interface
std::string openAudioFileDialog();

// FilePicker.mm — Objective-C++ 实现 / Obj-C++ impl
#ifdef __APPLE__
  #include <AppKit/AppKit.h>
  std::string openAudioFileDialog() {
      @autoreleasepool {
          NSOpenPanel* panel = [NSOpenPanel openPanel];
          [panel setAllowedFileTypes:
              @[@"mp3",@"wav",@"ogg",@"flac"]];
          if ([panel runModal] == NSModalResponseOK)
              return std::string(
                  [[[panel URLs] objectAtIndex:0]
                      fileSystemRepresentation]);
          return "";
      }
  }
#endif
```

---

# 创新点 ③ 自动谱面生成 / Auto Chart Generation

基于 aubio 的分析
Three-stage analysis pipeline based on aubio

```
音频文件 ──▶ ① BPM 检测 ──▶ ② Onset 检测 ──▶ ③ FFT 频谱
 (mp3)     (beat tracking)  (打击点时间)     (频率特征)
                                                │
                                                ▼
                                   Bass  → 左轨道 (lane 0,1)
                                   Mid   → 中轨道 (lane 2,3)
                                   High  → 右轨道 (lane 4,5)
                                   低能量 → Hold 长按音符
```

BPM 检测：aubio tempo → 中位数拍间距 → 换算 BPM
BPM detection: aubio tempo → median beat interval → convert to BPM
Onset 检测：打击点时间戳 + 80ms 最小间隔
Onset detection: onset timestamps + 80ms minimum gap
FFT 频谱：spectral centroid + bass ratio → 轨道分配
FFT spectrum: spectral centroid + bass ratio → lane assignment

---

# 创新点 ③ Onset 检测 / Onset Detection

每 512 个采样点为一帧，逐帧读取音频
Read audio in frames of 512 samples each

```
帧能量突然增大？ ──→ 记录该时间点为 onset（打击点）
Energy spike?       → Record this timestamp as an onset
```

过滤：相邻 onset 间隔 < 80ms 则丢弃（防止重复检测）
Filter: discard onsets closer than 80ms to avoid duplicates

效果：跑完整首歌得到打击点时间列表，即音符出现的时间
Result: a list of timestamps where notes should appear

---

# 创新点 ③ FFT 频谱分析 / FFT Spectrum Analysis

在每个 onset 时刻，对 512 采样点做 FFT 变换
At each onset, perform FFT on 512 samples

得到 256 个频率 bin，从中提取两个指标：
Get 256 frequency bins, extract two metrics:

**bassRatio** = 前 32 bin 强度 / 总强度 → 低音占比
**bassRatio** = first 32 bins energy / total energy → bass ratio

**centroid** = 加权重心位置 → 频谱质心，越高高频越多
**centroid** = weighted center → spectral centroid, higher = more high-freq

---

# 创新点 ③ 轨道分配 / Lane Assignment

bassRatio 大 → 低音 → 左轨道 (lane 0,1)
High bassRatio → bass → left lane (0,1)

centroid 大 → 高音 → 右轨道 (lane 4,5)
High centroid → treble → right lane (4,5)

都不突出 → 中频 → 中轨道 (lane 2,3)
Neither dominant → mid → center lane (2,3)

效果：低沉鼓点按左手，明亮高音按右手，模拟真实演奏
Low drums → left hand, bright highs → right hand, like real performance

---

# 创新点 ③ 段落变化策略 / Section Variation

每 8 拍切换轨道分配模式，避免单调
Switch lane assignment mode every 8 beats to avoid monotony

| 模式 | 行为 / Behavior |
|------|----------------|
| 0 | 纯频谱映射：低→左，高→右 / Pure spectrum mapping |
| 1 | 频谱 ± 随机偏移 / Spectrum ± random offset |
| 2 | 等差递增 / Arithmetic progression |
| 3 | 频谱 ± 大幅偏移 / Spectrum ± wide offset |
| 4 | 镜像：`5 - lane` / Mirror |

---

# 渲染系统 / Rendering System

2D 模拟 3D 透视效果
2D simulating 3D perspective effect

```
        ╲   ╱  ← 消失点 (VP_X, VP_Y)
         ╲ ╱
          V
         ╱ ╲
        ╱   ╲
       ╱     ╲  ← 判定线 (HIT_Y)
```

---

# 粒子特效 / Particle Effects

常驻背景花瓣：50 个半透明圆缓慢上浮，左右正弦摆动
Background petals: 50 translucent circles float upward with sinusoidal drift

**爆炸 (Explosion)**：PERFECT 时 25 个粒子向四周扩散
**Explosion**: 25 particles burst outward on PERFECT hit
白色 + 轨道色混合，部分带 sparkle 闪光
White + lane color mix, some with sparkle effect

---

# 粒子特效（续） / Particle Effects (cont.)

**螺旋 (Spiral)**：PERFECT 时 8 个粒子螺旋飞出
**Spiral**: 8 particles fly out in spiral on PERFECT hit
角度随时间旋转，使用相邻轨道配色
Angles rotate with time, using adjacent lane colors

**火焰 (Fire)**：Combo > 10 时在判定线向上喷射
**Fire**: Upward spray above hit line when combo > 10
窄角度向上的大粒子，营造连续击打的成就感
Narrow-angle large particles, creating a satisfying streak feel

---

# JSON 解析器 / JSON Parser


```cpp
struct JsonValue {
    JsonType type;   // Null/Bool/Number/String/Array/Object
    double num;  string str;
    vector<JsonValue> arr;
    vector<pair<string, JsonValue>> obj;
    const JsonValue& operator[](const char* key) const;
    const JsonValue& operator[](size_t i) const;
};
```

链式访问：`root["notes"][0]["time"]`
Chain access: `root["notes"][0]["time"]`

---

# OOP Principles

**封装** / **Encapsulation**
每个类隐藏内部实现，仅暴露必要接口
Each class hides internals, exposes only necessary interfaces
`JudgeSystem` 内部维护 score/combo，外部只调用 `judge()` / `apply()`
JudgeSystem internally maintains score/combo; externally only calls judge() / apply()

**单一职责** / **Single Responsibility**
InputManager 只管输入，AudioManager 只管音频，Renderer 只管渲染
InputManager handles input only, AudioManager handles audio only

**组合** / **Composition**
Game 通过组合持有子系统，无继承层级
Game composes subsystems, no inheritance hierarchy

---

# 设计模式 / Design Patterns

**适配器 (Adapter)**：FilePicker.mm 把 NSOpenPanel 的 Obj-C 接口转成 C++ 函数
**Adapter**: FilePicker.mm wraps NSOpenPanel Obj-C interface into a C++ function
对象适配器：内部组合 NSOpenPanel，对外暴露 `openAudioFileDialog()`
Object adapter: composes NSOpenPanel internally, exposes openAudioFileDialog()

**策略 (Strategy)**：`autoplay_` 标志切换手动/自动两种游玩行为
**Strategy**: autoplay_ flag switches between manual and auto play behavior

**迭代器 (Iterator)**：大量使用 STL 迭代器遍历音符、粒子、歌曲列表
**Iterator**: STL iterators used throughout for notes, particles, song lists

---

# C++ 基础 / C++ Basics

Makefile 构建
Makefile build

多文件项目：`.h` / `.cpp` 分离，`#pragma once` 头文件守卫
Multi-file project: `.h` / `.cpp` separation, `#pragma once` header guards

STL 容器：`vector`（音符/粒子列表）、`array<int,4>`（判定计数）
STL containers: `vector` for notes/particles, `array<int,4>` for judgment counts

文件 I/O：`std::ifstream` / `std::stringstream`
File I/O: `std::ifstream` / `std::stringstream`

---

# C++ 特性 / C++ Features

枚举类：`enum class JudgeResult : uint8_t` — 类型安全
Enum class: type-safe, prevents implicit conversions

结构化：`for (auto& [k, v] : obj)` 遍历 JsonValue 对象
Structure for JsonValue object traversal

Obj-C++ ：`.mm` 文件
Obj-C++: `.mm` files bridge C++ and macOS

---

# 总结 / Summary


核心创新 / Core Innovations：
多级下落判定系统、Obj-C++ 原生文件选择器、音频分析自动谱面生成
Multi-tier judgment, native Obj-C++ file picker, audio-driven auto chart generation


---

# 谢谢！Q & A

**aeacrA**

> 按键 / Keys: `S D F J K L` | 选歌界面按 `A` 自动演示 / Press `A` for auto-demo
