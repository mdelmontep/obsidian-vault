---
title: hot cache
date: 2026-07-13
tags: [stack, index]
---

# Hot Cache

Índice **caliente**: solo lo activo ahora (1 línea + link). El resto vive en `knowledge/learnings/`
(recall por relevancia) y transversales en [[index]] §Transversales / [[patterns-cross-proyecto]].
Podado 2026-07-13 (~40→15; lo retirado sigue íntegro en sus learnings, solo sale del índice rápido).

## Agente AGH (capacidad conversacional)
- **Recall/RAG sin umbral = confidently-wrong** — k=1 sin piso de distancia miente; devolver distancia+umbral+top-k+atribución+golden negativo. Ver [[recall-semantico-sin-umbral-es-confidently-wrong]] · [[asistente-enterprise-natural-pero-grounded-no-llm-libre]].
- **Presenter grounded: conserva los ítems verbatim, no aflojes el verificador** — el guard estricto es demasiado en ítems compuestos; arregla el prompt del presenter, no el verificador. Ver [[presenter-grounded-conservar-items-verbatim-no-aflojar-verificador]].
- **Evals de modelo real: agregar corridas + baseline con margen** — un fichero de 3 casos oscila 100%↔33%; gate = N corridas + baseline − margen − tolerancia. Es la red para tocar el prompt. Ver [[evals-de-modelo-real-oscilan-agregar-corridas-y-baseline-con-margen]].
- **Correr evals opt-in: `vitest --repeat` no es CLI + timeout 5s da falsos timeouts** — bucle bash o runner; `--testTimeout=25000`; el full ×1 amplifica la varianza del baseline (×3 es el comparable). Ver [[evals-opt-in-vitest-repeat-timeout]].
- **Fix validado solo in-memory oculta bug pg-solo-prod** — campo nuevo en estado persistido: grep el store Postgres + test pg round-trip antes de "hecho". Ver [[fix-validado-solo-in-memory-oculta-bug-pg-solo-prod]].

## Auditoría / agentes / rutinas cloud
- **Auditar/fixear con red** — worktree desde origin/main + dedup vs issues abiertos ANTES de filar; re-audita tus fixes con agentes independientes antes de mergear. Ver [[auditar-sobre-origin-main-worktree-no-cwd-stale]] · [[maker-checker-re-auditar-fixes-propios-antes-de-merge]].
- **Bot de auditoría recurrente: idempotencia por estado de issues** — dedup contra abiertos Y cerrados; cerrar = corregido (suprime salvo regresión) / `wontfix` (supresión permanente). La fuente de datos no sabe qué está arreglado. Ver [[audit-bot-recurrente-idempotencia-por-estado-de-issues]].
- **Rutinas cloud (RemoteTrigger/CCR): egress allowlist + identidad bot** — 403 en CONNECT a host privado → Network access Custom + Allowed domains (aplica a sesiones NUEVAS); postea por webhook, no por conector personal (suplanta). Ver `Stack/claude-code-harness.md` §Rutinas cloud.
- **Agentes background muertos por session limit → SendMessage al mismo agentId** — inventariar working tree primero; nunca dos sobre los mismos archivos. Ver [[agentes-background-mueren-por-session-limit-reanudar-con-sendmessage]].

## Git / worktrees / merge (multi-sesión)
- **Working tree en rama STALE → verifica antes de reimplementar** — lee de `git show origin/main:<path>` + `git merge-base --is-ancestor` antes de construir. Ver [[working-tree-en-rama-stale-verifica-antes-de-reimplementar]].
- **`git worktree add` sin `cd` inmediato → Bash cae en el checkout principal** — verifica `pwd`+`git branch --show-current` justo después. Ver [[worktree-add-sin-cd-bash-cae-en-checkout-principal]].
- **`gh pr merge` miente en stdout** — verifica `gh pr view <n> --json state` == MERGED. Ver [[gh-pr-merge-no-confirma-verificar-state-merged]].
- **PR stackeada + squash → `rebase --onto <base-vieja>`, no rebase normal** — el squash mete la base con SHA nuevo; un rebase normal la duplica. Luego retarget a main + verificar `baseRefName`. Ver [[rebase-onto-pr-stackeada-squash-no-duplicar]].
- **Actions caído (billing) → hooks locales = único gate** — `npm run lint` global antes de cada merge; node_modules real para que el pre-push build pase en worktree. Ver [[actions-sin-billing-hooks-locales-unico-gate]].

## Infra / Dokploy / Supabase / Stripe (FacturaIA)
- **NUNCA `compose.one`/`application.one`/`schedule.one` de Dokploy en crudo** — vuelcan el `env` con secrets en plano (fuga real 07-03); hook global BLOQUEA, usa `~/.claude/bin/dokploy-safe.sh`. Ver [[dokploy-api-get-schedule-list-expone-env-completo-secrets]].
- **Schedule Dokploy compose exige `serviceName`** — sin él runManually→500 y el cron no dispara (invisible); verifica el 1er run a mano. Ver [[dokploy-compose-schedule-requiere-servicename]].
- **Supabase egress restringido tumba la app vía healthcheck → Traefik 404** (Docker "healthy" engaña; `curl -I` da 404). Restaurar plan; egress es mensual. Ver [[supabase-egress-restringido-tumba-app-via-healthcheck-traefik-404]].
- **Stripe: el CLI puede ir a OTRA cuenta que la sk_live de la app** — "No such price" falso; verifica con `curl -u $SK` de la app. Ver [[stripe-cli-cuenta-distinta-de-la-app-price-no-existe-falso-positivo]].

---
Temas completos por área en `Stack/<tool>.md` (supabase-cloud, frontend-css-mobile, claude-code-gotchas/harness, docker-infra) y transversales en [[index]]. Lo retirado sigue en `knowledge/learnings/`, no se ha borrado ningún learning.
