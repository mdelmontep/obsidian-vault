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
