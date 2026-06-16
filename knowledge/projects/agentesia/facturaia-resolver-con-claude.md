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

## 103/104/106 — HECHOS + desplegados (2026-06-16, PR #316 → main `7884cacc`)

- **103** `sin_cambios` → Claude manda su último mensaje (stdout de `claude -p`) como
  `diagnostico` en el callback; el app lo publica como mensaje `admin` en
  `feedback_ticket_messages` (`recordSinCambiosDiagnostico`) y mueve el ticket
  `nuevo`→`en_revision`. `transitionAiJob` ahora devuelve `changed` → los efectos
  terminales (diagnóstico, email) solo se disparan en la transición real, no en
  callbacks idempotentes duplicados.
- **104** `claim` firma URL temporal de la 1ª captura (`getSignedUrl`); el runner la
  baja a `<wt>/.ticket-screenshot.<ext>` (gitignored, se borra con el worktree) y la
  referencia en el prompt. `claude-prompt.ts` ya soportaba `screenshotPath`.
- **106** plantilla `feedback-job-result` + `sendJobResultAlert` → email al superadmin
  (OWNER_EMAIL) en cada estado terminal con resultado + ticket + org + link al PR.
  Best-effort (no tumba el callback).
- **Deploy**: `compose.deploy` del runner + autoDeploy del app, ambos en `7884cacc`.
  ⚠️ Hallazgo: el runner estaba clavado en #304 — **no tenía el código 105** (heartbeat)
  pese a que #308 estaba en main; este deploy lo puso al día (105+103+104).
- **Smoke real pendiente**: ticket de UI con captura → confirmar que Claude lee
  `.ticket-screenshot.*`; y un `sin_cambios` real → diagnóstico en el hilo + email.

## Pendiente (issues 107, 108)

- **107** webhook GitHub PR-merged → ticket `resuelto`. ⚠️ **NECESITA acción humana**: alta
  del webhook + secret en el repo GitHub (como el PAT).
- **108** kill-switch (system_config) + audit_log por job + system_alerts en fallido +
  sección manual admin ("Resolver con Claude", merge siempre humano, renovar OAuth).

## 3 bugs reales que destapó el e2e (todos arreglados)

1. RPC `claim` con cola vacía devolvía "fila de nulls" `{id:null,...}` (no NULL) → runner
   en bucle apretado 9req/s contra /callback. Fix: guard `data?.id` + RPC PL/pgSQL + guard loop.
   Ver [[postgrest-rpc-composite-devuelve-fila-de-nulls]].
2. Runner reportaba `pr_abierto` aunque push/PR fallaran (no chequeaba exit codes). Fix: chequear.
3. `git push` del runner disparaba el pre-push hook (`npm build`) → 2º build → OOM. Fix:
   `--no-verify` (el runner ya gatea aparte). Ver [[runner-headless-git-push-dispara-pre-push-hook]].

## Cómo retomar (kickoff siguiente sesión)

103/104/106 cerrados y desplegados. Quedan **107** (cuando des de alta el webhook
GitHub PR-merged + secret) y **108** (kill-switch + audit_log + system_alerts +
manual admin). Antes de 108: hacer el **smoke real** de 103/104 (ticket con captura →
Claude la lee; `sin_cambios` real → diagnóstico al hilo + email al superadmin). El
runner está vivo en `7884cacc`; para pausarlo sin redeploy: `compose.stop`. Detalle
live en memoria del agente `reference_dokploy_facturaia.md`.
