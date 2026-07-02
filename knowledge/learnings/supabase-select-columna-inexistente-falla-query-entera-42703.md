---
title: select supabase con columna inexistente falla la query entera y nadie se entera
date: 2026-07-02
source: claude-code-session
tags: [supabase, postgrest, bugs-silenciosos]
---
Una columna inexistente/mal escrita en `.select('a, b, typo')` no degrada: PostgREST
devuelve 42703 y `data` llega **null para toda la query**. Como supabase-js no lanza
y el patrón habitual es `const { data } = await ...` sin mirar `error`, el flujo
"funciona" con data vacía — para siempre.
Casos reales FacturaIA (PR #648, destapados al tipar el cliente): worker VeriFACTU
no-op 6 semanas (columna de una VISTA pedida a la tabla) con cron reportando éxito;
todos los emails con branding fallback (`organizations.web` no existía); endpoint v1
duplicar siempre 404; `is_admin` nunca concedido (upsert a PK equivocada).
Defensas: cliente tipado con `Database` (el typegen convierte esto en error de
compilación, `SelectQueryError`), y para código no tipado: chequear `error` en
queries críticas. Un smoke "endpoint 200" NO lo caza: el 200 sale igual.
