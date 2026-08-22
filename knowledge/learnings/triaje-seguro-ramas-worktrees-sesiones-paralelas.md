---
title: triaje seguro de ramas y worktrees con sesiones paralelas
date: 2026-06-12
source: claude-code-session
tags: [git, worktrees, housekeeping, agentes-paralelos]
---

🚫 **`[ahead N]` NO es evidencia de nada** (7-ago, AGH): mide contra el upstream de ESA rama
(`origin/<rama>`), no contra `main`. Con rebase-antes-de-mergear, una rama mergeada queda casi siempre
«ahead» de su propio remoto —el remoto se rebasó durante la review y tu copia local guarda los commits
pre-rebase—. Reporté «trabajo sin empujar, se puede perder» en 11 ramas y **lo rescatable era CERO**. Lo
caro no es el trabajo perdido: es la falsa alarma que manda a auditar ramas de hace un mes.

Rama es borrable si **cualquiera** de estas da vacío (evidencia, no fecha):
- `git cherry origin/main rama | grep '^+'` → 0 (patch-equivalente). ⚠️ **Fiable solo si el repo mergea
  con merge commit o rebase**; con **squash** da falsos `+` masivos (37 de 85 en facturaia) porque N
  commits colapsan en uno y ningún patch-id casa → [[tres-puntos-y-git-cherry-mienten-en-ramas-squash-mergeadas]].
  Mirar la estrategia del repo antes de fiarse: en AGH (merge commits) el embudo 79→28→15→5→**0** salió limpio.
- `git diff origin/main rama -- <paths que toca>` vacío (contenido mergeado por otra vía aunque cherry marque `+`) — **el único inmune a la estrategia de merge**
- lo más barato con muchas ramas: `gh pr list --state merged --limit 400 --json headRefName` una vez y cruzar con `comm`. Un PR mergeado es prueba directa; 43 ramas en un `comm` en vez de 43 comprobaciones.

**El comando `clean_gone` (repo de comandos propio) NO es seguro tal cual** (3-ago): hace `git branch -D` sobre TODAS las `[gone]` y `git worktree remove --force` de sus worktrees. Ese día una `[gone]` (`chore/types-obras-irpf`) estaba checkouteada en el worktree de otra sesión → le habría borrado el directorio con su WIP. Y `git branch --merged origin/main` daba **0 de 44** por el squash, así que ni siquiera servía como guarda. Usar la evidencia de arriba + saltar toda rama que aparezca en `git worktree list --porcelain`.

Worktree con lock: leer el PID del mensaje de error y `ps -p <pid>` — si está muerto, el lock es huérfano y `git worktree remove -f -f` es seguro. Nunca forzar con PID vivo (sesión/agente activo).

Gotcha: un hook pre-push que corre `build` bloquea **hasta los `push --delete` de ramas** si hay un build paralelo (lock `.next/lock`). Ahí `--no-verify` está justificado (el build es irrelevante para borrar una ref).

Rescate si una paralela hizo `git stash` (con nombre) + checkout a otra rama: tus cambios a ficheros **tracked** están en el stash; tus ficheros **nuevos untracked** siguen en el working tree. Sin tocarla: `git worktree add <dir> <tu-rama>` → `git stash apply stash@{N}` → copia los untracked nuevos al worktree → `npm install` (NO symlink, [[turbopack-rechaza-symlink-node-modules-en-worktree]]). Commit ajeno en tu rama: `reset --mixed <tip-bueno>` + `checkout <tip> -- <sus ficheros>` (su commit sigue vivo en su rama).

Regla 2 semanas: lo retomable → pointer en hub antes de borrar; lo demás se va.

**Worktree ajeno con commits propios, aunque verifiques que los ficheros a tocar están intactos** (2026-07-06): el clasificador de seguridad de Claude Code bloquea `cp`/escritura ahí sin confirmación explícita del usuario — "verificado con git diff" no basta como justificación. Si el usuario no responde a tiempo, no forzar: rama/PR separado que referencie el original en la descripción es la salida segura y reversible (fusionar después si se quiere consolidar).

**Ancestría ≠ borrable: mirar SIEMPRE `git -C <worktree> status` antes de retirar** (2026-07-18): una rama "0 commits ahead" o `merge-base --is-ancestor rama main` = SÍ puede tener WIP **sin commitear** en su worktree. Casi borro 25 ficheros activos de `feat/modulo-obras-wapi` porque la ancestría decía "mergeada". El commit-ancestry solo habla de commits; el working tree es otro eje. Regla: worktree se retira solo si `status` vacío **y** rama borrable por [cherry/diff]. Ídem al final: tras merge+push, `git worktree remove` + `git branch -d` (falla solo si queda WIP).

**El stash es COMPARTIDO entre worktrees** (2026-07-27): el rescate descrito arriba tiene su cara B — otra sesión puede recuperar tu stash y dejarte sin fix, con su rama contaminada. Detalle y reglas en [[stash-es-compartido-entre-worktrees-y-rompe-sesiones-paralelas]].

**El dashboard del semáforo de CPU delata a la paralela ANTES de que exista rama remota o PR** (2026-08-22): `git worktree list` la ve solo si el worktree está registrado en tu repo, y `gh pr list` no la ve hasta que abre PR. `node ~/.claude/gate/gate-dash` sí: pinta worktree + rama de cada gate en cola o corriendo. Así descubrí que otra sesión llevaba el mismo fix del test rojo de `main`, ya en typecheck mientras el mío esperaba lint — retiré el duplicado y su PR (#2094) cerró el rojo. Mirarlo antes de arrancar un fix de algo que se ve desde main (test roto, warning de build) es más barato que descubrirlo al abrir el PR.
