---
title: tecnocloud
date: 2026-05-07
updated: 2026-08-07
tags: [cliente, tecnocloud, retell, voice, dokploy]
---

# Tecnocloud

Cliente de TuFacturaIA (Enterprise). Quiere su propio número WhatsApp para ingesta.
También tiene agente de voz Retell propio (Laura) para soporte técnico inbound.

## Estado

- **Org** activa en TuFacturaIA con plan Enterprise
- **15 facturas** emitidas en últimos 90d, 5 pendientes (33%)
- 0 proveedores con varianza alta (no recibe sugerencia antifraud)
- **Agente de voz Laura** (Retell) en producción para soporte L1, inbound al +34919935205

## Próximos hitos

1. **WhatsApp en TuFacturaIA** (LATER) — obtener `phone_number_id` de Meta Business → guardar en `organizations.settings.whatsapp.phone_number_id` → webhook override en n8n receptor v2
2. **PR #3 voice-webhook-tickets** (NEXT) — pendiente review Dani. Tras merge → smoke E2E con llamada real.

## Servidor DOKPLOYMANU — el Dokploy de Tecnocloud (07-ago-2026)

Host **`185.99.186.76`, puerto SSH 5251** (alias local `ssh tucrmia`, clave `~/.ssh/tucrmia_root`; documentado en 1Password, bóveda TUCRMIA). Proveedor distinto al de la tanda `185.47.13.x`, pero **misma contraseña root** — ver [[vps-dokploy-de-una-tanda-comparten-password-root]].

Ojo al alcance: aquí no solo vive lo de Tecnocloud. **20 contenedores**, entre ellos [[tucrmia|TuCRMIA]], un n8n de Agentesia, Chatwoot y notcaido. Un reboot los tira todos ~1 min, así que la ventana se acuerda con ellos.

- **07-ago**: parcheado (18 updates), kernel `5.15.0-174`, reiniciado, 20/20 arriba.
- El n8n de Agentesia no volvió solo tras ese reboot: **carrera con la overlay `dokploy-network`**, no su restart policy. Guardián systemd instalado y `enabled` (`/usr/local/bin/dokploy-restart-orphans.sh`, log en `/var/log/dokploy-restart-orphans/`), validado en sus dos ramas; **falta verlo en un reboot real**. → [[contenedor-que-no-vuelve-tras-reboot-dos-causas-que-se-confunden]]
- **Pendiente**: darlo de alta en `/agency/infrastructure` del portal — clave del monitor ya autorizada en el host, falta pegarla en el formulario. → [[agentesia]]
- Sin backups a Wasabi configurados; nunca se auditaron (`dokploy-backup-monitor` los cubre).

## Agente de voz Laura — Retell

- **agent_id**: `agent_add2e94a0f386f86243a9e80e6`
- **llm_id**: `llm_c32fb6e5ba5c6b493da0ba3f73ac` · modelo `gpt-5.4-mini` · `tool_call_strict_mode: true`
- **phone**: `+34919935205` (inbound)
- **Workflow n8n backend (tools)**: `aAfDL01MLPAOWfco` — "Retell Agent Tools - TECNOCLOUD"
  · Webhook: `https://n8ntecno.tecnocloud.es/webhook/retell-tecnocloud`
  · Tools: `buscar_FAQ` (RAG PGVector), `registrar_llamada` (Sheets + Gmail HTML a `incidencias@tecnocloud.es`)
  · OpenAI API key vía `$env.OPENAI_API_KEY` (movida de hardcode 2026-05-25)
- **Google Sheet de llamadas**: `1Jb6BR64IbkFCwk55m_1elAWAPSl9xNd2fBi1iwPP244` ("Registro TECNOCLOUD")
- **Personas internas conocidas** que clientes piden: Silvia, Dani, Carlos. Flujo rápido en el prompt pregunta motivo antes de derivar.

### Flujo "hablar con Silvia/Dani/Carlos" (2026-05-25)
Etapas obligatorias antes de disparar `registrar_llamada`:
1. Preguntar **motivo** ("¿para qué quieres hablar con [persona]?")
2. Pedir **nombre del cliente** (distinto de la persona solicitada)
3. Recién entonces ejecutar tool y despedir.

Lección: el LLM confundía PERSONA_SOLICITADA con NOMBRE_CLIENTE. Fix combinado:
- Precondiciones explícitas en `description` de la tool `registrar_llamada` (pesa más que el prompt).
- `tool_call_strict_mode: true`.
- `execution_message_description` neutralizado (no prometer "derivar" antes de tiempo).

### Resumen del email post-llamada
Generado en Code node "Registrar Llamada" vía gpt-4.1-mini con prompt que pide 4-8 frases
con datos concretos (mensaje de error literal, persona+motivo, pasos probados, estado final).
`max_tokens: 700`. Anteriormente se quedaba en 2-3 frases y se perdían detalles.

## Bloqueos / esperando a terceros

- Tecnocloud: facilitar phone_number_id de su Meta Business

## Links rápidos

- Org_id en Supabase: `8714c897-8e2e-472f-aa40-9f591510c88c`
- Retell dashboard agente: `agent_add2e94a0f386f86243a9e80e6`
- n8n: https://n8ntecno.tecnocloud.es
