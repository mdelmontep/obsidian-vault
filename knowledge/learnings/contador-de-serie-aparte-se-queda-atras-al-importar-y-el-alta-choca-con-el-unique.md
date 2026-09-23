---
title: un contador de serie en tabla aparte se queda atrás al importar y el alta choca con el unique
date: 2026-09-23
source: facturaia
tags: [postgres, numeracion, migracion-datos, importacion]
---
Patrón: la numeración sale de una tabla contador `(org, año) → ultimo_numero` con `INSERT … ON CONFLICT DO UPDATE +1`, y la tabla de documentos tiene un UNIQUE sobre ese número.

Gotcha: si se importan documentos con su número original (wapi → FacturaIA, sandbox de Obras), nadie siembra el contador. El siguiente alta pide el 1, el 2… y cae en `23505` → 500. Y si el contador se incrementa en una transacción distinta de la del insert, cada intento fallido quema un número sin crear nada.

Medida (23-sep-2026): contador de 2026 en 4, números 1-86 ocupados. El UNIQUE viejo habría fallado igual, así que no era la migración recién aplicada.

Fix: sembrar el contador con `GREATEST(ultimo_numero, max(numero))` en la propia importación, o que la función del contador salte números ocupados. El mismo choque aparece si un cliente pide «ponerlo a cero» a mitad de año con documentos de prueba vivos en ese año: resetear en año nuevo o borrar antes.

Detectar: `max(numero)` por `(org, año)` contra `ultimo_numero`, filas con contador < máximo.
