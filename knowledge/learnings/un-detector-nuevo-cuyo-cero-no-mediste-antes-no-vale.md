---
title: un detector nuevo cuyo cero no mediste antes de escribirlo no vale
date: 2026-08-09
source: claude-code-session
tags: [guards, trinquetes, harness, metodo, verificacion]
---

Dos formas de parir un guard muerto, las dos pagadas el 9-ago escribiendo `locator-guard`
(TuFacturaIA #1578):

**1. Su cero es infalsificable si no sabes cuántos DEBÍA encontrar.** La primera versión salió
**verde sobre un repo que tenía 2 hallazgos**: el contenido del string excluía toda comilla, así que
cortaba en la primera interior y `'[role="dialog"], .modal'` —la forma más común de selector— no
casaba. Su propia suite habría pasado entera: los casos a mano usan selectores simples. Lo cazó
haber **medido el corpus real ANTES** (5 choques esperados) y ver que el guard decía 0. Regla: mide
primero sobre el repo, escribe después, y si el número no cuadra el bug es del guard.

**2. Un guard que relaciona DOS artefactos tiene que dispararse desde los DOS lados.** Aquí el
locator (spec) contra la clase (`*.module.css`). El fallo real llegó en dos commits y **el segundo
no tocaba ningún spec**: uno escribió el locator con la clase aún global, otro hasheó la clase al
día siguiente. Mirando solo los specs staged, el commit que rompe pasa limpio. Con un `.module.css`
staged hay que barrer TODOS los specs. Vale igual para código↔migración y tipo↔consumidores.

Y el de siempre: **probarlo por el camino real**, con `git commit` de verdad y comprobando que NO se
creó el commit — no solo con su suite. Ver [[un-guard-cuya-aguja-cubre-una-sola-forma-sintactica-se-esquiva-refactorizando]] ·
[[verificar-que-un-test-tiene-dientes-con-una-mutacion]] · [[locator-de-test-atado-a-la-implementacion-caduca-y-da-falso-verde]]
