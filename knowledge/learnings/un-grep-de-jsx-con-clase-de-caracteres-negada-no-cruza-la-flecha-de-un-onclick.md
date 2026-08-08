---
title: un grep de JSX con clase de caracteres negada no cruza la flecha de un onClick
date: 2026-08-08
source: claude-code-session
tags: [jsx, testing, refactor, deuda-tecnica]
---

`<Button[^>]*>` parece que casa la etiqueta de apertura y no casa: `onClick={() =>
algo()}` tiene un `>` dentro, así que `[^>]*` se para ahí. Resultado: los botones
escritos en UNA línea salen y los de VARIAS con manejador inline no. El barrido
sale corto y no avisa de nada.

Caso real (8-ago, TuFacturaIA): tres sesiones rastrearon la misma deuda con tres
regex distintas y dieron 2, 10 y 16. El censo real era 51. Con la lista corta se
escribió «quedan dos» en el manual y se dio la deuda por cerrada dos veces.

Para casar una etiqueta JSX hay que **contar llaves** y saltarse el contenido de
las comillas, no negar caracteres:

```js
let llaves = 0, comilla = null
for (let i = inicio; i < src.length; i++) {
  const c = src[i]
  if (comilla) { if (c === comilla && src[i-1] !== '\\') comilla = null; continue }
  if (c === '"' || c === "'" || c === '`') { comilla = c; continue }
  if (c === '{') llaves++
  else if (c === '}') llaves--
  else if (c === '>' && llaves === 0) return i   // aquí cierra de verdad
}
```

Regla general: **un inventario que hay que rehacer a mano se rehace mal**. Si la
misma pregunta se hace dos veces, el censo va a un script con su línea base
commiteada y un test que exija clasificar lo nuevo. No obliga a arreglarlo:
obliga a decidirlo. Ver [[facturaia]].
