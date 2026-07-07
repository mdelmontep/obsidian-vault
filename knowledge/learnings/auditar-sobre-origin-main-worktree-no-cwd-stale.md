---
title: auditar/arreglar en worktree desde origin/main, no sobre el cwd stale (o el hallazgo se infla)
date: 2026-07-07
source: AGH auditoría Tier 1 agente Carlos
tags: [meta, audit, git, worktree]
---
Un audit/workflow corre en el cwd. Si el cwd es una rama por detrás de main, el reporte se INFLA con
lo ya resuelto. En el Tier 1 (cwd 27 commits tras main) 2 de 7 "confirmados" ya estaban arreglados en
main (#217/#226) o ya eran issue abierto (#237) → trabajo duplicado evitable, más ruido a filtrar.

Regla: audita/arregla SIEMPRE en worktree desde origin/main (`git worktree add ../x origin/main`), y
antes de FILAR cada hallazgo dedup contra los issues abiertos (`gh issue list`) + `git log origin/main`.
Si es faceta de un issue existente → coméntalo, no abras uno nuevo. Cruza contra el batch que ya haya
abierto otra sesión (los mismos #NN pueden aparecer dos veces). Ver [[verificacion-adversarial-lentes-triar-por-que-lente-refuta]].
