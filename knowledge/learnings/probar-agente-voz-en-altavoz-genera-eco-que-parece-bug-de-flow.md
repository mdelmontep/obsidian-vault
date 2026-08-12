---
title: probar un agente de voz en modo altavoz genera eco que parece bug del conversation flow
date: 2026-08-12
source: claude-code-session
tags: [retell, voz, testing, diagnostico]
---
Llamada de prueba real a un agente Retell: el transcript mostraba el turno "user" como continuación
literal, palabra por palabra, de lo que el propio agente acababa de decir o iba a decir a
continuación (ej. `agent: "Hola,"` / `user: "La soy Ana, asistente"` / `agent: "soy Ana,
asistente..."`). Parecía eco de la línea SIP y llevaba a sospechar del trunk telefónico (Netelip).

Causa real: la llamada de prueba se hizo con el móvil en **altavoz** — el propio micrófono del
llamante capta el audio que sale por su propio altavoz y se retransmite como si fuera su voz. No es
un defecto de la línea ni del Conversation Flow.

Antes de escalar a infraestructura de telefonía por un patrón de eco en el transcript, preguntar
primero cómo se hizo la llamada de prueba (altavoz vs. auricular/oído) — descarta la causa más
barata antes de tocar el trunk SIP.
