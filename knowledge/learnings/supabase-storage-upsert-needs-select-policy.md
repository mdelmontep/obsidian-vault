---
title: supabase storage upsert requiere policy SELECT aunque INSERT/UPDATE existan
date: 2026-06-12
source: claude-code-session
tags: [supabase, storage, rls, upsert]
---
`storage.upload(path, file, {upsert:true})` hace internamente INSERT + SELECT + UPDATE.
Sin policy SELECT en storage.objects, el SELECT retorna 0 filas → SDK no detecta si el
archivo existe → falla con error RLS aunque INSERT/UPDATE sean correctas.

Síntoma: 403 "new row violates row-level security policy" en upload aunque simular
las policies en SQL dé true y el bucket tenga INSERT/UPDATE correctas.

Fix:
`CREATE POLICY <bucket>_select ON storage.objects FOR SELECT TO authenticated USING (bucket_id = '<bucket>');`

Trampas:
- Borrar SELECT "para evitar listing anónimo" es incorrecto: anon ya no tiene SELECT policy.
  La que se necesita es la de `authenticated` para el upsert interno.
- Para buckets públicos la policy SELECT de auth no expone nada (el contenido ya es
  accesible vía /storage/v1/object/public/ sin auth).
- La policy puede borrarse accidentalmente desde el dashboard de Supabase aunque la
  migración quede marcada como aplicada en schema_migrations.
