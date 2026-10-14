---
title: kommo salesbot/run devuelve success:true aunque el bot no tenga acciones configuradas
date: 2026-04-30
source: claude-code-session
tags: [kommo, salesbot, n8n]
---

`POST /api/v2/salesbot/run` siempre devuelve `{"success":true}` si el bot existe,
independientemente de si tiene acciones configuradas o no.

Para que el salesbot envíe el mensaje WhatsApp, el bot necesita en su editor (Ajustes → Robots de ventas):
- Acción: "Enviar mensaje WhatsApp"
- Contenido: `{{lead.cf.FIELD_ID}}` donde FIELD_ID es el campo donde n8n escribe el mensaje

Sin esa acción: la llamada API "funciona" pero el usuario no recibe nada.
El PATCH previo que escribe en el campo custom sí ejecuta correctamente — el problema es siempre el bot sin acción.

Matiz (jun 2026): aunque el bot tenga la acción, **no entrega si el contacto no tiene un canal de WhatsApp vinculado** (solo número en el campo Phone). La plantilla de marketing no basta para iniciar — el salesbot envía a través de una conversación/canal existente. Lead creado a mano con teléfono pero sin chat WA → `success:true` pero Meta marca 0 enviados. El contacto debe haber escrito antes o tener el canal vinculado.

Matiz (oct 2026, Simarro): con el **canal de WhatsApp desconectado** (Meta quitó la app de Kommo de la WABA) los salesbots siguen dando `success:true` y n8n en verde: 7 días sin un saliente y nadie lo vio. Vigilar la **entrega**, no la ejecución: eventos `outgoing_chat_message` de `/api/v4/events` (corchetes del filtro url-encodeados, sin encodear devuelve vacío) o `GET /{waba}/phone_numbers?fields=status` por Graph. Ver [[whatsapp-conectar-numero-propio-en-movil-a-cloud-api]].
