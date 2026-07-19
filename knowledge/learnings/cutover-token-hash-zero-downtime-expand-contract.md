---
title: cutover de columna en claro → hash sin caída = expand-contract (conservar columna + trigger + DROP diferido)
date: 2026-07-19
source: claude-code-session
tags: [supabase, migraciones, seguridad, deploy]
---
Migrar un bearer token de `token` en claro a `token_hash` en un solo PR (migración
que hace `DROP token` + código que lee solo `token_hash`) es un cutover destructivo:
código-viejo+esquema-nuevo y código-nuevo+esquema-viejo son mutuamente incompatibles
→ ventana de 500s durante el deploy (el deploy va acoplado al merge, no lo puedes
sincronizar con el `db push`).

Fix zero-downtime (expand-contract), sin tocar el código nuevo:
- La migración CONSERVA `token` (pásalo a nullable) y añade `token_hash` + backfill.
- TRIGGER `BEFORE INSERT/UPDATE` que rellena `token_hash` desde `token` → los inserts
  del código VIEJO (que aún escribe `token`) siguen cumpliendo `token_hash NOT NULL`.
- El código nuevo escribe `token_hash` directo (token NULL); el trigger no lo pisa.
- Índice único parcial sobre `token WHERE token IS NOT NULL` para mantener su unicidad.
- El `DROP token` (crypto-erase) se DIFIERE a una migración posterior gated (B2), cuando
  ya nadie lee el plano. Viejo lee token, nuevo lee token_hash → coexisten, cero caída.

Ojo: si la app NUNCA lee la columna directamente (solo la toca vía RPC), la migración ya
es zero-downtime aunque anule/mueva el plano (caso phone_change_revoke_tokens: insert por
RPC + revoke por RPC → nadie hace `.eq('token',…)`). El problema es solo cuando hay
`.eq(columna_plana, …)` en código vivo. Ver [[schema-migrations-no-es-source-of-truth-si-aplicas-manual]].
