---
title: Una migración con número ya aplicado se salta en silencio, no da error
date: 2026-07-28
updated: 2026-09-07
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
repo sin el script, hazlo con `grep` sobre **todos los ficheros del diff** — y si el barrido
lo haces con `sed`, verifica por grep que cambió algo: BSD `sed` ignora `\b` en silencio y
sale en verde sin tocar nada ([[macos-shell-bsd-sed-label-una-linea-y-while-read-ultima-linea]]).
Ver [[facturaia-migracion-numero-duplicado-536-553]].

**La misma trampa vive en la base de pruebas COMPARTIDA** (7-sep-2026). El
pre-vuelo del `pre-push` la declaró `CON_ESQUEMA_AJENO`: tenía aplicadas 6
migraciones que no están en `origin/main` ni en el disco de ninguna rama viva
—las últimas, **995 a 999**—, huérfanas de una sesión que ya no existe. Numerar
ahí no da error: esa base daría tu migración por aplicada, **no la ejecutaría**,
y tu gate saldría verde midiendo un esquema sin tu cambio. Y no se limpia: la
instancia es una sola para los once worktrees, así que `db reset` se las quita
también a quien esté en verde ahora mismo. **Y el susto no se hereda a producción**: el máximo aplicado en prod ese día
era el **868**, sin ningún 99x. Merece decirlo porque las dos sesiones que
lo miramos enunciamos primero el dato de la base local como si fuera de prod.
Se esquiva numerando con `mig:renumerar`, que sí consulta prod, nunca a mano
mirando el hueco más alto.
