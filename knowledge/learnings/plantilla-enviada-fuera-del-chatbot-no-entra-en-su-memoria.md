---
title: una plantilla enviada fuera del chatbot no entra en su memoria y el bot se re-presenta
date: 2026-09-29
source: simarro (chatbot QLfRT9AWmV1HLMZs + voz XWY6oRNyiBV74c4z)
tags: [n8n, kommo, whatsapp, chatbot, memoria]
---
- Síntoma: el cliente contesta «Ok» a una plantilla de WhatsApp y el bot saluda como primer contacto («soy Ana…») y repite lo que ya decía la plantilla.
- Causa: la plantilla la envía un salesbot de Kommo (o un humano, o una API), no el agente. La memoria Postgres del agente (`memoryPostgresChat`) solo guarda lo que pasa por él, así que su historial arranca vacío.
- Una pista en el contexto («le enviamos la plantilla…») no basta si el prompt dice «explica X»: el modelo lo vuelve a explicar.
- Fix de origen: en el workflow que dispara la plantilla, INSERT en la tabla de memoria (`session_id` = la clave de sesión del bot) de un mensaje `ai` con formato LangChain: `{type:'ai',content,tool_calls:[],additional_kwargs:{},response_metadata:{},invalid_tool_calls:[]}`. Solo si el envío salió bien.
- Red para los envíos manuales: el contexto incluye el TEXTO de la plantilla + «no te presentes ni lo repitas; un "ok" aquí no es despedida».
- Trampa: la tabla de memoria vive en la BD de n8n (`n8n.public.<tabla>`), no en Supabase.
- Aplica a cualquier cliente con chatbot n8n + envíos por salesbot/plantilla (Clínica Zen, Laserys).
