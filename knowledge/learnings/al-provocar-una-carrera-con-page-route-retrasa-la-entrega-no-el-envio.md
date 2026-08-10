---
title: al provocar una carrera con page.route, retrasa la ENTREGA, no el envío
date: 2026-08-11
source: claude-code-session
tags: [playwright, testing, carreras, metodo]
---
Para hacer determinista un bug de carrera lectura-vs-escritura (issue #1595 de
TuFacturaIA) retrasé la lectura así:

```js
await route.continue()          // ← tras dormir 8 s: MAL
```

`continue()` dispara la petición **al soltarla**, así que salía después del PATCH
y volvía con el dato **ya corregido**. La sonda no medía nada y daba un «sin
víctima» falso. Lo correcto es disparar ya y retrasar la entrega:

```js
const resp = await route.fetch()          // sale AHORA → trae el valor viejo
const body = await resp.text()
await new Promise(r => setTimeout(r, 8000))
await route.fulfill({ response: resp, body })
```

Corolario del mismo caso: un **heisenbug de `console.log`** (deja de reproducir al
instrumentar) no es propiedad del bug, es propiedad de *perseguir* la carrera. Con
la precondición provocada, instrumentar vuelve a ser seguro. Y antes de declarar
equivalente una mutación sin víctima, mete un **testigo** (cambia un texto visible)
para probar que el servidor sirve tu checkout. Ver
[[un-control-negativo-que-no-discrimina-invalida-el-test-entero]] y
[[estado-cargado-por-effect-como-precondicion-de-escritura-descarta-el-gesto]].
