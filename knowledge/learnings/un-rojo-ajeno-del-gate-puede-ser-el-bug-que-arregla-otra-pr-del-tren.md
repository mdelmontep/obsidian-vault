---
title: un rojo ajeno del gate puede ser el bug que arregla otra pr del mismo tren
date: 2026-09-22
source: agh-iberica
tags: [gate, merge-train, flaky-tests]
---
**Qué pasó (22-sep, ola B):** el `gate:full` de PR-3 (#2012) salió rojo tres veces, siempre con un `57P01` no capturado desde un `.pg` que el diff no tocaba. Lo clasifiqué como carga de la máquina y relancé con carga < 10: rojo otra vez. Ese error era justo el bug #2009 (un `Pool` sin oyente de `'error'`), y su arreglo iba en otra PR del mismo tren, #2010. La integración que llevaba las dos juntas salía verde.

**Patrón:** si el rojo «ajeno» repite su firma entre intentos (no cambia de fichero) y el tren contiene una PR que arregla esa firma, no es ruido: el orden del tren está mal.

**Fix:** mergear primero la PR del arreglo, rebasar la otra encima y medir una sola vez. Con #2010 debajo, el gate de PR-3 pasó todas las suites a la primera.

**Discriminador:** «los ficheros en rojo cambian entre intentos» = carga; misma firma en cada intento, o que sobrevive a bajar la carga = causa real.

Relacionado: [[integrar-la-ola-entera-antes-de-mergear-caza-defectos-de-composicion]] · [[la-cola-del-gate-miente-en-dos-direcciones]]
