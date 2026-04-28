---
title: skill chain ui impeccable polish audit critique guidelines baseline typeset
date: 2026-04-28
source: claude-code-session
tags: [claude-code, skills, frontend]
---

Cadena de skills para llevar un componente UI de "funciona" a "producción flagship". Aplicar en este orden:

1. **`/impeccable craft`** — diseño con design context (lee `.impeccable.md`), construye con jerarquía y aesthetic intencional.
2. **`/polish`** — alineación al spacing scale 4pt, tipografía consistente, transiciones a 60fps, micro-interacciones.
3. **`/audit`** — score 0-4 en a11y, perf, theming, responsive, anti-patterns. Output con P0-P3.
4. **`/critique`** — Nielsen heuristics 0-4, personas (Alex/Jordan + custom), AI slop test, peak-end rule.
5. **`/web-design-guidelines`** — fetch live de Vercel guidelines, compliance específico (`overscroll-behavior: contain`, `touch-action`, focus-visible…).
6. **`/baseline-ui`** — anti-slop estricto: nada de gradients, AlertDialog para destructivos, tabular-nums en datos.
7. **`/typeset`** — pareja de fuentes, hierarchy ratio 1.25, line-height por contexto, `text-balance`/`text-pretty`.

Cada skill añade ~10-15 fixes específicos. Las 6-7 juntas llevan un componente medio de 16/20 a 20/20. Para componentes pequeños, basta `/polish` + `/audit`. Para flagship, las 7.
