---
title: Una migración con número ya aplicado se salta en silencio, no da error
date: 2026-07-28
source: TuFacturaIA — PR #1310 (578/579 → 580/581)
tags: [supabase, migraciones, postgres, gotcha]
---

`supabase db push` decide qué aplicar **por versión** (el `NNN` del nombre),
no por contenido. Si producción ya tiene registrado ese número por otra rama,
tu migración **no se ejecuta y no avisa**: el push sale en verde.

Caso real: prod tenía `578_feedback_admin_visto_at` y `579_purge_cron_runs...`
de ramas que mergearon mientras otro PR estaba en revisión. Ese PR traía su
propia 578 y 579. Un `db push` habría dado por arreglado un bug vivo
(`change_phone_confirm`) sin haber ejecutado nada.

**Regla**: antes de aplicar, siempre `supabase migration list --linked` y mirar
las filas con `local` vacío y `remote` con número: son versiones que la BD ya
tiene y tu fichero local nunca ejecutará. Y en el repo:

    git ls-files supabase/migrations | grep -oE '/[0-9]{3}_' | sort | uniq -d

El número se ocupa **al mergear**, no al crear la rama. Ver
[[facturaia-migracion-numero-duplicado-536-553]].
