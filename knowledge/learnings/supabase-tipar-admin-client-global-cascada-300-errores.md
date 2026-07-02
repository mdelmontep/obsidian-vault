---
title: tipar el cliente supabase global es una migración por fases, no una limpieza
date: 2026-07-02
source: claude-code-session
tags: [supabase, typescript, deuda-tecnica, facturaia]
---
`createClient()` → `createClient<Database>()` convierte CADA query en type-checked:
en FacturaIA destapó 341 errores en 135 ficheros (jsonb/Json, null-handling, selects
rotos), incluidos núcleos. Ejecutada 2026-07-02 (PR #648) en ~1 día con este patrón:
1. **Alias tipado incremental**: `createTypedAdminClient()` junto al untyped; migrar
   call-sites dominio a dominio (hoja→núcleo), cada commit con gate verde (el hook
   pre-commit hace incommitteable el big-bang). Flip final: renombrar y borrar alias.
2. Helpers canónicos primero: `zJson`/`zJsonRecord`/`isJsonObject`/`JsonObject`
   (payloads Zod→jsonb, narrowing sin casts) — evita N variantes por dominio.
3. Fan-out de agentes por dominio con catálogo de fixes canónicos + "si el fix cambia
   comportamiento → BLOQUEADO, decisión humana". Los núcleos, con revisión manual.
Bonus real: los `SelectQueryError` destapan bugs de producción — ver
[[supabase-select-columna-inexistente-falla-query-entera-42703]].
