---
title: un required status check en estado FAILING bloquea el merge incluso con admin/API
date: 2026-07-08
source: claude-code-session
tags: [github, ci, branch-protection]
---
`gh pr merge --admin` y la API REST (`PUT .../merge`) SÍ saltan un required check que está
"pending"/"no arrancó" (caso típico: Actions caído por billing), pero si el check corrió y
terminó en **failing** de verdad, ni `--admin` ni la API lo saltan — error 405 "Required status
check is failing". Solo el botón "Merge without waiting for requirements to be met" de la UI web
(y solo si el usuario tiene permiso de bypass) lo evita.

Diferencia clave: "not started"/"pending" (billing caído) vs "failing" (corrió y falló) son dos
estados distintos para branch protection, aunque ambos se vean en rojo en la UI de checks.

Fix si el fallo es un falso negativo conocido (p. ej. billing): verificar con
`gh run view <id>` que el job es "not started because recent account payments have failed" antes
de asumir que --admin bastará — si ya corrió y falló, hay que mergear desde la UI con el permiso
adecuado, no insistir por CLI.
