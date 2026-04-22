---
title: redis debounce con campo nombre diferente pierde mensajes silenciosamente
date: 2026-04-22
source: claude-code-session
tags: [n8n, redis, debounce, whisper, audio]
---

En un patrón debounce con Redis (SET → Wait → GET → IF), si el campo que se guarda en SET no coincide con el que viene del input, Redis almacena vacío y el IF descarta el mensaje.

Caso real: el nodo Merge pasaba `Mensaje` (texto WhatsApp) o `text` (transcripción Whisper/OpenAI). El Redis SET solo buscaba `Merge.json.Mensaje`, así que los audios se guardaban como vacío → el IF post-debounce los descartaba.

Fix: `$('Merge').first().json.Mensaje || $('Merge').first().json.text || ''`

Regla: cuando un nodo Merge recibe inputs de ramas distintas (texto, audio, imagen), verificar que **todos los campos de salida** están contemplados en los nodos downstream.
