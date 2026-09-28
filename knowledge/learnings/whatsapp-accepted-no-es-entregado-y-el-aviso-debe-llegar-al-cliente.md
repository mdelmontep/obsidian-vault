---
title: whatsapp accepted no es entregado, y el aviso del fallo debe llegar al cliente
date: 2026-09-28
source: centro-elphis
tags: [whatsapp, meta, observabilidad, n8n, avisos]
---

`POST /messages` de la Cloud API responde `message_status: accepted` y el flujo lo da por enviado. La entrega real llega **después, por el webhook de statuses** (`failed`, ~8-10 s en Elphis). Quien no procese `statuses[].status === 'failed'` cree que el paciente tiene el enlace.

- **131026 «Message undeliverable» es del destinatario** (sin WhatsApp, app vieja, condiciones sin aceptar, bloqueo), no de la plantilla: la misma plantilla se entregó y leyó a otro número el mismo día. **Reintentar no sirve** (medido: el reenvío falló igual a los 8 s).
- Enlazar fallo → mensaje: guardar el `wamid` que devuelve el POST (Elphis: `bot_outbound_log.meta_message_id`) y buscarlo al llegar el status. Dedup por `wamid`: Meta repite statuses.
- **El aviso a nuestro Slack no basta**: el fallo lo tiene que ver quien puede llamar al paciente (email a recepción + nota en el deal del CRM). Excluir destinos internos para no avisar al mismo número que falló. Ver [[persistir-el-error-no-basta-si-ninguna-superficie-lo-lee]].
- Además, cualquier resumen generado antes del status («se le ha enviado el enlace») queda falso: el aviso tiene que desmentirlo.

Caso: Elphis, `wa-inbound-bridge`, 28-sep-2026 → [[clientes/centro-elphis/index|centro-elphis]].
