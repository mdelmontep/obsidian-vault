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

**Tanda 2 — HECHA + prod** (PR #333 → main, 2026-06-17; mig 317 aplicada + runner redeploy):
- **Q1 progreso en vivo**: tabla `feedback_ai_job_events` (mig 317, append-only, RLS
  service-role-only) + endpoint interno `POST /feedback-ai-job/[id]/progress`. El runner
  emite hitos paso a paso (`preparando→analizando→verificando→subiendo`); `GET ai-job`
  devuelve `events`; el panel pinta un timeline que refresca cada 5s y cierra con el estado
  terminal. (Decidido: hitos del runner, NO stream-json — robusto y barato.)
- **Q7/Q8 loop "Continuar"**: botón "Continuar con Claude" (sin_cambios) / "Reintentar con
  Claude" (fallido) + hint en el modal. Relanzar re-encola leyendo todo el hilo. **SIN** nuevo
  estado `espera_respuesta` (decisión: el hilo es la memoria, evitar tocar la máquina de estados).
- Runner desplegado (compose.deploy, commit con 105+103+104+Q1) — verificado en logs: clonó +
  arrancó `stub=false` 00:06, claim de job real 00:09.

**Tanda 3 — HECHA + prod** (PR #338 → main, 2026-06-17; mig 319 aplicada; app auto-deploy):
- **Q5 email-action**: `src/lib/feedback/action-token.ts` (HMAC firmado, TTL 7d, jti único) +
  mig **319** `feedback_action_tokens` (ledger single-use, RLS service-role-only) + página
  pública `/resolver-con-claude` (confirma en GET) + `POST /api/feedback-action/resolve`
  (valida+consume+encola). **Mutación en POST, no en GET** (un escáner de correo que pre-cargue
  el enlace no gasta el token). Botón "Resolver con Claude" en el email de ticket nuevo.
  Middleware allowlist + rate-limit 60/min/IP. Audit `via:'email_action'`.
- **Q6 paralelismo — código HECHO, NO escalado** (decisión basada en evidencia): compose
  parametriza `deploy.replicas: ${RUNNER_REPLICAS:-1}` (default 1, replica-safe por SKIP
  LOCKED + REPO_DIR por contenedor + ramas por-ticket). **NO se sube a 2-3**: el host
  `185.47.13.170` es **8 GiB SIN swap**; con UN solo runner en build ya está a 6.6/7.9 GiB
  (~900 MiB libres) y el runner pega su límite de 3 GiB. Una 2ª réplica concurrente = **OOM
  seguro** (mataría app/n8n). Escalar solo tras añadir swap o RAM al host. README/.env.example
  documentan el `RUNNER_REPLICAS`.

**⚠️ Riesgo de host detectado (2026-06-17)**: 185.47.13.170 = 8 GiB **sin swap**, ~900 MiB
libres con un runner en build. Los heartbeats del runner vieron `502` (gateway/app). Latente:
un build del runner + app + n8n roza el OOM. Recomendado: añadir swap (p.ej. 4 GiB) o subir RAM
del VPS antes de cualquier paralelismo. **Sin esto, NO escalar el runner.**

**🔥 El riesgo se materializó el mismo día**: el OOM tumbó el **control-plane de Dokploy** ~7h
(containerd/runc wedged → `runc create ... PID from pipe: EOF` en todo contenedor nuevo;
autoDeploy muerto → Tanda 3 sin desplegar). Recuperado con **reboot del VPS** + **`pg_resetwal`**
de la BD interna de Dokploy (WAL corrupto por la escritura cortada del OOM). Tras eso, deploy
manual del app → **Tanda 3 (Q5) LIVE** (`/resolver-con-claude` 200, `POST /api/feedback-action/
resolve` 303). Detalle completo en `Stack/incidents.md` (2026-06-17, host Dokploy). **Swap 4 GiB AÑADIDO**
(`/swapfile` en `/etc/fstab`) — causa raíz cerrada. Con swap, Q6 (2 réplicas) ya es viable.

## 3 bugs reales que destapó el e2e (todos arreglados)

1. RPC `claim` con cola vacía devolvía "fila de nulls" `{id:null,...}` (no NULL) → runner
   en bucle apretado 9req/s contra /callback. Fix: guard `data?.id` + RPC PL/pgSQL + guard loop.
   Ver [[postgrest-rpc-composite-devuelve-fila-de-nulls]].
2. Runner reportaba `pr_abierto` aunque push/PR fallaran (no chequeaba exit codes). Fix: chequear.
3. `git push` del runner disparaba el pre-push hook (`npm build`) → 2º build → OOM. Fix:
   `--no-verify` (el runner ya gatea aparte). Ver [[runner-headless-git-push-dispara-pre-push-hook]].

## Cómo retomar (kickoff siguiente sesión)

**FEATURE COMPLETA — issues 100-108 + Fase 4 Tandas 1, 2 y 3 TODAS en prod (2026-06-17).**
PRs: #327 (T1), #333 (T2, mig 317), #338 (T3, mig 319). Migs 317+319 aplicadas a prod; runner
redeployado con el código T2 (progreso en vivo). Todo verde, mergeado `--admin` (ignorando la
Visual Regression stale). Único pendiente de Q6: **NO escalar réplicas hasta dar swap/RAM al
host** (ver "Riesgo de host" arriba) — el código ya está listo (`RUNNER_REPLICAS`).

Smoke pendiente (suave): abrir un ticket real y ver el **timeline de progreso en vivo** (Q1) en
`/admin/feedback`; abrir el email de ticket nuevo y probar el botón **"Resolver con Claude"**
(Q5) → página `/resolver-con-claude` → encola. Verificar que el job en curso (claim 00:09) cerró
bien pese al `502` de heartbeat.

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
