---
title: un script-gate con guard de entrypoint puede degradar a no-op silencioso y salir con 0
date: 2026-08-02
source: claude-code-session
tags: [gates, ci, node, testing]
---
Para poder testear las funciones de un script que hace su trabajo al importarse, la tentación es un
guard de entrypoint:

```js
if (process.argv[1] !== fileURLToPath(import.meta.url)) { /* solo exporta */ } else { …el gate… }
```

Modo de fallo: invocado por un **symlink** o cualquier wrapper, la comparación falla, el cuerpo no se
ejecuta y el proceso sale con **código 0**. El gate pasa a verde sin comprobar nada. Reproducido en
TuFacturaIA con los trinquetes de CSS y de diseño.

Fix: que no haga falta el guard. Las funciones puras a un módulo sin efectos (`scripts/lib/*.mjs`);
el script las importa y ejecuta siempre, el test importa solo el módulo.

Regla: un gate solo puede fallar **haciendo ruido**. Si existe un camino en el que no mide y devuelve
0, ese camino acabará siendo el de producción. Ver [[actions-sin-billing-hooks-locales-unico-gate]].
