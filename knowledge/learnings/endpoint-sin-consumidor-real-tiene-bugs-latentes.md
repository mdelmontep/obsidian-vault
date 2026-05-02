---
title: endpoint sin consumidor real esconde bugs latentes hasta primer uso
date: 2026-05-02
source: claude-code-session
tags: [testing, integration, backfill]
---

Un endpoint que pasa lint+typecheck+build y nunca se llamó en producción tiene probabilidad alta de fallar al primer uso real. Los errores típicos:

- Columna referenciada que no existe en la tabla (copy-paste desde un endpoint hermano sin verificar schema). Caso real FacturaIA: `getPresupuesto` pedía `documento_url` que solo existe en `facturas`. Postgres devolvía 42703.
- Field name distinto entre tablas similares (`vto` vs `vence`).
- Validación cliente-side cubre casos que en server fallan distinto.

Patrón operativo: **integrar un nuevo consumidor (backfill, cron, listing UI nueva) ejercita por primera vez rutas dormidas**. Presupuestar ~30 min de fix por cada flow nuevo que conectes. El log del backfill suele dar el bug en línea 1 (`column X does not exist`).

Mitigación a medio plazo: integration tests por endpoint con BD real (Supabase local) — más caros que unit pero atrapan estos. Sin tests, mínimo: smoke curl manual al desplegar cada endpoint nuevo, antes de declararlo "listo".
