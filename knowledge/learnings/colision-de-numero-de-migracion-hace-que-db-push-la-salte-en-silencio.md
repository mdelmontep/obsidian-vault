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

**Al renumerar barre TODAS las referencias, no solo el nombre del fichero**:
cabecera `-- NNN_`, marcadores internos que comprueban las asserciones
(`mig595palabras`), `COMMENT ON FUNCTION`, mensajes de `RAISE`, comentarios de
cabecera de rutas, nombres de tests y `gotchas.md`. Una se escapó y solo salió
con `grep` sobre **todos los ficheros del diff**, no sobre los sitios que uno
recuerda. Ver [[facturaia-migracion-numero-duplicado-536-553]].
