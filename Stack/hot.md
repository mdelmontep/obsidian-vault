---
title: hot cache
date: 2026-07-13
tags: [stack, index]
---

# Hot Cache

Índice **caliente**: solo lo activo ahora (1 línea + link). El resto vive en `knowledge/learnings/`
(recall por relevancia) y transversales en [[index]] §Transversales / [[patterns-cross-proyecto]].
Podado 2026-07-13 (~40→15; lo retirado sigue íntegro en sus learnings, solo sale del índice rápido).

## UI / listados (reutilizable)
- **Scroll-fade dinámico** en riel que no cabe (`.scroll-fade-x`+`useScrollFade`): difumina solo el borde con contenido oculto. Gotchas: sin `transition` sobre `@property` (se clava en 0px), la máscara recorta `box-shadow` externo, callback ref para portales. Ver [[scroll-fade-dinamico-mascara-gotchas]].
- **Buscador de listado = lupa expandible**, no fila propia ni inline fijo (estruja/hueco). Ver [[buscador-listado-lupa-expandible-no-fila-propia]].
- **Column-picker: ocultar por CSS (display:none), no desmontar** th/td → preserva colSpan/sort/bulk. Ver [[ocultar-columnas-tabla-por-css-no-desmontar]].
- **Refactor UI grande con agentes**: particiona por archivo disjunto (no por feature) + antes/después vía `git stash`. Ver [[refactor-ui-grande-agentes-paralelos-particionados-por-archivo]].
- **Submodal dentro de un drawer/contenedor que coordina Escape/focus a mano → NO migrar a `<Modal>` sin más** (doble cierre). Ver [[migrar-submodal-a-modal-choca-con-escape-del-contenedor]].

## Agente AGH (capacidad conversacional)
- **Recall/RAG sin umbral = confidently-wrong** — k=1 sin piso de distancia miente; devolver distancia+umbral+top-k+atribución+golden negativo. Ver [[recall-semantico-sin-umbral-es-confidently-wrong]] · [[asistente-enterprise-natural-pero-grounded-no-llm-libre]].
- **Presenter grounded: conserva los ítems verbatim, no aflojes el verificador** — el guard estricto es demasiado en ítems compuestos; arregla el prompt del presenter, no el verificador. Ver [[presenter-grounded-conservar-items-verbatim-no-aflojar-verificador]].
- **Evals de modelo real: agregar corridas + baseline con margen** — un fichero de 3 casos oscila 100%↔33%; gate = N corridas + baseline − margen − tolerancia. Es la red para tocar el prompt. Ver [[evals-de-modelo-real-oscilan-agregar-corridas-y-baseline-con-margen]].
- **Correr evals opt-in: `vitest --repeat` no es CLI + timeout 5s da falsos timeouts** — bucle bash o runner; `--testTimeout=25000`; el full ×1 amplifica la varianza del baseline (×3 es el comparable). Ver [[evals-opt-in-vitest-repeat-timeout]].
- **Fix validado solo in-memory oculta bug pg-solo-prod** — campo nuevo en estado persistido: grep el store Postgres + test pg round-trip antes de "hecho". Ver [[fix-validado-solo-in-memory-oculta-bug-pg-solo-prod]].

## Auditoría / agentes / rutinas cloud
- **Auditar/fixear con red** — worktree desde origin/main + dedup vs issues abiertos ANTES de filar; re-audita tus fixes con agentes independientes antes de mergear. Ver [[auditar-sobre-origin-main-worktree-no-cwd-stale]] · [[maker-checker-re-auditar-fixes-propios-antes-de-merge]].
- **Bot de auditoría recurrente: idempotencia por estado de issues** — dedup contra abiertos Y cerrados; cerrar = corregido (suprime salvo regresión) / `wontfix` (supresión permanente). La fuente de datos no sabe qué está arreglado. Ver [[audit-bot-recurrente-idempotencia-por-estado-de-issues]].
- **`audit_log` con 2º escritor (agente): procedencia en el `after` jsonb (sin columna), before sin carrera (FOR UPDATE / DELETE RETURNING), audit en la misma tx, deps opcionales** — atomicidad se prueba con pg-real (fake in-memory no lo demuestra). Ver [[audit-log-multi-escritor-procedencia-en-after-before-sin-carrera]].
- **Delegar implementación con deps opcionales → revisar el camino de composición, no solo la hoja** — gate verde ≠ cableado; el código muerto no rompe tests. Ver [[subagente-feature-sin-cablear-composicion]].
- **Capacidad en 2 capas (tool que anuncia + gate de endpoint que autoriza) → paridad como test de invariante** — desajuste = tool muerta (403) que el inventario aislado da por sana; cruzar tool↔endpoint. Ver [[capacidad-en-dos-capas-tool-mas-gate-endpoint-verificar-paridad-o-queda-muerta]].
- **Hook-guard de comandos: matchea sobre el comando SIN comillas (scrub `"…"`/`'…'`), no substring cruda** — si no, un `gh pr create --body`/`git commit -m` que menciona la frase da falso positivo. Ver [[guard-hooks-matchear-comando-sin-comillas-no-substring-cruda]].
- **Rutinas cloud (RemoteTrigger/CCR): egress allowlist + identidad bot** — 403 en CONNECT a host privado → Network access Custom + Allowed domains (aplica a sesiones NUEVAS); postea por webhook, no por conector personal (suplanta). Ver `Stack/claude-code-harness.md` §Rutinas cloud.
- **Agentes background muertos por session limit → SendMessage al mismo agentId** — inventariar working tree primero; nunca dos sobre los mismos archivos. Ver [[agentes-background-mueren-por-session-limit-reanudar-con-sendmessage]].
- **Prompt caching Anthropic: cachear solo system+tools deja el HISTORIAL sin cachear** — en runner multi-turno/agéntico añade 3er breakpoint MÓVIL en el último mensaje (máx 4/request); `input_tokens` ya excluye lo cacheado, loguea `cache_read`. Ver [[anthropic-prompt-cache-prefijo-system-tools]].

## Git / worktrees / merge (multi-sesión)
- **Working tree en rama STALE → verifica antes de reimplementar** — lee de `git show origin/main:<path>` + `git merge-base --is-ancestor` antes de construir. Ver [[working-tree-en-rama-stale-verifica-antes-de-reimplementar]].
- **Stash/WIP viejo puede estar ya en main** — con ramas en paralelo se vuelve obsoleto; `git log origin/main -S "<firma>"` antes de reconciliar, y `git apply --3way` con 0 diff = ya aplicado. Ver [[stash-o-wip-viejo-puede-estar-ya-en-main-verificar-antes-de-reconciliar]].
- **`git worktree add` sin `cd` inmediato → Bash cae en el checkout principal** — verifica `pwd`+`git branch --show-current` justo después. Ver [[worktree-add-sin-cd-bash-cae-en-checkout-principal]].
- **Worktree monorepo → symlinkar TAMBIÉN el node_modules anidado** (`dashboard/node_modules`), no solo el raíz; si no, tests del subpaquete fallan (`react/jsx-dev-runtime`) y parece regresión tuya. Ver [[worktree-monorepo-symlink-node-modules-anidado]].
- **`gh pr merge` miente en stdout** — verifica `gh pr view <n> --json state` == MERGED. Ver [[gh-pr-merge-no-confirma-verificar-state-merged]].
- **PR stackeada + squash → `rebase --onto <base-vieja>`, no rebase normal** — el squash mete la base con SHA nuevo; un rebase normal la duplica. Luego retarget a main + verificar `baseRefName`. Ver [[rebase-onto-pr-stackeada-squash-no-duplicar]].
- **PR apilado: NO borres la base antes de reapuntar el dependiente** — `gh pr merge PR0 --delete-branch` AUTO-CIERRA el PR dependiente (no reapunta) y ya no se puede reabrir → recrear. Reapunta (`gh pr edit N --base main`) o mergea sin `--delete-branch`; merge commits, no squash, en stacks. Ver [[gh-pr-merge-delete-branch-cierra-pr-apilado-dependiente]].
- **Actions caído (billing) → hooks locales = único gate** — `npm run lint` global antes de cada merge; node_modules real para que el pre-push build pase en worktree. Ver [[actions-sin-billing-hooks-locales-unico-gate]].
- **Limpiar root checkout viejo con worktrees → stash selectivo + ff-only** — nada de reset (git-guard lo bloquea); caracteriza los cambios (monolito pre-refactor = obsoleto); `stash push -- <paths>` (recuperable) + `merge --ff-only`. Ver [[limpiar-root-checkout-viejo-con-worktrees-stash-selectivo-ff-only]].

## Infra / Dokploy / Supabase / Stripe (FacturaIA)
- **NUNCA `compose.one`/`application.one`/`schedule.one` de Dokploy en crudo** — vuelcan el `env` con secrets en plano (fuga real 07-03); hook global BLOQUEA, usa `~/.claude/bin/dokploy-safe.sh`. Ver [[dokploy-api-get-schedule-list-expone-env-completo-secrets]].
- **Schedule Dokploy compose exige `serviceName`** — sin él runManually→500 y el cron no dispara (invisible); verifica el 1er run a mano. Ver [[dokploy-compose-schedule-requiere-servicename]].
- **Supabase egress restringido tumba la app vía healthcheck → Traefik 404** (Docker "healthy" engaña; `curl -I` da 404). Restaurar plan; egress es mensual. Ver [[supabase-egress-restringido-tumba-app-via-healthcheck-traefik-404]].
- **Stripe: el CLI puede ir a OTRA cuenta que la sk_live de la app** — "No such price" falso; verifica con `curl -u $SK` de la app. Ver [[stripe-cli-cuenta-distinta-de-la-app-price-no-existe-falso-positivo]].

## Frontend / UX / QA
- **Subida en lote vs rate-limit per-user: sin backoff el excedente se pierde** — Retry-After exacto (PTTL) + `code:rate_limited` en el 429 + `fetchWithTransientRetry` (backoff sobre 429-por-minuto/5xx/red, no sobre topes de plan) + panel de reintento. La cola de fondo NO cubre la ráfaga de subida HTTP. Ver [[subida-en-lote-cliente-backoff-sobre-rate-limit-servidor]].
- **Acción masiva en cliente con N round-trips en serie cuelga la UI** — batch read (`.in(ids)`) + un `UPDATE .in(ids)` si todas iguales, o pool acotado (~6) + contador `N/total` y relleno del botón. Ver [[accion-masiva-cliente-n-round-trips-serie-cuelga-usar-batch-y-pool]].
- **Clave de selección de fila = id único, no campo de negocio** — `num??id` colapsa duplicados (nº recibidas repite) → acciones en lote saltan filas en silencio. Ver [[clave-seleccion-fila-debe-ser-id-unico-no-campo-de-negocio]].
- **OpenAI vision lee un PDF del revés si rotas páginas con pdf-lib** — honra el `/Rotate`; auto-orientar reintentando en fallos [180,90,270]. Ver [[openai-vision-lee-pdf-del-reves-rotando-con-pdf-lib]].
- **Dep nativa (sharp) en ruta API → import dinámico en try/catch** — el import estático tumba TODA la ruta si el `.node` no carga en Alpine; + `serverExternalPackages`. Ver [[dep-nativa-import-dinamico-defensivo-en-ruta-api]].
- **agent-browser `eval` reutiliza contexto → `const` redeclarado peta** — envuelve en IIFE o usa `wait --fn` para esperar sin polling manual (evita cronometrajes falsos). Ver [[agent-browser-eval-contexto-persiste-const-usar-iife]].
- **Grid `1fr` no encoge bajo su contenido `nowrap` → desborda** — usar `minmax(0, 1fr)` + `min-width:0` en la cadena flex-column; el badge/importe se salía de pantalla pese al ellipsis. Lo caza el QA visual, no el build. Ver [[grid-1fr-no-encoge-con-contenido-nowrap-usar-minmax-0-1fr]].

---
Temas completos por área en `Stack/<tool>.md` (supabase-cloud, frontend-css-mobile, claude-code-gotchas/harness, docker-infra) y transversales en [[index]]. Lo retirado sigue en `knowledge/learnings/`, no se ha borrado ningún learning.
