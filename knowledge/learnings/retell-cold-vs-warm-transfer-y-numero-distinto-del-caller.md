---
title: transfer Retell — cold vs warm, y el número destino no puede ser el del que llama
date: 2026-06-02
source: claude-code-session
tags: [retell, voz, transfer]
---

Dos causas de "no transfiere":
1. **warm_transfer** (`transfer_option.type`): Alex llama al destino, espera descuelgue + detección de humano (`agent_detection_timeout_ms`, p.ej. 30s) y recién une. Si no descuelgan o falla la detección → va a la rama "Transfer failed". Frágil para un taller. Usar **cold_transfer** (`{type:"cold_transfer", show_transferee_as_caller:true}`) = reenvío directo, sin que la IA hable antes.
2. **El número destino = el número del que llama** → la IA marca tu propia línea ocupada → siempre falla. El nº de transfer humano debe ser distinto del caller; al probar, llamar desde OTRO móvil.

El nodo sigue siendo `transfer_call` built-in (lo único que transfiere SIP real). Caso EcoBox 2026-06-02. Ver [[retell-transfer-call-builtin-vs-custom-function-para-sip]].
