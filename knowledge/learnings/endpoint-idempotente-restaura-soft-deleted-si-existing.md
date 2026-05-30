---
title: endpoint POST idempotente restaura soft-deleted en vez de "ya existe"
date: 2026-05-30
source: claude-code-session
tags: [arquitectura, soft-delete, idempotencia]
---

Cuando una entidad tiene soft-delete (`archivado_at`/`deleted_at`) y
existe un endpoint de alta idempotente por clave de negocio (NIF,
email, sku), 3 caminos de respuesta — no 2:

- `status:'created'` — no existía, INSERT.
- `status:'restored'` — existía archivado, `UPDATE … SET deleted_at = NULL`.
- `status:'existing'` — existía activo, no toca.

La intención del caller al pedir alta de un identificador que estaba
archivado es claramente reactivar. Devolver `'existing'` confunde
(usuario no lo ve en su lista). Devolver `'created'` rompe la
unicidad. Restaurar es el path correcto.

Aplica también a importadores CSV, sync external systems, formularios
upsert. El payload debe incluir además los datos del existente para
que el caller pueda mostrar al user el nombre real (caso fantasma:
mismo NIF/clave pero distinto nombre del que esperaba).

Caso real TuFacturaIA: `/api/internal/voice/clientes/crear` (PR #115).
