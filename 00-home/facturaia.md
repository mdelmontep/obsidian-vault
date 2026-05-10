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

- **Pestaña notificaciones por org** — campana topbar + drawer feed. Inbox unificado: anomalías OCR + sugerencias IA + vencimientos + errores. Base ya construida (`module_events`). ~1-2 días. Spec: `docs/MODULOS-PRODUCTO.md`
- **Tests proformas + abonos rectificativos** — Vitest pendientes
- **agency-portal PRs abiertos**: #54 quotes actions, #55 actor passthrough, #56 unificación facturas. Esperando review Borja. Tras merge #54: regen `types.gen.ts`, quitar 3 `as never`, migration `quotes.converted_facturaia_factura_id` + populate

## Smoke tests pendientes

- **Deploy 2026-05-07 (post)**:
  1. Anular factura emitida → ver abono ligado en banner rojo del modal + tab "Abonos" con count correcto
  2. Crear presupuesto/proforma desde `/generar` (serie P/F + Ver PDF sin 404)
  3. Probar 3er botón "Emitir como pendiente" (Verifactu sí, email no, estado=`pendiente`)
  4. Dashboard KPIs no inflados con borradores
  5. Menú 3 puntitos sin Editar/Eliminar en factura emitida, sin Anular en abono
- **PR #47 prod** — verificar entries en `audit_log` tras marcar cobrada / reenviar email / anular / DELETE vía API v1
- **agency-portal PR #56 post-merge** — badge fiscal en row, redirect 301 `/agency/facturaia/*`, botones según estado/origen, modal motivo R1-R5 obligatorio, doble-click sin duplicar (Idempotency-Key)

## WIP (sesiones en curso, branches sin mergear)

_(añadir aquí ramas activas con propósito y bloqueador si lo hay)_

---

## NEXT (próximas 2 semanas)

- ⭐ **WhatsApp convertir presupuesto a factura por intención** — usuario dice "hazme la factura del último presupuesto para Manuel" → bot encuentra coincidencia, muestra `P2026-0042 · Manuel García · 1.200€ ¿confirmas?`. Endpoints `/api/voice/find-presupuesto` (matching difuso) + `/api/voice/convert-presupuesto`. Workflow `zYcHHa8jWXB6dY5i`. Casos edge: múltiples, ambiguos, sin presupuestos. ~1-2 sprints
- ⭐ **Admin módulo Voz/WhatsApp** — `/admin/voice` o tab en `/agentes`: invocaciones día/semana, tasa éxito, latencia, errores recientes, conversaciones sin factura, top NIFs. Inspección/edición prompts AI Agent por org (usa `module_metadata`). Playground sin tocar BD. Config tono/idioma/IBAN embebido. ~2-3 sprints
- **Stripe en activación add-ons** — hoy CTA "+XX€/mes" redirige a `/settings?tab=plan` sin cobro. Conectar checkout para que toggle = compra. Conciliación 19€ y Anti-fraude 9€ ya seedeados
- **Cobros backend** (módulo recomendador IA) — recordatorios escalados configurables (3/10/25 días, tono, hora). 6 opciones config con badge Próximamente esperan
- **Manuales actualizar Bloque 1** — `manual-usuario.md` y `manual-admin.md` describen flujo viejo: 2 botones generar (no 3), no mencionan anular ni tab Abonos ni nuevos pills/badges

## LATER (backlog)

- **Backends módulos pendientes** — Fiscal (modelos AEAT 303/111/115/347), Firma eIDAS, Cashflow IA forecast. ~21 opciones config con badge Próximamente
- **Conexión bancaria automática** (Plaid/GoCardless/BBVA Open Banking) — desbloquea Conciliación al 100%. Spec: [[facturaia-open-banking-psd2]]
- **Asistente IA multi-canal** — copiloto WhatsApp para consultas (vencidas, resúmenes, cobrador, predicción cashflow, auto-categorización, alertas, presupuestos por contexto, informe fiscal). Spec: [[facturaia-bloque-4-agent-query-spec]]
- **Google OAuth email por org** — cada org envía desde su email vía Gmail API
- **Canales Ingesta + Plan/Facturación** (spec 2026-04-24) — rediseño canales sin toggles, página planes reales con método pago e historial
- **Conciliación bancaria IA** (spec 2026-04-21) — 5 tablas, pipeline Claude 2 fases, UI aprobación por lotes
- **Cleanup mockup AgentesiaLab** — plan SQL elaborado. Org `ea201784-...`
- **Multi-WhatsApp números por org** — Tecnocloud necesita su phone_number_id Meta. Spec: [[facturaia-arquitectura-multi-whatsapp-numbers]]

---

## Ideas crudas / inbox

_(volcado sin filtrar — pasan a NEXT/LATER si maduran, o se descartan en poda quincenal)_

- _(añadir ideas aquí según surjan)_

## Decisiones pendientes (producto)

- **Cliente live vs congelado** — hoy snapshot fiscal al crear factura (datos cliente embebidos). Si editas cliente, PDFs viejos conservan datos antiguos (legalmente correcto, confunde UX). ¿Botón "Re-emitir con datos actuales" o congelado siempre? → cuando se decida, ADR en `decisions/`

## Bloqueos / esperando a terceros

- **Dani + Gonzalo**: subir certificado P12 + Declaración Responsable AEAT (SIF)
- **Borja**: review/merge agency-portal PR #54, #55, #56

---

## Stack técnico

- **Frontend**: Next 16 (App Router), Tailwind, primitives Button/Card/Input/Modal en `components/ui/`
- **Backend**: Next API routes + Supabase (Postgres, RLS obligatoria por tabla)
- **OCR**: OpenAI Vision (`gpt-4o-mini`), fallback Anthropic Claude Vision
- **Voz**: n8n workflows + Retell (números WhatsApp por tenant)
- **Pagos**: Stripe (checkout pendiente cablear a add-ons)
- **Fiscal**: Verifactu (QR en PDFs, AEAT integrado)
- **Auth/RLS**: superadmin impersona vía `?org_id=` query param, no cookie

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
