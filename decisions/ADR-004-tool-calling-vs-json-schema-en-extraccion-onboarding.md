---
title: ADR-004 — tool calling con tool_choice forzado para extracción estructurada en el bot de onboarding
date: 2026-05-18
status: accepted
tags: [adr, agency-portal, llm, openai]
---

## Contexto

El bot de onboarding por WhatsApp en agency-portal necesita responder al
usuario Y extraer ~70 campos en 11 secciones. La implementación previa
(regex sobre `<system_data>` hidden block) fallaba silenciosamente ~5% de
los turnos con system prompt largo + multi-idioma → progreso UI nunca avanzaba.

## Opciones consideradas

- **A. `response_format: { type: 'json_schema', strict: true }`** — todo el output es JSON con campo `response`. Simple. Pero el modelo "rellena formulario" en lugar de "conversar y etiquetar" → empobrece tono.
- **B. Function calling con tool `emit_turn` forzado vía `tool_choice`** — campo `reply_text` separado del payload estructurado. Modelo trata cada turno como "envío respuesta + metadatos". Preserva tono.
- **C. Dos llamadas (responder + extraer)** — duplica latencia y coste, pierde contexto entre llamadas.
- **D. Mantener regex con refuerzos en prompt** — parche al problema actual, no escala.

## Decisión

**B**, porque preserva tono conversacional (validado en 4 agentes paralelos: 2-1 a favor de B), `tool_choice` forzado es contractualmente más fuerte que el prompt, y `parsed_arguments` del SDK auto-valida con Zod.

## Consecuencias

- Pin de modelo a snapshot con Structured Outputs strict en tool calls (`gpt-4o-2024-11-20`).
- Schema Zod compartido como fuente única (parser + tool definition).
- Fail-loud en parser, degradación graciosa en handler con `logAuditEvent('extraction_failed')`.
- Cerrada la opción de "extract con un segundo call" — si latencia se vuelve crítica, alternativa es bajar a `gpt-4o-mini-2024-07-18` antes que partir en dos llamadas.

## Referencias

PR #67, [[llm-tool-calling-elimina-silent-fail-extraccion-estructurada]], [[llm-source-quote-anti-alucinacion-extraccion]].
