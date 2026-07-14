---
title: gh pr merge --delete-branch de un PR base cierra (no reapunta) el PR apilado dependiente
date: 2026-07-15
source: claude-code-session
tags: [git, github, gh-cli, stacked-prs]
---
Al mergear PRs apilados (PR1→PR0→main) con `gh pr merge PR0 --delete-branch`, GitHub NO reapunta el PR dependiente al nuevo base: lo AUTO-CIERRA (su base desapareció). Y un PR cerrado cuya base se borró NO se puede reabrir ni reapuntar (`Cannot change the base branch of a closed pull request`) → hay que recrearlo (`gh pr create --base main --head <rama>`; la rama HEAD sigue viva).

Fix: en stacks, reapunta el dependiente ANTES de borrar su base (`gh pr edit N --base main`), o mergea sin `--delete-branch` hasta que todos los dependientes estén reapuntados.

Método: usa merge commits (`--merge`), NO squash, para stacks — squash del base deja sus commits fuera de main y el dependiente muestra su diff duplicado/conflicto. Caso real: vista móvil FacturaIA (#895→#898→#899); #898 se auto-cerró, recreado como #900.
