---
title: top of mind
date: 2026-05-10
tags: [home, prioridades]
---

# Top of Mind

Índice transversal multi-proyecto. **NOW** = en lo que estás (máx 5). **NEXT** = lo inminente próximas 2 semanas, cross-cliente (1 línea + link al hub; el detalle vive en el hub). **Bloqueos** = esperando a terceros. El backlog completo de cada proyecto vive en su hub (ver `Vistas por cliente`), no aquí. Reestructurado 2026-06-26 (poda: backlog por-cliente devuelto a cada hub; backup en `00-home/archive/top-of-mind-pre-poda-2026-06-26.md`).

## NOW (máx 5)

- **Centro Elphis — go-live bloqueado en conexión nº real** — hardening ✅; chatbot WA E2E ✅ 30-jun. Bloqueo: negocio sin verificar (iniciar verif. KISAMU/Enrique) + decidir migración 659→Cloud API vs coexistencia(BSP); plantillas+bot real bloqueados hasta eso. App+token Meta nuevos (rotar token). Resto: DPAs Enrique, sesión crisis, número Alba. [[clientes/centro-elphis/index|centro-elphis]]
- **agency-portal — verificar extracción onboarding prod (PR #67)** — confirmar "Progreso por sección" + "Respuestas extraídas" por turno; si `onboarding.extraction_failed`, abrir issue. [[agentesia]]
- **AGH Ibérica — agente "Carlos" PROD VIVO · 14-jul noche: auditoría de COMUNICACIÓN cerrada** — 5 lentes sobre 441 trazas Langfuse, verificado contra `main` actual (el corpus era pre-fix; casi re-fixeo 3 bugs ya resueltos → [[verificar-que-el-bug-sigue-vivo-contra-codigo-actual-antes-de-fixear]]). En prod: **#511** (breaker del clarify en bucle, mig 0020) · **#514** (`client.prep` «prepárame lo de X») · **#522** (`note.create` nota por voz). **Pendiente de terceros:** **PR #519** (cita FORWARD, revisión de **Dani**/m365) · **#520** (corregir «lo último» no-cliente) y **#521** (deixis/ordinales, fork de diseño #247) → zona/nod de **Borja** (secuenciar con #454). Cerrados por análisis: #512/#513/#523/#525. Mañana temprano: #485/#482-p1/#452/#508 (audit del agente, self-recipient, módulo temporal, git-guard). L5/L3-A bloqueados RGPD. Detalle → [[agh-iberica]]

## NEXT (próximas 2 semanas — inminente, cross-cliente)

- **TuFacturaIA — prompt caching copiloto en prod (#894)** — smoke pendiente (grep logs del host por `copiloto/cache`). [[facturaia]]
- **TuFacturaIA — UI polish sidebar/clientes/facturas en prod (#882/#883/#884)** — smoke pendiente. [[facturaia]]
- **TuFacturaIA — unificación UI: Fase 4 Punto 1 + drenaje hex HECHOS (11 PRs 15/16-jul, hex 1327→465, lint:css 158→34)** — Punto 1 (SortableTh + Segmented superset + admin tabs) + tokenización total de hex a suelo legítimo. Queda estructural: inline-styles 856, admin.css `.adm-*`→primitivos, vaciar globals.css, ampliar token-system. Drawers (P2) y Card (P6) descartados por evidencia. Prompt de cierre multi-agente+/loop en memoria `project_unificacion_ui_facturaia`. [[facturaia]] · Ver [[verificar-primitivo-cubre-comportamiento-antes-de-consolidar-reinvencion]]
- **TuFacturaIA — Centro Fiscal (#825) en prod + migs 452/453** — solo smoke prod fiscal pendiente (Manu). [[facturaia]]
- **TuFacturaIA — cuadres fiscales rediseñados (#835 mergeado)** — 2 follow-ups (smoke 390 + bug gating hub /fiscal) en hub «Smoke». [[facturaia]]
- **TuFacturaIA — cobro Stripe Connect** — todo preparado, bloqueado solo en acción Manu (KYC dashboard `acct_1Td5cc`). [[facturaia]]
- **TuFacturaIA — QA export/bot** — 3 smokes prod restantes (ojo facturas · menús canónicos · Pre303 HITL). [[facturaia]]
- **TuFacturaIA — retirada de n8n (WhatsApp) completa en código (5 PRs)** — faltan re-smokes prod #2/#3/#4 + Fase 6. [[facturaia]]
- **TuFacturaIA — /soporte: Manu verifica #NNN + badge en admin** — carga OK; falta confirmación superadmin. [[facturaia]]
- **TuFacturaIA — Slack completo (#002-#007c) en prod** — falta smoke escritura + decisión Manage Distribution. [[facturaia]]
- **TuFacturaIA — smoke PRE Verifactu** — .p12 Gonzalo → SOAP F1/F2 en prewww1.aeat.es. [[facturaia]]
- **TuFacturaIA — decidir ofrecer skin "Cristal"** — QA APCA sin fallos; queda decisión de negocio (en hub «Smoke»). [[facturaia]]
- **TuFacturaIA — smoke #517 enforcement canales** — BLOQUEADO por falta de fixture (org suspended); en hub «Smoke». [[facturaia]]
- **TuFacturaIA — Marketing/Growth infra en prod (#799/#801)** — smoke prod pendiente; resto bloqueado en cuentas externas. [[facturaia]]
- **TuFacturaIA — pagar GitHub Advanced Security (~16 jul)** — si caduca el trial se apaga Code Quality. [[facturaia]]
- **TuFacturaIA — vista móvil 2ª ola COMPLETA en prod (15/16-jul, 8 PRs)** — migración 463 aplicada+verificada, push server-side (#929), manual+gestos (#928/#930), smoke visual con Artifact. Solo queda: confirmar deploy Dokploy del env VAPID + **blur calibration bloqueada esperando fotos de Manu**. Ver [[facturaia-vista-movil-segunda-ola]]. [[facturaia]]
- **TuFacturaIA — Supabase subido a Pro (10-jul)** — egress tumbó prod ~1h; ya no urge, vigilar uso, NO bajar a Free. [[facturaia]]
- **TuFacturaIA — OCR auto-orientación + scroll-fade toolbars en prod (#905)** — smoke en hub «Smoke». [[facturaia]]
- **TuFacturaIA — responder tickets** — Abba BORME + bgchivite `1762f07e` (#209); en hub «Smoke». [[facturaia]]
- **TuFacturaIA — UX feedback smoke #528/#529** — toast guardar + modal glass precio; en hub «Smoke». [[facturaia]]
- **TuFacturaIA — emails unificados (#527 en prod)** — falta logo real + smoke resto de emails. [[facturaia]]
- **TuFacturaIA — rotar secrets tras fuga Dokploy (Capa 2)** — Capa 1 cerrada (#870); rotar Supabase→Stripe→Meta. [[facturaia]]
- **Simarro — verificación E2E reserva tras recableo (06-25)** — 1 reserva por voz + 1 por WA → evento con calle+`location` + tarea Meeting + email. [[simarro]]
- **agency-portal — Pizarra/board PR #91** — review+merge Borja (aplica mig `board_comments`) + QA visual Manu local (`PORT=3002`). [[agentesia]]
- **Tecnocloud — PR #3 voice-webhook-tickets** — pendiente review Dani → smoke E2E con llamada real. [[tecnocloud]]
- **EcoBox — smokes pendientes** — grúa/Mutua→handoff+email; reserva E2E que dispare `Build Emails`; chat hueco nuevo no-doble-booking. [[clientes/ecobox/index|ecobox]]
- **cryptobruj-bot — EN REAL, monitorizar** — scalp-5m/BTC BingX, tope $10, ~88 USDT; vigilar drawdown/ntfy. Revertir: `EXCHANGE_TESTNET=true`.

## Bloqueos (esperando a terceros)

- **TuFacturaIA — CI (Actions) bloqueado por billing (recurrente desde 2026-07-03, Manu)** — los jobs mueren en 2-4s con 0 pasos (spending-limit). Subir el límite en Settings→Billing de la org GitHub. Mientras tanto los merges van con `gh pr merge --admin` + verificación local (lint+typecheck+build, `node_modules` real en worktree); el ruleset además impide aprobar tu propio PR (auto-review imposible), así que el bypass no es solo por la CI caída. Refuerzo aprendido: los PR con UI necesitan QA visual en localhost antes del merge, no solo CI verde (#664 destapó 2 bugs que el runner headless dejó pasar). Historial PR-por-PR en `archive-completed.md`. Ver [[gh-pr-merge-no-confirma-verificar-state-merged]] · [[actions-sin-billing-hooks-locales-unico-gate]] · [[facturaia-tokens-admin-sin-definir]].
- **TuFacturaIA — subir tier OpenAI (Manu)** — bot WhatsApp salta rate-limit (TPM 30k Tier 1). Subir a Tier 2 (450k) en platform.openai.com. (Ya no urge: 0 errores 429 en 30d.)
- **TuFacturaIA — HIBP leaked-password YA ACTIVABLE (Supabase en Pro desde 10-jul)** — activar el toggle "Prevent leaked passwords" en el dashboard de Auth.
- **agentesia-skills — PR #3 `onboarding-tour-spotlight`** — pendiente review de alguien del equipo antes de mergear (convención del repo: no merge directo a main).
- **TuFacturaIA — Salt Edge Test access (Manu)** — sin esto no se puede validar PR #610 (draft) contra sandbox real; además tiene un bug real de fuga cross-tenant sin resolver (re-revisado 2026-07-05, NO mergeado). Aprobar en dashboard Salt Edge → seguir en [[facturaia]].

## Vistas por cliente (el backlog vive en cada hub)

| Cliente | Hub | Estado |
|---|---|---|
| TuFacturaIA | [[facturaia]] | Activo · NEXT/Smoke/LATER en el hub |
| Agentesia / agency-portal | [[agentesia]] | Onboarding portal + chatbot ticketing |
| Simarro | [[simarro]] | Matching + voz/WA + outbound |
| Clínica Zen | [[clinica-zen]] | status_id Kommo + Retell leads |
| Tecnocloud | [[tecnocloud]] | PR #3 voice-webhook + voz Laura |
| EcoBox | [[clientes/ecobox/index\|ecobox]] | Voz+chat LIVE · smokes pendientes |
| Centro Elphis | [[clientes/centro-elphis/index\|centro-elphis]] | Go-live (externos) |
| IET | [[iet]] | iet.es en producción · pendientes menores |
| AGH Ibérica | [[agh-iberica]] | Agente "Carlos" · **PROD VIVO** · secretaria (P1/P2/P5) + #451 `ClientIntake` + #485 (audit) + #482-p1 (self-recipient) + **auditoría de comunicación** (#511 breaker clarify, #514 `client.prep`, #522 `note.create`) en prod; pendiente terceros: PR #519 (Dani), #520/#521 (Borja/#454); L5/L3-A bloqueados RGPD |

## Completado reciente

Ver `00-home/archive-completed.md` · histórico TuFacturaIA en [[facturaia-historico-detallado]]
