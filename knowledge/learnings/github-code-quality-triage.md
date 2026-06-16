---
title: github code quality (preview) — sin api, triaje en ui; 4 reglas ≈ ruff
date: 2026-06-17
source: claude-code-session
tags: [github, code-quality, codeql, ruff, ci]
---
"Code Quality" (/security/quality, preview) ≠ "Code Scanning": toggle distinto, corre CodeQL
con queries de mantenibilidad/fiabilidad vía default setup (baseline en main + gate por PR `Code Quality: PR #NNN`).
GAP: NO expone alertas por REST (`code-scanning/alerts` da 403 "must be enabled") → triaje solo en UI.
Reproducción local sin la UI: las reglas mapean a ruff —
empty-except=S110, file-not-closed=SIM115, unused-import=F401, unused-var=F841,
inconvertible-types≈no-unsafe-enum-comparison, useless-conditional≈no-unnecessary-condition.
`python3 -m pip install --user ruff` (no venía); fix line-targeted con aserción de conteo (`--fix` solo F401/F841).
Triaje FacturaIA (PR #322): 23 Python = scripts desechables en n8n-patches (arreglados), 9 JS fiabilidad = 0 bugs reales.
Trampa: CodeQL marca inicializadores defensivos (`let status=400`) como "useless"; quitarlos en
código sensible es cargo-cult y puede romper definite-assignment. F541 lo caza ruff pero CodeQL no.
