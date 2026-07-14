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

- **TuFacturaIA — prompt caching copiloto EN PROD (PR #894, 2026-07-14) — smoke pendiente** — cachea el historial (antes solo system+tools) + log `[copiloto/cache]`. Smoke: grep logs del host por `copiloto/cache`, `cacheRead>0`/`hitRatio>0` en turnos con historial (comando en el hub). [[facturaia]]
- **TuFacturaIA — UI polish sidebar/clientes/facturas EN PROD (#882/#883/#884, 2026-07-14) — smoke pendiente** — sidebar glass = Opción B confirmada (en prod desde 07-07); bulk en tarjetas de Clientes, skeleton-que-calca en emitidas/recibidas, fix teclado (checkbox no abre detalle). Smoke en el hub. [[facturaia]]
- **TuFacturaIA — Centro Fiscal (#825) MERGEADO + migs 452/453 en prod (2026-07-13) — solo smoke pendiente** — auditoría de los 9 modelos: 8 críticos + 2 medios corregidos (el más grave: `aprobar_recibida_con_lineas` gateaba `lineas_factura` por feature `stock` → starter declaraba 0€ en todo el Centro Fiscal). Mergeado `--admin --squash` (Manu nombró el bypass); migs aplicadas ANTES del merge (schema antes que deploy) y verificadas en BD (columna `situacion_inmueble` + `fiscal_plazos` 111/115/180/190/347). **Pendiente Manu**: smoke prod fiscal (180/347/303 sin 42703) + HITL export posicional/sandbox AEAT (necesita certificado). Detalle+smokes en el hub. [[facturaia]]
- **TuFacturaIA — cuadres fiscales rediseñados (PR #835 mergeado) — 2 follow-ups** — (1) smoke prod del "Resolver aquí" del 390 (drawer con enlaces a cada 303; declaraciones cacheadas necesitan Recalcular para chips `1T/3T`). (2) BUG pre-existente sin tocar: el hub `/fiscal/{ejercicio}` redirige a `/` para no-superadmin (feature `fiscal` en `proximamente`) → rompe el breadcrumb "2026" y el nav "Centro fiscal" para usuarios normales; decidir si se arregla (alinear gating hub↔detalle). Ver [[gating-de-modulo-duplicado-por-pagina-centralizar-en-helper]]. [[facturaia]]
- **TuFacturaIA — cobro Stripe Connect — todo lo previo PREPARADO, bloqueado SOLO en acción Manu (KYC)** — runbook completo en repo `docs/architecture/cobro-stripe-connect-runbook.md` (PR #781, incluye SQL de activación feature en AgentesiaLab). Prod usa `acct_1Td5ccGgQMT2aOqB` (sk_live), NO `acct_1TJrQvQY4tV8FMxQ` (la del CLI, setup por error). Pendiente = solo dashboard Stripe (`acct_1Td5cc`): KYC plataforma → webhook Connect LIVE (`account.updated`+`checkout.session.completed`) → `STRIPE_CONNECT_WEBHOOK_SECRET` Dokploy (container recreado). Hecho eso → aplicar SQL + smoke E2E. Ver [[stripe-cli-cuenta-distinta-de-la-app-price-no-existe-falso-positivo]]. [[facturaia]]
- **TuFacturaIA — QA export/bot: ojo facturas · menús canónicos · Pre303 HITL** (3 smokes prod restantes) — #681 mergeado y bot dual WhatsApp confirmado (2T real+3T estimado) 2026-07-05. Detalle en hub `Smoke tests pendientes`. [[facturaia]]
- **TuFacturaIA — RETIRADA DE n8n (WhatsApp) COMPLETA en código — 5 PRs mergeados 2026-07-10, faltan smokes prod** — n8n receptor `pqSWkDIHqmSVHotB` fuera del runtime (active:false, 0 ejec); receptor real = `src/app/api/whatsapp/webhook`. Auditoría destapó 2 regresiones del cutover (arregladas: opt-out STOP #814 · extractos por foto #816+mig451) y 2 flujos huérfanos portados (facturar-movimiento como tool copiloto #820 · cobro-confirmar cliente-final #822) + docs #817. Mig 451 (`bandeja_remitente_wa`) aplicada a prod por MCP (db push bloqueado por red). **Smokes prod (10-jul noche): 1 STOP ✅ · 2 extracto foto ✅** (fix #823 `detail:high` subió 2→8 de 9 movs; falta solo la nómina/único positivo — para 9/9 evaluar gpt-4o) **· 3 facturar-movimiento ❌→FIX MERGEADO** (repro real: usuario dijo "registra el gasto del cargo de 657,32…" → LLM llamó `searchMovimientos({query:"657.32"})`; el ILIKE va solo sobre `descripcion`, que no contiene el importe → count 0. Fix PR #824: `parseMontoQuery` reinterpreta query numérico como importe exacto + filtro abs a la query DB vía `.or()`. Verificado en BD) **· 4 cobro-confirmar ⏳** (necesita teléfono NO-miembro cliente con factura abierta). **UX ack extracto ✅ FIX MERGEADO** (#824: ack de encolado neutro "Recibido, estoy leyendo…" + confirmación de cierre solo para factura "Listo, está en tu bandeja"; el extracto ya no ve el ack contradictorio). **Ambos fixes en main 77daa397 (2026-07-11), deploy auto en curso.** Pendiente: re-smoke prod #2/#3 + #4 tras deploy. **Fase 6 (limpieza+archivar workflow) SIGUE POSPUESTA hasta smokes OK** (n8n=rollback). Detalle: memoria agente `project_facturaia_retirada_n8n`. [[facturaia]]
- **TuFacturaIA — /soporte: verificar #NNN + badge en admin (Manu)** — `/soporte` carga OK verificado en sandbox 2026-07-02 (bug del Dashboard arreglado); falta que Manu (superadmin) confirme `#NNN` + badge "IA revisando…" en `/admin/feedback` con un ticket de job activo (e2e+smoke no puede sin enviar feedback a soporte real). [[facturaia]]
- **TuFacturaIA — Slack completo (#002-#007c)** — todo en prod: OAuth, notifs, OCR, slash commands, bienvenida+modal OAuth, panel tip, created_via fix (#571). Pendiente: smoke escritura (vincular→`/factura cobrada`) + Manage Distribution (decisión negocio). [[facturaia]]
- **TuFacturaIA — smoke PRE Verifactu** — .p12 Gonzalo (~semana que viene) → validar namespace envelope SOAP + F1/F2 en prewww1.aeat.es. [[facturaia]]
- **TuFacturaIA — decidir ofrecer skin "Cristal" a usuarios** — QA contraste/APCA en pantallas densas hecho 2026-07-02 (sin fallos, oscuro+claro); queda solo la decisión de negocio de exponerlo. [[facturaia]]
- **TuFacturaIA — smoke prod #517 (auditoría enforcement canales) — BLOQUEADO por falta de fixture** — no hay ninguna org en prod con `billing_status` suspended/expired ahora mismo (todas active complimentary) para probar el corte de canal. No verificable hasta que exista un caso real o se cree uno de prueba a propósito. [[facturaia]]
- **TuFacturaIA — Marketing/Growth (panel interno admin) — infra 000/003/012 EN PROD (#799/#801, 2026-07-08), resto BLOQUEADO en cuentas externas** — fundaciones+guardarráiles+auditoría+cupones desplegados (migs 447/448 aplicadas, tipos regen, casts fuera). Pendiente sin bloqueo: smoke prod (`/admin/marketing/limites`+`/auditoria` como superadmin) + criterio 4 de 003 diferido a issues 004/008. Google Ads/Meta Ads/GA4/GSC esperan a que Manu cree proyecto GCP+developer token, app Meta+App Review, propiedades GA4/GSC. [[facturaia]]
- **TuFacturaIA — pagar GitHub Advanced Security (~16 jul 2026)** — si caduca el trial se apaga Code Quality (scan + gate PR). [[facturaia]]
- **TuFacturaIA — vista móvil nativa + PWA: PR0-PR2 EN PROD (2026-07-15, #895/#900/#899)** — home nativo (hero cobro=KPI desktop, KPIs, vencimientos, ingesta) + shell (header/tabbar) + PWA instalable, en main. Pendiente: smoke iOS/PWA en dispositivo real + **PR3-PR6** (sheet "+" con cámara, tab Facturas nativa, tab Documentos, menú "Más"; issues `mobile-11..14`). Detalle+smoke en el hub. [[facturaia]]
- **TuFacturaIA — Supabase SUBIDO A PRO (2026-07-10)** — el egress reventó y tumbó prod ~1h (404 Traefik + login roto, acelerado por QA pesado; ver incidents/learning). Ya no urge; vigilar uso mensual. NO bajar a Free (recurre + BD supera límites). [[facturaia]]
- **TuFacturaIA — responder tickets** — Abba BORME (re-escanear 2 docs → gonzalo.riera) + bgchivite `1762f07e` (deploy #209 en prod). [[facturaia]]
- **TuFacturaIA — UX feedback pendiente** — smoke prod #528 (toast guardar empresa/plantillas) + #529 (modal glass confirmación cambio precio en `/admin/plans`). [[facturaia]]
- **TuFacturaIA — emails unificados (#527 en prod)** — deploy Dokploy ✓ (confirmado: el 500 email-copy lo probó), schema-cache transitorio resuelto. Falta: **logo real** + smoke prod del resto de emails + verificar texto humanizado de alertas en panel/email (`e1f4fd66`, sin QA visual). [[facturaia]]
- **TuFacturaIA — rotar secrets tras fuga Dokploy (Capa 2)** — Capa 1 (guardarraíl anti-fuga) cerrada+deploy verificado (#870); falta rotar los secrets expuestos el 07-03 (alcance pragmático ya decidido, empezar Supabase→Stripe→Meta). Runbook en `ops/security/README.md`. Fuga fue a transcript privado. [[facturaia]]
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
