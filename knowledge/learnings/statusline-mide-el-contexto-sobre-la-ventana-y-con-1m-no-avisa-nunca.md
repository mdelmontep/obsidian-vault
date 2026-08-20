---
title: la statusline mide el contexto sobre la ventana del modelo, y con 1M no avisa nunca
date: 2026-08-20
source: claude-harness
tags: [claude-code, statusline, contexto, opus5]
---

`context_window.used_percentage` del input del `statusLine` se calcula sobre `context_window_size`, que en Opus 5 es **1.000.000**. Con **200k reales** en contexto marca **20 %, en verde** — justo cuando ya toca cortar. Los umbrales de aviso escritos como % (90/75/50) caen entonces en 900k/750k/500k: no avisan de nada.

Ése era el mecanismo por el que las sesiones llegaban a 900k sin que la barra dijera nada. `exceeds_200k_tokens` sí existe en el input, pero pintado en gris atenuado es invisible.

Fix: pintar la barra sobre un **presupuesto operativo** (200k por defecto, env para cambiarlo), con la **cifra absoluta** (`148k/200k · 74 %`) y **sin capar el % a 100** — a 400k hay que poder leer 200 %. Al cruzarlo, vídeo inverso rojo. La fórmula del total es input-only: `input + cache_creation + cache_read` (no incluye output).

Complemento determinista: `autoCompactWindow` en `settings.json` (o `/autocompact 300k`). Sin él, Opus 5 compacta al llegar al límite del modelo, o sea a 1M.

Lección general: **un indicador que mide sobre el límite físico no avisa de nada cuando el límite útil es económico.** El umbral que importa es el que te cuesta dinero, no el que rompe la API.

Ver [[donde-se-va-el-coste-de-claude-code-no-es-el-claude-md]]
