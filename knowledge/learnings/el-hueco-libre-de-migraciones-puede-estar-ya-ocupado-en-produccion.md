---
title: el hueco «libre» de migraciones puede estar ya ocupado en producción
date: 2026-08-03
source: claude-code-session
tags: [supabase, migraciones, facturaia, sesiones-paralelas]
---

El 3-ago el repo iba por la 629 y prod tenía aplicadas hasta la **636**, desde un
worktree paralelo sin mergear (obras-095). Es el estado NORMAL cuando se respeta
«migración antes que merge», no una anomalía.

`npm run mig:renumerar` **sí pregunta a la base** desde el 1-ago (#1448):
`max(repo ∪ prod) + 1`, y si no puede leer el remoto avisa fuerte en vez de
callar. Lo di por roto sin abrirlo y avisé de un peligro que no existía; el hub
ya lo decía. Antes de avisar de que una herramienta falla, leerla.

Para ver el rango realmente ocupado:

    supabase migration list --linked   # filas con local:"" = aplicadas sin fichero

Y si `db push` responde *«Remote migration
versions not found in local migrations directory»*, **no ejecutar el
`migration repair --status reverted` que sugiere**: mentiría sobre prod. Copiar
temporalmente (sin commitear) los `.sql` de la sesión paralela deja pasar la
comprobación y solo empuja lo tuyo — confirmar con `--dry-run` que la lista es
exactamente tu fichero.

Segunda trampa, para quien tenga la rama paralela: si renumeran antes del merge,
su SQL **ya aplicado** como 630-636 se reaplicaría con números nuevos.

**Resuelto el 03-ago (obras-095, #1514): NO se renumera.** El script pedía mover
630-636 → 638-644, y su cuenta era correcta: `max(repo ∪ prod) + 1` con el 637 ya
cogido da 638. Lo que su regla no puede saber es que esos ficheros **son** los ya
aplicados: vale para una migración nueva, no para una que ya tiene su número
escrito en `schema_migrations`. Moverlos los dejaría como «sin aplicar» y la
tabla acabaría con **las dos** numeraciones. Lo que hay que comprobar entonces no
es el hueco, sino que la secuencia final no tenga duplicados:

    git ls-files supabase/migrations | grep -oE '/[0-9]{3}_' | sort | uniq -d

Vacío = mergeable tal cual. Aquí quedó 626…637 contigua y se mergeó así.

**Las dos reglas del proyecto chocan, y conviene saberlo:** «el número se asigna
justo antes del merge» presupone que aún no has aplicado; «aplicar a prod antes
de mergear» obliga a lo contrario. Con un PR paralelo colándose en medio no se
pueden cumplir las dos, y manda la BD: el número ya está escrito en prod.

Ver [[dockerfile-que-lista-modulos-uno-a-uno-mata-el-servicio-sin-fallar-el-build]]
