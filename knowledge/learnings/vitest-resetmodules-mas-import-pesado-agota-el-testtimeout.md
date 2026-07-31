---
title: vi.resetModules() + import dinámico dentro del test agota el testTimeout en routes pesados
date: 2026-07-27
source: claude-code-session
tags: [vitest, testing, performance, nextjs]
---

Patrón común: `vi.resetModules()` en `beforeEach` y `await import('../route')` dentro del helper de cada test. Con un route pesado eso **no es aislamiento, es repetir la transformación del grafo entero** contra el `testTimeout`.

Medido en facturaia (route del Copiloto, arrastra runner + todas las tools): import #0 = 12.993 ms, #1 = 465 ms, #2 = 327 ms. Con timeout de 5 s reventaban los ~3 primeros tests de cada fichero y pasaban los siguientes, ya en caliente.

Síntomas que despistan:
- Fallos que **parecen** de aserción (`expected 409 to be 200`, inserts duplicados): al abortar por timeout, el trabajo async en vuelo sigue escribiendo en los mismos mocks y contamina el test siguiente.
- Distinto número de fallos en aislado que en la suite completa: otros ficheros ya calentaron parte del grafo.

Fix: subir el `import` a top-level tras las declaraciones de mocks, y quitar el `resetModules` si el módulo no tiene estado mutable a nivel de módulo (comprobarlo: si solo hay constantes y esquemas, no aislaba nada). En facturaia la suite bajó de 214 s a 122 s.

Antes de culpar a un mock: mide el coste del import con `vi.resetModules()` entre iteraciones. Ver [[e2e-baseline-contra-main-antes-de-culpar-a-tu-rama]].

**Cierre 2026-07-31**: el mismo mecanismo, sin `resetModules` de por medio. Dos ficheros pasaban por
"flaky por depender del reloj" y ninguno usa timers, `Date.now` ni `sleep`: el primer caso de cada
fichero paga transform + environment + import (medido, 528 ms y 335 ms frente a 1 ms y 50 ms de sus
hermanos) y bajo carga rebasa el default de 5 s. **El arreglo tiene que ser global** (`testTimeout` y
`hookTimeout` en la config), o el siguiente fichero pesado repite el flake. Un gate que se pone rojo
por causas ajenas al cambio enseña a ignorar los rojos.

