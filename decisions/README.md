---
title: Architecture Decision Records (ADRs)
date: 2026-05-10
tags: [decisions, adr, architecture]
---

# Decisiones

Una decisión = un archivo `ADR-NNN-slug.md`. Cuando elijas A sobre B y la elección no sea obvia leyendo el código (porque B también funcionaría), regístrala aquí. Sin esto, en 6 meses no recuerdas por qué.

## Cuándo crear ADR
- Elegir librería/herramienta entre alternativas reales (no "uso fetch porque sí").
- Schema de BD donde había 2+ formas válidas (single table vs split, FK vs JSON, etc.).
- Patrón arquitectónico (monolito vs micro, queue vs sync, etc.).
- Decisión que revertir luego costaría >1 día.

## Cuándo NO crear ADR
- Convenciones obvias del framework.
- Cambios revertibles en <1h.
- Bug fixes (van a `Stack/incidents.md`).

## Formato
Copiar `_template.md`, máx 15 líneas. Si necesita más, hay debate pendiente — resuélvelo antes.

## Index
<!-- añade aquí cada ADR como 1 línea: NNN · YYYY-MM-DD · título -->
- 001 · 2026-05-11 · [[ADR-001-cron-observability|Observabilidad de crons via tabla cron_runs + Dokploy externo]] (TuFacturaIA)
- 002 · 2026-05-18 · [[ADR-002-bot-state-machine-postgres|State machine conversacional del bot WhatsApp en Postgres chat_state]] (TuFacturaIA)
- 003 · 2026-05-18 · [[ADR-003-slot-resolver-determinista|Slot resolver determinista pre-LLM con regex en español]] (TuFacturaIA)
- 004 · 2026-05-18 · [[ADR-004-tool-calling-vs-json-schema-en-extraccion-onboarding|Tool calling con tool_choice forzado para extracción estructurada]] (agency-portal)
- 005 · 2026-05-18 · [[ADR-005-exencion-codigo-per-linea|Código exención IVA per-línea en lineas_factura.exencion_codigo]] (TuFacturaIA)
- 006 · 2026-05-20 · [[ADR-006-defense-in-depth-superadmin-impersonation|Override vs union semantics en impersonación de superadmin]] (TuFacturaIA)
- 007 · 2026-05-20 · [[ADR-007-sin-acceso-fallback-vs-loop-redirect|Página /sin-acceso para JWT vivo sin org operable]] (TuFacturaIA)
- 008 · 2026-05-20 · [[ADR-008-matriz-permisos-rol-aware-bd|Matriz canónica user_can_write_in_org BD + espejo TS]] (TuFacturaIA)
- 009 · 2026-05-21 · [[ADR-009-invitacion-consent-explicito-vs-activo-directo|Invitaciones consent explícito (toda invite = pending hasta aceptar)]] (TuFacturaIA)
- 010 · 2026-05-21 · [[ADR-010-helper-sql-atomico-vs-endpoint-encadenado|Helper SQL atómico para acciones con chain de triggers fiscales]] (TuFacturaIA)
- 011 · 2026-05-21 · [[ADR-011-bot-whatsapp-org-switch-v1-dos-turnos-vs-reprocesado|Bot WhatsApp org switch — v1 dos turnos vs reprocesado automático]] (TuFacturaIA)
- 012 · 2026-05-22 · [[ADR-012-ecobox-sin-crm-vs-chatwoot-vs-kommo|EcoBox sin CRM tradicional — Chatwoot compartido AgentesIA]] (EcoBox)
- 013 · 2026-05-22 · [[ADR-013-retell-conversation-flow-rigid-vs-flex-mode|EcoBox Retell Conversation Flow en Rigid Mode]] (EcoBox)
- 014 · 2026-05-22 · [[ADR-014-ecobox-log-universal-sheet-vs-chatwoot-voice-conversation|EcoBox log universal de leads en Google Sheet, no Chatwoot conversation]] (EcoBox)
- 015 · 2026-05-22 · [[ADR-015-centro-fiscal-mvp-vs-roadmap-completo|Centro Fiscal IA arranca como MVP 4 semanas, no roadmap 11 semanas]] (TuFacturaIA)
- 016 · 2026-05-22 · [[ADR-016-centro-fiscal-pricing-14-90|Centro Fiscal IA pricing 14,90€/mes (149€/año), no 9€ spec original]] (TuFacturaIA)
- 017 · 2026-05-22 · [[ADR-017-centro-fiscal-no-presenta-v1|Centro Fiscal IA v1 NO presenta telemáticamente, convenio AEAT diferido]] (TuFacturaIA)
- 018 · 2026-05-22 · [[ADR-018-centro-fiscal-stripe-scope-3-tiers-plus-addon|Centro Fiscal IA Stripe scope = 3 tiers TuFacturaIA + add-on, no solo add-on]] (TuFacturaIA)
- 019 · 2026-05-24 · [[ADR-019-precio-inclusive-iva-storage-canonico-vs-columna-precio-modo|Precio "con IVA incluido" en form: storage canónico base + toggle UX-only]] (TuFacturaIA)
- 020 · 2026-05-25 · [[ADR-020-source-of-truth-datos-emisor-template-config-vs-columnas|Datos emisor: template_config.emisor JSON único, columnas legacy deprecadas, sync explícito en código]] (TuFacturaIA)
- 021 · 2026-05-25 · [[ADR-021-html-email-strings-vs-react-email-mjml|HTML strings tipados para 6 templates email vs React Email/MJML]] (TuFacturaIA)
- 022 · 2026-05-27 · [[ADR-022-multidivisa-facturas-equivalente-eur-congelado|Facturas en divisa: equivalente EUR congelado + agregar siempre en EUR, VeriFACTU diferido]] (TuFacturaIA)
- 023 · 2026-05-28 · [[ADR-023-mapping-client-portal-cliente-remote-id-facturaia|Mapping client portal ↔ cliente_remote_id FacturaIA via union de fuentes, sin migration]] (agency-portal)
- 024 · 2026-05-29 · [[ADR-024-multidivisa-facturas-recibidas|Multidivisa facturas recibidas: FX en bandeja_ingesta congelado al aprobar]] (TuFacturaIA)
- 025 · 2026-05-29 · [[ADR-025-drive-sync-outbox-vs-fire-and-forget|Drive sync de PDFs facturas usa outbox + worker, no fire-and-forget post-response]] (TuFacturaIA)
- 026 · 2026-05-29 · [[ADR-026-saas-billing-stripe-hmac-fases-1-2|SaaS billing Stripe + HMAC fases 1-2]] (TuFacturaIA)
- 027 · 2026-05-31 · [[ADR-027-disponibilidad-slots-precomputados-vs-calculo-en-llm|Disponibilidad de citas: backend devuelve slots pre-computados, el LLM no calcula]] (Simarro)
- 028 · 2026-06-05 · [[ADR-028-multiempresa-scope-navegar-agregar-cobrar|Multiempresa: navegar=membresía, agregar=propiedad, cobrar=cuenta]] (TuFacturaIA)
