---
title: GIN pg_trgm no resuelve el LIKE invertido (aguja variable, pajar fijo)
date: 2026-07-25
source: claude-code-session
tags: [postgres, pg_trgm, indices, rendimiento]
---

Un índice GIN `pg_trgm` responde **"qué filas contienen ESTE patrón"**: el pajar está indexado, la aguja llega por query. No puede responder lo contrario: **"cuál de mis muchas agujas está contenida en ESTE texto fijo"**.

Caso real: buscar facturas cuyo `num` aparezca en la descripción de un movimiento bancario.
```sql
-- NO se indexa: la aguja varía por fila de facturas, el pajar es un único texto
WHERE position(normalizar_num(f.num) IN v_mov_desc) > 0
```
Un GIN sobre `movimientos_bancarios.descripcion` es inútil aquí → seq scan de todas las facturas de la org + una llamada a función por fila. Dentro de un trigger `FOR EACH ROW` de un import masivo, eso revienta.

Fix: darle la vuelta a igualdad indexada. Extraer los tokens del texto fijo **una vez** y comparar contra una expresión indexada del otro lado:
```sql
-- v_tokens := regexp_matches(v_mov_desc, <forma del nº>)
WHERE normalizar_num_match(f.num) = ANY(v_tokens)
-- CREATE INDEX ON facturas (org_id, normalizar_num_match(num));
```
Exige que la función sea **IMMUTABLE** (si no, no se puede indexar; ver [[postgres-unaccent-no-immutable-index-necesita-wrapper]]). Resultado: exacto, O(log n), sin trgm.

Regla de decisión: si el patrón viene de la query → GIN trgm sirve. Si el patrón vive en una columna y el texto viene de la query → reescribir como igualdad sobre índice de expresión. El trgm solo vuelve a ser útil si de verdad quieres *fuzzy*, y entonces el índice va del lado de la tabla de patrones (clientes/proveedores), no del texto. Relacionado: [[postgres-word-similarity-vs-similarity-para-needle-in-haystack]] · [[date-trunc-en-where-no-sargable-aunque-haya-indice]].
