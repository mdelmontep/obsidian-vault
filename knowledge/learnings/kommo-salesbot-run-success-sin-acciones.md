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
