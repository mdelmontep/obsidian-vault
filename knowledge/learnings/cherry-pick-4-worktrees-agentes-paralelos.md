---
title: 4 agentes paralelos en worktrees aislados + cherry-pick combinado a 1 PR
date: 2026-05-21
source: claude-code-session
tags: [claude-code, agentes, git, workflow]
---

Para paralelizar N fixes sobre el mismo módulo sin colisión:
1. **Verificar scope archivo-disjoint ANTES de delegar**. Cada agente debe tocar archivos no compartidos con otros.
2. Lanzar N agentes con `isolation: worktree`, cada uno con su branch `fix/X-...` desde `origin/main`.
3. Cada agente: implementa + lint + typecheck + tests en su worktree, commit local.
4. Tras retorno: `git checkout -b feat/combined main` + `git cherry-pick commit1 commit2 ...` en orden lógico.
5. Verify combined: `rm -rf .next` (cache stale entre branches) + lint + typecheck + build + tests.
6. 1 push + 1 PR único combinado.

Trampa: si dos agentes editan mismo archivo aunque sea sección distinta → conflicto en cherry-pick. Mejor consolidar scope antes que arreglar conflictos después.

Otra trampa: el `.next/dev/types/routes.d.ts` queda stale entre cambios de branch en main → `tsc --noEmit` falla con "is not a module". Solución: `rm -rf .next` antes del verify final.

Caso real: PR #69 conciliación hardening — 4 agentes (P0 #1, P0 #2, P0 #3, P1 #4), 42 tests nuevos, 0 conflictos, 0 regresiones. ~30 min total vs ~2-3h secuencial.

Ver [[3-agentes-paralelos-auditoria-cambios-grandes]] (para auditoría) y [[audits-cross-pr-vs-per-pr]] (composicional).
