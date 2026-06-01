---
title: TuFacturaIA — tokens CSS --panel/--border/--text usados pero sin definir
date: 2026-06-01
source: claude-code-session
tags: [facturaia, frontend, css, design-tokens, gotcha]
---

# `--panel` / `--border` / `--text`: usados en 20+ componentes admin, nunca definidos

Síntoma: el modal de `/admin/ia-ops` "casi no se veía" (contenedor transparente sobre el backdrop). Al squint, todo el admin (ia-ops, config, conciliación) se veía plano.

Causa: los componentes usan `var(--panel)` (45 usos), `var(--border)` (75) y `var(--text)` (41) pero **ninguno estaba definido** en `src/app/globals.css`. CSS resuelve un custom property indefinido a *nada* → `background: var(--panel)` se ignora (fondo transparente), `border: 1px solid var(--border)` inválido (sin borde), `color: var(--text)` cae a herencia (OK en light por casualidad, **roto en dark**). El theme define `--bg-elev`, `--line`, `--fg` — los componentes esperaban alias que nadie creó (copiados de otro design system).

Fix (origen único): definir en AMBOS bloques de tema de `globals.css`:
```
--panel: var(--bg-elev);  --border: var(--line);  --text: var(--fg);
```
Arregla los 20+ componentes de golpe. Commit `bf96976`. Para modales, añadir además `box-shadow: var(--shadow-lg)` (elevación).

Regla: si un componente usa `var(--algo)` y no pinta, **grep la definición del token** antes de retocar estilos. Un token indefinido falla en silencio.
