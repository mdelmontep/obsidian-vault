---
title: ADR-003 — Slot resolver determinista pre-LLM con regex en español
date: 2026-05-18
status: accepted
tags: [adr, facturaia, bot, llm, n8n]
---

## Contexto
Bot WhatsApp con listas ("cuál convierto?") necesitaba que "el 1", "el último", "el de 289 €", "P2026-0018" se resolvieran al UUID correcto. Tras 5 patches solo con state machine + LLM, el LLM seguía adivinando UUIDs y fallando ~30% de los turnos.

## Opciones consideradas
- **A — LLM-only** (status quo). El system prompt enseña al LLM a usar `last_listado.items[N-1].id`. Falla no-determinista; alucinaciones de UUIDs.
- **B — Intent Router con LLM-mini** (Haiku/gpt-4o-mini) que clasifica intent y resuelve slot antes del LLM principal. ~150-300ms extra + coste OpenAI doble. Profesional pero ROI bajo para volumen actual.
- **C — Code n8n con regex determinista** (8 patrones español: NUM, superlativo, fecha, importe, cliente, número, ordinal, pronombre) con precedencia explícita. 0ms latencia. Sin coste extra. Mantenible por humanos con sólo leer la regex.

## Decisión
**C**, porque ROI alto en lo nuestro (volumen bajo-medio, español dominante, patrones de selección por listado son ~10 formas comunes). El LLM nunca toca UUIDs — sólo decide qué tool llamar; el backend ya tiene el slot. Elimina clase entera de bugs por alucinación.

## Consecuencias
Capa 2 del patrón Stripe (state machine + slot resolver) implementada. Capas 3-4 (Response composer, Intent Router LLM-mini) quedan como Fase 2 LATER si volumen crece o aparecen patrones de NLU no cubiertos por regex. Cualquier idioma nuevo requiere ampliar regex (no inviable en español; portugués/inglés pendientes si hay clientes).

Ver [[facturaia]] · [[ADR-002-bot-state-machine-postgres]] · [[slot-resolver-deterministic-pre-llm-nlu-regex-espanol]]
