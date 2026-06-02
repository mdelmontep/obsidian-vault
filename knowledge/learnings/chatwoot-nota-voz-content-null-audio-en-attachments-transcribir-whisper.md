---
title: chatwoot nota de voz llega con content null y audio en attachments, transcribir con whisper
date: 2026-06-01
source: claude-code-session
tags: [chatwoot, n8n, whatsapp, whisper]
---

Una nota de voz en Chatwoot dispara `message_created` con `content:null` y el audio en `attachments[0]` (`file_type:audio`, `.ogg`/`audio/opus`, `data_url` = blob redirect). Un bot que filtra por `content notEmpty` ignora todos los audios silenciosamente.

Fix:
1. `IF mensaje cliente`: aceptar `content` **o** attachment audio (`attachments?.[0]?.file_type === 'audio'`).
2. Rama: `Download audio` (HTTP GET `data_url`, response=file → binario `data`) → transcribir.
3. Transcribir: HTTP POST `api.openai.com/v1/audio/transcriptions`, `predefinedCredentialType: openAiApi`, `multipart-form-data` con `model=whisper-1` + `formBinaryData file ← data`. Devuelve `{text}`.
4. `message = content || $json.text`.

Caso EcoBox 2026-06-01. Ver [[n8n-edit-fields-optional-chaining-body-args-plano-vs-wrapped]].
