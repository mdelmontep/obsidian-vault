---
title: CREATE OR REPLACE revierte un ALTER FUNCTION ... SET search_path anterior
date: 2026-08-06
source: claude-code-session facturaia
tags: [postgres, supabase, migraciones, extensions, search-path]
---

`CREATE OR REPLACE FUNCTION` conserva los GRANT pero **NO** conserva el
`search_path`: el que vale es el que declara el nuevo cuerpo. Si una migración
anterior lo ajustó con `ALTER FUNCTION … SET search_path`, reescribir la función
copiando la cabecera de su versión original **deshace ese ALTER en silencio**.

Caso TuFacturaIA (mig 642 sobre la 547): la mig 581 añadió `extensions` al
search_path de `calcular_score_match_doc` porque el cuerpo llama a
`word_similarity` sin cualificar y pg_trgm vive en `extensions`. La 547 declaraba
`SET search_path = public`. Copiar esa línea habría dejado `word_similarity` sin
resolver **dentro de un trigger de conciliación** — falla en runtime, no al aplicar.

- Antes de un `CREATE OR REPLACE`, leer el estado REAL, no el fichero anterior:
  `SELECT proconfig FROM pg_proc WHERE proname='…'` en el entorno donde vive.
- Y contrastar que el cuerpo local es el que está desplegado antes de partir de él:
  `md5(prosrc)` contra el md5 del bloque `AS $$ … $$` del fichero.
- La verificación de la migración debe abortar si `extensions` (o lo que fuera) no
  está en el `proconfig` resultante. Un guard que solo mira que la función existe
  no ve esta regresión.

Relacionado: [[pgcrypto-supabase-trigger-search-path]] ·
[[postgres-revoke-public-no-elimina-grants-individuales]]
