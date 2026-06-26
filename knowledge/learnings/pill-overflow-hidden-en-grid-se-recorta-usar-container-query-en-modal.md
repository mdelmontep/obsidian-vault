---
title: Pill con overflow:hidden en grid rígido se recorta en modal estrecho — usar container query
date: 2026-06-26
source: PR #508 TuFacturaIA (modal detalle cliente/proveedor en móvil)
tags: [css, frontend, facturaia, modal, container-query, grid]
---

## Síntoma
En el modal de detalle (cliente/proveedor) el listado de documentos cortaba la
pill de estado en móvil: `Pendiente`→`Per`, `Borrador`→`Bor`.

## Causa
La fila era un grid de 4 columnas fijas (`6rem 1fr auto 6rem`). En el modal
estrecho no caben; como la pill (`.gota`) tiene `overflow:hidden` y su
`min-content` es ~0, la rejilla **sacrifica esa columna** y recorta el texto.
La fecha es un token sin punto de corte (min-content = ancho completo) → no
cede; las dos columnas `6rem` son fijas → tampoco. La pill es la única que cede.

## Fix
- `container-type: inline-size` en el contenedor del listado: la fila se adapta
  al ancho del **panel/modal**, no del viewport (el modal mide ~760px desktop /
  ~350px móvil → un `@media` de viewport no sirve).
- `@container (max-width:400px)` → fila a **dos líneas** con `grid-template-areas`
  (nº+importe arriba, fecha+estado abajo). La pill nunca se comprime.

## Regla
Dentro de modales/drawers/sidebars: responsive = **container query**, no media
query. El ancho relevante es el del contenedor, no el del viewport. Y una pill/
chip con `overflow:hidden` en un grid debe ir en una columna que no se comprima
(o el layout debe poder relajarse antes de comprimirla).
