---
title: Supabase self-hosted — Realtime en bucle roto retiene WAL sin límite vía slot de replicación lógica
date: 2026-07-21
source: claude-code-session
tags: [supabase, self-hosted, postgres, wal, replication-slot, dokploy, disco]
---

Caso Clínica Zen: disco al 90% en el Dokploy del cliente. Causa raíz no era backups
ni logs — un slot de replicación lógica (`cainophile_<sufijo>`, creado por el
contenedor **Realtime** de Supabase) retenía **1.86GB de WAL** de Postgres desde
hacía días. `wal_level=logical` + `archive_mode=off` + `max_wal_size=1024MB` no
importan: un slot activo pero que no avanza (`restart_lsn` congelado) hace que
Postgres NUNCA libere WAL más allá de ese punto, sin importar los límites de
tamaño configurados.

Diagnóstico:
```sql
SELECT slot_name, active, pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS retained
FROM pg_replication_slots;
```
Un `retained` de cientos de MB/varios GB en un slot = la causa, no "hay que ampliar disco".

En este caso Realtime estaba en bucle infinito de reconexión (`docker logs`: "Connection
process starting up" → "Applying migrations" → repetir cada ~5s, sin nunca
estabilizarse) y nadie en el proyecto usaba Supabase Realtime (el RAG del chatbot
n8n usa pgvector/match_documents directo, no la API de Realtime) — mismo patrón que
[[ollama-blueprint-sin-usar-consume-disco]]: pieza de la plantilla nunca usada por
el cliente, pero esta además causa daño activo (crecimiento sin límite) en vez de
solo ocupar espacio estático.

Fix aplicado:
1. `docker stop` el contenedor Realtime (confirmar antes que ningún n8n workflow lo usa).
2. El slot puede quedar "activo" (`active=t`) con el backend aún conectado en Postgres
   aunque el contenedor ya esté parado — verificar `pg_stat_replication` por `pid` y
   `pg_terminate_backend(pid)` antes de poder `pg_drop_replication_slot(slot_name)`
   (si no, error "replication slot ... is active for PID").
3. `CHECKPOINT;` manual tras borrar el slot para liberar el espacio YA, sin esperar
   al ciclo natural de checkpoint.

Gotcha adicional: Supabase self-hosted tiene **más de un** componente con su propio
slot de replicación lógica (Realtime Y Logflare/analytics, cada uno `cainophile_*`
con sufijo aleatorio). No asumir que solo hay uno — listar `pg_replication_slots`
completo y comprobar cada slot por separado (`retained` estable en el tiempo = sano,
creciente = roto). En este caso el slot de Logflare estaba sano (158kB estables)
y no se tocó.

Aviso de persistencia: `docker stop` no sobrevive a un **redeploy** del stack desde
Dokploy (recrea todos los servicios del compose, incluido Realtime) — si se quiere
eliminar de forma permanente hay que quitarlo del `docker-compose.yml` del stack,
cambio de aplicación explícito que no se hizo aquí.
