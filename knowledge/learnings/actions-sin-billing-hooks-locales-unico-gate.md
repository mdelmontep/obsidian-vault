---
title: con Actions caído (billing), los git hooks locales son el único gate de lint/build en facturaia
date: 2026-06-25
source: claude-code-session
tags: [facturaia, ci, git-hooks, eslint, deploy]
---

El CI de GitHub Actions de facturaia está caído por billing → no corre lint/typecheck/build
en los PRs. Los hooks de `.githooks` (pre-commit: trinquete + lint + typecheck; pre-push: build)
son la ÚNICA red. Si un merge usa `--no-verify`, cuela lint/build roto a `main` sin que nadie
se entere.

Caso real (jun 2026): la feature SEPA devoluciones coló a `main` un `react-hooks/set-state-in-effect`
(eslint-plugin-react-hooks@7.1.1) en `facturas-view.tsx` → `npm run lint` global en rojo; lo
arrastraron varios PRs con `--no-verify` hasta el fix #482. Confirmado que NO era skew: el
`package-lock` fijaba la 7.1.1 exacta.

Reglas mientras Actions siga sin billing:
- `npm run lint` global en local antes de cualquier merge a main. NO `--no-verify` salvo
  emergencia documentada; si el hook falla por algo ajeno a tu diff, arréglalo en su propio PR primero.
- Para que el pre-push (build) pase en un worktree hay que usar node_modules REAL (`npm ci`),
  no symlink. Ver [[turbopack-rechaza-symlink-node-modules-en-worktree]].
- PR abierto por un runner/bot (p.ej. "Resolver con Claude") NO pasa por los hooks locales: llega
  con los 4 checks en rojo muriendo en ~2 s (arranque por billing, no fallos del código). Gate
  manual antes de mergear = worktree detached sobre la rama + `git merge origin/main` (la rama
  suele ir varios commits por detrás) + `npm ci` + lint/typecheck/vitest/build.

**Alcance medido 2026-07-27.** Último verde no-Dependabot: 19-jul 11:46. Desde entonces
**235 PRs / 265 commits** a `main` sin CI. Además de lint/build (que cubren los hooks) se
pierde CodeQL, la regresión visual y la re-ejecución fuera de la máquina de quien commitea.

**Lo grave no es lo que no se verifica: es lo que no se EJECUTA.** Las mitigaciones de
incidentes pasados viven dentro de Actions y están muertas con ella —`deploy-mcp.yml` (el
MCP se volvió a quedar sin desplegar, ver [[dokploy-autodeploy-false-desfase-silencioso]])
y el cron de `scheduler-watchdog`. Y el check de migración duplicada del `pre-push` solo
mira al empujar: una rama en review no se revalida cuando otra PR le ocupa el número (caso
#1226, 27-jul).

Efecto cultural: 24 PRs con 4 checks rojos y ninguno significativo. Un guard siempre en
rojo enseña a ignorar el rojo. Opciones (incl. runner self-hosted, que no gasta minutos
pero hay que comprobar si el bloqueo es por gasto o por suspensión): issue #1267 del repo.

**Coste medido 2026-08-02.** Al retirar el disparador de `ci.yml` (ADR-043), todo gate que
vivía SOLO ahí dejó de existir — y eso no se auditó gate a gate. `ratchet:design` era uno:
no es que fallara y nadie lo mirase, **no se ejecutaba**. Entraron **111 ocurrencias de
deuda** (31 ficheros con `<button>` nativo o hex crudo) en semanas. Los tres trinquetes
pasan a `.githooks/pre-commit` — cuestan 0,5 s los tres, así que el "no cargues el hook"
nunca fue el trade-off real. **Al matar un CI, migrar sus gates UNO A UNO al hook**: lo que
quede allí es documentación, no verificación. Ver
[[una-metrica-por-regex-sin-test-del-parser-cuenta-ruido-y-se-vuelve-ignorable]].

**La señal que hace creer que Actions ha vuelto (12-ago).** `gh api .../actions/runs`
mostraba runs de **Dependabot en verde** del 10-ago. No significan nada: las
actualizaciones de Dependabot corren en su propia infraestructura. Disparando
`ci.yml` a mano (`gh workflow run ci.yml --ref main`) los dos jobs murieron en
**2 segundos con 0 pasos**, que es la firma del impago y no un fallo de los tests.
El único indicador que discrimina es `steps` de los jobs: si es 0, sigue bloqueado.
