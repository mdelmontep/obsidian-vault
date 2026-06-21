---
title: aceptar una sugerencia HITL debe cerrar la decisión o el gate de acierto nunca abre
date: 2026-06-21
source: claude-code-session
tags: [agentic, hitl, gating, metrics]
---

Patrón gate shadow→activo: mides `auto_accuracy` comparando lo que la IA habría hecho
(zona verde) con lo que decide el humano.

Bug latente: si **aceptar la sugerencia** (botón confirmar / bulk-confirm) NO cierra la
decisión de medición ni alimenta el aprendizaje, y el único cierre (cambiar el valor) se
etiqueta SIEMPRE como "corrección", el acierto medido ≈0% → el gate nunca llega a ≥95%
→ "activo" inalcanzable en la práctica. La feature parece completa pero es un dead-end.

Fix: (1) la aceptación cierra la decisión con fuente **derivada por comparación**
(igual al valor IA → aceptación; distinto → corrección); (2) la métrica de "corregida"
compara el valor, no la etiqueta. Verde per-issue; lo destapa la **composición**.
