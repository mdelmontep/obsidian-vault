---
title: header sticky con glass translúcido sangra el fondo por las esquinas — usar opaco
date: 2026-06-15
source: claude-code-session
tags: [frontend, css, glassmorphism, sticky]
---
Un header `position: sticky` con fondo translúcido + `backdrop-filter: blur`
sobre un mesh/gradiente de marca: (1) al hacer scroll el contenido pasa por
debajo y se transparenta; (2) el mesh se cuela por la tarjeta y en las esquinas
redondeadas dibuja un escalón/borde "sucio" que parece un radio roto.

NO es el border-radius ni la box-shadow: se confirma quitándolos en vivo y el
artefacto sigue; `elementsFromPoint` en la esquina no encuentra elemento con
radio → es el fondo colándose por el cristal.

Fix: el chrome sticky debe ser **opaco** (`--bg-elev` sólido) + borde de línea
+ sombra suave. Reserva el cristal translúcido para overlays sobre contenido
estable, no para barras sticky. Caso: TuFacturaIA `.summary-strip-compact`.

**Reincidencia 26-ago, y el matiz que la explica**: el fix de arriba dice «usar
`--bg-elev` sólido», pero en el tema glass `--bg-elev` **es** el translúcido
(`color-mix(in oklch, white 60%, transparent)`). Columna `sticky` del nombre en
la tabla de inventario: tres celdas numéricas leyéndose a través del nombre con
`scrollLeft=250`. Opaco de verdad = el mismo cristal sobre una base opaca:
`linear-gradient(var(--bg-elev), var(--bg-elev)), var(--bg)` — idéntico al resto
de la fila, pero sin dejar ver nada. Y el comentario del bloque ya decía «tiene
que ser OPACO»: escrito en prosa, no lo verificaba nadie. El guard parte el
`background` por comas de primer nivel y exige que la última capa sea opaca.
