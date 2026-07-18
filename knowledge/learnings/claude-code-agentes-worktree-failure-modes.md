---
title: Claude Code agentes worktree — failure modes y cómo blindarlos
date: 2026-05-23
source: sesión PR-PSD2-3.3/3.4 + PR-A4 + PR-B-anomalías paralelos
tags: [claude-code, agentes, worktree, multi-agent, gotchas]
---

# Agentes worktree-aislados — 3 failure modes que vi en una sesión

Lancé 3 agentes en paralelo (`isolation: worktree`) sobre el mismo repo. Resultado: 1 entrega limpia, 1 con conflicto de merge, 1 murió sin commitear. Aprendizajes para futuras tandas multi-agente.

## Failure mode A: agente muere sin notif completion, deja cambios unstaged en working tree del repo principal

**Síntoma**: lanzo agente con `isolation: worktree`. Pasan 50+ min. Output file (`/private/tmp/claude-501/.../tasks/<id>.output`) deja de crecer. No llega notificación de completion ni de fallo. `ps -ef` no muestra procesos vivos. El branch del worktree (`worktree-agent-<id>`) no tiene commits propios — HEAD apunta al commit base previo.

**Lo sutil**: `git status` en el repo PRINCIPAL muestra los archivos modificados sin staged. El agente trabajó pero algo en la harness lo killó antes de hacer el commit final, dejando los cambios al aire.

**Diagnóstico**:
```sh
# Output file no crece desde hace tiempo
stat -f "%Sm" /private/tmp/.../tasks/<id>.output

# Worktree no tiene commits propios encima del base
cd .claude/worktrees/agent-<id> && git log --oneline -3

# PERO el working tree principal SÍ tiene cambios
cd repo_principal && git status --short
```

**Fix**: revisar el diff de los archivos modificados a mano (`git diff <paths>`), si la lógica está bien y los tests pasan, commitear tú con autoría compartida. Si está roto, `git checkout HEAD -- <paths>` y relanzar.

**Cómo blindar**: en el prompt del agente, exigir explícitamente "haz commit DENTRO del worktree con `git commit -m` antes de devolver resultado, NUNCA dejes cambios unstaged". Aún así puede fallar la harness, pero al menos sabes qué cambios pretendía hacer.

## Failure mode B: agente forka worktree de main desfasado, diff masivo contra HEAD actual

**Síntoma**: agente entrega commit propio en su worktree branch, pero al hacer `git diff main <worktree-branch> --stat` aparecen 60+ archivos modificados, muchos NO relacionados con el PR del agente — son archivos que cambiaron en main MIENTRAS el agente trabajaba (otros PRs paralelos del mismo repo).

**Causa raíz**: la harness crea el worktree haciendo checkout del HEAD de main en el momento del lanzamiento. Si main avanza durante la ejecución del agente (por commits tuyos o de otras sesiones), el worktree queda anclado al HEAD viejo. Si haces `git merge worktree-branch` o `git rebase`, traes diff de TODO lo que cambió en medio (revertiendo commits ajenos).

**Fix**: cherry-pick selectivo por paths del PR, NO merge entero:
```sh
git checkout <worktree-branch> -- \
  'src/lib/feature-x/' \
  'src/app/api/feature-x/' \
  'src/components/feature-x.tsx'
# Verificar git status no incluye archivos ajenos
# Commit con autoría compartida
```

**Cómo blindar**: en el prompt del agente, lista explícita de paths que SÍ debe tocar + paths que NO. Después del commit verificar `git diff main HEAD --stat` y si hay archivos fuera del scope esperado, descartar el merge entero y cherry-pick selectivo.

## Failure mode C: dos agentes paralelos tocan el mismo archivo (colisión silenciosa)

**Síntoma**: agente A escribe `src/lib/modules/catalog.ts` para añadir un setting. Agente B (otro PR no relacionado) edita el MISMO archivo para reescribir la descripción de otro módulo. Al mergear los dos worktrees, los hunks se solapan o uno pisa el otro sin warning.

**Causa raíz**: archivos "junk drawer" (catálogos, registries, archivos config grandes) atraen ediciones de muchos PRs distintos. Sin coordinación, los agentes se pisan.

**Fix**: hacer `git add --patch <archivo>` con hunks selectivos, commitear solo los míos. Los ajenos quedan unstaged para que su dueño los recoja después.

**Cómo blindar**: identificar los archivos "junk drawer" del repo (catálogos, registries) y mencionarlos en el prompt del agente: "si tocas `src/lib/modules/catalog.ts`, edita SOLO la entrada relevante a tu PR — no toques otras descripciones aunque las veas obsoletas".

## Failure mode D: subagente read-only lee el checkout PRINCIPAL, no el worktree manual

**Síntoma**: trabajo en un worktree manual (`/repo-feature`, rama con N slices ya commiteadas). Lanzo un **Explore** (read-only, sin `isolation:worktree`) para mapear patrones. Devuelve firmas/funciones que NO coinciden con lo que tengo: es la versión del **checkout principal** (`/repo`, sin mis slices) → mapa STALE para paths que existen en ambos.

**Causa**: el subagente resuelve rutas contra el cwd del proceso (repo principal), no contra mi worktree. Para archivos compartidos lee la copia equivocada sin avisar.

**Fix**: (1) en el prompt, ruta ABSOLUTA del worktree + "es un worktree, NO el repo principal; NO leas `/repo`". (2) Re-verifica claims críticos (firmas, auth) leyendo el worktree tú mismo — los del subagente no se heredan. Caso real 2026-06-18 (MCP slice 050): el Explore reportó `withApiV1`/endpoints pre-044 del repo principal.

## Failure mode E: OTRA sesión (no un agente mío) edita el mismo working tree principal mientras trabajo

**Síntoma**: trabajando en el repo principal (sin worktree), aparece un archivo nuevo que no creé (ej. una migración SQL de otra feature) entre dos de mis propios commits. No es un agente que lancé — es otra sesión Claude Code (o humana) usando el mismo checkout en paralelo.

**Diagnóstico**: `git worktree list` + comparar mtimes de archivos sospechosos contra el timeline de mi sesión. Si el archivo no encaja con nada que yo haya tocado, es trabajo ajeno concurrente.

**Fix**: no seguir editando el principal. Crear worktree propio desde `origin/main` (`git worktree add <path> -b <rama> origin/main`), copiar a mano los archivos de MI trabajo en curso al nuevo worktree, y revertir/limpiar el principal (`git checkout -- <mis-archivos>`, borrar mis archivos nuevos) para no interferir con la otra sesión. Symlink `node_modules` desde el principal en vez de reinstalar (ojo: Turbopack/`next build` rechaza el symlink, `tsc`/`vitest` no — usar `npm install` real si necesitas `next build` en el worktree).

**Cómo blindar**: antes de empezar trabajo largo en el checkout principal (no en un worktree), `git worktree list` + revisar si hay señales de actividad reciente ajena (archivos modificados con mtime fresco que no son míos) en el `git status` inicial.

## Failure mode F: `fork` (hereda contexto completo) se va meta y se cuelga en features grandes

**Síntoma**: para implementar una feature grande multi-dominio (db+backend+frontend) lancé UN `subagent_type:"fork"` (hereda todo mi contexto). A los 600s: watchdog "no progress", murió sin crear siquiera el worktree. Su mensaje final mostraba al fork investigando su PROPIO árbol de agentes (mencionaba un sub-subagente que había generado) en vez de implementar → se fue meta.

**Causa raíz**: un fork con contexto enorme heredado + tarea grande tiende a razonar sobre la orquestación (incluso a re-delegar) en vez de ejecutar; más superficie para colgarse en el stream.

**Fix**: para features grandes de implementación, hazlas TÚ inline (o un `general-purpose` fresco con brief acotado y paths explícitos), no un `fork`. El fork rinde en tareas de análisis/verificación acotadas que se benefician de tu contexto, no en construir 10 ficheros. Verificar SIEMPRE en disco lo que produjo (worktree creado, commits) antes de fiarte del reporte. Caso real 2026-07-04: fork wa-fase3 Stripe → 0 output; rehecho inline con TDD, limpio.

## Failure mode G: worktree "corrupto" — build falla en origin/main puro, worktree hermano pasa → recrear

**Síntoma**: `next build` en un worktree falla determinista (`InvariantError: Expected workStore to be initialized. This is a bug in Next.js` en el prerender de páginas ajenas al diff), incluso tras revertir TODO el diff a origin/main. Un worktree HERMANO con el mismo origin/main + mismo `node_modules` (symlink compartido) buildeale limpio. Caché limpia (`.next`, `node_modules/.cache`), carga baja, browser cerrado — sigue fallando solo ese worktree.

**Causa probable**: estado local del worktree envenenado tras un `npm install` INTERRUMPIDO (timeout) contra el `node_modules` symlinkado compartido + builds concurrentes. `npm ci` en la raíz restaura el node_modules compartido pero NO cura el worktree.

**Fix**: no perseguir el fantasma — **recrear el worktree**. El commit vive en la rama: `git worktree remove --force <path>` + `git worktree add <path> <rama>` + re-symlink env/node_modules → buildeale limpio. Caso real 2026-07-15 (PR-B móvil).

**Blindaje**: NUNCA `npm install <dep>` dentro de un worktree con `node_modules` symlinkado compartido (afecta a todos + puede colgar). Añadir deps desde el checkout que posee node_modules, o al mergear.

## Failure mode H: `git stash` comparte stack entre TODOS los worktrees del repo → pop aplica stash ajeno

**Síntoma**: `git stash pop` en mi worktree aplica cambios que NO son míos (de otra rama/sesión) con conflictos `UU` en ficheros que no toqué.

**Causa**: el stack de stashes (`refs/stash`) es del REPO, compartido por todos los worktrees. `git stash push` apila sobre el stack común; un `pop` posterior saca lo que haya en el tope — puede ser de otra sesión paralela.

**Fix / blindaje**: **no usar `git stash` para aislar en un repo con worktrees.** Para probar "con/sin mi diff" usa `git checkout <ref> -- <paths>` (revertir ficheros puntuales) o un worktree/rama aparte. Si ya pasó: `stash pop` en conflicto NO borra el stash (sigue en el stack, nada perdido) → `git checkout HEAD -- <ficheros UU>` para descartar la copia mal aplicada y verificar `git stash list` intacto. Caso real 2026-07-15: popé un stash de otra sesión (13 en el stack). Relacionado: [[git-stash-sin-u-deja-untracked-y-hook-falla]].

## Failure mode I: `isolation:worktree` arranca sobre main y/o deja el HEAD del coordinador driftado

**Síntoma (I-1)**: el worktree del agente arranca en la LÍNEA MAIN, no en la rama de trabajo de la sesión (`feat/x`). Si la feature vive solo en `feat/x` (no en main), el agente no ve el módulo y su commit/merge sale mal. Varios agentes de una misma tanda lo reportaron; los que tocaban ficheros de la feature se autocorrigieron con `git checkout -b <rama> feat/x`, otros no.

**Síntoma (I-2, peor)**: tras completar un agente `isolation:worktree`, `git branch --show-current` en MI checkout (coordinador) devuelve la rama DEL AGENTE, no `feat/x`. Un `git merge <agente>` da "Already up to date" (mi HEAD ya es esa rama) → parece que no pasó nada. En realidad la operación de worktree del agente driftó mi HEAD.

**Fix**: (1) en el prompt del agente, exigir `git checkout -b <rama-hija> feat/x` como PRIMER paso + verificar que existen ficheros clave de la feature; PARAR si faltan. (2) Coordinador: `git branch --show-current` ANTES de cada merge/commit; si driftó, `git checkout feat/x` y reconciliar (`git merge <rama-agente>` con ff, luego seguir). El trabajo NO se pierde (vive en la rama del agente), solo hay que realinear el puntero. Caso real 2026-07-18 (Obras facturación, 8 agentes). Relacionado con B (base desfasada) y E (edición concurrente del principal).

## Checklist pre-lanzamiento de tandas multi-agente

Antes de lanzar N agentes paralelos:

1. **Disjoint scope**: cada agente toca paths sin solape. Lista explícita en el prompt: SÍ toca / NO toca.
2. **Prompt incluye pre-commit gates**: `npm run lint + typecheck + vitest <paths>` obligatorios antes de commitear.
3. **Prompt incluye instrucción explícita de commit local antes de devolver**. Y de NO push a main (que el caller decide merge tras review).
4. **Tras notificación de completion, verificar 3 cosas**:
   - `git log <worktree-branch>` tiene el commit nuevo (no solo el base).
   - `git status` del repo principal está limpio O tiene cambios solo del agente esperado.
   - `git diff main <worktree-branch> --stat` muestra solo paths del scope.
5. **Si el agente NO notifica completion en 2× el tiempo esperado**, verificar manualmente: process status, output file timestamp, working tree del repo principal por si dejó cambios sin commitear.
6. **Merge a main siempre selectivo**: `git checkout <branch> -- <paths>` mejor que `git merge <branch>`. Reduce sorpresas.

Sources:
- Sesión 2026-05-22/23 PR-PSD2-3.3+3.4 + PR-A4 + PR-B-anomalías
- Commits `5cf959e`, `3536cf1`, `7cbebb9`, `26ce766`
