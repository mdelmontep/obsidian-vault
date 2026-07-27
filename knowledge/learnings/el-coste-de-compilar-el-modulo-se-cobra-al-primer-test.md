---
title: el coste de compilar el módulo se le cobra al primer test y lo saca de su timeout
date: 2026-07-28
source: claude-code-session
tags: [testing, vitest, flaky, rendimiento]
---

Un fichero de tests que hace `await import('../route')` dentro del primer test le
está cobrando a ese test la **transformación de todo el grafo de módulos**. Vitest
la cachea después, así que el reparto queda absurdo: el primero tarda segundos y
los demás decenas de milisegundos.

Medido en TuFacturaIA: primer test **2.804 ms**, resto 30-65 ms. Y con la suite
completa (767 ficheros compitiendo por CPU) esa transformación pasa de **10 s**.
Con el `testTimeout` por defecto de 5 s, el resultado es un flaky que aparece solo
cuando la máquina está ocupada y **con mensajes de aserción**, no de timeout
(`expected 409 to be 200`), porque el test se corta a medias. Parece un bug de
lógica y no lo es.

Fix: sacar el coste del reloj de los tests con un hook de precalentado, con su
propio timeout generoso:

```ts
beforeAll(async () => { await import('../route') }, 60_000)
```

Los tests conservan su timeout estricto, que es donde debe saltar un cuelgue real.
Subir `testTimeout` en su lugar esconde el problema y deja los tests sin red.

Distinguir del otro caso: si lo caro es **trabajo del test** (renderizar un tab y
abrir un popup en jsdom: 569 ms), no hay nada que mover y lo correcto sí es un
timeout mayor **en ese test concreto**, documentando la medida. Diagnóstico
primero: `--reporter=verbose` y mirar la duración del primero contra el resto.

Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]]
