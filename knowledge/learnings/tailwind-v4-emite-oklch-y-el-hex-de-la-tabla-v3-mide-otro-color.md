---
title: tailwind v4 emite oklch, y el hex de la tabla v3 mide otro color
date: 2026-09-10
source: ecobox
tags: [tailwind, css, accesibilidad, gates]
---
Un gate de contraste que resuelve `bg-emerald-500` mirando la tabla de colores de
Tailwind v3 mide **un color que la página no pinta**. v4 define su paleta en
`oklch()`, y el sRGB resultante no es el hex de v3:

    emerald-500   v3 (tabla) #10b981   ·   v4 (renderizado) #00bc7d

Sobre el verde real, texto blanco da 2,47:1 — falla AA y el gate lo llamaba
aprobado porque medía el otro verde.

Fix: el gate no traduce nombres de clase a hex de memoria; **lee los tokens del
CSS compilado** (o los píxeles renderizados) y convierte oklch→sRGB. Lo mismo
vale para cualquier paleta declarada en un espacio de color moderno: `color-mix()`,
`lab()`, `hsl()` con `calc` dentro.

Señal de que estás en esto: un valor de contraste que no cambia nunca aunque
toques el token. Ver [[apca-gate-script-tokens]].
