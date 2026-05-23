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
