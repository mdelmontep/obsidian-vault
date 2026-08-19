---
title: la maqueta se mide con el motor, no se modela sumando anchos
date: 2026-08-08
source: claude-code-session
tags: [testing, css, frontend, playwright, guards]
---

Un test que suma anchos de CSS para decidir si algo CABE solo vale si las
columnas son anchos declarados. Con pistas `auto`, `grid-template-areas`, texto
que envuelve o un marco de página que no está en ese fichero, el modelo miente
en las dos direcciones — y un guard más flojo que la realidad da confianza falsa.

La salida no es un modelo mejor: es no modelar. Un proyecto de Playwright que
monta el componente con el CSS del repo (`setContent` + los módulos con
`:global()` aplanado) y lo mide en el navegador. **Sin servidor, sin sesión y sin
datos**: no puede ponerse rojo porque alguien borre un registro, y corre en un
clon sin credenciales (`testDir` propio: los specs con seed revientan al
IMPORTARSE sin `.env.test`).

Nació rojo y cazó un desbordamiento que la aritmética daba por bueno: otro PR
había metido un código de unidad de 10 px por celda que nadie sumó.

**Y el fixture tiene que reproducir el MARCO de la página, no solo el
componente.** El primero colgaba la tarjeta del `<body>` sin el relleno del
shell: 32 px de más, o sea un guard que podía dar verde con 32 px de
desbordamiento real — y los dio. Con el marco puesto salió que la fila seguía
desbordando en el ancho de móvil más común. Si no puedes reproducir la cadena
entera, resta un colchón medido y que el fixture peque de estrecho: optimista es
peor que inexistente.

**Y el HTML literal tiene que llevar las clases del primitivo, con su CSS
inyectado.** Un `<button>` desnudo en el fixture se pinta con el chrome del
navegador —fuente, padding y borde por defecto— y **la barra mide lo que miden
sus botones**: la maqueta del anclaje en lote medía una barra que no es la de la
app. Medido con el arnés de mutación: quitar la inyección del CSS del primitivo
dejaba el gate en VERDE, porque `btn` salía de un comentario de `globals.css`,
`ghost` de `.saldo-hero-btn.ghost` y `sm` de `.icon-btn.sm` — tres clases de
otros componentes. Así que el gate deriva el vocabulario del CSS del propio
primitivo y exige su inyección. El trinquete de deuda de diseño no lo veía: solo
barre `src/**`.

Tres cosas más que cuestan una tarde si no se saben:
- **Sin `<meta viewport>` la emulación móvil maqueta contra 980 px** y ninguna
  media query aplica: el fixture aprueba una fila que en un móvil no cabe.
- «Mismo renglón» se decide por SOLAPE vertical de los rangos. Ni `top` (una
  fila con `align-items: center` no lo comparte) ni el centro (que se desplaza
  en cuanto una celda envuelve en tres líneas y su vecina no). Las dos me dieron
  renglones inventados.
- El fixture necesita candado contra la deriva: comparar sus celdas con las que
  pinta hoy el JSX. Si no, mides una maqueta que ya no existe.

Ver [[columna-que-aloja-un-control-necesita-un-ancho-por-tipo-de-puntero]] ·
[[un-guard-sobre-el-minimo-no-acota-la-magnitud]] · [[facturaia]].
