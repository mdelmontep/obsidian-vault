---
title: el stop-gate corre el gate contra la base compartida, y un temporal sin trackear lo dispara
date: 2026-09-13
source: agh-iberica
tags: [claude-code, hooks, gate, postgres, worktrees]
---
- **Qué pasa:** `~/.claude/hooks/stop-gate.sh` lanza `npm run gate` si el cwd tiene cambios sin commitear. En agh-iberica lo lanza **sin `--base-efimera`**, así que los `.pg` caen al default `agh_dev`. Si esa base está atrasada, `db-al-dia` aborta antes de ejecutar un solo test (`CORRIDA ABORTADA … falta 0041, 0042, 0043`) y el hook bloquea el turno con un «gate en ROJO» que no es del diff.
- **Qué lo disparó:** una config temporal sin trackear (`vitest.tmp1717.config.ts`, el apaño de #1717) en el worktree que era el cwd, con todo el trabajo real ya commiteado.
- **Cómo se reconoce:** lint y typecheck en verde, `agente:test — sin resumen de vitest`, y la base citada es `agh_dev`, no `agh_gate_*`.
- **Qué hacer:** no migrar `agh_dev` para callarlo, porque es compartida. Declararlo ajeno y pegar la línea de TU gate con base efímera. Borra los temporales del worktree en cuanto dejes de usarlos.
- Relacionado: [[vitest-exclude-claude-rompe-el-run-por-fichero-en-worktrees-de-claude-code]]
