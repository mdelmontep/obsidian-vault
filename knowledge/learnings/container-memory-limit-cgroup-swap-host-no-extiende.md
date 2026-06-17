---
title: límite memory de un contenedor es techo de cgroup; el swap del host no lo extiende
date: 2026-06-17
source: claude-code-session
tags: [docker, dokploy, oom, ci, runner]
---
Un contenedor con `deploy.resources.limits.memory: 3G` tiene un techo de cgroup DURO.
Añadir swap al HOST no sube ese techo (haría falta subir el memswap del contenedor). Un
`npm run build` (pico 2-3G) lo OOM-killea aunque el host tenga swap de sobra.

Corolario de diseño: si CI ya corre el build en cada PR (y el bot no puede mergear sin
review), repetir el build dentro de un gate con poca RAM es redundante y solo produce
falsos fallos. Caso real (runner "Resolver con Claude", #354): el build del gate
OOMeaba → TODO PR salía en draft con "Gate FALLÓ" pese a estar verde en CI. Fix: gate =
lint+typecheck; CI = gate autoritativo del build.

Y siempre captura stdout/stderr del gate: "FALLÓ" sin log no es diagnosticable.
Ver [[runner-headless-git-push-dispara-pre-push-hook]].
