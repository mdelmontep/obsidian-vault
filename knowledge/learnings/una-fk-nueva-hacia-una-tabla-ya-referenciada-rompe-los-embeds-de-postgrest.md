---
title: una FK nueva hacia una tabla ya referenciada rompe TODOS los embeds de PostgREST
date: 2026-09-05
source: facturaia
tags: [postgrest, supabase, migraciones, incidentes]
---
Una segunda FK de `hija → padre` deja **ambiguo todo embed entre esas dos tablas, en las dos
direcciones**: `300 PGRST201`. No es un warning, la petición falla. La mig 845 de FacturaIA añadió
`lineas_factura.linea_origen_factura_id → facturas` y tumbó 10 sitios, entre ellos el PDF que se
manda al cliente y el cargador fiscal.

- El hint es `tabla!columna(...)` o `tabla!constraint(...)`.
- **`!inner` NO desambigua**: es cardinalidad, no hint. `facturas!inner(...)` sigue dando 300; la
  forma correcta es `facturas!factura_id!inner(...)`. Es la trampa, porque parece cualificado.
- El `order=tabla(col)` colgado de un embed ya cualificado NO lleva hint: nombra el alias.
- El typecheck no lo ve mientras los tipos vayan por detrás → [[gen-types-linked-no-db-url]].
- Censar a ojo no basta; derívalo de las FK de `database.types.ts` — así salieron 2 sitios más,
  uno roto de antes. Agrupa por `foreignKeyName`, **no por columna**: dos constraints sobre la
  misma columna también dan 300. Las vistas salen como `referencedRelation`, así que cada par
  trae su gemelo contra la vista (22 pares en FacturaIA, 6 contra vistas).
- **Un censo sobre un checkout viejo cuenta de menos y no lo dice**: los mismos tipos que ocultan
  el fallo ocultan el par que lo causa. Mide sobre `git show origin/main:<ruta>`.
  Misma familia que [[un-guard-sobre-sql-tiene-que-conocer-el-embed-y-el-alias-de-postgrest]].
