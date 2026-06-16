---
title: TuFacturaIA — Resolver con Claude (feedback fase 3)
date: 2026-06-16
source: claude-code-session
tags: [facturaia, feedback, claude-code, runner, dokploy]
---

Botón "Resolver con Claude" en `/admin/feedback`: un runner propio en Dokploy
ejecuta Claude Code headless con el prompt del ticket, abre un PR (NUNCA mergea)
y deja trazado el resultado. **OPERATIVO en prod con Claude real desde 2026-06-16.**

## Estado (2026-06-16) — núcleo en prod, robusto

- **Mergeado**: #283 (Issue 100, cola+endpoints+botón) + #287 (Issue 101, claim+runner)
  + #301 + #305 + #308. Migs **305** (feedback_ai_jobs), **306** (claim RPC + rol RO),
  **310** (fix claim) aplicadas a prod.
- **Runner Dokploy VIVO**: compose `ticket-runner` composeId `Mv4mWVmR05Xviw8ZmwZ3q`
  (proyecto tufacturaia-prod). `STUB=0` (Claude real, Opus, OAuth suscripción).
- **102 (Claude real + gate)**: validado. e2e STUB→PR real del bot; smoke real→`sin_cambios`
  genuino. El bot `mdelmonteagentesia` NO puede mergear (ruleset `Protect main` id 17755984,
  bypass solo team `facturaia-maintainers`). Org ahora **enterprise** (CI Actions desbloqueado).
- **105 (robustez)**: heartbeat 60s + timeout duro + check exit code de claude + cron
  `feedback-ai-job-watchdog` (scheduleId `cIvhvuFsnFl_N2PfjVAFI`, cada 5 min) que rescata
  jobs `ejecutando` zombi (>15 min sin latido) → `fallido`. Verificado (rescued 1).

## Credenciales (1Password vault FacturAIA)

Bot PAT classic `repo` → item "Token Github Bot mdelmonteagentesia" · OAuth Claude →
item "CLAUDE_CODE_OAUTH_TOKEN" · rol RO `claude_runner_ro` URL → item `hybhsynd4p6xb6xivglbwrwsiy`.
(Bot es colaborador externo → fine-grained PAT NO sirve, classic `repo` sí.)

## Pendiente (issues 103,104,106,107,108)

- **103** `sin_cambios` → postear diagnóstico de Claude al hilo (`feedback_ticket_messages`)
  + ticket `en_revision`. Endpoint interno nuevo + runner captura el diagnóstico.
- **104** descargar screenshot del ticket al worktree (claim devuelve URL firmada vía
  `getSignedUrl`, bucket `feedback-screenshots`) y referenciarlo en el prompt (gitignored).
- **106** email al superadmin al estado terminal (Resend, plantilla nueva, best-effort).
- **107** webhook GitHub PR-merged → ticket `resuelto`. ⚠️ **NECESITA acción humana**: alta
  del webhook + secret en el repo GitHub (como el PAT).
- **108** kill-switch (system_config) + audit_log por job + system_alerts en fallido +
  sección manual admin ("Resolver con Claude", merge siempre humano, renovar OAuth).
- Gap menor abierto: el runner toca `run-ticket.mjs` en 103+104 → un solo redeploy al final.

## 3 bugs reales que destapó el e2e (todos arreglados)

1. RPC `claim` con cola vacía devolvía "fila de nulls" `{id:null,...}` (no NULL) → runner
   en bucle apretado 9req/s contra /callback. Fix: guard `data?.id` + RPC PL/pgSQL + guard loop.
   Ver [[postgrest-rpc-composite-devuelve-fila-de-nulls]].
2. Runner reportaba `pr_abierto` aunque push/PR fallaran (no chequeaba exit codes). Fix: chequear.
3. `git push` del runner disparaba el pre-push hook (`npm build`) → 2º build → OOM. Fix:
   `--no-verify` (el runner ya gatea aparte). Ver [[runner-headless-git-push-dispara-pre-push-hook]].

## Cómo retomar (kickoff siguiente sesión)

Seguir con issues **103 → 104 → 106** (sin dependencia humana), luego **107** (cuando
des de alta el webhook GitHub) y **108**. Tras 103+104 (tocan `ops/ticket-runner/run-ticket.mjs`)
→ un `compose.deploy` del runner (API Dokploy, key en memoria) + verificar. El runner
está vivo; para pausarlo sin redeploy: `compose.stop`. Detalle live en memoria del agente
`reference_dokploy_facturaia.md`.
