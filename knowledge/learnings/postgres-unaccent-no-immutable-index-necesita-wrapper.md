---
title: unaccent() de postgres no es IMMUTABLE — falla en un índice sin wrapper
date: 2026-07-08
source: claude-code-session
tags: [postgres, index, unaccent]
---
Un `CREATE UNIQUE INDEX ... (lower(unaccent(trim(name))))` falla con `42P17 functions in index
expression must be marked IMMUTABLE` — `unaccent()` depende del diccionario de text search y
Postgres no la considera pura, aunque en la práctica sí lo sea para un uso normal.

Fix estándar: envolverla en una función SQL propia marcada IMMUTABLE:
```sql
CREATE OR REPLACE FUNCTION immutable_unaccent(text) RETURNS text AS $$
  SELECT unaccent('unaccent', $1)
$$ LANGUAGE sql IMMUTABLE PARALLEL SAFE STRICT;
```
y usar `immutable_unaccent(...)` en el índice en vez de `unaccent(...)` directo. Requiere
`CREATE EXTENSION IF NOT EXISTS unaccent;` antes. Si la normalización de negocio (dedup por
nombre) usa acentos+mayúsculas, este es el único camino para respaldarlo con un UNIQUE index real.
