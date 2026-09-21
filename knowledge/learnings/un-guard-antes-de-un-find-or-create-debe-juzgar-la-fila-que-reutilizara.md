---
title: un guard antes de un find-or-create debe juzgar la fila que este reutilizará
date: 2026-09-21
source: facturaia
tags: [validacion, find-or-create, guard, fiscal]
---
**Patrón:** un guard que va ANTES de un find-or-create, para no dejar filas huérfanas si rechaza, suele juzgar una entidad sintética («cliente nuevo, sin país»). Pero cuando la entrada trae la clave de deduplicación (el NIF) y no el id, el find-or-create reutiliza una fila EXISTENTE, con sus datos reales. El guard y la escritura juzgan entonces dos entidades distintas.

**Caso (facturaia #2815, PR #2842):** el guard del 0 % de `importarEmitidaExterna` juzgaba `{nif, pais: null}`, lo que equivale a «nacional». Si ya había una ficha con ese NIF y `pais = US`, rechazaba una exportación legítima. Ningún test lo pilló: el fake solo resolvía la búsqueda por id. Lo cazó la dimensión de cabos del `/fia-cierre`, al ver que el mensaje mandaba corregir una ficha que en ese camino no existía.

**Fix:** antes del guard, hacer una búsqueda de solo lectura con la MISMA normalización que usa el find-or-create, y juzgar esa fila. La entidad sintética queda solo para el caso de verdad nuevo, y el mensaje al usuario distingue los dos casos. Comprobarlo con `mutate` quitando la búsqueda: el test tiene que caer.

**Tell:** un mensaje de error que da por hecho que un registro existe, en una rama donde puede no existir, o al revés.
