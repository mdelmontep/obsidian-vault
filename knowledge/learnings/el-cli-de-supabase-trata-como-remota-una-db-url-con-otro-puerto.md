---
title: el cli de supabase trata como remota una db-url con otro puerto y exige tls
date: 2026-10-15
source: facturaia (PR #3515, CI integration en el runner gates-1)
tags: [supabase, cli, ci, postgres]
---
**Síntoma**: `supabase db push --db-url postgres://…@127.0.0.1:<puerto>/postgres` contra una base local
efímera falla con `server refused TLS connection`, aunque la URL no pida TLS.

**Causa** (CLI 2.109.1): si el puerto de `--db-url` no es el de `config.toml`, el CLI la da por
REMOTA, rehace la URL sin el `sslmode` que trajera y exige TLS. Un Postgres local no lo ofrece.

**Fix**: `PGSSLMODE=disable` en el entorno del proceso que lanza el push (el CLI lo respeta).

**Gotcha previo, mismo CI**: `npx --no-install supabase` sin versión resuelve la que haya en caché o
en `package.json`, no la que fijaste en el workflow; pedía la 2.121.0. Llamar al binario fijado
(o `npx supabase@<versión>`) en TODOS los sitios que lo invocan, no solo en el principal.
