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

**Fix corto (preferido, medido 22-ago): `npx supabase start -x vector`.** Un flag, nada que
crear ni borrar. Se pierden Studio→Logs y `supabase logs`, que no hacen falta para la suite.

**Y cuidado con el diagnóstico**: al fallar, `supabase start` hace `Stopping containers...` y tira
el stack, así que el error se lee como «no arranca la base local» cuando las migraciones habían
pasado ENTERAS y había llegado al `seed`. Eso mandó al issue #1919 de TuFacturaIA cuatro días con
una causa falsa («la mig 643 aborta»). Antes de culpar a una migración, buscar el `vector` al final
del log.

Fix alternativo (si además molesta analytics): `supabase/config.toml` con
`[analytics] enabled = false`. En TuFacturaIA ya existe uno commiteado (`project_id = "fia-dbtest"`,
puertos 544xx), así que el «el repo no lo trae» de la versión vieja de esta nota ya no aplica.
