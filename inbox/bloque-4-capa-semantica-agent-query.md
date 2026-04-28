---
title: facturaia bloque 4 capa semantica agent query
date: 2026-04-28
source: claude-code-session
tags: [facturaia, ai, whatsapp, design]
---

Endpoint nuevo `/api/agent/query/*` para consultas naturales por WhatsApp:

- "envíame la última factura de Pepe" → busca, manda PDF
- "qué tengo pendiente de cobrar este mes" → resumen
- "manda el presupuesto P2026-0012 a juan@empresa.com" → envío email
- "marca pagada la factura A2026-0034" → mutación

Decisiones de diseño pendientes:
- Tool-calling Claude API vs intent classifier ad-hoc
- Qué operaciones se exponen como tools (consultar / enviar / marcar / cancelar)
- Cómo prevenir que diga "borra todas las facturas" → allowlist de mutaciones + confirmación obligatoria por botones WhatsApp
- Cómo conectar con AI Agent del workflow `zYcHHa8jWXB6dY5i` o crear flujo separado

Sesión grande con Opus + plan mode aparte. NO empezar antes de cerrar Bloques 1+2 (form manual + vistas separadas).
