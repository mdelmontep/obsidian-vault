---
title: facturaia
date: 2026-05-10
tags: [cliente, facturaia, hub]
---

# FacturaIA — Hub maestro

App SaaS de facturación con IA (OCR, agente WhatsApp, voz, recomendador). Multi-tenant. **Este archivo es el ÚNICO punto de entrada al proyecto.** Todo lo nuevo (idea, pendiente, smoke test, decisión, doc) entra aquí o se enlaza desde aquí.

## Cómo usar este hub

- **Al empezar sesión FacturaIA**: leer este archivo entero. Es la foto del proyecto.
- **Durante**: añadir cualquier cosa nueva en su sección. No esperar al final.
- **Al cerrar sesión**: `/obsidian-1` propondrá actualizar las secciones tocadas + mover lo cerrado a `## Histórico`.
- **Reglas**: 1-2 líneas por entrada. Si necesita más, link a subfile en `knowledge/projects/agentesia/facturaia-*.md`.

---

## Estado actual

- **Producción**: facturaia.agentesia.world (Dokploy)
- **Stack**: Next 16 + Supabase (proyecto `lahqlyaxvobqjgdiftag`) + n8n + OpenAI Vision + Anthropic Claude
- **Plan comercial**: Starter / Pro / Enterprise + add-ons (Conciliación 19€, Anti-fraude 9€, +21 con badge Próximamente)
- **Orgs activas en prod**: AgentesiaLab (Enterprise), tecnocloud (Enterprise), Borja Galván (Enterprise), AgenteIA PRUEBA (Starter)
- **Última deploy mayor**: 2026-05-08 (PR #47 audit log + idempotency)
- **Tests Vitest**: 175+ pasando (HMAC, cursor, idempotency, SERIE_BY_TIPO, IVA, rate-limit)

---

## NOW (trabajo activo)

- **Bloque 1 — generar-view form manual** (commit `820684b`, 2026-05-07) — corregido `SERIE_POR_TIPO` (proforma F, abono eliminado), `tipo_documento` seteado en INSERTs, rama proforma cae en presupuestos. Abono manual desde generar-view eliminado por incumplir RD 1619/2012. Nuevo flujo: botón "Anular y emitir abono" en detalle de factura emitida con selector R1-R5 (`POST /api/facturas/[id]/anular`). `GET /api/render-pdf?tipo=&id=` (cierra 404 "Ver PDF" en presupuestos). `/api/email/send` acepta `presupuesto_id` (`sendPresupuestoByEmail` lib nueva)
- **Cumplimiento fiscal: referencia en abonos** — PDF de abono debe mostrar nº y fecha de la factura original que rectifica. Campo `factura_origen_id` ya en BD pero templates no lo muestran. Bloque separado del commit anterior
- **Pestaña notificaciones por org** — campana topbar + drawer feed. Inbox unificado: anomalías OCR + sugerencias IA + vencimientos + errores. Base ya construida (`module_events`). ~1-2 días. Spec: `docs/MODULOS-PRODUCTO.md`
- **Tests proformas + abonos rectificativos** — Vitest pendientes
- **Mobile responsive resto** — PR #5 cubre críticos. Pendiente: formularios <480px, search topbar polish, admin pages
- **Archivar sub-workflows voz antiguos en n8n** — Voice Process / Confirm / Correct (arquitectura v1) ya no se usan desde receptor v2. Activos pueden confundir
- **agency-portal PRs abiertos**: #54 quotes actions, #55 actor passthrough, #56 unificación facturas. Esperando review Borja. Tras merge #54: regen `types.gen.ts`, quitar 3 `as never`, migration `quotes.converted_facturaia_factura_id` + populate

## Smoke tests pendientes

- **Deploy 2026-05-07 (post)**:
  1. Anular factura emitida → ver abono ligado en banner rojo del modal + tab "Abonos" con count correcto
  2. Crear presupuesto/proforma desde `/generar` (serie P/F + Ver PDF sin 404)
  3. Probar 3er botón "Emitir como pendiente" (Verifactu sí, email no, estado=`pendiente`)
  4. Dashboard KPIs no inflados con borradores
  5. Menú 3 puntitos sin Editar/Eliminar en factura emitida, sin Anular en abono
- **Bloque 1 manual post-deploy** (`820684b`):
  1. Crear factura/presupuesto/proforma desde `/generar` y verificar serie A/P/F + `tipo_documento` correcto en BD
  2. Anular factura emitida con motivo R1-R5 → abono serie B con líneas en negativo + factura origen anulada + remisión AEAT si VeriFACTU
  3. "Ver PDF" en presupuestos sin 404
  4. Enviar presupuesto/proforma por email con PDF adjunto
- **VeriFACTU cron — verificar frecuencia** — confirmar en Dokploy que cron de `/api/verifactu/process` corre cada 1min (no cada hora). Si fuera 1h, incumple normativa AEAT (remisión no puede ser diferida). Solo config, sin código
- **PR #47 prod** — verificar entries en `audit_log` tras marcar cobrada / reenviar email / anular / DELETE vía API v1
- **agency-portal PR #56 post-merge** — badge fiscal en row, redirect 301 `/agency/facturaia/*`, botones según estado/origen, modal motivo R1-R5 obligatorio, doble-click sin duplicar (Idempotency-Key)

## WIP (sesiones en curso, branches sin mergear)

_(añadir aquí ramas activas con propósito y bloqueador si lo hay)_

## Progreso en vivo

Log cronológico de cada cosa que se trabaja. **Antes de empezar** algo nuevo, Claude busca aquí (+ NOW + Histórico) para detectar conflictos, solapes o trabajo previo. **Al avanzar/cerrar** algo, Claude añade entrada.

Formato: `YYYY-MM-DD HH:MM · estado · qué · ref (commit/PR/file)`. Estados: `[empezado]` / `[en progreso]` / `[bloqueado: razón]` / `[hecho]` / `[descartado: razón]`.

Reglas para el motor de conflictos:
- Idea nueva → grep en este log + NOW + LATER + Histórico ANTES de añadir. Si match → avisar "ya existe / ya se hizo / ya está en progreso por X" y proponer fusionar.
- Si dos cosas tocan el mismo archivo/feature → flagear solape y preguntar prioridad.
- Si lleva >7 días `[en progreso]` sin update → marcar `[stale]` en poda quincenal.
- Cuando una entrada llegue a `[hecho]` y sea hito relevante → mover a `## Histórico de hitos` con fecha + 1 línea.

<!-- nuevas entradas debajo, lo más reciente arriba -->

- 2026-05-11 · `[hecho]` · **Observabilidad de crons + panel admin** — tabla `cron_runs` (063), `withCronTracking` wrapper en 6 crons, panel `/admin/system/crons` con semáforo + tooltips + ejemplos reales por cron. Notif `cron_failed_<name>` a campanita de org de control si falla. Registry con descripción human-friendly. Commits `9892e4c` + `1b14779` + `d4b7566` + `d43f80d`
- 2026-05-11 · `[hecho]` · **Bug destapado y arreglado** — `storage-quota-check` fallaba semanal en silencio por env `STORAGE_QUOTA_WARN_MB=""` → `Number("")=0` ≤ 0 → throw. Fix con helper `parseMb` (fallback robusto null/empty/non-numeric). Destapado al primer run de `cron_runs`. Commit `5255547`
- 2026-05-11 · `[hecho]` · **Módulos IA mejorados — OCR + Conciliación via triggers BD** — migrations 060/061: `respect_ocr_auto_categorizar` (BEFORE INSERT/UPDATE facturas) + `auto_mark_pagada_on_bank_match` (AFTER INSERT/UPDATE facturas + AFTER INSERT movimientos_bancarios). Triggers cubren todos los callers (n8n, ingesta-view, API v1, voice). Catálogo: `auto_categorizar` + `auto_marcar_cobradas` `implemented: true`. Commit `33d5c7c`
- 2026-05-11 · `[hecho]` · **Cashflow IA opts + cron Opción B** — `buildCashflowData` acepta `{horizonteDias, incluirRecurrentes}`, cableado en cashflow-view/dashboard-view/impersonate. Nuevo cron `/api/internal/cashflow-alerts` (Dokploy `30 7 * * *`, chunks 10 + Promise.all, dedupe 24h, gate orgHasFeature). Commit `164dd9a`
- 2026-05-11 · `[hecho]` · **Copiloto — gate + idioma + persistencia historial** — gate `orgHasFeature('copiloto')` en `/api/ai-assistant` (cierra fuga billing preexistente), Topbar oculta botón sin feature, `AIAssistantHost` gatekeep evento `open-ai-assistant`. System prompt en `{idioma}`. Tabla `copiloto_conversaciones` (062, RLS por user_id) + thread_id desde cliente. Commit `19ee00f`
- 2026-05-11 · `[hecho]` · **ModuloConfig UI fixes** — toggles respetan `f.default` cuando config vacío (afectaba auto_categorizar, auto_marcar_cobradas, incluir_recurrentes, guardar_historial — se mostraban "Desactivado" la primera vez). Error handling con toasts en `save()`. Commit `3fefc3a`
- 2026-05-11 · `[hecho]` · **6 agentes paralelos auditaron cambios** (2 rondas × 3 expertise: security/backend/frontend) — 1 P0 + 3 P1 + 2 P2 reales aplicados, ~50% falsos positivos descartados con razón documentada
- 2026-05-10 · `[empezado]` · **Sistema comunicaciones email — Resend** — Spec consolidada tras review de 5 agentes paralelos (codebase, security, architecture, UX product, UI consistency). 5 PRs secuenciales reemplazan plan original 60d. Reutiliza `outbox_events` + `notifications` + `ai_module_suggestions` (NO duplica). Auth via Supabase + Custom SMTP Resend en dominio separado `auth.facturaia.agentesia.world`. Spec completa: [[facturaia-comunicaciones-emails]]. **Pendiente: Manuel hace setup Resend (2 dominios + Cloudflare DNS + Supabase SMTP + Dokploy env) antes de PR 1**
- 2026-05-10 · `[hecho]` · Hub maestro FacturaIA creado con NOW/Smoke/WIP/NEXT/LATER/Ideas/Decisiones/Stack/Manuales/Specs/Workflows/Histórico · commit `922ccea` vault
- 2026-05-10 · `[hecho]` · Sección Progreso en vivo añadida al hub para tracking de conflictos · commit pendiente vault
- 2026-05-10 · `[hecho]` · Hub poblado desde Slack canvas Panel FacturaIA — Bloque 1 generar-view, smoke tests Bloque 1, mobile responsive, sub-workflows voz a archivar, sección Seguridad (3 prio + 3 hardening), 9 features IA en NEXT, 8 features producto en LATER, suite E2E Playwright al histórico · commit pendiente vault
- 2026-05-10 · `[hecho]` · Manuales actualizados con UX real del módulo voz — manual-usuario sección "Convertir presupuesto" reescrita con 4 escenarios (1 match / candidatos numerados / fallback típos Whisper / ya facturado) + manual-admin sección 23.12 con root cause + fix técnico. Commit `4e98d76`
- 2026-05-10 · `[hecho]` · **Fix UX matching presupuestos** (E2E real reveló): resumen 0€ por iterar `data.lineas` que el agente no devuelve para `convertir_presupuesto` → branch en `Parsear y Calcular Totales` con lookup HTTP a Supabase. Y system prompt mejorado: matching permisivo (acentos/diminutivos/typos Whisper), lista candidatos numerados en >1 match, fallback "últimos 5 abiertos" en 0 matches, memoria conversacional para que el usuario responda "1"/"2". Commits `5cf48a3` + `6d41b9b`. Backups en ops/n8n-backups/
- 2026-05-10 · `[hecho]` · **F1+F2 voz + híbrido + workflow patched + verificación exhaustiva** — 12 commits: endpoints find/convert + UI variables/avanzado + métricas drill-down + admin /admin/voice + binding chat_id↔org_id + pg_cron purge + endpoint internal voice-system-prompt + endpoint voice-chat-bindings + workflow patched (consultar_presupuestos toolCode + branch convert post-confirm) + 5 bugs hardening (PGRST203, feature_gate, iva_pct min/max, invalid_json 400, ocr-audit FK 404). 101 tests E2E reales contra Supabase prod, 60/60 unit, lint/typecheck/build OK. **Pendiente push + deploy + activar generador_voz por org + phone en profiles antes de E2E con Meta**

---

## NEXT (próximas 2 semanas)

- ~~⭐ WhatsApp convertir presupuesto a factura por intención~~ ✅ **HECHO 2026-05-10** (commits + workflow patched, falta push/deploy + E2E real con Meta)
- ~~⭐ Admin módulo Voz/WhatsApp~~ ✅ **HECHO 2026-05-10** (`/admin/voice` con tabla overrides + métricas drill-down + sistema híbrido prompt variables/avanzado)
- **Sistema comunicaciones email (Resend)** — 5 PRs secuenciales: mailer core + auth via Supabase SMTP, outbox unificado + 8 plantillas, notifications multi-canal, módulo + UI cliente, admin UI + custom domain + 3 IA. Spec: [[facturaia-comunicaciones-emails]]. Bloqueado por setup Resend manual (cuenta + 2 dominios + DNS + Supabase SMTP + Dokploy env). ~3 semanas total
- **Stripe en activación add-ons** — hoy CTA "+XX€/mes" redirige a `/settings?tab=plan` sin cobro. Conectar checkout para que toggle = compra. Conciliación 19€ y Anti-fraude 9€ ya seedeados
- **Cobros backend** (módulo recomendador IA) — recordatorios escalados configurables (3/10/25 días, tono, hora). 6 opciones config con badge Próximamente esperan
- **Manuales actualizar Bloque 1** — `manual-usuario.md` y `manual-admin.md` describen flujo viejo: 2 botones generar (no 3), no mencionan anular ni tab Abonos ni nuevos pills/badges
- **Abono ligado a factura real** — nueva tool n8n `consultar_facturas_recientes` para que el agente confirme "¿te refieres a F2026-0042 a Tecnocloud por 121€?" antes de generar abono. Liga vía `factura_origen_id`. ~1 día
- **Post-confirm "añadir al catálogo"** — tras crear documento, si hubo productos marcados con ✨ (no estaban en catálogo), enviar mensaje extra con botones "Sí, añadir / No". Endpoint nuevo `/api/voice/learn-product`. ~1 día
- **Cobrador inteligente** — job nocturno detecta facturas vencidas y envía WhatsApp personalizado al cliente del emisor sin intervención. Reutiliza agente WhatsApp existente. Config por org: días de gracia, tono, canales. ~1-2 días. **Impacto alto** — mayor dolor de autónomos/PYMEs
- **Alertas anomalías facturas recibidas** — al ingestar factura de proveedor conocido, comparar importe contra histórico. Si desviación >X% → "Esta factura de Vodafone es 40% más alta que la media". Coste: query histórico en pipeline OCR. ~medio día
- **OCR conversacional bidireccional** — cuando OCR no encuentra campo crítico (NIF, total, fecha), agente pregunta por WhatsApp en vez de dejar fila incompleta. Reutiliza agente conversacional. ~1 día
- **Auto-categorización de gastos** — clasificar facturas recibidas leyendo histórico del proveedor: "facturas de Vodafone siempre van a Telefonía". Pedir confirmación solo cuando hay duda. ~1-2 días
- **Diagnóstico inteligente rechazos AEAT** — hoy errores AEAT llegan como código técnico. Mejorar para que IA explique en lenguaje llano qué falló y cómo corregir, en el modal de la factura. Reutiliza `ai-validate.ts`. ~horas
- **Predicción de cashflow** — con historial de facturas + patrones de cobro por cliente (quién paga 30d, quién 90d), proyectar cashflow del próximo mes con desglose confirmado vs en riesgo. Datos ya en BD. ~2-3 días
- **Versionado de defaults módulos** — cambiar default global no debe sorprender a orgs sin override (snapshot del valor previo o aviso visible)
- **Log de cambios de config por org** — audit trail granular para reconstruir "quién cambió qué config de qué org cuándo"

## LATER (backlog)

- **Backends módulos pendientes** — Fiscal (modelos AEAT 303/111/115/347), Firma eIDAS, Cashflow IA forecast. ~21 opciones config con badge Próximamente
- **Conexión bancaria automática** (Plaid/GoCardless/BBVA Open Banking) — desbloquea Conciliación al 100%. Spec: [[facturaia-open-banking-psd2]]
- **Asistente IA multi-canal** — copiloto WhatsApp para consultas (vencidas, resúmenes, cobrador, predicción cashflow, auto-categorización, alertas, presupuestos por contexto, informe fiscal). Spec: [[facturaia-bloque-4-agent-query-spec]]
- **Google OAuth email por org** — cada org envía desde su email vía Gmail API
- **Canales Ingesta + Plan/Facturación** (spec 2026-04-24) — rediseño canales sin toggles, página planes reales con método pago e historial
- **Conciliación bancaria IA** (spec 2026-04-21) — 5 tablas, pipeline Claude 2 fases, UI aprobación por lotes
- **Cleanup mockup AgentesiaLab** — plan SQL elaborado. Org `ea201784-...`
- **Multi-WhatsApp números por org** — Tecnocloud necesita su phone_number_id Meta. Spec: [[facturaia-arquitectura-multi-whatsapp-numbers]]
- **Exportación contable** — formato compatible con gestorías (A3, Sage, etc.)
- **App iOS sin Swift** — Expo Go / React Native, mínima para consultar facturas recibidas/emitidas/bandeja IA. Gestión compleja → desktop. Valorar dificultad vs nativa Swift
- **Control de stock**
- **Enlace contable** para programas de contabilidad
- **Entrada y salida de caja**
- **Liquidaciones de facturas recibidas**
- **Facturación recurrente con SEPA**
- **Dashboard financiero avanzado** con predicciones cashflow basadas en patrones históricos

---

## Ideas crudas / inbox

_(volcado sin filtrar — pasan a NEXT/LATER si maduran, o se descartan en poda quincenal)_

- _(añadir ideas aquí según surjan)_

## Decisiones pendientes (producto)

- **Cliente live vs congelado** — hoy snapshot fiscal al crear factura (datos cliente embebidos). Si editas cliente, PDFs viejos conservan datos antiguos (legalmente correcto, confunde UX). ¿Botón "Re-emitir con datos actuales" o congelado siempre? → cuando se decida, ADR en `decisions/`

## Bloqueos / esperando a terceros

- **[IMPORTANTE] Declaración Responsable AEAT como fabricante de SIF** — AgentesIA debe presentar este trámite administrativo para que FacturaIA opere legalmente en producción con VERI*FACTU. SIF = Sistema Informático de Facturación (RD 1007/2023). Sin esto el sistema no está homologado. Confirmar con Dani+Gonzalo si ya está o iniciar trámite
- **Dani + Gonzalo**: subir certificado P12 por org en Ajustes → VERIFACTU. Sin él no se envían facturas a AEAT y aparece error en dashboard
- **Borja**: review/merge agency-portal PR #54, #55, #56

## Seguridad

🟡 **Hardening diferido**:
- Logs estructurados en endpoints (correlation IDs)
- CSP headers más estrictos
- Métricas de uso de API IA (consumo OpenAI/Anthropic por org)

---

## Stack técnico

- **Frontend**: Next 16 (App Router), Tailwind, primitives Button/Card/Input/Modal en `components/ui/`
- **Backend**: Next API routes + Supabase (Postgres, RLS obligatoria por tabla)
- **OCR**: OpenAI Vision (`gpt-4o-mini`), fallback Anthropic Claude Vision
- **Voz**: n8n workflows + Retell (números WhatsApp por tenant)
- **Pagos**: Stripe (checkout pendiente cablear a add-ons)
- **Fiscal**: Verifactu (QR en PDFs, AEAT integrado)
- **Auth/RLS**: superadmin impersona vía `?org_id=` query param, no cookie
- **Tests**: Vitest (175+ unit/integration) + Playwright E2E (`tests/e2e/`: setup, smoke, explorer). Pre-release: `npm run e2e:explorer` y revisar `report.json`

## Reglas de proyecto (resumen)

Ver `facturaia/CLAUDE.md` (en repo) para versión completa.
- `lint` + `typecheck` + `build` limpios pre-commit
- Toda tabla nueva = `ENABLE ROW LEVEL SECURITY` + políticas en la misma migración
- Migration `ADD COLUMN NOT NULL` = `ADD nullable → UPDATE backfill → SET NOT NULL` en transacción
- Endpoint nuevo = auth + rate limit + validación input siempre
- Cambios Zod API público = `openapi.json` en mismo commit (clientes openapi-typescript no leen `refine`)
- UI con badge "implementado" = grep que el backend lee el valor (anti regresión silenciosa)

---

## Manuales y docs

| Doc | Link | Estado |
|---|---|---|
| Manual usuario | [GitHub](https://github.com/AgentesIA-MAdrid/facturaia/blob/main/docs/manuals/manual-usuario.md) | Bloque 1 desactualizado (3 botones, abonos, pills) |
| Manual admin | [GitHub](https://github.com/AgentesIA-MAdrid/facturaia/blob/main/docs/manuals/manual-admin.md) | Bloque 1 desactualizado |
| Módulos producto | [docs/MODULOS-PRODUCTO.md](https://github.com/AgentesIA-MAdrid/facturaia/blob/main/docs/MODULOS-PRODUCTO.md) | Vivo |
| CLAUDE.md proyecto | `facturaia/CLAUDE.md` | Vivo |

## Specs detalladas (subfiles)

- [[facturaia-comunicaciones-emails]] — sistema emails Resend + auth Supabase, 5 PRs, reutiliza outbox/notifications/ai_module_suggestions
- [[facturaia-integracion-api-v1-portal]] — webhooks HMAC, outbox, Stripe-style sync con agency-portal
- [[facturaia-test-tanda-2-3]] — tests de tanda 2 y 3
- [[facturaia-arquitectura-multi-whatsapp-numbers]] — multi-tenant WhatsApp por org
- [[facturaia-bloque-4-agent-query-spec]] — copiloto IA multi-canal
- [[facturaia-open-banking-psd2]] — conexión bancaria PSD2

## Workflows n8n (backups en `knowledge/projects/agentesia/n8n-backups/facturaia/`)

| Workflow | ID | Función |
|---|---|---|
| OCR Factura | `zf2la2N2YBXKQNKk` | Vision → estructurado |
| WhatsApp Receptor v2 | `zYcHHa8jWXB6dY5i` | Ingesta + intención |
| WhatsApp Verify | `LlBeZfa2P6mg13wc` | Verificación Meta |
| Voice Process | `KVk45rJARQk0EKaF` | Procesar audio |
| Voice Confirm | `5Q3pmag3XnIQOkQV` | Confirmación voz |
| Voice Correct | `Q1WB42g8GtyX3qnp` | Corrección voz |
| Email Polling | `dqvzeyeifTcNv50u` | Ingesta email |

---

## Links rápidos

- [GitHub repo](https://github.com/AgentesIA-MAdrid/facturaia)
- [App producción](https://facturaia.agentesia.world)
- [Dokploy](https://dokploy.agentesia.world)
- [Slack canvas Panel FacturaIA](https://agentesialab.slack.com/docs/T0ARXF0V31S/F0AV38CHYSJ) (`F0AV38CHYSJ`)
- [Canal Slack](https://agentesialab.slack.com/archives/pro-facturaia) (#pro-facturaia)
- WhatsApp público: `+34 919 93 26 18`

## Credenciales (refs en memoria, NO secrets aquí)

- Supabase FacturaIA → memoria `supabase-facturaia.md`
- Anthropic API key → memoria `anthropic-api-key.md`
- OpenAI API key → memoria `openai-api-key.md`
- WhatsApp config → memoria `whatsapp-facturaia.md`
- Gemini (backup) → memoria `gemini-api-key.md`

---

## Histórico de hitos

- **2026-05-11** Sesión grande módulos IA + observabilidad — (1) Módulos IA mejorados: OCR `auto_categorizar` + Conciliación `auto_marcar_cobradas` via triggers BD (migrations 060/061 cubren todos los callers n8n/manual/API v1/voice); Cashflow IA `{horizonteDias, incluirRecurrentes, umbral_alerta_caja}` con cron `/api/internal/cashflow-alerts` Opción B (chunks 10 + dedupe 24h + gate orgHasFeature); Copiloto `idioma` + `guardar_historial` con tabla `copiloto_conversaciones` (062) + gate `orgHasFeature('copiloto')` cerrando fuga billing preexistente + Topbar oculta botón + `AIAssistantHost` gatekeep evento global; ModuloConfig fix defaults `value !== undefined ? value : default` + error handling. (2) Observabilidad crons: tabla `cron_runs` (063), `withCronTracking` wrapper aplicado a 6 crons (webhook-dispatcher, check-vencimientos, cashflow-alerts, storage-quota-check, run-module-suggestions, verifactu-process — éste con auth custom `SUPABASE_SERVICE_ROLE_KEY`), panel `/admin/system/crons` con semáforo + tooltips con ejemplos reales + notif `cron_failed_<name>` a campanita. (3) Bug destapado: storage-quota-check fallaba semanal por env vacía → fix `parseMb`. (4) Auditoría: 6 agentes paralelos (2 rondas × 3 expertise) → 1 P0 + 3 P1 + 2 P2 aplicados, ~50% falsos positivos descartados con razón. Commits: `33d5c7c` + `164dd9a` + `19ee00f` + `3fefc3a` + `9892e4c` + `1b14779` + `5255547` + `d4b7566` + `d43f80d` + `6442182` (CLAUDE.md vault). 4 migrations aplicadas en prod. ADR-001 documenta decisión cron observability. **Patrones aprendidos** 6 learnings nuevos + 1 update + 9 reglas CLAUDE.md global + sección Vault Obsidian en CLAUDE.md proyecto
- **2026-05-10** Primera prueba E2E real WhatsApp del módulo voz — Borja envió audio "convierte el presupuesto a factura" → bot detectó intención correctamente y mostró botones, pero descubiertos 2 bugs UX en producción: (1) resumen con totales 0€ por iterar `data.lineas` que el agente no devuelve para `convertir_presupuesto` (fix con lookup HTTP a Supabase REST en `Parsear y Calcular Totales`); (2) matching estricto con dictado por voz fallaba ("manvel"≠"Manuel") y bot pedía "número exacto" en bucle (fix con system prompt: matching permisivo + 4 casos: 1 match / >1 candidatos numerados / 0 matches con últimos 5 abiertos / memoria conversacional para responder "1"/"2"). Commits `5cf48a3` + `6d41b9b` + `4e98d76` (manuales). Backups en ops/n8n-backups/. **Patrones aprendidos** documentados como 3 learnings nuevos: lista candidatos numerados + memoria conversacional vs error genérico (LLM ambiguity), parchear downstream o lookup recurso real al extender contrato JSON-out, verificar persistencia tras PUT con grep marker único (idempotency check defectuoso reportó OK sin aplicar). Pendiente: que Borja reintente la prueba con bot ya parcheado en producción
- **2026-05-10** Módulo Voz F1+F2 completo — convertir presupuesto por intención + admin completo. 12 commits a main: endpoints `/api/voice/find-presupuesto` + `convert-presupuesto` + `/api/internal/{voice-system-prompt,voice-chat-bindings}` + `/api/modules/generador_voz/{prompt,history,restore,preview,playground}` + `/admin/voice` (tabla overrides). 6 migraciones (053 voice_invocations, 054 voice_idempotency PK compuesta, 055 voice_chat_bindings, 056 voice_prompt_versions con RLS por org, 057 grants/purge, 058 pg_cron 03:00 UTC). Sistema híbrido del prompt: 12 variables tipadas + modo Avanzado override libre, template canónico HEADER/FOOTER inviolables. UI tab Configuración custom + tab Avanzado banner rojo + Playground con tokens/coste/historial + WAI-ARIA tabs completo. 5 bugs hardening detectados E2E: PGRST203 RPC overload (todas las conversiones rotas en prod), feature_gate ausente en find/convert, iva_pct sin .min(0).max(100), invalid_json devolvía 422 (debe 400), ocr-audit FK violation devolvía 500. Workflow `zYcHHa8jWXB6dY5i` patcheado vía API n8n: 64→67 nodos, +consultar_presupuestos toolCode + Es Conversion? IF + Convertir Presupuesto HTTP post-confirm. Backup en `ops/n8n-backups/`. **101 tests E2E reales contra Supabase prod (0 fail), 60/60 unit, lint/typecheck/build OK**. Pendiente push + deploy + activar generador_voz en orgs + phone en profiles antes de E2E real con Meta WhatsApp
- **2026-05-08** Suite E2E Playwright (`tests/e2e/`) — 3 proyectos: setup (login → storageState), smoke (4 paths críticos) y explorer (bot recorre app, rellena forms, clica tabs/filas/modales, captura console errors + HTTP 4xx/5xx + crashes). Output a `tests/e2e/report.json`. Comandos: `npm run e2e:smoke|e2e:explorer|e2e:report`. 2 bugs UI detectados y fixeados (commit `394a7ff`): (a) `/emitidas` y `/recibidas` 404 silenciosos por falta de guard `logo_url='not_found'` en `facturas-view.tsx:842,1082` (estaba en otros 4 sitios — bug por inconsistencia entre componentes); (b) `/ingesta` con 0 canales apuntaba a `/admin/connectors` (404), redirigida a `/settings?tab=integraciones`. CI verde tras fix `vitest.config.ts` (excluir `tests/e2e/**`). Re-run explorer post-deploy: 0 issues vs 8 antes. **Patrón aprendido**: cuando un guard `algo === 'sentinel_string'` se replica entre componentes, verificar TODOS los puntos de uso con grep
- **2026-05-08** PR #47 mergeado — audit log en marcar-cobrada/reenviar-email/anular/DELETE + idempotency en DELETE
- **2026-05-07** Sesión grande — 31 commits a main: 175 tests, withApiAuth en 19 endpoints, UI primitives, 14 modales role=dialog, FacturaMeta badges, tabs Facturas/Abonos, fix bug fiscal informes IVA, fix EstadoPill MAP, 3er botón "Emitir como pendiente", menú condicional por estado, CI integration job, RLS migration_037, .env.example expandido, migrations 047/048/049, deploy verde, 5 learnings + 5 reglas CLAUDE.md
- **2026-05-07** Voz WhatsApp en producción — 10 puntos verificados (e2e orgs, OCR receptor v2, presupuestos, textos WA, 403 toggles, modal series, duplicados BD, response limpio)
- **2026-05-07** Presupuestos/Proformas/Abonos completos — emisión funcional desde form manual + voz
- **2026-05-07** Secrets rotados — `fia_live_…` API key + `whsec_fia_…` webhook secret
- **2026-05-06** Sistema módulos premium completo — catálogo + add-ons + recomendador IA con 2 evaluators reales + activity feed + métricas + 137 tests Vitest
- **2026-05-06** Cron Dokploy recomendador IA configurado y validado (1 sugerencia generada para AgentesiaLab)
- **2026-05-02** Integración API v1 ↔ agency-portal — webhooks HMAC, outbox, Stripe-style sync, 7 PRs apilados
- **2026-04-28** Presupuestos/proformas/abonos voz + form manual; modal series builder; validación formato; invitaciones equipo; fix workflow voz abono; cleanup mockup AgentesiaLab
- **2026-04-27** VeriFACTU integración completa (QR en PDFs, AEAT)
- **2026-04-26** Billing banner + feature-locked rediseñados; datos fiscales completos clientes/proveedores; simplificación workflow voz WhatsApp
- **2026-04-25** Plantillas factura PDF pixel-perfect; system_config + admin config; security hardening; admin limits/storage fix; generador facturas voz desplegado; rediseño formulario nueva factura + email
- **2026-04-21** WhatsApp ingesta multi-tenant + Admin Panel + Feature Flags
