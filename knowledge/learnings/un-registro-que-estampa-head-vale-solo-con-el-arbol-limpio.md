---
title: un registro que estampa HEAD vale solo con el árbol limpio
date: 2026-09-03
source: facturaia
tags: [git, harness, gate, cierre]
---
Un script que apunta «esto se verificó» con `git rev-parse HEAD` escribe el commit ANTERIOR
al trabajo si corre antes de commitear, que es justo cuando se corre un gate. Caso: tres
cierres de tres ramas quedaron con el mismo sha, el `main` del momento (facturaia, 2-sep-2026,
`docs/plan/cierres.json`); el histórico no decía qué se cerró en ninguno y nada avisó.

Fix (PR #2419): el registrador se niega con `git status --porcelain` no vacío, excluyendo el
fichero que él mismo escribe (`:(exclude)<ruta>`), y acepta `--commit <sha>` resuelto con
`rev-parse --verify --quiet <sha>^{commit}` para registrar desde otro estado. La skill pide
commit → registrar → commit propio `chore(cierre)` que el squash absorbe.

Gotcha al testearlo: `git status --porcelain` colapsa un directorio untracked entero en una
línea (`?? docs/`), no lista sus ficheros; para buscar una ruta, `--untracked-files=all`.
Probar el guard con `mutate`: sin él, el test del árbol sucio debe caer.
