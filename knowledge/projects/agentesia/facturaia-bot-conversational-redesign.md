---
title: FacturaIA — Bot WhatsApp rediseño conversacional
date: 2026-05-21
source: sesión Phase 1 multi-org branch + feedback Manu
tags: [facturaia, bot, whatsapp, ux, n8n, copiloto, agente-facturador, conversational]
---

# Bot WhatsApp — rediseño conversacional

Origen: Phase 1 multi-org desplegada 2026-05-21 (commit n8n PUT). Smoke E2E verde pero feedback Manu: el bot entra directo en "modo factura" ante cualquier mensaje (incluido "Hola") devolviendo 🧾 con campos vacíos. UX robótica, no humana.

## Objetivo

Bot conversacional tipo colega contable: saluda corto, pregunta una cosa a la vez, asume contexto cuando lo hay, no se presenta cada mensaje. Detección de intención antes de generar nada.

## Comportamiento target

### Primera vez (sin historial)
```
[User] Hola
[Bot]  ¡Hola Manu! 👋 ¿En qué te ayudo?
       Puedo generar facturas, abonos, presupuestos,
       consultar pendientes o convertir documentos.
```

### Día a día (con historial)
```
[User] Hola
[Bot]  ¡Hey! ¿Qué necesitas?

[User] buenos días
[Bot]  Buenas Manu, dime.
```

### Intención clara pero incompleta
```
[User] factura
[Bot]  ¿Para qué empresa?           ← solo si multi-org sin sticky
       [📋] AgentesiaLab · FacturaIA Sandbox

[User] (elige AgentesiaLab)
[Bot]  Ok. Cliente, concepto y precio.

[User] Pérez SL, consultoría 75€
[Bot]  🧾 Pérez SL · Consultoría · 75€ + IVA = 90,75€
       ¿Emito? [Sí] [Cambiar] [No]
```

### Intención completa de golpe
```
[User] Factura para Pérez SL, consultoría 75€
[Bot]  🧾 Pérez SL · Consultoría · 75€ + IVA = 90,75€
       (asume sticky org silenciosamente)
       ¿Emito? [Sí] [Cambiar] [No]
```

## Reglas del system prompt

- Saludo conversacional corto SIN presentarse (asume contexto). Si `IS_FIRST_TIME=true` → presentación breve. Si false → respuesta natural.
- Sin emojis innecesarios. Cero "🎉 ¡Estoy aquí para ayudarte!" robotizado.
- Frases cortas (1-2 líneas). Pregunta UNA cosa a la vez, no listar 4 campos de golpe.
- Sticky org existente → asumir, NO preguntar. Solo preguntar org si: (a) multi-org sin sticky, (b) usuario nombra otra org explícito, (c) menciona empresa que no coincide con sticky.
- Tono colega contable: "vale", "dime", "ok", "perfecto". Evitar "¡Excelente!", "¡Por supuesto!", "Estoy listo para ayudarte".
- Nunca generar 🧾 con campos vacíos o "Sin nombre". Si falta data crítica → preguntar.
- Detección intención: small-talk / petición creación / consulta / conversión / cancelar / confirmar. Routing claro en prompt.

## Cambios técnicos requeridos

### 1. Detección de "primera vez"
- Query `SELECT COUNT(*) FROM n8n_chat_histories WHERE session_id=$hash` ya existe en `Check Sesion Voz Activa`.
- Pasar `cnt` como variable downstream hasta `Preparar Input Agente`.
- Inyectar al prompt: `IS_FIRST_TIME: ${cnt === 0}`.

### 2. Inyectar contexto humano
En `Preparar Input Agente` añadir al system prompt:
- `KNOWN_USER_NAME: ${profile.full_name || 'desconocido'}`
- `STICKY_ORG_NAME: ${org_nombre || null}`
- `IS_FIRST_TIME: ${boolean}`
- `LAST_INTERACTION_AT: ${chat_state.updated_at || null}` (para "ayer", "hace rato", etc)

### 3. Phase 2 Interactive Lists (multi-org + selección)
Heredada del plan original ([[n8n-receptor-multiorg-resolve-context]] §Phase 2):
- Parsear `interactive.list_reply.id` en `Parsear Mensaje`.
- Router temprano: si `list_reply.id` empieza por `org_select:` → POST `/api/internal/whatsapp/select-org` → reprocesar mensaje original (no pedir al user que reescriba).
- Tabla / columna nueva `chat_state.pending_org_selection jsonb` con TTL 5min para guardar mensaje original tras list.
- Sustituir `Responder Multi-Org Texto` por WhatsApp List Message interactivo.

### 4. System prompt rediseñado
Reescribir el system prompt del `Agente Facturador` desde cero con:
- Sección INSTRUCCIONES con las reglas humanas arriba.
- Sección CONTEXTO con las variables inyectadas.
- Sección INTENCIONES con detección clara (small_talk, generate_doc, query, convert, confirm, cancel).
- Sección REGLAS DE PREGUNTA (una cosa a la vez, no listar todo).
- Few-shots de cada caso (saludo first-time, saludo recurrente, intención incompleta, intención completa, ambigüedad org).

### 5. Smoke E2E

Casos:
1. **First-touch**: limpiar n8n_chat_histories para session_hash → "Hola" → respuesta con presentación breve.
2. **Saludo recurrente**: tras varias interacciones → "Hola" → respuesta corta sin presentarse.
3. **Multi-org first**: 2 orgs, sin sticky, "factura" → list interactiva → seleccionar → "Cliente, concepto y precio".
4. **Multi-org sticky**: 2 orgs con sticky → "factura para Pérez 75€" → asume sticky, genera resumen, pide confirmación.
5. **Cambio explícito de org**: con sticky AgentesiaLab → "factura para Pérez 75€ desde Sandbox" → detecta override → confirmar org + datos.
6. **Petición incompleta**: "quiero una factura" → pregunta cliente/concepto/precio (una cosa).
7. **Small-talk no factura**: "¿qué tal?" → respuesta conversacional, NO genera 🧾.
8. **Confirmación**: tras propuesta → "sí" → genera + PDF + URL.
9. **Cambio en propuesta**: tras propuesta → "cambia IVA al 10" → recalcula + nueva propuesta.
10. **Cancelar**: tras propuesta → "no, deja" → confirma cancelación.

## Estimación

~1-2 días: prompt engineering + 1 nodo detección first-time + Phase 2 Interactive Lists + smoke 10 casos.

Riesgo: medio. Toca el flow crítico del bot. Mitigación: trabajar sobre el backup `whatsapp-receptor-v2-20260521-002111-pre-multiorg.json` + Workflow History n8n + smoke staged antes de activar.

## Dependencias

- Phase 1 multi-org ya desplegada (commit n8n 2026-05-21).
- Endpoint `/api/internal/whatsapp/select-org` ya existe (mig 125).
- Tabla nueva `chat_state.pending_org_selection` requiere migración Supabase.
- LLM configurado en `/admin/llm` operativo (hoy bloqueado por OpenAI 429 + Anthropic key inválida — debe resolverse antes de smoke).

## Phase split

- **PR-Bot-1 — Detección first-time + system prompt humano**: cambios prompt + 1 variable nueva + smoke casos 1, 2, 6, 7. Sin Interactive Lists todavía. ~4-6h.
- **PR-Bot-2 — Interactive Lists multi-org + sticky-aware**: Phase 2 completa + smoke 3, 4, 5. ~4-6h.
- **PR-Bot-3 — State machine confirmación/cambio/cancelar**: smoke 8, 9, 10 + edge cases. ~3-4h.

Total ~12-16h en 3 PRs incrementales. Cada uno con smoke staged.

## Decisiones pendientes

- Personalidad del bot: "colega contable" vs "asistente profesional formal" vs "informal con humor"? — Manu confirmó **colega contable** (tono natural, breve, sin formalidad).
- Soportar múltiples idiomas? — diferir, solo ES por ahora.
- Voice notes con saludo conversacional? — sí, mismo tratamiento.
- Persistir `pending_org_selection` en `chat_state` (nueva columna) o tabla aparte? — preferir nueva columna jsonb (atómico con la sesión).

## Relacionado

- [[n8n-receptor-multiorg-resolve-context]] — runbook Phase 1 + plan Phase 2.
- [[facturaia-conciliacion-roadmap]] — PR-A3.1 copiloto WhatsApp del módulo conciliación reusará Interactive Lists.
- [[whatsapp-interactive-lists-phase2]] — memoria persistente del trigger.
