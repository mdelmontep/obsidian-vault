---
title: supabase autoalojado no hace falta entero, y sus seis errores señalan al sitio equivocado
date: 2026-08-11
source: claude-code-session
tags: [supabase, dokploy, docker, postgrest, kong]
---
Para una app que solo usa Postgres+RLS, login y API REST bastan **cuatro** contenedores
(`db`, `auth`, `rest`, `kong`) en vez de los once del compose oficial. Menos RAM y, sobre todo,
menos que se rompa — Realtime es el que llena el disco vía WAL ([[supabase-selfhosted-realtime-roto-slot-replicacion-crece-wal-sin-limite]]).

Los seis fallos del montaje tienen mensajes que apuntan a otro sitio:

| Mensaje | Dónde está de verdad |
|---|---|
| `role "postgres" does not exist` | `supabase/postgres` trae **un solo** rol: `supabase_admin` |
| `must be owner of function uid` | Creaste `auth.uid()` antes que GoTrue; va DESPUÉS de que migre |
| `Invalid authentication credentials` | Kong **no expande variables** en su YAML: registró `$ANON_KEY` literal |
| `No such file or directory` al parsear | El `eval "echo \"$(cat …)\""` del compose oficial hace globbing con los `*` de las rutas |
| `Permission denied` sobre su config | Kong corre como uid **100**, no root |
| Tabla con datos, API devuelve vacío | PostgREST cachea el esquema AL ARRANCAR → event trigger `pgrst_watch` |

`sslip.io` da HTTPS sin tocar DNS. Y comprobar siempre una consulta **con join** al final: una tabla
suelta responde bien con la caché vieja, y el fallo se ve como "no hay datos", no como error.
Montaje completo: `~/Projects/learn-agentesia/CLAUDE.md` §"El aula publicada".
