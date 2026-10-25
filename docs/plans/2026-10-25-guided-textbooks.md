# Guided textbook revision

> **For Codex:** execute the steps in this session and use the already authorized course agents for separate chapter ownership and independent review.

**Goal:** Make each explanation reproducible by a reader who has not previously learned the algorithm or notation. Start with data structures, then apply the same standard to computer systems and physics.

**Architecture:** Canonical Chinese Markdown remains the source for Wiki and Typst. Each worked algorithm shows its actual input, every relevant state transition, a reason for that transition, and the stopping/result interpretation. Static diagrams are complete in PDF. Trusted site code can progressively enhance an explicitly marked repository SVG into a step player. Scripts embedded in Markdown remain prohibited. Failure to load an interactive enhancement leaves the complete static explanation readable.

**Tech Stack:** Markdown, Pandoc, Typst, Python SVG generation; existing notes frontend with plain JavaScript, SVG, CSS, Playwright.

## Tasks

1. Re-read teach, wait-what, Humanizer and actual course sources; consult primary textbook explanations, with source links in the source appendix. Record vocabulary and notation consistently.
2. Rewrite DS 01–10, 11–20, 21–33 in three separately owned agent tasks. Review every introduced procedure and formula, rather than satisfying a length or illustration quota.
3. Add a shared SVG trace format and player: previous/next, play/pause, draggable timeline, keyboard operation, speed, prediction reveal; preserve static diagrams and reduced-motion preference. Each frame includes an action and its reason. No automatic motion on page load.
4. Integrate selected genuinely useful examples into the corresponding chapter. Include all intermediate states in static editions. Keep original teacher slide pages intact where their full diagram is needed.
5. Use unfamiliar-input and visual cross-review to find omitted transitions, undefined symbols, false invariants and ambiguous color/edge conventions. Correct them and review again.
6. Revisit systems and physics with the same standard: actual memory/register/process states and numerical/vector/field derivations with diagrams. The DS work takes priority.
7. Rebuild Typst and PDF, inspect changed pages at readable scale, verify Wiki math/images/interactive behavior and private-file boundaries. Commit, publish, then compare live content and inspect the actual live page.

## Acceptance

The reader can reproduce an example from the initial state without guessing an omitted operation or looking up an unexplained symbol. Drawn states, executable trace and prose agree. The explanation tells the reader why an operation is valid and how it leads to the result; formulas define variables and justify transformations. Page count, word count and animation count are not acceptance criteria.
