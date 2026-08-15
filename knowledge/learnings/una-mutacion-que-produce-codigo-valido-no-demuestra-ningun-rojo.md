---
title: una mutación que produce código válido no demuestra ningún rojo, y se lee igual que un gate flojo
date: 2026-08-15
source: claude-code-session
tags: [gates, mutacion, harness, tucrmia]
---
Para demostrar el rojo de un gate de sintaxis, inyecté un acento grave dentro de un `.mjs` real.
El gate salió **verde**, y la conclusión fácil era «el gate no vigila esa mitad». Falsa: el
parche cerraba una plantilla y abría otra, o sea que **producía JavaScript válido**. Mutación
sin víctima.

Se distingue en un paso: antes de culpar al gate, comprueba que la mutación **rompe de verdad
lo que dices romper** — aquí, `node --check` sobre el fichero mutado. Si el fichero mutado sigue
siendo válido, no has probado nada.

Es el hermano del fallo que `~/.claude/bin/mutate` ya cubre por el otro lado (el arnés no
ejecutó los tests): allí el medidor no mide, aquí **el estímulo no estimula**. Los dos dan el
mismo síntoma —verde tras mutar— y la conclusión contraria.

Rehecha inyectando dentro de una plantilla existente → exit 1. Y el caso simétrico también pasó
esa noche: un gate correcto rechazando el arreglo correcto sólo se ve **aplicándolo al árbol
real**, no a un fixture.

Ver [[dos-trampas-al-escribir-un-gate-por-arbol-de-sintaxis]] · [[un-detector-nuevo-cuyo-cero-no-mediste-antes-no-vale]]
