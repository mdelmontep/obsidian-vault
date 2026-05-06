---
title: metricas en ui necesitan tabla de dominio mas event-log como complemento
date: 2026-05-06
source: claude-code-session
tags: [arquitectura, ux, gotcha]
---

Si una métrica visible al cliente cuenta SOLO de un event-log creado junto con la feature, los datos pre-feature serán 0 indefinidamente. El cliente abre la pestaña Métricas el día del lanzamiento y ve "0 facturas extraídas" cuando lleva años usando OCR.

Diseñar siempre con TABLA DE DOMINIO existente como fuente primaria + events como complemento de detalle.

Caso real facturaia: endpoint `/api/modules/[id]/metrics` inicialmente solo contaba `module_events` (creada con migration 045). AgentesiaLab tenía 49 facturas en `bandeja_ingesta`, 0 en module_events → métrica decía "0 procesadas (30d)". Fix: contar `bandeja_ingesta` directo + `module_events` solo para flujos nuevos.

Patrón:
```ts
// Por modulo, mapear a su tabla de dominio
if (id === 'ocr') count = await admin.from('bandeja_ingesta').count(...)
if (id === 'cobros') count = await admin.from('facturas').eq('estado','vencida').count(...)
```

Solo usar events para métricas que NO tienen agregado natural en una tabla.
