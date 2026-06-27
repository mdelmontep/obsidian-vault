---
title: port/adapter devuelve dato discriminado; el caller traduce a throw en su borde
date: 2026-06-27
source: claude-code-session
tags: [arquitectura, ports-adapters, testabilidad, facturaia]
---

Al meter una capa port/adapter entre el código de negocio y el data layer (para subir
testabilidad de categoría 4 "mock módulo" a 3 "inyección"), el port **nunca lanza** por
una precondición de negocio: devuelve **resultado discriminado** (`{kind:'found'|'none'|
'ambiguous'}`, `{kind:'ok'|'conflict'}`). El caller traduce ese dato al canal de control
que espera su framework, EN SU BORDE.

Caso FacturaIA #538 (puerto `CopilotoStore`): el runner del copiloto usa `throw Error(mensaje
español)` como señal (lo captura `evaluateConfirmationGate` → respuesta sin botones). El port
devuelve datos; la tool decide qué dato es un error de precondición y lo lanza. Resultado:
el runner NO cambia (cero churn en el framework) y el adapter in-memory testea el camino
completo sin re-mockear el query-builder de PostgREST (que ni modelaba el guard atómico real).

Inyección con blast radius mínimo: campo OPCIONAL en el contexto (`ctx.store?`) + helper
`getStore(ctx)` con default lazy al adapter de prod → las piezas no migradas y sus tests no
se tocan. Gate de regresión: grep que prohíbe `createAdminClient`/`.from(...)` en los ficheros
migrados. Ver [[integracion-en-jsonb-tabla-generica-pierde-observabilidad]] · [[defensa-en-codigo-vs-prompt-llm-para-invariantes-de-dominio]].
