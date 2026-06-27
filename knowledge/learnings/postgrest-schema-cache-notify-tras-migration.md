---
title: postgrest schema cache miss — NOTIFY pgrst tras añadir columna
date: 2026-05-01
source: claude-code-session
tags: [supabase, postgrest, migrations, gotcha]
---

Tras `ALTER TABLE x ADD COLUMN nueva` (o CREATE TABLE / DROP COLUMN), PostgREST puede tardar minutos en refrescar su schema cache. Síntoma asimétrico:

- SELECT funciona (PostgREST lee directo de Postgres)
- INSERT/UPDATE con la columna nueva responde 404 `PGRST204` "Could not find the 'nueva' column of 'x' in the schema cache"

Fix: añadir al final de la migration:

```sql
NOTIFY pgrst, 'reload schema';
```

PostgREST escucha el canal `pgrst` y recarga al recibir notify. Aplica también tras cambios en functions usadas por RPC.

También aplica a **CREATE TABLE** entera: el SELECT falla con *"Could not find the table 'x' in the schema cache"* (no solo INSERT/columna). Es **transitorio tras deploy** (código llega antes que la propagación) y se auto-recupera en minutos. Puede disparar una **falsa alarma 5xx** (caso real `admin/email-copy` ×17, 2026-06-26, tras deploy #527). Antes de "arreglar": verifica si la tabla ya existe y dejó de fallar — probablemente ya está resuelto. Humanizar estas alertas ayuda a no entrar en pánico → [[humanizar-errores-crudos-en-capa-de-render]].

Bug real: migration agency-portal `20260430180000_facturaia_documents.sql` — primeros INSERTs fallaban hasta añadir el NOTIFY.
