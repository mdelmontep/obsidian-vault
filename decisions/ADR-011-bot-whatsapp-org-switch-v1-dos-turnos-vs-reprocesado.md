---
title: ADR-011 · Bot WhatsApp org switch — v1 dos turnos vs reprocesado automático
date: 2026-05-21
status: aceptado
tags: [adr, facturaia, bot, whatsapp, ux]
---

# Contexto

Bot WhatsApp multi-org. Cuando el user dice "factura para Sandbox 75€" estando con sticky=AgentesiaLab, hay dos diseños posibles tras cambiar la sticky a Sandbox.

# Opciones

**v1 (elegida)** — Dos turnos. Bot cambia sticky + responde "Cambiado a Sandbox. Repite tu mensaje cuando quieras." El user repite. Cero persistencia adicional.

**v2** — Reprocesado automático. Bot persiste el mensaje original en `chat_state.pending_message`, cambia sticky, reinyecta el mensaje al agente con la nueva org sticky activa. User no repite. Requiere columna nueva + TTL + logic de re-entrada al workflow + cleanup tras éxito o expiración.

# Decisión

v1 dos turnos. Razones:

- Simplicidad: sin tabla nueva ni TTL, sin re-entrada al workflow, menos surface de bugs.
- Robusto bajo cambios concurrentes (no hay riesgo de reprocesar contra una sticky stale).
- Manu validó la fricción en smoke E2E: 2 turnos extras son aceptables vs el coste de mantener un buffer.

v2 queda para PR-Bot-3 si la fricción se nota en uso real prolongado. Ver [[facturaia-bot-conversational-redesign]] §future.
