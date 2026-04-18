---
title: n8n debounce redis con wait 1s causa duplicados en chatbot
date: 2026-04-18
source: claude-code-session
tags: [n8n, redis, chatbot, debounce]
---

En el patrón de debounce Redis (push → Wait → get all → delete → process), un Wait de 1 segundo es insuficiente: llegan mensajes rápidos del usuario que disparan múltiples ejecuciones antes de que la primera termine el ciclo get+delete.

Con Wait de 10 segundos se agrupa correctamente. El chatbot acumula todos los mensajes del usuario en esos 10s y responde una sola vez.

Síntoma visible: el bot envía múltiples respuestas al mismo mensaje, a veces repitiendo preguntas ya contestadas.
