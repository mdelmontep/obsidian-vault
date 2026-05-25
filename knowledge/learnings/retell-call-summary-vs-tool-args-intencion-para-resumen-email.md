---
title: retell call_summary (transcript completo) supera a args.intencion para emails post-llamada
date: 2026-05-25
source: claude-code-session
tags: [retell, voice, post-call, openai]
---

Dos fuentes de "resumen" en el payload `call_analyzed` de Retell:

- `call.call_analysis.call_summary` — Retell lo genera **del transcript completo** con su modelo de análisis. Cobertura amplia.
- `args.intencion` del `tool_call` de cierre — lo que el LLM del agente sintetiza **en línea** mientras habla con el cliente. Suele truncarse a 2-3 frases porque el prompt empuja a la concisión.

Si usas `args.intencion` como resumen del email, vas a perder datos que el cliente sí dio (mensajes de error literales, motivo de la transferencia, app implicada, etc.).

Patrones recomendados:
1. **Trivial**: usar `call_summary` directamente.
2. **Mejor**: en n8n, regenerar el resumen con `gpt-4.1-mini` desde el `transcript` completo con prompt estructurado: (a) motivo+app, (b) datos literales citados, (c) persona+motivo si aplica, (d) pasos probados+resultado, (e) estado final. `max_tokens >= 700`, `response_format: json_object`. Da control total sobre formato y secciones.

Caso real Tecnocloud (Laura): se cambió la prompt del Code node "Registrar Llamada" del workflow `aAfDL01MLPAOWfco` con esos 5 puntos, máx 8 frases. Email pasó de 2 frases huérfanas a resumen completo.
