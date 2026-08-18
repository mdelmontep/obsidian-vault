---
title: un gate derivado del repo pasa en verde si su lista de objetivos sale vacía
date: 2026-08-18
source: facturaia
tags: [gates, testing, ci]
---
Un gate que **descubre** lo que audita (grep del repo, `it.each` sobre lo encontrado) tiene un modo
de fallo que no tiene el que lleva lista fija: si el patrón deja de encajar —renombran la tabla,
cambia el estilo del `.select()`, se mueve la carpeta— la lista sale **vacía** y la suite pasa en
verde sin haber comprobado nada. No falla: se calla.

Dos cosas que hay que escribirle encima, y las dos se verifican mutando:
- **Suelo explícito**: `expect(objetivos.length).toBeGreaterThanOrEqual(N)`. Mutando el patrón del
  detector, la suite tiene que ponerse roja (medido: 19 casos → 2, y falla).
- **Fallar cerrado** con lo que no sabe leer. Si el `.select()` trae las columnas en una variable, no
  se puede saber si incluye el campo vigilado: cuenta como infractor y que lo declare el autor.
  Descartarlo «porque no se puede analizar» es invisible, y lo invisible acaba siendo el camino
  normal.

Corolario: el detector va en su propio módulo con tests de fuentes sintéticas, no dentro del test que
lo usa. Ver [[un-script-gate-con-guard-de-entrypoint-degrada-a-no-op-silencioso]] ·
[[un-guard-que-grepea-el-texto-del-fichero-no-distingue-uso-de-asercion]].
