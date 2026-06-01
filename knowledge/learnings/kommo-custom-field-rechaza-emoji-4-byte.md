---
title: kommo rechaza emojis de 4 bytes en el valor de un custom field vía api
date: 2026-06-02
source: claude-code-session
tags: [kommo, whatsapp, encoding]
---
PATCH a un CF (textarea/text) con un emoji de 4 bytes (🏡, 🏠…) → Kommo descarta TODO
el valor en silencio (devuelve 200) y el campo queda vacío. Causa: columna utf8 (3-byte),
no utf8mb4. Si ese CF alimenta el {{N}} de una plantilla WhatsApp, Meta acaba enviando el
texto de EJEMPLO del placeholder (parece que "funciona" pero con datos falsos).
Fix: nada de emojis 4-byte en valores que van por API. €, ·, acentos y \n SÍ se guardan.
El emoji en texto FIJO de la plantilla sí va; el problema es solo el valor inyectado por API.
Ver [[whatsapp-template-variable-no-admite-saltos-de-linea]].
