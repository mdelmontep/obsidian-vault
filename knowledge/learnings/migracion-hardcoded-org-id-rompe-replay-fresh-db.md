---
title: insert con uuid literal de org de prod en una migración rompe el replay en BD fresca
date: 2026-07-01
source: claude-code-session
tags: [supabase, migraciones, ci, postgres]
---

Un `insert into org_features (...) values ('<uuid-prod>', ...)` sin guarda, referenciando
un org_id hardcodeado de producción, funciona en prod (donde el org existe) pero rompe
`supabase db reset`, CI (fresh DB) y onboarding de un dev nuevo: viola la FK
`org_features_org_id_fkey` y **aborta el replay completo de migraciones ahí mismo** —
todas las migraciones posteriores quedan sin aplicar en ese entorno, no solo la fila.

Caso real: mig 400 de TuFacturaIA abortaba el job `integration` de CI desde el 17/06,
enmascarado porque además Actions llevaba bloqueado por billing (nadie vio el log real).

Fix: guardar con `where exists (select 1 from organizations where id = '<uuid>')`. En
prod el resultado es idéntico (el org existe); en BD fresca el insert se salta sin error.

Relacionado: [[grandfathering-snapshot-antes-de-reempaquetar-planes]].
