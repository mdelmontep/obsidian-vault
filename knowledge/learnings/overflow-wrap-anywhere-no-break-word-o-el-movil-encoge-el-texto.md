---
title: en móvil `break-word` no evita que la página se dibuje más ancha que el teléfono
date: 2026-08-11
source: claude-code-session
tags: [css, movil, frontend]
---
Un elemento más ancho que la pantalla se paga de dos formas y **solo una se ve**: o aparece scroll
lateral, o el navegador dibuja la página más ancha que el dispositivo y todo el texto sale
encogido, sin ninguna barra que lo delate. A ojo parece "que la letra es pequeñita".

`word-break: break-word` NO arregla el segundo caso: no reduce el *ancho mínimo intrínseco*, que es
el número con el que el navegador decide el ancho de layout. Hace falta `overflow-wrap: anywhere`.

Aplicarlo a todo lo que lleve rutas, identificadores o URLs: `code`, citas `fichero:línea`,
breadcrumbs, celdas de tabla.

Para medirlo, el ancho de **layout** de `<html>` contra el del dispositivo — nunca
`window.innerWidth`, que en emulación reporta el área desplazable y da falso positivo con cualquier
bloque que tenga scroll propio. Para encontrar al culpable, bisección del DOM: ocultar elementos uno
a uno y ver cuál baja el `scrollWidth`. Gate de ejemplo: `learn-agentesia/scripts/mirar-movil.mjs`.
