---
title: un ensayo en seco que sustituye el gate no prueba la medida
date: 2026-09-23
source: facturaia
tags: [harness, medicion, fia-gate, hooks, claude-code]
---

Preparando la tanda nocturna del arnés, los dos ensayos en seco se hicieron **contra un
doble** del semáforo: uno con un stub de `fia-gate` en `_sandbox/`, otro con
`FIA_GATE_MIN=4`. Los dos dieron verde. Con el gate REAL, la palanca murió en el primer
intento: `fia-gate` lanza `bash -c "$1" </dev/null`, así que **aísla el stdin** y la
línea de refs que el `pre-push` recibe por ahí no llegaba al script de etapas — 0 filas
medidas y `ec=98`. Arreglado pasando el dato por variable (`$ETAPAS_REFS`) y dejando el
stdin como camino alternativo; re-verificado a través del gate real, incluido el negativo
(canal roto → sigue abortando).

**Patrón:** un ensayo que sustituye la pieza que va a estar en producción no prueba nada
sobre el camino real. Es el mismo error que el hook con 15 casos en verde que no disparaba
nunca porque el `git status` corría en otro cwd. Si la medida va a pasar por el gate, el
ensayo pasa por el gate.
Ver [[una-lectura-de-load1-no-acredita-una-ventana-de-medida]] · [[fia-gate]].
