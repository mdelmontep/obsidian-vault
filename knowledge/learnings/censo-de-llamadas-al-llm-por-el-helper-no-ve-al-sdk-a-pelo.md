---
title: un censo de llamadas al LLM hecho por el helper no ve a quien llama al SDK a pelo
date: 2026-08-25
source: facturaia
tags: [llm, auditoria, censo, grep, opus5]
---

El 25-ago audité «las 19 llamadas al modelo» de FacturaIA y di el área por CERRADA
en el hub. El censo salió de grepear el wrapper propio (`callLlm`,
`callLlmWithRetry`) — y tres rutas no lo usan: instancian `new Anthropic()`
directamente. Dos de las tres tenían defecto real: el explicador fiscal guardaba
en `fiscal_explicaciones` un texto que no había comprobado que estuviera
completo (y el caché por hash lo servía para siempre), y el playground de voz de
`/admin` probaba prompts **sin `temperature`** — la API va a 1 — cuando el runner
que contesta los WhatsApp va a 0.2.

El censo se hace por **el import del SDK**, que es lo que no se puede evitar:
`grep -rl "@anthropic-ai/sdk\|from 'openai'" src/`. El wrapper es una convención,
y una convención mide a los que la siguen.

Corolario para cualquier auditoría por superficie: buscar la **dependencia
externa**, no el envoltorio interno. Ver [[una-suite-en-verde-no-prueba-el-camino-real]].

**Caso 2 (3-sep-2026, tickets 169/170)**: ADR-064 decía «tres resolutores de proveedor». El cuarto (`aprobarItem` de `/ingesta`) hacía su propio `.select('id, nif')` + `.find()` y no salía grepeando el helper (`elegirProveedorExistente`, `resolve_proveedor`); lo sacó el gate de cierre grepeando **la tabla**: `from('proveedores')`. Misma regla: se censa por el recurso (tabla, SDK), no por el envoltorio.
