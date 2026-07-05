---
title: langfuse v3 self-host — gotchas de deploy (traceId, clickhouse RAM, headless init)
date: 2026-07-05
source: claude-code-session
tags: [langfuse, observability, clickhouse, dokploy]
---
Langfuse v3 self-host = 6 servicios obligatorios (web + worker + postgres + clickhouse + redis + minio):

- **Ingesta**: un `event-create` SIN `traceId` NO crea traza en v3 (queda huérfano/ignorado → 0 trazas). Para que aparezca: `trace-create` con `traceId` (turno = traza). Verificar contra la instancia real (`POST /api/public/ingestion`, Basic pk:sk), no fiarse del payload.
- **ClickHouse RAM**: es hambriento. En box pequeño capar con `<max_server_memory_usage>` EXPLÍCITO en bytes (config.d), NO `max_server_memory_usage_to_ram_ratio` — el ratio puede calcularse sobre la RAM del HOST, no del cgroup → OOM-loop.
- **web (Next.js)**: `HOSTNAME=0.0.0.0` + `NODE_OPTIONS=--max-old-space-size` alineado al `mem_limit` (Node no lee el cgroup → OOM). Ver [[next-js-standalone-hostname-bind]].
- **Headless init** (`LANGFUSE_INIT_*`): idempotente POR EXISTENCIA — si el usuario/proyecto ya existe NO lo actualiza (cambiar solo la password en env no sirve; cambiar el email crea uno nuevo). Sin comillas dobles en los valores.
