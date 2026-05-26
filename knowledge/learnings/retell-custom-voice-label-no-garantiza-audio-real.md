---
title: Retell custom voice — la etiqueta no garantiza el audio real
date: 2026-05-25
source: claude-code-session
tags: [retell, voice, elevenlabs]
---

Las custom voices heredadas en una cuenta Retell tienen un `voice_name` arbitrario asignado al crearlas, pero el `voice_id` subyacente de ElevenLabs puede apuntar a otra voz distinta.

Síntoma: voz llamada "Borja - Clever and Credible" reproduce audio femenino. El UI muestra "Borja", `voice_name` API también, pero el audio TTS es de otra voz.

Causa: alguien creó la custom apuntando a un ElevenLabs voice_id equivocado y le puso ese nombre. El error se propaga porque Retell no expone el voice_id de ElevenLabs subyacente, solo su propio `custom_voice_xxx`.

Verificación obligatoria antes de fijar voz:
```
curl https://retell-utils-public.s3.us-west-2.amazonaws.com/<custom_voice_id>.mp3
```
Escuchar el preview MP3 ANTES de asignar al agente. Si el preview no coincide con el nombre, no usar.

Caso real: EcoBox 2026-05-25 — descartado `custom_voice_9cdd6de86c85185d6f988b147a` (etiquetado Borja, sonaba mujer), elegido `custom_voice_ba7fd23dc476d2ac821f8edd10` (Pablo Fernández, voz masculina real).
