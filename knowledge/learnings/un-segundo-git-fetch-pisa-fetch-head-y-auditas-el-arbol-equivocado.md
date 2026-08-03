---
title: un segundo git fetch pisa FETCH_HEAD y auditas el árbol equivocado
date: 2026-08-03
source: claude-code-session
tags: [git, verificacion, code-review]
---

Auditando una PR: `git fetch origin <rama-pr>` y luego greps contra `FETCH_HEAD`. A mitad de la revisión, `git fetch origin <otra-rama>` para comparar → **`FETCH_HEAD` pasó a apuntar a la otra rama** y todas las comprobaciones posteriores midieron el árbol equivocado.

Resultado concreto: reporté que un arreglo pedido «no se había hecho» y que la rama tenía un solo commit. Las dos cosas eran de la rama vieja; en la PR real el arreglo estaba y bien documentado. Es el peor tipo de error de review: **da un falso negativo con toda la apariencia de evidencia** (hay un `file:line` detrás).

Regla: en una auditoría de más de un `fetch`, no usar nunca `FETCH_HEAD`. Usar la ref remota explícita, que es estable:

```
git fetch origin && git grep -n "<patrón>" origin/<rama> -- <ruta>
git log --oneline origin/main..origin/<rama>
```

Señal de alarma: si el `git show --stat` de la rama no cuadra con el `+N/-M` que reporta `gh pr view`, no es que la PR mienta — es que estás mirando otro commit.

Ver [[rama-nueva-desde-un-main-local-sin-fetch-revierte-trabajo-ajeno]]
