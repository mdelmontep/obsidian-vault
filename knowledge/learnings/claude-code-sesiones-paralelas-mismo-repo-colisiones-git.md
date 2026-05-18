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

**Checklist defensivo en sesiones paralelas**:
- Antes de commit: `git branch --show-current` (esperar `main` o tu rama). Si no → `git checkout main && git cherry-pick <hash>`.
- Antes de elegir número de migración: `ls supabase/migrations/0XX*` + `git log --all --pretty=format:'%h %s' -- 'supabase/migrations/0XX*'`.
- Stage SIEMPRE explícito: `git add file1 file2 file3`, nunca `-A` / `.`.
- Si un commit "desaparece" tras notificación: verificar con `git log --all --oneline | grep '<keyword>'`. Si está en `origin/<otra-rama>`, ya está; si no, re-commit.

Caso real FacturaIA Sprint 3: 3 colisiones git en una sola sesión (commits en `fix/verifactu-toggle-unify` necesitando cherry-pick a main; renumeración 092 → 093/094/096/097 evitando colisión con `092_verifactu_settings_unify.sql` paralela; commit `d360731` mobile polish desaparecido tras hook, re-commiteado como `1a95e47`).
