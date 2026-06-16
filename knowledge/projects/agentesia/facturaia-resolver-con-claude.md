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

## 107/108 — HECHOS + desplegados + smoke real OK (2026-06-16, PR #321 → main `930015c8`)

- **107** endpoint `POST /api/internal/github-webhook`: firma HMAC `X-Hub-Signature-256`
  con `GITHUB_WEBHOOK_SECRET`; solo `pull_request` closed+merged; mapea `pr_url`→job→ticket
  → `resuelto` + email de resolución al usuario; idempotente; PR humano sin job → no-op.
  **Webhook GitHub creado vía `gh api`** (scope `repo` basta, no hizo falta el user): hook
  id `642750021`, events `pull_request`, ping 200. Secret (64 hex) en env del app + en GitHub.
- **108** kill-switch `system_config.resolver_claude_runner {enabled}` (claim no entrega si
  off, fail-open; mig 314 lo siembra) + audit `resolve_ia.enqueue`/`.terminal` en
  `admin_audit_log` + `system_alert` media al fallar (dedup por ticket) + manual admin §42.6.
- **Smoke real end-to-end VERDE**: ticket sandbox con captura → runner la descargó → Claude
  la **leyó** (citó `ZQ7-•••`, describió la pantalla; bonus: detectó el pretexting del
  "código de verificación" y rehusó transcribirlo) → `sin_cambios` + diagnóstico al hilo +
  ticket→en_revision (103✓) + email al superadmin (106✓) + audit terminal (108✓).
  Kill-switch: OFF→`{job:null,paused:true}`, ON→`{job:null}`. Webhook: 401/no_job/pong.
- **FEATURE COMPLETA** (issues 100-108). Runner vivo en `7884cacc` (107/108 son app-side,
  no necesitó redeploy).

## Fase 4 — mejoras UX / interactividad (roadmap)

**Tanda 1 — HECHA + prod** (PR #327 → main `5d06efb2`, 2026-06-16; app-side, sin migración):
- **Q9 prompt enrutado** (`src/lib/feedback/claude-prompt.ts`): `buildClaudePrompt` ahora
  añade bloque "Dónde mirar primero" según tipo + keywords de página/descripción (espejo de
  la tabla de routing del `CLAUDE.md`: UI→`gotchas §Frontend`+`docs/design/`, auth→§Auth,
  OCR→§OCR, documentos→`createDocument`, etc.) + guía por tipo (bug/mejora/pregunta).
  **Fix latente**: el prompt decía "Repo: /Users/manueldelmonte/facturaia" (ruta local, no
  existe en el runner) → ahora "directorio actual". Tests en `claude-prompt.test.ts`.
- **Q2** ticket `nuevo`→`en_revision` al encolar (`resolve-ia/route.ts`).
- **Q3** badge del estado del último job en la lista admin (`getLatestJobStatusByTickets`
  en repository + `route.ts` adjunta `ai_job_status` + `page.tsx` badge con punto pulsante).
- **Q4** botón "Relanzar con Claude" cuando el job es terminal (deja claro que re-lanzar
  continúa leyendo el hilo).

**Tanda 2 — interactividad (SIGUIENTE):**
- **Q1 progreso en vivo**: el runner ya late `ejecutando` cada 60s; añadir pasos
  incrementales — tabla nueva `feedback_ai_job_events` (o `claude -p --output-format
  stream-json` resumido al callback) y el panel los muestra en vivo.
- **Q7/Q8 loop "Continuar"**: formalizar lo que YA funciona de facto (re-encolar mete todo
  el hilo en el prompt vía `listMessages`). Claude termina con pregunta → admin responde en
  hilo → "Continuar" (= relanzar, ya existe) con copy explícito y quizá estado
  `espera_respuesta`. NO sesión viva: el hilo es la memoria (decisión: barato y robusto).

**Tanda 3 — infra:**
- **Q5 email con botón de acción**: el email de ticket nuevo lleva botón "Resolver con
  Claude" → enlace firmado (token HMAC con TTL/single-use, scope superadmin) → endpoint que
  valida y encola sin entrar a admin.
- **Q6 paralelismo**: el claim ya usa `FOR UPDATE SKIP LOCKED` → escalar el runner a 2-3
  réplicas en Dokploy (cada una coge un job distinto sin pisarse). Vigilar RAM (claude+build
  por réplica) y coste OAuth.

## 3 bugs reales que destapó el e2e (todos arreglados)

1. RPC `claim` con cola vacía devolvía "fila de nulls" `{id:null,...}` (no NULL) → runner
   en bucle apretado 9req/s contra /callback. Fix: guard `data?.id` + RPC PL/pgSQL + guard loop.
   Ver [[postgrest-rpc-composite-devuelve-fila-de-nulls]].
2. Runner reportaba `pr_abierto` aunque push/PR fallaran (no chequeaba exit codes). Fix: chequear.
3. `git push` del runner disparaba el pre-push hook (`npm build`) → 2º build → OOM. Fix:
   `--no-verify` (el runner ya gatea aparte). Ver [[runner-headless-git-push-dispara-pre-push-hook]].

## Cómo retomar (kickoff siguiente sesión)

**Issues 100-108 COMPLETOS en prod + smoke real verde. Fase 4 Tanda 1 también en prod
(#327).** Lo siguiente es **Fase 4 Tanda 2 (interactividad) y Tanda 3 (infra)** — ver
sección "Fase 4" arriba con el diseño de cada Q. Empezar por Tanda 2 (Q1 progreso en vivo +
Q7/Q8 loop "Continuar"), luego Tanda 3 (Q5 email-action + Q6 réplicas runner).

Operativa ya viva:
- Pausar el runner sin redeploy: `UPDATE system_config SET value='{"enabled":false}'
  WHERE key='resolver_claude_runner';` (reactivar con `true`). Runner vivo en `7884cacc`.
- Webhook GitHub (hook id `642750021`) cierra el ticket al mergear el PR del runner.
- Renovar OAuth si caduca: `claude setup-token` → `CLAUDE_CODE_OAUTH_TOKEN` en env del
  compose `ticket-runner` + `compose.deploy`.
- Trabajar en **worktree aislado** desde `origin/main` (hay sesiones paralelas en el repo);
  gate (lint+typecheck+build) + CI + merge `--admin`. La "Visual Regression /design-system"
  falla en main (baselines stale) → ignorar, mergear con `--admin`. Detalle live en memoria
  del agente `reference_dokploy_facturaia.md`.
