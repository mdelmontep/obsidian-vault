---
title: table-layout fixed con columnas extra comprime la última columna fija
date: 2026-04-21
source: claude-code-session
tags: [css, tablas, facturaia]
---

En tablas con `table-layout: fixed`, añadir una columna condicional (ej: "Origen" solo en recibidas) sin ajustar los porcentajes de las demás columnas comprime la última columna con ancho fijo en `px` (típicamente la de acciones/3-dot menu).

**Síntoma**: el botón de acciones aparece en distinta posición horizontal entre tablas con y sin la columna extra.

**Fix**: usar clase condicional en el `<table>` (ej: `.has-origen`) con porcentajes reducidos que sumen exactamente lo mismo que la tabla base. Así la columna de acciones (px fijo) empieza en la misma posición en ambas variantes.

```css
/* Base: 91% + 76px fijos */
.fact-table .col-num { width: 13%; }
.fact-table .col-name { width: 22%; }

/* Con columna extra: también 91% + 76px */
.fact-table.has-origen .col-num { width: 12%; }
.fact-table.has-origen .col-name { width: 19%; }
.fact-table.has-origen .col-origen { width: 7%; }
```

Regla general: al añadir columnas condicionales, la suma de porcentajes debe ser idéntica en ambas variantes para mantener consistencia visual.
