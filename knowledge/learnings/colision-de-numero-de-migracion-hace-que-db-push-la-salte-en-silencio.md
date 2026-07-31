---
title: Una migración con número ya aplicado se salta en silencio, no da error
date: 2026-07-28
updated: 2026-07-31
source: TuFacturaIA — #1310 (578/579) · #1384 (595→596→597) · #1388 (596→599)
tags: [supabase, migraciones, postgres, gotcha]
---

`supabase db push` decide qué aplicar **por versión** (el `NNN` del nombre),
no por contenido. Si producción ya tiene registrado ese número por otra rama,
tu migración **no se ejecuta y no avisa**: el push sale en verde y prod se
queda con la función vieja.

El número se ocupa **al mergear**, no al crear la rama — y con 5+ PRs en
paralelo eso ya no basta: el 30-jul el mismo PR (#1384) chocó **dos veces en
unas horas** (595 se lo llevó #1383, luego 596 se lo llevó #1389) y #1388
volvió a chocar con 596. Las tres las cazó el hook `pre-push`, no una revisión.

**Antes de aplicar**: `supabase migration list --linked` y mirar filas con
`local` vacío. En el repo:
`git ls-files supabase/migrations | grep -oE '/[0-9]{3}_' | sort | uniq -d`

**Renumerar a mano se deja referencias fuera** (cabecera `-- NNN_`, marcadores
que comprueban las asserciones, `COMMENT ON FUNCTION`, `RAISE`, tests, docs):
en julio se escapó una en prosa (`la 596 para el resto`) que solo salió al
grepear el diff entero. En TuFacturaIA eso ya es un comando (#1405, 31-jul):

    npm run mig:renumerar -- --dry   # qué haría
    npm run mig:renumerar            # git mv + barrido

Mueve al primer hueco libre, traduce `NNN_slug` / `migNNNtoken` / `mig NNN`, y
**aborta listando lo que no supo traducir** para cerrarlo a mano. Ese último
paso es el valor: la lista de sitios hay que generarla, no recordarla. En otro
repo sin el script, hazlo con `grep` sobre **todos los ficheros del diff**.
Ver [[facturaia-migracion-numero-duplicado-536-553]].
