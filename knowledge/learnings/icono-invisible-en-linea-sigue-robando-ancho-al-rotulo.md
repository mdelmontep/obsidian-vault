---
title: un icono con opacity 0 sigue ocupando ancho y recorta el rótulo de al lado
date: 2026-07-29
source: claude-code-session
tags: [css, frontend, tablas, a11y]
---

Cabecera de tabla que recorta con "…" **teniendo hueco visible al lado**: ese
hueco no está libre. `opacity: 0` oculta, no saca del flujo — la flecha de orden
seguía ocupando sus 12 px más los 4 del `gap` en TODAS las columnas, también en
las inactivas donde nunca se ve.

Medido (Materiales, columna a 81 px): 24 de padding + 16 de icono invisible = 41
px útiles para un rótulo que necesita 46. Faltaban 5.

Fix: el icono a `position: absolute` con el botón de ancla, y `padding-right`
equivalente SOLO donde el icono es permanente (columna activa) o el texto va
pegado al borde (columnas numéricas) — así esas se ven igual que antes.

Efecto que hay que aceptar a propósito: en hover sobre una cabecera llena, el
icono se superpone al final del texto. Reservarle el hueco solo en hover mueve el
texto bajo el cursor, que despista más.

Antes de tocar anchos, mide el NODO DEL TEXTO (`scrollWidth > clientWidth`), no
la celda: dice si recorta y cuánto falta. Ver
[[table-layout-fixed-con-width-100-reparte-los-px-en-vez-de-respetarlos]].
