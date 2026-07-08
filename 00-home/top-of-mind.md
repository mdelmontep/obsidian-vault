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
- **AGH Ibérica — #150 + triaje + cierre YA HECHOS, quedan 2 PRs por revisar de Borja** — PR #347 (deps vitest 2→4/TS 6, 0 vulns, gate verde) + PR #348 (docs status) abiertas sin mergear. Triaje: 11 issues→`ready-for-agent`, #85→`needs-info` (posible duplicado del dashboard CRM), #256 cerrado. **Próxima sesión**: mergear #347/#348, coger los `ready-for-agent` nuevos, decidir #85 con Borja. Dashboard CRM de Borja/Dani = proyecto paralelo, zona fría, ya en prod y navegable (#327). [[agh-iberica]]

## NEXT (próximas 2 semanas — inminente, cross-cliente)

- **TuFacturaIA — cobro Stripe Connect — todo lo previo PREPARADO, bloqueado SOLO en acción Manu (KYC)** — runbook completo en repo `docs/architecture/cobro-stripe-connect-runbook.md` (PR #781, incluye SQL de activación feature en AgentesiaLab). Prod usa `acct_1Td5ccGgQMT2aOqB` (sk_live), NO `acct_1TJrQvQY4tV8FMxQ` (la del CLI, setup por error). Pendiente = solo dashboard Stripe (`acct_1Td5cc`): KYC plataforma → webhook Connect LIVE (`account.updated`+`checkout.session.completed`) → `STRIPE_CONNECT_WEBHOOK_SECRET` Dokploy (container recreado). Hecho eso → aplicar SQL + smoke E2E. Ver [[stripe-cli-cuenta-distinta-de-la-app-price-no-existe-falso-positivo]]. [[facturaia]]
- **TuFacturaIA — QA export/bot: ojo facturas · menús canónicos · Pre303 HITL** (3 smokes prod restantes) — #681 mergeado y bot dual WhatsApp confirmado (2T real+3T estimado) 2026-07-05. Detalle en hub `Smoke tests pendientes`. [[facturaia]]
- **TuFacturaIA — smoke WhatsApp G5 canary: 3º y 4º bug destapados y arreglados (PR #796/#797), falta smoke final + OCR completo** — selector multi-org (PR #764) y logging Meta (PR #768) ya en prod. Nuevo: lote de fotos preguntaba empresa 1 vez por foto (riesgo de subir el doc equivocado) + botón "Cambiar empresa" salía con 1 sola empresa + doble tap podía duplicar la ingesta — los 3 arreglados 2026-07-08. Falta: confirmar en real que ya no sale "Cambiar empresa" con 1 empresa, reenviar documento fresco y confirmar OCR completo (estado=listo en bandeja_ingesta). Detalle en hub `Smoke tests pendientes`. [[facturaia]]
- **TuFacturaIA — /soporte: verificar #NNN + badge en admin (Manu)** — `/soporte` carga OK verificado en sandbox 2026-07-02 (bug del Dashboard arreglado); falta que Manu (superadmin) confirme `#NNN` + badge "IA revisando…" en `/admin/feedback` con un ticket de job activo (e2e+smoke no puede sin enviar feedback a soporte real). [[facturaia]]
- **TuFacturaIA — Slack completo (#002-#007c)** — todo en prod: OAuth, notifs, OCR, slash commands, bienvenida+modal OAuth, panel tip, created_via fix (#571). Pendiente: smoke escritura (vincular→`/factura cobrada`) + Manage Distribution (decisión negocio). [[facturaia]]
- **TuFacturaIA — smoke PRE Verifactu** — .p12 Gonzalo (~semana que viene) → validar namespace envelope SOAP + F1/F2 en prewww1.aeat.es. [[facturaia]]
- **TuFacturaIA — decidir ofrecer skin "Cristal" a usuarios** — QA contraste/APCA en pantallas densas hecho 2026-07-02 (sin fallos, oscuro+claro); queda solo la decisión de negocio de exponerlo. [[facturaia]]
- **TuFacturaIA — smoke prod #517 (auditoría enforcement canales) — BLOQUEADO por falta de fixture** — no hay ninguna org en prod con `billing_status` suspended/expired ahora mismo (todas active complimentary) para probar el corte de canal. No verificable hasta que exista un caso real o se cree uno de prueba a propósito. [[facturaia]]
- **TuFacturaIA — Marketing/Growth (panel interno admin) — 3/14 issues hechos vía TDD, resto BLOQUEADO en cuentas externas (2026-07-07)** — fundaciones+guardarráiles+cupones Stripe en verde (build/lint/typecheck); Google Ads/Meta Ads/GA4/GSC esperan a que Manu cree proyecto GCP+developer token, app Meta+App Review, propiedades GA4/GSC. [[facturaia]]
- **TuFacturaIA — pagar GitHub Advanced Security (~16 jul 2026)** — si caduca el trial se apaga Code Quality (scan + gate PR). [[facturaia]]
- **TuFacturaIA — Supabase org "EXCEEDING USAGE LIMITS" (gracia hasta 25 jul 2026)** — revisar plan/uso en dashboard o los proyectos se restringen tras esa fecha. [[facturaia]]
- **TuFacturaIA — responder tickets** — Abba BORME (re-escanear 2 docs → gonzalo.riera) + bgchivite `1762f07e` (deploy #209 en prod). [[facturaia]]
- **TuFacturaIA — UX feedback pendiente** — smoke prod #528 (toast guardar empresa/plantillas) + #529 (modal glass confirmación cambio precio en `/admin/plans`). [[facturaia]]
- **TuFacturaIA — emails unificados (#527 en prod)** — deploy Dokploy ✓ (confirmado: el 500 email-copy lo probó), schema-cache transitorio resuelto. Falta: **logo real** + smoke prod del resto de emails + verificar texto humanizado de alertas en panel/email (`e1f4fd66`, sin QA visual). [[facturaia]]
- **Simarro — verificación E2E reserva tras recableo (06-25)** — 1 reserva por voz + 1 por WA → evento con calle+`location` + tarea Meeting + email. [[simarro]]
- **agency-portal — Pizarra/board PR #91** — review+merge Borja (aplica mig `board_comments`) + QA visual Manu local (`PORT=3002`). [[agentesia]]
- **Tecnocloud — PR #3 voice-webhook-tickets** — pendiente review Dani → smoke E2E con llamada real. [[tecnocloud]]
- **EcoBox — smokes pendientes** — grúa/Mutua→handoff+email; reserva E2E que dispare `Build Emails`; chat hueco nuevo no-doble-booking. [[clientes/ecobox/index|ecobox]]
- **cryptobruj-bot — EN REAL, monitorizar** — scalp-5m/BTC BingX, tope $10, ~88 USDT; vigilar drawdown/ntfy. Revertir: `EXCHANGE_TESTNET=true`.

## Bloqueos (esperando a terceros)

- **TuFacturaIA — CI (Actions) bloqueado por billing (recurrente desde 2026-07-03, Manu)** — los jobs mueren en 2-4s con 0 pasos (spending-limit). Subir el límite en Settings→Billing de la org GitHub. Mientras tanto los merges van con `gh pr merge --admin` + verificación local (lint+typecheck+build, `node_modules` real en worktree); el ruleset además impide aprobar tu propio PR (auto-review imposible), así que el bypass no es solo por la CI caída. Refuerzo aprendido: los PR con UI necesitan QA visual en localhost antes del merge, no solo CI verde (#664 destapó 2 bugs que el runner headless dejó pasar). Historial PR-por-PR en `archive-completed.md`. Ver [[gh-pr-merge-no-confirma-verificar-state-merged]] · [[actions-sin-billing-hooks-locales-unico-gate]] · [[facturaia-tokens-admin-sin-definir]].
- **TuFacturaIA — subir tier OpenAI (Manu)** — bot WhatsApp salta rate-limit (TPM 30k Tier 1). Subir a Tier 2 (450k) en platform.openai.com. (Ya no urge: 0 errores 429 en 30d.)
- **TuFacturaIA — HIBP leaked-password requiere Supabase Pro (Manu)** — toggle "Prevent leaked passwords" falla en free. Activar al subir a Pro.
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
| AGH Ibérica | [[agh-iberica]] | Agente "Carlos" · **PROD VIVO** · #150+triaje hechos, PRs #347/#348 a revisión Borja |

## Completado reciente

Ver `00-home/archive-completed.md` · histórico TuFacturaIA en [[facturaia-historico-detallado]]
