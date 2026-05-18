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
- 001 · 2026-05-11 · [[ADR-001-cron-observability|Observabilidad de crons via tabla cron_runs + Dokploy externo]] (FacturaIA)
- 002 · 2026-05-18 · [[ADR-002-bot-state-machine-postgres|State machine conversacional del bot WhatsApp en Postgres chat_state]] (FacturaIA)
- 003 · 2026-05-18 · [[ADR-003-slot-resolver-determinista|Slot resolver determinista pre-LLM con regex en español]] (FacturaIA)
- 004 · 2026-05-18 · [[ADR-004-tool-calling-vs-json-schema-en-extraccion-onboarding|Tool calling con tool_choice forzado para extracción estructurada]] (agency-portal)
- 005 · 2026-05-18 · [[ADR-005-exencion-codigo-per-linea|Código exención IVA per-línea en lineas_factura.exencion_codigo]] (FacturaIA)
