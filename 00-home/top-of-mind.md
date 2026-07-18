---
title: top of mind
date: 2026-05-10
tags: [home, prioridades]
---

# Top of Mind

Índice transversal multi-proyecto. **NOW** = en lo que estás (máx 5). **NEXT** = lo inminente próximas 2 semanas, cross-cliente (1 línea + link al hub; el detalle vive en el hub). **Bloqueos** = esperando a terceros. El backlog completo de cada proyecto vive en su hub (ver `Vistas por cliente`), no aquí. Reestructurado 2026-06-26 (poda: backlog por-cliente devuelto a cada hub; backup en `00-home/archive/top-of-mind-pre-poda-2026-06-26.md`).

## NOW (máx 5)

- **Centro Elphis — 659 en Cloud API + bot WA real VIVO (17-jul)** — migrado vía A + prompt afinado ("nuestro director", paciente/familiar, `*` correcto, reutiliza contexto) + 2 cuentas Chatwoot recepción admin. Pendiente: rotar `META_APP_SECRET` (expuesto en captura), **plantilla HSM para reservas por VOZ** (texto libre falla fuera de ventana 24h), DPAs Enrique, sesión crisis, número directo Alba. [[clientes/centro-elphis/index|centro-elphis]]
- **agency-portal — verificar extracción onboarding prod (PR #67)** — confirmar "Progreso por sección" + "Respuestas extraídas" por turno; si `onboarding.extraction_failed`, abrir issue. [[agentesia]]
- **AGH Ibérica — agente "Carlos" PROD VIVO · 16-jul: coherencia del prompt + composición multi-write en prod** — **#529** (auditoría de coherencia del `SYSTEM_PROMPT`: catálogo `capabilities` completo, regla única «apuntar», `email.send` en sub-viñetas, `#231` consolidado) + **#530** (composición multi-write explícita, política pro-precisión, con ejes de eval nuevos `composition`/`confusion`). Descubrimiento clave: el modelo YA componía por generalización → el cambio es **blindaje, no fix** (foto ×3 antes de tocar el prompt) → [[prompt-coherencia-fotografiar-evals-antes]]. Gate 1632/1632 + evals ×3 98.4% sin regresiones + backstop `.pg` 182/182. Antes (15-jul): #519 (cita FORWARD) + #520 («lo último» no-cliente) ya en prod. **Pendiente de terceros:** ojo post-hoc de **Borja** a F2/F3 del prompt + **#521** (deixis/ordinales, secuenciar con #454, zona Borja). **Abiertos para next:** **#531** (señales de descubrimiento en Langfuse) · **#532** (`meeting.update` con `participants` aditivo, para el «añade a la reunión» add-after). L5/L3-A bloqueados RGPD. Detalle → [[agh-iberica]]

## NEXT (próximas 2 semanas — inminente, cross-cliente)

- **TuFacturaIA — auditoría de cifrado en PR #998 (18-jul): Fase 1 (cripto PII/cert/kid) + Fase 2 (migs 513-515: cifrado IBAN dual-write + hash tokens fiscal/phone) — migs validadas en Supabase local.** B4/B6 decididos (ADR-010 env+hardening; TTL 7d). Antes del merge: envs `PII_BANK_*` (64-hex distintas) + `db push` migs 513-515 + `gen:types` + smoke E2E (A6/A2/A3). Pendiente orden estricto: B1 backfill prod → A7 matching bidx → B2 cutover. Handoff: [[facturaia-cifrado-continuacion]]. [[facturaia]]
- **TuFacturaIA — landing captación `/verifactu` (lead magnet) + panel admin de leads + email con diseño EN PROD (PRs #997/#1002, mig 512, 18-jul)** — test VeriFactu público (A/B/C + factura por WhatsApp) → `marketing_leads` + aviso email plantilla + `/admin/leads`. Opcional: env `MARKETING_LEADS_NOTIFY_EMAILS`. Ideas futuras (ebook, banner retención, canal asesorías) en hub. [[facturaia]]
- **TuFacturaIA — copy anti-slop (PR #996, 18-jul)** — quitados tells de IA (em-dash) en marketing/emails/in-app/manual-usuario + guardarraíl `copy-humano.md`. Pendiente: merge #996 + rehacer de-slop de `manual-admin.md` (subagente no escribió). Ver [[copy-espanol-raya-tell-ia-dominante]]. Detalle en hub. [[facturaia]]
- **TuFacturaIA — módulo OCR: gate real `auto_categorizar` + métricas de aprendizaje IA (auto_accuracy + progreso al gate) + polish EN PROD (PR #990, 2026-07-18)** — 2 smokes en hub (toggle categoría OFF; %precisión con ≥50 decisiones). Detalle en hub. [[facturaia]]
- **TuFacturaIA — cashflow base caja + capa Vencimientos + fixes de smoke EN PROD (PRs #986/#987/#988 + mig 495, 2026-07-17)** — saldo 90d ya no duplica; calendario con capa Vencimientos + aclaración caja; KPIs "Salud del negocio" arreglados en Vista cliente. Pendiente: smoke Manu (refrescar Vista cliente → tarjetas), bug tragado `fiscal_plazos.org_id` (baja sev) y reconciliar migs timestamp (con Obras). Detalle en hub. [[facturaia]]
- **TuFacturaIA — importar facturas externas (emitidas/recibidas OCR) EN CURSO, rama sin mergear** — registro espejo sin VeriFactu (ADR-038); backend+OCR+UI hechos y QA'd (dropzone glass); falta aplicar mig 470 a prod → luego UI que la lee + F6/F7. Detalle en hub «WIP». [[facturaia]]
- **TuFacturaIA — Módulo Obras (mini-ERP instalaciones, sustituye WAPI) EN PRODUCCIÓN.** Núcleo + FASE 2 + **FASE 3 (PR #999, 18-jul)** mergeados a main y con smoke prod verde. FASE 3 = decisiones de Natalia: coste MO fiel (tarifa por instalador, precio hora especial por obra, dieta default, calendario mensual de partes), módulo **Herramientas** (foto+event log+alta por WhatsApp vía copiloto), corregir descuento/precio desde recibida, **proforma a origen** (informe PDF, NO createDocument, ADR-obras-001), generar pedido desde presupuesto con expansión de UO, chip recibido X/Y. Migs 471-511 reconciliadas (schema_migrations local==remote). `/fia-cierre` cross-issue cazó 2 bloqueantes que los gates por-issue no vieron (`.or()` sin entrecomillar en tools copiloto con test mock no-op → ver [[postgrest-or-no-escapa-delimitadores]]; clave React/dedup rota al componer olas). **Org REAL de Natalia YA existe y con sector ACTIVO**: "Instalaciones Eléctricas y de Telecomunicación, S.A." (`b9d5d6f7-…`, is_test=false, creada 16-jul, miembro `administracion@iet.es`). Sembrado el catálogo de **745 tipos M.O.** (copiado del Sandbox, suma horas 3826,901 idéntica, 18-jul). **Pendiente = carga inicial que hace ELLA**: importar materiales/tarifas (CSV Telematel), instaladores + matriz tarifas hora (extra 25€), ajustes (+33%, dieta). Docs `docs/architecture/obras/fase3-plan-decisiones.md` + ADRs 001/002/003. [[facturaia]]
- **TuFacturaIA — provider IMAP genérico ACTIVO en prod (6 PRs, mig 466+469, 2026-07-17)** — conectar cualquier servidor IMAP (SSRF pinning verificado); botón "Otro (IMAP)" operativo; falta smoke real del cliente de Manu. [[facturaia]]
- **TuFacturaIA — registro standalone + onboarding claro + validación en vivo ACTIVO en prod (PR #984, 2026-07-17)** — falta smoke prod; pendiente aparte: mismo bug de `.field` sin diseño en 3 modales no tocados. [[facturaia]]
- **TuFacturaIA — multi-cuenta email por proveedor COMPLETA en prod (7 PRs, mig 464, 2026-07-16)** — Gmail/M365/iCloud admiten N cuentas por org; falta reconectar 2ª cuenta real para smoke round-trip (login OAuth interactivo). [[facturaia]]
- **TuFacturaIA — prompt caching copiloto en prod (#894)** — smoke pendiente (grep logs del host por `copiloto/cache`). [[facturaia]]
- **TuFacturaIA — UI polish sidebar/clientes/facturas en prod (#882/#883/#884)** — smoke pendiente. [[facturaia]]
- **TuFacturaIA — Centro Fiscal (#825) en prod + migs 452/453** — solo smoke prod fiscal pendiente (Manu). [[facturaia]]
- **TuFacturaIA — cuadres fiscales rediseñados (#835 mergeado)** — 2 follow-ups (smoke 390 + bug gating hub /fiscal) en hub «Smoke». [[facturaia]]
- **TuFacturaIA — cobro Stripe Connect** — todo preparado, bloqueado solo en acción Manu (KYC dashboard `acct_1Td5cc`). [[facturaia]]
- **TuFacturaIA — QA export/bot** — 3 smokes prod restantes (ojo facturas · menús canónicos · Pre303 HITL). [[facturaia]]
- **TuFacturaIA — retirada de n8n (WhatsApp) completa en código (5 PRs)** — faltan re-smokes prod #2/#3/#4 + Fase 6. [[facturaia]]
- **TuFacturaIA — /soporte: Manu verifica #NNN + badge en admin** — carga OK; falta confirmación superadmin. [[facturaia]]
- **TuFacturaIA — Slack completo (#002-#007c) en prod** — falta smoke escritura + decisión Manage Distribution. [[facturaia]]
- **TuFacturaIA — smoke PRE Verifactu (ÚNICO paso a operacional; PR #947 + mig 465 ya en prod)** — bloqueado solo por certificado: .p12 Gonzalo → subir en Ajustes→VERIFACTU → SOAP F1/F2 en prewww1.aeat.es. [[facturaia]]
- **TuFacturaIA — decidir ofrecer skin "Cristal"** — QA APCA sin fallos; queda decisión de negocio (en hub «Smoke»). [[facturaia]]
- **TuFacturaIA — smoke #517 enforcement canales** — BLOQUEADO por falta de fixture (org suspended); en hub «Smoke». [[facturaia]]
- **TuFacturaIA — Marketing/Growth infra en prod (#799/#801)** — smoke prod pendiente; resto bloqueado en cuentas externas. [[facturaia]]
- **TuFacturaIA — pagar GitHub Advanced Security (~16 jul)** — si caduca el trial se apaga Code Quality. [[facturaia]]
- **TuFacturaIA — vista móvil 2ª ola COMPLETA en prod (15/16-jul, 8 PRs)** — migración 463 aplicada+verificada, push server-side (#929), manual+gestos (#928/#930), smoke visual con Artifact, blur calibration validada. Solo queda confirmar deploy Dokploy del env VAPID. Ver [[facturaia-vista-movil-segunda-ola]]. [[facturaia]]
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
| AGH Ibérica | [[agh-iberica]] | Agente "Carlos" · **PROD VIVO** · secretaria (P1/P2/P5) + #451 `ClientIntake` + #485 (audit) + #482-p1 (self-recipient) + auditoría de comunicación (#511/#514/#522) + #519/#520 + **#529 coherencia prompt + #530 composición multi-write** en prod; pendiente terceros: ojo de Borja a F2/F3 del prompt + #521 (#454); next: #531 (Langfuse), #532 (meeting.update participants); L5/L3-A bloqueados RGPD |

## Completado reciente

Ver `00-home/archive-completed.md` · histórico TuFacturaIA en [[facturaia-historico-detallado]]
