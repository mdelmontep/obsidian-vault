---
title: postgrest rpc hint revela signature aplicada en prod
date: 2026-05-22
source: claude-code-session
tags: [supabase, postgrest, smoke, debugging]
---

PostgREST devuelve `hint: "Perhaps you meant public.X(arg1, arg2, arg3)"` en 404 `PGRST202` cuando llamas a un RPC con un subset de sus args. Útil para verificar en prod sin acceso psql que una migración con `CREATE FUNCTION` está aplicada y con la signature esperada.

Probe: `POST /rest/v1/rpc/<nombre>` con `{p_uno: "<uuid bogus>"}` + service-role → el hint enumera todos los params reales.

Caso 2026-05-22: confirmé mig 131 `desvincular_asignacion` aplicada (signature `(p_asignacion_id, p_razon, p_user_id)`) en FacturaIA prod sin psql ni Studio. Útil cuando `supabase migration list` confunde por columnas vacías ([[supabase-cli-adoptar-tarde-en-proyecto-con-migrations-aplicadas-por-studio]]).

Tip: usar UUID `00000000-0000-0000-0000-000000000000` como bogus — garantizado fuera de rango, no contamina nada aunque la signature acepte 1 arg.
