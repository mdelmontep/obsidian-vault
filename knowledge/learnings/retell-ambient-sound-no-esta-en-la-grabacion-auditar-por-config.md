---
title: retell ambient_sound no aparece en la grabación — auditar la config, no el wav
date: 2026-07-28
source: claude-code-session
tags: [retell, audio, qa-voz, clinica-zen]
---
`recording_multichannel.wav` trae los canales por separado ANTES del mix de salida: con
`ambient_sound` activo, el canal del agente sale limpio (silencio digital, −99 dBFS entre
frases). Quien escucha la grabación no oye el ruido que sí oyó el cliente por teléfono, y
encima sobre codec de banda estrecha ese ruido enmascara consonantes.

Caso real (Clínica Zen): queja de "no se escucha nítido" que en la grabación no existía —
agente a −19,8 dBFS, 0 muestras saturadas, y el que sonaba 5 dB más bajo era el llamante.
La config tenía `ambient_sound: call-center` + `voice_speed 1.12` + `volume 0.84`.

Ante una queja de nitidez: medir el wav (clipping/nivel/SNR) para DESCARTAR el TTS, y
después revisar `ambient_sound`, `voice_speed`, `volume` y la latencia e2e (p50 >2 s ya se
percibe como "cuesta entenderse"), que es donde suele estar. Ver [[clinica-zen]]
