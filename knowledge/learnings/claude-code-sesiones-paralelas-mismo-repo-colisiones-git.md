---
title: Claude Code — sesiones paralelas mismo repo causan colisiones git
date: 2026-05-19
source: facturaia auditoría cruzada Sprint 3 (sesión propia + sesión paralela mig 095)
tags: [proceso, git, claude-code, workflow]
---

Dos sesiones Claude Code corriendo simultáneas en el mismo repositorio causan colisiones reales:

1. **Branch switching silente**: cuando una sesión hace `git checkout` o algún hook git cambia HEAD, la otra puede commitear en branch ajena sin darse cuenta. Síntoma: `git log` muestra commit en `fix/X` cuando se esperaba `main`. Fix: cherry-pick a main + verificar.

2. **Colisión naming migraciones**: ambas sesiones eligen el mismo número (ej. `092`). La primera en mergear gana; la segunda debe renumerar. Fix: `ls supabase/migrations/0XX*` **antes** de Write para detectar; usar el siguiente número libre considerando ramas no mergeadas (`git log --all --diff-filter=A -- 'supabase/migrations/0XX*'`).

3. **Commits "desaparecen"**: un hook git (probablemente `post-commit` o auto-rebase) puede rebobinar un commit recién hecho si la otra sesión hizo `git fetch` + reset. Síntoma: `git log` no muestra el commit pero el working tree tiene los mismos archivos modificados. Fix: re-commit con nuevo hash.

4. **Working tree contaminado**: archivos modificados por la otra sesión aparecen en `git status` del propio. Fix: filtrar `git add` explícito por path; NUNCA `git add -A` ni `git add .`.

5. **Merge limpio pero comportamiento cambiado** (2026-06-19): tu PR (basado en main viejo) **auto-mergea sin conflicto** sobre un main donde una sesión paralela **rediseñó el MISMO fichero** (caso: #387 rehízo `integrations-section` de tarjetas→filas mientras yo hacía W1). Git no se queja (hunks disjuntos), pero el render/comportamiento del resultado combinado **NO es el que tú QA'easte** pre-merge. Fix: tras mergear, **re-QA el resultado en main real** (no te fíes de la captura pre-merge); si tu lógica vivía en el diseño viejo, verifica que sigue encajando en el nuevo (`git log --oneline -N <fichero> origin/main` para ver qué tocó la paralela).

6. **Tu cambio sin commitear acaba dentro del commit ajeno** (2026-06-19): la paralela hace `git add -A`/`commit -a` y arrastra tus ficheros modificados-no-staged a SU commit (caso: mi fix de `globals.css` quedó dentro de su `d4a31ad4` "fix(mobile)"). Síntoma: tu `git diff <file>` está **vacío** pero el cambio sí está en el archivo. Confirmar con `git show <hash-ajeno> -- <file>`. No se pierde (vive en su rama); re-aplica el hunk en worktree desde `origin/main` y llévalo a tu PR.

**Checklist defensivo en sesiones paralelas**:
- Antes de commit: `git branch --show-current` (esperar `main` o tu rama). Si no → `git checkout main && git cherry-pick <hash>`.
- Antes de elegir número de migración: `ls supabase/migrations/0XX*` + `git log --all --pretty=format:'%h %s' -- 'supabase/migrations/0XX*'`.
- Stage SIEMPRE explícito: `git add file1 file2 file3`, nunca `-A` / `.`.
- Si un commit "desaparece" tras notificación: verificar con `git log --all --oneline | grep '<keyword>'`. Si está en `origin/<otra-rama>`, ya está; si no, re-commit.

**Síntomas extra en merge (2026-06-11)**: `fatal: Unable to write index` durante `git merge` (índice bloqueado por la otra sesión → reintentar); `MERGE_HEAD` desaparece a mitad → el merge se cierra con `MERGE_MSG` ajeno (asunto equivocado pero padres correctos, verifica con `git show -s --format=%P`); `git push` bloqueado por el gate pre-push con `"Another next build process is already running"` (lock `.next` compartido).

**Patrón de salida limpio**: si `main` divergió Y la sesión paralela está mutando la rama compartida (la contamina con commits ajenos), no pelees el merge in-place — aísla con `git worktree add --detach <tmp> origin/<rama>` + edita/`cherry-pick` + push fast-forward (o `--force-with-lease=<rama>:<oid-esperado>` si reescribes el remoto de una PR contaminada) + PR. Lleva solo tu commit sin arrastrar WIP ajeno.

**GOTCHA — el pre-push compila el WORKING TREE, no tu commit** (2026-06-23): el hook pre-push corre `npm run build` sobre el árbol de trabajo actual; si la paralela dejó código suyo a medias sin commitear, **bloquea tu push limpio** aunque tu commit compile. El worktree aislado es la salida — pero NO le symlinkees `node_modules` (Turbopack peta «Symlink node_modules is invalid», ver [[turbopack-rechaza-symlink-node-modules-en-worktree]]); haz `npm ci` real en el worktree y el build del hook valida de verdad, sin `--no-verify`. Caso 2026-06-23: la paralela pusheó `VIGENTE=true` + un fix ajeno a mi rama de PR y mergeó en main local → respaldo en rama `wip/` + `force-with-lease` del remoto a mi último commit + resto del fix vía worktree+`npm ci`.

**GOTCHA — compound `stash+commit+pop` en un solo bash call** (2026-06-30): si el timeout de Bash corta entre el commit y el `git stash pop`, el stash queda sin restaurar y la rama activa puede haber cambiado silenciosamente. Síntoma: archivos revertidos, commit en rama equivocada, mensaje de commit mezclado con WIP ajeno. Fix: nunca encadenar `git stash push && git add && git commit && git stash pop` en un solo comando; ejecutar en pasos separados confirmando `git status` entre cada uno.

**GOTCHA — `git commit -- <pathspec>` aísla tu commit sin worktree ni `git add`** (2026-06-30): si tus archivos NO se solapan con los de la sesión paralela (sin hunks compartidos en el mismo fichero), no hace falta worktree — `git commit -m "..." -- file1 file2 file3` commitea el contenido actual de esos paths del working tree e ignora cualquier otra cosa ya staged en el índice compartido, dejándola intacta para que la otra sesión la commitee cuando termine. Evita el riesgo de `git add <mis-files>` + `git commit` normal, que sí commitearía TODO lo staged (mezclando su WIP con tu mensaje). Detectar la colisión antes: `ps aux | grep "git commit"` + `git status --short` (columna izquierda `M`/`A` = staged por alguien, puede no ser tuyo).

Caso real TuFacturaIA Sprint 3: 3 colisiones git en una sola sesión (commits en `fix/verifactu-toggle-unify` necesitando cherry-pick a main; renumeración 092 → 093/094/096/097 evitando colisión con `092_verifactu_settings_unify.sql` paralela; commit `d360731` mobile polish desaparecido tras hook, re-commiteado como `1a95e47`). Caso 2026-06-11 (fixes glass /emitidas + switcher): merge fallido por índice + `MERGE_HEAD` perdido + rama compartida contaminada con feature de feedback ajena → salida vía worktree+cherry-pick aislado → PR #206 a main.
