---
title: salida de runner-llm cara al cliente — bloques delimitados + borrador con aprobación humana
date: 2026-06-17
source: claude-code-session
tags: [llm, agentes, automatizacion-cliente, facturaia]
---

Cuando un runner LLM headless (Claude Code, n8n+IA) genera texto que verá un cliente final:

1. **No publiques el stdout entero.** Exige en el prompt dos bloques delimitados y parséalos por los marcadores: uno técnico interno (`[DIAGNÓSTICO]`) y otro cliente-facing (`[RESUMEN]`, tono llano). Si faltan marcadores → todo al interno, el cliente-facing vacío (nunca publicar texto sin verificar formato).
2. **Borrador con gate humano.** El resumen entra como borrador, NO se publica solo: un humano lo revisa/edita y pulsa "publicar". Evita que un fallo del LLM llegue directo al cliente.
3. **Runner sin credenciales de Storage** → sube blobs (capturas) vía endpoint interno (base64 + HMAC), no le des creds.

Caso: TuFacturaIA "Resolver con Claude" (PR #371). Relacionado: [[defensa-en-codigo-vs-prompt-llm-para-invariantes-de-dominio]] · [[runner-headless-git-push-dispara-pre-push-hook]].
