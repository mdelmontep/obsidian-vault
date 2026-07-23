---
title: Supabase Storage rechaza con 400 una key con nombre en Unicode NFD (macOS/Chrome)
date: 2026-07-23
source: claude-code-session
tags: [supabase, storage, unicode, i18n]
---

macOS/Chrome mandan `file.name` en Unicode **NFD** (forma descompuesta): "í" llega como "i" + `U+0301` (acento combinante suelto), no como el codepoint precompuesto `U+00ED`. Si ese nombre se usa tal cual como key de un objeto en Supabase Storage, el servidor responde **400** — y como muchos handlers traducen cualquier error de `storage.upload()` a un `500` genérico hacia el cliente, el síntoma visible es "Error del servidor" para **cualquier** archivo con tilde/ñ/diéresis subido desde Mac. Determinista, no intermitente.

Fix: antes de construir la key, `name.normalize('NFC')` (recompone lo común) + sustituir cualquier no-ASCII restante (combinantes sueltas, emoji) por `_`. El nombre original sin sanear se guarda aparte para mostrar en la UI — el saneo es solo de la key interna del bucket.

Aplica a cualquier endpoint que construya una key de Storage a partir de un nombre de archivo de usuario (upload directo, adjuntos de email, cualquier ingesta de terceros) — auditar TODOS los puntos de entrada, no solo el más visible: en FacturaIA había un segundo punto (adjuntos de email) que ni siquiera saneaba separadores de ruta.

Relacionado: mismo patrón raíz (asumir ASCII en código que maneja español) que [[regex-word-boundary-no-casa-acentos-js-normalizar-nfd]].
