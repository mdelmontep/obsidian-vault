---
title: retirar un campo de una interfaz no es un candado — el excess-property check no mira los spreads
date: 2026-08-14
source: claude-code-session agh-iberica
tags: [typescript, testing, candados, gotcha]
---
Al quitar un campo de un contrato para que dejara de viajar, el razonamiento natural —«lo retiro del
tipo, ya está protegido»— es **falso**, y se mide en dos líneas:

```ts
f({ a, b, c, fila: 7 })                    // TS2353 ✅ lo caza
f({ a, b, c, ...(cond ? {} : { fila }) })  // tsc exit 0 ❌ PASA
```

El **excess-property check solo se aplica a literales de objeto**, no a lo que entra por un spread.

Lo caro es que **las dos vías de verificación dan verde a la vez**: `tsc` pasa, y el arnés de mutación
es ciego a los tipos por construcción (transpila con esbuild, ver
[[un-arnes-de-mutacion-sobre-vitest-no-ve-los-candados-de-tipos]]). Se puede declarar «protegido por el
tipo» con las dos medidas en verde y el hueco intacto.

**Fix:** el candado es un **test que le pasa el campo igual** al productor y exige que la salida no
cambie. Y el diseño que lo hace por construcción: **que la función pura ignore lo no declarado**, en vez
de confiar en que nadie se lo pase. Al escribir en una PR «esto lo cubre el tipo», poner el
contraejemplo del spread y comprobar que también cae; si no cae, el tipo cubre la mitad.

⚠️ No dar por hecho que un flag lo arregla (`exactOptionalPropertyTypes`): probarlo **contra este mismo
contraejemplo** antes de recomendarlo.
