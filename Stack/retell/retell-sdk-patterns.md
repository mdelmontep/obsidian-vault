---
title: retell voice SDK — patrones y reglas
date: 2026-04-20
source: claude-md-migration
tags: [retell, voice, sdk, webhooks]
---

# Stack Retell / Voice SDK

- **`RetellWebClient` extiende `eventemitter3`** — tiene `.off(event, handler)`. Los listeners registrados en `useEffect` se acumulan entre remounts (HMR en dev o Strict Mode) si no los limpias. Guardar handlers como referencias con nombre y llamar `client.off(...)` en el cleanup:
  ```tsx
  const onStarted = () => { ... }
  client.on("call_started", onStarted)
  return () => client.off("call_started", onStarted)
  ```
- **Pre-check de micrófono con `navigator.mediaDevices.getUserMedia({ audio: true })`** antes de `startCall` → distingue `NotAllowedError` (permiso denegado) y `NotFoundError` (sin micro) con mensajes útiles para el usuario, en vez del error genérico del SDK que llega después
- **Timeout de seguridad en estado `connecting`** (10-15s) — si Retell no dispara `call_started`, el estado queda colgado indefinidamente. El orb late eterno y el usuario no entiende qué pasa
- **Singleton lazy del cliente** (`getRetellClient()` con try/catch que instancia en primer uso) evita crashes al cargar el módulo si el navegador no soporta WebRTC o mediaDevices
- **Normalizar la respuesta del webhook de Retell** — puede venir como `access_token`, `accessToken` o `token` según cómo lo construyas en n8n. Hacer `data.access_token ?? data.accessToken ?? data.token`
- **API de Retell — endpoints separados**: `PATCH /update-agent/{agent_id}` para config del agente (voz, webhook), `POST /update-retell-llm/{llm_id}` para prompt y tools. Son dos llamadas distintas
- **`parameter_type` en custom tools debe coincidir con n8n**: si n8n lee `$json.body.args.X` (JSON anidado), la tool debe usar `"json"`. Con `"form"`, n8n recibe `body['args[name]']` en vez de `body.args.name` — la reserva falla silenciosamente
- **Checklist antes de subir prompt Retell → n8n**:
  1. URLs de tools apuntan al dominio correcto (verificar DNS — EasyPanel y dominio custom pueden ser IPs distintas)
  2. Cada tool referenciada en el prompt existe en `general_tools` (ej: `transfer_call`)
  3. Nombres de parámetros coinciden con los `Edit Fields` / `Set` del workflow n8n
  4. El workflow destino está activo y no archivado
  5. `parameter_type` es `"json"` si n8n espera `body.args.X`
