---
title: supabase start en Mac+colima aborta todo el stack si falla el contenedor vector
date: 2026-07-01
source: claude-code-session
tags: [supabase, docker, colima, macos]
---

En macOS con colima (virtiofs), `supabase start` puede fallar así:

```
failed to start docker container "supabase_vector_facturaia": ... mkdir .../docker.sock: operation not supported
```

No es solo una advertencia del servicio de analytics — **tumba todo el stack** (DB, API,
Studio incluidos), aunque el replay de migraciones ya haya terminado bien. Reintentar
`supabase start` o `colima restart` no lo arregla (es un límite del mount virtiofs, no algo
transitorio).

Fix: crear un `supabase/config.toml` temporal (NUNCA commitear, el repo no lo trae por
defecto) con:

```toml
project_id = "facturaia"
[analytics]
enabled = false
```

Con eso `supabase start` levanta DB+API+Storage sin el contenedor `vector` y permite correr
tests de integración reales contra Postgres local. Borrar el archivo al terminar.
