---
title: kommo salesbot puede mover leads de estado sin que n8n lo sepa
date: 2026-04-22
source: claude-code-session
tags: [kommo, salesbot, n8n, debug]
---

Los salesbots de Kommo tienen lógica interna configurada en la GUI (no visible vía API). Además de enviar mensajes, pueden tener acciones como "Cambiar estado del lead".

Cuando un workflow n8n dispara `POST /api/v2/salesbot/run`, el bot ejecuta TODA su cadena interna — incluyendo cambios de estado. Esto puede mover un lead sin que ningún nodo de n8n lo haga explícitamente.

Síntoma: un lead cambia de status entre dos ejecuciones del chatbot, sin que ningún sub-workflow (Reservar_cita, etc.) se haya ejecutado. El webhook `status_lead` se dispara "solo".

Debug: si un lead cambia de estado misteriosamente, revisar la configuración del salesbot en Kommo GUI → buscar acciones "Cambiar etapa" o "Mover a pipeline".

Caso real: bot_id 68822 en Clínica Zen movía leads de 104111891 a 104115975 al enviar cada mensaje.
