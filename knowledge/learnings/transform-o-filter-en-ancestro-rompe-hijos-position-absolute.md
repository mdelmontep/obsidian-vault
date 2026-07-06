---
title: transform/filter en un ancestro rompe hijos position:absolute (animación de entrada sobre un odómetro)
date: 2026-07-06
source: claude-code-session
tags: [css, animation, positioning, gotcha]
---
`transform`, `filter`, `perspective`, `will-change:transform` o `backdrop-filter` en un elemento lo convierten en el **bloque contenedor** de sus descendientes `position:absolute`/`fixed` (no solo el positioned-ancestor habitual).

Síntoma real (TuFacturaIA): apliqué una animación de entrada `.reveal` (con `transform: translateY + scale` y `filter: blur`) a la KPICard. Dentro, `OdometerValue` posiciona el carril de dígitos rodantes con `position:absolute`. El transform/blur de la card durante la animación reancló ese carril → las celdas de dígitos aparecían VACÍAS (card con borde pero sin contenido).

Regla: no metas animaciones de entrada con transform/filter en un contenedor que aloja hijos `position:absolute` (carruseles de dígitos, tooltips anclados, popovers inline, sparklines SVG posicionados). Opciones:
- que el elemento ya tenga su propio gesto (el odómetro se anima solo → no le añadas .reveal encima),
- animar solo `opacity` (no crea bloque contenedor),
- o portar el hijo absoluto fuera del subárbol animado.

Regla general: un gesto de entrada por superficie, no dos compitiendo. Ver [[skeleton-debe-calcar-el-layout-real-para-no-hacer-snap]].
