---
title: retell tool schema — required debe listar exactamente las claves de properties
date: 2026-08-12
source: claude-code-session
tags: [retell, tools, json-schema]
---
En una tool de conversation flow, `parameters.required` puede listar claves que NO existen en
`parameters.properties` (ej. `required:["After","Before"]` con `properties:{_after,_before}`) sin
que Retell rechace el schema al guardarlo. El LLM rellena lo que VE en `properties` — nunca lo que
dice `required` — así que el backend nunca recibe `After`/`Before`, sin ningún error visible en
ningún lado.

Confirmado empíricamente en Simarro: con el payload exacto que el LLM enviaría (`_after`/`_before`),
el webhook n8n respondía "No me ha llegado la fecha a consultar" — cada consulta de disponibilidad
por voz fallaba en silencio desde que existía la tool.

Fix: verificar que TODAS las claves de `required` aparezcan literalmente en `properties` (mismo
nombre, mismas mayúsculas) antes de publicar. Grep del propio JSON del tool sirve: cada string de
`required` debe aparecer como clave de `properties`.
