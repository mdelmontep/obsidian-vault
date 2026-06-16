---
title: TuFacturaIA — Resolver con Claude (feedback fase 3)
date: 2026-06-16
source: claude-code-session
tags: [facturaia, feedback, claude-code, runner, dokploy]
---

Botón "Resolver con Claude" en `/admin/feedback`: un runner propio en Dokploy
ejecuta Claude Code headless con el prompt del ticket, abre un PR (NUNCA mergea)
y deja trazado el resultado. Fases 1-2 (banner, hilo, "Copiar prompt") ya en prod.

## Estado (2026-06-16)

- **PRD + 9 issues**: `issues/prd-resolver-con-claude.md` + `issues/100`–`108`.
- **PR #283** (Issue 100): cola `feedback_ai_jobs` + endpoints (resolve-ia/ai-job/
  callback) + botón panel + lógica pura TDD (claude-prompt, ai-jobs). Gates verdes.
- **PR #287** (Issue 101, stacked sobre #283): claim atómico (RPC mig 304) + rol RO
  `claude_runner_ro` + scaffolding runner en `ops/ticket-runner/` (Dockerfile,
  compose, run-ticket.mjs, deny-list, README). Gates verdes.
- Ambos **sin mergear**. Worktrees `facturaia-resolver-claude` y `facturaia-runner`.

## Decisiones (grilladas)

Trigger = runner polling · auth Claude = **OAuth de suscripción** (no toca API key) ·
BD = rol read-only · salida = PR o diagnóstico (`pr_abierto|sin_cambios|fallido`) ·
gate = runner re-corre lint/typecheck/build (CI repo rojo por billing) · modelo = Opus ·
permisos = aislamiento infra + skip-permissions + deny-list · screenshot = descarga local ·
zombies = timeout 30min + heartbeat · aviso = panel + email superadmin · cierre = webhook GH.

## Candado "nunca merge" — BLOQUEO en plan Free (verificado doc oficial)

En **org Free + repo privado NO hay candado nativo**: rulesets exigen GitHub Team+,
la protección de ramas en privados también, y no se puede forkear un privado en Free.
Y en GitHub no se puede separar push de merge (ambos = `contents:write`). Opciones:
- **A. Subir org a GitHub Team** (~4 $/usuario/mes) → ruleset en `main` con bypass solo
  para Manuel = candado duro.
- **B. Quedarse en Free** → garantía **procedural** (el runner nunca llama `gh pr merge`
  + deny-list + bot bajo privilegio + PAT scopeado). Ya implementada en el código de #287.
  Riesgo: un bug podría mergear. **Arrancar con B**, subir a Team si hace falta.
- **Pendiente**: confirmar si `AgentesIA-MAdrid` ya está en Team (billing). Si sí → A gratis.

Ver [[github-free-org-privado-sin-branch-protection-ni-rulesets]].

## Prerequisitos de setup (HITL)

Cuenta bot `mdelmonteagentesia` con Write en `facturaia` (no owner) · PAT fine-grained
(Contents+PR, scope 1 repo) · `claude setup-token` (OAuth) · migs 303+304 + `ALTER ROLE
claude_runner_ro WITH LOGIN PASSWORD` · deploy Dokploy con `CLAUDE_RUNNER_STUB=1` primero.

## Kickoff siguiente sesión

Mergear #283 → #287, aplicar migs, desplegar runner con STUB=1, verificar
claim→PR→callback e2e, quitar stub (Claude real), seguir issues 102→108.
