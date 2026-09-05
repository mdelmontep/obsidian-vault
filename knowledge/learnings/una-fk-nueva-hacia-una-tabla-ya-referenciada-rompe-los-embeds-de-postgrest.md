---
title: una FK nueva hacia una tabla ya referenciada rompe TODOS los embeds de PostgREST
date: 2026-09-05
source: facturaia
tags: [postgrest, supabase, migraciones, incidentes]
---
Añadir una segunda FK de `hija → padre` deja **ambiguo todo embed entre esas dos tablas**, en las
dos direcciones: PostgREST responde `300 PGRST201 "more than one relationship was found"`. No es un
warning; la petición falla. Caso real: la mig 845 de FacturaIA añadió
`lineas_factura.linea_origen_factura_id → facturas` y tumbó 8 sitios, entre ellos el PDF que se
manda al cliente y el cargador fiscal.

- El hint es `tabla!columna(...)` o `tabla!nombre_del_constraint(...)`.
- **`!inner` NO desambigua**: es cardinalidad, no hint. `facturas!inner(...)` sigue dando 300; la
  forma correcta es `facturas!factura_id!inner(...)`. Es la trampa, porque parece cualificado.
- El `order=tabla(col)` que cuelga de un embed ya cualificado NO lleva hint: nombra el alias.
- El typecheck **no lo ve** mientras los tipos generados vayan por detrás del esquema; ver
  [[gen-types-linked-no-db-url]].
- Censar a ojo no basta: derivar los pares ambiguos de las FK de `database.types.ts` encontró 2
  sitios más, uno roto desde antes (el copiloto no podía explicar un movimiento con sugerencias).
  Misma familia que [[un-guard-sobre-sql-tiene-que-conocer-el-embed-y-el-alias-de-postgrest]].
