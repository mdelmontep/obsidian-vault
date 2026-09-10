---
title: cerrar un webhook exige censar TODOS sus emisores, no solo el obvio
date: 2026-09-10
source: ecobox
tags: [n8n, seguridad, retell, whatsapp, metodo]
---
Activar `authentication: headerAuth` en un webhook de n8n rompe a cualquier emisor que no mande la
cabecera. El riesgo no es técnico, es de **censo**: casi siempre hay más de un emisor.

Caso real (EcoBox): los 4 webhooks de citas los llaman **dos** clientes distintos — los custom
tools de Retell (voz) y los nodos `@n8n/n8n-nodes-langchain.toolHttpRequest` del workflow del bot
de Chatwoot (WhatsApp). Parchear solo Retell y activar la auth habría tumbado WhatsApp entero.

Orden seguro, y es de coste cero porque **n8n ignora las cabeceras que no espera** (comprobado en vivo):
1. Parchear **todos** los emisores para que manden ya la cabecera. Nada se cae: el receptor no la mira.
2. Esperar **tráfico REAL** por cada camino (una llamada de verdad, un WhatsApp de verdad) y
   comprobar la cabecera en el nodo `Webhook` de esas ejecuciones. Una casilla marcada a ojo no verifica nada.
3. Solo entonces, activar la auth en el receptor.

- n8n responde **403**, no 401, cuando falla la autenticación de cabecera.
- Emisor que **no puede** mandar cabeceras (Chatwoot): token en query (`?t=…`) + Code node + `Respond 401`.

Ver [[n8n-webhook-sin-auth-frontea-service-role-key]] · [[migracion-auth-sin-downtime-con-signing-legacy-until]]
