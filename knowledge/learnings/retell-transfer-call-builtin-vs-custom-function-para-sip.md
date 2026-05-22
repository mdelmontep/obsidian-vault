---
title: Retell transfer_call built-in vs custom function — solo el built-in transfiere SIP
date: 2026-05-22
source: claude-code-session
tags: [retell, voice, transfer, safety]
---

Un custom function tool que devuelve `{transfer_to:"+34X"}` **NO transfiere la llamada**; Retell solo le pasa los datos como respuesta al LLM, que puede decir "te transfiero" pero la línea sigue activa con el agente.

La única forma de transferencia SIP determinista en Retell es el tool built-in:
```
type: "transfer_call"
transfer_destination: { type: "predefined", number: "+34717003717" }
transfer_option: { type: "cold_transfer" }  // o "warm_transfer"
```

Crítico en contextos safety-critical (crisis suicida, emergencia médica): el bot puede creer que está transfiriendo cuando solo está hablando. Verificar siempre con una llamada real antes de declarar listo.

Caso real Elphis 2026-05-22: agente Laura con `transferir_crisis` custom function dejaba al usuario sin transfer. Fix: built-in `transfer_to_emergency` al +34717003717 (Teléfono de la Esperanza), cold transfer.
