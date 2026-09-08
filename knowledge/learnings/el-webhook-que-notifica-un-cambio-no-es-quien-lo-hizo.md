---
title: el webhook que notifica un cambio no es quien lo hizo — el autor está un segundo antes
date: 2026-09-09
source: clinica-zen
tags: [kommo, n8n, webhooks, diagnostico, integraciones]
---
En una integración bidireccional (Kommo, Chatwoot, HubSpot) cada cambio dispara
un webhook DE VUELTA hacia el automatizador. Al buscar quién movió algo, la
ejecución que cuadra **al segundo** con la hora del cambio suele ser ese webhook
entrante: se entera, no lo hizo. Atribuírselo es la conclusión fácil y falsa.

El autor real está **0,5–1 s ANTES**, y es quien ESCRIBE. Cómo separarlos:
- ordenar los nodos por `startTime` del `runData`, no por hora de la ejecución;
- el webhook trae el cambio en su PAYLOAD DE ENTRADA (`...[status_id]`,
  `[old_status_id]`): eso es notificación;
- el autor lo lleva en el CUERPO QUE ENVÍA (`jsonBody`) y su salida es la
  respuesta de la API.

Y no basta con grepear `status_id` en la ejecución: el nodo lo manda en sus
PARÁMETROS, no en sus datos de salida, así que un detector que mire solo la
salida da **cero falsos negativos silenciosos**. Corolario: cuando el registro
del CRM ya no existe (Kommo: `GET` 204, `PATCH` 400), sus eventos son
irrecuperables y esta es la única vía. Ver [[kommo-webhook-status-lead-dispara-en-todos-los-cambios]]
