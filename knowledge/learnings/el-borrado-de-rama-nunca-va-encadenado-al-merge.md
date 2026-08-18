---
title: el borrado de rama nunca va encadenado al merge — corre aunque el merge aborte, y cierra la PR
date: 2026-08-18
source: claude-code-session agh-iberica
tags: [github, gh-cli, git, metodo, prs-apiladas]
---
Un `&&` entre «mergear» y «borrar la rama» destruye el trabajo justo cuando el detector funciona.

Medido (AGH #1347). Un solo comando hacía: contar ficheros del diff → mergear si cuadra → `git push origin --delete`. **El contador funcionó y abortó el merge** (declaraba 5 ficheros, el diff traía 4), pero el borrado venía detrás **sin estar condicionado** y corrió igual. Borrar la rama **CIERRA la PR y no se puede reabrir** («su base ya no existe»): se perdieron el cuerpo y el hilo de revisión. Segunda vez en una semana (#1120).

- El paso «contar antes de mergear» existe para **abortar**. El detector y la acción destructiva no pueden vivir en la misma invocación.
- Un `[ "$n" = "$esperado" ] && merge` **no** protege las líneas siguientes: solo el merge. Si hay que agrupar, `if … else exit; fi` con el destructivo DENTRO del `then`.
- El borrado de ramas es un **paso aparte al final de la tanda**, cuando ninguna es base de nada y **después** de comprobar que el merge ocurrió.
- Remedio si ya pasó: `git reflog` → `git branch <nueva> <sha>` → push → **PR nueva**. La original no se reabre.
- Y **el número declarado sale del diff, no de la memoria**: `git diff --name-only <base>..HEAD | wc -l`. Dos fallos en dos días por contar la unidad equivocada (un `.txt` de golden no contado; **sitios** contados como **ficheros**).

Hermanos por el mismo comando: [[gh-pr-merge-delete-branch-no-borra-la-rama-si-falla-su-checkout-local]] · [[gh-pr-merge-no-confirma-verificar-state-merged]] · [[gh-borrar-base-de-pr-apilada-cierra-la-hija-irreversible]] (mismo daño, mecanismo distinto: allí desaparece la base de OTRA PR; aquí la rama de la propia) · [[rebase-onto-pr-stackeada-squash-no-duplicar]]
