---
title: migrar input nativo a componente con overlay — borrar reglas css del nativo (especificidad)
date: 2026-06-25
source: claude-code-session
tags: [css, design-system, frontend, facturaia]
---

Al sustituir un `<input type=checkbox/radio>` nativo por un componente con
**overlay transparente** (`input{position:absolute;inset:0;width:100%;opacity:0;z-index:2}`
sobre una casilla estilizada), hay que **eliminar las reglas CSS viejas del nativo**.

Por qué: un selector como `.wrapper input[type=checkbox]{width:16px}` tiene
especificidad **(0,2,1)** y GANA al `.input{width:100%}` del componente **(0,1,0)**.
Resultado: el overlay se encoge a 16px y deja **bordes muertos** sin clic. El `accent-color`
ya era invisible (input opacity 0), pero el `width/height` sí rompe la interacción.

Fix: borrar `.wrapper input[type=checkbox]{...}` al migrar. NO tocar las de
`input[type=radio]` ni las del switch/Toggle.

Corolario: el wrapper del componente debe ser `<span>`, **no `<label>`** — así puede
anidarse dentro de un `<label>` externo sin HTML inválido ni doble toggle.

Caso real FacturaIA: tick "Burst" como componente único (`src/components/ui/checkbox.tsx`),
34 checkboxes migrados; reglas muertas en `.fact-table`/`.gen-send-toggle-row`/
`.series-modal-checkbox`/`.adm-checkbox`/`.toggleArchivadas`.
