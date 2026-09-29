---
title: un guard de merge que mide la cabeza del pr no certifica el árbol que queda en main
date: 2026-09-29
source: facturaia (scripts/merge-gate-guard.mjs)
tags: [gate, merge, git, integridad]
---
El guard exige un verde registrado para el árbol de la cabeza del PR. Un squash sobre un main que ha avanzado produce un árbol distinto, que nadie ha medido.

- **Medido el 29-sep:** #3079, #3080, #3091 y #3092 entraron con la cabeza atrasada. La constancia existía para el árbol de la cabeza y no para el que quedó en main. El main final quedó medido por suerte, porque el último PR entró al día.
- **Sin red en el servidor:** repo privado en plan free, así que no hay protección de rama ni rulesets (la API da 403).
- **Cierre:** exigir `git merge-base --is-ancestor origin/main <cabeza>` o medir el árbol resultante del merge.
- **Mismo agujero con otra cara:** el PR decide qué etapas componen su verde, porque el script `gate` se lee de su propio `package.json`. La constancia tiene que nombrar el hash del arnés, o el guard tiene que compararlo con main.

Ver [[suite-filtrada-por-carpetas-del-pr-no-ve-los-guards-de-arquitectura]] · [[fia-gate]]
