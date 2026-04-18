---
title: integración ticketing chatbot mejorado pendiente de test con cliente real
date: 2026-04-17
source: claude-code-session
tags: [inbox, pendiente, agentesia, ticketing, chatbot]
---

El tool "Crear Ticket" está desplegado en el ChatBOT mejorado (`89B9QN23hOHDq6oP`) y funciona: la tool se ejecuta, el HTTP llega al portal (`https://clientes.agentesia.madrid/api/webhooks/whatsapp-ticket`), los parámetros se parsean correctamente.

## Pendiente

1. **Testear con número de cliente real** — el test con el número de Manuel devolvió 404 porque no tiene `primary_contact_phone` en la BD del portal. Pedir que le pongan el teléfono al cliente de test "Soporte técnico" y repetir la prueba
2. **Verificar flujo completo** — que el AI Agent interprete correctamente `TICKET_CREATED ticketId=X` / `TICKET_APPENDED` / `ERROR_NO_CLIENTE` y responda al usuario según el `<flujo_soporte>` del prompt
3. **Verificar que flujos existentes no se rompieron** — captación, agendamiento, handoff manual
4. **Limpiar workflow temporal** — borrar `a96XVFKX4WujMCKW` ("TEMP - Limpiar memoria chat")

## Contexto técnico

- El toolCode usa `query` (variable global) en vez de `$fromAI()` por bug en n8n 2.15.x
- HTTP via `this.helpers.httpRequest` sin `returnFullResponse`, status codes en catch
- Normalización de teléfono: 9 dígitos → prepend `34` (España)
