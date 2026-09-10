---
title: el inventario de automatismos no está solo en el orquestador
date: 2026-09-10
source: simarro
tags: [kommo, n8n, integraciones, auditoria]
---
Antes de soltar una integración que CREA entidades en un CRM, audité los 31 workflows n8n activos
para responder «¿qué le puede llegar al cliente?». Conclusión: solo uno, y controlado. Un rato
después una clienta recibía un WhatsApp automático 1 segundo después de crearle el lead.

No salió de n8n. Salió de un **salesbot atado a una etapa del pipeline dentro de Kommo**: crear el
lead en esa etapa ES el disparador. Ningún workflow lo invoca, así que grepear el orquestador no lo
encuentra nunca.

Regla: el orquestador es UNA de las fuentes de automatismos, no el inventario. Al escribir en un
sistema de terceros hay que enumerar también **sus** automatizaciones internas (salesbots/automations
por etapa, reglas, triggers de BD) antes del primer write real.

Detección sin acceso a la config: `GET /api/v4/events` tras crear una entidad de prueba —
`outgoing_chat_message` / `talk_created` en el mismo segundo delatan al bot. La lista de bots no sale
por API (`/api/v2/salesbot` da 403/404), pero sí desde el navegador con sesión: ver [[kommo]].

Ver [[dar-de-alta-con-fecha-pasada-despierta-los-automatismos-de-esa-fecha]] · [[recordatorios-visita-por-task-type]]
