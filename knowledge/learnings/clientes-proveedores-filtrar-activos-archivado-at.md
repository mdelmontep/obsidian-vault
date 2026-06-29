---
title: clientes/proveedores: filtrar activos con archivado_at IS NULL, no activo=true
date: 2026-06-29
source: claude-code-session
tags: [supabase, postgrest, facturaia, soft-delete]
---

`clientes` y `proveedores` NO tienen columna `activo` booleana.
Mig 190 añadió `archivado_at timestamptz`: NULL = activo, NOT NULL = archivado.

Filtro correcto en PostgREST / Supabase client:
`.is('archivado_at', null)`

`.eq('activo', true)` → error 400 silencioso (columna inexistente, data=null).

Índices parciales ya creados sobre esta condición exacta:
`clientes_org_activos_idx` y `proveedores_org_activos_idx` → úsalos en WHERE.

Caso real: `listarClientes.ts` copiloto — usaba `.eq('activo', true)`, fallaba
en runtime con error "hubo un problema" mientras el tool parecía pasar.
Fix: sustituir por `.is('archivado_at', null)`.

Ver también [[endpoint-idempotente-restaura-soft-deleted-si-existing]].
