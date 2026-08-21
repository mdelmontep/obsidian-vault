---
title: buscar sin acentos en postgrest es imatch con clases, no unaccent
date: 2026-08-21
source: facturaia
tags: [postgrest, supabase, postgres, busqueda]
---

PostgREST **no** deja aplicar una función a la columna en un filtro: `unaccent(nombre).ilike.*x*` no existe. Y una columna generada normalizada solo sirve si la tienen TODOS los campos buscables (el proveedor que lee el OCR vive dentro de un JSONB, no la tiene).

Salida sin tocar el esquema: `imatch` (el `~*` de Postgres) con clases de equivalencia por letra.

- Escapar primero los especiales de regex (`\ ^ $ . | ? * + ( ) [ ] { }`), luego cada letra a su clase: `a`→`[aáàäâ]`, `n`→`[nñ]`, `c`→`[cç]`.
- Varias palabras se unen con `.*`: "telefonica espana" casa "Telefónica de España, S.A." con sus comas y sus puntos.
- El plegado de mayúsculas de `~*` **también actúa dentro de la clase**: `[ií]` casa `Í`. No hay que añadir las acentuadas en mayúscula.
- Vale igual sobre JSONB (`datos_extraidos->>prov.imatch.<patron>`) y dentro de un `or=(...)`.
- Sin índice es seq scan: aceptable en un listado ya filtrado por `org_id`; si crece, índice trigram sobre la expresión.

Caso real (ticket 152): cuatro grafías del mismo proveedor conviviendo en prod, una sola consulta las devuelve las cuatro. Validado contra el PostgREST de producción **antes** de escribir el código.
