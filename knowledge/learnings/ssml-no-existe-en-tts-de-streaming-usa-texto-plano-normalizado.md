---
title: no uses SSML en un agente de voz de streaming — normaliza el texto tú, en código
date: 2026-08-06
source: claude-code-session
tags: [retell, tts, voz, elevenlabs, cartesia]
---
Para que un TTS lea un teléfono dígito a dígito, el instinto es SSML
(`<say-as interpret-as="telephone">`, `<break>`). **En este stack no existe:**

- **Retell** no documenta SSML en ninguna parte (0 hits de `ssml`/`say-as`/`<break` en su
  volcado completo de docs), y el frame del Custom-LLM WebSocket solo transporta `content`
  en texto plano. Su mecanismo documentado es dígitos en palabras separados por ` - `.
- **Cartesia** solo tiene 5 tags «SSML-like» (sin `say-as`) y **desaconseja su propio
  `<spell>` para teléfonos**: manda pasar el número plano.
- **ElevenLabs**: `<break>` no va en v3; hay issue abierto en su repo oficial donde con
  `stream=True` **el `<break>` se LEE EN VOZ ALTA**. Deepgram lo descartó por escrito;
  OpenAI lo sustituyó por `instructions`.
- W3C: el troceado de `interpret-as="telephone"` es «processor specific» → no reproducible.

El modo de fallo del marcado no es «se ignora»: es que **el agente dice la etiqueta delante
del cliente**. Fix: rendir los dígitos como PALABRAS en código propio, con **comas** como
pausa (funciona en cualquier motor, sobrevive a un cambio de voz). Agrupación: no hay norma
(E.123 §2.9 aconseja sin prescribir; el RD 2296/2004 solo fija 9 dígitos) → decisión de
producto, escríbela. Nunca en parejas: 2/12 y 3/13 se confunden de oído.
Ver [[un-control-negativo-que-no-discrimina-invalida-el-test-entero]].
