---
title: regenerar types.gen contra prod si hay PR abierto que lo toca = conflict
date: 2026-05-05
source: claude-code-session
tags: [openapi, git, workflow, ci]
---

Si hay un PR abierto que toca `types.gen.ts` (regen previo o cambio manual), no regenerar contra prod desde main hasta que el PR mergee. Conflict garantizado en ese fichero — autogenerado por openapi-typescript = orden de keys, comments, y formato cambian con cada run.

**Patrón**: consolidar en UN solo PR post-merge:
1. Regen `types.gen.ts` contra prod
2. Quitar `as never` y `eslint-disable` workarounds que dependían de tipos viejos
3. Features dependientes de los tipos nuevos (columnas, handlers que usan campos recién documentados)

Caso: agency-portal #54 (en revisión) toca `types.gen.ts`. Para añadir migration `quotes.converted_facturaia_factura_id` + populate, esperar merge de #54 antes de tocar tipos generados.

Excepción: si el PR abierto NO regenera tipos (solo añade `as never` workaround), se puede regenerar en paralelo siempre que no haya cambios en el openapi.json upstream que el otro PR ignore.
