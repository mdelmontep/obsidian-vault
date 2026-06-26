---
title: top of mind
date: 2026-05-10
tags: [home, prioridades]
---

# Top of Mind

Índice transversal multi-proyecto. **NOW** = en lo que estás (máx 5). **NEXT** = lo inminente próximas 2 semanas, cross-cliente (1 línea + link al hub; el detalle vive en el hub). **Bloqueos** = esperando a terceros. El backlog completo de cada proyecto vive en su hub (ver `Vistas por cliente`), no aquí. Reestructurado 2026-06-26 (poda: backlog por-cliente devuelto a cada hub; backup en `00-home/archive/top-of-mind-pre-poda-2026-06-26.md`).

## NOW (máx 5)

- **TuFacturaIA — notifs fiscal residuales (manual)** — marcar leídas notifs viejas + abrir/recalcular borradores 130 2T/3T/4T (drift abono B2026-0001) + check visual drawer. [[facturaia]]
- **Centro Elphis — go-live** — hardening ✅; pendiente todo externo (Pablo coexistencia WA, 4 plantillas HSM, 659→Cloud API, DPAs Enrique, sesión crisis, número Alba). [[clientes/centro-elphis/index|centro-elphis]]
- **agency-portal — verificar extracción onboarding prod (PR #67)** — confirmar "Progreso por sección" + "Respuestas extraídas" por turno; si `onboarding.extraction_failed`, abrir issue. [[agentesia]]

## NEXT (próximas 2 semanas — inminente, cross-cliente)

- **TuFacturaIA — crear prices Stripe live de Plus** (29/278,40) + rotar env `STRIPE_PRICE_ID_PLUS_*` — desbloquea que el tier Plus sea comprable. [[facturaia]]
- **TuFacturaIA — smoke prod #517 (auditoría enforcement canales)** — cuenta active sigue facturando/usando bot igual; cuenta suspendida recibe corte por canal voz/WA; verifactu cert solo admin. [[facturaia]]
- **TuFacturaIA — pagar GitHub Advanced Security (~16 jul 2026)** — si caduca el trial se apaga Code Quality (scan + gate PR). [[facturaia]]
- **TuFacturaIA — responder tickets** — Abba BORME (re-escanear 2 docs → gonzalo.riera) + bgchivite `1762f07e` (deploy #209 en prod). [[facturaia]]
- **Simarro — verificación E2E reserva tras recableo (06-25)** — 1 reserva por voz + 1 por WA → evento con calle+`location` + tarea Meeting + email. [[simarro]]
- **agency-portal — Pizarra/board PR #91** — review+merge Borja (aplica mig `board_comments`) + QA visual Manu local (`PORT=3002`). [[agentesia]]
- **Tecnocloud — PR #3 voice-webhook-tickets** — pendiente review Dani → smoke E2E con llamada real. [[tecnocloud]]
- **EcoBox — smokes pendientes** — grúa/Mutua→handoff+email; reserva E2E que dispare `Build Emails`; chat hueco nuevo no-doble-booking. [[clientes/ecobox/index|ecobox]]
- **cryptobruj-bot — EN REAL, monitorizar** — scalp-5m/BTC BingX, tope $10, ~88 USDT; vigilar drawdown/ntfy. Revertir: `EXCHANGE_TESTNET=true`.

## Bloqueos (esperando a terceros)

- **TuFacturaIA — billing GitHub Actions re-bloqueado (Manu)** — desde 17/06 jobs mueren a 0 pasos (spending limit). Subir límite en Settings → Billing org `AgentesIA-MAdrid`. **Mientras siga, merges con `gh pr merge --admin`** (requiere OK explícito). Ver [[github-actions-org-private-free-tier-2000-min]].
- **TuFacturaIA — subir tier OpenAI (Manu)** — bot WhatsApp salta rate-limit (TPM 30k Tier 1). Subir a Tier 2 (450k) en platform.openai.com. (Ya no urge: 0 errores 429 en 30d.)
- **TuFacturaIA — HIBP leaked-password requiere Supabase Pro (Manu)** — toggle "Prevent leaked passwords" falla en free. Activar al subir a Pro.

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

## Completado reciente

Ver `00-home/archive-completed.md` · histórico TuFacturaIA en [[facturaia-historico-detallado]]
