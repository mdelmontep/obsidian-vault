---
title: un patrón que filtra por nombre de identificador se enumera, no se imagina
date: 2026-08-23
source: facturaia
tags: [regex, guards, copiloto, gotcha]
---
`^[a-zA-Z]+_failed:` parece cubrir «cualquier `<tool>_failed:`» y no cubre
ninguno cuyo nombre lleve `_` dentro: `[a-zA-Z]+` no cruza el guion bajo, así
que `buscar_catalogo_fuzzy_failed:` no encaja y el texto crudo de Postgres pasa
de largo. En FacturaIA eran 3 de los 16 prefijos reales, y el filtro existía
justo para que ese texto no llegara al LLM, que lo parafrasea en afirmaciones
falsas («no tienes movimientos» cuando falló la query).

No se detecta leyendo el regex: se detecta enumerando el conjunto real,
`grep -rhoE "'[a-zA-Z_]+_failed:|\`[a-zA-Z_]+_failed:" <dir> | sort -u`, y
comprobando cuántos encajan. Vale para cualquier lista negra sobre nombres que
genera otro sitio (tools, eventos, códigos de error, feature flags).

Corolario: si el patrón vigila algo que importa, el conjunto que cubre se
imprime en un test, no se confía a la vista.
