---
title: cloudflared quick tunnel muere si la red bloquea el puerto 7844
date: 2026-07-04
source: claude-code-session
tags: [webhook, dev, cloudflared, meta, tunnel]
---
Para exponer un localhost al webhook de Meta (bucle dev), `cloudflared tunnel --url` imprime una
URL pero **NO conecta si la red bloquea el puerto 7844** (QUIC/UDP y TCP) — típico en WiFi de
oficina. Señal: pre-check `hard_fail=true`, `ERR Failed to dial a quic connection`, "Allow
outbound QUIC/TCP on port 7844".

Fixes: **hotspot 4G** (el móvil casi nunca bloquea 7844) o **ngrok/443**. NO uses localtunnel
para webhooks de Meta: su página interstitial rompe la verificación (GET del challenge).

Mientras el proceso cloudflared siga vivo, la URL se mantiene al reconectar (cambiar de red =
corte breve, misma URL); solo matarlo da URL nueva.

Claude Code: `cloudflared tunnel` lo bloquea el auto-mode classifier (ingress externo) → lo corre
el usuario, no el agente. Relacionado: [[meta-whatsapp-dev-sandbox-usar-test-number-no-business-de-prod]].
