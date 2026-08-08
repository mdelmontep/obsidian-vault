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

Tres cosas que cuestan una tarde si no se saben:
- **Sin `<meta viewport>` la emulación móvil maqueta contra 980 px** y ninguna
  media query aplica: el fixture aprueba una fila que en un móvil no cabe.
- Una fila con `align-items: center` NO comparte `top` entre celdas del mismo
  renglón: compara centros, o inventas renglones.
- El fixture necesita candado contra la deriva: comparar sus celdas con las que
  pinta hoy el JSX. Si no, mides una maqueta que ya no existe.

Ver [[columna-que-aloja-un-control-necesita-un-ancho-por-tipo-de-puntero]] ·
[[un-guard-sobre-el-minimo-no-acota-la-magnitud]] · [[facturaia]].
