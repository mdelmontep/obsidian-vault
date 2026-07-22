---
title: git commit sin add previo commitea el index (staged), no el working tree
date: 2026-07-22
source: claude-code-session
tags: [git, gotcha]
---

Si algo (un subagente, un intento anterior) ya hizo `git add -A` y luego
falló/fue matado antes de terminar el commit, el índice se queda con ESA
versión staged. Si después arreglas el archivo en el working tree (vía Edit)
y confirmas con `npm run lint` en standalone (lee working tree, pasa limpio),
pero luego solo corres `git commit -m "..."` (sin `-a` ni un `git add`
nuevo), el commit resultante contiene el índice VIEJO, no tu fix — aunque el
lint standalone diera verde (linteaba el working tree, no lo que se
commiteó).

**Síntoma**: tras el commit, `git status` sigue mostrando el archivo como
modificado — significa que el working tree difiere del HEAD recién
commiteado, y lo que se commiteó fue la versión pre-fix.

**Fix**: tras cualquier edición posterior a un `git add`, vuelve a `git add
-A` (o `git commit -am`) antes de commitear — nunca asumas que "ya está
staged" solo porque un intento anterior lo dejó así. Verificar con `git diff
HEAD -- <archivo>` tras el commit si hay dudas: vacío = lo commiteado
coincide con el working tree.
