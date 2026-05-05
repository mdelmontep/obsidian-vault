---
title: facturaia bloque 4 capa semántica agent query spec
date: 2026-04-28
source: claude-code-session
tags: [facturaia, ai, whatsapp, design, spec]
---

# Bloque 4 — `/api/agent/query/*` capa semántica

Endpoint nuevo para consultas naturales por WhatsApp que el AI Agent del workflow voz puede invocar.

## Casos de uso

- "envíame la última factura de Pepe" → busca cliente por nombre, factura más reciente, manda PDF
- "qué tengo pendiente de cobrar este mes" → resumen agregado
- "manda el presupuesto P2026-0012 a juan@empresa.com" → envío email
- "marca pagada la factura A2026-0034" → mutación

## Decisiones pendientes

- **Tool-calling Claude API vs intent classifier ad-hoc** — la API de Claude soporta tools nativamente, evita re-implementar router de intents; pero añade latencia de un round-trip extra al modelo
- **Operaciones expuestas como tools** — split por riesgo: `consultar_*` (libres), `enviar_*` (confirmación opcional), `marcar_*` (confirmación), `cancelar_*` / `eliminar_*` (confirmación obligatoria + allowlist)
- **Prevenir mutaciones masivas accidentales** — allowlist explícita de mutaciones + confirmación obligatoria por botones WhatsApp ("¿Confirmas marcar pagada A2026-0034?"). Prohibir tools tipo "borrar todas las facturas"
- **Conexión con AI Agent existente** — workflow voz `zYcHHa8jWXB6dY5i` ya tiene un AI Agent. Opciones: (a) extender ese agent con las nuevas tools, (b) flujo separado para consultas (workflow nuevo) que se decide por intent al llegar el mensaje

## Pre-requisitos

NO empezar antes de cerrar Bloques 1+2 de FacturaIA (form manual + vistas separadas). Es sesión grande con Opus + plan mode aparte.

Relacionado: [[agency-portal-n8n]]
