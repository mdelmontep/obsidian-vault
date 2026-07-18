---
title: playwright boundingBox() mide la geometría del elemento aunque un ancestro lo recorte con overflow:hidden
date: 2026-07-18
source: claude-code-session
tags: [playwright, testing, css, frontend]
---

Al verificar un colapso/ocultado por CSS: `locator.boundingBox()` devuelve el rectángulo de
LAYOUT del elemento (p.ej. 230×30) **aunque un ancestro con `overflow:hidden` + altura 0 lo esté
recortando visualmente**. El hijo se maqueta y luego se recorta; boundingBox no refleja el recorte.

→ Para comprobar que algo colapsa de verdad, mide el **alto del contenedor** que colapsa
(`el.offsetHeight` / `getBoundingClientRect().height` del wrapper), no el boundingBox del hijo.
Confirmación cruzada de "no clicable": intenta `locator.click({timeout})` — con `inert` lanza
timeout, señal directa de que el click no llega.

Caso real: repro del bug del sub-menú de Obras (FacturaIA) — el sub-item daba 230×30 en boundingBox
pese a estar en un grupo cerrado; el wrapper pasó de 65px→0px con el fix. Ver
[[colapso-grid-0fr-child-divergente-queda-inert-visible]].
