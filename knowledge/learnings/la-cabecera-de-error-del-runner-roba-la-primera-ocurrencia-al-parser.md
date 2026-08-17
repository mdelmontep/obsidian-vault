---
title: la cabecera de error del runner roba la primera ocurrencia y el parser cuenta 0 pasados
date: 2026-08-17
source: claude-code-session
tags: [testing, parsing, gate, vitest, ci]
---

Un parser de la salida de un runner que hace `output.match(/\bTests\s+(.+)/)` —**sin `g`**, o sea la
PRIMERA ocurrencia— acierta en verde y **miente en toda corrida con fallos**: vitest imprime el
detalle del fallo bajo una cabecera `⎯⎯⎯ Failed Tests 1 ⎯⎯⎯`, que contiene la misma palabra que el
resumen y aparece **antes**.

```
1a ocurrencia  "Tests 1 ⎯⎯⎯⎯⎯"                    <- la cabecera: lo que captura
la de verdad   "Tests  1 failed | 1270 passed"    <- el resumen
```

Sobre lo capturado no hay `passed` → el recuento sale **0**. Y `0 passed` se lee como «no arrancó»,
que es la conclusión **opuesta** a la verdad (habían pasado 1.270).

- **La pista que lo delata** es una asimetría: `Test Files` sí acertaba (su regex no colisiona con
  ninguna cabecera) y `Tests` no. Si un campo del resumen acierta y su hermano no, sospecha del regex,
  no de la corrida.
- **Fix**: coger la ÚLTIMA ocurrencia, o anclar al bloque de resumen.
- **El candado tiene que llevar la cabecera dentro del fixture**: un fixture con sólo el resumen
  limpio pasa igual con el regex roto y con el bueno. Ver
  [[una-metrica-por-regex-sin-test-del-parser-cuenta-ruido-y-se-vuelve-ignorable]].

Vale para cualquier runner cuya salida repita sus palabras clave en las cabeceras de error (jest,
pytest, eslint). Caso real: la línea del gate de agh-iberica lo hacía desde su origen, y el síntoma
—«`tests 0 passed` habiendo pasado 3.429»— se había atribuido a un timeout que no reproducía.
