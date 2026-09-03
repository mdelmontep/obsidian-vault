---
title: ADR-079 — una reserva de Doctoralia mueve todos los deals abiertos del lead; una cancelación vuelve a «Volver a contactar»
date: 2026-09-03
status: accepted
tags: [adr, elphis, clientify, doctoralia, n8n]
---

## Contexto
Recepción recibía el aviso del lead (voz o WhatsApp) sin saber si esa persona había reservado después en Doctoralia. Un lead suele tener varios deals abiertos (voz, chat, enlace de cita) y `doctoralia-email-sync` creaba siempre uno nuevo «Cita Doctoralia», así que en la ficha convivían 2-3 deals en «Entrada Lead Nuevo» que parecían pendientes.

## Opciones consideradas
- **A — crear siempre un deal nuevo por reserva** (lo que había): trazable, pero los deals del bot siguen en «Entrada» y recepción llama a quien ya tiene cita.
- **B — mover solo el deal más reciente**: barato, pero el resto sigue pareciendo pendiente y depende del orden de creación.
- **C — mover todos los deals abiertos del lead** (tags `lead_bot|visita_programada|doctoralia` o nombre; excluye Won/Lost; tope 10) a «1º Visita Programada» con nota «Cita Doctoralia: fecha · servicio» y vencimiento = día de la cita; crear «Cita Doctoralia» solo si no había ninguno.
- Cancelación: **Lost** (desaparece del embudo y se pierde la llamada de rescate) o **«Volver a contactar» (260088)** con vencimiento hoy+7.

## Decisión
**C**, y cancelación a «Volver a contactar»: la ficha responde de un vistazo «¿tiene cita?» y una cancelación es un lead a recuperar, no uno perdido. Reprogramación actualiza la nota, no crea deal.

## Consecuencias
`clientify-move-deal` acepta `remarks_append` y `expected_closed_date` (fusiona sobre el detalle actual); todo PATCH lleva pipeline+etapa+estado+vencimiento ([[clientify-post-deals-ignora-pipeline-y-un-patch-parcial-reevalua-etapa-y-vencimiento]]). Quien reserva sin haber pasado por el bot sigue sin fila en `conversation_state` ([[ADR-053-la-cita-de-doctoralia-vive-en-conversation-state]]).
