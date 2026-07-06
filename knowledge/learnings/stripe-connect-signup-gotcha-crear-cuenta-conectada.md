---
title: "stripe connect: 'sign up for connect' al crear cuenta conectada = perfil de plataforma incompleto, no código"
date: 2026-07-05
source: claude-code-session
tags: [stripe, connect, pagos, gotcha]
---

`POST /v1/accounts {type:standard}` → 400 `"You can only create new accounts if you've signed up for Connect"`.
NO es un bug de código ni un tema v1-vs-v2. Es que la **cuenta plataforma** no ha completado el onboarding de Connect (`charges_enabled:false`, `dashboard_account_status:"restricted"`, `requirements.disabled_reason:"requirements.past_due"` — típicamente falta una persona con nombre/dirección/dob/email).

Pistas de diagnóstico (sin crear cuentas):
- El objeto de la cuenta plataforma con `"type":"standard"` + `"is_connected_v2_account":false` confirma que **v1 `type=standard` es lo correcto** (el asistente del dashboard usa `/v2/core/accounts` pero eso no obliga a migrar).
- El wizard "elige modelo de negocio" (Plataforma vs Marketplace) NO completa el perfil — la franja rosa "tarea requerida vencida" sí es lo que hay que cerrar.

Testing local de Connect:
- `stripe listen --forward-connect-to localhost:3000/...` hace de receptor; NO hace falta registrar un webhook.
- `account_links` exige `return_url` **https** (rechaza `http://localhost`) → usar la URL de prod aunque el retorno caiga ahí.
