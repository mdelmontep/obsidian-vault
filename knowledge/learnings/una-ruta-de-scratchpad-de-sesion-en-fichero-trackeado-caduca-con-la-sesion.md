---
title: una ruta de scratchpad de sesión en un fichero trackeado caduca con la sesión
date: 2026-09-11
source: facturaia
tags: [tests, gates, claude-code, worktrees]
---
`qa-funcional.test.ts` clavaba como raíz de sus temporales la ruta absoluta del
scratchpad de una sesión de Claude Code (`/private/tmp/claude-501/…/<uuid>/scratchpad`).
Funciona mientras esa sesión existe. **El primer reinicio del Mac vacía `/private/tmp`**
→ `mkdtemp` da ENOENT → 20 casos rojos.

El daño no se queda en su fichero: como el pre-push corre `npm run test`, **bloquea el
push de CUALQUIER rama**, con un error que no nombra ni al reinicio ni a la sesión y que
parece un fallo de quien no ha tocado nada. Dos sesiones lo diagnosticaron a la vez sin
saberlo (#2719 duplicó al #2721).

Patrón: **estado de máquina o de sesión —uuid, pid, cwd, puerto, scratchpad— nunca en un
fichero trackeado.** La raíz la da el SO: `mkdtempSync(join(tmpdir(), 'x-'))`.
Detección: `grep -rln "claude-501" --include="*.ts" --include="*.mjs"`.
Ver [[el-suelo-de-un-semaforo-explica-quien-entra-no-cuanto-tarda]].
