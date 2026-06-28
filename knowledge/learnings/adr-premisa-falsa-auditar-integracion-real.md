---
title: un adr puede partir de una premisa falsa — auditar la integración real antes de implementar
date: 2026-06-28
source: claude-code-session
tags: [arquitectura, adr, n8n, proceso]
---

El ADR G5 (TuFacturaIA) asumía "n8n solo recibe y envía; el cerebro ya está en la app". La auditoría del workflow receptor real (183 nodos) reveló un **segundo agente GPT-4o** con ~16 tools que pegan directo a Supabase REST con SERVICE_ROLE_KEY. La topología aprobada ("Next.js único receptor = extraer receptor + reenviar media") era en realidad portar un orquestador entero.

Patrón: **antes de implementar sobre la premisa de un ADR, auditar la integración real** (workflow, endpoints que llama, tráfico) — sobre todo si nadie la ha mirado en meses. Una decisión "aprobada" puede descansar sobre una foto obsoleta del sistema.

Señal de alarma: el ADR describe un sistema externo en una frase ("n8n solo transporta") sin evidencia citada. Coste de un Read del workflow < coste de construir la topología equivocada y romper prod en el cutover.

Relacionado: [[n8n-reimplementa-endpoint-backend-pierde-sus-defensas]].
